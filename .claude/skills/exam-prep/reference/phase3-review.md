# Phase 3 — Review (retention)

Two modes: targeted spaced review of red-list items, and daily mixed sessions. Both draw
on `exams/<exam-name>/.examprep/red-list.md`, `review-schedule.md`, and `state.json`.

## Spaced intervals

Fixed schedule, in days from the date an item was last answered correctly:
`1, 3, 7, 14, 30`. A red-list item starts at interval `1` the moment it's logged (see
Phase 2 Step 4). Store each item's current interval index and `nextReviewDue` date in
`review-schedule.md`, one line per item, referencing the same identifier used in
`red-list.md`:

```
- <date-logged> | <topic> | <question-short> | interval=1 | nextDue=<date>
```

On each review of an item:

- **Correct** -> advance to the next interval in the list (cap at `30`; once an item
  clears at the `30`-day interval, mark it `resolved` in `red-list.md` rather than
  scheduling further and decrement `redListCount`/`redListTotal` in `state.json`).
- **Incorrect** -> reset to interval `1` and log it as a *new* mistake occurrence in
  `red-list.md` (don't overwrite the old entry — a recurring miss on the same concept is
  itself useful signal, and should bump it up in priority for the next mixed session).

Per-topic `nextReviewDue` in `state.json` should reflect the **earliest** due date among
that topic's open red-list items, so a quick scan of `state.json` alone tells you what's
overdue.

## Targeted spaced review

1. Compute what's due: any red-list item (or topic) whose `nextReviewDue` is today or
   earlier.
2. Quiz those first, in the item's topic's language (see [language.md](language.md)).
3. Re-stamp intervals per the rule above immediately after each answer, not batched at the
   end — if the session gets cut short, whatever was already answered should have correct
   state.
4. If nothing is due, say so plainly rather than manufacturing a review session — don't
   pad with unrelated topics under this mode; that's what the mixed session is for.

## Daily mixed-question session

1. Pull a cross-topic question set: bias toward P1/P2 topics and toward topics with
   currently-open red-list items, but don't exclude everything else — the point is
   interleaved retrieval practice across the whole syllabus, not just the weak spots.
2. Run it conversationally like Phase 2 Step 4: any new mistake goes on the red list with
   the same logging format, any topic that was previously resolved but gets missed again
   gets reopened.
3. This mode doesn't require anything to be "due" — it's meant to run daily regardless of
   the spaced schedule.

## Keep in mind

The red list only works if it's used aggressively — err toward logging a mistake (even a
near-miss or a right-answer-wrong-reasoning) rather than letting it slide because the
final answer happened to be correct.
