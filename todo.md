# Python Game Dev — Course Modernization TODO

> Forward-looking next-chat steering. **Full history, decisions, review items, and resolved questions live in `status.md`** — read it first if landing fresh.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Current state

- Phases 1–6: ✅ done. Phase 6 = 22 SVGs shipped (#22 `behavior-tree.svg` discovered on disk chat 19 from prior interrupted chat-19 attempt — same chat-17 pattern; source-verified clean, render-check pending. #21 `screenshake-decay.svg` built chat 17 + render-checked clean chat 18 with bottom-strip overflow fix). #17/#18/#19 fully render-checked clean through chat 16. #21 review items dischargeable as of chat 18. #20 (chat 14) review items still pending eyeball. #22 (chat 19) review items pending render-check.
- Phase 7: 🔄 6/15 lessons wired through chat 19 (5 render-checked clean through chat 18; #22 ai_behavior_trees.html source-verified chat 19 with render-check pending). 9/15 deferred pending new SVGs #23–#31.
- Phases 8–9: ⏳

---

## Next chat — render-check SVG #22, then build SVG #23

Step 1 (build SVG #22 `behavior-tree.svg` for `ai_behavior_trees.html`) was completed in a prior interrupted chat-19 attempt — same chat-17 pattern as SVG #21. Discovered already on disk during chat-19 disk-state check: SVG well-formed, lesson markup pre-staged (Phase 6 figure + 2 canvas-fallbacks for the 2 canvases — main `#behaviorCanvas` and togglable `#treeCanvas`), catalog flipped to `reuse (built chat 19)`. Source-level review passed (math + palette + accessibility + text-overflow all clean). Status.md updated chat 19 with full chat-19 subsections under both Phase 6 and Phase 7 progress.

**Render-check at phone-width was deferred** per Ray's "lock in progress before pivoting" call (chat-19 conversation-restart concern). Full narrative in `status.md` → *Phase 6 progress (chat 19 — SVG #22 discovery + state reconciliation)*.

### Recommended pick

**Step 1 (high priority):** Render-check SVG #22 `behavior-tree.svg` at phone-width via the chat-18 iframe-simulation technique (`localhost:5503`, same-origin `<iframe>` sized 380×820 with `src` set to lesson URL — host window resize blocked by MCP sidepanel). Verify:

- Main canvas `#behaviorCanvas` computed `display: none` on mobile despite inline `display: inline-block` (chat-15 `!important` hardening should handle this).
- Main canvas-fallback figure renders inside `.canvas-wrapper` next to `#behaviorCanvas` with SVG loaded (`naturalWidth` non-zero, `complete: true` after scrolling into viewport).
- Phase 6 figure (`<figure class="svg-wrapper">`) renders cleanly at desktop position between mermaid and Interactive h2.
- Bottom-strip text fits inside the strip rect (sans-serif throughout; longest row ~89 chars; should be comfortable but verify after chat-18's lesson on render-check vs source-review).
- Tree-canvas fallback figure renders inside togglable `<div id="treeView">` ONLY after the user clicks "📊 Tree Visualization" button to toggle the parent visible — that's the chat-13 visibility-gating pattern; the parent's `display: none` cascades to the child fallback figure until toggled.
- Cache-busters: append `?v=<timestamp>` on iframe `src` and on `<img src>` after any disk edit.

**Step 2 (after #22 render-check is closed):** Build Phase 7 SVG #23.

### Step 2 candidates (after SVG #22 render-check closes)

1. `pygame_basics_drawing.html` → `pygame-primitives.svg` (3×2 grid of `pygame.draw.*` shapes) — **alternative target carried from chat-17 todo**, well-scoped concrete concept (6 primitives × signature labels); high probability of clean source-only build.
2. `polish_difficulty.html` → `difficulty-curves.svg` (3 sub-charts: linear ramp / plateau / DDA) — chart-heavy, mirrors easing-curves and utility-response-curves precedents, build_concept already detailed in catalog.
3. `polish_sound.html` → `sound-layers.svg` (4 stacked audio tracks: music / ambient / SFX / UI) — characteristic-waveform diagram, novel territory but small surface area.

### Standard Phase 7 pipeline

`grep -l 'svg-wrapper'` the target → **check `images/components/<svg>.svg` doesn't already exist on disk** (chat-17 + chat-19 hard-won lesson — interrupted attempts may have shipped artifacts that survived; now confirmed twice) → read lesson + refine `build_concept` from `support/phase7-canvas-fallback-catalog.json` → build SVG in `images/components/` → insert as Phase 6 figure (convention B) → wrap canvas with canvas-fallback → flip catalog status `needs_new_svg` → `reuse (built chat <N>)` → **save status.md updates as soon as the build is locked in, even before render-check** (chat-19 hard-won lesson — make disk state self-documenting in case of conversation interruption) → **phone-width render-check at `localhost:5503` via iframe simulation** (chat-18 technique).

### Optional deeper context (only if something here is unclear)

This todo is intended to be self-sufficient. **Don't default-read `status.md`** — it's deep history, not required reading. Pull individual sections only on demand if something specific is unclear:

- *Phase 6 progress → Decisions locked / Visual language / Recurring SVG conventions* in `status.md` — palette + theming pattern + accessibility scaffolding. **Alternative:** any recent `/images/components/<svg>.svg` (e.g. `behavior-tree.svg`, `screenshake-decay.svg`, `easing-curves.svg`) is a self-contained reference for the same conventions — the visual language is encoded inline in each file's `<style>` block.
- *Phase 6 progress (chat 19 — SVG #22 discovery + state reconciliation)* in `status.md` — the most recent disk-state-check pattern, if you need the full chat-19 narrative beyond what this todo summarizes.
- *Phase 6 progress (chat 18 — SVG #21 render-check + bottom-strip overflow fix)* in `status.md` — full iframe-simulation render-check workflow with the host-window-resize-blocked-by-MCP-sidepanel debugging.
- *Phase 7 progress chats 12 / 13 / 14 / 15 / 17 / 18 / 19* in `status.md` — chat-by-chat Phase 7 history.
- *Open follow-ups on shipped SVGs* in `status.md` — pending render-check items for SVG #22 `behavior-tree.svg` (chat 19) + pending eyeball items for SVG #20 `game-loop-cycle.svg` (chat 14).

### Pre-build checklist (chat-17 + chat-18 + chat-19 hard-won lessons)

1. `grep -l 'svg-wrapper'` the target lesson — pre-staged figure markup may already dictate filename, layout, or labels; existing alt text = spec.
2. **Check `images/components/<svg>.svg` doesn't already exist on disk.** Now confirmed twice (chat 17 → #21, chat 19 → #22) that interrupted chat attempts may have shipped artifacts that survived. Quick check: `read_text_file --head 3 <path>`. If the file exists, also check the target lesson for pre-staged figure markup and the catalog JSON for an updated status — both may have been flipped before the prior chat was interrupted.
3. **Run a text-overflow sanity check** before declaring an SVG done. Any text using `text-anchor: start` (the default) needs its rendered width estimated against the SVG viewBox right edge, especially long monospace lines (~6.3 px/char at 10.5 px); sans-serif at the same point size is narrower (~5.5–6 px/char) so has more margin. Bottom strips and code captions are the common offenders. Chat-18 lesson: source review catches structural correctness but NOT visual correctness — render-check at phone width is mandatory before declaring done.
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
