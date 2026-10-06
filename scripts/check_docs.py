#!/usr/bin/env python3
"""Deterministic editorial checks for the Federated Ads documents.

Enforces the mechanical rules in docs/STYLE.md:
  - project naming (no "OpenAds", "FedAds" or "FAP" outside the phrases that
    explain the old and confusable names), in every tracked Markdown file;
  - inclusive language (no whitelist, blacklist, master or slave), in every
    tracked Markdown file;
  - no em dashes in the whitepaper and the editorial documents;
  - no uppercase BCP 14 keywords in the informative whitepaper;
  - whitepaper references: every [N] cited exists in Appendix B, every
    reference is cited, numbering is sequential with no duplicates;
  - every in-page #anchor link in the whitepaper resolves;
  - whitepaper Markdown and HTML are changed together (warning only).

Usage:
  scripts/check_docs.py            check the working tree; the HTML-sync
                                   warning covers this branch's commits
                                   (against origin/main) and local changes
  scripts/check_docs.py --staged   check the staged (index) content instead,
                                   as the pre-commit hook does

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
WHITEPAPER = "docs/whitepaper/federated-ads-whitepaper.md"
WHITEPAPER_HTML = "docs/whitepaper/web/federated-ads-whitepaper.html"
# Documents that follow the full punctuation rules (STYLE.md §6).
EDITORIAL = [WHITEPAPER, "docs/STYLE.md", "CLAUDE.md", "CONTRIBUTING.md", "README.md"]
# Markdown that is historical or private and is not checked.
SKIP_PREFIXES = ("docs/whitepaper/archive/", "docs/outreach/", "docs/brainstorms/")

STAGED = "--staged" in sys.argv[1:]
errors: list[str] = []
warnings: list[str] = []


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def read(path: str) -> str | None:
    """Content to check: the staged blob with --staged, else the working file."""
    if STAGED:
        try:
            return git("show", f":{path}")
        except subprocess.CalledProcessError:
            return None
    file = ROOT / path
    return file.read_text(encoding="utf-8") if file.exists() else None


def tracked_markdown() -> list[str]:
    files = git("ls-files", "--cached", "--", "*.md").split("\n")
    if not STAGED:
        files += git("ls-files", "--others", "--exclude-standard", "--", "*.md").split("\n")
    return sorted({f for f in files if f and not f.startswith(SKIP_PREFIXES)})


def error(path: str, line: int, msg: str) -> None:
    errors.append(f"{path}:{line}: {msg}")


def warn(msg: str) -> None:
    warnings.append(msg)


FENCE = re.compile(r"^\s*(```|~~~)")


def lines_outside_code(text: str):
    """Yield (line_no, line) for lines outside fenced code blocks."""
    fence = None
    for no, line in enumerate(text.splitlines(), 1):
        m = FENCE.match(line)
        if m:
            if fence is None:
                fence = m.group(1)
            elif m.group(1) == fence:
                fence = None
            continue
        if fence is None:
            yield no, line


def strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


# ---------------------------------------------------------------------------
# Naming and inclusive language: all tracked Markdown
# ---------------------------------------------------------------------------

NAMING = re.compile(r"\b(OpenAds|Open Ads|FedAds|Fed Ads|FAP)\b")
# Phrases that legitimately name the old or confusable names. They are removed
# from the line before searching, so an unrelated hit on the same line is
# still reported.
NAMING_ALLOWED = re.compile(
    r"[\"“](?:OpenAds|Open Ads|FedAds|Fed Ads|FAP)[\"”]|"
    r"Trade Desk(?:'s|’s)? (?:sell-side solution )?\"?OpenAds\"?(?: header-bidding wrapper)?|"
    r"OpenAds announcement|Open Ads Protocol|openads-initiative"
)
EXCLUSIONARY = re.compile(r"\b(whitelist\w*|blacklist\w*|master\w*|slave\w*)\b", re.IGNORECASE)
EXCLUSIONARY_ALLOWED = re.compile(
    r"MasterCard|Master's degree|"
    r"never \"whitelist\", \"blacklist\", \"master\" or \"slave\"",
    re.IGNORECASE,
)


def check_language(path: str, text: str) -> None:
    for no, line in lines_outside_code(text):
        body = strip_inline_code(line)
        for m in NAMING.finditer(NAMING_ALLOWED.sub("", body)):
            error(path, no, f"old or wrong project name {m.group(0)!r}; use 'Federated Ads' (STYLE.md §3)")
        for m in EXCLUSIONARY.finditer(EXCLUSIONARY_ALLOWED.sub("", body)):
            error(path, no, f"non-inclusive term {m.group(0)!r} (STYLE.md §9)")


def check_punctuation(path: str, text: str) -> None:
    for no, line in lines_outside_code(text):
        if "—" in strip_inline_code(line):
            error(path, no, "em dash; use a colon, comma or new sentence (STYLE.md §6)")


# ---------------------------------------------------------------------------
# Whitepaper-specific checks
# ---------------------------------------------------------------------------

BCP14 = re.compile(
    r"\b(NOT RECOMMENDED|MUST NOT|MUST|SHALL NOT|SHALL|SHOULD NOT|SHOULD|"
    r"REQUIRED|RECOMMENDED|MAY|OPTIONAL)\b"
)
CITATION = re.compile(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\](?!\()")


def expand_citation(group: str) -> list[int]:
    numbers: list[int] = []
    for part in re.split(r"\s*,\s*", group):
        bounds = re.split(r"\s*[–-]\s*", part)
        if len(bounds) == 2:
            lo, hi = int(bounds[0]), int(bounds[1])
            numbers.extend(range(lo, hi + 1))
        else:
            numbers.append(int(bounds[0]))
    return numbers


def slugify(heading: str) -> str:
    """GitHub-style heading anchor (before duplicate suffixes)."""
    text = re.sub(r"\s+#+\s*$", "", heading.strip())  # closing hashes
    text = text.replace("`", "")
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def collect_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    previous = ""
    for _, line in lines_outside_code(text):
        heading = None
        m = re.match(r"^#{1,6} (.+)$", line)
        if m:
            heading = m.group(1)
        elif re.match(r"^(=+|-+)\s*$", line) and previous.strip() and not previous.lstrip().startswith(("|", "-", "*")):
            heading = previous  # setext heading
        if heading is not None:
            slug = slugify(heading)
            count = seen.get(slug, 0)
            anchors.add(slug if count == 0 else f"{slug}-{count}")
            seen[slug] = count + 1
        for m in re.finditer(r"""<a\s[^>]*\b(?:id|name)=["']([^"']+)["']""", line):
            anchors.add(m.group(1))
        for m in re.finditer(r"""\bid=["']([^"']+)["']""", line):
            anchors.add(m.group(1))
        previous = line
    return anchors


def check_whitepaper(path: str, text: str) -> None:
    for no, line in lines_outside_code(text):
        body = strip_inline_code(line)
        if "BCP 14" in body or "RFC 2119" in body:
            continue
        for m in BCP14.finditer(body):
            error(path, no, f"uppercase {m.group(0)!r} in the informative whitepaper; normative keywords belong in the Internet-Draft (STYLE.md §2)")

    marker = "## Appendix B. References"
    if marker not in text:
        error(path, 1, "Appendix B. References heading not found")
        return
    before, rest = text.split(marker, 1)
    refs_part, after = (rest.split("## Appendix C", 1) + [""])[:2]
    ref_line_offset = before.count("\n") + 1

    defined: dict[int, int] = {}
    withdrawn: set[int] = set()
    for i, line in enumerate(refs_part.splitlines()):
        m = re.match(r"^(\d+)\. ", line)
        if m:
            n = int(m.group(1))
            if n in defined:
                error(path, ref_line_offset + i, f"reference [{n}] defined twice")
            defined[n] = ref_line_offset + i
            # References are never renumbered; a removed claim's source is
            # kept as a "*Withdrawn.*" entry, which must not be cited.
            if line[m.end():].startswith("*Withdrawn.*"):
                withdrawn.add(n)
    if defined:
        missing = sorted(set(range(1, max(defined) + 1)) - set(defined))
        if missing:
            error(path, ref_line_offset, f"gap in reference numbering: missing {missing}")

    # Citations anywhere outside Appendix B itself (Appendix C included).
    cited: dict[int, int] = {}
    after_offset = ref_line_offset + refs_part.count("\n")
    for chunk, offset in ((before, 0), (after, after_offset)):
        for no, line in lines_outside_code(chunk):
            for m in CITATION.finditer(strip_inline_code(line)):
                for n in expand_citation(m.group(1)):
                    cited.setdefault(n, offset + no)
    for n, no in sorted(cited.items()):
        if n not in defined:
            error(path, no, f"citation [{n}] has no entry in Appendix B")
        elif n in withdrawn:
            error(path, no, f"citation [{n}] points to a withdrawn reference")
    for n, no in sorted(defined.items()):
        if n not in cited and n not in withdrawn:
            error(path, no, f"reference [{n}] is never cited in the text")

    anchors = collect_anchors(text)
    for no, line in lines_outside_code(text):
        for m in re.finditer(r"\]\(#([^)\s]+)\)", line):
            if m.group(1) not in anchors:
                error(path, no, f"link to missing anchor #{m.group(1)}")


def changed_files() -> set[str]:
    if STAGED:
        return set(git("diff", "--cached", "--name-only").split())
    changed: set[str] = set()
    try:
        base = git("merge-base", "HEAD", "origin/main").strip()
        changed |= set(git("diff", "--name-only", f"{base}...HEAD").split())
    except subprocess.CalledProcessError:
        pass
    changed |= {l[3:] for l in git("status", "--porcelain").splitlines()}
    return changed


def check_html_sync() -> None:
    try:
        changed = changed_files()
    except (OSError, subprocess.CalledProcessError):
        return
    if WHITEPAPER in changed and WHITEPAPER_HTML not in changed:
        warn(f"{WHITEPAPER} changed but {WHITEPAPER_HTML} did not: sync the HTML rendering (STYLE.md §11)")


def main() -> int:
    for path in tracked_markdown():
        text = read(path)
        if text is None:
            continue
        check_language(path, text)
        if path in EDITORIAL:
            check_punctuation(path, text)
        if path == WHITEPAPER:
            check_whitepaper(path, text)
    check_html_sync()

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
