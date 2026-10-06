#!/usr/bin/env python3
"""Render the whitepaper Markdown into the article body of its HTML page.

docs/whitepaper/web/federated-ads-whitepaper.html is a hand-designed page
(masthead, styles, side index). Only the content between <article> and
</article> is generated from the Markdown, with pandoc, so that the two never
drift apart. The masthead and footer are left untouched and must be updated
by hand when the front matter changes.

The conversion reproduces the page's existing conventions:
  - the Markdown "Contents" block is omitted (the page builds its own index);
  - tables are wrapped in <div class="tbl">;
  - Mermaid diagrams are wrapped in <div class="diagram"><pre class="mermaid">.

Usage:
  scripts/render_whitepaper.py           rewrite the HTML article in place
  scripts/render_whitepaper.py --check   exit 1 if the HTML is out of date

Requires pandoc (tested with 3.9).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return Path(top)
    except (OSError, subprocess.CalledProcessError):
        return Path(__file__).resolve().parent.parent


ROOT = _repo_root()
MD = ROOT / "docs/whitepaper/federated-ads-whitepaper.md"
HTML = ROOT / "docs/whitepaper/web/federated-ads-whitepaper.html"


def markdown_body(md: str) -> str:
    """From the executive summary to the closing rule, without Contents."""
    body = md[md.index("## Executive summary"):md.rindex("\n---")]
    start = body.index("## Contents")
    end = body.index("\n---", start)
    return body[:start] + body[end + len("\n---"):].lstrip("\n")


def render(md: str) -> str:
    out = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none"],
        input=markdown_body(md), capture_output=True, text=True, check=True,
    ).stdout
    out = out.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    out = re.sub(r'<pre class="mermaid"><code>(.*?)</code></pre>',
                 r'<div class="diagram"><pre class="mermaid">\1</pre></div>', out, flags=re.S)
    return out


def splice(html: str, article: str) -> str:
    a = html.index("<article>") + len("<article>")
    b = html.index("</article>")
    return html[:a] + "\n" + article + "\n  " + html[b:]


def main() -> int:
    md = MD.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    new = splice(html, render(md))
    if "--check" in sys.argv[1:]:
        if new != html:
            print(f"{HTML.relative_to(ROOT)} is out of date: run scripts/render_whitepaper.py", file=sys.stderr)
            return 1
        print("render_whitepaper: up to date")
        return 0
    if new != html:
        HTML.write_text(new, encoding="utf-8")
        print(f"render_whitepaper: updated {HTML.relative_to(ROOT)}")
    else:
        print("render_whitepaper: already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
