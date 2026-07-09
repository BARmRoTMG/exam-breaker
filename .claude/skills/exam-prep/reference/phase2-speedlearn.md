# Phase 2 — Speed-Learn (per topic)

Run one topic at a time. Track progress via `state.json`'s `topics[].phase2Step`
(0 = not started, 1-4 = last completed step). All output for a topic lives under
`.examprep/topics/<slug>/`.

## Step 1 — Initial questions (diagnostic + question-type discovery)

1. Gather as many real questions on this topic as `raw/` supports: past-paper questions,
   any question bank, textbook end-of-chapter questions. For topics with material spread
   across many sources, fan out with `Agent` (`general-purpose`, one per source) to pull
   candidate questions in parallel, then merge.
2. Write the pulled questions to `topics/<slug>/question-sample.md`, and for each one tag
   the **question type** you observe: `fact` (recall a definition/fact), `process` (recall
   or apply a procedure/steps), or `calc` (numeric/derivation). This classification is the
   point of the step — it tells you *how* this topic is actually examined, which drives
   how Step 3 should be focused (e.g. a calc-heavy topic needs worked examples in layered
   notes, not just definitions).
3. Have the user attempt 5-10 of these live in conversation, in the topic's language (see
   [language.md](language.md)), before you reveal answers or explanations — this is a
   genuine diagnostic of current level, not a teaching moment yet.
4. Note the observed question-type mix and rough diagnostic performance in
   `question-sample.md`'s header.

## Step 2 — Skim (≈10 minutes, all priorities)

Using the single best available summary or lecture deck for the topic (prefer an explicit
"summary"/"high-yield" file if one exists; otherwise the most concise deck) plus, if the
user supplies one, a YouTube link — capture in `topics/<slug>/skim-notes.md`:

1. **What the topic is about** — one or two sentences, plain language.
2. **What sections it splits into** — the sub-structure as the source material presents
   it.
3. **Which sections link to which exam questions** — cross-reference against
   `question-sample.md` from Step 1: which sub-section does each sampled question actually
   draw on? This is what makes the skim targeted rather than generic.

Set `phase2Step` to `2` in `state.json`. For P2-P4 topics, this is typically the last step
unless the user explicitly asks to go further.

## Step 3 — Deep learning (P1 topics only)

Confirm the topic is P1 in `state.json` before running this step; if it isn't, check with
the user that they actually want the full treatment on a non-P1 topic before proceeding.

1. **Layered read** — go through the source material three times, writing each layer
   into `topics/<slug>/layered-notes.md` under its own heading:
   - *Basics* — the bare minimum definitions/facts.
   - *General concepts* — how the basics fit together, why they matter.
   - *Details* — the fine print, edge cases, exact numbers/derivations.
2. **Compare** — add a short section comparing this topic against 1-2 related topics
   already covered (similarities, differences, common confusions) — this is what actually
   builds durable understanding, not just re-reading.
3. **Mindmap** — build a single-page visual mindmap combining this topic with 1-2 related
   ones, following [mindmap-guide.md](mindmap-guide.md) exactly (central visual metaphor,
   90% visual, one-two words per node). Write it as `topics/<slug>/mindmap.html` and
   publish it with the `Artifact` tool. Set page direction per
   [language.md](language.md) based on the topics' language.

Set `phase2Step` to `3`.

## Step 4 — Full question session

1. Run a full, timed-feel question session on this topic in conversation (mix of question
   types identified in Step 1, weighted toward whatever type dominates this topic's real
   exam questions).
2. For every question the user gets wrong, immediately append an entry to
   `exams/<exam-name>/.examprep/red-list.md`:
   `- [<date>] <topic> — Q: <question> — Why wrong: <misconception, in the user's words if
   possible> — Status: open`
   Increment `redListCount` for this topic and `redListTotal` in `state.json`, and stamp a
   `nextReviewDue` of tomorrow (1-day interval — see
   [phase3-review.md](phase3-review.md)) for that specific mistake.
3. While answering, push the user to think broader than the literal question — ask a
   quick follow-up connecting it to the concept behind it, not just marking right/wrong.
4. Immediately after the session (not deferred to later), for each wrong answer: do a
   mini layered pass on just that specific concept, and a quick compare against the
   related concept it's most often confused with. This closes the loop while it's fresh.

Set `phase2Step` to `4`. Update `lastReviewed` for the topic to today.
