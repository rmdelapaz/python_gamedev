#!/usr/bin/env python3
"""
inject_section_ids.py

Add stable, slugified `id` attributes to every <h2> and <h3> in lesson HTML
files that doesn't already have one. Enables deep-linking to sections and
lets nav-enhancements.js auto-build a sticky table of contents.

What it does for each file:
  * Finds every <h2> and <h3>
  * Skips any heading that already has an id
  * Slugifies the heading text (strips HTML tags + emoji, lowercases, hyphenates)
  * Resolves collisions by appending -2, -3, …
  * Inserts id="<slug>" as the first attribute

Behavior:
  * Idempotent — running twice produces no diff.
  * Stable — slugs are deterministic from heading text, so subsequent runs
    keep the same anchors as long as headings don't change.
  * Preserves all other attributes (class, role, etc.).
  * Writes a sibling .bak copy before modifying (disable with --no-backup).
  * --dry-run shows what would change without touching anything.

Usage:
    python3 inject_section_ids.py                       # current dir
    python3 inject_section_ids.py /path/to/python_gamedev
    python3 inject_section_ids.py --dry-run
    python3 inject_section_ids.py --no-backup
    python3 inject_section_ids.py --include-index
    python3 inject_section_ids.py --levels h2          # only h2 (default: h2,h3)
    python3 inject_section_ids.py --pattern "lesson_*.html"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    RED    = "\033[31m"
    CYAN   = "\033[36m"


def _strip_color() -> None:
    for n in ("RESET", "BOLD", "DIM", "GREEN", "YELLOW", "RED", "CYAN"):
        setattr(C, n, "")


# ---------------------------------------------------------------------------
# Slugify
# ---------------------------------------------------------------------------

TAG_RE       = re.compile(r"<[^>]+>")
NON_ASCII_RE = re.compile(r"[^\x20-\x7E]+")  # strip emoji & non-ASCII
SLUG_RE      = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Turn heading text into a URL-safe stable slug."""
    text = TAG_RE.sub(" ", text)        # strip nested HTML
    text = NON_ASCII_RE.sub(" ", text)  # strip emoji / non-ASCII
    text = text.lower()
    text = SLUG_RE.sub("-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "section"


# ---------------------------------------------------------------------------
# Heading rewrite
# ---------------------------------------------------------------------------

# Match a heading element with its open tag, attributes, content, close tag
def heading_pattern(levels: list[str]) -> re.Pattern:
    tag_alt = "|".join(re.escape(t) for t in levels)
    return re.compile(
        rf"<({tag_alt})\b([^>]*)>(.*?)</\1>",
        re.IGNORECASE | re.DOTALL,
    )


ID_ATTR_RE = re.compile(r'\bid\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)


def rewrite_headings(html: str, levels: list[str]) -> tuple[str, int, int]:
    """Return (new_html, added, kept).

    added = number of headings that received a new id attribute.
    kept  = number of headings that already had an id and were left alone.
    """
    pattern = heading_pattern(levels)
    used: set[str] = set()
    added = 0
    kept = 0

    # First pass: collect existing ids so we don't collide with them
    for m in pattern.finditer(html):
        existing = ID_ATTR_RE.search(m.group(2))
        if existing:
            used.add(existing.group(1))

    def repl(m: re.Match) -> str:
        nonlocal added, kept
        tag, attrs, content = m.group(1), m.group(2), m.group(3)

        # Already has an id? Leave alone.
        if ID_ATTR_RE.search(attrs):
            kept += 1
            return m.group(0)

        base = slugify(content)
        slug = base
        n = 2
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)

        # Inject id as the first attribute (preserve all existing attrs)
        new_attrs = f' id="{slug}"{attrs}'
        added += 1
        return f"<{tag}{new_attrs}>{content}</{tag}>"

    new_html = pattern.sub(repl, html)
    return new_html, added, kept


# ---------------------------------------------------------------------------
# Per-file
# ---------------------------------------------------------------------------

class Result(NamedTuple):
    path: Path
    status: str   # updated | nochange | error
    added: int = 0
    kept: int = 0
    detail: str = ""


def process_file(path: Path, *, levels: list[str], dry_run: bool, backup: bool) -> Result:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return Result(path, "error", detail=f"read failed: {e}")
    except UnicodeDecodeError as e:
        return Result(path, "error", detail=f"not valid UTF-8: {e}")

    new_text, added, kept = rewrite_headings(text, levels)

    if added == 0:
        return Result(path, "nochange", added=0, kept=kept,
                      detail="all headings already have ids" if kept else "no headings found")

    if dry_run:
        return Result(path, "updated", added=added, kept=kept,
                      detail="dry-run, no file written")

    if backup:
        bak = path.with_suffix(path.suffix + ".bak")
        try:
            bak.write_bytes(path.read_bytes())
        except OSError as e:
            return Result(path, "error", detail=f"backup failed: {e}")

    try:
        path.write_text(new_text, encoding="utf-8", newline="")
    except OSError as e:
        return Result(path, "error", detail=f"write failed: {e}")

    return Result(path, "updated", added=added, kept=kept)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Add stable id attributes to <h2> and <h3> elements in lesson HTML files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("directory", nargs="?", default=".", type=Path,
                   help="Course directory (default: current)")
    p.add_argument("--pattern", default="*.html",
                   help="Glob for files (default: *.html)")
    p.add_argument("--levels", default="h2,h3",
                   help="Comma-separated heading levels to process (default: h2,h3)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-backup", action="store_true")
    p.add_argument("--include-index", action="store_true")
    p.add_argument("--no-color", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.no_color or not sys.stdout.isatty():
        _strip_color()

    base = args.directory.resolve()
    if not base.is_dir():
        print(f"{C.RED}Error: {base} is not a directory{C.RESET}", file=sys.stderr)
        return 2

    levels = [lvl.strip().lower() for lvl in args.levels.split(",") if lvl.strip()]
    invalid = [l for l in levels if l not in {"h1", "h2", "h3", "h4", "h5", "h6"}]
    if invalid:
        print(f"{C.RED}Invalid heading level(s): {invalid}{C.RESET}", file=sys.stderr)
        return 2

    files = sorted(base.glob(args.pattern))
    if not args.include_index:
        files = [f for f in files if f.name.lower() != "index.html"]

    if not files:
        print(f"{C.YELLOW}No files matched pattern '{args.pattern}' in {base}{C.RESET}")
        return 0

    mode = " (dry-run)" if args.dry_run else ""
    print(f"{C.BOLD}{C.CYAN}Section ID injection{mode}{C.RESET}")
    print(f"{C.DIM}Directory:{C.RESET} {base}")
    print(f"{C.DIM}Files:    {C.RESET} {len(files)}")
    print(f"{C.DIM}Levels:   {C.RESET} {', '.join(levels)}")
    if not args.dry_run:
        print(f"{C.DIM}Backups:  {C.RESET} {'no' if args.no_backup else 'yes (.bak)'}")
    print()

    results = [
        process_file(f, levels=levels, dry_run=args.dry_run, backup=not args.no_backup)
        for f in files
    ]

    counts = {"updated": 0, "nochange": 0, "error": 0}
    total_added = 0
    total_kept = 0
    for r in results:
        counts[r.status] += 1
        total_added += r.added
        total_kept += r.kept
        symbol, color = {
            "updated":  ("✓", C.GREEN),
            "nochange": ("•", C.DIM),
            "error":    ("✗", C.RED),
        }[r.status]
        line = f"  {color}{symbol}{C.RESET} {r.path.name}"
        if r.added or r.kept:
            line += f" {C.DIM}[+{r.added} added, {r.kept} kept]{C.RESET}"
        if r.detail:
            line += f" {C.DIM}— {r.detail}{C.RESET}"
        print(line)

    print()
    print(f"{C.BOLD}Summary:{C.RESET}")
    print(f"  {C.GREEN}files updated   {C.RESET} {counts['updated']}")
    print(f"  {C.DIM}files unchanged {C.RESET} {counts['nochange']}")
    print(f"  {C.RED}errors          {C.RESET} {counts['error']}")
    print(f"  {C.GREEN}IDs added       {C.RESET} {total_added}")
    print(f"  {C.DIM}IDs preserved   {C.RESET} {total_kept}")

    return 1 if counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
