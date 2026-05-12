# Python Game Dev — Course Modernization TODO

> Forward-looking next-chat steering. **Read `support/session.md` first** for the immediate resume pointer; then this file for the next-chat task. Phase-1-through-Phase-8 history lives in per-chat archives at `support/archive/chat-NN.md` (chats 64+) or in this file's git history (chats 30-63). Phase-9 catalog of record: `support/phase9-lint-catalog.json`.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Current state

- **Phases 1–7:** ✅ done. Phase 7 closed at chat 36 (15/15 lessons wired + render-checked clean). 25 Phase-6 SVGs + 16 Phase-7 SVGs shipped clean.
- **Phase 8:** ✅ **CLOSED at chat-84.** 64/64 lessons `done` across 13 modules; 21 per-chat archives (`chat-64.md` through `chat-84.md`); 14 Phase-8 findings + Finding-14 codified at chat-54 (recovery mechanism, ultimately invoked 19+ times across Phases 8+9). Historical detail: `support/archive/chat-84.md` (Phase 8 final archive).
- **Phase 9:** 🔄 **in-progress at chat-100 M2 close** (absorbed into chat-101 cleanup-chat M0 per Finding-14 cross-chat-startup pattern). **11/24+ high-priority lessons linted; cumulative 13 lessons linted = 11 high-priority + 2 medium-priority closeouts.**
  - **2/12 Phase-9 modules complete:** architecture 5/5 (closed chat-92) + polish 5/5 (closed chat-100).
  - **Module partials:** ai 1/5, networking 1/5, graphics 1/5.
  - **Locked decisions** (chat-86 M3): (1) pragmatic dataclass split; (2) type-hint mid-tier; (3) size triage with comprehensive-API-surface SKIP vs game-framework-demo DISTILL.
  - **Locked process** (chat-100 cutover): catalog notes ~1KB target, full-collapse at M2, archives ~3-5KB, briefs ~2KB, session.md ~600B, Finding-19 split-payload protocol mandatory for catalog manual updates.
- **Phase-9 cohort sequence (chats 87+):** chat-87 save_load, chat-89 event_systems, chat-90 component_systems, chat-91 state_machines, chat-92 scene_management (architecture complete), chat-93 ai_pathfinding, chat-94 networking_lag_compensation, chat-95 graphics_procedural, chat-96 polish_difficulty, chat-97 polish_tweening, chat-98 polish_sound, chat-99 polish_screenshake, chat-100 polish_playtesting (polish complete).
- **13 high-priority lessons remain** across genres (4) + networking (3) + physics (3) + sprites (2) + game_mathematics (1).

---

## Chat 102 — 🔄 IN PROGRESS — Phase-9 lint cohort 14 (soft-default `physics_gravity.html`; Ray-confirmation invited at M0)

First chat under post-chat-101-cleanup infrastructure. Target + plan in `support/next-chat-prompt.md`. Opens physics module 0/5 → 1/5 if soft-default lands.

---

## Chat 101 — ✅ closed at M2 (cleanup chat; Finding-14 chat-100-M2 absorption + P0+P1 process trims)

No lint cohort work. Absorbed chat-100 M2 deferral; rewrote `todo.md` 430 KB → 16 KB via flat-index; created `support/closed-phases/` + `support/scripts-archive/` and relocated 14 closed-phase + one-shot artifacts; wrote `support/archive/chat-100.md` (6.8 KB) + `support/archive/chat-101.md` (7.8 KB). See `support/archive/chat-101.md` for detail.

---

## Chat 100 — ✅ closed at M2 via Finding-14 absorption at chat-101 M0

`polish_playtesting.html` linted (Decision 3 SKIP; Decision 1 PASS canonical mixed-finding-retained TWELFTH consecutive; Decision 2 = 27 annotations across 14 atomic pairs). **POLISH MODULE 5/5 COMPLETE** = SECOND complete Phase-9 module. High-priority 11/24+; cumulative 13 lessons. First application of chat-100 process cutover conventions. See `support/archive/chat-100.md`.

---

## Chats 94-99 — ✅ closed (Phase-9 lint-pass cohorts 7-12)

