#!/usr/bin/env python3
"""
wrap_canvas_fallbacks.py  \u2014  Phase 7

Wraps <canvas> elements in canvas-heavy lessons with a static SVG fallback
for mobile users (where the existing CSS rule
    @media (max-width: 768px) { canvas { display: none; } }
hides the live demo).

Reads per-lesson mappings from phase7-canvas-fallback-catalog.json. For each
canvas in a target lesson:
  \u2022 Locate every <canvas \u2026></canvas> tag.
  \u2022 If the wrap marker (class="canvas-fallback") already follows the canvas
    within ~600 chars, skip it (idempotent).
  \u2022 Otherwise inject a <figure class="canvas-fallback">\u2026</figure> snippet
    immediately after the canvas tag, inside the existing .canvas-wrapper.

Lessons whose fallback SVG file does not yet exist in /images/components/ are
"deferred" and listed in the run summary \u2014 the script does not modify those
files. Once the SVG is built, re-run the script and they get wrapped.

Usage examples:
    python wrap_canvas_fallbacks.py --dry-run
    python wrap_canvas_fallbacks.py
    python wrap_canvas_fallbacks.py --no-backup
    python wrap_canvas_fallbacks.py --lesson networking_basics.html
    python wrap_canvas_fallbacks.py --status reuse
    python wrap_canvas_fallbacks.py --lesson polish_tweening.html --dry-run

Conventions follow inject_main_nav.py / inject_section_ids.py:
  \u2022 Idempotent. Re-runs are safe.
  \u2022 --dry-run reports what would change.
  \u2022 .bak siblings written by default; --no-backup to skip.
  \u2022 Color terminal output, summary block at end.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# ---- ANSI colors (mirrors the other inject scripts) ----
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


PROJECT_ROOT = Path(__file__).parent.resolve()
CATALOG_PATH = PROJECT_ROOT / "phase7-canvas-fallback-catalog.json"
COMPONENTS_DIR = PROJECT_ROOT / "images" / "components"

# Match an entire <canvas \u2026></canvas> element (or <canvas \u2026 /> if anyone ever
# self-closes one). Lazy on attributes, lazy on inner content so we don't span
# multiple canvases. re.DOTALL so a multi-line canvas tag still matches.
CANVAS_TAG_RE = re.compile(
    r"(<canvas\b[^>]*?>(?:.*?</canvas>)?)",
    re.IGNORECASE | re.DOTALL,
)

WRAP_MARKER = 'class="canvas-fallback"'
LOOKAHEAD_CHARS = 600  # how far past the canvas to scan for an existing fallback


def _esc(text: str) -> str:
    """Minimal HTML-attribute escaping for alt/caption text from the catalog."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


def fallback_snippet(svg: str, alt: str, caption: str) -> str:
    """Render the <figure> snippet to inject after a <canvas> tag.

    Indentation matches the typical 4-space lesson markup and leaves a leading
    newline so the figure sits on its own line below the canvas.
    """
    return (
        "\n        <figure class=\"canvas-fallback\">\n"
        f"            <img src=\"/images/components/{svg}\"\n"
        f"                 alt=\"{_esc(alt)}\"\n"
        "                 class=\"responsive-svg\"\n"
        "                 loading=\"lazy\">\n"
        f"            <figcaption>{_esc(caption)}</figcaption>\n"
        "        </figure>"
    )


