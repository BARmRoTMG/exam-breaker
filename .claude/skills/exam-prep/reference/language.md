# Language handling (Hebrew / English / mixed)

Course material can be all-Hebrew, all-English, or mixed — even within a single topic.
Never translate source material by default; work in whatever language the topic's
material is in, and quiz/discuss that topic in the same language. Detection and
confirmation happen once per topic during Phase 1, stored in `state.json` as
`topics[].language`.

## Detecting language

During the Phase 1 folder scan, sample a few lines of text from each topic's source
files (filenames plus actual extracted content, not just filenames — a Hebrew-titled deck
can have English-only slide content and vice versa):

- Only Hebrew characters (`֐-׿`) present -> `"he"`.
- Only Latin script present -> `"en"`.
- Both appear in meaningful proportion (not just an isolated acronym or formula) ->
  `"mixed"`.

Always show the detected language per topic to the user during Phase 1 confirmation
rather than silently committing to it — misdetection is easy on short filenames.

## Where this matters

- **Conversational quizzing** (Phase 2 Steps 1/4, Phase 3 review): ask and expect answers
  in the topic's language. For `"mixed"` topics, mirror whatever mix the source material
  itself uses rather than forcing one language.
- **Generated markdown notes** (`skim-notes.md`, `layered-notes.md`, `question-sample.md`,
  `red-list.md` entries): write in the topic's source language. Markdown has no direction
  metadata, so no extra handling is needed there beyond just writing correctly.
- **`frequency-tally.csv`**: write UTF-8 **with BOM**. A plain UTF-8 CSV without a BOM
  renders Hebrew as mojibake when double-clicked open in Excel on Windows (Excel's CSV
  auto-detect defaults to the system codepage, not UTF-8, unless a BOM signals it). Use
  `scripts/extract_text.py`'s `write_csv_utf8_bom` helper, or when writing the CSV directly
  via the Write tool, prepend the BOM character `﻿` to the file content before the
  header row.
- **`mindmap.html` Artifacts** (Phase 2 Step 3): set direction at the page level —
  `<html lang="he" dir="rtl">` for `"he"` topics, `<html lang="en" dir="ltr">` for `"en"`,
  and for `"mixed"` topics use the dominant language's `dir` at the page level with
  `dir="auto"` (or `unicode-bidi: plaintext` in CSS) on any inline `<span>` holding an
  embedded term in the *other* script — e.g. an English acronym inside Hebrew body text,
  or a Hebrew term quoted inside English notes — so bidi reordering doesn't scramble it
  visually. Mirror layout elements that have implicit direction (arrows, timelines) to
  match the page-level `dir` so flow reads naturally.
- **`extract_text.py`**: always read/write UTF-8 explicitly. Windows' default codepage for
  Hebrew locales (cp1255) silently mangles text if Python falls back to a locale-default
  encoding instead of UTF-8 — this fails quietly (wrong characters, not an exception), so
  it's worth double-checking output on any Hebrew-sourced file after extraction.

## What NOT to do

- Don't auto-translate Hebrew material to English (or vice versa) to "normalize" it before
  taking notes — this loses fidelity to how the exam actually phrases things and defeats
  matching the source's own terminology, which is often what's tested.
- Don't assume one language for a whole exam just because most topics share it — check
  per-topic, since one lecturer's slides in an otherwise-Hebrew course are a common case
  of a lone `"en"` or `"mixed"` topic.
