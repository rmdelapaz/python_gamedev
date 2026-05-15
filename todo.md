# Python Game Dev — Course Modernization TODO

> Forward-looking next-chat steering. **Read `support/session.md` first** for the immediate resume pointer; then this file for the next-chat task. Phase-1-through-Phase-8 history lives in per-chat archives at `support/archive/chat-NN.md` (chats 64+) or in this file's git history (chats 30-63). Phase-9 catalog of record: `support/phase9-lint-catalog.json`.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Current state

- **Phases 1–7:** ✅ done. Phase 7 closed at chat 36 (15/15 lessons wired + render-checked clean). 25 Phase-6 SVGs + 16 Phase-7 SVGs shipped clean.
- **Phase 8:** ✅ **CLOSED at chat-84.** 64/64 lessons `done` across 13 modules; 21 per-chat archives (`chat-64.md` through `chat-84.md`); 14 Phase-8 findings + Finding-14 codified at chat-54 (recovery mechanism, ultimately invoked 19+ times across Phases 8+9). Historical detail: `support/archive/chat-84.md` (Phase 8 final archive).
- **Phase 9:** 🔄 **in-progress at chat-110 M2 close** (chat-110 = Phase-9 lint cohort 20 on `sprite_animation.html` 352-line opening sprites module 0/2 → 1/2 partial; 33 atomic Decision-2 pairs across Blocks 1-5 split as LARGE-bucket Group A 17 + Group B 16 per chat-105 precedent; Block 6 SKIP at 352 lines = FOURTEENTH consecutive monolithic-bucket-SKIP; Decision 1 PASS NINETEENTH consecutive; both groups dry-run-plus-commit clean first attempt; NEW PRECEDENT: `Filesystem:edit_file` handles up to ~19 KB single-pair payload on current Filesystem MCP without Finding-19 timeout, contradicting older chat-99 ~10 KB threshold finding; NEW PRECEDENT: TWO-PHASE catalog flip via direct `Filesystem:edit_file` (Phase 1 small surgical edits ~1 KB for status/axes/lint_priority/stats + Phase 2 large notes-embed single pair ~19 KB targeting unique `_audit_extras` tail), both phases clean first attempt; NEW PRECEDENT: `Callable[[], None]` for event callbacks; NEW PRECEDENT: pre-flight collision-check on Decision-3-SKIP block contents before staging Decision-2 annotation pairs; NEW PRECEDENT: `pygame.Surface` / `pygame.Rect` annotations OK in blocks without explicit pygame import as forward-references not runtime-evaluated). **17/24+ high-priority lessons linted; cumulative 21 lessons linted = 17 high-priority + 4 medium-priority/catalog-cleanup closeouts.**
  - **5/12 Phase-9 modules complete:** architecture 5/5 (closed chat-92) + polish 5/5 (closed chat-100) + networking 4/5 high-priority (closed chat-105; only medium networking_client_server remains) + game_mathematics 1/1 (closed chat-106) + physics 3/3 (closed chat-109).
  - **Module partials:** ai 1/5, graphics 1/5, sprites 1/2.
  - **Locked decisions** (chat-86 M3): (1) pragmatic dataclass split; (2) type-hint mid-tier; (3) size triage with comprehensive-API-surface SKIP vs game-framework-demo DISTILL.
  - **Locked process** (chat-100 cutover + chat-102 automation cutover + chat-105 per-block-group split-call cutover + chat-106 split-strategy forward-ref precedent + chat-107 MEDIUM-bucket split-call calibration plus full-body-rewrite __init__ disambiguation + chat-108 catalog-flip-in-chat-via-local-script-execution precedent): catalog notes ~2-22KB calibration band, full-collapse at M2, archives ~3-5KB, briefs ~2KB, session.md ~600B, catalog M1 updates via `support/phase9_catalog_update.py` (replaces Finding-19 split-payload protocol); per-block-group dry-run-plus-commit pairs for LARGE sweeps (greater-than-30 atomic pairs) per chat-105 precedent and for MEDIUM sweeps with oldText uniqueness concerns per chat-107 precedent; split-strategy forward-refs for central-class-library plus auxiliary-block lessons per chat-106 precedent; Decision-2 locals-optional clause exempts no-def-no-class blocks per chat-106 precedent; full-body-rewrite for __init__ methods plus docstring-anchor or inline-comment-anchor for collision-prone single-line method signatures per chat-107 precedent; catalog-flip-in-chat via local-script-execution when Claude environment has bash+Python plus Filesystem MCP read access per chat-108 precedent (`Any` for duck-typed object parameters when no concrete class exists in scope; pygame.math.Vector2 for explicit-Vector2 params even when pygame import missing).
