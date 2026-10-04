# Federated Ads Protocol: Internet-Draft

This directory holds the IETF Internet-Draft that specifies the wire
protocol of the Federated Ads Protocol.

| File | What it is |
|---|---|
| `draft-rajan-federated-ads-protocol-00.md` | Source, in kramdown-rfc Markdown. Edit this file. |
| `draft-rajan-federated-ads-protocol-00.xml` | Generated xml2rfc v3 XML. This is the file you submit. |
| `draft-rajan-federated-ads-protocol-00.txt` | Generated plain-text rendering (about 75 pages). |
| `draft-rajan-federated-ads-protocol-00.html` | Generated HTML rendering. |

## What the draft covers

The draft is normative and covers only the wire protocol:

- the JSON object model (Node, Policy, Inventory, Offer, Deal, Licence,
  Revocation, ReceiptBatch, Statement and the other objects);
- the HTTP Message Signatures (RFC 9421) and W3C Data Integrity
  (`eddsa-jcs-2022`) profiles;
- discovery through `/.well-known/federated-ads` and WebFinger;
- inbox messaging, licensing and revocation, receipts and transparency
  logs, and conformance levels;
- security, privacy and IANA considerations.

The market design, economics, governance and regulatory analysis stay in
the whitepaper (`../whitepaper/federated-ads-whitepaper.md`). The draft
cites the whitepaper as an informative reference.

## Why the name is `draft-rajan-federated-ads-protocol`

An individual Internet-Draft (one not adopted by a working group) is
named `draft-<lead author's surname>-<topic>-<version>`. The name may use
only lowercase ASCII letters, digits and hyphens. The suggested name
`openads-initiative-openads-protocol-00` does not follow this
convention, for three reasons:

1. it does not begin with `draft-`;
2. the second part should be the author's surname, not an organization;
3. it uses the old project name, which was dropped to avoid confusion
   with unrelated "OpenAds" products.

If a working group adopts the draft, it will be renamed
`draft-ietf-<wg>-federated-ads-protocol-00`. Some authors put the target
group in an individual draft's name, for example
`draft-rajan-dispatch-federated-ads`. That is optional, and this draft
does not do it.

## Intended status

The draft is submitted as **Experimental** (`category: exp`). This is a
normal choice for a new individual -00 submission that has no
implementations yet. If a working group adopts it, and there are
interoperable implementations, it can move to the Standards Track
(`category: std`).

## How to build

You need Ruby 3.x and Python 3.

```sh
# kramdown-rfc (Markdown to XML). On macOS, use Homebrew Ruby, not the
# system Ruby 2.6.
gem install kramdown-rfc

# xml2rfc (XML to text and HTML)
python3 -m venv .venv && . .venv/bin/activate
pip install xml2rfc

# Build
kramdown-rfc draft-rajan-federated-ads-protocol-00.md \
  > draft-rajan-federated-ads-protocol-00.xml
xml2rfc --v3 --text --html draft-rajan-federated-ads-protocol-00.xml

# Optional: check nits (https://github.com/ietf-tools/idnits)
idnits draft-rajan-federated-ads-protocol-00.txt
```

`kdrfc draft-rajan-federated-ads-protocol-00.md -h -t` runs both steps in
one command. kramdown-rfc downloads RFC and I-D reference entries from
bib.ietf.org, so the first build needs network access.

The current build gives **no errors or warnings** from kramdown-rfc
1.7.43 or xml2rfc 3.34.1. idnits 2.17.1 reports:

- **0 errors.**
- **1 warning:** "couldn't figure out when the document was first
  submitted". This is normal for a document that has never been
  submitted.
- **1 comment:** RFC 6962 is obsolete. It is cited deliberately,
  alongside RFC 9162, because the leaf format is named after it.

## How to submit

Use the IETF Datatracker submission tool at
<https://datatracker.ietf.org/submit/>. This was checked on 5 October
2026.

1. Create a Datatracker account if you do not have one, and sign in.
2. Before submitting, read the IETF Note Well
   (<https://www.ietf.org/about/note-well/>) and BCP 78/79. Submitting
   means you agree to the IETF Trust's licence terms (`ipr: trust200902`).
   It also obliges you to disclose any patents or patent applications
   you know of that cover the draft.
3. Upload the **XML** file. The Datatracker prefers xml2rfc v3 and
   generates the text and HTML renderings itself, so a separate `.txt`
   file is optional.
4. Check the metadata the tool extracts (title, authors, abstract), then
   submit.
5. The first version of a new draft must be confirmed by email. The
   Datatracker sends a confirmation link to the author's address. The
   draft is posted only after you click it.
6. **Submission blackout:** the Datatracker currently shows a cut-off of
   **2026-11-02 23:59 UTC** for drafts before the next IETF meeting.
   Submissions reopen after **2026-11-14 23:59 PST**. Submit before the
   cut-off if you want the draft discussed at that meeting.
7. If you have technical problems, contact support@ietf.org.

## Recommended path to discussion

1. **DISPATCH (dispatch@ietf.org).** DISPATCH is the IETF's entry point
   for proposals of new work in the Applications and Real-Time (ART)
   area, the Security area, and the non-transport parts of the Web and
   Internet Transport (WIT) area. Subscribe at
   <https://www.ietf.org/mailman/listinfo/dispatch>. After the draft is
   posted, send a short message that:
   - links to the draft;
   - states the problem;
   - names the existing work it builds on (RFC 9421, Data Integrity,
     transparency logs, Privacy Pass);
   - asks where the work should go.

   You can also ask the DISPATCH chairs for agenda time at the next
   meeting.
2. **SECDISPATCH no longer exists separately.** The SECDISPATCH working
   group has closed and merged into DISPATCH; its list,
   secdispatch@ietf.org, is archival. Raise the signing,
   transparency-log and Privacy Pass parts on dispatch@ietf.org too,
   for example by asking for review by the Security area.
3. **Registration reviews (later).** The media type
   `application/federated-ads+json` is reviewed on media-types@ietf.org.
   The `/.well-known/federated-ads` URI is reviewed on
   wellknown-uri-review@ietf.org. You can ask for early review once the
   draft is posted.
4. **Related groups to consult.**
   - HTTPAPI: HTTP API conventions.
   - PRIVACYPASS: the V3 attestation binding.
   - The transparency-log community (C2SP, and the IETF's
     transparency-related work).

   Interest from these groups would strengthen the DISPATCH case.

Do not expect DISPATCH to recommend a new working group until there is
evidence of interest from implementers.

## Open issues

The draft's "Open Issues" appendix lists known gaps. Track discussion at
<https://github.com/federated-ads/spec/issues>.
