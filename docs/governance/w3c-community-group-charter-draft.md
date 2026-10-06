# [DRAFT] Federated Ads Protocol Community Group Charter

This draft follows the W3C Community Group charter template (https://github.com/w3c/cg-charter, `CGCharter.md`, checked 5 October 2026). Boilerplate from the template is kept word for word where it carries process meaning. Group-specific text is based on the Federated Ads Protocol whitepaper v0.3.

This Charter is a work in progress. To submit feedback, please use https://github.com/federated-ads/spec/issues, where the Charter is being developed. (Remove this sentence before the group adopts the charter.)

* **This Charter:** https://github.com/federated-ads/spec/blob/main/CHARTER.md (to be created)
* **Previous Charter:** none
* **Start Date:** {date the group adopts the charter}
* **Last Modified:** 5 October 2026

## Goals

Digital advertising pays for much of the open web, but the systems that deliver it are concentrated, opaque and built on tracking people. Independent publishers, newsletters, podcasts, fediverse communities and AI chat services have no neutral, interoperable way to sell advertising directly.

The mission of the Federated Ads Protocol Community Group is to incubate an open, federated protocol in which independent servers ("nodes") run by publishers, advertisers, agencies or cooperatives can:

1. discover each other by domain;
2. agree deals with signed offers;
3. serve creatives that the advertiser still owns, under time-limited licences it can revoke;
4. prove delivery with signed, aggregated receipts recorded in tamper-evident logs;
5. settle payment on any payment rail the parties choose.

The protocol is contextual by default, carries no cross-site personal identifiers, and gives the people who see ads enforceable rights: an explanation, an opt-out, an ad-free option and a way to report abuse.

## Scope of Work

The group will define, in Specifications:

* **Discovery and identity:** how nodes publish their keys, endpoints and policies under their domain, using existing mechanisms such as well-known URIs and WebFinger.
* **Core objects and their lifecycle:** offers, deals, creative manifests, licences, revocations, receipt batches, statements and disputes, with state machines and error semantics.
* **Signatures:** per-hop authentication with HTTP Message Signatures and end-to-end signatures on stored objects with W3C Data Integrity, without requiring a JSON-LD processor to verify.
* **Transparency logs:** how nodes commit receipts, revocations, statements and key rotations to append-only logs, and how witnesses check them.
* **Vocabulary:** JSON Schemas, a JSON-LD context under `https://w3id.org/federated-ads/`, and registries (event types, pricing models, surface, settlement and jurisdiction profiles, revocation reasons, error types, taxonomy versions and critical extensions; see whitepaper section 15.10).
* **Measurement and verification:** aggregated receipt cells with minimum-count thresholds, verification levels V0–V4, the open measurement module, and conformance levels (core, extended, verified).
* **Market objects:** inventory descriptions (including ad-density and other quality signals), standing offers, pricing models (including cost per viewable hour), and the cooperative selling-node profile.
* **Surface profiles:** web display and native, social and fediverse, email newsletters, podcasts and audio, and AI chat surfaces.
* **End-user rights:** the required "why this ad" disclosure, opt-out handling (including Global Privacy Control), ad-free offers, reporting and blocking, and the minor-safe default.
* **Bridges (non-normative mappings or normative profiles as the group decides):** to OpenRTB 2.6, AdCOM, VAST, the IAB taxonomies, ads.txt and sellers.json, and C2PA.

Key use cases: a newsletter selling a flat-fee sponsorship to an advertiser it has never dealt with; a podcast host proving delivery to an agency without sharing listener data; a fediverse instance running community-approved ads; an advertiser withdrawing a creative from every placement within a defined time.

Where the IETF takes up the wire protocol (see Dependencies), this group will not duplicate that work. It will instead focus on the vocabulary, surface profiles, end-user rights and conformance, and reference the IETF document.

### Out of Scope

* New browser or user-agent APIs. These belong in the Private Advertising Technology Community Group (PATCG) and Working Group (PATWG).
* Cross-site identifiers, cross-publisher reach and frequency management, and individual-level conversion tracking.
* Defining its own attribution system. The group may profile existing aggregate systems, such as the W3C Attribution API or IETF DAP.
* A native token or blockchain, or any mandatory payment provider. Settlement profiles, including the optional regulated-stablecoin profile, are referenced, not defined.
* Moderating or judging publisher content.
* Video and connected TV beyond what VAST bridging provides.
* Any discussion of actual or planned prices, fees or commercial terms of specific participants (see the antitrust policy below).
* Operating network infrastructure such as relays, labelers, witnesses or run-time registry services.

## Deliverables

### Specifications

* **Federated Ads Protocol: Core.** Discovery, objects, lifecycle, signatures and transparency logs. If the IETF adopts the wire protocol, this becomes a W3C vocabulary and binding document that references the IETF specification.
* **Federated Ads Protocol: Vocabulary and Schemas.** JSON Schemas, the JSON-LD context and registries.
* **Federated Ads Protocol: Surface Profiles.** Web, social, email, audio and AI chat. May be split into separate documents.
* **Federated Ads Protocol: End-User Rights.** Disclosure, opt-out, ad-free offers, reporting and minor protections.

Estimated schedule: first drafts of Core and Vocabulary within 6 months of the group's start; a candidate Core only after two independent interoperable implementations exist.

### Non-Normative Reports

The group may produce other Community Group Reports within the scope of this charter that are not Specifications, such as use cases, requirements, or white papers.

Planned reports: use cases and requirements; security and privacy considerations; implementation guide; mapping notes for OpenRTB, VAST and the IAB taxonomies. The existing Federated Ads Protocol whitepaper is input to the group, not a group report.

### Test Suites and Other Software

The group **may** produce test suites to support the specifications. See the GitHub `LICENSE` file for test suite contribution licensing information.

The group intends to maintain a conformance test suite and test vectors. Reference implementations may be developed by participants outside the group; the group does not endorse any one implementation.

## Dependencies or Liaisons

* **W3C Private Advertising Technology CG and WG (PATCG, PATWG):** client-side privacy features, the Attribution API, and privacy principles for advertising.
* **W3C Social Web Working Group and Social Web Incubator CG:** the ActivityPub surface profile.
* **W3C Verifiable Credentials Working Group:** Data Integrity and Controlled Identifiers, which this group uses.
* **W3C privacy and security horizontal review groups:** privacy and security review of drafts.
* **IETF:** the wire protocol may be brought to the IETF through DISPATCH as `draft-rajan-federated-ads-protocol`. Related IETF work: HTTP Message Signatures, Privacy Pass, Oblivious HTTP, DAP.
* **IAB Tech Lab:** ads.txt, sellers.json, ads.cert, OpenRTB, AdCOM, VAST, taxonomies, and the AAMP agentic protocols.
* **C2PA:** creative provenance.
* **C2SP:** transparency log formats (tlog-tiles, signed-note, tlog-witness).
* **Fediverse Enhancement Proposals (FEP):** fediverse integration.

## Community and Business Group Process

The group operates under the [Community and Business Group Process](https://www.w3.org/community/about/process). Terms in this Charter that conflict with those of the Community and Business Group Process are void.

As with other Community Groups, W3C seeks organizational licensing commitments under the [W3C Community Contributor License Agreement (CLA)](https://www.w3.org/community/about/process/cla/). When people request to participate without representing their organization's legal interests, W3C will in general approve those requests, with the following understanding: W3C will seek and expect an organizational commitment under the CLA starting with the individual's first request to make a contribution to a group Deliverable. The section on Contribution Mechanics describes how W3C expects to monitor these contribution requests.

The [W3C Code of Conduct](https://www.w3.org/policies/code-of-conduct/) and [W3C Antitrust and competition policy](https://www.w3.org/policies/antitrust-2024/) apply to participation in this group.

In addition, consistent with the whitepaper's competition-law section, the group publishes agendas and minutes, and never shares forward-looking or participant-level pricing through group channels.

## Work Limited to Charter Scope

The group will not publish specifications on topics other than those listed under Specifications. See below for how to modify the charter.

## Contribution Mechanics

Substantive contributions to specifications can only be made by Community Group Participants who have agreed to the [W3C Community Contributor License Agreement (CLA)](https://www.w3.org/community/about/process/cla/).

Reports other than Specifications published by this group should use the [W3C Software and Document License](https://www.w3.org/copyright/software-license-2023/) where possible.

Community Group participants agree to make all contributions in the GitHub repository the group is using for the particular document — e.g., via pull requests, issues, or comments on existing issues.

All GitHub repositories attached to the Community Group must contain a copy of the [CONTRIBUTING](https://github.com/w3c/licenses/blob/main/CG-CONTRIBUTING.md) and [LICENSE](https://github.com/w3c/licenses/blob/main/CG-LICENSE.md) files.

The group's repositories are under https://github.com/federated-ads. (Note for the proposer: the whitepaper licenses text under CC BY 4.0 and code under Apache-2.0. Repositories attached to the group need the W3C CG LICENSE file. Keep the whitepaper in a repository or folder that is clearly marked as pre-group input, or reconcile the licences before attaching the spec repository.)

## Transparency

The group will conduct all technical work in public. If the group uses GitHub, technical work will occur in its GitHub repositories (and not privately on mailing lists).

Meetings may be restricted to Community Group participants, but a public summary or minutes must be posted to the group's public mailing list or as an issue on GitHub.

The group records how its documents were produced, including the use of AI tools, in each document's acknowledgements.

## Decision Process

This group will seek to make decisions where there is consensus. Groups are free to decide how to make decisions (e.g., Participants who have earned Committer status for a history of useful contributions assess consensus, or the Chair assesses consensus, or where consensus isn't clear there is a Call for Consensus [CfC] to allow multi-day online feedback for a proposed course of action). It is expected that participants can earn Committer status through a history of valuable contributions, as is common in open source projects. After discussion and due to consideration of different opinions, a decision should be publicly recorded (where GitHub is used as the resolution of an Issue).

If substantial disagreement remains (e.g., the group is divided) and the group needs to decide an Issue in order to continue to make progress, the Committers will choose an alternative that had substantial support (with a vote of Committers if necessary). Individuals who disagree with the choice are strongly encouraged to take ownership of their objection by taking ownership of an alternative fork. This is explicitly allowed (and preferred to blocking progress) to let implementation experience inform which spec is ultimately chosen by the group to move ahead with.

Any decisions reached at any meeting are tentative and should be recorded in a GitHub Issue for groups that use GitHub and otherwise on the group's public mail list. Any group participant may object to a decision reached at an online or in-person meeting within 7 days of publication of the decision provided that they include clear technical reasons for their objection. The Chairs will facilitate discussion to try to resolve the objection according to this decision process.

It is the Chairs' responsibility to ensure that the decision process is fair, respects the consensus of the CG, and does not unreasonably favor or discriminate against any group participant or their employer.

Group-specific rules, carried over from the whitepaper (section 23.3) and CONTRIBUTING.md:

* No feature is marked stable until at least two independent, interoperable implementations exist.
* Breaking changes to a feature marked stable need at least 90 days' public notice and a migration path.
* Calls for Consensus run for at least 14 days.
* The group seeks publisher, advertiser and user-advocacy perspectives on every substantive decision.

## Chair Selection

Participants in this group choose their Chair(s) and can replace their Chair(s) at any time using whatever means they prefer. However, if 5 participants, no two from the same organization, call for an election, the group must use the following process to replace any current Chair(s) with a new Chair, consulting the Community Development Lead on election operations (e.g., voting infrastructure and using [RFC 3797](https://datatracker.ietf.org/doc/html/rfc3797)):

* Participants announce their candidacies. Participants have 14 days to announce their candidacies, but this period ends as soon as all participants have announced their intentions. If there is only one candidate, that person becomes the Chair. If there are two or more candidates, there is a vote. Otherwise, nothing changes.
* Participants vote. Participants have 21 days to vote for a single candidate, but this period ends as soon as all participants have voted. The individual who receives the most votes, no two from the same organization, is elected chair. In case of a tie, RFC3797 is used to break the tie. An elected Chair may appoint co-Chairs.

Participants dissatisfied with the outcome of an election may ask the Community Development Lead to intervene. The Community Development Lead, after evaluating the election, may take any action including no action.

Initial arrangement: the proposer (Suneesh Rajan) acts as interim chair at launch and will seek a co-chair from a different organization within six months, to reduce single-maintainer risk. No single organization should hold all chair positions once the group has participants from three or more organizations.

## Amendments to This Charter

The group can decide to work on a proposed amended charter, editing the text using the Decision Process described above. The decision on whether to adopt the amended charter is made by conducting a 30-day vote on the proposed new charter. The new charter, if approved, takes effect on either the proposed date in the charter itself, or 7 days after the result of the election is announced, whichever is later. A new charter must receive 2/3 of the votes cast in the approval vote to pass. The group may make simple corrections to the charter such as deliverable dates by the simpler group decision process rather than this charter amendment process. The group will use the amendment process for any substantive changes to the goals, scope, deliverables, decision process or rules for amending the charter.

## Acknowledgements

This draft charter was prepared with Claude (Anthropic) under the direction of Suneesh Rajan, who is responsible for its contents.