- **Phase-9 cohort sequence (chats 87+):** chat-87 save_load, chat-89 event_systems, chat-90 component_systems, chat-91 state_machines, chat-92 scene_management (architecture complete), chat-93 ai_pathfinding, chat-94 networking_lag_compensation, chat-95 graphics_procedural, chat-96 polish_difficulty, chat-97 polish_tweening, chat-98 polish_sound, chat-99 polish_screenshake, chat-100 polish_playtesting (polish complete), chat-103 networking_basics, chat-104 networking_sockets, chat-105 networking_lobby (networking high-priority complete), chat-106 game_mathematics_vectors (game_mathematics complete), chat-107 physics_bounce_friction (physics opens 0/3 → 1/3 partial), chat-108 physics_collision_response (physics 1/3 → 2/3 partial), chat-109 physics_gravity (catalog-flip-only side-quest closing physics 3/3), chat-110 sprite_animation (opens sprites 0/2 → 1/2 partial).
- **5 high-priority lessons remain** across genres (4) + sprites (1). sprites module partial at 1/2 after chat-110 sprite_animation; sprite_groups_layers 445-line remaining. Chat-111 SOFT-DEFAULT: sprite_groups_layers.html 445-line (closes sprites 1/2 → 2/2 high-priority = potential SIXTH complete Phase-9 module; ascending-size discipline within sprites bucket).

---

## Chat 111 — 🔄 IN PROGRESS — Phase-9 lint cohort 21 (soft-default `sprite_groups_layers.html` 445-line closes sprites 1/2 → 2/2 = potential SIXTH complete Phase-9 module; Ray-confirmation invited at M0)

Closes sprites module 1/2 → 2/2 high-priority via ascending-size discipline (sprite_animation 352 closed at chat-110). Alternatives: genres_rpg_python 462 (opens genres bucket), larger genres entries (911/1046/801), ai-module continuation (4 remaining at 153-299), graphics-module continuation (4 remaining at 109-293). Standard chat-86 Decisions 1+2+3 lint pass workflow. ADDITIONAL chat-111 M0 mandatory steps per chat-109 NEW DISCIPLINE: (1) verify chat-110 flip landed by checking `stats.by_lint_pass_status` for `linted_chat_110: 1` key present plus `sprite_animation` entry has `lint_pass_status=linted_chat_110` + `chat_110_lint_pass_notes` payload (~18.5 KB); (2) broader sanity check sampling 2-3 linted entries' disk state against catalog axes (including sprite_animation chat-110 Group A/B annotations on disk). Target + plan in `support/next-chat-prompt.md`.

---

## Chat 110 — ✅ closed at M2 (Phase-9 lint cohort 20; SOFT-DEFAULT sprite_animation.html confirmed clean at M0)

