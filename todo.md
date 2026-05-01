# Python Game Dev — Course Modernization TODO

> Forward-looking next-chat steering. **Read `support/session.md` first** for the immediate resume pointer; then this file for the next-chat task. Full history, decisions, review items, and resolved questions live in `status.md` — pull individual sections only on demand.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Current state

- Phases 1–6: ✅ done. Phase 6 = 24 SVGs shipped (plus SVG #25 source-level-cleared chat 23, render-check pending). **#25 `sound-layers.svg` source-level-cleared chat 23** (4th interrupted-chat-artifact case after chat 17→#21, chat 19→#22, chat 21→#24): SVG was already built and inserted from a prior interrupted chat-23 attempt — viewBox 720×400, 5-row stacked layout (music / ambient / SFX / UI / master-bus summed envelope), theme-aware via `prefers-color-scheme`, ID prefix `sl-`, full a11y scaffolding; `polish_sound.html` has Phase 6 `<figure class="svg-wrapper">` (convention B between mermaid taxonomy and `<h2 id="interactive-sound-design-studio">`, alt ~590 chars matching #24 precedent) and canvas-fallback `<figure class="canvas-fallback">` wrapping `#soundCanvas` inside `.canvas-wrapper`; catalog flipped `"reuse (built chat 23)"`. Source-level pass clean: sans-serif bottom strip ~485 px wide ending well within strip right edge x=704 (>180 px clearance), per-cell waveform clearances all positive (SFX top tightest at 5 px from cell edge), 5-row stack y=16–290 inside viewBox height 400 with strip y=302–380. **#24 `difficulty-curves.svg` render-checked clean chat 22**, **#23 `pygame-primitives.svg` chat 21**, **#22 `behavior-tree.svg` chat 20**, **#21 `screenshake-decay.svg` chat 18** — all five verification points cleared in each. #20 `game-loop-cycle.svg` (chat 14) is the only remaining "pending eyeball" item.
- Phase 7: 🔄 9/15 lessons wired through chat 23 (8/15 render-checked clean; SVG #25 source-level-cleared with render-check deferred to chat 24). 6/15 deferred pending new SVGs #26–#31.
- Phases 8–9: ⏳

**Two new working disciplines added chat 23 (Ray-driven, in response to 4th interrupted-artifact case):**

1. **save-first-not-last** — doc updates happen at milestone boundaries, not chat end. Stub `todo.md` + `status.md` writes at chat start; incremental updates after each milestone. Reverses the chat-19/21/22 failure pattern (saves were ordered *near* the interruption window; this moves them *away* from it).
2. **`support/session.md`** — single-paragraph resume pointer, **first file to read on chat start** before this `todo.md`. Overwritten at every milestone; does not accumulate history (`status.md`'s job). Schema in the file itself.

---

## Next chat (chat 24) — render-check SVG #25 + optional next build

Chat 23 source-level-cleared SVG #25 `sound-layers.svg` (4th interrupted-chat-artifact case). Render-check deferred to chat 24 per build-in-N / check-in-N+1 pattern. **Read `support/session.md` first** for the precise resume state before reading anything else.

### Step 0 — chat-start save-first stub (new chat-23 discipline)

First tool call of the chat updates `support/session.md` with the chat-24 in-progress state; second tool call adds a stub line to this `todo.md` ("chat 24 in progress, plan = render-check #25") and to `status.md` (chat-24 section header with placeholder body). Don't wait for milestones to save — that pattern failed in chats 19 / 21 / 22 / 23 (4 of 7 chats lost narrative writes to chat-end interruption).

### Step 1 — render-check SVG #25 at iframe-simulated 380×820

Five verification points (chat-22 #24 closure pattern):

1. `#soundCanvas` `computedDisplay: none` despite inline `display: inline-block` (chat-15 `!important` hardening — the inline-display case it anticipated; will be the 5th lesson confirming, after `polish_screenshake.html` chat 18, `ai_behavior_trees.html` chat 20, `polish_difficulty.html` chat 22).
2. `.canvas-wrapper` parent inside `<main>` (Phase 7 markup convention).
3. Phase 6 figure (`figure.svg-wrapper`) between mermaid taxonomy and `<h2 id="interactive-sound-design-studio">` (convention B placement); confirm `display: block`, `imgComplete: true`, alt ~590 chars.
4. Canvas-fallback figure (`figure.canvas-fallback`) sibling of `#soundCanvas` inside `.canvas-wrapper`; `display: block`, `imgComplete: true`, concise fallback alt.
5. Visual gate: 5 rows render cleanly (music continuous sine bed / ambient slow drone / SFX 3 damped-oscillation bursts / UI 4 click-spikes / Master summed envelope with dashed zero-axis), right-side gain labels (−12 / −18 / −6 / −10 dB / Σ) intact, bottom-strip 3 explanation lines fully inside viewBox.

### Step 2 (recommended) — programmatic getBBox check

Per chat-21 + chat-22 precedent. `fetch` the SVG → `DOMParser` parse → mount inline in an off-screen div → walk all `<text>` elements with `getBBox()` → compare each right edge against viewBox right edge x=720 (or strip right edge x=704 for in-strip text). Source-level estimate: 0/N overflows expected with comfortable clearances on the bottom strip (>180 px estimated). Chat 23 deferred this step — chat 24 gets to do both inline (cheap once Chrome MCP is up).

### Step 3 (optional, only if budget allows after render-check) — build next deferred SVG

6 deferred Phase 7 lessons remain. Pick from:

- `genres_puzzle.html` → `puzzle-mechanics-grid.svg`
- `genres_racing.html` → `racing-track-physics.svg`
- `genres_rpg.html` → `rpg-stats-progression.svg`
- `genres_strategy.html` → `strategy-resource-flow.svg`
- `genres_tower_defense.html` → `tower-defense-lane.svg`
- `polish_playtesting.html` → `playtesting-feedback-loop.svg`

`build_concept` sketches in `support/phase7-canvas-fallback-catalog.json`.

### Standard Phase 7 pipeline reminder

Read `support/session.md` → stub `todo.md` + `status.md` updates immediately (save-first discipline) → `grep -l 'svg-wrapper'` the target → **check `images/components/<svg>.svg` doesn't already exist on disk** (chat-17/19/21/23 hard-won lesson — four confirmed cases of interrupted-chat artifacts surviving) → read lesson + refine `build_concept` from catalog → build SVG → insert as Phase 6 figure (convention B) → wrap canvas with canvas-fallback → flip catalog status → **incremental `status.md`/`todo.md`/`session.md` saves at each milestone** → render-check deferred to chat N+1.

### Optional deeper context (only if something here is unclear)

This todo is intended to be self-sufficient. **Don't default-read `status.md`** — it's deep history, not required reading. Pull individual sections only on demand if something specific is unclear:

- *Phase 7 progress (chat 23 — SVG #25 discovery + save-first-not-last discipline added)* in `status.md` — most recent narrative + the new save-first + session.md disciplines in detail.
- *Phase 7 progress (chat 22 — SVG #24 render-check closure + retroactive chat-21 narrative)* in `status.md` — most recent render-check precedent for the 5-verification-point pattern.
- *Phase 6 progress (chat 18 — SVG #21 render-check + bottom-strip overflow fix)* in `status.md` — precedent overflow case (monospace-driven), motivating example for the now-standard programmatic getBBox check.
- *Open follow-ups on shipped SVGs* in `status.md` — pending eyeball items for SVG #20 `game-loop-cycle.svg` (chat 14).
- Any recent `/images/components/<svg>.svg` (e.g. `sound-layers.svg`, `difficulty-curves.svg`, `pygame-primitives.svg`, `behavior-tree.svg`) is a self-contained reference for the visual language conventions.

### Pre-build checklist (chat-17/18/19/20/21/22/23 hard-won lessons combined)

1. **Read `support/session.md` first** (chat-23 added). Single-paragraph resume pointer. Tells you the exact state of play and the next step before you read anything else.
2. **Stub `todo.md` + `status.md` writes immediately at chat start** (chat-23 added — save-first-not-last discipline). Don't wait for milestones.
3. `grep -l 'svg-wrapper'` the target lesson — pre-staged figure markup may already dictate filename, layout, or labels; existing alt text = spec.
4. **Check `images/components/<svg>.svg` doesn't already exist on disk.** Now confirmed FOUR times (chat 17 → #21, chat 19 → #22, chat 21 → #24, chat 23 → #25). Quick check: `read_text_file --head 3 <path>`. If the file exists, also check the target lesson for pre-staged figure markup and the catalog JSON for an updated status — both may have been flipped before the prior chat was interrupted.
5. **Run a text-overflow sanity check** before declaring an SVG done. **Source-level estimate:** any text using `text-anchor: start` (the default) needs its rendered width estimated against the SVG viewBox right edge, especially long monospace lines (~6.3 px/char at 10.5 px); sans-serif at the same point size is narrower (~5.5–6 px/char). **Programmatic check (chat-20 addition; chat-21 + chat-22 reinforced):** `fetch` the SVG → `DOMParser` parse → mount inline in an off-screen div → walk all `<text>` elements with `getBBox()` → compare each right edge against viewBox right edge.
6. **Save `todo.md` + `status.md` + `session.md` updates at every milestone**, not at chat end. Chat-23 hard-won lesson — the save-first-not-last discipline reverses the chat-19/21/22 failure pattern that even repeated reinforcement could not fix while saves were ordered near the interruption window.

---

## Out-of-scope flags from chat 15 (decide separately if any are worth a focused chat)

1. **`details.toc-card` floating outline overlays canvas-fallback area on mobile.** Sticky `<details class="card toc-card auto-toc">`, z-index 100, ~229 px tall, default-open. Visually covers canvas-fallback figure on phones. Pre-existing (Phase 5 auto-TOC infra). Possible fixes: default-collapsed below 768 px, fully hidden below 768 px, or shrink the sticky height.
2. **Canvas demo JS animation loops keep running on mobile when canvas is hidden** — wasted CPU. Pre-existing across all 53 canvas demos. Easy per-lesson fix (`if (matchMedia('(max-width: 768px)').matches) return;` early-out at top of animation loop) but rolling out to 53 canvases is a script-pass.
3. **Lazy-load on canvas-fallback `<img>`** is correct behavior — noted only because it caused initial diagnostic confusion (`naturalWidth: 0` on first JS query, resolves on scroll). Implication for future render checks: query `naturalWidth` AFTER scrolling into viewport.

---

## Live open questions (full list incl. resolved in `status.md`)

1. `_python.html` companion files — standalone learning resources or appendix code dumps? (3 still missing both Summary + Exercise as of post-Phase-6 audit.)
2. `index.html` — join the design system (CSS vars, theme toggle) or stay bespoke?
