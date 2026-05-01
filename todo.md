# Python Game Dev — Course Modernization TODO

> Forward-looking next-chat steering. **Full history, decisions, review items, and resolved questions live in `status.md`** — read it first if landing fresh.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Current state

- Phases 1–6: ✅ done. Phase 6 = 23 SVGs shipped (#23 `pygame-primitives.svg` built chat 20 from-scratch — first genuine clean-slate Phase 7 build since #20, no prior interrupted-chat artifact unlike #21 / #22; render-check + optional getBBox gate pending, deferred to chat 21. #22 `behavior-tree.svg` built in interrupted chat-19 attempt + render-checked clean chat 20 with inline-SVG `getBBox()` overflow check returning 0 overflows / 53.6 px clearance. #21 `screenshake-decay.svg` built chat 17 + render-checked clean chat 18 with bottom-strip overflow fix). #17/#18/#19 fully render-checked clean through chat 16. #21 (chat 18) and #22 (chat 20) review items dischargeable. #20 (chat 14) and #23 (chat 20) review items still pending eyeball.
- Phase 7: 🔄 7/15 lessons wired through chat 20 (6 render-checked clean + SVG #23 `pygame-primitives.svg` awaiting render-check). 8/15 deferred pending new SVGs #24–#31.
- Phases 8–9: ⏳

---

## Next chat — render-check SVG #23 (and optionally build SVG #24)

Chat 20 closed two milestones: (a) SVG #22 `behavior-tree.svg` render-check at iframe-simulated 380×820 cleared all five verification points (`#behaviorCanvas` `display: none` despite inline `inline-block`; Phase 6 figure + main canvas-fallback load post eager-decode; tree-canvas fallback correctly visibility-gated by `#treeView` toggle; inline-SVG `getBBox()` 0 overflows / 53.6 px clearance) — ships clean. (b) SVG #23 `pygame-primitives.svg` built from scratch (3×2 grid of pygame's six drawing primitives, color-tinted signatures: teal=position, amber=size, blue=line-end, red=arc-angles), wired into `pygame_basics_drawing.html` (Phase 6 figure before `Interactive Shape Drawing Demo` h2 + canvas-fallback wraps on both `#shapesCanvas` and `#spriteCanvas`), catalog flipped. Full narratives in `status.md` → *Phase 6 progress (chat 20 — SVG #23 build: pygame-primitives.svg)* and *Phase 7 progress (chat 20 — SVG #23 build)*.

### Step 1 — SVG #23 render-check (build-in-N / check-in-N+1 pattern, third instance)

Follow chat-18 / chat-20 iframe-simulation technique against `localhost:5503/pygame_basics_drawing.html?v=chat21rc<timestamp>` at 380×820. Five verification points to clear:

1. **`#shapesCanvas` mobile hiding** — the canvas tag has no inline `display:` attribute (clean from-scratch lesson, no inline-display landmine); the global `canvas { display: none !important; }` rule from chat-15 hardening should hide it cleanly. Verify computed `display: none`.
2. **`#spriteCanvas` mobile hiding** — same as above; both canvases sit inside `<div style="...text-align: center;">` ad-hoc styled divs, NOT `.canvas-wrapper` divs (mirrors `pygame_basics_game_loop` chat-15 finding — global rule still applies). Verify computed `display: none`.
3. **Phase 6 figure renders cleanly** — `<figure class="svg-wrapper">` between Drawing Polygons code block and `<h2 id="interactive-shape-drawing-demo">`. Force-eager + decode the img if probe timing is uncertain (chat-15/18/20 lazy-load finding). Alt text intact (~570 chars).
4. **Both canvas-fallback figures render** — `<figure class="canvas-fallback">` after each `<canvas>` at `display: block` on mobile, with their imgs loaded post-decode. Mobile users see the SVG 3× in this lesson per V1 catalog limitation — expected, accepted (open-question #6 chat-14 resolution).
5. **Bottom-strip text fits inside viewBox** — run the chat-20 inline-SVG `getBBox()` overflow check (see step 2 below). Programmatic + visual gates both required.

### Step 2 (optional but recommended) — programmatic getBBox overflow check before/during render-check

The chat-20 SVG #23 build narrative flagged **cell 4 `line` signature** as borderline-tight: `line(surface, color, start, end, width)` is 39 chars at ~5.4 px/char monospace = ~211 px sitting in a 224 px cell with text-anchor=middle, leaving ~6.5 px each side. Cell 5 ellipse (`ellipse(surface, color, (x, y, w, h))` at 38 chars) is similarly tight. Walk all `<text>` elements via `fetch` + `DOMParser` + off-screen probe div + `getBBox()`, comparing each text right edge against (a) its parent cell rect right edge for per-cell signatures, (b) viewBox right edge x=720 for bottom-strip lines. Report any overflow > 0.5 px. If any cell signature overflows, fix in source (likely abbreviate the arg name or drop one of the modifier args from the displayed signature) before render-check.

### Step 3 (if budget allows) — build SVG #24

If chat-21's tool budget has room after render-check + any source-level fixes, pick up a Phase 7 SVG. Two candidates carry forward from chat-19's original list (since #23 was the third):

1. `polish_difficulty.html` → `difficulty-curves.svg` (3 sub-charts: linear ramp / plateau / DDA) — chart-heavy, mirrors easing-curves and utility-response-curves precedents, build_concept already detailed in catalog.
2. `polish_sound.html` → `sound-layers.svg` (4 stacked audio tracks: music / ambient / SFX / UI) — characteristic-waveform diagram, novel territory but small surface area.

Or pick from any of the remaining 8 deferred lessons in `support/phase7-canvas-fallback-catalog.json` — all have `build_concept` sketches.

### Standard Phase 7 pipeline reminder

`grep -l 'svg-wrapper'` the target → **check `images/components/<svg>.svg` doesn't already exist on disk** (chat-17 + chat-19 hard-won lesson; chat 20 was the third Phase 7 build and the first genuine clean-slate one) → read lesson + refine `build_concept` from `support/phase7-canvas-fallback-catalog.json` → build SVG in `images/components/` → insert as Phase 6 figure (convention B) → wrap canvas with canvas-fallback → flip catalog status `needs_new_svg` → `reuse (built chat <N>)` → **save status.md updates as soon as the build is locked in, even before render-check** (chat-19 hard-won lesson — make disk state self-documenting in case of conversation interruption) → **phone-width render-check at `localhost:5503` via iframe simulation** (chat-18/20 technique; can be tail-end task this chat or leading task next chat per the established "build in chat N, render-check in chat N+1" pattern from chats 17→18, 19→20, and now 20→21). **Optional new step:** programmatic inline-SVG `getBBox()` overflow check (chat-20 addition) before declaring source-level done.

### Optional deeper context (only if something here is unclear)

This todo is intended to be self-sufficient. **Don't default-read `status.md`** — it's deep history, not required reading. Pull individual sections only on demand if something specific is unclear:

- *Phase 6 progress → Decisions locked / Visual language / Recurring SVG conventions* in `status.md` — palette + theming pattern + accessibility scaffolding. **Alternative:** any recent `/images/components/<svg>.svg` (e.g. `behavior-tree.svg`, `screenshake-decay.svg`, `easing-curves.svg`) is a self-contained reference for the same conventions — the visual language is encoded inline in each file's `<style>` block.
- *Phase 6 progress (chat 20 — SVG #23 build: pygame-primitives.svg)* in `status.md` — full design narrative for the SVG you'll be checking, including the borderline `line` signature width-tightness flag (the explicit reason to run the getBBox check).
- *Phase 6 progress (chat 20 — SVG #22 render-check closure + inline-SVG overflow check)* in `status.md` — the most recent render-check precedent + the new programmatic overflow tool. Use as reference for both the iframe-simulation technique and the inline-SVG `getBBox()` check.
- *Phase 6 progress (chat 18 — SVG #21 render-check + bottom-strip overflow fix)* in `status.md` — the precedent overflow case (monospace-driven, ~180 px past viewBox edge), motivating example for the new programmatic check.
- *Phase 7 progress chats 12 / 13 / 14 / 15 / 17 / 18 / 19 / 20* in `status.md` — chat-by-chat Phase 7 history.
- *Open follow-ups on shipped SVGs* in `status.md` — pending eyeball items for SVG #20 `game-loop-cycle.svg` (chat 14) and SVG #23 `pygame-primitives.svg` (chat 20).

### Pre-build checklist (chat-17 + chat-18 + chat-19 + chat-20 hard-won lessons)

1. `grep -l 'svg-wrapper'` the target lesson — pre-staged figure markup may already dictate filename, layout, or labels; existing alt text = spec.
2. **Check `images/components/<svg>.svg` doesn't already exist on disk.** Now confirmed twice (chat 17 → #21, chat 19 → #22; both closed cleanly chat 18 / chat 20) that interrupted chat attempts may have shipped artifacts that survived. Quick check: `read_text_file --head 3 <path>`. If the file exists, also check the target lesson for pre-staged figure markup and the catalog JSON for an updated status — both may have been flipped before the prior chat was interrupted.
3. **Run a text-overflow sanity check** before declaring an SVG done. **Source-level estimate:** any text using `text-anchor: start` (the default) needs its rendered width estimated against the SVG viewBox right edge, especially long monospace lines (~6.3 px/char at 10.5 px); sans-serif at the same point size is narrower (~5.5–6 px/char) so has more margin. **Programmatic check (chat-20 addition):** `fetch` the SVG → `DOMParser` parse → mount inline in an off-screen div → walk all `<text>` elements with `getBBox()` → compare each right edge against viewBox right edge. Cheaper than visual eyeball and catches the specific monospace-text-overflow-at-strip-right-edge class of bug. Bottom strips and code captions are the common offenders. Chat-18 lesson reinforced chat-20: source review catches structural correctness but NOT visual correctness — render-check at phone width is mandatory before declaring done.
4. **Save status.md updates as soon as substantial work is locked in, even before render-check.** Chat-19 lesson — when conversation continuity is uncertain (chats restarting unexpectedly), prioritize the documentation step earlier in the pipeline. Render-check can be a tail-end task this chat or the leading task next chat; either way the disk state is self-documenting.

---

## Out-of-scope flags from chat 15 (decide separately if any are worth a focused chat)

1. **`details.toc-card` floating outline overlays canvas-fallback area on mobile.** Sticky `<details class="card toc-card auto-toc">`, z-index 100, ~229 px tall, default-open. Visually covers canvas-fallback figure on phones. Pre-existing (Phase 5 auto-TOC infra). Possible fixes: default-collapsed below 768 px, fully hidden below 768 px, or shrink the sticky height.
2. **Canvas demo JS animation loops keep running on mobile when canvas is hidden** — wasted CPU. Pre-existing across all 53 canvas demos. Easy per-lesson fix (`if (matchMedia('(max-width: 768px)').matches) return;` early-out at top of animation loop) but rolling out to 53 canvases is a script-pass.
3. **Lazy-load on canvas-fallback `<img>`** is correct behavior — noted only because it caused initial diagnostic confusion (`naturalWidth: 0` on first JS query, resolves on scroll). Implication for future render checks: query `naturalWidth` AFTER scrolling into viewport.

---

## Live open questions (full list incl. resolved in `status.md`)

1. `_python.html` companion files — standalone learning resources or appendix code dumps? (3 still missing both Summary + Exercise as of post-Phase-6 audit.)
2. `index.html` — join the design system (CSS vars, theme toggle) or stay bespoke?
