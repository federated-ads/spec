#!/usr/bin/env python3
"""Deterministic editorial checks for the Federated Ads documents.

Enforces the mechanical rules in docs/STYLE.md:
  - project naming (no "OpenAds" / "FedAds" outside the naming note and history);
  - inclusive language (no whitelist/blacklist/master/slave);
  - no em dashes in the whitepaper or style guide;
  - no uppercase BCP 14 keywords in the informative whitepaper;
  - whitepaper references: every [N] cited exists in Appendix B, every
    reference is cited, numbering is sequential with no duplicates;
  - every in-page #anchor link in the whitepaper resolves to a heading;
  - whitepaper Markdown and HTML are changed together (warning only).

Usage:
  scripts/check_docs.py            check the working tree
  scripts/check_docs.py --staged   also warn if the whitepaper .md is staged
                                   without the .html rendering

Exit status 1 if any error is found. Warnings never fail the run.
Standard library only, so it runs unchanged in CI.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from pathlib import Path

def _repo_root() -> Path:
    # The hooks run this script from the trusted ref via stdin, where __file__
    # is not a path in the clone, so ask git for the working-tree root.
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return Path(top)
    except (OSError, subprocess.CalledProcessError):
        return Path(__file__).resolve().parent.parent


ROOT = _repo_root()
WHITEPAPER = ROOT / "docs/whitepaper/federated-ads-whitepaper.md"
WHITEPAPER_HTML = ROOT / "docs/whitepaper/web/federated-ads-whitepaper.html"
STYLE = ROOT / "docs/STYLE.md"
DRAFT_DIR = ROOT / "docs/ietf"

errors: list[str] = []
warnings: list[str] = []


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def error(path: Path, line: int, msg: str) -> None:
    errors.append(f"{rel(path)}:{line}: {msg}")


def warn(msg: str) -> None:
    warnings.append(msg)


def lines_outside_code(text: str):
    """Yield (line_no, line) for lines outside fenced code blocks."""
    in_fence = False
    for no, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield no, line


def strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


# ---------------------------------------------------------------------------
# Naming and inclusive language: all Markdown documents
# ---------------------------------------------------------------------------

NAMING = re.compile(r"\b(OpenAds|Open Ads|FedAds|Fed Ads)\b")
# Lines that legitimately discuss the old or confusable names.
NAMING_ALLOWED = re.compile(
    r"Naming note|unrelated|renamed|Renamed|working name|Trade Desk|OpenAds announcement|"
    r"Open Ads Protocol|Openads|openads-initiative|avoid confusion|\"OpenAds\"",
)
EXCLUSIONARY = re.compile(r"\b(whitelist\w*|blacklist\w*|master|slave\w*)\b", re.IGNORECASE)
# "Master" is fine in established proper nouns and degrees; extend if needed.
EXCLUSIONARY_ALLOWED = re.compile(r"Mastodon|MasterCard|Master's degree|never \"whitelist\"", re.IGNORECASE)


def check_language(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for no, line in lines_outside_code(text):
        body = strip_inline_code(line)
        if NAMING.search(body) and not NAMING_ALLOWED.search(body):
            error(path, no, f"old or wrong project name {NAMING.search(body).group(0)!r}; use 'Federated Ads'")
        m = EXCLUSIONARY.search(body)
        if m and not EXCLUSIONARY_ALLOWED.search(body):
            error(path, no, f"non-inclusive term {m.group(0)!r} (STYLE.md §9)")


# ---------------------------------------------------------------------------
# Whitepaper-specific checks
# ---------------------------------------------------------------------------

BCP14 = re.compile(r"\b(MUST NOT|MUST|SHALL NOT|SHALL|SHOULD NOT|SHOULD|REQUIRED|RECOMMENDED|OPTIONAL)\b")


def slugify(heading: str) -> str:
    """GitHub-style heading anchor."""
    text = re.sub(r"`", "", heading.strip())
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def check_whitepaper() -> None:
    path = WHITEPAPER
    text = path.read_text(encoding="utf-8")

    # Em dashes and BCP 14 keywords (prose only).
    for no, line in lines_outside_code(text):
        body = strip_inline_code(line)
        if "—" in body and not line.lstrip().startswith("*The Federated Ads Protocol"):
            error(path, no, "em dash; use a colon, comma or new sentence (STYLE.md §6)")
        m = BCP14.search(body)
        if m and "BCP 14" not in body and "RFC 2119" not in body:
            error(path, no, f"uppercase {m.group(0)!r} in the informative whitepaper; normative keywords belong in the Internet-Draft (STYLE.md §2)")

    # References.
    if "## Appendix B. References" not in text:
        error(path, 1, "Appendix B. References heading not found")
        return
    body, refs_part = text.split("## Appendix B. References", 1)
    refs_part = refs_part.split("## Appendix C", 1)[0]

    defined: dict[int, int] = {}
    ref_line_offset = body.count("\n") + 1
    for i, line in enumerate(refs_part.splitlines()):
        m = re.match(r"^(\d+)\. ", line)
        if m:
            n = int(m.group(1))
            if n in defined:
                error(path, ref_line_offset + i, f"reference [{n}] defined twice")
            defined[n] = ref_line_offset + i
    if defined:
        expected = list(range(1, max(defined) + 1))
        missing_numbers = sorted(set(expected) - set(defined))
        if missing_numbers:
            error(path, ref_line_offset, f"gap in reference numbering: missing {missing_numbers}")

    cited: dict[int, int] = {}
    for no, line in lines_outside_code(body):
        for m in re.finditer(r"\[(\d+)\](?!\()", strip_inline_code(line)):
            cited.setdefault(int(m.group(1)), no)
    for n, no in sorted(cited.items()):
        if n not in defined:
            error(path, no, f"citation [{n}] has no entry in Appendix B")
    for n, no in sorted(defined.items()):
        if n not in cited:
            error(path, no, f"reference [{n}] is never cited in the text")

    # Anchors.
    anchors = set()
    for _, line in lines_outside_code(text):
        m = re.match(r"^#{1,6} (.+)$", line)
        if m:
            anchors.add(slugify(m.group(1)))
    for no, line in lines_outside_code(text):
        for m in re.finditer(r"\]\(#([^)\s]+)\)", line):
            if m.group(1) not in anchors:
                error(path, no, f"link to missing anchor #{m.group(1)}")


def check_html_sync(staged: bool) -> None:
    try:
        if staged:
            out = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout.split()
        else:
            out = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            out = [l[3:] for l in out.splitlines()]
    except (OSError, subprocess.CalledProcessError):
        return
    md, html = rel(WHITEPAPER), rel(WHITEPAPER_HTML)
    if md in out and html not in out:
        warn(f"{md} changed but {html} did not: sync the HTML rendering (STYLE.md §11)")


def main() -> int:
    staged = "--staged" in sys.argv[1:]
    docs = [WHITEPAPER, STYLE, ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    docs += sorted(DRAFT_DIR.glob("draft-*.md"))
    for path in docs:
        if path.exists():
            check_language(path)
    if WHITEPAPER.exists():
        check_whitepaper()
    check_html_sync(staged)

    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if errors:
        print(f"\ncheck_docs: {len(errors)} error(s). See docs/STYLE.md.", file=sys.stderr)
        return 1
    print("check_docs: OK" + (f" ({len(warnings)} warning(s))" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
