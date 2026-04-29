#!/usr/bin/env python3
"""
audit_lessons.py

Scan every lesson HTML file in a course directory and produce a content-audit
report: per-file metrics + a summary identifying outliers and gaps.

Designed for the python_gamedev course but works on any directory of HTML
lessons that follow a similar shape.

What it measures per file:
    words             approx prose word count (HTML stripped)
    h2 / h3           section/sub-section counts
    mermaid           number of <div class="mermaid"> diagrams
    canvas            number of <canvas> elements (interactive demos)
    canvas_px         total area in pixels (rough proxy for demo size)
    static_svg        number of authored <svg> elements (NOT mermaid output)
    img               <img> tag count
    code_blocks       number of <pre> blocks
    code_lines        total lines of code inside <pre>
    inline_boxes      inline-style colored boxes (info/note/neutral)
    section_ids       count of elements with an id (anchors for TOC)
    has_summary       has a "Summary" / "Takeaways" / "Wrap-up" section
    has_exercise      contains "Exercise" or "Practice" headings
    has_quiz          contains a quiz section
    has_lesson_nav    has a <nav class="lesson-nav"> (prev/next)
    clipboard_js      references clipboard.js
    course_enh_js     references course-enhancements.js

Outputs:
    - A markdown table to stdout (one row per file)
    - A summary block flagging gaps (no summary, no exercise, etc.)
    - Optionally a CSV file if --csv PATH is passed

Usage:
    python3 audit_lessons.py                        # current dir
    python3 audit_lessons.py /path/to/python_gamedev
    python3 audit_lessons.py --csv audit.csv        # also write CSV
    python3 audit_lessons.py --pattern "lesson_*.html"
    python3 audit_lessons.py --include-index
    python3 audit_lessons.py --sort words           # sort by column
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

TITLE_RE         = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
H2_RE            = re.compile(r"<h2[^>]*>", re.IGNORECASE)
H3_RE            = re.compile(r"<h3[^>]*>", re.IGNORECASE)
MERMAID_RE       = re.compile(r'<div\s+[^>]*class="[^"]*\bmermaid\b[^"]*"', re.IGNORECASE)
CANVAS_TAG_RE    = re.compile(r'<canvas\b[^>]*>', re.IGNORECASE)
CANVAS_W_RE      = re.compile(r'\bwidth\s*=\s*["\']?(\d+)["\']?', re.IGNORECASE)
CANVAS_H_RE      = re.compile(r'\bheight\s*=\s*["\']?(\d+)["\']?', re.IGNORECASE)
SVG_RE           = re.compile(r"<svg\b[^>]*>", re.IGNORECASE)
IMG_RE           = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
PRE_BLOCK_RE     = re.compile(r"<pre[^>]*>(.*?)</pre>", re.IGNORECASE | re.DOTALL)
INLINE_BOX_RE    = re.compile(
    r'style="[^"]*background(?:-color)?:\s*#(?:f0f8ff|fff5f5|f9f9f9)',
    re.IGNORECASE,
)
# Only IDs that live on heading elements count as "section anchors"
HEADING_WITH_ID_RE = re.compile(
    r'<h[234]\b[^>]*\bid\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)
SCRIPT_SRC_RE    = re.compile(r'<script[^>]+src="([^"]+)"', re.IGNORECASE)
LESSON_NAV_RE    = re.compile(r'<nav[^>]*class="[^"]*lesson-nav', re.IGNORECASE)

# Heading text for "summary"-ish sections
SUMMARY_RE = re.compile(
    r"<h[23][^>]*>[^<]*(?:summary|takeaways|wrap[- ]?up|key points|recap|conclusion|what's next|next steps)",
    re.IGNORECASE,
)
EXERCISE_RE = re.compile(
    r"<h[23][^>]*>[^<]*(?:exercise|practice|try it|challenge|hands[- ]on)",
    re.IGNORECASE,
)
QUIZ_RE = re.compile(
    r'(?:<h[23][^>]*>[^<]*quiz)|(?:class="[^"]*quiz-)',
    re.IGNORECASE,
)

# IDs that are not content section anchors (kept for documentation; no longer used
# now that section_ids only counts ids on h2/h3/h4 elements)
NON_CONTENT_IDS = {
    "main-content", "nav-links", "mobile-menu-toggle", "theme-toggle",
    "search-input", "search-results", "print-button", "overall-progress",
}


# ---------------------------------------------------------------------------
# Tag stripping & word counting
# ---------------------------------------------------------------------------

SCRIPT_STYLE_BLOCK_RE = re.compile(
    r"<(script|style)\b[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL
)
PRE_BLOCK_STRIP_RE = re.compile(r"<pre\b[^>]*>.*?</pre>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def strip_to_text(html: str) -> str:
    # Remove <script>, <style>, <pre> blocks (they're not prose)
    no_scripts = SCRIPT_STYLE_BLOCK_RE.sub(" ", html)
    no_pre = PRE_BLOCK_STRIP_RE.sub(" ", no_scripts)
    no_tags = TAG_RE.sub(" ", no_pre)
    return WS_RE.sub(" ", no_tags).strip()


def count_words(text: str) -> int:
    return len(text.split()) if text else 0


# ---------------------------------------------------------------------------
# Per-file analysis
# ---------------------------------------------------------------------------

class Metrics(NamedTuple):
    file:          str
    title:         str
    words:         int
    h2:            int
    h3:            int
    mermaid:       int
    canvas:        int
    canvas_px:     int
    static_svg:    int
    img:           int
    code_blocks:   int
    code_lines:    int
    inline_boxes:  int
    section_ids:   int
    has_summary:   bool
    has_exercise:  bool
    has_quiz:      bool
    has_lesson_nav: bool
    clipboard_js:  bool
    course_enh_js: bool


def analyze(path: Path) -> Metrics | None:
    try:
        html = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    # Title
    m = TITLE_RE.search(html)
    title = (m.group(1).strip() if m else "").replace("\n", " ")
    title = WS_RE.sub(" ", title)[:80]

    # Word count from prose only
    words = count_words(strip_to_text(html))

    # Section counts
    h2 = len(H2_RE.findall(html))
    h3 = len(H3_RE.findall(html))

    # Visual aids
    mermaid = len(MERMAID_RE.findall(html))
    canvas_tags = CANVAS_TAG_RE.findall(html)
    canvas = len(canvas_tags)
    canvas_px = 0
    for tag in canvas_tags:
        w = CANVAS_W_RE.search(tag)
        h = CANVAS_H_RE.search(tag)
        if w and h:
            canvas_px += int(w.group(1)) * int(h.group(1))
    static_svg = len(SVG_RE.findall(html))
    img = len(IMG_RE.findall(html))

    # Code
    pre_blocks = PRE_BLOCK_RE.findall(html)
    code_blocks = len(pre_blocks)
    code_lines = sum(block.count("\n") + 1 for block in pre_blocks if block.strip())

    # Styling boxes
    inline_boxes = len(INLINE_BOX_RE.findall(html))

    # Section IDs — only count IDs on heading elements (true anchors)
    section_ids = len(HEADING_WITH_ID_RE.findall(html))

    # Heading-based markers
    has_summary  = bool(SUMMARY_RE.search(html))
    has_exercise = bool(EXERCISE_RE.search(html))
    has_quiz     = bool(QUIZ_RE.search(html))
    has_lesson_nav = bool(LESSON_NAV_RE.search(html))

    # Script references
    scripts = [s.lower() for s in SCRIPT_SRC_RE.findall(html)]
    clipboard_js  = any("clipboard.js" in s for s in scripts)
    course_enh_js = any("course-enhancements.js" in s for s in scripts)

    return Metrics(
        file=path.name,
        title=title,
        words=words,
        h2=h2,
        h3=h3,
        mermaid=mermaid,
        canvas=canvas,
        canvas_px=canvas_px,
        static_svg=static_svg,
        img=img,
        code_blocks=code_blocks,
        code_lines=code_lines,
        inline_boxes=inline_boxes,
        section_ids=section_ids,
        has_summary=has_summary,
        has_exercise=has_exercise,
        has_quiz=has_quiz,
        has_lesson_nav=has_lesson_nav,
        clipboard_js=clipboard_js,
        course_enh_js=course_enh_js,
    )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def yn(b: bool) -> str:
    return "✓" if b else "·"


# Compact column set for terminal-friendly markdown table
TABLE_COLUMNS = [
    ("file",         lambda m: m.file),
    ("words",        lambda m: f"{m.words}"),
    ("h2",           lambda m: f"{m.h2}"),
    ("h3",           lambda m: f"{m.h3}"),
    ("merm",         lambda m: f"{m.mermaid}"),
    ("canv",         lambda m: f"{m.canvas}"),
    ("svg",          lambda m: f"{m.static_svg}"),
    ("img",          lambda m: f"{m.img}"),
    ("code#",        lambda m: f"{m.code_blocks}"),
    ("codeLn",       lambda m: f"{m.code_lines}"),
    ("ids",          lambda m: f"{m.section_ids}"),
    ("summ",         lambda m: yn(m.has_summary)),
    ("exer",         lambda m: yn(m.has_exercise)),
    ("quiz",         lambda m: yn(m.has_quiz)),
    ("nav",          lambda m: yn(m.has_lesson_nav)),
]


def print_table(rows: list[Metrics]) -> None:
    headers = [c[0] for c in TABLE_COLUMNS]
    # Compute column widths
    widths = [len(h) for h in headers]
    str_rows: list[list[str]] = []
    for m in rows:
        cells = [fn(m) for _, fn in TABLE_COLUMNS]
        str_rows.append(cells)
        for i, c in enumerate(cells):
            widths[i] = max(widths[i], len(c))

    # Header
    line = "| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |"
    sep  = "|" + "|".join("-" * (widths[i] + 2) for i in range(len(headers))) + "|"
    print(line)
    print(sep)
    for cells in str_rows:
        print("| " + " | ".join(cells[i].ljust(widths[i]) for i in range(len(cells))) + " |")


def print_summary(rows: list[Metrics]) -> None:
    if not rows:
        return
    n = len(rows)
    avg = lambda f: sum(f(m) for m in rows) / n

    print()
    print("## Summary")
    print(f"- Files analyzed: **{n}**")
    print(f"- Average words/lesson: **{avg(lambda m: m.words):.0f}**  "
          f"(min {min(m.words for m in rows)}, max {max(m.words for m in rows)})")
    print(f"- Average code lines/lesson: **{avg(lambda m: m.code_lines):.0f}**  "
          f"(max {max(m.code_lines for m in rows)})")
    print(f"- Total mermaid diagrams: **{sum(m.mermaid for m in rows)}**")
    print(f"- Total canvas demos: **{sum(m.canvas for m in rows)}**  "
          f"(avg size {avg(lambda m: m.canvas_px):.0f} px²)")
    print(f"- Total static SVGs: **{sum(m.static_svg for m in rows)}**  "
          f"(currently mostly absent)")

    print()
    print("## Lessons missing key sections")

    no_summary  = [m.file for m in rows if not m.has_summary]
    no_exercise = [m.file for m in rows if not m.has_exercise]
    no_quiz     = [m.file for m in rows if not m.has_quiz]
    no_nav      = [m.file for m in rows if not m.has_lesson_nav]
    no_section_ids = [m.file for m in rows if m.section_ids == 0]
    very_long   = [m for m in rows if m.words > 4000]
    canvas_heavy = [m for m in rows if m.canvas_px > 400000]
    no_static_visuals = [m for m in rows if m.static_svg == 0 and m.img == 0]

    def show(label: str, items: list, limit: int = 8) -> None:
        if not items:
            print(f"- **{label}**: none ✓")
            return
        head = items[:limit]
        more = f" (+ {len(items) - limit} more)" if len(items) > limit else ""
        # items can be Metrics or filenames
        names = [i.file if isinstance(i, Metrics) else i for i in head]
        print(f"- **{label}** ({len(items)}/{n}): {', '.join(names)}{more}")

    show("missing a Summary section", no_summary)
    show("missing an Exercise section", no_exercise)
    show("missing a Quiz section", no_quiz)
    show("missing prev/next lesson nav", no_nav)
    show("no section IDs (can't anchor a TOC)", no_section_ids)
    show("very long (> 4000 words)", very_long)
    show("canvas-heavy (> 400k px², hidden on mobile)", canvas_heavy)
    show("no static images or SVGs (mermaid only)", no_static_visuals)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

SORT_KEYS = {
    "file":       lambda m: m.file,
    "words":      lambda m: -m.words,
    "h2":         lambda m: -m.h2,
    "mermaid":    lambda m: -m.mermaid,
    "canvas":     lambda m: -m.canvas,
    "canvas_px":  lambda m: -m.canvas_px,
    "code_lines": lambda m: -m.code_lines,
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Audit lesson HTML files and produce a content report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("directory", nargs="?", default=".", type=Path,
                   help="Course directory (default: current)")
    p.add_argument("--pattern", default="*.html",
                   help="Glob for files (default: *.html)")
    p.add_argument("--include-index", action="store_true",
                   help="Also process index.html (excluded by default)")
    p.add_argument("--csv", metavar="PATH", default=None,
                   help="Also write a full CSV (every column) to PATH")
    p.add_argument("--sort", choices=sorted(SORT_KEYS), default="file",
                   help="Sort key (default: file)")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    base = args.directory.resolve()
    if not base.is_dir():
        print(f"Error: {base} is not a directory", file=sys.stderr)
        return 2

    files = sorted(base.glob(args.pattern))
    if not args.include_index:
        files = [f for f in files if f.name.lower() != "index.html"]

    rows: list[Metrics] = []
    for f in files:
        m = analyze(f)
        if m is not None:
            rows.append(m)

    if not rows:
        print("No analyzable files found.")
        return 0

    rows.sort(key=SORT_KEYS[args.sort])

    print(f"# Lesson Audit — {base.name}")
    print(f"_Sorted by `{args.sort}`. {len(rows)} files._\n")
    print_table(rows)
    print_summary(rows)

    if args.csv:
        out = Path(args.csv).resolve()
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(Metrics._fields)
            for m in rows:
                writer.writerow(list(m))
        print(f"\nCSV written: {out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
