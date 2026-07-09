# Mindmap guide (Phase 2 Step 3)

One single-page visual mindmap combining 2-3 related topics, built as a self-contained
HTML file at `topics/<slug>/mindmap.html` and published via the `Artifact` tool. The point
is a memorable visual, not a text outline — if it could just as well be a bullet list, it
hasn't done its job.

## Process

1. **Pick 2-3 related topics** to study together — prefer topics that are already being
   learned around the same time and share some real connection (not just "the same
   exam").
2. **Extract only the key concepts/facts** actually needed on the page — this is a memory
   aid, not a second copy of the layered notes. Ruthlessly cut anything not essential.
3. **Draft notes for all topics at once**, side by side, so genuine comparisons surface
   naturally rather than being bolted on afterward.
4. **Find the central connection** between the topics before drawing anything — is it a
   cause/effect chain, a shared location/structure, a shared process with different
   stages, a spectrum from one extreme to the other? Write this connection down in one
   sentence first.
5. **Pick one visual metaphor for the center** that represents that connection — a
   diagram, a funnel, a flowchart, a spectrum, a cycle. Be creative here; an unusual visual
   is what makes it stick. This goes in the literal center of the page.
6. **Arrange the remaining key concepts around that center**, connected by lines/arrows
   back to it or to each other. Target **90% visual** — shapes, icons, spatial grouping,
   color-coding by topic — with **one or two words max** per node. If a node needs a full
   sentence, it belongs in the layered notes, not here.

## HTML implementation notes

- Self-contained single file: inline `<style>`, no external resources (matches the
  Artifact tool's CSP — no CDN scripts/fonts/images).
- Use CSS (flexbox/grid/absolute positioning within a bounded container, SVG or styled
  `<div>`s for connecting lines/shapes) to build the actual spatial layout — this should
  render as a real one-page diagram, not a scrolling document.
- Fit on one viewport where reasonably possible; if genuinely dense, it's fine to require
  scrolling inside a bounded `overflow: auto` container rather than shrinking text past
  legibility.
- Support both light and dark viewing per the Artifact tool's theming conventions
  (`prefers-color-scheme` plus `[data-theme]` overrides) so it's comfortable to review at
  any time of day.
- **Language/direction**: set `<html lang="he" dir="rtl">`, `lang="en" dir="ltr">`, or the
  dominant-language default with `dir="auto"` spans for embedded foreign terms, per
  [language.md](language.md). Mirror any inherently directional visual (arrows, funnels,
  timelines) to match the page's `dir` so it reads the natural way for that language.
- Pick a stable favicon emoji for mindmap artifacts (e.g. 🧠) and keep it consistent across
  topics/redeploys so the user can spot mindmap tabs at a glance.

## Anti-patterns to avoid

- A plain bullet-point outline with boxes drawn around it — that's not visual, it's text
  wearing a diagram costume.
- Cramming every fact from the layered notes onto the map — defeats the "key concepts
  only" point and makes nothing stand out.
- Skipping the central-connection step and just placing topics side by side with no
  unifying idea — the connection is what makes it memorable, not just proximity.
