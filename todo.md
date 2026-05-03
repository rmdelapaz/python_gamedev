# Python Game Dev — Course Modernization TODO

> Forward-looking next-chat steering. **Read `support/session.md` first** for the immediate resume pointer; then this file for the next-chat task. Full history, decisions, review items, and resolved questions live in `status.md` — pull individual sections only on demand.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Current state

- Phases 1–6: ✅ done. Phase 6 = 25 SVGs shipped, **all 25 render-checked clean as of chat 24** (#25 `sound-layers.svg` was the last open render-check; passed all 5 verification points at iframe-simulated 380×820 — 5th confirmation of the chat-15 `!important` hardening for inline-display canvases). #20 `game-loop-cycle.svg` (chat 14) eyeball-discharged out-of-band by Ray between chats 23 and 24 — **no "pending eyeball" items remain on any shipped SVG.**
- Phase 7: 🔄 11/15 lessons wired AND render-checked clean (#27 `strategy-resource-flow.svg` for `genres_strategy.html` render-checked clean chat 28 — 7th confirmation of chat-15 `!important` hardening). 4/15 deferred pending new SVGs (`genres_racing` / `genres_rpg` / `genres_tower_defense` / `polish_playtesting`).
- Phases 8–9: ⏳

**Two new working disciplines added chat 23 (Ray-driven, in response to 4th interrupted-artifact case):**

1. **save-first-not-last** — doc updates happen at milestone boundaries, not chat end. Stub `todo.md` + `status.md` writes at chat start; incremental updates after each milestone. Reverses the chat-19/21/22 failure pattern (saves were ordered *near* the interruption window; this moves them *away* from it).
2. **`support/session.md`** — single-paragraph resume pointer, **first file to read on chat start** before this `todo.md`. Overwritten at every milestone; does not accumulate history (`status.md`'s job). Schema in the file itself.

**Four new conventions added chat 27 (Ray-driven, in response to interruption-rate analysis), effective chat 28+:**

1. **Default to region-scoped reads.** Use `head` / `tail` / `view_range` for lesson HTML, precedent lesson HTML, and precedent SVG — not full-file reads. Build chats were consuming 30–50% more input tokens than necessary. Full-file reads are a deliberate escalation, not the default.
2. **Keep `status.md` chat-N sections concise (~1.5 KB target, not 7 KB).** Disk artifacts are the source of truth; the narrative is annotation. Trim ruthlessly: SVG details visible from the SVG header comment don't need to be repeated; healthy getBBox margins are just "clean."
3. **Intermediate catalog status `built_unwired_chat_N`** between SVG-on-disk and wire-complete. Immediately after the SVG file is written, flip the lesson's catalog entry to `built_unwired_chat_N`. The dominant failure mode (5/5 interrupted-artifact cases) hits exactly the SVG→wire window; this records the build automatically. Effective chat 29+ (next build chat).
4. **Slim chat-N+1 kickoff prompt to ~500 bytes** for build chats; modestly longer for render-check chats (visual-gate content list needs explicit listing). Kickoff structure: project root + UNC reminder + 1 sentence pointing to `session.md` + 1 sentence describing the chat-N task. Working files carry the convention details.

Full rationale and pattern recognition in `status.md` → *Phase 7 progress (chat 27)* → "Conventions added this chat" paragraph + the durable bullets in the *Conventions / things to remember* section.

---

## Chat 29 — IN PROGRESS — build SVG #28 for one of 4 deferred Phase 7 lessons

**Chat 29 in progress, plan = build SVG #28 for one of `genres_racing` / `genres_rpg` / `genres_tower_defense` / `polish_playtesting`.** Stub pre-staged at chat-28 close per save-first-compounding discipline (6th consecutive chat in the chat-23 discipline streak; **4th consecutive chat where chat-N close has pre-staged the chat-N+1 IN PROGRESS section** — chat 25 first, 26 second, 27 third, this chat-28→29 fourth).

**Chat 28 closed clean.** Render-checked SVG #27 `strategy-resource-flow.svg` in `genres_strategy.html` at iframe-simulated 380×820. **All 5 verification points pass; 7th confirmation of the chat-15 `!important` hardening** (canvas inline `display: inline-block` → computed `display: none`). getBBox re-clear reproduced chat-27 numbers exactly (34 nodes / 0 overflows / 56.34 / 23.4 / 67.58 / 11.05). Visual gate via chat-26 parent-page inline-render workaround clean. Phase 7 wired-AND-render-checked count: 10/15 → **11/15**. Deferred unchanged at 4/15. **First chat under the four chat-27 conventions** — region-scoped reads landed (status.md was `head 120` + `tail 200`); status.md chat-28 narrative ~2 KB (close to 1.5 KB target); `built_unwired_chat_N` intermediate status first exercised this chat (chat 29); slim kickoff was the first to follow the rule.

Phase 7 status now: **11/15 wired AND render-checked clean (chat 28), 4/15 deferred pending new SVGs.**

**Read `support/session.md` first** for the precise resume state, then `support/next-chat-prompt.md` for the chat-29 task brief. **Don't default-read this todo.md** as the resume pointer.

### Step 0 — chat-start save-first stub (chat-23 discipline; chat-24/25/26/27/28 all validated)

First tool call updates `support/session.md` with the chat-29 in-progress state. The chat-29 placeholder section in `status.md` and the chat-29 IN PROGRESS line in this `todo.md` were both **pre-staged at chat-28 close** (save-first compounding). At chat 29 start, only the `session.md` overwrite is required — chat 29 inherits a fully primed save-state. **Continue the pattern at chat-29 close** (pre-stage chat-30 stubs as part of the chat-29 closing milestone).

### Step 1 — build SVG #28 (primary chat-29 task)

Pick one of the 4 deferred Phase 7 lessons. Catalog `build_concept` sketches in `support/phase7-canvas-fallback-catalog.json`. The build pipeline now runs through the new chat-27 intermediate-status convention:

1. **Region-scoped read** the target lesson HTML — grep for `svg-wrapper` and the canvas-wrapper anchor first, then `view_range` only the mermaid-and-canvas-wrapper region. Same for the precedent lesson HTML. For the precedent SVG, read header comment + `tail 5` only unless visual-language reuse is genuinely needed. Full-file reads are deliberate escalation, not the default.
2. Refine `build_concept` from canonical lesson terminology (button labels in the canvas demo are the source of truth).
3. Write the SVG file (`/images/components/<name>.svg`).
4. **Flip catalog `status` to `built_unwired_chat_29`** *immediately after* the SVG file write — first chat to exercise this intermediate status. This records the build-on-disk milestone *before* the wire/save spike (the dominant interrupted-artifact failure window).
5. Programmatic getBBox text-overflow pre-clear (chat-20 mandatory). `fetch` SVG → `DOMParser` parse → mount in off-screen 720×400 div → walk all `<text>` and `<tspan>` with `getBBox()` → compare each edge against viewBox edges. Aim for 0 overflows; tightest margin > 0 px on all four sides.
6. Wire Phase 6 `<figure class="svg-wrapper">` between mermaid and the relevant h2, plus `<figure class="canvas-fallback">` inside `.canvas-wrapper` as a sibling of the lesson's `<canvas>` (chat-25/27 precedent).
7. **Flip catalog `status` from `built_unwired_chat_29` to `built chat 29`** after wiring is complete.
8. Pre-stage chat-30 stubs (`status.md` placeholder + this `todo.md` IN PROGRESS line + `support/next-chat-prompt.md`) before chat close — 5th consecutive save-first-compounding step.

### Step 2 (chat 30 work) — render-check SVG #28

Build-in-N / check-in-N+1 pattern. Standard 5-verification-point pattern at iframe-simulated 380×820. Visual gate via chat-26 parent-page inline-render workaround until `Claude in Chrome:computer` `zoom` action coord-system quirk is confirmed reliable.

### Optional deeper context (only if something here is unclear)

This todo is intended to be self-sufficient. **Don't default-read `status.md`** — it's deep history, not required reading. Pull individual sections only on demand:

- *Phase 7 progress (chat 28 — SVG #27 render-check)* in `status.md` — most recent narrative; documents the 7th confirmation of the chat-15 `!important` hardening + first execution under the four chat-27 conventions.
- *Phase 7 progress (chat 27 — SVG #27 build + recovery from mid-pipeline interruption)* in `status.md` — closest precedent for SVG #28 build (full pipeline including the recovery procedure if compaction hits mid-build).
- *Phase 7 progress (chat 25 — SVG #26 build: puzzle-mechanics-grid.svg)* in `status.md` — closest precedent for multi-cell-grid SVG style.
- *Conventions / things to remember* in `status.md` — durable bullets including the four chat-27 conventions.
- Any recent `/images/components/<svg>.svg` (e.g. `strategy-resource-flow.svg`, `puzzle-mechanics-grid.svg`, `sound-layers.svg`) is a self-contained reference for visual language conventions.

### Pre-build checklist (chat-17/18/19/20/21/22/23/24/26/27 hard-won lessons + chat-27 conventions)

1. **Read `support/session.md` first** (chat-23 added; chat-24/25/26/27/28 validated).
2. **Stub `todo.md` + `status.md` writes immediately at chat start** (chat-23 added). For chat 29 only the `session.md` overwrite is required because chat 28 pre-staged the chat-29 stubs.
3. **Default to region-scoped reads** (chat-27 added; first build chat to apply it). Use `head` / `tail` / `view_range` for lesson HTML, precedent lesson HTML, and precedent SVG. Full-file reads are deliberate escalation, not the default. The chat-28 read pattern (`status.md` was `head 120` + `tail 200`) is a working precedent.
4. **Catalog status flow: `needs_new_svg` → `built_unwired_chat_29` → `built chat 29`** (chat-27 added; first build chat to exercise the intermediate status). Flip to `built_unwired_chat_29` *immediately after* SVG file write; flip to `built chat 29` *after* wiring is complete.
5. **Programmatic getBBox text-overflow pre-clear is mandatory** before declaring the build done (chat-20 addition; reinforced through chat-28).
6. **`Claude in Chrome:javascript_tool` does not accept top-level `await`** — kicked-off-then-poll pattern (chat-27 discovery; chat-28 reused uniformly across 3 async scripts).
7. **Save `todo.md` + `status.md` + `session.md` updates at every milestone**, not at chat end.

---

## Out-of-scope flags from chat 15 (decide separately if any are worth a focused chat)

1. **`details.toc-card` floating outline overlays canvas-fallback area on mobile.** Sticky `<details class="card toc-card auto-toc">`, z-index 100, ~229 px tall, default-open. Visually covers canvas-fallback figure on phones. Pre-existing (Phase 5 auto-TOC infra). Possible fixes: default-collapsed below 768 px, fully hidden below 768 px, or shrink the sticky height.
2. **Canvas demo JS animation loops keep running on mobile when canvas is hidden** — wasted CPU. Pre-existing across all 53 canvas demos. Easy per-lesson fix (`if (matchMedia('(max-width: 768px)').matches) return;` early-out at top of animation loop) but rolling out to 53 canvases is a script-pass.
3. **Lazy-load on canvas-fallback `<img>`** is correct behavior — noted only because it caused initial diagnostic confusion (`naturalWidth: 0` on first JS query, resolves on scroll). Implication for future render checks: query `naturalWidth` AFTER scrolling into viewport.

---

## Live open questions (full list incl. resolved in `status.md`)

1. `_python.html` companion files — standalone learning resources or appendix code dumps? (3 still missing both Summary + Exercise as of post-Phase-6 audit.)
2. `index.html` — join the design system (CSS vars, theme toggle) or stay bespoke?
