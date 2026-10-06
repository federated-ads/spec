# Federated Ads Protocol explainer

## Authors:

- Suneesh Rajan (Federated Ads Initiative)
- Arjun Krishna (Federated Ads Initiative)

This explainer was drafted with Claude, an AI model made by Anthropic, under the direction of the authors, who are accountable for its contents.

## Participate
- Issue tracker: https://github.com/federated-ads/spec/issues
- Discussion forum: https://github.com/federated-ads/spec/discussions

## Table of Contents

- [Introduction](#introduction)
- [User-Facing Problem](#user-facing-problem)
  - [Goals](#goals)
  - [Non-goals](#non-goals)
- [User research](#user-research)
- [Proposed Approach](#proposed-approach)
  - [Dependencies on non-stable features](#dependencies-on-non-stable-features)
  - [Solving goal 1: contextual ads without tracking](#solving-goal-1-contextual-ads-without-tracking)
  - [Solving goal 2: an advertiser withdraws a creative](#solving-goal-2-an-advertiser-withdraws-a-creative)
  - [Solving goal 3: delivery that both sides can verify](#solving-goal-3-delivery-that-both-sides-can-verify)
- [Alternatives considered](#alternatives-considered)
- [Accessibility, Internationalization, Privacy, and Security Considerations](#accessibility-internationalization-privacy-and-security-considerations)
- [Stakeholder Feedback / Opposition](#stakeholder-feedback--opposition)
- [References & acknowledgements](#references--acknowledgements)

## Introduction

The Federated Ads Protocol is an open protocol that lets independent servers ("nodes") run by publishers, advertisers, agencies or cooperatives find each other by domain, agree advertising deals, serve creatives under time-limited licences the advertiser can withdraw, prove delivery with signed, aggregated receipts recorded in transparency logs, and settle payment on any rail.

Matching is contextual by default, so protocol messages carry no cross-site identifiers. People who see ads get an explanation of why they saw them, an opt-out, an ad-free option and a way to report abuse. The full argument and evidence are in the [whitepaper](whitepaper/federated-ads-whitepaper.md); the wire protocol is specified in the Internet-Draft [`draft-rajan-federated-ads-protocol`](ietf/draft-rajan-federated-ads-protocol-00.md).

## User-Facing Problem

People who read websites, newsletters, podcasts, social feeds and AI assistants are tracked across sites so that ads can be targeted at them, and they have little ability to see or change why an ad was shown. Publishers that depend on advertising, especially small and independent ones, have no neutral, interoperable way to sell ads without joining that tracking system. Advertisers cannot reliably withdraw a creative once it has entered the supply chain, or verify independently what was delivered. The whitepaper sets out the evidence for each of these problems ([§1](whitepaper/federated-ads-whitepaper.md#1-the-problem)).

### Goals

1. **Contextual ads without tracking.** A reader sees ads matched to the page, episode, post or conversation, not to a profile of them built across sites.
2. **Advertiser control of creatives.** An advertiser can license a creative for a limited time and withdraw it, and receive proof that the withdrawal was honoured.
3. **Verifiable delivery.** Buyers, sellers and independent auditors can check what was delivered from signed records, without per-person data.
4. **Choice of intermediaries.** Any party can run a node and deal directly or through intermediaries it chooses, with every fee declared.
5. **User agency.** Every ad carries a "why this ad" disclosure, and people can opt out, pay to avoid ads and report abuse.

### Non-goals

- Cross-publisher reach and frequency management, which needs cross-site identity.
- Real-time per-impression auctions across nodes as the default.
- A token, blockchain or mandatory payment provider.
- Conversion tracking at the level of individual people.
- Moderating publishers' own content.

## User research

No user research has been conducted yet. The design draws on published studies of the advertising supply chain and on prior systems, summarised in the whitepaper ([§1](whitepaper/federated-ads-whitepaper.md#1-the-problem), [§2](whitepaper/federated-ads-whitepaper.md#2-what-has-been-tried-lessons-from-prior-art)). A pilot with publishers and advertisers is planned before any part of the protocol is marked stable ([§24](whitepaper/federated-ads-whitepaper.md#24-roadmap-and-success-metrics)).

## Proposed Approach

Nodes discover each other through `/.well-known/federated-ads` on their domain and exchange signed JSON objects over HTTPS. Each hop is signed with HTTP Message Signatures (RFC 9421), and stored objects carry W3C Data Integrity proofs. The lifecycle is: discover, describe inventory and policy, offer, agree a deal, license creatives, serve, report, revoke at any time, and settle ([whitepaper §5.3](whitepaper/federated-ads-whitepaper.md#53-lifecycle-in-brief)). Normative details are in the Internet-Draft.

The protocol does not change how browsers work and needs no new web platform API. Its browser-facing parts (rendering a creative, showing a "why this ad" disclosure, an optional viewability script) use existing platform features.

### Dependencies on non-stable features

- **W3C Attribution** (Private Advertising Technology Working Group, Working Draft) for a planned aggregate conversion-measurement profile.
- **IETF Distributed Aggregation Protocol** (PPM Working Group, Internet-Draft) for the same planned profile.
- The core protocol does not depend on either; both are optional profiles ([whitepaper §10.6](whitepaper/federated-ads-whitepaper.md#106-conversions-and-attribution)).

### Solving goal 1: contextual ads without tracking

A selling node publishes the contexts it can offer; a buying node's offer targets only context categories, language, coarse region, time, device class and placement. The selling node chooses an ad locally when the page renders, so nothing about the reader is sent to buyers ([whitepaper §6.6](whitepaper/federated-ads-whitepaper.md#66-ad-decisioning-on-the-selling-node), [§8](whitepaper/federated-ads-whitepaper.md#8-audience-matching-options-compared)).

```json
"targeting": {
  "taxonomy": "https://w3id.org/federated-ads/tax/1",
  "contexts": ["sports:cycling", "technology"],
  "regions": ["IN-KL", "IN-KA"],
  "languages": ["en", "ml"]
}
```

*Taken from the Internet-Draft's Offer example; illustrative.*

### Solving goal 2: an advertiser withdraws a creative

The advertiser issues a Licence bound to one deal, one licensee and an expiry. To withdraw the creative, it appends a signed Revocation to its own transparency log and sends it to every licensee. Each licensee returns a signed, logged acknowledgement, and impressions after the deadline are not billable ([whitepaper §7.4](whitepaper/federated-ads-whitepaper.md#74-revocation-mechanics)).

```json
{
  "type": "Revocation",
  "id": "https://ads.acme.example/fa/revocations/5b2c",
  "issuer": "https://ads.acme.example/fa/node",
  "issuedAt": "2026-10-12T08:30:00Z",
  "scope": {
    "deal": "https://ads.acme.example/fa/deals/3d9e7a1c",
    "manifestHash": "sha256-LJpNdR1icOVWU9oFx6AudeMrsiNfhqPDpjdn2UZhUJQ="
  },
  "reason": "pricing-error",
  "effectiveAt": "2026-10-12T08:30:00Z",
  "proof": { "type": "DataIntegrityProof", "...": "..." }
}
```

*Taken from the Internet-Draft's Revocation example (context omitted); illustrative.*

### Solving goal 3: delivery that both sides can verify

The selling node reports delivery as signed, aggregated cells (deal, creative, hour, context, coarse region, event type and count), with small cells merged, and commits each batch to a transparency log that independent witnesses cosign. Deals state how much further verification is required ([whitepaper §10.2](whitepaper/federated-ads-whitepaper.md#102-aggregated-receipts), [§10.3](whitepaper/federated-ads-whitepaper.md#103-verification-levels)).

## Alternatives considered

### Extending existing protocols only (OpenRTB, agent protocols)

#### Pros

* Existing buyers, sellers and libraries.

#### Cons

* Real-time bidding broadcasts information about each impression to many bidders; ownership, revocation and verifiable receipts would have to be added on.

#### Reason for rejection

A new core built on existing primitives, with bridges to OpenRTB and complementary use alongside agent protocols such as AdCP, keeps the design properties while giving existing demand a way in ([whitepaper §14.1](whitepaper/federated-ads-whitepaper.md#141-approaches-compared)).

### A network of existing ad networks

#### Pros

* Fast adoption by incumbents.

#### Cons

* Power stays with the intermediaries the protocol is meant to make optional.

#### Reason for rejection

Any network can run a Federated Ads node, so this model is a subset of the chosen one ([whitepaper §5.1](whitepaper/federated-ads-whitepaper.md#51-models-considered)).

### Fully on-chain matching and settlement

#### Pros

* Programmable settlement and public auditability.

#### Cons

* Cost and latency per event, commercial data exposed on public ledgers, and regulatory burden.

#### Reason for rejection

Signed objects and transparency logs give the auditability without a chain; on-chain settlement remains an optional profile ([whitepaper §5.1](whitepaper/federated-ads-whitepaper.md#51-models-considered)).

### Cross-site identity for targeting

#### Pros

* Higher relevance and cross-publisher frequency control.

#### Cons

* Tracks people across sites, which the protocol exists to avoid.

#### Reason for rejection

Contextual matching is mandatory; on-device and first-party opt-in profiles are optional, and cross-site identifiers are prohibited in protocol messages ([whitepaper §8](whitepaper/federated-ads-whitepaper.md#8-audience-matching-options-compared)).

## Accessibility, Internationalization, Privacy, and Security Considerations

- **Accessibility.** Every ad carries a "why this ad" disclosure in human-readable and machine-readable form, and it must render on every surface, including as a spoken disclosure on audio and AI surfaces ([whitepaper §12](whitepaper/federated-ads-whitepaper.md#12-end-user-rights)).
- **Internationalization.** Objects carry language tags, currencies as ISO codes with decimal-string amounts, and regions as country or first-level subdivision codes. Legal variation is carried in machine-readable jurisdiction profiles ([whitepaper §19.6](whitepaper/federated-ads-whitepaper.md#196-jurisdiction-policy-profiles)).
- **Privacy.** No cross-site identifiers; aggregated receipts with minimum cell sizes; IP address and user agent processed transiently on the selling node only; Global Privacy Control honoured; minor-safe defaults ([whitepaper §18](whitepaper/federated-ads-whitepaper.md#18-privacy-considerations)).
- **Security.** Domain-bound keys, signed hops and objects, witnessed logs against equivocation, hash-pinned creative assets and a sandbox for interactive creatives ([whitepaper §17](whitepaper/federated-ads-whitepaper.md#17-security-considerations)).

## Stakeholder Feedback / Opposition

The project is at the discussion stage, and no implementer or standards body has stated a position yet.

- Browser engines: No signals
- Publishers and advertisers: No signals
- IAB Tech Lab: No signals
- AgenticAdvertising.org (AdCP): No signals

## References & acknowledgements

This explainer follows the W3C TAG template, *Writing Effective Explainers*. The whitepaper's Appendix B lists every source.

Thanks to the following proposals, projects and standards for their work on similar problems that influenced this proposal:

- ActivityPub and the Fediverse Enhancement Proposals
- Ad Context Protocol (AdCP)
- ads.txt, sellers.json and ads.cert
- AT Protocol labelers
- C2PA
- Certificate Transparency and the C2SP transparency-log specifications
- EthicalAds
- Global Privacy Control
- IETF Distributed Aggregation Protocol and W3C Attribution
- OpenRTB and AdCOM
- Privacy Pass
