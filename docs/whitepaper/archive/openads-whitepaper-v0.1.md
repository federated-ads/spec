# The Open Ads Standard

### A Federated, Owner-Controlled Protocol for Advertising on the Open Web

**Whitepaper · Version 0.1 (Draft for Public Comment) · 4 October 2026**

**Published by:** The OpenAds Initiative
**Contributors:** Suneesh Rajan; Claude (Anthropic)
**License:** Text © the contributors, released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Reference code (when published) under Apache-2.0.

> **Authored with Claude.** This whitepaper was researched, structured, and drafted in collaboration with Claude, an AI model made by Anthropic, under the direction of a human contributor who set its goals, made every design decision, and is accountable for its contents. See [§18 AI-Assistance Disclosure](#18-ai-assistance-disclosure).

---

## Abstract

Digital advertising funds much of the open internet, yet the machinery that delivers it is concentrated in a handful of platforms, opaque to the people who pay for it, and dependent on tracking individuals across the web. Publishers outside the largest platforms — independent sites, newsletters, podcasts, fediverse communities, and emerging AI interfaces — have no neutral, interoperable way to sell advertising on their own terms. Advertisers, meanwhile, lose control of their creative the moment it enters the supply chain.

This paper proposes the **Open Ads Standard ("OpenAds")**: an open protocol through which independent nodes — run by publishers, advertisers, agencies, cooperatives, or networks — discover one another, exchange signed advertising offers, deliver creatives that **remain owned by and revocable by the advertiser at any time**, and settle payment using **cryptographically signed proof-of-delivery receipts** on any payment rail. OpenAds is contextual-first and privacy-preserving by default, gives end users enforceable rights (explanation, opt-out, ad-free payment, and reporting), and spans web display and native, fediverse and social feeds, newsletters and podcasts, and AI/chat surfaces.

We describe the problem, the design principles, a hybrid federated architecture, comparisons of the main design alternatives, a draft v0.1 protocol specification with example payloads, a threat model, a governance model, and a roadmap. This is a draft for public comment; every section is open to revision.

---

## Table of Contents

1. [The Problem](#1-the-problem)
2. [Vision and Design Principles](#2-vision-and-design-principles)
3. [Actors and Roles](#3-actors-and-roles)
4. [Architecture: Federated Hybrid Nodes](#4-architecture-federated-hybrid-nodes)
5. [Creative Ownership and Revocation](#5-creative-ownership-and-revocation)
6. [Audience Matching: Options Compared](#6-audience-matching-options-compared)
7. [Brand Safety and Content Policy: Options Compared](#7-brand-safety-and-content-policy-options-compared)
8. [Measurement and Proof of Delivery](#8-measurement-and-proof-of-delivery)
9. [Settlement: Rail-Agnostic Payments](#9-settlement-rail-agnostic-payments)
10. [End-User Rights](#10-end-user-rights)
11. [Surfaces in Scope for v1](#11-surfaces-in-scope-for-v1)
12. [Relationship to Existing Standards: Options Compared](#12-relationship-to-existing-standards-options-compared)
13. [Draft Protocol Specification v0.1](#13-draft-protocol-specification-v01)
14. [Security and Threat Model](#14-security-and-threat-model)
15. [Governance and Licensing](#15-governance-and-licensing)
16. [Roadmap](#16-roadmap)
17. [Open Questions](#17-open-questions)
18. [AI-Assistance Disclosure](#18-ai-assistance-disclosure)
19. [Glossary](#19-glossary)
20. [References](#20-references)

---

## 1. The Problem

### 1.1 Concentration

A small number of companies operate the dominant ad buying tools, selling tools, exchanges, and the largest owned-and-operated inventories — often simultaneously. When the same entity represents buyers, represents sellers, and runs the marketplace between them, prices, rules, and data access are set by that entity rather than by an open market. Publishers outside the largest platforms must accept whatever terms and revenue shares are offered, and switching costs are high because integrations are proprietary.

### 1.2 Opacity and Leakage

The programmatic supply chain is long and difficult to audit. The ISBA/PwC *Programmatic Supply Chain Transparency Study* (2020) found that, on average, publishers received roughly half of advertiser spend, and that around 15% of spend could not be attributed to any identifiable party at all. Advertisers frequently cannot prove where their ads ran; publishers frequently cannot see what an advertiser paid. Ad fraud thrives in exactly this kind of unverifiable environment.

### 1.3 Surveillance as Infrastructure

Mainstream ad targeting was built on cross-site identifiers, third-party cookies, device fingerprinting, and data brokerage. This model is under sustained regulatory pressure (GDPR, ePrivacy, CCPA/CPRA, the EU Digital Markets and Digital Services Acts) and erodes user trust. Browser-vendor efforts to replace it have been fragmented and, in several cases, controlled by the same firms that dominate ad sales.

### 1.4 Loss of Creative Control

Once an advertiser's creative enters the supply chain it is copied — into ad servers, exchanges, caches, and CDNs the advertiser does not control. Pulling a creative (because of a legal issue, a recall, a pricing error, an expired licence for talent or music, or a brand crisis) is slow and incomplete. Stale creative continues to run, sometimes for days.

### 1.5 The Unmonetized Open Web

New and independent publishing ecosystems — the fediverse (ActivityPub, AT Protocol), independent newsletters, podcasts, open-source project sites, and now AI assistants and agents — lack any values-aligned, interoperable advertising layer. Each either avoids advertising entirely, signs an exclusive deal with a single network, or builds bespoke sponsorship sales. None of these scale, and none interoperate.

### 1.6 What Is Missing

There is no **open, federated protocol** for advertising — the equivalent of what SMTP is for email or ActivityPub is for social posting — that lets any party run a node, transact directly or through intermediaries of its choosing, keep ownership of what it contributes, and verify what happened.

---

## 2. Vision and Design Principles

**Vision:** *Anyone can run an ad node. Advertisers own their creative. Publishers own their audience relationship. Users own their attention. Everyone can verify what happened.*

| # | Principle | What it means in practice |
|---|-----------|---------------------------|
| P1 | **Federated, not centralized** | No mandatory central server, exchange, or registry. Nodes interoperate via an open protocol. Intermediaries are optional and replaceable. |
| P2 | **Owner control of creative** | Creatives are referenced, licensed, and revocable — never surrendered. Revocation propagates within a bounded time. |
| P3 | **Privacy by default** | Contextual matching by default. No cross-site personal identifiers in the protocol. Any personal signal is opt-in, minimal, and preferably processed on-device. |
| P4 | **Verifiable, not trusted** | Every economically meaningful event (offer, acceptance, delivery, click, revocation) is a signed, timestamped, auditable message. |
| P5 | **Rail-agnostic money** | The protocol proves *what is owed*; it does not dictate *how it is paid*. |
| P6 | **User agency** | Users can understand, refuse, pay to avoid, and report ads, and those choices are honored network-wide. |
| P7 | **Surface-neutral** | One protocol across web, apps, feeds, email, audio, and AI interfaces, with surface-specific profiles. |
| P8 | **Bridge to today** | Interoperate with existing buying tools so the network is not empty on day one. |
| P9 | **Simple to implement** | Built on boring, widely implemented primitives: HTTPS, JSON, HTTP Message Signatures, WebFinger. A minimal node should be buildable in a weekend. |

---

## 3. Actors and Roles

| Actor | Description | Runs a node? |
|-------|-------------|--------------|
| **Advertiser** | Brand, business, or individual buying attention. Owns creatives. | Optional (may delegate to an agency/network node) |
| **Publisher** | Website, app, newsletter, podcast, fediverse instance, or AI surface that displays ads. | Optional (may delegate) |
| **Agency / Buying node** | Acts for one or more advertisers. | Yes |
| **Network / Selling node** | Represents one or more publishers (e.g., a co-op of independent sites or a group of fediverse instances). | Yes |
| **Exchange / Relay node** | Optional aggregator that routes offers between many buying and selling nodes. Cannot alter signed content. | Yes |
| **Creative host** | Origin that stores creatives on behalf of the advertiser — the advertiser's own server, or a host of its choosing. | Yes (may be the advertiser node) |
| **Auditor** | Independent verifier that samples receipts and creative-host logs. | Yes |
| **Settlement provider** | Moves money according to reconciled receipts (bank, payment processor, stablecoin service). | Out of protocol scope; integrates via profile |
| **End user** | The person who sees or hears the ad. | Never required to run anything |

A single organization may play multiple roles (e.g., a publisher that runs its own selling node). The protocol requires that each **role** be declared in the node descriptor so counterparties know whom they are dealing with — a direct analogue of `ads.txt`/`sellers.json`, but signed and machine-verifiable.

---

## 4. Architecture: Federated Hybrid Nodes

### 4.1 Models Considered

| Model | Summary | Strengths | Weaknesses |
|-------|---------|-----------|------------|
| **A. Hybrid federated nodes** *(chosen)* | Independent nodes discover each other and exchange signed messages over HTTPS; optional relays; optional legacy bridge. | Decentralizes power; low latency; no blockchain dependency; familiar web primitives; works for any surface. | Requires reputation/trust mechanisms; settlement must be reconciled off-protocol. |
| **B. Network-of-networks** | Only existing ad networks/exchanges federate via a common protocol. | Fastest adoption among incumbents. | Power stays with intermediaries; small publishers and advertisers remain dependent. |
| **C. Fully P2P / on-chain** | Matching and settlement on a public ledger with smart contracts. | Maximal transparency and programmable settlement. | Latency and cost per event; regulatory burden; volatile assets; agency reluctance; public ledgers leak commercial data. |

**Decision:** OpenAds adopts **Model A**. Model B is supported as a *subset* (a network can simply run an OpenAds node). Model C is supported as a *settlement profile* (§9), not as the core transport.

### 4.2 Topology

```
                         ┌───────────────────────┐
                         │  Exchange/Relay Node  │  (optional)
                         └──────────┬────────────┘
                                    │ signed, unaltered
     ┌──────────────────┐           │            ┌──────────────────┐
     │  Advertiser /    │◀──────────┼───────────▶│  Publisher /     │
     │  Buying Node     │   direct or relayed    │  Selling Node    │
     └────────┬─────────┘                        └────────┬─────────┘
              │ owns                                       │ renders on
     ┌────────▼─────────┐  licensed fetch (TTL)   ┌────────▼─────────┐
     │  Creative Host   │────────────────────────▶│  Surface: web,   │
     │  (advertiser-    │                         │  feed, email,    │
     │   controlled)    │◀── revocation ──────────│  audio, AI chat  │
     └──────────────────┘   (push + pull)         └────────┬─────────┘
                                                           │
              ◀──────────── signed delivery receipts ──────┘
                                    │
                         ┌──────────▼────────────┐
                         │  Auditor (sampling)   │
                         └───────────────────────┘
                                    │ reconciled totals
                         ┌──────────▼────────────┐
                         │ Settlement Profile    │  (fiat, stablecoin, …)
                         └───────────────────────┘

     Legacy DSPs ──OpenRTB──▶ [ OpenRTB Bridge Node ] ──OpenAds──▶ federation
```

### 4.3 Lifecycle in Brief

1. **Discover.** Nodes find each other via WebFinger and fetch each other's signed **Node Descriptor**, which declares roles, endpoints, public keys, accepted policies, and supported profiles.
2. **Publish policy.** Each side publishes a machine-readable **Policy**: what a publisher accepts (categories, formats, floor prices); what an advertiser requires (brand-safety exclusions, geographies, surfaces).
3. **Offer.** A buying node sends a signed **Offer** (a campaign line: price, budget, schedule, targeting constraints, creative references) to selling nodes — directly, or broadcast through relays.
4. **Accept.** A selling node evaluates the offer against its policy and replies with a signed **Acceptance** (or a counter-offer/decline). The pair now constitutes a **Deal**.
5. **Fetch under licence.** The selling node fetches the **Creative Manifest** from the creative host. The manifest is signed and carries a **licence** with an expiry (TTL).
6. **Serve.** At render time the selling node selects among active Deals using context (§6) and renders the creative with a "why this ad" disclosure.
7. **Receipt.** Each impression, view, or click produces an entry in a signed, batched **Receipt** sent to the buying node.
8. **Revoke (any time).** The advertiser publishes a signed **Revocation**; nodes must stop serving within the SLA (§5).
9. **Reconcile and settle.** Buying and selling nodes reconcile receipts (optionally with an auditor) and settle via an agreed **Settlement Profile**.

### 4.4 Real-Time vs. Pre-Negotiated

OpenAds deliberately favors **pre-negotiated deals evaluated locally at render time** over per-impression real-time auctions across the network. This keeps user context on the publisher's node (no bid stream broadcasting user data to dozens of parties), reduces latency, and makes the system implementable by small operators. A selling node *may* run an internal auction among its active deals. Real-time bidding across nodes is available only as an optional profile, and it carries strict data-minimization rules (§13.9).

---

## 5. Creative Ownership and Revocation

### 5.1 Principle

An advertiser grants a **licence to display**, not a copy. The licence is bounded in time, scope (which nodes and surfaces), and purpose, and it can be withdrawn.

### 5.2 Tiered Model

| Tier | Mechanism | Revocation latency | Use when |
|------|-----------|-------------------|----------|
| **Tier 1 — Pointer (default)** | The Creative Manifest points at assets on the advertiser-controlled creative host. Selling nodes fetch assets on demand or keep them for at most a short licence TTL (default **15 minutes**). Revoked assets return `410 Gone`. | ≤ licence TTL (default ≤ 15 min), typically seconds when push revocation is used | Default for all creatives |
| **Tier 2 — Signed cache** | Selling nodes may cache assets locally for performance (e.g., podcasts, email, and offline apps) under a signed licence with a longer TTL (max **24 hours**), and must subscribe to revocation. | ≤ 60 s after a push revocation is received; ≤ TTL in the worst case | High-volume, latency-sensitive, or offline-delivered formats |

**Why proxy the fetch rather than having browsers hit the advertiser directly?** If end-user devices fetched creatives straight from the advertiser's host, the advertiser would learn every viewer's IP address — a tracking channel. OpenAds therefore requires the **selling node** (or an Oblivious HTTP relay) to fetch assets, so the advertiser keeps control without gaining surveillance. The creative host's fetch logs still give the advertiser an *independent, node-level* signal for audit (§8).

### 5.3 Revocation Mechanics

- **Push:** The advertiser (or its creative host) sends a signed `Revocation` to every node holding an active licence for that creative. Relays must forward revocations unaltered and with priority.
- **Pull:** Every creative host exposes a signed revocation feed; nodes must poll it at least once per licence TTL. This covers missed pushes.
- **Effect:** After revocation, any further impression of that creative is **non-billable** and constitutes a protocol violation, detectable from receipts (timestamps after the revocation) and from creative-host logs (fetches after the revocation).
- **Reasons (optional, structured):** `legal`, `recall`, `pricing_error`, `rights_expired`, `brand_safety`, `campaign_ended`, `other`.
- **Edits are revocations plus re-issues:** a modified creative gets a new content hash and manifest version, so a stale version can never be mistaken for the current one.

### 5.4 Honest Limits

No protocol can force a malicious party to delete bytes it has already received. OpenAds instead makes misuse **unprofitable and detectable**: an expired or revoked licence makes impressions non-billable; signatures make violations provable; and node reputation (§14) makes repeat offenders easy to exclude. Screenshots, archives, and lawful retention obligations (e.g., political ad libraries) are out of scope for revocation and are addressed in policy profiles.

---

## 6. Audience Matching: Options Compared

| Approach | How it works | Privacy | Relevance | Implementation burden | Regulatory exposure |
|----------|-------------|---------|-----------|----------------------|---------------------|
| **Contextual** | Match on page/post/episode/conversation topic, publisher category, coarse geography (country/region), language, time, device class. | Excellent: no personal data | Good, and improving with modern content classification | Low | Low |
| **On-device interest** | Interest signals are derived and stored on the user's device. The device selects among candidate ads locally; only aggregate, noised reports leave it. | Very good | Good–High | High (needs client support) | Low–Medium |
| **Contextual + opt-in profile** | Contextual by default; users may explicitly share a small set of interest categories with a publisher they trust. | Good (consent-based) | High for opted-in users | Medium | Medium (consent management) |
| **Cross-site identity (status quo)** | Persistent identifiers track users across sites. | Poor | High | Medium | High |

**Recommendation:** OpenAds v1 mandates **contextual matching as the baseline** that every conformant node supports. **On-device matching** is defined as an optional profile for clients that implement it. **Opt-in interest sharing** is allowed only first-party (user → publisher), never forwarded in raw form to buying nodes. **Cross-site identifiers are prohibited** in protocol messages.

Targeting expressions in Offers may therefore reference only context attributes (§13.6), coarse geography, and — through the optional profile — opaque on-device interest cohorts that never identify an individual.

---

## 7. Brand Safety and Content Policy: Options Compared

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **Bilateral policy** | Each advertiser publishes requirements; each publisher publishes what it accepts; a Deal forms only where both match. | Maximum autonomy; no central arbiter; simple to reason about. | Without a shared vocabulary, policies don't compare cleanly; each pairing is bespoke. |
| **Shared taxonomy + local rules** | A common open content taxonomy (categories, sensitive topics, formats) plus node-local rules, like fediverse instance moderation. | Interoperable; machine-comparable; communities keep local norms. | Taxonomy governance becomes political; risk of over-blocking legitimate news and minority voices. |
| **Central certification** | An authority certifies publishers and advertisers. | Simple trust signal for buyers. | Recentralizes power; gatekeeping; contradicts P1. |

**Recommendation — combine the first two:** OpenAds defines a **shared, versioned, open taxonomy as vocabulary** (initially mapped to the IAB Tech Lab Content and Ad Product Taxonomies for compatibility) and **bilateral enforcement**: policies are expressed in that vocabulary and evaluated mechanically by both sides. No central certifier is required, though independent third parties *may* publish signed attestations (e.g., "this publisher passed our audit") that nodes can choose to trust. The taxonomy explicitly separates **"sensitive" from "unsafe"** so that news, health, and LGBTQ+ content are not blocked by default — a known failure of keyword blocklists.

Regulated categories (political, alcohol, gambling, pharmaceuticals, financial products, and ads to minors) require **policy profiles** that carry jurisdiction-specific rules and disclosure obligations, including transparency-library requirements for political advertising.

---

## 8. Measurement and Proof of Delivery

### 8.1 Signed Receipts

Every billable event creates a receipt entry, and entries are batched and signed by the selling node:

- **Event types:** `impression` (rendered), `viewable` (met a viewability rule from the Deal), `click`, `listen` (audio: the ad segment was played), `open` (email; reported as best effort and labeled as such), `engagement` (surface-specific, such as a boost or reply on a sponsored post).
- **Batching:** entries are grouped per deal per time window and committed with a **Merkle root**, so a buying node or auditor can request proof of inclusion for sampled entries without receiving every log line.
- **Content:** deal ID, creative content hash, timestamp, surface, coarse context, and event type. **No user identifiers.**

### 8.2 Corroboration Layers

| Layer | Signal | Who verifies |
|-------|--------|--------------|
| L0 | Selling-node-signed receipts | Buying node |
| L1 | Creative-host fetch logs (node-level fetch counts consistent with claimed volume under the licence TTL) | Advertiser |
| L2 | **Client attestation (optional):** privacy-preserving, unlinkable tokens (e.g., IETF Privacy Pass) showing that a real client rendered the ad, without identifying it | Buying node / auditor |
| L3 | Independent auditor sampling with Merkle proofs and spot checks | Auditor |

A Deal declares which layers are required. Small direct deals may rely on L0+L1; large network deals may require L2+L3.

### 8.3 Attribution and Conversions

Conversion measurement is optional and must be **aggregate and privacy-preserving**. OpenAds does not define its own attribution system. Instead it will adopt the output of the W3C Private Advertising Technology work (for example, privacy-preserving attribution APIs that use aggregation and differential privacy) as an optional profile. Click-through with a non-identifying campaign parameter (UTM-style) is allowed. Per-user conversion pixels are not.

### 8.4 Disputes

When receipts and corroboration diverge beyond a Deal's tolerance (default 10%), either party may open a signed `Dispute` message referencing the batch. v0.1 defines the message format only; the resolution process (bilateral, arbitration by a named auditor, or an escalation path) is an open question (§17).

---

## 9. Settlement: Rail-Agnostic Payments

The protocol proves *what is owed*; **Settlement Profiles** define *how it is paid*.

1. Each Deal names one or more acceptable settlement profiles.
2. At period end, both nodes compute totals from reconciled receipts and exchange a signed `Statement`.
3. Once both sides countersign the statement, it is the authoritative invoice.
4. Payment occurs through the agreed profile. A signed `PaymentNotice` references the statement.

| Profile | Description | Notes |
|---------|-------------|-------|
| `settle:invoice` | Traditional invoicing; bank transfer or card through any processor | Default; works everywhere |
| `settle:processor` | Direct payout via payment-processor APIs (marketplace or connect-style accounts) | Good for self-serve small advertisers |
| `settle:prepaid` | Advertiser pre-funds an escrow balance at the selling node; it draws down per statement | Reduces credit risk for small publishers |
| `settle:stablecoin` | Settlement in a regulated stablecoin, with the countersigned statement hash recorded on-chain | Optional; for parties that want programmable or instant payouts |
| `settle:micropay` | Streaming or micro-settlement (e.g., Web Monetization-style) | Experimental |

Intermediary fees are **declared in the signed Deal** (e.g., "relay fee 5%"), so every party can see exactly how a dollar is split. This structurally addresses the "unknown delta" described in §1.2.

---

## 10. End-User Rights

Every conformant selling node and surface must provide:

| Right | Requirement |
|-------|-------------|
| **Why this ad** | Every ad carries a machine-readable and human-readable disclosure: advertiser identity (verified), the paying entity, why it was shown (e.g., "matched to: article topic *cycling*; region: *Kerala*"), the intermediaries involved, and a link to the advertiser's OpenAds profile. |
| **Global opt-out** | Nodes must honor the **Global Privacy Control (GPC)** signal and an OpenAds-specific `Sec-OpenAds-Pref` preference (e.g., `contextual-only`, `no-ads-where-possible`). Opt-outs apply to every profile beyond contextual. |
| **Ad-free payment** | Selling nodes may advertise an **ad-free offer** (subscription, one-time payment, or micropayment) through a standard `adfree` endpoint in the Node Descriptor, so clients can show a consistent "remove ads" option. |
| **Report / block** | Users can report an ad (misleading, offensive, scam, or sensitive) or block an advertiser. Reports are sent as signed `Report` messages to the selling node, and forwarded in aggregate to the buying node and advertiser. Block preferences are stored client-side or first-party and are never shared as a cross-site identity. |

---

## 11. Surfaces in Scope for v1

| Surface | Profile | Key considerations |
|---------|---------|--------------------|
| **Web display and native** | `surface:web` | Standard sizes plus responsive native assets (title, body, image, CTA); a sandboxed iframe or server-side render; no third-party script execution in the creative by default (HTML5 creatives must run sandboxed and without network access except to the licensed host via the node). |
| **Fediverse and social posts** | `surface:social` | Sponsored posts are rendered as distinct objects (an ActivityPub `Note` with an OpenAds `sponsored` extension, or an AT Protocol record with an equivalent label). Instance admins choose whether to participate; user clients must label the post visibly; sponsored posts never federate as organic posts. |
| **Newsletters** | `surface:email` | Creatives are rendered at send time under a Tier 2 licence; open tracking is best effort and labeled; click receipts go through the selling node's redirect, which carries no personal parameters. |
| **Podcasts and audio** | `surface:audio` | Dynamic ad insertion by the hosting node; `listen` receipts based on segment delivery; host-read ads represented as a creative script plus approval workflow. |
| **AI and chat surfaces** | `surface:ai` | See §11.1. |

### 11.1 AI and Chat Surfaces: Additional Rules

AI assistants and agents are a new and sensitive ad surface, because users may not be able to tell persuasion from answers.

1. **Separation:** Sponsored content must be shown as a **distinct unit**, visually and semantically separate from the generated answer. Paid influence on the content of the organic answer is prohibited.
2. **Labeling:** Every sponsored unit carries a persistent "Sponsored" label and a why-this-ad disclosure.
3. **Context handling:** Matching may use the topic of the current conversation, derived in-session on the publisher's (AI provider's) node. Conversation content must not be sent to buying nodes, and must not be retained for ad purposes beyond the session unless the user opts in.
4. **Agentic actions:** An AI agent acting for a user must not select a sponsored option over a better organic one without disclosing it. Agent purchases influenced by sponsorship must be flagged to the user.
5. **Sensitive contexts:** Conversations classified as health, crisis, minors, or legal/financial distress are ineligible for ads by default.

---

## 12. Relationship to Existing Standards: Options Compared

| Option | Pros | Cons |
|--------|------|------|
| **Bridge-first (extend ActivityPub, OpenRTB, etc.)** | Existing buyers can participate on day one; fediverse servers adopt it cheaply; standards bodies and regulators see continuity; mature libraries. | Inherits quirks: ActivityPub's loose typing and OpenRTB's bid-stream data leakage. Ownership and revocation would be bolted on. |
| **Clean-slate** | Designed for ownership, revocation, receipts, and privacy from the start; a smaller, more consistent spec. | No liquidity at launch; agencies are skeptical; no existing tooling. |
| **Clean-slate core on existing primitives + bridges** *(recommended)* | A native design where it matters (offers, licences, revocation, receipts), proven building blocks everywhere else, and an on-ramp for existing demand. | The bridge needs careful privacy stripping; two code paths to maintain. |

**OpenAds reuses:**

| Standard | Use in OpenAds |
|----------|----------------|
| HTTPS / HTTP Semantics (RFC 9110) | Transport |
| **HTTP Message Signatures (RFC 9421)** | Authenticating every node-to-node message |
| **WebFinger (RFC 7033)** | Node discovery from a domain |
| JSON / JSON-LD 1.1 | Message encoding and extensible vocabulary |
| Ed25519 (RFC 8032) | Default signature algorithm |
| Oblivious HTTP (RFC 9458) | Optional relaying for privacy |
| Privacy Pass (RFC 9576–9578) | Optional client attestation |
| Global Privacy Control | User opt-out signal |
| ActivityPub / AT Protocol | Rendering sponsored posts on social surfaces |
| IAB Tech Lab taxonomies, `ads.txt`, `sellers.json` | Vocabulary mapping and authorized-seller compatibility |
| OpenRTB 2.6 / 3.0 | Bridge profile only |

**The OpenRTB bridge** translates bid requests from existing DSPs into OpenAds offers and the reverse. It **strips** user IDs, device IDs, precise geolocation, and other personal fields, and passes only OpenAds-permitted context. DSPs that need personal data simply cannot buy through the bridge — and that is intentional.

---

## 13. Draft Protocol Specification v0.1

> **Status:** Draft. Non-normative examples. The key words MUST, SHOULD, and MAY are used as in RFC 2119 and are subject to change.

### 13.1 Conventions

- All messages are JSON objects with `"@context": "https://openads.org/ns/v0"` (namespace placeholder pending domain acquisition).
- All node-to-node HTTP requests MUST be signed with HTTP Message Signatures (RFC 9421), covering `@method`, `@target-uri`, `content-digest`, and `date`.
- Persisted artifacts (manifests, offers, receipts, revocations) MUST also carry an embedded detached signature (`proof`) so they remain verifiable after transport.
- Timestamps use RFC 3339 UTC. Money is expressed as `{ "amount": "12.50", "currency": "USD" }`, with the amount as a decimal string.
- Identifiers are URIs. Nodes are identified by `https://` URLs; objects by `urn:openads:<type>:<uuid>`.

### 13.2 Discovery

A node for `example.com` is discovered via WebFinger:

```
GET https://example.com/.well-known/webfinger?resource=acct:ads@example.com
```

```json
{
  "subject": "acct:ads@example.com",
  "links": [
    {
      "rel": "https://openads.org/ns/node",
      "type": "application/openads+json",
      "href": "https://ads.example.com/node"
    }
  ]
}
```

Publishers without their own node declare a delegate in `/.well-known/openads.json`, which is the signed successor to `ads.txt`:

```json
{
  "@context": "https://openads.org/ns/v0",
  "domain": "example.com",
  "authorizedSellers": [
    { "node": "https://coop.indie-sites.net/node", "relationship": "reseller" }
  ]
}
```

### 13.3 Node Descriptor

```json
{
  "@context": "https://openads.org/ns/v0",
  "type": "Node",
  "id": "https://ads.example.com/node",
  "name": "Example News Selling Node",
  "roles": ["publisher", "selling"],
  "operator": { "name": "Example Media Ltd", "jurisdiction": "IN", "contact": "mailto:ads@example.com" },
  "publicKeys": [
    { "id": "https://ads.example.com/node#key-2026", "type": "Ed25519", "publicKeyMultibase": "z6Mk..." }
  ],
  "endpoints": {
    "offers": "https://ads.example.com/oa/offers",
    "receipts": "https://ads.example.com/oa/receipts",
    "revocations": "https://ads.example.com/oa/revocations",
    "reports": "https://ads.example.com/oa/reports",
    "adfree": "https://example.com/subscribe"
  },
  "surfaces": ["surface:web", "surface:email"],
  "policy": "https://ads.example.com/oa/policy",
  "settlement": ["settle:invoice", "settle:prepaid"],
  "conformance": "openads-core-0.1"
}
```

### 13.4 Policy

```json
{
  "@context": "https://openads.org/ns/v0",
  "type": "Policy",
  "id": "https://ads.example.com/oa/policy",
  "taxonomy": "openads-taxonomy-0.1",
  "accepts": {
    "adCategories": { "exclude": ["gambling", "tobacco", "political"] },
    "formats": ["native", "display:300x250", "display:728x90"],
    "floors": [{ "format": "native", "cpm": { "amount": "3.00", "currency": "USD" } }]
  },
  "contentCategories": ["news", "technology", "sports"],
  "sensitiveTopicsPresent": ["news:conflict"],
  "proof": { "type": "Ed25519Signature2026", "verificationMethod": "https://ads.example.com/node#key-2026", "proofValue": "z3F..." }
}
```

### 13.5 Creative Manifest (with Licence)

```json
{
  "@context": "https://openads.org/ns/v0",
  "type": "CreativeManifest",
  "id": "urn:openads:creative:6f1c2a9e-1b7d-4c55-9a0e-2f3b8d1e7c44",
  "version": 3,
  "advertiser": { "id": "https://ads.acme-bikes.com/node", "verifiedName": "Acme Bikes Pvt Ltd" },
  "format": "native",
  "assets": {
    "title": "Ride further on a single charge",
    "body": "The new Acme E-Tour: 120 km range.",
    "image": {
      "href": "https://creative.acme-bikes.com/a/etour-1200x628.webp",
      "contentHash": "sha256-9b74c9897bac770ffc029102a200c5de",
      "width": 1200, "height": 628
    },
    "cta": { "label": "See the E-Tour", "href": "https://acme-bikes.com/etour?oa=c6f1c" }
  },
  "adCategory": "automotive:bicycles",
  "licence": {
    "tier": "pointer",
    "issuedAt": "2026-10-04T10:00:00Z",
    "ttlSeconds": 900,
    "scope": { "nodes": ["https://ads.example.com/node"], "surfaces": ["surface:web"] },
    "revocationFeed": "https://creative.acme-bikes.com/oa/revocations"
  },
  "proof": { "type": "Ed25519Signature2026", "verificationMethod": "https://ads.acme-bikes.com/node#key-1", "proofValue": "z5K..." }
}
```

### 13.6 Offer

```json
{
  "@context": "https://openads.org/ns/v0",
  "type": "Offer",
  "id": "urn:openads:offer:0c8e5d3a-77f1-4a9b-8e21-5c4b6a1f9d02",
  "from": "https://ads.acme-bikes.com/node",
  "to": "https://ads.example.com/node",
  "creatives": ["urn:openads:creative:6f1c2a9e-1b7d-4c55-9a0e-2f3b8d1e7c44"],
  "pricing": { "model": "cpm", "price": { "amount": "4.20", "currency": "USD" } },
  "budget": { "amount": "1500.00", "currency": "USD" },
  "schedule": { "start": "2026-10-05T00:00:00Z", "end": "2026-10-31T23:59:59Z" },
  "targeting": {
    "context": { "contentCategories": ["technology", "sports:cycling"] },
    "geo": { "countries": ["IN"], "regions": ["IN-KL", "IN-KA"] },
    "languages": ["en", "ml"]
  },
  "brandSafety": { "excludeContent": ["news:conflict", "adult"] },
  "measurement": { "required": ["L0", "L1"], "viewability": "50pct-1s", "disputeTolerance": 0.10 },
  "fees": [],
  "settlement": ["settle:invoice"],
  "expires": "2026-10-04T23:59:59Z",
  "proof": { "...": "..." }
}
```

The selling node responds with `Acceptance`, `CounterOffer`, or `Decline`, each referencing `offer.id` and signed. An accepted offer becomes a **Deal**, identified as `urn:openads:deal:<uuid>`.

### 13.7 Receipt Batch

```json
{
  "@context": "https://openads.org/ns/v0",
  "type": "ReceiptBatch",
  "id": "urn:openads:receipts:a71b...",
  "deal": "urn:openads:deal:3d9e...",
  "issuer": "https://ads.example.com/node",
  "window": { "start": "2026-10-05T10:00:00Z", "end": "2026-10-05T11:00:00Z" },
  "totals": { "impression": 18240, "viewable": 12011, "click": 97 },
  "byCreative": [
    { "contentHash": "sha256-9b74c9897bac770ffc029102a200c5de", "impression": 18240 }
  ],
  "merkleRoot": "sha256-1f0e...",
  "attestation": { "type": "privacypass", "tokensRedeemed": 11702 },
  "proof": { "...": "..." }
}
```

Individual entries can be retrieved by an authorized counterparty or auditor via `GET {receipts}/{batchId}/proof?index=n`, which returns the entry and its Merkle inclusion path.

### 13.8 Revocation

```json
{
  "@context": "https://openads.org/ns/v0",
  "type": "Revocation",
  "id": "urn:openads:revocation:e2c4...",
  "creative": "urn:openads:creative:6f1c2a9e-1b7d-4c55-9a0e-2f3b8d1e7c44",
  "versions": "all",
  "effectiveAt": "2026-10-12T08:30:00Z",
  "reason": "pricing_error",
  "issuer": "https://ads.acme-bikes.com/node",
  "proof": { "...": "..." }
}
```

Receivers MUST respond `202 Accepted` and stop serving within the SLA for the licence tier. Relays MUST forward revocations within 10 seconds.

### 13.9 Other Message Types (v0.1 Summary)

| Message | Purpose |
|---------|---------|
| `Acceptance` / `CounterOffer` / `Decline` | Offer responses |
| `DealUpdate` / `DealPause` / `DealEnd` | Change budget, pause, or end a deal |
| `Statement` | Period totals for settlement; countersigned by both parties |
| `PaymentNotice` | Reference to an off-protocol payment made against a statement |
| `Dispute` | Flags a receipt or statement mismatch |
| `Report` | End-user report, forwarded in aggregate |
| `Attestation` | Third-party signed claim about a node (audit passed, verified advertiser, etc.) |
| `BidRequest` / `Bid` *(optional `rtb` profile)* | Real-time path, limited to context fields and coarse geography; no user or device identifiers |

### 13.10 Conformance Levels

| Level | Requirements |
|-------|-------------|
| **openads-core** | Discovery, Node Descriptor, Policy, Offer/Acceptance, Tier 1 licences, revocation (push and pull), L0 receipts, why-this-ad, GPC, Report |
| **openads-extended** | Core + Tier 2 cache, Merkle proofs, Statements, at least one settlement profile, the adfree endpoint |
| **openads-verified** | Extended + L2 client attestation + periodic independent audit attestation |

Each surface profile (`surface:web`, `surface:social`, `surface:email`, `surface:audio`, `surface:ai`) adds rendering and labeling requirements on top of these levels.

### 13.11 Versioning

The protocol uses semantic versioning. Nodes advertise supported versions in their Node Descriptor. Unknown fields MUST be ignored, and extensions MUST use namespaced JSON-LD terms.

---

## 14. Security and Threat Model

| Threat | Mitigation |
|--------|-----------|
| **Impression inflation by a selling node** | L1 creative-host corroboration, L2 client attestation, L3 sampled audits, and reputation. Fraud is provable because receipts are signed. |
| **Bots and invalid traffic** | Privacy Pass-style attestation; behavioral filtering on the selling node; standard invalid-traffic categories mapped to receipt flags. |
| **Domain spoofing / unauthorized resellers** | Signed `/.well-known/openads.json` and verified Node Descriptors; every message is bound to a key published at the claimed domain. |
| **Malvertising and malicious creatives** | Sandboxed rendering; no arbitrary third-party JavaScript; content-hash pinning; selling nodes may scan assets on fetch; Report flow. |
| **Creative tampering by intermediaries** | Signed manifests and content hashes; relays cannot alter signed payloads. |
| **Ignoring revocation** | Post-revocation impressions are non-billable and provable; reputation penalties; Attestation revocation. |
| **Data leakage via creative fetch** | Fetches are made by the selling node or through an OHTTP relay, never directly from the user's device. |
| **Sybil nodes** | Reputation through Attestations from parties a node already trusts; prepaid settlement for unknown counterparties; rate limits. |
| **Key compromise** | Key rotation via the Node Descriptor; signed key-revocation statements; short-lived signing subkeys. |
| **Regulatory misuse (illegal or discriminatory targeting)** | Contextual-only baseline; regulated-category policy profiles; prohibited targeting on protected characteristics. |

**Reputation** in v0.1 is deliberately simple: each node chooses which `Attestation` issuers to trust, much as fediverse instances choose whom to federate with. Shared blocklists and allowlists are published as signed documents. There is no global score.

---

## 15. Governance and Licensing

### 15.1 Recommended Path

| Phase | Trigger | Structure |
|-------|---------|-----------|
| **1. Community incubation** *(now)* | Publication of this whitepaper | Public GitHub organization; RFC process (proposal → discussion → editor's draft → last call); named editors; a public issue tracker; open meetings with published notes. |
| **2. Standards-track** | Two or three independent interoperable implementations | Transfer to a **W3C Community Group** (free and open to anyone) to gain neutral process and policy credibility; liaise with the IAB Tech Lab and the W3C Private Advertising Technology work. |
| **3. Neutral foundation** | Material commercial adoption, a need to hold trademarks or fund a test suite or audit accreditation | An independent non-profit foundation (or a project under an existing open-source foundation) with a multi-stakeholder board: publishers, advertisers, civil society, and implementers, **with no single company holding a majority.** |

### 15.2 Commitments From Day One

- **Open licensing:** spec text under CC BY 4.0; code under Apache-2.0; a royalty-free patent commitment required from contributors (modeled on the W3C Community Contributor License Agreement).
- **Neutrality:** no contributor organization may hold exclusive control of the namespace, the test suite, or the trademark.
- **Transparency:** all decisions are made in public with recorded rationale.
- **Stakeholder balance:** working groups must include publisher, advertiser, and user-advocacy voices.

### 15.3 Why Community-Led First

A foundation on day one adds cost and bureaucracy before there is anything to govern. Publishing the neutrality commitment and the transition triggers up front lets the project move fast while assuring advertisers, publishers, and regulators that it will not become one company's protocol.

---

## 16. Roadmap

| Milestone | Deliverables |
|-----------|-------------|
| **M0 — Whitepaper v0.1** | This document; public comment period |
| **M1 — Spec editor's draft v0.2** | Normative core spec, JSON Schemas, taxonomy v0.1, test vectors for signatures and Merkle proofs |
| **M2 — Reference implementation** | Open-source selling node, buying node, and creative host; a WordPress/Ghost plugin; a Mastodon/fediverse integration; a conformance test suite |
| **M3 — Pilot network** | 10–50 independent publishers (newsletters, fediverse instances, niche sites) and 5–10 advertisers running real campaigns through `settle:invoice` / `settle:prepaid` |
| **M4 — Bridges and surfaces** | OpenRTB bridge; audio (podcast) profile; AI/chat profile pilot with at least one assistant provider |
| **M5 — Standards-track** | W3C Community Group formed; v1.0 candidate |

---

## 17. Open Questions

1. **Name.** "Open Ads Standard" / "OpenAds" is the working name. Alternatives: *Adfed*, *Open Ad Protocol*, *Commons Ads*, *FedAds*. Avoid the "OAS" acronym, which clashes with the OpenAPI Specification.
2. **Funding.** Who funds the reference implementation, the test suite, and early editors, without compromising neutrality?
3. **Dispute resolution.** Bilateral, auditor arbitration, or a standing panel? What evidence is decisive?
4. **AI surfaces.** How should sponsored units in conversational interfaces and autonomous agents be labeled and constrained? Should agents be allowed to *act on* sponsored offers at all?
5. **Revocation vs. legal retention.** How does revocation interact with political-ad transparency libraries, archiving laws, and evidence preservation?
6. **On-device profile.** Which client platforms will implement it, and should OpenAds define its own or adopt an emerging browser API?
7. **Taxonomy governance.** Who maintains the shared taxonomy, and how are disputes about "sensitive" versus "unsafe" content resolved?
8. **Small-advertiser onboarding.** Can a local business run a campaign without operating any node, through a hosted buying node, without recentralizing the network?
9. **Pricing discovery.** Without network-wide real-time auctions, how do prices converge? Are public, anonymized price indices desirable?
10. **Measurement acceptance.** What do major agencies need before receipts plus corroboration are accepted in place of incumbent verification vendors?

Feedback on these questions is explicitly invited.

---

## 18. AI-Assistance Disclosure

This whitepaper was **authored with Claude**, an AI model developed by Anthropic.

- **Human direction:** A human contributor (Suneesh Rajan) initiated the project, defined the problem space, and made all key design decisions through a structured requirements interview. These included the federation model, tiered creative revocation, rail-agnostic settlement, signed-receipt measurement, end-user rights, v1 surfaces, governance approach, and authorship form.
- **AI contribution:** Claude proposed the alternatives and trade-offs for the human to decide between, structured the document, drafted the prose, the comparison tables, the architecture diagram, and the example protocol payloads, and recommended where the human asked for recommendations.
- **Accountability:** The human contributor and the OpenAds Initiative are responsible for the contents. Claude is credited as a contributor for transparency, not as a responsible party.
- **Verification:** Cited standards (RFCs, W3C specifications) and the third-party study cited in §1.2 should be independently verified by readers. Example payloads are illustrative and non-normative.

We disclose this because a proposed open standard should be open about how it was made.

---

## 19. Glossary

| Term | Definition |
|------|-----------|
| **Node** | A server that speaks the OpenAds protocol in one or more roles. |
| **Deal** | An accepted Offer: a signed agreement between a buying node and a selling node. |
| **Creative Manifest** | A signed description of a creative's assets, metadata, and licence. |
| **Licence** | The time-bounded, scope-bounded, revocable permission to display a creative. |
| **Revocation** | A signed instruction from the advertiser to stop displaying a creative. |
| **Receipt Batch** | A signed, Merkle-committed set of delivery events for a Deal and time window. |
| **Settlement Profile** | A pluggable specification for how amounts owed are paid. |
| **Surface Profile** | Rendering, labeling, and measurement rules for a specific medium. |
| **Relay** | An optional node that routes signed messages between other nodes without altering them. |
| **Bridge** | A node that translates between OpenAds and a legacy protocol such as OpenRTB. |

---

## 20. References

- ISBA & PwC, *Programmatic Supply Chain Transparency Study*, 2020.
- IETF RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels.
- IETF RFC 3339 — Date and Time on the Internet: Timestamps.
- IETF RFC 7033 — WebFinger.
- IETF RFC 8032 — Edwards-Curve Digital Signature Algorithm (EdDSA).
- IETF RFC 9110 — HTTP Semantics.
- IETF RFC 9421 — HTTP Message Signatures.
- IETF RFC 9458 — Oblivious HTTP.
- IETF RFC 9576, 9577, 9578 — Privacy Pass architecture, HTTP authentication scheme, and issuance protocols.
- W3C — ActivityPub (Recommendation, 2018).
- W3C — JSON-LD 1.1 (Recommendation, 2020).
- W3C — Private Advertising Technology Community Group / Working Group materials.
- Global Privacy Control specification.
- AT Protocol specification (Bluesky).
- IAB Tech Lab — OpenRTB 2.6 / 3.0, ads.txt, sellers.json, Content Taxonomy, Ad Product Taxonomy.

---

*The Open Ads Standard — Whitepaper v0.1 — The OpenAds Initiative — Authored with Claude (Anthropic). Comments welcome.*
