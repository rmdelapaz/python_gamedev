#!/usr/bin/env python3
"""
inject_main_nav.py

Add the new sticky top navigation, the nav-enhancements.js script tag, and
(optionally) upgrade the Mermaid initialization to a theme-aware form, across
every lesson HTML file in a course directory.

What it does for each file:
  1. Inject  <script src=".../js/nav-enhancements.js" defer></script>  before </head>
  2. Inject  <nav class="main-nav">…</nav>  near the top of <body>
       — placed AFTER any existing <a class="skip-to-main"> and <div class="progress-indicator">
         so the skip-link remains the first focusable element on the page.
  3. (Optional, default ON) Rewrite the Mermaid <script type="module"> block
     so it exposes  window.__mermaid  and picks an initial theme based on
     the saved/OS preference. This is what lets the theme toggle flip diagrams.

Behavior:
  * Idempotent — files already containing  class="main-nav"  are detected and
    skipped, so you can re-run safely.
  * Path-style aware — if the file uses absolute  /styles/main.css  paths the
    new script tag uses  /js/nav-enhancements.js; otherwise relative
    js/nav-enhancements.js. Detected per file.
  * Preserves skip-to-main and progress-indicator placement when present.
  * Writes a sibling .bak copy before modifying (disable with --no-backup).
  * --dry-run shows what would change without touching anything.

Usage:
    python3 inject_main_nav.py                       # current dir, all *.html except index.html
    python3 inject_main_nav.py /path/to/python_gamedev
    python3 inject_main_nav.py --dry-run             # preview only
    python3 inject_main_nav.py --no-backup
    python3 inject_main_nav.py --include-index       # also process index.html
    python3 inject_main_nav.py --no-mermaid-update   # skip the mermaid rewrite
    python3 inject_main_nav.py --pattern "lesson_*.html"

Tweak the NAV_LOGO_TEXT / NAV_LINKS constants below to customize the nav for a
different course.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Customization — edit these for a different course
# ---------------------------------------------------------------------------

NAV_LOGO_TEXT = "🎮 Python Game Dev"
NAV_LOGO_HREF = "index.html"
# Each entry: ("Label", "href"). Use ("__divider__", "") to insert a divider.
NAV_LINKS: list[tuple[str, str]] = [
    ("Home", "index.html"),
    ("__divider__", ""),
    ("Ray's House of Fun", "https://rays-home.netlify.app/"),
    ("Contact", "https://rays-home.netlify.app/contact"),
]


# ---------------------------------------------------------------------------
# Terminal colors
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
# Patterns
# ---------------------------------------------------------------------------

# Idempotence signature — file already migrated
ALREADY_DONE = re.compile(r'class="main-nav"')

# Anchor for script-tag injection (just before </head>)
HEAD_CLOSE = re.compile(r'</head>', re.IGNORECASE)

# Anchor for nav injection (the opening <body…> tag)
BODY_OPEN = re.compile(r'<body[^>]*>', re.IGNORECASE)

# Detect the path style used in the file
ABS_PATH_HINT = re.compile(r'(?:href|src)="/(?:styles|js)/')

# Skip-to-main and progress-indicator detection (used to position nav after them)
SKIP_LINK = re.compile(
    r'<a[^>]*class="[^"]*skip-to-main[^"]*"[^>]*>.*?</a>',
    re.DOTALL | re.IGNORECASE,
)
PROGRESS_DIV = re.compile(
    r'<div[^>]*class="[^"]*progress-indicator[^"]*"[^>]*>.*?</div>',
    re.DOTALL | re.IGNORECASE,
)

# Mermaid module init detection — flexible for nested braces and minor whitespace variations
MERMAID_INIT = re.compile(
    r'<script\s+type="module">\s*'
    r'import\s+mermaid\s+from\s+'
    r"'https://cdn\.jsdelivr\.net/npm/mermaid@\d+/dist/mermaid\.esm\.min\.mjs';\s*"
    r'mermaid\.initialize\(\s*\{.*?\}\s*\);\s*'
    r'</script>',
    re.IGNORECASE | re.DOTALL,
)
# Detect whether mermaid block has already been upgraded (idempotence)
MERMAID_UPGRADED = re.compile(r'window\.__mermaid\s*=\s*mermaid')


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def build_script_tag(path_prefix: str) -> str:
    return f'    <script src="{path_prefix}js/nav-enhancements.js" defer></script>\n'


def build_nav_block(indent: str = "    ") -> str:
    """Build the <nav class='main-nav'> HTML block."""
    link_lines = []
    for label, href in NAV_LINKS:
        if label == "__divider__":
            link_lines.append(f'{indent}            <span class="nav-divider"></span>')
        else:
            # Escape any HTML-special chars in the label (apostrophes are fine in HTML attrs but text needs care)
            link_lines.append(f'{indent}            <a href="{href}">{label}</a>')

    links_html = "\n".join(link_lines)

    return (
        f"\n{indent}<!-- Main Navigation (auto-injected by inject_main_nav.py) -->\n"
        f'{indent}<nav class="main-nav" aria-label="Main navigation">\n'
        f'{indent}    <div class="nav-container">\n'
        f'{indent}        <a href="{NAV_LOGO_HREF}" class="nav-logo">{NAV_LOGO_TEXT}</a>\n'
        f'{indent}        <button id="mobile-menu-toggle" class="mobile-menu-toggle" '
        f'aria-expanded="false" aria-controls="nav-links">☰</button>\n'
        f'{indent}        <div class="nav-links" id="nav-links">\n'
        f"{links_html}\n"
        f'{indent}            <button id="theme-toggle" aria-label="Toggle dark/light mode">🌙</button>\n'
        f'{indent}        </div>\n'
        f'{indent}    </div>\n'
        f'{indent}</nav>\n'
    )


def build_upgraded_mermaid() -> str:
    """The new mermaid module block that exposes window.__mermaid and picks initial theme."""
    return (
        '<script type="module">\n'
        "    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';\n"
        "    window.__mermaid = mermaid;\n"
        "    const isDark = localStorage.getItem('theme') === 'dark' ||\n"
        "        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);\n"
        "    mermaid.initialize({\n"
        "        startOnLoad: true,\n"
        "        theme: isDark ? 'dark' : 'default',\n"
        "        themeVariables: isDark\n"
        "            ? { primaryColor: '#2d2d30', primaryTextColor: '#d4d4d4', primaryBorderColor: '#569cd6', lineColor: '#94a3b8', secondaryColor: '#1e1e1e', tertiaryColor: '#0f172a' }\n"
        "            : { primaryColor: '#f0f8ff', primaryTextColor: '#1e293b', primaryBorderColor: '#3b82f6', lineColor: '#64748b', secondaryColor: '#f8fafc', tertiaryColor: '#f1f5f9' }\n"
        "    });\n"
        "</script>"
    )


# ---------------------------------------------------------------------------
# Core rewrite
# ---------------------------------------------------------------------------

class Result(NamedTuple):
    path: Path
    status: str   # updated | skipped_already | no_body | no_head | error
    detail: str = ""
    changes: tuple[str, ...] = ()  # which pieces actually changed


def detect_path_prefix(text: str) -> str:
    """Return '/' if the file uses absolute /styles/ or /js/ paths, else ''."""
    return "/" if ABS_PATH_HINT.search(text) else ""


def find_nav_insertion_point(text: str) -> int | None:
    """Return char index where the main-nav block should be inserted, or None."""
    body_m = BODY_OPEN.search(text)
    if not body_m:
        return None

    pos = body_m.end()
    # Skip whitespace following <body>
    while pos < len(text) and text[pos].isspace():
        pos += 1

    # Skip past skip-to-main link if present
    sk = SKIP_LINK.match(text, pos)
    if sk:
        pos = sk.end()
        while pos < len(text) and text[pos].isspace():
            pos += 1

    # Skip past progress-indicator div if present
    pr = PROGRESS_DIV.match(text, pos)
    if pr:
        pos = pr.end()

    return pos


def detect_indent_at(text: str, pos: int) -> str:
    """Look at the line at/after pos to figure out indentation. Default 4 spaces."""
    # Find start of next line
    nl = text.find("\n", pos)
    if nl == -1:
        return "    "
    line_start = nl + 1
    indent_chars = []
    for ch in text[line_start:line_start + 16]:
        if ch in (" ", "\t"):
            indent_chars.append(ch)
        else:
            break
    return "".join(indent_chars) or "    "


def process_file(
    path: Path,
    *,
    dry_run: bool,
    backup: bool,
    update_mermaid: bool,
) -> Result:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return Result(path, "error", f"read failed: {e}")
    except UnicodeDecodeError as e:
        return Result(path, "error", f"not valid UTF-8: {e}")

    if ALREADY_DONE.search(text):
        return Result(path, "skipped_already", "already has class=\"main-nav\"")

    if not BODY_OPEN.search(text):
        return Result(path, "no_body", "no <body> tag")

    if not HEAD_CLOSE.search(text):
        return Result(path, "no_head", "no </head> tag")

    changes: list[str] = []
    new_text = text
    path_prefix = detect_path_prefix(new_text)

    # 1. Inject script tag before </head>
    if "nav-enhancements.js" not in new_text:
        script_tag = build_script_tag(path_prefix)
        # Insert just before the FIRST </head>
        new_text = HEAD_CLOSE.sub(lambda m: script_tag + m.group(0), new_text, count=1)
        changes.append("script tag")

    # 2. Inject nav block after body / skip-to-main / progress-indicator
    insert_at = find_nav_insertion_point(new_text)
    if insert_at is None:
        return Result(path, "no_body", "could not locate <body>")

    indent = detect_indent_at(new_text, insert_at)
    nav_html = build_nav_block(indent=indent)
    new_text = new_text[:insert_at] + nav_html + new_text[insert_at:]
    changes.append("nav block")

    # 3. Optionally upgrade mermaid init
    if update_mermaid:
        if MERMAID_UPGRADED.search(new_text):
            pass  # already upgraded — no-op
        else:
            m = MERMAID_INIT.search(new_text)
            if m:
                new_text = new_text[:m.start()] + build_upgraded_mermaid() + new_text[m.end():]
                changes.append("mermaid init")

    if dry_run:
        return Result(path, "updated", "dry-run, no file written", tuple(changes))

    if backup:
        bak = path.with_suffix(path.suffix + ".bak")
        try:
            bak.write_bytes(path.read_bytes())
        except OSError as e:
            return Result(path, "error", f"backup failed: {e}")

    try:
        path.write_text(new_text, encoding="utf-8", newline="")
    except OSError as e:
        return Result(path, "error", f"write failed: {e}")

    return Result(path, "updated", "", tuple(changes))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Inject the new top nav + nav-enhancements.js script into lesson HTML files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage:", 1)[1] if "Usage:" in __doc__ else None,
    )
    p.add_argument("directory", nargs="?", default=".", type=Path,
                   help="Course directory (default: current)")
    p.add_argument("--pattern", default="*.html",
                   help="Glob for files (default: *.html)")
    p.add_argument("--dry-run", action="store_true",
                   help="Preview which files would change without modifying them")
    p.add_argument("--no-backup", action="store_true",
                   help="Skip writing .bak copies")
    p.add_argument("--include-index", action="store_true",
                   help="Also process index.html (excluded by default)")
    p.add_argument("--no-mermaid-update", action="store_true",
                   help="Don't rewrite the mermaid init block")
    p.add_argument("--no-color", action="store_true",
                   help="Disable ANSI color output")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.no_color or not sys.stdout.isatty():
        _strip_color()

    base = args.directory.resolve()
    if not base.is_dir():
        print(f"{C.RED}Error: {base} is not a directory{C.RESET}", file=sys.stderr)
        return 2

    files = sorted(base.glob(args.pattern))
    if not args.include_index:
        files = [f for f in files if f.name.lower() != "index.html"]

    if not files:
        print(f"{C.YELLOW}No files matched pattern '{args.pattern}' in {base}{C.RESET}")
        return 0

    mode = " (dry-run)" if args.dry_run else ""
    print(f"{C.BOLD}{C.CYAN}Main-nav injection{mode}{C.RESET}")
    print(f"{C.DIM}Directory:     {C.RESET} {base}")
    print(f"{C.DIM}Files:         {C.RESET} {len(files)}")
    print(f"{C.DIM}Mermaid update:{C.RESET} {'no' if args.no_mermaid_update else 'yes'}")
    if not args.dry_run:
        print(f"{C.DIM}Backups:       {C.RESET} {'no' if args.no_backup else 'yes (.bak)'}")
    print()

    results = [
        process_file(
            f,
            dry_run=args.dry_run,
            backup=not args.no_backup,
            update_mermaid=not args.no_mermaid_update,
        )
        for f in files
    ]

    counts = {"updated": 0, "skipped_already": 0, "no_body": 0, "no_head": 0, "error": 0}
    symbols = {
        "updated":         ("✓", C.GREEN),
        "skipped_already": ("•", C.DIM),
        "no_body":         ("?", C.YELLOW),
        "no_head":         ("?", C.YELLOW),
        "error":           ("✗", C.RED),
    }
    for r in results:
        counts[r.status] += 1
        symbol, color = symbols[r.status]
        line = f"  {color}{symbol}{C.RESET} {r.path.name}"
        if r.changes:
            line += f" {C.DIM}[{', '.join(r.changes)}]{C.RESET}"
        if r.detail:
            line += f" {C.DIM}— {r.detail}{C.RESET}"
        print(line)

    print()
    print(f"{C.BOLD}Summary:{C.RESET}")
    print(f"  {C.GREEN}updated         {C.RESET} {counts['updated']}")
    print(f"  {C.DIM}already migrated{C.RESET} {counts['skipped_already']}")
    print(f"  {C.YELLOW}no <body>       {C.RESET} {counts['no_body']}")
    print(f"  {C.YELLOW}no </head>      {C.RESET} {counts['no_head']}")
    print(f"  {C.RED}errors          {C.RESET} {counts['error']}")

    if counts["no_body"] or counts["no_head"]:
        print(
            f"\n{C.YELLOW}Some files lacked <body> or </head> markers and were skipped.\n"
            f"Inspect them manually if they are real lessons.{C.RESET}"
        )

    return 1 if counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
