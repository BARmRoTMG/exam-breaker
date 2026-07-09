# Exam Prep

This folder holds one subfolder per exam/course. A Claude Code skill
(`.claude/skills/exam-prep/`) runs a structured study workflow over each exam's
material: triage which topics matter most, speed-learn them, then keep them
retained with spaced review. It works fully in Hebrew, English, or a mix of
both — per topic, not per exam.

## 1. Set up an exam folder

Create a subfolder for the exam and put your material inside a `raw/`
directory:

```
exams/
  <exam-name>/
    raw/
      syllabus.txt              (or any file with the topic list)
      past-paper-2024.pdf
      past-paper-2023.pdf
      lecture-slides.pptx
      summary.docx
      ...
```

- **PDF** and **.txt/.md** files are read directly — no extra steps.
- **.pptx / .docx** files need a one-time text extraction pass before Claude
  can read their content:

  ```
  pip install python-pptx python-docx
  python .claude/skills/exam-prep/scripts/extract_text.py "exams/<exam-name>/raw" --recursive
  ```

  This writes a `<file>.extracted.txt` next to each source file. Re-run it any
  time you add new slides/docs — it skips files whose extracted text is
  already up to date.

You don't need a syllabus file — if none exists, the skill derives the topic
list from past-paper headings and lecture titles and asks you to confirm it.

## 2. Start with triage

In Claude Code, from this folder, just ask in plain language, e.g.:

> Triage `<exam-name>`

This scans `raw/`, tallies how often each topic is actually tested across
your past papers (or skims + asks for teacher/older-student hints if you only
have a couple of papers), asks you which topics feel weak vs. strong, and
writes:

- `exams/<exam-name>/.examprep/triage/frequency-tally.csv` + `.md`
- `exams/<exam-name>/.examprep/triage/triage-table.md` — your P1–P4 grid

## 3. Speed-learn topic by topic

Ask for a specific topic and step, e.g.:

> Run phase 2 step 1 for `<topic>`
> Skim `<topic>` for me
> Do the full learning pass on `<topic>` (P1 topics only — layered notes + mindmap)
> Run a full question session on `<topic>`

Each step writes into `exams/<exam-name>/.examprep/topics/<topic-slug>/`.
Step 3's mindmap is published as a visual HTML page (via the Artifact tool),
right-to-left automatically if the topic is in Hebrew.

## 4. Review

> Review `<exam-name>` today
> Run a daily mixed session for `<exam-name>`

Every mistake gets logged to `.examprep/red-list.md` and scheduled for spaced
review (1/3/7/14/30-day intervals) in `.examprep/review-schedule.md`. Just ask
for a review whenever you sit down to study — the skill tells you what's
actually due.

## Notes

- Nothing in `raw/` is ever modified — all generated output lives in the
  sibling `.examprep/` folder, safe to delete and regenerate if you ever want
  to start over on an exam.
- Everything resumes across sessions: `state.json` inside `.examprep/` tracks
  where you left off per topic, so you can pick any exam back up days later.
- You don't need to remember the exact commands above — describing what you
  want ("let's triage physics", "quiz me on entropy") is enough; the skill
  figures out the right phase/step from `state.json` and asks if it's
  ambiguous.
- Full methodology details live in `.claude/skills/exam-prep/reference/` if
  you want to read or tweak how any phase works.