`sprite_animation.html` linted (Decision 3 SKIP at 352-line monolithic Block 6 CompleteAnimationDemo + WalkingCharacter + FlyingCreature + PulsingUI + ExplosionEffect + ClickEffect + SimpleAnimation 8-class comprehensive pygame demo exercising all techniques from Blocks 1-5 in single runnable application, FOURTEENTH consecutive monolithic-bucket-SKIP matching chat-107 BounceAndFrictionDemo shape; Decision 1 PASS canonical clean-no-mixed-finding NINETEENTH consecutive matching chat-104 networking_sockets plus chat-106 game_mathematics_vectors plus chat-107 physics_bounce_friction plus chat-108 physics_collision_response shape; Decision 2 LARGE sweep at 33 atomic edit pairs across Blocks 1-5 split into Group A 17 pairs (Blocks 1+2+3) + Group B 16 pairs (Blocks 4+5) per chat-105 LARGE-bucket precedent, plus 3 from-scratch typing-import-line additions (Block 3 `from typing import Any, Optional`; Block 4 `from typing import Any, Callable, Optional`; Block 5 `from typing import Any, Optional`); both groups dry-run-plus-commit clean first attempt = 4 Filesystem:edit_file invocations total). NEW PRECEDENT: edit_file handles up to ~19 KB single-pair payload on current Filesystem MCP without Finding-19 timeout (contradicting older chat-99 ~10 KB threshold; likely older MCP infrastructure). NEW PRECEDENT: TWO-PHASE catalog flip via direct Filesystem:edit_file (alternative to chat-108 catalog_update.py script): Phase 1 small surgical edits (5 pairs ~1 KB for status/axes/lint_priority/stats) + Phase 2 large notes-embed single pair (~19 KB targeting unique _audit_extras tail); both clean first attempt. NEW PRECEDENT: Callable[[], None] for event callbacks (AnimationWithEvents events dict + add_event callback param). NEW PRECEDENT: pre-flight collision-check on Decision-3-SKIP block contents before staging Decision-2 annotation pairs to catch `def update(self):` / `def update(self, dt):` collisions; chat-110 caught Pair 19 AdvancedAnimation.update collision with Block 6 SimpleAnimation.update, resolved via 4-line extended anchor including `current_image, current_duration = self.frame_data[self.current_frame]`. NEW PRECEDENT: pygame.Surface / pygame.Rect annotations OK in blocks without explicit pygame import (forward-references not runtime-evaluated). sprites module 0/2 high-priority → 1/2 partial = FIRST sprites-module Phase-9 cohort. High-priority 16/24+ → 17/24+; cumulative 20 → 21 lessons linted. Stats final: by_priority high 5 medium 34 skip 25; by_lint_pass_status pending 39 + 21 linted_chat keys (added linted_chat_110: 1) + skipped 4; by_type_hint_coverage none 29 partial 22 full 13. Catalog file 254 KB → 273 KB (+19 KB from chat-110 notes embed). File grew 1313 → 1319 lines on disk. M0 disk-vs-catalog verification caught no drift: chat-109 flips (linted_chat_108 retroactive + linted_chat_109) both confirmed landed cleanly; broader sanity check on polish_difficulty chat-96 + networking_basics chat-103 + physics_bounce_friction chat-107 all clean. OPEN FOLLOW-UP carried forward: physics_bounce_friction catalog type_hint_coverage=none stale despite chat-107 lint pass annotating 4 blocks fully (catalog-flip-only-no-axis-refresh case); future cleanup chat should re-audit. See `support/archive/chat-110.md`.

---

## Chat 109 — ✅ closed at M2 (Phase-9 catalog-flip-only side-quest closing physics 3/3 = FIFTH complete Phase-9 module)

`physics_gravity.html` catalog-flip-only side-quest landed (re-audit refreshed example_solution_size_lines 429 → 108, all_blocks_largest_size 429 → 108, type_hint_coverage none → partial via pre-Phase-9 Block 4 5-typed-defs annotation pass at unknown chat-N, lint_findings emptied, lint_priority high → skip via override). PLUS chat-108 retroactive recovery: physics_collision_response chat-108 flip never landed on Ray WSL catalog pre-chat-109; chat-109 M0 caught the drift by surveying stats.by_lint_pass_status for missing-chat-108 key; chat-108-notes.txt preserved on disk at 17.5 KB used verbatim for retroactive flip. Scope B+ confirmed mid-M1 after M0 surfaced second drift case. NEW PRECEDENT: M0 disk-vs-catalog verification ESCALATED to also check that recent-chat flips actually landed on Ray WSL catalog (chat sequence by_lint_pass_status jumped 87/89/90/91/92/93/94/95/96/97/98/99/100/103/104/105/106/107 → 109 skipping 108 pre-chat-109). NEW PRECEDENT: push final catalog back to Ray WSL via Filesystem:edit_file batch (47-edit ~48 KB payload dry-run-plus-commit clean first attempt; 1 stats block replace + 2 full-entry replaces + 44 surgical insertions for schema-bump-gap pending entries + js_only skipped tags) rather than leaving canonical command for Ray. NEW PRECEDENT: broader sanity check at M0 sampling 2-3 linted entries' disk state. 44 schema-bump-gap pending entries gained explicit `lint_pass_status: pending` (entries audited at chat-86 baseline but never got chat-87-M0 schema-bump). 4 js_only entries gained explicit `lint_pass_status: skipped`. Physics module 2/3 partial → 3/3 complete = FIFTH complete Phase-9 module. Cumulative lessons linted: 18 → 20 (chat-108 retroactive + chat-109 catalog cleanup). Stats final: by_priority high 6 medium 34 skip 24; by_type_hint_coverage none 30 partial 21 full 13; monolithic_python_blocks_gt_300_lines 17. See `support/archive/chat-109.md`.

