# Python Game Dev — Course Modernization TODO

> Context handoff for the next chat. Captures everything done so far, what's queued
> next, key conventions, and open questions. Living doc — update as work progresses.

**Project root:** `\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev`
(Use `\\wsl$\` paths, not `\\wsl.localhost\`.)

---

## Status — Phases 1–5 complete, 6+ pending

| Phase | What | Status |
|---|---|---|
| 1 | Theme system foundation (CSS vars, dark/light toggle support) | ✅ done |
| 2 | Top nav + `nav-enhancements.js` injected across 64 lessons | ✅ done |
| 3 | Dark-mode polish for inline-styled boxes (`#f0f8ff`, `#fff5f5`, `#f9f9f9`) + mermaid container | ✅ done |
| 4 | Audit script written, run, bug-fixed | ✅ done (script ready to re-run) |
| 5 | Section-ID injection script + auto-TOC JS + CSS | ⚠️ code in place, **script not yet run** |
| 6 | Reusable SVG component library | ⏳ next |
| 7 | Mobile fallbacks for canvas demos | ⏳ |
| 8 | Pedagogy upgrade (formal exercises + quizzes) | ⏳ |
| 9 | Code quality / lint pass | ⏳ |

---

## Immediate actions (do these first in next chat)

```bash
cd ~/projects/python_gamedev

# 1. Rename misnamed Python file (it's a .py with .html extension)
mv genres_racing_python.html genres_racing_python.py

# 2. Run Phase 5 script — adds id="..." to every <h2>/<h3>
python3 inject_section_ids.py --dry-run
python3 inject_section_ids.py

# 3. Re-run audit with the bug-fixed script for a clean post-Phase-5 baseline
python3 audit_lessons.py --csv audit-post-phase5.csv

# 4. Eyeball a couple of lessons in browser to confirm the auto-TOC appears
#    (lessons with 3+ <h2>s will sprout a sticky TOC under the lesson <h1>)

# 5. After verifying, clean up backups
rm *.html.bak
```

After step 2, every lesson with 3+ H2 headings will sprout a sticky, FAB-collapsing
auto-TOC at runtime. The CSS and JS are already in place.

---

## Files created/modified across all phases

### CSS / JS (the design system)
- `styles/enhanced.css` — extended with: CSS variables, dark/light theme rules,
  sticky top nav, mobile hamburger, dark-mode polish for inline boxes, FAB-collapse
  auto-TOC styles. Phase 1, 2, 3, and 5 work all live here. Original
  `@media (prefers-color-scheme: dark)` block was rewritten to be conditional on
  `:root:not([data-theme="light"])` so the manual toggle wins.
- `styles/main.css` — **untouched** (legacy Eric Meyer reset + fixed-px margins).
  Hardcoded white on `.mermaid` containers and `!important` dark text on mermaid
  labels were addressed via overrides in `enhanced.css`, not by editing main.css.
- `js/course-enhancements.js` — **untouched** (mostly Prism.js bundle plus
  reading-time / progress-bar / keyboard-nav). Kept modular by design.
- `js/nav-enhancements.js` — **new file** containing: theme toggle (with localStorage
  persistence), mobile menu open/close, mermaid theme reinit on toggle, auto-TOC
  builder. All initialized on `DOMContentLoaded`.
- `js/clipboard.js` — **untouched**.

### Scripts (the migration tooling)
- `inject_main_nav.py` — Phase 2. Already run. Injected nav block + script tag
  into all 64 lessons; upgraded mermaid `<script type="module">` to expose
  `window.__mermaid` and pick initial theme.
- `audit_lessons.py` — Phase 4. Bug-fixed for canvas size + section-ID counting.
  Ready to re-run for clean post-Phase-5 numbers.
- `inject_section_ids.py` — Phase 5. **Not yet run.** Slugifies H2/H3 text into
  stable `id` attributes; idempotent.

### Lessons (the content, after Phases 1–3)
- All 64 `*.html` lesson files have:
  - `<script src="...js/nav-enhancements.js" defer></script>` in `<head>`
  - `<nav class="main-nav">…</nav>` after `<body>` (preserving skip-to-main + progress-indicator placement)
  - Upgraded mermaid module init (where mermaid was present)
- `index.html` — **untouched by injection** (excluded by default). Has its own
  bespoke inline `<style>` block for course-hero + module-section. Doesn't
  currently flip on theme toggle. Decide whether to bring it into the system in
  a later phase.
- `genres_racing_python.html` — **misnamed**, actually a Python source file.
  Rename to `.py` (see Immediate Actions).

---

## Audit findings (key insights from Phase 4)

Run produced: 65 files analyzed, average **471 words / 402 code lines per lesson**.
Lessons are code-heavy and prose-light — pedagogical density lives in code samples.

**Universal gaps (every lesson):**
- 0 static SVGs anywhere — Phase 6 target
- 0 quizzes anywhere — Phase 8 target

**Outliers worth attention:**
- `architecture_state_machines.html` — thinnest standalone lesson (1 H2, 61 lines, no exercise)
- 4 `_python.html` companion files (`genres_puzzle_python.html`,
  `genres_strategy_python.html`, `genres_tower_defense_python.html`,
  `genres_rpg_python.html`) — all lack a Summary section, look like code-only
  appendices. Decide if they should be standalone or restructured.
- `networking_lobby.html` (1304 lines), `genres_tower_defense_python.html`
  (1100 lines), `networking_sockets.html` (864 lines), `sprite_groups_layers.html`
  (806 lines) — heavy code, candidates for `<details>`-collapsing the longest
  blocks behind a "show full code" toggle.

The audit's `has_summary` flag is permissive — it counts "What's Next" sections,
which are common. So a ✓ doesn't mean the lesson has a real "Key Takeaways" wrap-up.
A stricter pass is hand work.

---

## Phase 6 — SVG component library (next chat priority)

Goal: hand-craft 10–15 reusable, theme-aware SVG templates that fill the gap
between abstract mermaid flowcharts and full canvas demos. They work on mobile
(canvas demos don't), they communicate spatial/structural concepts mermaid can't,
and they theme cleanly via the CSS variables we already have.

**Approach:**
- Standalone files in `images/components/` directory, OR inline `<svg>` snippets
  pasted into lessons. Decide which.
- Use `var(--text-color)`, `var(--card-bg)`, `var(--border-color)`,
  `var(--primary-color)` for theming.
- 800×600 max footprint to feel intentional next to canvas demos. Internally
  they should scale via `viewBox`.

**Suggested initial set (priority order):**

1. **Vector diagram** — object with labeled velocity arrow. Reused everywhere
   (physics, AI movement, networking lag). Parameterize: position, vector
   direction, label.
2. **Force diagram** — object with gravity + normal force + friction arrows
   (physics_gravity, physics_bounce_friction, physics_collision_response).
3. **Packet structure** — header / payload / checksum byte breakdown
   (networking_basics, networking_sockets).
4. **Network topology** — client-server vs P2P vs star vs mesh, side-by-side
   (networking_basics, networking_client_server).
5. **Pixel grid** — sprite or sampling pattern with labeled cells
   (sprite_loading_images, sprite_sheets, graphics_lighting).
6. **Sprite sheet layout** — grid showing animation frames
   (sprite_animation, sprite_sheets).
7. **Scene graph** — tree structure with labeled nodes
   (architecture_scene_management, architecture_component_systems).
8. **State machine** — proper labeled state diagram with transitions
   (better than mermaid for these — `architecture_state_machines`,
   `ai_state_machines`).
9. **Pathfinding grid** — A* with labeled costs/parents
   (ai_pathfinding).
10. **FOV cone** — vision range with angle (ai_state_machines, ai_decision_making).
11. **Animation strip** — frame timing diagram (sprite_animation, polish_tweening).
12. **Save file structure** — JSON tree visualization (architecture_save_load).
13. **Component diagram** — entity + components with labels
    (architecture_component_systems).
14. **Lighting model** — ambient + diffuse + specular contribution
    (graphics_lighting).
15. **Parallax layers** — side view of multiple scrolling planes
    (platformer_parallax).

**Process:** start with 3–5 in next chat, paste them into 2–3 representative
lessons, see how they read alongside existing content. Iterate on the format.
Then expand to the full set once the format is locked.

---

## Phase 7 — Mobile fallbacks for canvases

`<canvas>` elements are hidden on mobile via `enhanced.css` rule
`canvas { display: none; }`. The existing `.mobile-diagram-note` is a generic
apology, not a substitute.

**Approach (sketch):**
- Script wraps every `<canvas>` in a `<div class="canvas-with-fallback">`
  containing canvas + a static SVG (from Phase 6 library) + descriptive caption.
- CSS swaps which is visible based on viewport width.
- Need a per-lesson mapping: which canvas demo gets which SVG fallback.

Probably needs a JSON catalog file mapping `lesson_filename` →
`canvas_id` → `fallback_svg_name`. Hand-curated.

---

## Phase 8 — Pedagogy upgrade (per-lesson, hand work)

Add formal "Practice Exercise" + 3-question quiz section to each lesson, mirroring
python_intro's pattern.

**Quiz markup (from python_intro):**
```html
<div class="card quiz-container">
    <h3>🎯 Quick Quiz</h3>
    <div class="quiz-question">
        <p><strong>Question 1:</strong> ...</p>
        <div class="quiz-options">
            <button class="quiz-option" data-correct="false" data-hint="...">A) ...</button>
            <button class="quiz-option" data-correct="true" data-explanation="...">B) ...</button>
            <button class="quiz-option" data-correct="false" data-hint="...">C) ...</button>
        </div>
        <div class="quiz-feedback"></div>
    </div>
</div>
```

The quiz JS is already in `js/course-enhancements.js` for python_intro but **NOT
in python_gamedev's `course-enhancements.js`** (which is mostly Prism). Will
need to either port the quiz init code or add it to nav-enhancements.js.

**Process:** could scaffold with a script that injects empty quiz/exercise
templates into each lesson, then humans fill in actual questions. Or do it
purely by hand a few lessons at a time.

---

## Phase 9 — Code quality pass

Lint script flags inconsistent style across lessons:
- Mixed dataclass usage (some lessons use `@dataclass`, some don't)
- Inconsistent type hints
- Drifting class naming conventions
- Long monolithic class examples vs. focused snippets

Hand rewrites of worst offenders. Could use `pylint` or `ruff` programmatically
but the variance is more about pedagogical consistency than code correctness.

---

## Smaller items mentioned but not scoped yet

- **Standardize breadcrumb format** — each lesson hand-codes its own crumb
  ("Section 4: Game Physics - Lesson 5", "Advanced Module - Section 1: Advanced
  Graphics - Lesson 2"). Script could rewrite using a JSON catalog of
  module/section/lesson structure.
- **"Lesson X of N in <Module>" indicator** — same JSON catalog drives this.
- **Index.html theme polish** — index has its own purple/teal hero in inline
  `<style>`. Currently doesn't flip on theme toggle. Either add `--include-index`
  to the next inject script run, or hand-edit index's inline styles to use
  CSS variables.
- **Path style inconsistency** — some lessons use absolute `/styles/main.css`,
  others relative `styles/main.css`. `inject_main_nav.py` handled this per-file
  for new script tags, but the existing CSS/icon links remain mixed. Script
  could normalize to all-relative for portability.
- **Decide fate of `_python.html` companion files** — standalone lessons or
  appendix code? If appendix, should they be linked from their parent lesson
  rather than appearing in the navigation as siblings?

---

## Conventions / things to remember

- **Filesystem tool > computer use tool** for all WSL file ops in this project
- **Prefer `edit_file` over `write_file`** for existing files (less rewrite risk)
- **Warn when conversation is getting long** rather than letting auto-compaction hit
- **Don't add content not present in existing lessons** unless explicitly requested
- **Don't add PetalFawnStudio branding** unless explicitly requested
- **Path: `\\wsl$\Ubuntu\…`** not `\\wsl.localhost\Ubuntu\…`
- All injection scripts in this project follow the same shape: idempotent,
  `--dry-run`, `--no-backup`, `.bak` sibling files, color terminal output, summary
  block at end. Use `migrate_toc_summary.py` / `inject_main_nav.py` /
  `inject_section_ids.py` as references when writing the next one.

---

## Sister projects (for cross-reference)

- **python_intro** — completed, 10 lessons. FAB-collapse TOC done. Hand-coded
  per-lesson TOC (vs gamedev's auto-built TOC). Source of truth for the design
  system patterns.
- **python_intermediate** — completed, 12 lessons. FAB-collapse TOC done via
  `migrate_toc_summary.py` script with regex tolerance for both
  `Sticky Table of Contents` and `Table of Contents` comments.
- **python_gamedev** — in progress (this project). Different shape: 64 topic-named
  lessons rather than sequential `lesson_NN.html`, much heavier reliance on
  `<canvas>` interactive demos.

---

## Open questions for next chat

1. Should Phase 6 SVGs be standalone files (`images/components/*.svg`) or
   inline snippets pasted into lessons? Standalone is more reusable but adds
   HTTP requests. Inline is heavier but self-contained per lesson.
2. Are the `_python.html` companion files meant to be standalone learning
   resources, or appendix code dumps for their parent lessons? Determines
   whether they need summaries/exercises or should be restructured.
3. Should `index.html` join the design system (CSS vars, theme toggle) or stay
   bespoke? Currently doesn't theme-flip.
4. Phase 7 (mobile fallbacks) needs a per-canvas → per-SVG mapping. Build the
   catalog by hand, or have a script auto-suggest based on filename keywords?