def wrap_lesson(
    file_path: Path,
    entry: dict,
    *,
    dry_run: bool,
    backup: bool,
) -> dict:
    """Process one lesson file. Returns a stats dict."""
    if not file_path.exists():
        return {"status": "missing", "wrapped": 0, "skipped": 0}

    text = file_path.read_text(encoding="utf-8")
    original = text

    svg = entry["fallback_svg"]
    alt = entry.get("fallback_alt") or entry.get("fallback_caption", svg)
    caption = entry["fallback_caption"]
    snippet = fallback_snippet(svg, alt, caption)

    wrapped = 0
    skipped = 0

    # Track replacements via a running offset so the lookahead stays correct
    # against the *original* text (we don't want a freshly-inserted figure to
    # look like a "skip" trigger for the next canvas in the same file).
    out_parts: list[str] = []
    last_end = 0
    for m in CANVAS_TAG_RE.finditer(original):
        out_parts.append(original[last_end:m.start()])
        canvas_tag = m.group(1)
        lookahead = original[m.end(): m.end() + LOOKAHEAD_CHARS]
        if WRAP_MARKER in lookahead:
            out_parts.append(canvas_tag)
            skipped += 1
        else:
            out_parts.append(canvas_tag)
            out_parts.append(snippet)
            wrapped += 1
        last_end = m.end()
    out_parts.append(original[last_end:])
    new_text = "".join(out_parts)

    if new_text == original:
        return {"status": "noop", "wrapped": wrapped, "skipped": skipped}

    if dry_run:
        return {"status": "would-update", "wrapped": wrapped, "skipped": skipped}

    if backup:
        bak = file_path.with_suffix(file_path.suffix + ".bak")
        shutil.copy2(file_path, bak)
    file_path.write_text(new_text, encoding="utf-8")
    return {"status": "updated", "wrapped": wrapped, "skipped": skipped}


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Wrap <canvas> elements with mobile SVG fallbacks (Phase 7).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without writing files.",
    )
    ap.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not write .bak sibling files when applying.",
    )
    ap.add_argument(
        "--lesson",
        action="append",
        metavar="FILENAME",
        help="Limit to specific lesson filename(s). Can be repeated.",
    )
    ap.add_argument(
        "--status",
        choices=["reuse", "needs_new_svg"],
        help="Limit to lessons with this catalog status.",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    if not CATALOG_PATH.exists():
        print(f"{RED}Catalog missing:{RESET} {CATALOG_PATH}", file=sys.stderr)
        return 1

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    lessons = catalog.get("lessons", {})

    if not lessons:
        print(f"{YELLOW}Catalog has no lessons.{RESET}", file=sys.stderr)
        return 1

    # --- filter ---
    selected: dict[str, dict] = {}
    for fn, entry in lessons.items():
        if args.lesson and fn not in args.lesson:
            continue
        if args.status and entry.get("status") != args.status:
            continue
        selected[fn] = entry

    if not selected:
        print(f"{YELLOW}No lessons match the requested filters.{RESET}")
        return 0

    # --- partition by SVG availability ---
    ready: dict[str, dict] = {}
    deferred: dict[str, dict] = {}
    for fn, entry in selected.items():
        svg_path = COMPONENTS_DIR / entry["fallback_svg"]
        (ready if svg_path.exists() else deferred)[fn] = entry

    print(f"{CYAN}{BOLD}Phase 7 \u2014 Canvas Fallback Wrapper{RESET}")
    print(f"{DIM}Catalog:  {CATALOG_PATH.name}{RESET}")
    print(f"{DIM}Project:  {PROJECT_ROOT}{RESET}")
    print(
        f"{DIM}Selected: {len(selected)} (ready: {len(ready)}, "
        f"deferred: {len(deferred)}){RESET}"
    )
    if args.dry_run:
        print(f"{YELLOW}[DRY RUN] no files will be written{RESET}")
    print()

    totals = {
        "updated": 0,
        "would-update": 0,
        "noop": 0,
        "missing": 0,
        "wrapped": 0,
        "skipped": 0,
    }

    if ready:
        print(f"{BOLD}Ready (SVG present, lessons processed):{RESET}")
        for fn, entry in sorted(ready.items()):
            path = PROJECT_ROOT / fn
            result = wrap_lesson(
                path, entry, dry_run=args.dry_run, backup=not args.no_backup
            )
            totals[result["status"]] = totals.get(result["status"], 0) + 1
            totals["wrapped"] += result["wrapped"]
            totals["skipped"] += result["skipped"]

            status = result["status"]
            color = {
                "updated": GREEN,
                "would-update": YELLOW,
                "noop": DIM,
                "missing": RED,
            }.get(status, "")
            tag = entry.get("status", "?")
            print(
                f"  {color}{status:>14}{RESET}  {fn:<40}  "
                f"[{tag:>14}]  wrapped={result['wrapped']} "
                f"skipped={result['skipped']}  \u2192 {entry['fallback_svg']}"
            )

    if deferred:
        print()
        print(
            f"{BOLD}Deferred{RESET} {DIM}(SVG not yet built \u2014 run again later):{RESET}"
        )
        for fn, entry in sorted(deferred.items()):
            tag = entry.get("status", "?")
            print(
                f"  {DIM}{'deferred':>14}{RESET}  {fn:<40}  "
                f"[{tag:>14}]  needs {entry['fallback_svg']}"
            )

    print()
    print(f"{CYAN}{BOLD}Summary:{RESET}")
    for k in ("updated", "would-update", "noop", "missing"):
        if totals.get(k):
            print(f"  {k}: {totals[k]}")
    if deferred:
        print(f"  deferred lessons: {len(deferred)}")
    print(f"  total canvases wrapped this run: {totals['wrapped']}")
    print(f"  total canvases already wrapped (skipped): {totals['skipped']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