---

## Chat 108 — ✅ closed at M2 (Phase-9 lint cohort 19; SOFT-DEFAULT physics_collision_response.html confirmed clean at M0)

`physics_collision_response.html` linted (Decision 3 SKIP at 405-line monolithic Block 4 CollisionResponseDemo plus CircleObject plus PolygonObject comprehensive pygame demo bundling THREE collision-shape resolution variants circle-circle + circle-polygon + polygon-polygon plus interactive mouse-spawn plus keyboard handlers, THIRTEENTH consecutive monolithic-bucket-SKIP; Decision 1 PASS canonical clean-no-mixed-finding EIGHTEENTH consecutive matching chat-104 networking_sockets plus chat-106 game_mathematics_vectors plus chat-107 physics_bounce_friction shape; Decision 2 MEDIUM sweep at 20 atomic edit pairs across 4 blocks plus 3 from-scratch typing-import-line additions (Block 1 `from typing import Any`; Block 2 + Block 3 `from typing import Any, Optional` each) = approximately 53 total annotations applied (33 parameter + 4 instance-attribute + 16 return-type); 4 block groups × 2 dry-run-plus-commit = 8 Filesystem:edit_file invocations all clean first attempt). NEW PRECEDENT: catalog-flip-in-chat via local-script-execution (Claude container bash + Python + Filesystem MCP read access; script validates dry-run + commit byte-for-byte; canonical command left for Ray to run on user's WSL filesystem). NEW PRECEDENT: `Any` for duck-typed object parameters when no concrete class exists in scope (Protocol too heavy; string forward-ref technically incorrect); pygame.math.Vector2 for explicit-Vector2 params even when pygame import missing from block (pre-existing teaching-snippet convention; annotations not runtime-evaluated by default). oldText uniqueness verified 16 of 17 atomic pairs via simple single-line match; 1 pair (Block 5 Ball.update) required 3-line inline-comment-anchor (`# Four walls`) disambiguating from 3 same-signature def update methods in SKIP Block 4 (CollisionResponseDemo + CircleObject + PolygonObject). NO chat-106 split-strategy forward-reference applied (no central class library; each block standalone). NO Block-level Decision-2 locals-optional SKIP (each lint-pass block had at least one def or class). physics module 1/3 high-priority → 2/3 partial = SECOND physics-module Phase-9 cohort continuing chat-107-opened physics sequence. High-priority 15/24+ → 16/24+; cumulative 17 → 18 lessons. M0 disk-vs-catalog verification caught brief-drift: chat-106 + chat-107 pending catalog flips per chat-108 brief were ALREADY LANDED on disk at chat-108 M0 startup. Catalog update validated dry-run + commit in Claude container at chat-108 M1; Ray runs `python3 support/phase9_catalog_update.py physics_collision_response.html --chat 108 --notes-file support/chat-108-notes.txt` (17.5 KB notes) on user's WSL filesystem to land identical byte-for-byte result. See `support/archive/chat-108.md`.

---

## Chat 107 — ✅ closed at M2 (Phase-9 lint cohort 18; SOFT-DEFAULT physics_bounce_friction.html confirmed clean at M0)

`physics_bounce_friction.html` linted (Decision 3 SKIP at 373-line monolithic Block 4 BounceAndFrictionDemo plus PhysicsBall comprehensive pygame demo, TWELFTH consecutive monolithic-bucket-SKIP; Decision 1 PASS canonical clean-no-mixed-finding SEVENTEENTH consecutive matching chat-104 networking_sockets plus chat-106 game_mathematics_vectors shape; Decision 2 MEDIUM sweep at 21 atomic edit pairs across 4 blocks plus 1 from-scratch `from typing import Optional` import-line addition (Block 1 for handle_bounce Optional[float] return) = approximately 92 total annotations applied (44 parameter + 31 instance-attribute + 17 return-type); 4 block groups × 2 dry-run-plus-commit = 8 Filesystem:edit_file invocations all clean first attempt). NEW PRECEDENT: full-body-rewrite for __init__ methods provides natural class-specific disambiguation via instance-attr suffix (self.material vs self.on_surface vs self.angular_velocity vs self.bounces); docstring-anchor (Block 3 set_material with `"""Set material properties"""` + update with `"""Update physics"""` plus `# Apply forces` comment) plus inline-comment-anchor (Block 5 apply_force-update merged with `# Gravity each frame (chat-44 M2 pattern)` comment) handle method-signature collisions with same-signature methods in SKIP Block 4 (PhysicsBall.set_material + apply_force; BounceAndFrictionDemo.update). NO chat-106 split-strategy forward-reference applied (no central class library; each block standalone with only external pygame.math.Vector2 references). NO Block-level Decision-2 locals-optional SKIP (each lint-pass block had at least one def or class). physics module 0/3 high-priority → 1/3 partial = FIRST physics-module Phase-9 cohort = FIFTH Phase-9 cohort opening a new module joining chat-94 networking + chat-95 graphics + chat-103 networking-completion-pivot + chat-106 game_mathematics first-and-only. High-priority 14/24+ → 15/24+; cumulative 16 → 17 lessons. Catalog update bundled with M2 close report per chat-104 protocol; Ray runs `python3 support/phase9_catalog_update.py physics_bounce_friction.html --chat 107 --notes-file support/chat-107-notes.txt` (alongside pending chat-106 catalog flip). See `support/archive/chat-107.md`.

---

## Chat 106 — ✅ closed at M2 (Phase-9 lint cohort 17; SOFT-DEFAULT game_mathematics_vectors.html confirmed clean at M0)

`game_mathematics_vectors.html` linted (Decision 3 SKIP at 319-line monolithic Block 8 VectorGame pygame demo, ELEVENTH consecutive monolithic-bucket-SKIP; Decision 1 PASS canonical clean-no-mixed-finding SIXTEENTH consecutive matching chat-104 networking_sockets shape; Decision 2 MEDIUM-LARGE sweep at 36 atomic edit pairs across 8 blocks plus 1 from-scratch `from __future__ import annotations` import-line addition (Block 1) = approximately 85 total annotations applied (50 parameter + 35 return), falling just above the chat-105 30-pair LARGE threshold; 4 block groups × 2 dry-run-plus-commit = 8 Filesystem:edit_file invocations all clean first attempt). NEW PRECEDENT: split-strategy forward-references (central class library Block 1 received `from __future__ import annotations` for unquoted self-references; auxiliary Blocks 3-7, 9 used string forward-refs `"Vector2"`; Block 10 used PEP 585 lowercase `list[float]` for plain-list practice-exercise helpers). NEW PRECEDENT: Block-level SKIP under Decision-2 locals-optional clause for Block 2 (15-line module-level vector-arithmetic demo with zero def or class definitions). One diagnostic shift from brief premise: Block 1 turned out to be a 60-line Vector2 class library (not the monolithic) and Block 8 was the 319-line VectorGame pygame demo (the monolithic); SKIP rationale unchanged. game_mathematics module 0/1 → 1/1 = FOURTH complete Phase-9 module after architecture + polish + networking. High-priority 13/24+ → 14/24+; cumulative 15 → 16 lessons. Catalog update bundled with M2 close report per chat-104 protocol; Ray runs `python3 support/phase9_catalog_update.py game_mathematics_vectors.html --chat 106 --notes-file support/chat-106-notes.txt`. See `support/archive/chat-106.md`.

---

## Chat 105 — ✅ closed at M2 (Phase-9 lint cohort 16; SOFT-DEFAULT networking_lobby.html confirmed clean at M0)

`networking_lobby.html` linted (Decision 3 SKIP at 609-line NEW HIGH-WATER monolithic-bucket cohort, 145 lines above prior high from chat-103 networking_basics 464; TENTH consecutive monolithic-bucket-SKIP; Decision 1 PASS canonical mixed-finding-retained-under-override FIFTEENTH consecutive matching chat-94 partial-dataclass-plus-2-findings shape; Decision 2 = approximately 158 annotations across 84 atomic edit pairs spanning 5 block groups plus 1 from-scratch typing-import-line addition (Block 3) plus 1 in-place typing-import-line extension (Block 1) = NEW LARGEST Decision 2 sweep across Phase-9 history exceeding chat-104 record of 115 annotations / 34 pairs by 43 annotations and 50 pairs). NEW PRECEDENT: per-block-group dry-run-plus-commit pairs for LARGE sweeps (greater-than-30 atomic pairs); 4 block groups × 2 invocations = 8 Filesystem:edit_file calls all clean first attempt. Networking 4/5 partial (only medium-priority networking_client_server remains). High-priority 13/24+ to 14/24+; cumulative 15 to 16 lessons linted. Catalog update bundled with M2 close report per chat-104 protocol; Ray runs `python3 support/phase9_catalog_update.py networking_lobby.html --chat 105 --notes-file support/chat-105-notes.txt`. See `support/archive/chat-105.md`.

---

## Chat 104 — ✅ closed at M2 (Phase-9 lint cohort 15; SOFT-DEFAULT networking_sockets.html confirmed clean at M0)

`networking_sockets.html` linted (Decision 3 SKIP at 320-line SMALLEST monolithic-bucket cohort to date; NINTH consecutive monolithic-bucket-SKIP; Decision 1 PASS canonical clean-no-mixed-finding FOURTEENTH consecutive matching chat-99 shape; Decision 2 = 115 annotations across 34 atomic pairs plus 3 from-scratch typing-import-line additions = LARGEST Decision 2 sweep across Phase-9 history). NEW PRECEDENT: catalog `example_solution_size_lines` axis bumps under from-scratch typing-import-line additions (Block 1 320 to 321 on-disk; does NOT shift Decision 3 classification; catalog notes document this for future chat reference). PEP 585 lowercase `list`/`dict` pattern established for auxiliary-block annotations. Networking 3/5 partial. High-priority 12/24+ to 13/24+; cumulative 15 lessons. See `support/archive/chat-104.md`.

---

## Chat 103 — ✅ closed at M2 (Phase-9 lint cohort 14; pivoted from physics_gravity to networking_basics at M0 after catalog-stale finding)

`networking_basics.html` linted (Decision 3 SKIP at 464-line comprehensive client-server-API-surface bundle = LARGEST monolithic-bucket SKIP to date; Decision 1 PASS canonical mixed-finding-retained THIRTEENTH consecutive; Decision 2 = 42 annotations across 25 atomic pairs). FIRST production invocation of chat-102 `phase9_catalog_update.py` script (clean; stats refreshed first time since chat-86). Networking 2/5 partial. NEW finding: physics_gravity catalog-stale (on-disk Block 4 already distilled outside Phase-9; sampling confirmed isolated). High-priority 11/24+ → 12/24+; cumulative 14 lessons. See `support/archive/chat-103.md`.

---

## Chat 102 — ✅ closed at M2 (automation-infrastructure meta-chat; no lint cohort)

Wrote `support/phase9_catalog_update.py` replacing Finding-19 split-payload protocol for catalog M1 updates; extended `support/phase9_lint_audit.py` with `load_prior_chat_notes()` preserving ~96 KB of chat_NN_lint_pass_notes across audit re-runs; moved stale chat-64-startup one-shot `compact_todo.py` to `support/scripts-archive/`. See `support/archive/chat-102.md` for detail.

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
