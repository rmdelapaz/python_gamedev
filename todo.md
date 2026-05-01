# Python Game Dev — Course Modernization TODO

> Forward-looking next-chat steering. **Full history, decisions, review items, and resolved questions live in `status.md`** — read it first if landing fresh.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Current state

- Phases 1–6: ✅ done. Phase 6 = 20 SVGs shipped.
- Phase 7: 🔄 4/15 lessons wrapped + render-checked clean on mobile through chat 15. 11/15 deferred pending new SVGs #21–#31.
- Phases 8–9: ⏳

---

## Next chat — pick one (recommended order)

1. **Build SVG #21.** Easiest first picks (concrete `build_concept` in `support/phase7-canvas-fallback-catalog.json`):
   - `ai_behavior_trees.html` → `behavior-tree.svg` (hierarchical tree + tick path)
   - `pygame_basics_drawing.html` → `pygame-primitives.svg` (3×2 grid of `pygame.draw.*` shapes)
   - `polish_screenshake.html` → `screenshake-decay.svg` (two stacked decay charts — lowest design risk after the existing chart precedents)

   Pattern (same as chat 14): build SVG file → insert as Phase 6 figure (convention B-equivalent: between mermaid/explanation and Interactive Demo h2) → wrap every canvas in the lesson with canvas-fallback → flip catalog JSON status from `needs_new_svg` to `reuse (built chat <N>)` → increment Phase 6 count → **phone-width render-check at localhost:5503 before declaring done**.

2. **Render-check Phase 6 SVGs #17/#18/#19** (`parallax-layers.svg`, `utility-response-curves.svg`, `easing-curves.svg`). Review items pending in `status.md` → *Open follow-ups on shipped SVGs*. Pure visual; can interleave with option 1 (same browser session at localhost:5503).

**Before writing any new SVG:** `grep -l 'svg-wrapper'` the target lesson(s). Pre-staged `<figure class="svg-wrapper">` markup may already dictate filename, layout, or labels — existing alt text = spec.

**Reload from `status.md` before starting:**
- *Phase 6 progress → Decisions locked / Visual language / Recurring SVG conventions*
- *Phase 7 progress chats 12 / 13 / 14 / 15* (catalog schema → infrastructure → first wraps → render-check + CSS hardening)
- *Open follow-ups on shipped SVGs → SVG #20 `game-loop-cycle.svg`* — review items still pending eyeball

---

## Out-of-scope flags from chat 15 (decide separately if any are worth a focused chat)

1. **`details.toc-card` floating outline overlays canvas-fallback area on mobile.** Sticky `<details class="card toc-card auto-toc">`, z-index 100, ~229 px tall, default-open. Visually covers canvas-fallback figure on phones. Pre-existing (Phase 5 auto-TOC infra). Possible fixes: default-collapsed below 768 px, fully hidden below 768 px, or shrink the sticky height.
2. **Canvas demo JS animation loops keep running on mobile when canvas is hidden** — wasted CPU. Pre-existing across all 53 canvas demos. Easy per-lesson fix (`if (matchMedia('(max-width: 768px)').matches) return;` early-out at top of animation loop) but rolling out to 53 canvases is a script-pass.
3. **Lazy-load on canvas-fallback `<img>`** is correct behavior — noted only because it caused initial diagnostic confusion (`naturalWidth: 0` on first JS query, resolves on scroll). Implication for future render checks: query `naturalWidth` AFTER scrolling into viewport.

---

## Live open questions (full list incl. resolved in `status.md`)

1. `_python.html` companion files — standalone learning resources or appendix code dumps? (3 still missing both Summary + Exercise as of post-Phase-6 audit.)
2. `index.html` — join the design system (CSS vars, theme toggle) or stay bespoke?
