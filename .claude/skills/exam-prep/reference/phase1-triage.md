# Phase 1 — Triage

Goal: for every syllabus topic, know (a) how often it's actually examined, and (b) whether
it's a personal weakness or strength — then place it in the P1-P4 grid so effort goes
where it pays off most.

## Step 1 — Build the topic list

Prefer a syllabus file in `raw/` if one exists (look for filenames like
"syllabus", "outline", "תוכנית לימודים", "נושאים"). If none exists, derive the topic list
from past-paper section headers and lecture deck titles, then show the derived list to the
user for confirmation before tallying anything — a wrong topic list poisons everything
downstream.

## Step 2 — Frequency: common or uncommon

Choose depth based on how much past-paper material actually exists in `raw/`:

- **Few past papers (roughly ≤3) or none**: skim what's there directly, and explicitly ask
  the user for any hints from teachers or older students about what's commonly tested.
  Record the source of each frequency judgment (paper-based vs. hearsay) in
  `triage/frequency-tally.md` notes so it's clear later which topics have real data behind
  them.
- **Many past papers (roughly ≥4)**: tally properly. For each past paper, count how many
  questions touch each topic (a question can count toward more than one topic). With more
  than ~5 papers, fan this out: one `general-purpose` Agent per paper (or small batch of
  papers), each returning a structured `{topic: count}` map for that paper; aggregate the
  results yourself into one table. `.pptx`/`.docx` papers need
  `scripts/extract_text.py` run first.
- Write results to **both**:
  - `triage/frequency-tally.csv` — rows = topics, columns = one per past paper (by
    year/name) plus a `total` column. UTF-8 with BOM (see
    [language.md](language.md) if any topic is Hebrew/mixed).
  - `triage/frequency-tally.md` — same data as a readable markdown table.
- Look for patterns worth calling out to the user directly (not just left in the table):
  topics that appear in *every* paper, topics whose question count is trending up/down
  across years, topics that only ever appear as one small sub-question vs. a full
  question.
- Classify each topic `common` or `uncommon` based on the tally (or the skim+hints
  judgment for the low-data path) — use a sensible relative threshold (e.g. top half of
  topics by total count) rather than an absolute number, since "common" is relative to
  this exam's own topic spread.

## Step 3 — Strength: weak or strong

Ask the user directly per topic (fastest and most reliable — self-assessment plus any
past exam/quiz scores they can point to). If the user has prior graded work in `raw/`,
use per-topic performance on it as corroborating evidence, but the user's own read on
where they're weak takes priority over inferred data.

## Step 4 — Build the triage table

Place every topic in exactly one quadrant based on `frequency` x `strength`, and write it
to `triage/triage-table.md` as a 2x2 grid (rows = common/uncommon, columns = weak/strong)
listing every topic in its cell:

| | Weak | Strong |
|---|---|---|
| **Common** | **P1** — highest priority | P2 |
| **Uncommon** | P3 | P4 — lowest priority |

Update `state.json`: set `frequency`, `strength`, and derived `priority` for every topic.
P1 topics are the ones that get the full Phase 2 Step 3 (layered notes + mindmap)
treatment; P2-P4 typically stop at Step 2 unless the user asks otherwise.
