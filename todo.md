# Python Game Dev — Course Modernization TODO

> Forward-looking next-chat steering. **Read `support/session.md` first** for the immediate resume pointer; then this file for the next-chat task. Full history, decisions, review items, and resolved questions live in `status.md` — pull individual sections only on demand.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Current state

- Phases 1–6: ✅ done. Phase 6 = 25 SVGs shipped, **all 25 render-checked clean as of chat 24** (#25 `sound-layers.svg` was the last open render-check; passed all 5 verification points at iframe-simulated 380×820 — 5th confirmation of the chat-15 `!important` hardening for inline-display canvases). #20 `game-loop-cycle.svg` (chat 14) eyeball-discharged out-of-band by Ray between chats 23 and 24 — **no "pending eyeball" items remain on any shipped SVG.**
- Phase 7: 🔄 **13/15 lessons wired AND render-checked clean through chat 32** (SVG #29 `racing-track-physics.svg` for `genres_racing.html` was render-checked clean chat 32 — 9th `!important` hardening confirmation; getBBox re-clear timing 4.6 ms validated the chat-31 rAF-removal finding at 68× speedup). **2/15 deferred** pending new SVGs (`genres_rpg` / `genres_tower_defense`). 0 wired-but-render-pending.
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

## Chat 33 — IN PROGRESS — build SVG #30 for next deferred lesson

**Chat 33 in progress, plan = build + wire next Phase 7 SVG**. Two deferred lessons remain: `genres_rpg.html` (`rpg-stats-progression.svg`) or `genres_tower_defense.html` (`tower-defense-lane.svg`). Lesson pick happens in milestone 1 (region-scoped grep + visual-language fit). **Fourth test bed for the chat-30 streaming-narrative discipline** — chat 30 render-check / chat 31 build / chat 32 render-check / chat 33 second build-chat application. **Second exercise of the chat-27 `built_unwired_chat_N` intermediate catalog status** (first was chat 31).

**Chat 32 closed clean** — render-check SVG #29 `racing-track-physics.svg` in `genres_racing.html` passed all 5 verification points at iframe-simulated 380×820. **9th confirmation of the chat-15 `!important` hardening** (canvas inline `display: inline-block` AND `background: #1a1a1a` both present). getBBox re-clear: 25 text/tspan nodes, 0 overflows, all four tightest margins byte-identical to chat-31 build-time (right 5.11 / bottom 15.4 / left 21.02 / top 11.05 px). **chat-31 rAF-removal finding strongly validated** — 4.6 ms vs chat-31's 315.2 ms (68× speedup). Streaming-narrative discipline held across all 6 milestones. Phase 7 status: 12/15 → 13/15 wired-AND-render-checked clean; deferred drops to 2/15.

**Read `support/session.md` first** for the precise resume state, then `support/next-chat-prompt.md` for the chat-33 task brief. **Don't default-read this todo.md** as the resume pointer.

### Step 0 — chat-start save-first stub validation (chat-23 discipline; chat-32 close = 11th consecutive)

First action at chat 33 start is to validate the pre-stage rather than rebuild it. Chat-32 close pre-staged all four files: `session.md` (chat-33-IN-PROGRESS state with task brief + process expectations), `status.md` chat-33 placeholder section (7 build-chat sub-headers pre-staged), `todo.md` chat-33 IN PROGRESS line (this section), and `support/next-chat-prompt.md` (slim build-chat kickoff per chat-27 ~500-byte target). At chat 33 start, no overwrites should be needed — just confirmation that all four files are in chat-33 state.

### Step 1 — build SVG #30 for next deferred lesson (primary chat-33 task)

**Streaming-narrative discipline (chat-30 added; chat-31 first build-chat test bed; chat 32 second render-check; this is the fourth overall):** after each milestone, append a short prose paragraph to the chat-33 `status.md` section *immediately*, not at chat close. Use the milestone template already pre-staged in `status.md`.

1. **Lesson pick + markup audit.** Region-scoped reads on both deferred lessons. Per chat-31 milestone-1: RPG has 4-panel crowding risk (stats + XP bar + inventory grid + equipment slots in one viewBox); tower defense's catalog tower types (arrow/cannon/freezer) diverge from the lesson's actual roster (basic/cannon/laser/slow/bank), forcing a build_concept rewrite. Pick on visual-language fit + complexity. Confirm `.canvas-wrapper` anchor + inline canvas styles (chat-15 hardening case expected). Note any wrinkles. → Append Milestone 1 paragraph.
2. **build_concept refinement + SVG file write → catalog flip to `built_unwired_chat_33`.** Land SVG at `images/components/<filename>.svg` (viewBox ~720×400 typical, theme-aware via `prefers-color-scheme: dark`). Catalog status flipped immediately after file write — second exercise of the chat-27 intermediate status. → Append Milestone 2 paragraph.
3. **getBBox text-overflow pre-clear (chat-20 mandatory).** Kicked-off-then-poll. **No `requestAnimationFrame` defensive wait** — chat-31 finding settled in chat 32 (4.6 ms vs 315.2 ms). Compare timing to chat-32's 4.6 ms baseline. → Append Milestone 3 paragraph.
4. **Lesson HTML edits + catalog finalize to `built chat 33`.** Phase 6 svg-wrapper figure inserted (chat-30 convention B placement) + canvas-fallback figure inserted inside `.canvas-wrapper` immediately after primary `<canvas>` (chat-30 prevSibIsCanvas convention). Catalog flipped `built_unwired_chat_33 → built chat 33` and `fallback_alt`/`fallback_caption` tightened. → Append Milestone 4 paragraph.
5. **Pre-stage chat-34 stubs** (session.md + status.md placeholder with render-check sub-headers + todo.md IN PROGRESS line + slim render-check kickoff in next-chat-prompt.md, longer than build-chat kickoff per chat-27 convention). → Append Milestone 5 paragraph.
6. **Chat close** — short wrap-up: Phase 7 status delta (13/15 → 13/15 wired-AND-render-checked unchanged; +1 wired-but-render-pending = chat-33 SVG; deferred drops to 1/15), MCP outage observations, validate-or-revise notes on the streaming-narrative discipline now applied across 4 chats.

### Step 2 (chat 34 work) — render-check the chat-33 SVG

Standard 5-verification-point render-check pipeline at iframe-simulated 380×820. 10th confirmation of the chat-15 `!important` hardening expected (assuming the chat-33 lesson is also a hardening case — every Phase 7 wire so far has been).

### Pre-build-check checklist (chat-17 through chat-32 hard-won lessons + chat-27/30 conventions + chat-31 finding settled in chat 32)

1. **Read `support/session.md` first** (chat-23; validated repeatedly).
2. **Stub `todo.md` + `status.md` writes immediately at chat start** — for chat 33, only validation needed (chat-32 close pre-staged everything including session.md).
3. **Default to region-scoped reads** (chat-27 added; chat-31 used; chat-32 used).
4. **Programmatic getBBox text-overflow pre-clear** as part of build (chat-20 mandatory).
5. **`Claude in Chrome:javascript_tool` does not accept top-level `await`** — kicked-off-then-poll. **Chat-31 finding (now settled in chat 32): do NOT use defensive `requestAnimationFrame()` waits before getBBox calls** (rAF stalls on backgrounded tabs; getBBox triggers layout itself; chat-32 timing of 4.6 ms vs chat-31's 315.2 ms made the verdict overwhelming).
6. **Stream `status.md` narrative incrementally per milestone** (chat-30 added; chat-31 first build-chat application; chat-32 second render-check application; chat-33 will be second build-chat application).
7. **Catalog flow `needs_new_svg → built_unwired_chat_33 → built chat 33`** with the intermediate status flipped immediately after SVG file write, before lesson HTML wiring (chat-27 convention; chat-31 first exercised; this is second).
8. **Save `todo.md` + `status.md` + `session.md` updates at every milestone**, not at chat end.

---

## Chat 32 — ✅ closed clean

**Chat 32 closed clean** — render-check SVG #29 `racing-track-physics.svg` in `genres_racing.html` was completed at iframe-simulated 380×820. All 5 verification points passed. **9th confirmation of the chat-15 `!important` hardening** (canvas inline `style="border: 2px solid #333; display: inline-block; background: #1a1a1a;"` — BOTH `display: inline-block` AND `background: #1a1a1a` patterns present; `enhanced.css` `!important` rule wins, computed display "none"). getBBox re-clear: 25 text/tspan nodes, 0 overflows, all four tightest margins byte-identical to chat-31 build-time (right 5.11 / bottom 15.4 / left 21.02 / top 11.05 px) — confirms no SVG drift. **chat-31 rAF-removal finding strongly validated** — elapsed 4.6 ms vs chat-31's 315.2 ms (68× speedup) and chat-30's 123.8 ms (27×); rAF was the bottleneck, not the bbox walk. Settled convention going forward. Streaming-narrative discipline held across all 6 milestones (Milestone 0 / 1 / 2 / 3 / 4 / 5 + Chat close), no interruption — third consecutive clean exercise (chat 30 + 31 + 32 = 3/3). Phase 7 status delta: 12/15 → **13/15 wired-AND-render-checked clean**; 0 wired-but-render-pending; deferred drops to 2/15 (`genres_rpg` / `genres_tower_defense` remaining). Detailed walkthrough lives in `status.md` → *Phase 7 progress (chat 32 — SVG #29 render-check: `racing-track-physics.svg` in `genres_racing.html`)*.

---

## Chat 31 — ✅ closed clean

**Chat 31 closed clean** — built and wired SVG #29 `racing-track-physics.svg` for `genres_racing.html` in one build chat (deferred → wired). Two-panel diagram: top-down track view with car-at-apex showing 3 labeled vectors (velocity / grip max / required lateral) plus a dashed skid path; friction-circle inset with cross axes and a saturated-plus-overshoot vector pair geometrically tied to panel 1. **First genuine exercise of the chat-27 `built_unwired_chat_N` intermediate catalog status** — flow `needs_new_svg → built_unwired_chat_31 → built chat 31` ran end-to-end with the SVG-on-disk-then-flip step happening before wiring. **First build-chat application of the chat-30 streaming-narrative discipline** — 5 milestone paragraphs appended incrementally to `status.md`, no interruption. getBBox pre-clear caught 1 overflow ("Turn R" axis label by 0.89 px); fixed via 2-edit symmetric label shift; re-run clean (0 overflows, tightest right margin 5.11 px). New chat-31 finding: do NOT use defensive `requestAnimationFrame()` waits before getBBox (rAF stalls on backgrounded tabs; getBBox triggers layout itself). Phase 7 status delta: 12/15 wired-AND-render-checked unchanged; +1 wired-but-render-pending = chat-31 SVG; deferred drops to 2/15. Detailed walkthrough lives in `status.md` → *Phase 7 progress (chat 31 — SVG #29 build: `racing-track-physics.svg` for `genres_racing.html`)*.

---

## Chat 30 — ✅ closed clean

**Chat 30 closed clean** — render-check SVG #28 `playtesting-feedback-loop.svg` in `polish_playtesting.html` was completed at iframe-simulated 380×820. All 5 verification points passed; 8th confirmation of the chat-15 `!important` hardening; chat-30 streaming-narrative discipline successfully exercised end-to-end (6 milestone paragraphs appended incrementally to `status.md` as each step completed; chat-close write was just a short wrap-up). Phase 7 wired-AND-render-checked count went from 11/15 to 12/15. Deferred unchanged at 3/15 (`genres_racing` / `genres_rpg` / `genres_tower_defense`). Detailed walkthrough lives in `status.md` → *Phase 7 progress (chat 30 — SVG #28 render-check)*.

---

## Out-of-scope flags from chat 15 (decide separately if any are worth a focused chat)

1. **`details.toc-card` floating outline overlays canvas-fallback area on mobile.** Sticky `<details class="card toc-card auto-toc">`, z-index 100, ~229 px tall, default-open. Visually covers canvas-fallback figure on phones. Pre-existing (Phase 5 auto-TOC infra). Possible fixes: default-collapsed below 768 px, fully hidden below 768 px, or shrink the sticky height.
2. **Canvas demo JS animation loops keep running on mobile when canvas is hidden** — wasted CPU. Pre-existing across all 53 canvas demos. Easy per-lesson fix (`if (matchMedia('(max-width: 768px)').matches) return;` early-out at top of animation loop) but rolling out to 53 canvases is a script-pass.
3. **Lazy-load on canvas-fallback `<img>`** is correct behavior — noted only because it caused initial diagnostic confusion (`naturalWidth: 0` on first JS query, resolves on scroll). Implication for future render checks: query `naturalWidth` AFTER scrolling into viewport.

---

## Live open questions (full list incl. resolved in `status.md`)

1. `_python.html` companion files — standalone learning resources or appendix code dumps? (3 still missing both Summary + Exercise as of post-Phase-6 audit.)
2. `index.html` — join the design system (CSS vars, theme toggle) or stay bespoke?
