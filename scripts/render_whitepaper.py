#!/usr/bin/env python3
"""Render the whitepaper Markdown into the article body of its HTML page.

docs/whitepaper/web/federated-ads-whitepaper.html is a hand-designed page
(masthead, styles, side index). Only the content between <article> and
</article> is generated from the Markdown, with pandoc, so that the two never
drift apart. The masthead and footer are left untouched and must be updated
by hand when the front matter changes.

The conversion reproduces the page's existing conventions:
  - the Markdown "Contents" block is omitted; instead the side index
    (<nav class="toc">) is generated from the article's part and section
    headings;
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


def toc(article: str) -> str:
    """Side-index items: a label per part, a numbered link per section."""
    items = []
    appendices = False
    for level, hid, text in re.findall(r'<h([12]) id="([^"]+)">(.*?)</h\1>', article):
        text = re.sub(r"<[^>]+>", "", text)
        if level == "1":
            items.append(f'<li class="part">{text}</li>')
            continue
        m = re.match(r"(?:Appendix )?([0-9]+|[A-Z])\. (.*)", text)
        num, title = (m.group(1), m.group(2)) if m else ("", text)
        if text.startswith("Appendix ") and not appendices:
            items.append('<li class="part">Appendices</li>')
            appendices = True
        items.append(f'<li><a href="#{hid}"><span>{num}</span>{title}</a></li>')
    return "\n".join("      " + i for i in items)


def splice(html: str, article: str) -> str:
    a = html.index("<article>") + len("<article>")
    b = html.index("</article>")
    html = html[:a] + "\n" + article + "\n  " + html[b:]
    nav = html.index('<nav class="toc"')
    a = html.index("<ol>", nav) + len("<ol>")
    b = html.index("</ol>", nav)
    return html[:a] + "\n" + toc(article) + "\n    " + html[b:]


def main() -> int:
    md = MD.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    try:
        new = splice(html, render(md))
    except FileNotFoundError:
        print("render_whitepaper: pandoc not found (tested with 3.9)", file=sys.stderr)
        return 1
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
