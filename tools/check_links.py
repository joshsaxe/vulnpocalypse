#!/usr/bin/env python
"""Check that every relative link and image in the repository's Markdown files points at something that exists.

The README files and docs link to each other, to code, to data tables and to headings inside other pages. This script
finds every relative link (Markdown `[text](target)` and HTML `href=` / `src=`), then checks that the file or folder
exists and, when the link ends in `#heading`, that the target page has a heading that GitHub would give that anchor.
Web links (http, https, mailto) are not fetched: no network connection is used.

    python tools/check_links.py            # prints a summary; exits with status 1 if any link is broken
    python tools/check_links.py -v         # also lists every link it checked
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv"}

MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
HTML_LINK = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def slug(text: str) -> str:
    """The anchor GitHub gives a heading: lower case, markup and punctuation dropped, spaces become hyphens."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)        # [text](url) -> text
    text = re.sub(r"<[^>]+>", "", text)                            # HTML tags
    text = text.replace("`", "").replace("*", "")
    text = unicodedata.normalize("NFC", text).strip().lower()
    out = []
    for ch in text:
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch == " ":
            out.append("-")
    return "".join(out)


def strip_code(lines: list[str], inline: bool = True) -> list[str]:
    """Blank out fenced code blocks and (optionally) inline code, which can contain brackets that are not links."""
    out, fenced = [], False
    for ln in lines:
        if FENCE.match(ln):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else (re.sub(r"`[^`]*`", "``", ln) if inline else ln))
    return out


_anchor_cache: dict[Path, set[str]] = {}


def anchors(path: Path) -> set[str]:
    if path not in _anchor_cache:
        seen: dict[str, int] = {}
        found: set[str] = set()
        for ln in strip_code(path.read_text(encoding="utf-8").splitlines(), inline=False):
            m = HEADING.match(ln)
            if not m:
                continue
            s = slug(m.group(2))
            n = seen.get(s, 0)
            seen[s] = n + 1
            found.add(s if n == 0 else f"{s}-{n}")
        # explicit anchors, e.g. <a id="x"></a> or <a name="x">
        for m in re.finditer(r"""<a\s+[^>]*(?:id|name)\s*=\s*["']([^"']+)["']""", path.read_text(encoding="utf-8")):
            found.add(m.group(1))
        _anchor_cache[path] = found
    return _anchor_cache[path]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-v", "--verbose", action="store_true", help="list every link checked")
    args = ap.parse_args()

    files = sorted(p for p in ROOT.rglob("*.md") if not (set(p.relative_to(ROOT).parts) & SKIP_DIRS))
    n_links, bad = 0, []
    for md in files:
        lines = strip_code(md.read_text(encoding="utf-8").splitlines())
        for i, ln in enumerate(lines, 1):
            targets = [m.group(1).strip("<>") for m in MD_LINK.finditer(ln)] + HTML_LINK.findall(ln)
            for t in targets:
                if re.match(r"^[a-z][a-z0-9+.-]*:", t, re.I) or t.startswith("//"):
                    continue                                      # http, https, mailto: not fetched
                n_links += 1
                path_part, _, frag = unquote(t).partition("#")
                dest = md if path_part == "" else (md.parent / path_part).resolve()
                where = f"{md.relative_to(ROOT)}:{i}"
                if not dest.exists():
                    bad.append(f"{where}: no such file or folder: {t}")
                    continue
                try:
                    dest.relative_to(ROOT)
                except ValueError:
                    bad.append(f"{where}: points outside the repository: {t}")
                    continue
                if frag and dest.suffix.lower() == ".md":
                    if frag not in anchors(dest):
                        bad.append(f"{where}: no heading '#{frag}' in {dest.relative_to(ROOT)}")
                        continue
                if args.verbose:
                    print(f"ok   {where}: {t}")
    for b in bad:
        print("BROKEN", b)
    print(f"{n_links} relative links in {len(files)} Markdown files: {len(bad)} broken")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
