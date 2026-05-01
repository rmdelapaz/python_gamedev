# Python Game Dev — Course Modernization TODO

> Forward-looking next-chat steering. **Full history, decisions, review items, and resolved questions live in `status.md`** — read it first if landing fresh.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Current state

- Phases 1–6: ✅ done. Phase 6 = 24 SVGs shipped. **#24 `difficulty-curves.svg` render-checked clean chat 22**: all five verification points cleared at iframe-simulated 380×820 — `#difficultyCanvas` `computedDisplay: none` despite inline `display: inline-block` (chat-15 `!important` hardening confirmed in the field, fourth lesson); `.canvas-wrapper` parent inside `<main>`; Phase 6 figure at iframe y=1429, 366×347 px, alt 580 chars, complete, before h2 (convention B placement); canvas-fallback figure at y=1916, 346×350 px, sibling of `#difficultyCanvas` inside `.canvas-wrapper`; visual gate confirmed three cells + bottom-strip text fully inside viewBox (getBBox pre-cleared chat 21 with 0/13 overflows). Originally **discovered chat 21 as another pre-shipped interrupted-chat artifact** (third instance after chat 17 → #21 and chat 19 → #22). **#23 `pygame-primitives.svg` render-checked clean chat 21**: all five verification points cleared at iframe-simulated 380×820 (inline-SVG getBBox returning 0/32 text overflows; cell 4 `line` signature tightest at 3.45 px each side — borderline confirmed but positive clearance, no source-level fix needed; bottom-strip sans-serif lines 144–194 px right clearance). #22 `behavior-tree.svg` (chat 19 build / chat 20 render-check) and #21 `screenshake-decay.svg` (chat 17 build / chat 18 render-check) both shipped clean. #17/#18/#19 fully render-checked clean through chat 16. #21 / #22 / #23 / #24 review items now dischargeable. #20 (chat 14) review items still pending eyeball.
- Phase 7: 🔄 8/15 lessons wired and render-checked clean through chat 22. 7/15 deferred pending new SVGs #25–#31.
- Phases 8–9: ⏳

---

## Next chat — build SVG #25

Chat 22 closed SVG #24 `difficulty-curves.svg` render-check at iframe-simulated 380×820 — all five verification points cleared:

1. `#difficultyCanvas` `computedDisplay: none` despite inline `display: inline-block` (chat-15 `!important` hardening confirmed in the field for the fourth lesson, after `polish_screenshake.html` chat 18, `ai_behavior_trees.html` chat 20, and same situation here);
2. `.canvas-wrapper` parent inside `<main>` (Phase 7 markup convention);
3. Phase 6 figure (`figure.svg-wrapper`) at iframe y=1429, 366×347 px, `display: block`, `imgComplete: true`, alt 580 chars, positioned **before** the h2 anchor (convention B placement between mermaid taxonomy and `<h2 id="interactive-difficulty-testing-lab">`);
4. Canvas-fallback figure (`figure.canvas-fallback`) at iframe y=1916, 346×350 px, `display: block`, sibling of `#difficultyCanvas` inside `.canvas-wrapper`;
5. Visual gate at 380×820 confirmed three cells (Linear ramp / Plateau / Dynamic DDA) and bottom-strip text fully inside viewBox; getBBox pre-cleared chat 21 (0/13 overflows + 16/146 px bottom-strip clearances).

Chat 22 also wrote retroactive chat-21 narrative to `status.md` after discovering chat 21 closed `todo.md` cleanly but skipped the status.md narrative writes before chat end (second documented case after chat 19; lesson reinforced — status.md writes happen at SAME milestones as todo.md updates). MCP servers timed out for one turn mid-chat and self-recovered on probe — pattern documented for future outages.