- **Chat 99:** polish_screenshake (334 lines; clean Decision-1-PASS without mixed-finding; 56-annotation/7-pair sweep; Finding-19 split-payload protocol DISCOVERED). See `support/archive/chat-99.md`.
- **Chat 98:** polish_sound (361 lines; THIRD consecutive monolithic-bucket-SKIP; dispersed-method-signature 14-pair sweep). See `support/archive/chat-98.md`.
- **Chat 97:** polish_tweening (342 lines; SECOND monolithic-bucket-SKIP; 12-pair Optional-wrap correction). See `support/archive/chat-97.md`.
- **Chat 96:** polish_difficulty (305 lines; FIRST monolithic-bucket-SKIP at the 5-line-over-threshold boundary case; 21-annotation/8-pair). See `support/archive/chat-96.md`.
- **Chat 95:** graphics_procedural (184 lines; opens graphics module 0/5 → 1/5; 25-annotation/7-pair). See `support/archive/chat-95.md`.
- **Chat 94:** networking_lag_compensation (202 lines; opens networking 0/5 → 1/5; 14-annotation/4-pair). See `support/archive/chat-94.md`.

---

## Chats 30-93 — flat-index

| Chat | Outcome | Archive |
|---|---|---|
| 30 | ✅ closed clean | _(git history)_ |
| 31 | ✅ closed clean | _(git history)_ |
| 32 | ✅ closed clean | _(git history)_ |
| 33 | ✅ closed clean | _(git history)_ |
| 34 | ✅ closed clean (across two attempts; second consecutive recovery exercise) | _(git history)_ |
| 35 | ✅ closed clean (across two attempts; third consecutive recovery exercise) | _(git history)_ |
| 36 | ✅ closed clean (FINAL Phase 7 chat — PHASE 7 CLOSED) | _(git history)_ |
| 37 | ✅ closed clean (Phase 8 kickoff: M2 + stage-38; pilot deferred to chat 38) | _(git history)_ |
| 38 | ✅ closed clean (Phase 8 pilot — pygame_basics_game_loop.html end-to-end) | _(git history)_ |
| 39 | ✅ closed clean (Phase 8 scaffold-script build — 63 lessons injected + Findings 7+8) | _(git history)_ |
| 40 | ✅ closed clean (Phase 8 question-content fill cohort 1 — pygame_basics module 5/5 done) | _(git history)_ |
| 41 | ✅ closed at M2 done (Phase 8 question-content fill cohort 2, partial — 2 of 4 sprite_* lessons… | _(git history)_ |
| 42 | ✅ closed clean (Phase 8 question-content fill cohort-2 finish — sprite_* module 4/4 done = 2nd complete Phase-8 module) | _(git history)_ |
| 43 | ✅ closed clean via interruption-recovery (Phase 8 question-content fill cohort-3 finish… | _(git history)_ |
| 44 | ✅ closed clean via interruption-recovery (Phase 8 question-content fill cohort 4 — physics_* module 5/5 done = 4th complete Phase-8 module) | _(git history)_ |
| 45 | ✅ closed clean (meta-chat: chat-44 M6 recovery + portable INTERRUPTION_RECOVERY.md + chat-46 stage; no cohort work) | _(git history)_ |
| 46 | ✅ closed clean — Phase 8 question-content fill (cohort-5 platformer foundational triplet: character_controller Finding-10 reconciliation… | _(git history)_ |
| 47 | ✅ closed clean — Phase 8 question-content fill (cohort-5 finish: parallax M1 standard authoring… | _(git history)_ |
| 48 | ✅ closed early at M1 via brief-documented drop-the-last-lesson safety-valve | _(git history)_ |
| 49 | ✅ closed clean — Phase 8 question-content fill (cohort-6-finish: polish_sound M1 + polish_tweening M2 standard authoring… | _(git history)_ |
| 50 | ✅ closed clean — Phase 8 question-content fill (cohort 7: polish_difficulty M1 + polish_playtesting M2 standard authoring… | _(git history)_ |
| 51 | ✅ closed early at M1 via brief-documented drop-the-last-lesson safety-valve | _(git history)_ |
| 52 | ✅ closed clean — Phase 8 question-content fill (cohort-8-finish: networking_sockets M1 + networking_client_server M2 standard authoring… | _(git history)_ |
| 53 | ✅ closed early at M1 via brief-documented drop-the-last-lesson safety-valve | _(git history)_ |
| 54 | ✅ closed early at M2 via brief-documented drop-the-last-lesson safety-valve | _(git history)_ |
| 55 | ✅ closed clean at M2 — Phase 8 question-content fill (cohort-10-finish-extended: architecture_scene_management M1 done… | _(git history)_ |
| 56 | ✅ closed clean at M2 (with mid-chat partial-disk-asymmetry at M1+staging-finish boundary absorbed via Finding-14… | _(git history)_ |
| 57 | ✅ closed clean at M2 (with mid-chat partial-todo.md-asymmetry at M1+staging-finish boundary absorbed via Finding-14… | _(git history)_ |
| 58 | ✅ closed clean at M2 (with mid-chat partial-bookkeeping-asymmetry at M1+staging-op-1-finish boundary absorbed via Finding-14… | _(git history)_ |
| 59 | ✅ closed clean at M2 (with mid-chat partial-bookkeeping-asymmetry at M1+catalog-flip-finish boundary absorbed via Finding-14… | _(git history)_ |
| 60 | ✅ closed at M2 (with mid-chat partial-bookkeeping-asymmetry at M1+staging-op-3-finish boundary absorbed via Finding-14… | _(git history)_ |
| 61 | ✅ closed clean at M2 — Phase 8 question-content fill (cohort-17: ai_behavior_trees… | _(git history)_ |
| 62 | ✅ closed at M2 (with mid-chat partial-bookkeeping-asymmetry at M1+catalog-flip-finish boundary absorbed via Finding-14… | _(git history)_ |
| 63 | ✅ closed at M2 (with mid-chat partial-bookkeeping-asymmetry at M1+catalog-flip-finish boundary absorbed via Finding-14… | _(git history)_ |
| 64 | ✅ closed at M2 end-to-end clean — Phase 8 question-content fill (cohort-20: particle_effects… | [chat-64.md](support/archive/chat-64.md) |
| 65 | ✅ closed at M2 (with mid-chat partial-bookkeeping-asymmetry at staging-op-1-to-op-2 boundary absorbed via Finding-14 in-chat-re… | [chat-65.md](support/archive/chat-65.md) |
| 66 | ✅ closed at M2 end-to-end clean — Phase 8 question-content fill (cohort-22: graphics_postprocessing… | [chat-66.md](support/archive/chat-66.md) |
| 67 | ✅ closed at M2 end-to-end clean — Phase 8 question-content fill (cohort-23: graphics_ui_hud… | [chat-67.md](support/archive/chat-67.md) |
| 68 | ✅ closed at M2 end-to-end clean — Phase 8 question-content fill (cohort-24: graphics_procedural… | [chat-68.md](support/archive/chat-68.md) |
| 69 | ✅ closed at M2 end-to-end clean — Phase 8 question-content fill (cohort-25: graphics_shaders… | [chat-69.md](support/archive/chat-69.md) |
| 70 | ✅ closed at M2 end-to-end clean — Phase 8 question-content fill (cohort-26: publishing_executables… | [chat-70.md](support/archive/chat-70.md) |
| 71 | ✅ closed at M2 (back-archived earlier; fat IN-PROGRESS section collapsed at chat-85 historical cleanup pass) | [chat-71.md](support/archive/chat-71.md) |
| 72 | ✅ closed at M2 end-to-end clean — Phase 8 question-content fill (cohort-28: publishing_performance… | [chat-72.md](support/archive/chat-72.md) |
| 73 | ✅ closed at M2 end-to-end clean (collapse pass deferred to chat-75 startup as Op A under Finding-14… | [chat-73.md](support/archive/chat-73.md) |
| 74 | ✅ closed at M2 via Finding-14 cross-chat-startup absorption pattern | [chat-74.md](support/archive/chat-74.md) |
| 75 | ✅ closed at M2 end-to-end clean against the lesson target itself | [chat-75.md](support/archive/chat-75.md) |
| 76 | ✅ closed at M2 via Finding-14 cross-chat-startup absorption pattern | [chat-76.md](support/archive/chat-76.md) |
| 77 | ✅ closed at M2 end-to-end clean against the lesson target itself | [chat-77.md](support/archive/chat-77.md) |
| 78 | ✅ closed at M2 via Finding-14 cross-chat-startup absorption pattern | [chat-78.md](support/archive/chat-78.md) |
| 79 | ✅ closed at M2 via Finding-14 cross-chat-startup absorption pattern | [chat-79.md](support/archive/chat-79.md) |
| 80 | ✅ closed at M2 via chat-81 M2 TWO-CHAT batch (close-at-M0-only via Ray-directed chat-47 context-budget-flagging split at M0/M1… | [chat-80.md](support/archive/chat-80.md) |
| 81 | ✅ closed at M2 end-to-end clean via continuation chat after Ray-directed chat-47 context-budget-flagging split at NEW M1/staging… | [chat-81.md](support/archive/chat-81.md) |
| 82 | ✅ closed at M2 end-to-end clean via chat-82 continuation chat after Ray-directed chat-47 context-budget-flagging split at NEW post-staging-pre… | [chat-82.md](support/archive/chat-82.md) |
| 83 | ✅ closed at M2 end-to-end clean — Phase 8 question-content fill (cohort-38: genres_tower_defense… | [chat-83.md](support/archive/chat-83.md) |
| 84 | ✅ closed at M2 end-to-end clean — Phase 8 question-content fill (cohort-39: genres_tower_defense_python… | [chat-84.md](support/archive/chat-84.md) |
| 85 | ✅ closed at M2 (twenty-second per-chat archive file = first cleanup-chat archive under chat-64-startup discipline) | [chat-85.md](support/archive/chat-85.md) |
| 86 | ✅ closed at M4 (twenty-third per-chat archive file = first Phase-9 archive under chat-64-startup discipline) | [chat-86.md](support/archive/chat-86.md) |
| 87 | ✅ closed at chat-88 M2 (twenty-fourth per-chat archive file = second Phase-9 archive joining `chat-86.md`) | [chat-87.md](support/archive/chat-87.md) |
| 89 | ✅ closed at M2 via Finding-14 cross-chat-startup recovery absorbed at chat-90 M0 startup | [chat-89.md](support/archive/chat-89.md) |
| 90 | ✅ closed at M2 across one mid-chat-resume slice point under Ray-directed "most efficient and less chat tokens" execut… | [chat-90.md](support/archive/chat-90.md) |
| 91 | ✅ closed at M2 end-to-end clean across compaction resume… | [chat-91.md](support/archive/chat-91.md) |
| 92 | ✅ closed at M2 across one compaction-recovery resume… | [chat-92.md](support/archive/chat-92.md) |
| 93 | ✅ closed at M2 via mid-chat Finding-14 absorption pattern… | [chat-93.md](support/archive/chat-93.md) |

> **Note on chat-30-63 sources.** Chats 30-63 predate the chat-64-startup archive-and-collapse discipline; no per-chat archive files exist for them. Full streaming-narrative content for those chats is recoverable from this file's git history (`git show HEAD~1:todo.md` immediately after this cleanup, or `git log -p -- todo.md` for the full window).

---

## Out-of-scope flags from chat 15 (decide separately if any are worth a focused chat)

1. **`details.toc-card` floating outline overlays canvas-fallback area on mobile.** Sticky `<details class="card toc-card auto-toc">`, z-index 100, ~229 px tall, default-open. Visually covers canvas-fallback figure on phones. Pre-existing (Phase 5 auto-TOC infra). Possible fixes: default-collapsed below 768 px, fully hidden below 768 px, or shrink the sticky height.
2. **Canvas demo JS animation loops keep running on mobile when canvas is hidden** — wasted CPU. Pre-existing across all 53 canvas demos. Easy per-lesson fix (`if (matchMedia('(max-width: 768px)').matches) return;` early-out at top of animation loop) but rolling out to 53 canvases is a script-pass.
3. **Lazy-load on canvas-fallback `<img>`** is correct behavior — noted only because it caused initial diagnostic confusion (`naturalWidth: 0` on first JS query, resolves on scroll). Implication for future render checks: query `naturalWidth` AFTER scrolling into viewport.

---

## Live open questions (full list incl. resolved in `status.md`)

1. `_python.html` companion files — standalone learning resources or appendix code dumps? (3 still missing both Summary + Exercise as of post-Phase-6 audit.)
2. `index.html` — join the design system (CSS vars, theme toggle) or stay bespoke?
