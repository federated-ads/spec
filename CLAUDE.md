# Federated Ads Protocol: instructions for Claude

The editorial rules for this repository live in `docs/STYLE.md`, which is shared with human contributors. Follow it for every edit:

@docs/STYLE.md

## Rules specific to working with Claude

- **The evidence gate is absolute** (STYLE.md §4). Before writing any factual sentence, open the source and confirm the fact is there. If you cannot verify it, do not write it; tell the user what could not be supported. Never fill a gap from memory.
- **Ideals before instructions.** If a requested change conflicts with the ideals in STYLE.md §1, stop and flag the conflict with a recommendation. Do not write it in silently.
- **Cross-section consistency.** When editing a section, read the sections it references and the sections that reference it, and report contradictions.
- **Draft impact.** When a whitepaper change touches objects, fields, flows or conformance, tell the user the Internet-Draft (`docs/ietf/`) needs a matching change.
- **HTML sync.** `docs/whitepaper/web/federated-ads-whitepaper.html` has no generator. Sync it by hand after Markdown edits, or batch the sync at the end of a review part and say so.
- **Git.** Commit with `/atomic:atomic-commit`, never raw git. No AI co-author trailers. `main` is protected: work on a branch and open a pull request. Ask which source branch to use before creating one.
- **Privacy.** Never send the maintainers' personal details (for example email addresses) to external services, including in request headers.

## Section-by-section review method

When reviewing the paper with the user, take one subsection at a time:

1. Explain in plain terms what the section says and how its argument runs.
2. Verify every factual claim against current primary sources, and report what is confirmed, out of date or unsupported.
3. Flag clarity, structure, tone, length-budget and consistency problems, including conflicts with other sections or with the ideals.
4. Ask the user to decide, with a recommended option.
5. Apply the approved changes, update references, the glossary and Appendix C, then move on.