Full narratives in `status.md` → *Phase 7 progress (chat 21 — SVG #23 render-check + SVG #24 discovery)* and *Phase 7 progress (chat 22 — SVG #24 render-check closure + retroactive chat-21 narrative)*.

### Step 1 — build SVG #25

Pick from the 7 deferred Phase 7 lessons. Carryforward candidate from chat 19 / chat 21 / chat 22:

1. **`polish_sound.html` → `sound-layers.svg`** (recommended) — characteristic-waveform diagram, 4 stacked audio tracks (music / ambient / SFX / UI), `build_concept` already detailed in `support/phase7-canvas-fallback-catalog.json`. Novel territory but small surface area.

Other deferred lessons (all have `build_concept` sketches in the catalog):

- `genres_puzzle.html` → `puzzle-mechanics-grid.svg`
- `genres_racing.html` → `racing-track-physics.svg`
- `genres_rpg.html` → `rpg-stats-progression.svg`
- `genres_strategy.html` → `strategy-resource-flow.svg`
- `genres_tower_defense.html` → `tower-defense-lane.svg`
- `polish_playtesting.html` → `playtesting-feedback-loop.svg`

### Step 2 (optional) — programmatic getBBox check before declaring source-level done

`fetch` the SVG → `DOMParser` parse → mount inline in an off-screen div → walk all `<text>` elements with `getBBox()` → compare each right edge against viewBox right edge. Catches monospace-bottom-strip overflow class of bug (chat-18 case) before render-check. Chat 21 + 22 confirmed positive value: caught the cell-4-line signature width-tightness flag from chat-20 build at 3.45 px each side (positive clearance, but caught the borderline case proactively).

### Step 3 — render-check deferred to chat 24

Per the established build-in-N / check-in-N+1 pattern (chats 17→18, 19→20, 20→21, 21→22 — four consecutive instances). Save status.md AND todo.md updates as soon as the build is locked in, before chat end — chat 22 lesson reinforced chat 19: BOTH files together form the self-documenting handoff between chats.

### Standard Phase 7 pipeline reminder

`grep -l 'svg-wrapper'` the target → **check `images/components/<svg>.svg` doesn't already exist on disk** (chat-17 / chat-19 / chat-21 hard-won lesson — three confirmed cases of interrupted-chat artifacts surviving) → read lesson + refine `build_concept` from catalog → build SVG in `images/components/` → insert as Phase 6 figure (convention B) → wrap canvas with canvas-fallback → flip catalog status `needs_new_svg` → `reuse (built chat <N>)` → save **todo.md AND status.md** updates BEFORE render-check (chat 19 + 21 + 22 reinforced) → render-check deferred to chat N+1 per the established pattern.

### Optional deeper context (only if something here is unclear)

This todo is intended to be self-sufficient. **Don't default-read `status.md`** — it's deep history, not required reading. Pull individual sections only on demand if something specific is unclear:

- *Phase 6 progress → Decisions locked / Visual language / Recurring SVG conventions* in `status.md` — palette + theming pattern + accessibility scaffolding. **Alternative:** any recent `/images/components/<svg>.svg` (e.g. `difficulty-curves.svg`, `pygame-primitives.svg`, `behavior-tree.svg`) is a self-contained reference for the same conventions.
- *Phase 7 progress (chat 22 — SVG #24 render-check closure + retroactive chat-21 narrative)* in `status.md` — most recent render-check precedent + retroactive-narrative pattern.
- *Phase 7 progress (chat 21 — SVG #23 render-check + SVG #24 discovery)* in `status.md` — chat-21 work captured retroactively at chat-22 close, including the third interrupted-chat-artifact case + the chat-21 getBBox check confirming positive 3.45 px clearance against the build-time tightness flag.
- *Phase 6 progress (chat 18 — SVG #21 render-check + bottom-strip overflow fix)* in `status.md` — precedent overflow case (monospace-driven), motivating example for the now-standard programmatic getBBox check.
- *Open follow-ups on shipped SVGs* in `status.md` — pending eyeball items for SVG #20 `game-loop-cycle.svg` (chat 14). SVG #21 / #22 / #23 / #24 review items all dischargeable post chat 18 / 20 / 21 / 22 render-checks.

### Pre-build checklist (chat-17 / 18 / 19 / 20 / 21 / 22 hard-won lessons combined)

1. `grep -l 'svg-wrapper'` the target lesson — pre-staged figure markup may already dictate filename, layout, or labels; existing alt text = spec.
2. **Check `images/components/<svg>.svg` doesn't already exist on disk.** Now confirmed three times (chat 17 → #21, chat 19 → #22, chat 21 → #24; all closed cleanly chat 18 / 20 / 22). Quick check: `read_text_file --head 3 <path>`. If the file exists, also check the target lesson for pre-staged figure markup and the catalog JSON for an updated status — both may have been flipped before the prior chat was interrupted.
3. **Run a text-overflow sanity check** before declaring an SVG done. **Source-level estimate:** any text using `text-anchor: start` (the default) needs its rendered width estimated against the SVG viewBox right edge, especially long monospace lines (~6.3 px/char at 10.5 px); sans-serif at the same point size is narrower (~5.5–6 px/char) so has more margin. **Programmatic check (chat-20 addition; chat-21 + chat-22 reinforced):** `fetch` the SVG → `DOMParser` parse → mount inline in an off-screen div → walk all `<text>` elements with `getBBox()` → compare each right edge against viewBox right edge. Cheaper than visual eyeball and catches the specific monospace-text-overflow-at-strip-right-edge class of bug. Bottom strips and code captions are the common offenders.
4. **Save todo.md AND status.md updates as soon as substantial work is locked in, even before render-check.** Chat 19 + 21 + 22 hard-won lesson — when conversation continuity is uncertain (chats restarting unexpectedly + MCP server outages mid-chat), prioritize the documentation step earlier in the pipeline. **BOTH files** update together; chat 21 wrote todo.md but skipped status.md, leaving chat 22 to retroactively reconstruct the chat-21 narrative.

---

## Out-of-scope flags from chat 15 (decide separately if any are worth a focused chat)

1. **`details.toc-card` floating outline overlays canvas-fallback area on mobile.** Sticky `<details class="card toc-card auto-toc">`, z-index 100, ~229 px tall, default-open. Visually covers canvas-fallback figure on phones. Pre-existing (Phase 5 auto-TOC infra). Possible fixes: default-collapsed below 768 px, fully hidden below 768 px, or shrink the sticky height.
2. **Canvas demo JS animation loops keep running on mobile when canvas is hidden** — wasted CPU. Pre-existing across all 53 canvas demos. Easy per-lesson fix (`if (matchMedia('(max-width: 768px)').matches) return;` early-out at top of animation loop) but rolling out to 53 canvases is a script-pass.
3. **Lazy-load on canvas-fallback `<img>`** is correct behavior — noted only because it caused initial diagnostic confusion (`naturalWidth: 0` on first JS query, resolves on scroll). Implication for future render checks: query `naturalWidth` AFTER scrolling into viewport.

---

## Live open questions (full list incl. resolved in `status.md`)

1. `_python.html` companion files — standalone learning resources or appendix code dumps? (3 still missing both Summary + Exercise as of post-Phase-6 audit.)
2. `index.html` — join the design system (CSS vars, theme toggle) or stay bespoke?
