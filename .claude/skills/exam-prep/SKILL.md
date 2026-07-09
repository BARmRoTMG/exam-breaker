---
name: exam-prep
description: Run a structured 3-phase exam-prep workflow (Triage -> Speed-Learn -> Review) over a folder of exam material (past papers, lecture PDFs/pptx/docx, summaries). Tracks per-topic priority, generates a frequency-tally spreadsheet and triage table, runs the 4-step speed-learn cycle per topic (question sampling, skim, layered notes + visual mindmap, full question sessions), and drives spaced review off a persistent "red list" of mistakes. Works fully in Hebrew, English, or mixed-language material. Use whenever the user wants to study for an exam using material in exams/<exam-name>/raw/, asks to triage/tally past papers, learn/skim/review a topic, or run a red-list / spaced-review session.
---

# Exam Prep

Runs the user's exam-prep methodology against `exams/<exam-name>/raw/`. Owns persistent
state so work resumes correctly across many separate conversations. Detailed procedures
live in `reference/*.md` and are loaded only when that phase actually runs (progressive
disclosure) — this file is just the dispatcher.

## 0. Resolve the exam and load state

1. Determine `<exam-name>`: from an explicit argument, or by listing subfolders of the
   `exams/` root (siblings of `.claude/`) and asking the user if more than one exists and
   none was named. Each exam lives at `exams/<exam-name>/` with raw material in
   `raw/` inside it.
2. Read `exams/<exam-name>/.examprep/state.json` if it exists. If it does not:
   - Create `.examprep/`, `.examprep/triage/`, `.examprep/topics/`.
   - Scan `raw/` (list all files; look for anything syllabus-like).
   - Detect language per likely topic/file: `he`, `en`, or `mixed` (see
     [reference/language.md](reference/language.md)) — confirm with the user rather than
     silently guessing.
   - Write an initial `state.json` per the schema in
     [reference/state-schema.md](reference/state-schema.md), with an empty/placeholder
     topic list, and ask the user to confirm or correct the topic list before proceeding.
3. `.pptx` / `.docx` files anywhere under `raw/` need text extraction before they can be
   read for content — use `scripts/extract_text.py` (see that file's header for usage and
   the required `pip install` if the packages are missing). PDF and `.md`/`.txt` files are
   read directly.

## 1. Decide what to run

Figure out the requested phase/step from the user's message (e.g. "triage this",
"phase 2 step 3 for thermodynamics", "review today", "daily mixed session"). If it's
ambiguous, use `state.json` to find the most sensible next action (e.g. no triage table
yet -> Phase 1; a P1 topic stuck mid-speed-learn -> resume that step; red-list items are
due -> Phase 3) and confirm with the user before starting.

Dispatch:

| Request | Read |
|---|---|
| Triage / tally past papers / build P1-P4 table | [reference/phase1-triage.md](reference/phase1-triage.md) |
| Learn / skim / mindmap / question session for a topic | [reference/phase2-speedlearn.md](reference/phase2-speedlearn.md) |
| Review / red list / daily mixed session | [reference/phase3-review.md](reference/phase3-review.md) |
| Building the Phase 2 Step 3 mindmap specifically | [reference/mindmap-guide.md](reference/mindmap-guide.md) (linked from phase2 too) |
| Any per-topic or per-mistake language handling | [reference/language.md](reference/language.md) |
| Writing/updating `state.json` | [reference/state-schema.md](reference/state-schema.md) |

## 2. After doing the work

- Update `state.json` (topic status, priority, dates, red-list count) to reflect exactly
  what was completed.
- Append one line to `exams/<exam-name>/.examprep/session-log.md`: date, what ran, key
  outcome (e.g. "Phase1 triage: 14 topics tallied across 6 papers" or "Phase2 Step4
  thermodynamics: 12/15 correct, 3 new red-list items").
- Never leave state stale relative to what actually happened in the conversation — the
  next invocation (possibly days later, possibly a fresh conversation) depends on it being
  accurate.

## Fanning out heavy reading work

When a step requires reading/tallying across many files (e.g. Phase 1 tallying 8+ past
papers, or Phase 2 Step 1 sampling questions across several question banks), use the
`Agent` tool with `general-purpose` subagents, one per file or small batch, run in
parallel, rather than reading everything serially in the main conversation. Aggregate
their structured results yourself. For a handful of files, just read them directly —
delegation overhead isn't worth it below roughly 5 source files.
