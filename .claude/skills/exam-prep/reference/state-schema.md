# state.json schema

Lives at `exams/<exam-name>/.examprep/state.json`. This is the single source of truth for
resuming work — read it fully before doing anything, and rewrite it (not append) after
every session.

```json
{
  "examName": "thermo-101",
  "examDate": "2026-08-20",
  "rawScanAt": "2026-07-09",
  "topics": [
    {
      "slug": "first-law",
      "name": "First Law of Thermodynamics",
      "language": "en",
      "frequency": "common",
      "strength": "weak",
      "priority": "P1",
      "phase2Step": 2,
      "lastReviewed": "2026-07-05",
      "nextReviewDue": "2026-07-12",
      "redListCount": 3
    }
  ],
  "redListTotal": 7,
  "notes": ""
}
```

Field notes:

- `slug` is the folder name under `.examprep/topics/<slug>/` — kebab-case, derived from
  `name`, ASCII-transliterated if the topic name is in Hebrew (the `name` field itself
  stays in the original language; only the folder slug is transliterated for filesystem
  safety).
- `language`: `"he"`, `"en"`, or `"mixed"` — see [language.md](language.md). Set once
  during Phase 1 scan, editable if the user corrects it.
- `frequency`: `"common"` or `"uncommon"` — from the Phase 1 tally.
- `strength`: `"weak"` or `"strong"` — from user self-assessment or past performance.
- `priority`: `"P1"` (common+weak), `"P2"` (common+strong), `"P3"` (uncommon+weak), `"P4"`
  (uncommon+strong) — derived directly from `frequency` x `strength`, don't set it
  independently.
- `phase2Step`: `0` = not started, `1`-`4` = last completed step for this topic. P2-P4
  topics stop meaningfully at step 2 (skim) per the methodology — step 3 (layered
  notes/mindmap) is P1-only unless the user explicitly asks for a non-P1 topic too.
- `lastReviewed` / `nextReviewDue`: spaced-repetition dates, ISO `YYYY-MM-DD`. Absent
  until the topic has been through at least one Phase 2 Step 4 or Phase 3 session.
- `redListCount`: mistakes currently open for this topic (mirrors count of this topic's
  entries in `.examprep/red-list.md` that aren't yet resolved).

Keep `topics` sorted by priority (P1 first) so a quick read of the file already surfaces
what matters most.
