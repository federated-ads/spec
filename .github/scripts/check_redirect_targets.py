#!/usr/bin/env python3
"""Fail if a change would break the pages that w3id.org/federated-ads/ redirects to.

The redirect rules live in perma-id/w3id.org (ids/federated-ads/.htaccess) and
point at the GitHub Pages site built from docs/. Moving or deleting any of the
files below, or dropping an error-type anchor, breaks a published identifier.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
DRAFT = DOCS / "ietf" / "draft-rajan-federated-ads-protocol-00.md"

REQUIRED = [
    "index.md",            # w3id.org/federated-ads/ (and anything unmatched)
    "ns/v0.jsonld",        # w3id.org/federated-ads/v0 for JSON-LD clients
    "ns/v0.md",            # w3id.org/federated-ads/v0 for browsers
    "errors/index.md",     # w3id.org/federated-ads/errors/<name>
    "rel/index.md",        # w3id.org/federated-ads/rel/<name>
    "tax/index.md",        # w3id.org/federated-ads/tax/...
]

problems = []

for rel in REQUIRED:
    if not (DOCS / rel).is_file():
        problems.append(f"missing redirect target docs/{rel}")

context_file = DOCS / "ns" / "v0.jsonld"
if context_file.is_file():
    try:
        ctx = json.loads(context_file.read_text())["@context"]
        if ctx.get("@vocab") != "https://w3id.org/federated-ads/v0#":
            problems.append("docs/ns/v0.jsonld: @vocab is not https://w3id.org/federated-ads/v0#")
    except (ValueError, KeyError, AttributeError) as exc:
        problems.append(f"docs/ns/v0.jsonld is not a valid JSON-LD context: {exc}")

errors_page = DOCS / "errors" / "index.md"
if errors_page.is_file() and DRAFT.is_file():
    draft = DRAFT.read_text()
    end = draft.find("{: #tab-errors")
    start = draft.rfind("| Name | Status | Meaning |", 0, end)
    names = re.findall(r"^\| `([a-z0-9-]+)` \| \d{3} \|", draft[start:end], flags=re.M) if start != -1 else []
    if not names:
        problems.append("could not read the error-type table from the Internet-Draft")
    page = errors_page.read_text()
    for name in names:
        if f'id="{name}"' not in page:
            problems.append(f"docs/errors/index.md has no anchor for error type '{name}'")

rel_page = DOCS / "rel" / "index.md"
if rel_page.is_file() and not re.search(r"^## node\s*$", rel_page.read_text(), flags=re.M):
    problems.append("docs/rel/index.md has no '## node' section (target of w3id.org/federated-ads/rel/node)")

if problems:
    print("Redirect target check failed:")
    for p in problems:
        print(f"  - {p}")
    print("\nIf a target really must move, update ids/federated-ads/.htaccess in perma-id/w3id.org first.")
    sys.exit(1)
print(f"Redirect targets OK ({len(REQUIRED)} files, error anchors and link relations present).")
