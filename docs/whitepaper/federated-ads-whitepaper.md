# The Federated Ads Protocol

### An open, federated, owner-controlled protocol for advertising on the open web

**Whitepaper · Version 0.3 · Draft for public comment · 5 October 2026**

| | |
|---|---|
| **Short name** | Federated Ads (identifier: `federated-ads`) |
| **Published by** | The Federated Ads Initiative (see [§23](#23-governance-ipr-and-funding) for what this is today) |
| **Contributors** | Suneesh Rajan; Arjun Krishna; Claude (Anthropic) |
| **Contact** | Suneesh Rajan · suneeshtr@gmail.com |
| **Repository and issues** | https://github.com/federated-ads/spec |
| **Namespace (provisional)** | `https://w3id.org/federated-ads/v0` |
| **Licence** | Text: CC BY 4.0. Reference code: Apache-2.0. Contributor patent commitment: see [§23.4](#234-intellectual-property) |
| **Status** | Discussion document. Not a standard, and not endorsed by any standards body. The normative protocol text is maintained separately as an Internet-Draft (`draft-rajan-federated-ads-protocol`). |

> **Authored with Claude.** This whitepaper was researched, structured and drafted with Claude, an AI model made by Anthropic, under the direction of a human contributor who set its goals, made every design decision, and is accountable for its contents. Research findings were gathered with AI-assisted web research and should be independently checked; items resting on secondary sources are flagged. See [§28](#28-ai-assistance-disclosure).

> **Naming note.** This project is unrelated to The Trade Desk's "OpenAds" header-bidding wrapper (announced October 2025), to the blockchain project "Open Ads Protocol", and to the historical "Openads" ad server (later OpenX/Revive). Version 0.1 of this paper used the working name "OpenAds"; it was renamed to avoid confusion.

---

## Executive summary

**The problem.** Digital advertising pays for much of the open internet, but the system that delivers it is concentrated, opaque and built on tracking people.

- The ten largest US ad sellers now take **84.1%** of US internet ad revenue, up from 78.6% in 2021 [5].
- Outside China, Alphabet, Meta and Amazon take **57.6%** of all advertising revenue [6].
- A US federal court and the European Commission have both found that Google abused its position in ad tech [7][8].
- Even after years of reform, the ANA's benchmark finds that a large share of programmatic spend still fails to become effective, viewable, valid impressions [4].
- About **1.1 billion people**, roughly 30% of internet users, block ads [11].

Meanwhile, the publishers who most need a fair way to earn have no neutral, interoperable option. That includes independent sites, newsletters, podcasts, fediverse communities and now AI assistants.

**The proposal.** The Federated Ads Protocol ("Federated Ads") is an open protocol, in the tradition of email and ActivityPub, that lets independent servers ("nodes") run by publishers, advertisers, agencies or cooperatives:

1. **find each other** by domain;
2. **agree deals** with signed offers;
3. **serve creatives the advertiser still owns and can withdraw at any time**, under a time-limited licence;
4. **prove delivery** with signed, aggregated receipts recorded in tamper-evident logs;
5. **settle payment** on whatever payment rail the parties choose.

Matching is **contextual by default**, so the protocol carries no cross-site identifiers. People who see ads get enforceable rights: an explanation, an opt-out, an ad-free option and a way to report abuse. One protocol covers websites, fediverse and social feeds, newsletters, podcasts and AI/chat surfaces.

**What is new.** Most pieces exist separately: domain-bound signing (DKIM, ads.cert), contextual networks (EthicalAds, Carbon), on-device matching (Brave), transparency logs (Certificate Transparency). Federated Ads combines them into one open, federated protocol with three properties that, as far as our search found, no current system offers together ([§2](#2-what-has-been-tried-lessons-from-prior-art)):

- the advertiser keeps ownership of its creative and can revoke it;
- delivery is verifiable without surveillance;
- the parties choose their own intermediaries.

**What this paper is honest about.** Federated Ads will not offer cross-publisher reach-and-frequency planning, and that is by design. Its verification is weaker than incumbent verification vendors for anonymous, high-value deals until independent auditors and client attestation mature. It also faces a hard cold-start problem. [§20](#20-economics-a-worked-example), [§22](#22-adoption-strategy) and [§25](#25-risks-and-mitigations) address these directly.

**What we are asking for.** Review and criticism from standards bodies (W3C, IETF, IAB Tech Lab), from publishers and advertisers, and from civil society. Specifically:
- Is the problem framed correctly?
- Are the trade-offs acceptable?
- Would you implement, pilot or govern this?

---

## Contents

**Part I: Why**
1. [The problem](#1-the-problem)
2. [What has been tried: lessons from prior art](#2-what-has-been-tried-lessons-from-prior-art)

**Part II: What**
3. [Vision, principles, goals and non-goals](#3-vision-principles-goals-and-non-goals)
4. [Actors and roles](#4-actors-and-roles)
5. [Architecture](#5-architecture)
6. [Market design: how buying and selling works](#6-market-design-how-buying-and-selling-works)
7. [Creative ownership, licensing and revocation](#7-creative-ownership-licensing-and-revocation)
8. [Audience matching: options compared](#8-audience-matching-options-compared)
9. [Brand safety and content policy: options compared](#9-brand-safety-and-content-policy-options-compared)
10. [Measurement and verification](#10-measurement-and-verification)
11. [Settlement](#11-settlement)
12. [End-user rights](#12-end-user-rights)
13. [Surfaces](#13-surfaces)
14. [Interoperability with existing standards](#14-interoperability-with-existing-standards)

**Part III: How**
15. [Protocol overview](#15-protocol-overview)
16. [End-to-end worked example](#16-end-to-end-worked-example)
17. [Security considerations](#17-security-considerations)
18. [Privacy considerations](#18-privacy-considerations)
19. [Legal and regulatory considerations](#19-legal-and-regulatory-considerations)

**Part IV: Making it real**
20. [Economics: a worked example](#20-economics-a-worked-example)
21. [Comparison with existing systems](#21-comparison-with-existing-systems)
22. [Adoption strategy](#22-adoption-strategy)
23. [Governance, IPR and funding](#23-governance-ipr-and-funding)
24. [Roadmap and success metrics](#24-roadmap-and-success-metrics)
25. [Risks and mitigations](#25-risks-and-mitigations)
26. [Open questions](#26-open-questions)
27. [Frequently asked questions](#27-frequently-asked-questions)
28. [AI-assistance disclosure](#28-ai-assistance-disclosure)

**Appendices:** [A. Glossary](#appendix-a-glossary) · [B. References](#appendix-b-references) · [C. Change history](#appendix-c-change-history)

---

# Part I: Why

## 1. The problem

### 1.1 Concentration

Advertising revenue is consolidating into fewer hands.

**US market share.** The IAB/PwC *Internet Advertising Revenue Report* for 2025 puts US internet ad revenue at **$294.6 billion**. The top ten companies hold **84.1%**, up from 78.6% in 2021. Companies ranked 11–25 hold 8.3%, and everyone else shares the remaining 7.5% [5].

**Global share.** WPP Media's mid-2026 forecast estimates global advertising revenue of about $1.3 trillion in 2026, with Alphabet, Meta and Amazon taking **57.6%** of the market outside China [6].

**Conflicts of interest.** The concentration problem goes beyond market share. The same firm often represents buyers, represents sellers and runs the exchange between them. Authorities in three jurisdictions have acted on this:

- **United States.** In *United States v. Google* (E.D. Va.), the court found on **17 April 2025** that Google had illegally monopolised the publisher ad server and ad exchange markets and unlawfully tied them together. In September 2026 the court rejected divestiture of Google's AdX exchange. It instead ordered behavioural remedies, including interoperability with the open-source Prebid header-bidding framework and a ban on "first look"/"last look" advantages, overseen by a monitor [7]. Google has said it will appeal.
- **European Union.** On **5 September 2025** the European Commission fined Google **€2.95 billion** for self-preferencing its ad exchange since 2014 and signalled that a structural remedy might be needed [8].
- **Canada.** The Competition Bureau filed for divestiture of Google's publisher ad server and exchange in November 2024 [9].

Regulators broadly agree on the diagnosis: conflicted intermediaries control the rails. They differ on the cure. The US remedy notably requires **interoperability with an open, multi-party framework**, which is the kind of remedy an open protocol makes possible.

### 1.2 Opacity and leakage

**ISBA/PwC studies.** In 2020 the ISBA/PwC *Programmatic Supply Chain Transparency Study* found that only **51%** of advertiser spend reached publishers. **15%** was an "unknown delta" that could not be attributed to anyone [1].

The 2023 follow-up found real improvement where participants shared log-level data and used private deals [2]:
- publishers received **65%** (against a restated 57% for the earlier study);
- the unknown delta fell to **3%**.

**ANA study.** The ANA's 2023 *Programmatic Media Supply Chain Transparency Study* covered $123 million of spend and 35.5 billion impressions [3]. It found that:
- only about **36 cents** of each dollar entering a demand-side platform reached consumers as an effective impression;
- made-for-advertising sites took **15%** of spend;
- an average campaign ran on **44,000** websites.

**ANA/TAG TrustNet benchmark.** The quarterly benchmark shows the industry improving [4]:
- Q4 2025: "TrueAdSpend" of 56.7% for top performers and 37.5% for laggards.
- Over **92%** of median web and mobile programmatic spend now flows through private marketplaces.

**What this tells us.** Verifiable records work: transparency rose sharply wherever log-level data and deal identifiers were available. But the industry's fix has largely been to retreat into private deals between large parties. Those deals are walled gardens by another name, and they are not open to the long tail of publishers. Federated Ads aims to make verifiable, deal-based buying a **property of the protocol**, available to anyone.

### 1.3 Fraud

Estimates of ad fraud vary widely by method. Juniper Research's model put fraud at about **$84 billion in 2023**, 22% of online ad spend [12]. That is a modelled upper-bound estimate. Verification vendors report much lower invalid-traffic rates on the inventory they measure. Either way, fraud thrives where delivery cannot be verified and identities cannot be authenticated, and both are design targets for Federated Ads.

### 1.4 Surveillance as infrastructure, and the collapse of its replacement

Mainstream targeting was built on cross-site identifiers, and that model has run into trouble on several fronts:

- **Browsers.** Safari and Firefox block third-party cookies by default.
- **Regulators.** GDPR, the ePrivacy Directive, the EU Digital Services and Digital Markets Acts, US state privacy laws and India's Digital Personal Data Protection Act all restrict it ([§19](#19-legal-and-regulatory-considerations)).
- **Privacy Sandbox.** Google's proposed replacement was abandoned. In July 2024 Google dropped its plan to remove third-party cookies from Chrome. On **17 October 2025** it retired most Privacy Sandbox APIs, including Topics, Protected Audience and Attribution Reporting, citing low adoption [10].
- **The result:** after six years of industry engineering effort on APIs controlled by one vendor, Chrome still has third-party cookies, and no privacy-preserving replacement is widely deployed.

The surviving multi-vendor effort is the W3C Private Advertising Technology Working Group's *Attribution* specification, which is still a Working Draft [24].

Civil society and policy researchers have called for alternatives to surveillance-based advertising for years. The Norwegian Consumer Council and Accountable Tech called for a ban [57][87], and a 2022 US bill proposed one [88]. EFF argued for putting privacy first [60], and the Panoptykon Foundation set out requirements for a privacy-friendly ad system built on publisher collaboration [56], which this paper closely follows. A European Parliament study examined the policy options [59]. What none of them could point to was an open, interoperable protocol that implements the alternative.

### 1.5 Loss of creative control

Once a creative enters the supply chain, it is copied into ad servers, exchanges, caches and CDNs that the advertiser does not control. Advertisers have many reasons to pull a creative quickly:
- a legal problem;
- a product recall;
- a pricing error;
- expired rights to talent or music;
- a brand crisis.

In today's supply chain, pulling a creative is slow and incomplete. No interoperable "stop" signal exists, and nothing proves that it was honoured.

### 1.6 The unmonetised open web

The ecosystems with the strongest values-based objections to surveillance advertising are also the ones with no workable alternative:

- **Fediverse and decentralised social.** Mastodon promises it "will never serve ads" [16]. Bluesky's CEO has said the company "can't enshittify the network with ads", but has not ruled out "user intent-driven" advertising [17].
- **Newsletters and podcasts.** These are funded mostly by **direct-sold sponsorships**, which are growing but manual and unverifiable. US podcast advertising reached **$2.86 billion in 2025** [15].
- **Open-source and developer sites.** Small contextual networks have shown that tracking-free advertising can pay. EthicalAds paid publishers about **$117,000 in Q2 2026** across about 200 sites [19]. These networks are small, centralised and not interoperable.
- **AI assistants.** These are becoming an ad surface faster than norms can form:
  - OpenAI began testing ads in ChatGPT in February 2026 under self-declared principles: answers not influenced by ads, ads clearly labelled, conversations kept private from advertisers [13]. By August 2026 it reported a $1 billion annualised run rate [90].
  - Perplexity, by contrast, stopped its sponsored follow-up questions in early 2026, citing user trust [14].
  - No AI provider's ad principles are independently verifiable.

### 1.7 Ad blocking as a verdict

The eyeo *2026 Ad Blocking Report* estimates about **1.1 billion** ad-blocking users, roughly 30% of internet users, with mobile blocking up 27% since 2023. **81%** of respondents worry about how their data is used [11]. A large minority of the audience has opted out of today's advertising model altogether. Advertising that is non-tracking, accountable and clearly labelled is a credible way to win part of that audience back.

### 1.8 What is missing

There is no open, federated protocol for advertising, comparable to SMTP for email or ActivityPub for social posting. Such a protocol would let any party:
- run a node;
- transact directly or through intermediaries it chooses;
- keep ownership of what it contributes;
- verify what happened;
- do all of this without tracking the people who see the ads.

---

## 2. What has been tried: lessons from prior art

Federated Ads builds on, and has learned from, many earlier efforts. The table summarises what each did and what Federated Ads takes from it.

| Effort | What it did | What happened | Lesson for Federated Ads |
|---|---|---|---|
| **ads.txt / sellers.json / SupplyChain object** (IAB Tech Lab) | Plain-text and JSON files on the domain declaring authorised sellers | ads.txt: near-universal; sellers.json and SupplyChain object: widespread but uneven | Domain-hosted declarations spread when they cost almost nothing. Federated Ads keeps that pattern and adds signatures. |
| **ads.cert 1.0 and 2.0** (IAB Tech Lab) | Signed bid requests; v2 binds keys to domains via DNS ("Call Signs") and signs server-to-server requests [20] | v1 was tied to OpenRTB 3.0 and stalled. v2's reference implementation stopped at MVP. No buyer required it. | The closest precedent. Signing cost was never the problem. Ship production-grade libraries and key management, and get major participants to *require* signatures. |
| **OpenRTB 3.0 / AdCOM** | A clean-slate redesign of real-time bidding | Not backward compatible; adoption stayed minimal; useful parts moved back into 2.x [21] | Breaking compatibility loses to incremental change. Provide bridges and a phased path. |
| **Privacy Sandbox** (Google) | Browser APIs for interest-based ads and measurement without third-party cookies | Most APIs retired in October 2025 [10] | A "standard" controlled by one vendor with conflicting interests can be cancelled unilaterally. Require multi-stakeholder governance and independent implementations. |
| **Prebid.org** | Neutral open-source header bidding with a multi-company board | Widely adopted. A unilateral 2025 change to transaction IDs prompted a public dispute with IAB Tech Lab and a fork by The Trade Desk [22][23] | Neutral bodies work, but change control, notice periods and representation must be written down. |
| **Do Not Track** | A browser header asking sites not to track | The W3C group closed in 2019 for insufficient deployment; "tracking" was never defined; no legal force [26] | Vague signals fail. |
| **Global Privacy Control** | A narrow, well-defined opt-out header | Recognised under California and Colorado law and in enforcement settlements; now a W3C Working Draft [25] | Narrow semantics plus legal backing succeed. Federated Ads honours GPC. |
| **Acceptable Ads / Coalition for Better Ads** | Industry criteria for "acceptable" formats | Criticised for pay-to-allowlist economics and for enforcement by an interested party | Keep rule-making, enforcement and revenue separate. |
| **Brave Ads** | On-device matching from a downloaded catalogue; anonymous reporting via Privacy Pass-style tokens | Works at scale (Brave reports over 100 million monthly active users [18]), but within one browser and one operator. Settled in its own token (BAT) [48] | Local matching and anonymous tokens work technically. Federation and payment neutrality are what is missing. |
| **Web Monetization / Coil** | Streaming micropayments as an alternative to ads | Coil shut down in March 2023; the work continues under the Interledger Foundation [27] | One company carrying an "open" standard is fragile. Payment rails are the hardest part, so stay rail-agnostic. |
| **Blockchain ad projects** (AdEx, Lucidity, the AdChain registry, Kochava XCHNG and others) [46][47] | On-chain ad accounting, token-curated domain registries, tokenised insertion orders | Pivoted or absorbed. Participants concluded what was really needed was "a better PKI" | Signatures and verifiable logs are the valuable part. They need no blockchain. |
| **EthicalAds, Carbon Ads** | Contextual, privacy-respecting networks | Commercially viable, small, centralised; pays publishers 70% of revenue [19][81] | Contextual advertising pays. Federation could let many such networks interoperate. |
| **Email (SMTP, DKIM, DMARC)** | Federated messaging with domain-bound signatures and aggregate reports | Authentication adoption jumped once large receivers *required* it of bulk senders (Gmail/Yahoo, February 2024) | The strongest model for Federated Ads: domain keys, aligned policy, aggregate reports and a few important parties requiring them. |
| **ActivityPub and Fediverse Enhancement Proposals (FEPs); AT Protocol labelers** | Federated social with a community extension process; composable, subscribable moderation [30][31] | Living ecosystems | A ready-made community process. Brand safety and fraud lists can be independent, subscribable "labelers". |
| **C2PA / Content Credentials** | Signed provenance manifests for media [34] | Growing adoption in cameras, phones and tools | Creative manifests should interoperate with C2PA, not reinvent provenance. |
| **AdCP and IAB Tech Lab AAMP** (2025–26) | Protocols for AI agents to plan and buy media [28][29] | Fast-moving; two camps | Federated Ads should not be a third agent protocol. It can be the federated identity, licence and receipt layer that agent protocols call. |
| **Academic privacy-preserving ad systems** (Adnostic 2010, Privad 2011, ObliviAd 2012) [37][38][39] | Local matching, cryptographic billing, anonymising intermediaries, click-fraud defence without identity | Prototypes and small deployments; never adopted by industry | The cryptography for private billing and fraud defence has existed for 15 years. What was missing was neutral governance and a reason for incumbents to adopt it. |
| **THEMIS** (Brave Research, 2020–21) [40] | Decentralised ad platform with zero-knowledge-verifiable campaign reports on a sidechain | Research prototype | Advertisers can accept privacy if reports are verifiable. Federated Ads aims for the same auditability with signed receipts and transparency logs, without a chain or token. |
| **Graze ads on Bluesky feeds** (2025) [41] | Advertisers buy placement in topical custom feeds; feed operators approve ads; no user-data targeting | Live and small (reported $1 CPM, 30% intermediary share) | Advertising by community and context works on federated social networks. Federated Ads would let many such operators interoperate without a single intermediary. |
| **Nostr ad proposals** (NOSTR-DAN, 2023; nostrads) [42][43] | Signed ad-space offers and bids over relays, with Lightning payouts | NOSTR-DAN unmerged after an ad-industry reviewer objected to auction-scale traffic over relays; nostrads experimental | Per-impression auctions do not fit federated transports. Deals and standing offers do ([§5.4](#54-why-deals-and-not-per-impression-auctions)). |
| **Privacy-preserving attribution research and standards** (IPA → W3C Attribution; IETF DAP; serve-time attestation) [24][44][45] | Aggregate, differentially private conversion measurement; signatures at serve time to resist fraud | Standards in progress at W3C and IETF | Receipts should be compatible with DAP and serve-time attestation rather than inventing a parallel measurement stack. |

**How Federated Ads differs from the closest work.** A literature and project search (October 2026) found no existing proposal that combines domain federation, contextual-by-default matching, verifiable delivery without a blockchain, and advertiser-owned, revocable creatives. The closest academic work, THEMIS [40], provides verifiable reporting but depends on a sidechain and a token and matches on behaviour. The closest live deployment, Graze [41], is contextual and community-controlled but is a single company, not an open protocol. We found no prior work applying transparency logs to ad delivery receipts, and no prior proposal for time-limited, revocable creative licences. We make this claim cautiously, because absence of evidence in a search is not proof, and we welcome pointers to work we missed.

**The ten lessons Federated Ads is designed around:**

1. **Bind identity to domains and make signing mandatory**, as email authentication did.
2. **Bridge rather than break.** Map to OpenRTB 2.6, AdCOM, VAST, the IAB Global Privacy Platform (GPP) and the IAB taxonomies.
3. **Ship production-grade reference code and key management**, not just text.
4. **No single vendor controls the standard.** Require two independent interoperable implementations before calling anything stable.
5. **Keep rule-making, enforcement and revenue separate.**
6. **Write change control into governance from day one.**
7. **Fund the stewards and avoid having the foundation operate critical infrastructure.** Matrix's funding crisis is the warning [33].
8. **No token, no chain.** Use PKI and verifiable logs.
9. **Define every term narrowly and honour signals that have legal force.**
10. **Plug into existing trust frameworks** (C2PA, Media Rating Council (MRC) definitions, Privacy Pass, W3C Attribution, agent protocols) instead of rebuilding them.

---

# Part II: What

## 3. Vision, principles, goals and non-goals

**Vision.** *Anyone can run an ad node. Advertisers own their creative. Publishers own their audience relationship. People own their attention. Everyone can verify what happened.*

### 3.1 Principles

| # | Principle | In practice |
|---|---|---|
| P1 | **Federated** | No mandatory central server, exchange, registry or token. Intermediaries are optional and replaceable. |
| P2 | **Owner control of creative** | Creatives are licensed, time-limited and revocable, never surrendered. |
| P3 | **Privacy by default** | Contextual matching. No cross-site personal identifiers in protocol messages. Aggregated receipts. Personal signals only by opt-in and preferably on the device. |
| P4 | **Verifiable** | Every economically meaningful event is a signed object recorded in an append-only, witnessable log. |
| P5 | **Rail-agnostic** | The protocol proves what is owed. Payment happens on any rail. |
| P6 | **User agency** | People can understand, refuse, pay to avoid, and report ads, and those choices are honoured. |
| P7 | **Surface-neutral** | One core protocol with profiles for web, social, email, audio and AI. |
| P8 | **Bridge to today** | Interoperate with existing buying and measurement systems. |
| P9 | **Boring primitives** | HTTPS, JSON, HTTP Message Signatures, W3C Data Integrity, Merkle logs. Verifiers never need a JSON-LD processor. |
| P10 | **Honest limits** | Where the protocol cannot guarantee something (deletion, humanity, cross-site frequency), it says so. |

### 3.2 Goals for v1

- Interoperable discovery, deal-making, licensing, revocation, receipts and statements between independently built nodes.
- At least two independent node implementations passing a shared conformance suite.
- Profiles for five surfaces: web display/native, social, email, audio and AI/chat.
- A privacy design that works with **no personal data** for matching and billing.
- A bridge that lets existing demand buy Federated Ads inventory without receiving personal data.

### 3.3 Non-goals for v1

- **Cross-publisher reach and frequency management.** This is impossible without cross-site identity, and Federated Ads deliberately gives that up.
- **Video and connected TV** beyond what VAST bridging gives. These are deferred to v2 because of format and measurement complexity.
- **Real-time auctions across nodes as the default.** They are available only as a constrained optional profile ([§6.4](#64-price-discovery)).
- **A native token, blockchain or mandatory payment provider.**
- **Conversion tracking at the individual level.** Only aggregate, privacy-preserving measurement is supported ([§10.6](#106-conversions-and-attribution)).
- **Content moderation of publisher content.** Federated Ads describes content but does not judge it.

---

## 4. Actors and roles

| Actor | Description | Runs a node? |
|---|---|---|
| **Advertiser** | Brand, business, non-profit or individual buying attention. Owns creatives. | Optional (may use a hosted buying node) |
| **Publisher** | A website, app, newsletter, podcast, fediverse instance or AI surface that shows ads. | Optional (may use a hosted selling node or cooperative) |
| **Buying node** | Acts for one or more advertisers. An agency, trading desk or self-serve tool. | Yes |
| **Selling node** | Acts for one or more publishers. A publisher itself, a cooperative of independent sites, or a group of instances. | Yes |
| **Relay** | Optional aggregator that routes offers between nodes and may add value through discovery, curation or credit. Cannot alter signed content. | Yes |
| **Creative host** | Stores creatives for the advertiser. Often the buying node itself. | Yes |
| **Witness** | Independently cosigns transparency-log checkpoints so a node cannot show different histories to different parties. | Yes |
| **Auditor** | Samples receipts and runs test clients; issues attestations. | Yes |
| **Labeler** | Publishes signed labels about nodes, domains or creatives: brand safety, fraud, verified identity. | Yes |
| **Attester / token issuer** | Issues privacy-preserving tokens that vouch for a client ([§10.5](#105-client-attestation)). | External |
| **Settlement provider** | Bank, payment processor or regulated stablecoin service that moves money. | External |
| **End user** | The person who sees or hears the ad. | Never required to run anything |

One organisation may hold several roles. Each node declares its roles in its signed Node Descriptor, the signed, machine-verifiable successor to ads.txt and sellers.json.

---

## 5. Architecture

### 5.1 Models considered

| Model | Summary | Strengths | Weaknesses |
|---|---|---|---|
| **A. Hybrid federated nodes** *(chosen)* | Independent nodes discover each other and exchange signed objects over HTTPS. Optional relays, witnesses and bridges. | Decentralises power; low latency; familiar web primitives; works for any surface. | Needs reputation and verification mechanisms; settlement is reconciled off-protocol. |
| **B. Network of networks** | Only existing ad networks federate. | Fast incumbent adoption. | Power stays with intermediaries. |
| **C. Fully peer-to-peer or on-chain** | Matching and settlement on a public ledger. | Programmable settlement; public auditability. | Latency and cost per event; public ledgers leak commercial data; regulatory burden; history of failure ([§2](#2-what-has-been-tried-lessons-from-prior-art)). |

Federated Ads adopts **Model A**. Model B is a subset, since a network can run a Federated Ads node. Model C appears only as an optional settlement profile ([§11](#11-settlement)).

### 5.2 Topology

```mermaid
flowchart LR
  subgraph Buy side
    ADV[Advertiser] --> BN[Buying node]
    BN --- CH[(Creative host)]
  end
  subgraph Sell side
    SN[Selling node] --> SURF[Surface: web, feed,<br/>email, audio, AI]
    PUB[Publisher] --- SN
  end
  BN <-- "signed offers / deals<br/>(direct or via relay)" --> SN
  R[Relay - optional] -.-> BN
  R -.-> SN
  CH -- "licensed fetch<br/>(TTL-bounded)" --> SN
  BN -- "revocations (push + log)" --> SN
  SN -- "aggregated signed receipts" --> BN
  W[Witnesses / auditors] -. "cosign logs, sample" .- SN
  W -. "cosign logs" .- BN
  BRIDGE[Bridge node] -- "OpenRTB / VAST" --- LEGACY[Existing DSPs and ad servers]
  BRIDGE --- SN
```

### 5.3 Lifecycle in brief

1. **Discover.** A node is found from a domain via `/.well-known/federated-ads` or WebFinger. It publishes a signed Node Descriptor listing roles, endpoints, keys, policies and profiles.
2. **Describe.** Selling nodes publish **Policies**: what they accept, their floors and their content categories. They also publish **Inventory** descriptions: forecast volumes, formats and contexts.
3. **Offer.** Buying nodes send signed **Offers** to specific sellers, or publish **Standing Offers** that any matching seller may claim.
4. **Agree.** The seller accepts, counters or declines. Acceptance creates a **Deal** with an allocated budget and the approved creative hashes.
5. **License.** For each approved creative, the advertiser issues a **Licence** bound to the deal, the licensee, the surfaces and an expiry.
6. **Serve.** At render time the selling node chooses among active deals ([§6.6](#66-ad-decisioning-on-the-selling-node)) and renders the creative with a "why this ad" disclosure.
7. **Report.** The selling node sends frequent **Spend Reports** for pacing and signed, aggregated **Receipt Batches** for billing. Both are committed to its transparency log.
8. **Revoke, any time.** The advertiser logs and pushes a **Revocation**. Receivers acknowledge it with a signed, logged **Revocation Acknowledgement**.
9. **Settle.** Both sides agree a **Statement** with two signatures and pay through the settlement profile they agreed.

### 5.4 Why deals and not per-impression auctions

Federated Ads prefers **pre-agreed deals evaluated locally at render time** to per-impression real-time bidding across the network. There are four reasons:

- **Privacy.** User context stays on the publisher's node. Nothing is broadcast to dozens of bidders.
- **Latency.** No network round trip is needed when rendering.
- **Accessibility.** A small operator can run a node.
- **Market evidence.** Even in conventional programmatic advertising, over 90% of median spend now runs through deals [4].

---

## 6. Market design: how buying and selling works

Version 0.1 left the market mechanism vague, and reviewers rightly called that the paper's largest gap. This section specifies it.

### 6.1 Inventory and rate cards

A selling node publishes an **Inventory** document so buyers can plan:

- **Placements:** surface, format, position, and context categories.
- **Forecasts:** expected impressions, sends or downloads per week by placement and context. Forecasts are always aggregated and rounded.
- **Rate card:** a posted price per placement and pricing model, plus minimum spend, lead time and whether creatives need approval.
- **Avails:** optional near-term availability by week.
- **Quality signals:** maximum ratio of ads to content and whether the page meets the Better Ads Standards [70]; ads per hour (audio) and per issue (email); refresh policy; and a saturation limit for feeds, as Bluesky feed operators already set [82]. Buyers can filter and price on low clutter ([§20.4](#204-improving-publisher-revenue)).
- **Floors and calendar:** per-placement floor prices for each pricing model, day-parts and a seasonal rate calendar.
- **Support options:** subscription, contribution and ad-free offers the publisher accepts.

### 6.2 Offer types

| Type | Use | How it works |
|---|---|---|
| **Direct Offer** | A buyer targets one known seller | One signed offer to one seller. The seller accepts, counters or declines. |
| **Standing Offer** | A buyer wants to reach many sellers without negotiating each one | One signed campaign with a total budget, price, targeting and policy, published to relays or directly. Any eligible seller may **claim** a slice up to a per-seller cap. The buyer's node confirms each claim, which turns it into a Deal. |
| **Request for proposals** | A buyer asks sellers to bid | The buyer publishes requirements. Sellers reply with priced proposals. The buyer accepts some, creating Deals. |

Standing Offers solve the many-to-many negotiation problem. A local advertiser can reach a hundred newsletters with one signed object, and each seller still keeps full control over what it accepts.

### 6.3 Pricing models

| Model | Code | Typical surface |
|---|---|---|
| Cost per thousand rendered impressions | `cpm` | Web, social, AI |
| Cost per thousand viewable impressions | `vcpm` | Web |
| Cost per click | `cpc` | All |
| Flat fee per unit (issue, episode, day, week) | `flat` | Newsletters, podcasts, sponsorships |
| Cost per delivered audio ad (IAB "Ad Delivered") | `cpad` | Podcasts |
| Fixed sponsorship of a section or feed | `sponsorship` | All |
| Cost per viewable hour (attention), from aggregate in-view time measured by the open module [65] | `cpvh` | Web, social, AI |

### 6.4 Price discovery

Federated Ads does not mandate a single auction. Prices form in three ways:

1. **Posted prices.** Sellers publish rate cards and buyers accept them. This is how newsletter and podcast sponsorship is sold today.
2. **Offer prices.** Standing Offers carry the buyer's price, and sellers choose which offers to claim.
3. **Local competition.** Each selling node ranks its eligible deals by effective price at render time ([§6.6](#66-ad-decisioning-on-the-selling-node)). Buyers who want delivery must pay competitive prices.

An optional `rtb` profile lets a selling node run a real-time auction among *pre-qualified* buyers. Bid requests are limited to context, coarse geography and placement, with no user or device identifiers.

**Price indices and competition law.** Public, aggregated price indices would help small participants. They must be designed to stay clear of competition law ([§19.8](#198-competition-law)):
- published by independent parties;
- aggregated across many nodes;
- delayed by at least 30 days;
- above minimum cell sizes;
- never forward-looking;
- never at the level of individual nodes.

### 6.5 Budgets, pacing and frequency

**Budgets.**
- Each Deal has an allocated budget. A Standing Offer has a total budget and a per-seller cap.
- Delivery beyond a Deal's budget is **not billable**. The seller carries the risk of overdelivery.

**Pacing.**
- Deals specify `even`, `asap` or day-parted pacing.
- Selling nodes send lightweight signed **Spend Reports** at least every 15 minutes (configurable per deal), so buyers can pause or shift budget.
- Signed hourly or daily **Receipt Batches** remain the billing record.

**Frequency.** Federated Ads is explicit about what is possible:
- **Per publisher:** supported. The selling node or the user's client enforces a frequency cap using first-party state only.
- **On-device:** supported through the optional on-device profile ([§8](#8-audience-matching-options-compared)), where the client holds the counters.
- **Across publishers:** not supported, by design. Deduplicated reach across publishers requires cross-site identity, which Federated Ads does not use. Buyers should plan Federated Ads buying as contextual, community-based reach, not upper-funnel reach-and-frequency buying.

### 6.6 Ad decisioning on the selling node

When an ad slot renders, the selling node:

1. filters active deals by eligibility: active licence, surface, context match, policy, budget remaining, frequency cap, and minor-safe or jurisdiction rules;
2. applies **priority tiers** (sponsorship > guaranteed > non-guaranteed > house);
3. ranks within a tier by effective price: an eCPM computed from the deal's pricing model and the node's own historical rates;
4. applies **competitive separation**, so two competitors are not shown side by side and advertiser category exclusions are respected;
5. renders, then counts the event for receipts.

The algorithm is the node's own. The protocol standardises only the inputs (deals, licences, policies) and the outputs (receipts).

---

## 7. Creative ownership, licensing and revocation

### 7.1 The principle

An advertiser grants a **licence to display**. It does not hand over a copy. The licence is limited in time, in scope (which deal, which licensee, which surfaces) and in purpose, and it can be withdrawn.

### 7.2 Objects

- **Creative Manifest:** a signed description of a creative's assets, each pinned by a content hash, plus metadata. Where the asset carries a C2PA manifest, the Creative Manifest references it [34]. Google has said its ad systems are starting to use C2PA metadata in policy enforcement [89].
- **Licence:** a separate signed object linking a manifest hash to a licensee node, a deal, surfaces, an issue time, a time-to-live (TTL) and a revocation source. Keeping the licence separate from the manifest means one creative can be licensed to many nodes, including through relays, without re-signing the creative.
- **Approval:** the selling node's signed acceptance of specific creative hashes, recorded in the Deal. A changed creative gets a new hash and needs a new approval. That closes the "swap the creative after approval" loophole.

### 7.3 Licence tiers

| Tier | Mechanism | Default TTL | Use |
|---|---|---|---|
| **Pointer** (default) | Assets stay on the creative host. The selling node fetches and caches them only within the TTL, renewing ahead of time so revocation checks never sit in the page's rendering path. | 15 minutes | Web, social, AI |
| **Signed cache** | The selling node may hold assets longer. It must subscribe to revocations. | Up to 24 hours | Email rendering, podcast ad insertion, offline apps |

**Why the selling node fetches, not the browser.** If people's devices fetched creatives directly from the advertiser's host, the advertiser would learn every viewer's IP address, which is a tracking channel. The selling node, or an Oblivious HTTP relay with a gateway at the creative host, does the fetching instead. The advertiser keeps control without gaining surveillance.

### 7.4 Revocation mechanics

1. **Log.** The advertiser appends a signed `Revocation` to its transparency log ([§15.8](#158-transparency-logs)). `effectiveAt` may not be earlier than the log inclusion time, so revocations cannot be backdated to avoid paying for impressions already served.
2. **Push.** The advertiser posts the revocation to every licensee. Relays forward it unaltered and with priority, subject to rate limits.
3. **Acknowledge.** Each receiver returns a signed `RevocationAck` and logs it. A receiver cannot later deny having received a revocation.
4. **Pull.** Licensees poll the advertiser's log checkpoint at least once per TTL, which covers missed pushes.
5. **Effect.** Impressions after `effectiveAt` (plus a grace period, 60 s by default) are **not billable**. Receipts and logs make them provable.

### 7.5 What revocation guarantees, per surface

Version 0.1 overstated revocation. The guarantees actually achievable are below.

| Surface | Guaranteed | Not guaranteed |
|---|---|---|
| **Web / native** | No new renders after the deadline (TTL or acknowledgement + 60 s). Assets purged from node caches. | Screenshots; copies in users' browser caches until they expire. |
| **Social posts** | No new sponsored posts. The selling node edits or deletes sponsored objects it has already posted (ActivityPub `Delete`/`Update`). | Copies that reach remote servers anyway (for example through boosts, quotes or replies), which may ignore deletes. |
| **Email** | No new sends. Images served through the node stop rendering where mail clients don't cache them. | Text already delivered to inboxes. Images cached by mail-provider proxies. |
| **Podcasts** | No new insertions into future downloads. | Episodes already downloaded and stored on listeners' devices. |
| **AI/chat** | No new sponsored units. Removal from regenerated or re-rendered sessions. | Conversation history and exports the user already has. |

Revocation is therefore defined as **"no new deliveries after the deadline, plus purging wherever technically possible."** The protocol does not promise that bytes disappear everywhere.

### 7.6 Revocation versus legal retention

Some laws require advertising records to be kept, not deleted:
- political advertising rules ([§19](#19-legal-and-regulatory-considerations));
- platform ad-repository duties;
- tax and anti-money-laundering record-keeping.

Federated Ads separates **serving** from **evidence**. Revocation stops serving immediately. A sealed archive record (creative hash, metadata, delivery totals) is kept for the legally required period, with deletion locked, in a store that is never used for serving.

### 7.7 Honest limits

No protocol can force a malicious party to delete bytes it has already received. Federated Ads makes misuse **unprofitable and provable** instead:
- an expired or revoked licence makes impressions unbillable;
- signatures and logs make violations attributable;
- labelers and node reputation let repeat offenders be excluded.

---

## 8. Audience matching: options compared

| Approach | How it works | Privacy | Relevance | Burden | Regulatory exposure |
|---|---|---|---|---|---|
| **Contextual** | Match on page, post, episode or conversation topic; publisher category; language; coarse region; time; device class | Excellent | Good, and improving with content classification | Low | Low |
| **On-device** | The client stores interest signals and selects among candidate ads locally; only aggregate, anonymous reports leave the device (the model Brave has proven [18]) | Very good | Good to high | High (needs client support) | Low to medium (device access may need consent) |
| **First-party opt-in** | A user knowingly shares interests with a publisher they trust; the publisher uses them only on its own node | Good | High for those who opt in | Medium | Medium (needs consent) |
| **Cross-site identity** (status quo) | Persistent identifiers track people across sites | Poor | High | Medium | High |

**Decision:**
- Every conformant node must support **contextual** matching.
- **On-device** matching is an optional profile. Its catalogue and reporting formats will be specified once at least one client implementer commits; until then it stays experimental.
- **First-party opt-in** signals may be used only by the publisher's own node and are never forwarded raw.
- **Cross-site identifiers are prohibited** in protocol messages.

Targeting in offers may therefore refer only to context categories (from the IAB Content Taxonomy 3.x, mapped into Federated Ads vocabulary), language, coarse region (country or first-level subdivision), time, device class and placement.

---

## 9. Brand safety and content policy: options compared

| Approach | Pros | Cons |
|---|---|---|
| **Bilateral policy**: each side publishes rules; a deal forms only where they match | Maximum autonomy; no central arbiter | Without shared vocabulary, policies cannot be compared by machine |
| **Shared taxonomy plus local rules**: one open vocabulary, with each node's own rules on top | Interoperable; communities keep their norms | Governing the taxonomy becomes political; risk of over-blocking news and minority voices |
| **Central certification** | A simple trust signal | Recentralises power; contradicts P1 |
| **Subscribable labelers** (as in AT Protocol): independent services publish signed labels, and each party chooses which to trust | Separates rule-making from enforcement; lets the market compete on brand safety and fraud detection; no single gatekeeper | Labelers need reputations of their own; risk of label inflation |

**Decision: shared vocabulary, bilateral enforcement, subscribable labelers.**

- Federated Ads defines an open, versioned taxonomy. It is mapped to the IAB Tech Lab Content Taxonomy 3.x and Ad Product Taxonomy 2.0 for compatibility.
- Policies are written in that taxonomy and evaluated by machine on both sides.
- Brand-safety, fraud and verification judgements come from **labelers** that advertisers and publishers choose to subscribe to. There is no central certifier.
- The taxonomy separates **"sensitive" from "unsafe"**, so news, health and LGBTQ+ content are not blocked by default. That is a known failure of keyword blocklists.
- **Regulated categories** require jurisdiction profiles ([§19.6](#196-jurisdiction-policy-profiles)). These include political and issue ads, alcohol, gambling, pharmaceuticals, financial and crypto promotions, and anything aimed at minors.
- **Landing-page cloaking**, where a page changes after approval, is countered in four ways:
  - the call-to-action (CTA) URL is pinned in the approved manifest;
  - selling nodes may periodically re-crawl landing pages;
  - labelers may flag cloaking;
  - a changed landing page voids the approval.

---

## 10. Measurement and verification

Version 0.1's measurement design was its second-largest weakness. In particular, its claim that creative-host fetch logs corroborate volume was wrong, because a caching node fetches the same number of times whether it serves a thousand impressions or a million. This section rebuilds the trust model.

### 10.1 Events

| Event | Definition | Billable? |
|---|---|---|
| `impression` | Creative rendered in the placement | Yes |
| `viewable` | Met the deal's viewability rule. The default follows the MRC: display 50% of pixels for 1 continuous second; large display 30% for 1 s; video 50% for 2 s [35] | Yes |
| `viewable_time` | Aggregate in-view seconds measured by the open measurement module; the basis for `cpvh` ([§6.3](#63-pricing-models)) | If the deal says so |
| `click` | User activated the CTA through the selling node's redirect | Yes |
| `ad_delivered` | Audio: 100% of the ad's bytes delivered within a valid download, per IAB Podcast Measurement v2.2 [36] | Yes |
| `ad_play_confirmed` | Audio: client-side confirmation of playback, where the player supports it | Yes, if the deal says so |
| `send` | Email: newsletter issue containing the ad sent to a deliverable address | Yes |
| `open` | Email: image load | **No.** Informational only, because privacy proxies such as Apple Mail Privacy Protection inflate it |
| `engagement` | Surface-specific actions, such as a reply to a sponsored post | If the deal says so |

### 10.2 Aggregated receipts

Receipts are **aggregate cells**, not per-impression logs. Each cell is one combination of:
- deal;
- creative hash;
- hour;
- context category;
- coarse region;
- event type;
- count.

Cells below a minimum count (default **k = 50**) are merged into an "other" cell. Each cell is a leaf in a Merkle tree, salted so that outsiders cannot confirm guesses. The batch is signed and its root is committed to the node's transparency log ([§15.8](#158-transparency-logs)).

### 10.3 Verification levels

A Deal states which levels are required. Price should reflect the level of verification.

| Level | Mechanism | What it proves | What it doesn't prove |
|---|---|---|---|
| **V0: signed self-report** | Seller-signed receipts in a witnessed log | The seller asserted these numbers, cannot later change them, and showed everyone the same history | That the numbers are true |
| **V1: licence compliance** | Creative-host fetch logs and revocation acknowledgements | The seller held a valid licence while serving and honoured revocations | Volume |
| **V2: outcome corroboration** | The advertiser counts arrivals on its landing page carrying the deal's non-personal parameter, and compares them with reported clicks. Statistically, impressions and clicks are compared with norms for the same context | Clicks broadly happened; detects gross inflation | Individual impressions |
| **V3: client attestation** | Privacy Pass tokens bound to the deal, redeemed for a sample of renders ([§10.5](#105-client-attestation)) | An attester vouched for a real client during that render | That a human saw it; coverage is limited to supporting platforms |
| **V4: independent audit** | An auditor runs test clients, checks Merkle inclusion for sampled cells, checks that the measurement-module hash matches, and attests | An independent party checked a sample | Everything outside the sample |

**Guidance:**
- V0 + V1 is suitable for prepaid or trusted, low-value deals.
- V0–V2 suits most direct deals.
- Large anonymous deals should require V3 or V4.

### 10.4 Viewability without third-party scripts

Federated Ads publishes an **open-source measurement module**. It is a small script whose hash is pinned, which measures viewability using standard browser APIs (Intersection Observer). Receipts record the module's hash, and auditors check that pages actually load that hash.

This is weaker than an independent verification vendor's script, because the publisher controls the page. It is also more transparent: anyone can read the module, and tampering with it is detectable in audits. For apps, a native equivalent is planned, aligned with the IAB Open Measurement SDK concepts.

### 10.5 Client attestation

Privacy Pass (RFC 9576–9578) lets an attester vouch for a client without identifying it.

**How Federated Ads uses it:**
- Token type **0x0002** (Blind RSA, publicly verifiable), so buyers and auditors can verify tokens themselves.
- The token challenge's `redemption_context` is set to `SHA-256(dealId ‖ creativeHash ‖ windowStart)`, so each token is bound to one deal, creative and time window.
- Redeemed tokens are committed in a Merkle tree alongside the receipt batch.

**Limits:**
- A token proves only that an *attester* vouched for the client. It does not prove a human.
- Deployment is uneven. Apple's Private Access Tokens cover recent Safari. Chrome implements a different API (Private State Tokens). The rate-limited token draft has expired.
- The attesters that exist today are large platform companies, which is in tension with P1.

V3 is therefore optional and sampled. Who should act as attesters is an open question ([§26](#26-open-questions)).

### 10.6 Conversions and attribution

Federated Ads does not define its own attribution system.

- **Allowed now:** click-through with a non-personal, deal-level parameter, plus aggregate on-site counting by the advertiser.
- **Planned profiles:**
  - an IETF DAP profile (Distributed Aggregation Protocol, Prio3 histograms) in which the advertiser's site reports conversions over coarse campaign buckets to two unaffiliated aggregators, under a fixed privacy budget per campaign per week;
  - a profile that consumes the W3C Attribution API output once that specification matures [24].
- **Prohibited:** per-user conversion pixels and click identifiers that are unique to a person.

### 10.7 Invalid traffic without fingerprinting

Selling nodes filter invalid traffic using:
- known-bot lists;
- data-centre IP ranges;
- rate heuristics;
- optional attestation.

Signals are processed transiently and not logged per user. Invalid-traffic categories are recorded as flags on receipt cells. Residual invalid traffic will be higher than with device fingerprinting, and buyers should expect it to be reflected in price.

### 10.8 Disputes

A party may open a signed `Dispute` against a receipt batch or statement when:
- verification signals diverge from receipts beyond the deal's tolerance (default 10%); or
- impressions appear after a revocation.

The dispute process in this draft:

1. **Bilateral review** within 14 days, using log proofs and verification evidence.
2. **Escalation to an arbiter** named in the deal, usually an auditor, whose decision binds for that deal.
3. **Escrow.** Under prepaid settlement, the disputed amount stays in escrow until resolved.

The burden of proof is set by verification level: under V0-only deals the seller's log stands unless the buyer shows contrary evidence.

---

## 11. Settlement

The protocol proves what is owed. **Settlement profiles** define how it is paid.

1. Each deal names acceptable settlement profiles and payment terms.
2. At period end, both nodes compute totals from receipts and exchange a signed `Statement`. The second signature is chained to the first (Data Integrity proof chains).
3. The doubly signed statement is the authoritative invoice basis.
4. Payment happens off-protocol. A signed `PaymentNotice` references the statement.

| Profile | Description | Notes |
|---|---|---|
| `settle:invoice` | Invoice plus bank transfer or card | Default; universal |
| `settle:processor` | Payouts through a regulated payment processor's marketplace accounts | Good for self-serve and small advertisers. Nodes never hold funds. |
| `settle:prepaid` | The advertiser pre-funds an escrow at a **regulated** provider; draws down per statement | Recommended default when the counterparty is unknown; protects publishers from credit risk |
| `settle:stablecoin` | Settlement in a regulated stablecoin; the statement hash may be recorded on-chain | Optional; restricted by jurisdiction ([§19.7](#197-payments)) |
| `settle:micropay` | Streaming or micro-settlement, e.g. Interledger Open Payments | Experimental |

**Design rules:**
- **Nodes should not hold other people's money.** Holding funds usually requires payment, e-money or money-transmission licences. Settlement profiles route funds through regulated providers, and a node that does hold funds must declare its licensing status.
- **All intermediary fees are declared in the signed deal**, so every party sees how each unit of currency is split. This attacks the "unknown delta" structurally.
- **Statements carry tax metadata:** supplier and customer jurisdiction, VAT or GST identifiers, and a reverse-charge indicator, so invoices can be generated.
- **Each deal states its terms:** payment terms, cancellation notice, make-good policy and currency. Deals may adopt existing industry terms by reference.

---

## 12. End-user rights

| Right | Requirement |
|---|---|
| **Why this ad** | Every ad carries a human-readable and machine-readable disclosure. It covers the advertiser's verified legal name; the payer, if different; the main reasons the ad was selected (e.g. "matched to: article topic *cycling*; region: *Kerala*"); the intermediaries and their declared fees; and how to change preferences. This matches the EU DSA Article 26 transparency elements and must render on every surface, including spoken disclosures in audio and AI. |
| **Opt-out** | Nodes honour the Global Privacy Control signal (`Sec-GPC: 1`) as a binding opt-out wherever law gives it effect. They honour equivalent legally recognised signals as these emerge. Because Federated Ads is contextual-only by default, opting out turns off every optional profile beyond contextual (on-device, first-party opt-in, conversion measurement). |
| **Ad-free option** | A selling node may advertise an ad-free offer (subscription, one-time payment or micropayment) at a standard endpoint. Following EDPB guidance, the ad-free option sits *alongside* a free contextual tier, never as a forced choice between consent and payment. |
| **Report and block** | People can report an ad (misleading, offensive, scam, sensitive) or block an advertiser. Reports go to the selling node and are forwarded in aggregate to the buyer and advertiser. Block lists stay on the device or with the first party and never become cross-site identifiers. Scam reports in financial categories have a defined takedown time. |
| **Minor-safe default** | Where a user's age is unknown, or the user is known to be under 18, only contextual delivery is allowed: no profiling, no on-device interest profile and no conversion measurement ([§19](#19-legal-and-regulatory-considerations)). |

---

## 13. Surfaces

### 13.1 Web display and native (`surface:web`)

**Creative formats allowed in v1:**

1. **Native** (default): a title, body, image or video asset and a CTA, rendered by the publisher's own template. No creative code.
2. **Display:** a static image (WebP, AVIF, PNG, JPEG, or SVG loaded as an image, never inline).
3. **HTML5:** allowed only at the extended conformance level. It runs in an `<iframe sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation">` served from a dedicated cookieless origin run by the selling node. The HTML and every file it loads must be hash-pinned assets of the approved manifest. A strict CSP lets the creative load only those assets from that origin, with scripts allowed by origin or hash and never `unsafe-eval`, and blocks every other request: no `connect-src`, no forms, no other origins. (A bare `default-src 'none'` would block the creative's own scripts and styles too.) `allow-same-origin` is never combined with `allow-scripts`.
4. **Never allowed:** third-party JavaScript, tracking pixels, or unpinned assets.

### 13.2 Social and fediverse (`surface:social`)

**ActivityPub.** ActivityStreams has no sponsorship concept, and remote servers drop properties they don't understand. The disclosure therefore appears **in the visible content** as well as in a machine-readable tag:

```json
{
  "@context": ["https://www.w3.org/ns/activitystreams",
               {"fa": "https://w3id.org/federated-ads/v0#", "Sponsorship": "fa:Sponsorship"}],
  "type": "Note",
  "attributedTo": "https://social.example.net/users/announcements",
  "content": "<p><strong>Sponsored · Paid partnership with Acme Bikes</strong></p><p>Ride further on a single charge…</p>",
  "tag": [{
    "type": "Sponsorship",
    "href": "https://ads.acme-bikes.example/fa/creatives/etour-v3",
    "name": "Acme Bikes Pvt Ltd"
  }]
}
```

Federated Ads will propose `fa:Sponsorship` as a Fediverse Enhancement Proposal [30]. We found no existing FEP for sponsored posts, only community concept documents. On Bluesky, Graze already sells ads placed in topical custom feeds and approved by feed operators [41], which shows demand for this model. Rules for this surface:
- **Opt-in.** Instance administrators choose whether to participate. Sponsored posts appear only in the feeds of that instance's users.
- **No federation as organic content.** Sponsored posts are addressed to local users only, never federated as public posts.
- **Revocation** is an ActivityPub `Delete`.

**AT Protocol.** Posts carry a self-label, and a Federated Ads labeler service issues signed `sponsored` labels so participating clients can recognise them [31]:

```json
"labels": { "$type": "com.atproto.label.defs#selfLabels", "values": [{ "val": "sponsored" }] }
```

A Lexicon record in the publisher's repository (its namespace identifier will be assigned once the project controls a domain) links the post to its manifest and deal.

### 13.3 Newsletters (`surface:email`)

- Creatives are rendered at send time under a signed-cache licence.
- The billable unit is `send` or `click`. Opens are informational only ([§10.1](#101-events)).
- Clicks go through the selling node's redirect and carry no personal parameters.
- The sponsorship label must appear in the email body text, not only in markup.

### 13.4 Podcasts and audio (`surface:audio`)

- Dynamically inserted ads are delivered by the hosting node using IAB Podcast Measurement v2.2 definitions for valid downloads and delivered ads [36].
- Host-read ads are represented as a script creative with an approval workflow.
- A VAST 4.x bridge (audio ads, VMAP placement) connects to existing ad-insertion servers.
- The disclosure is spoken ("This episode is sponsored by…") and also appears in the episode notes.

### 13.5 AI and chat surfaces (`surface:ai`)

People may not be able to tell an answer from persuasion. Additional rules apply:

1. **Separation.** Sponsored content is a distinct unit, visually and semantically separate from the generated answer. Paid influence on the organic answer is prohibited.
2. **Labelling.** A persistent "Sponsored" label and a why-this-ad disclosure on every sponsored unit.
3. **Context handling.** Matching may use the topic of the current conversation, derived in the session on the AI provider's node. Conversation content is never sent to buying nodes and is not kept for advertising beyond the session unless the user opts in.
4. **Ineligible contexts.** Conversations classified as health, mental health, crisis, politics or legal or financial distress, and accounts known to belong to minors, receive no ads by default. This is broadly in line with what OpenAI announced for ChatGPT [13].
5. **No emotional targeting.** Sponsored units may not be selected or worded using inferences about the user's emotional state or vulnerabilities (relevant to EU AI Act Article 5).
6. **Synthetic creatives** are marked as AI-generated and carry provenance metadata (C2PA where available).
7. **Creative integrity.** Research on LLM advertising proposes merging ads into the generated answer itself, through auctions on summaries or retrieval-augmented insertion [62][63][64]. Federated Ads does not allow this by default. A licensed creative is shown as the advertiser approved it and may not be paraphrased, summarised or blended into generated text unless its Licence explicitly permits adaptation, and an adapted unit must still be labelled and kept separate from the organic answer. This answers the concern that commercial influence in AI answers must be attributable, measurable and contestable [61].

### 13.6 AI agents (`profile:agent`)

When an AI agent acts for a user, for example comparing products or booking services:
- It must disclose to the user when a sponsored option influenced its choice.
- It must not prefer a sponsored option over a better organic one without disclosure.
- Federated Ads offers a binding that exposes node functions (discover inventory, create offers, fetch receipts) as tools for agent frameworks. This lets agent protocols such as AdCP and IAB Tech Lab's AAMP use Federated Ads as their **identity, licence and receipt layer**, instead of Federated Ads competing with them [28][29].

---

## 14. Interoperability with existing standards

### 14.1 Approaches compared

| Option | Pros | Cons |
|---|---|---|
| **Extend existing protocols** (ActivityPub, OpenRTB) | Existing buyers and servers; continuity for standards bodies; mature libraries | Inherits OpenRTB's data leakage and ActivityPub's loose typing; ownership and revocation would be bolted on |
| **Clean slate** | Designed for ownership, revocation, receipts and privacy | No liquidity at launch; no tooling |
| **Clean-slate core on existing primitives, plus bridges** *(chosen)* | Native design where it matters; proven building blocks elsewhere; an on-ramp for existing demand | Bridges need careful privacy stripping; two code paths |

### 14.2 What Federated Ads reuses

| Standard | Role |
|---|---|
| HTTP Semantics (RFC 9110) | Transport |
| HTTP Message Signatures (RFC 9421) and Digest Fields (RFC 9530) | Authenticating each hop |
| W3C Data Integrity 1.0 with `eddsa-jcs-2022`; JSON Canonicalization Scheme (RFC 8785) | End-to-end signatures on stored objects |
| W3C Controlled Identifiers 1.0 (Multikey) | Key representation |
| WebFinger (RFC 7033); well-known URIs (RFC 8615) | Discovery |
| Problem Details (RFC 9457) | Errors |
| Merkle tree hashing (RFC 6962/9162); C2SP tlog-tiles, tlog-checkpoint, signed-note, tlog-witness | Transparency logs |
| Privacy Pass (RFC 9576–9578) | Client attestation |
| Oblivious HTTP (RFC 9458) | Optional private fetching |
| WebSub (W3C) | Pattern for push subscriptions (revocations) |
| IETF DAP (draft); W3C Attribution (draft) | Future aggregate conversion profiles |
| Global Privacy Control (W3C draft); IAB GPP | Opt-out and consent signals |
| ActivityPub, AT Protocol | Social surfaces |
| IAB Content Taxonomy 3.x, Ad Product Taxonomy 2.0, ads.txt, sellers.json | Vocabulary and seller authorisation mapping |
| OpenRTB 2.6, AdCOM, VAST 4.x, IAB Podcast Measurement v2.2, MRC viewability | Bridges and measurement definitions |
| C2PA | Creative provenance |

### 14.3 Bridges

**OpenRTB bridge.** In conventional programmatic advertising, *sell-side platforms send bid requests to demand-side platforms*. The Federated Ads bridge plays that sell-side role on behalf of Federated Ads selling nodes:

- It holds Federated Ads deals with publishers and issues OpenRTB 2.6 requests to existing buyers for that inventory, using deal IDs (private marketplace, PMP) where possible.
- It removes all user and device identifiers, precise location and other personal fields.
- It converts winning bids into Federated Ads deals and licences.

Expect modest demand through the bridge. Existing buyers pay less for inventory without identifiers. The bridge exists to avoid a completely empty marketplace, not to replace direct Federated Ads buying.

**VAST bridge.** It turns a Federated Ads manifest into a VAST `InLine` response for ad-insertion servers and video players.

**Agent binding.** It exposes Federated Ads operations as tools for agent frameworks, as described in [§13.6](#136-ai-agents-profileagent).

---

# Part III: How

## 15. Protocol overview

> This section is informative. Normative requirements, including the MUST/SHOULD/MAY keywords as defined in BCP 14 (RFC 2119 and RFC 8174), live in the Internet-Draft `draft-rajan-federated-ads-protocol`. All example values are illustrative. Keys, signatures and hashes are placeholders unless stated otherwise.

### 15.1 Conventions

- Objects are JSON. The namespace is `https://w3id.org/federated-ads/v0`, a permanent identifier that redirects to the specification. Verifiers process the **JSON bytes**. JSON-LD processing is optional and used only for vocabulary extension.
- Object identifiers are `https://` URLs on the issuing node, e.g. `https://ads.example.com/fa/offers/0c8e5d3a`.
- Timestamps are RFC 3339 in UTC with a literal `Z`. Money is `{"amount": "12.50", "currency": "USD"}`, with the amount as a decimal string.
- Content hashes use the Subresource Integrity format, `sha256-<base64>`.
- The media type is `application/federated-ads+json` (registration planned).

### 15.2 Two layers of signatures

| Layer | Mechanism | Protects |
|---|---|---|
| **Transport (each hop)** | RFC 9421 HTTP Message Signatures with `created`, `expires`, `keyid`, `alg="ed25519"`, `tag="federated-ads"`, covering `@method`, `@target-uri`, `content-type` and `content-digest` when there is a body. Responses are also signed (covering `@status` and the request via `;req`). | Authenticity and freshness of each request and response; replay protection |
| **Object (end to end)** | W3C Data Integrity proof, cryptosuite `eddsa-jcs-2022` | Integrity of stored objects across relays and over time. Relays re-sign the transport but cannot alter object proofs. |

The same `eddsa-jcs-2022` cryptosuite is used by the fediverse's object-integrity proofs (FEP-8b32), which Mastodon 4.7 verifies [32].

Example signed request:

```http
POST /fa/inbox HTTP/1.1
Host: ads.example.com
Content-Type: application/federated-ads+json
Content-Digest: sha-256=:Pc1EWC05sjJPosvus5LefPh+i3TViCo38kEWdpN6oa0=:
Signature-Input: fa=("@method" "@target-uri" "content-type" "content-digest");created=1791187200;expires=1791187500;keyid="https://ads.acme-bikes.example/fa/node#key-2026";alg="ed25519";tag="federated-ads"
Signature: fa=:<base64 Ed25519 signature>:
```

Example object proof:

```json
"proof": {
  "type": "DataIntegrityProof",
  "cryptosuite": "eddsa-jcs-2022",
  "created": "2026-10-05T10:00:00Z",
  "verificationMethod": "https://ads.acme-bikes.example/fa/node#key-2026",
  "proofPurpose": "assertionMethod",
  "proofValue": "z2HnFSSPPBzR36zdDgK8PbEHeXbR56YF24jwMpt3R1eHXQz…"
}
```

### 15.3 Identity, keys and discovery

**Discovery.** A domain publishes `/.well-known/federated-ads`, to be registered under RFC 8615. It lists the domain's own node or its authorised delegates. WebFinger (`resource=https://example.com`) is supported as an alternative.

**Node Descriptor.** The descriptor is itself a W3C Controlled Identifier document. Keys are `Multikey` entries:
- `assertionMethod` keys sign objects;
- `authentication` keys sign HTTP messages.

**Key rotation.**
1. Publish the new key alongside the old one.
2. Log a `KeyRotation` signed by the old key.
3. Retire the old key after the maximum object lifetime.

**Compromise.** Log a `KeyRevocation` with `revokedAt`. Because key history lives in the log, signatures on old receipts remain verifiable after rotation. Hot signing keys should be short-lived subkeys certified by an offline root key.

```json
{
  "@context": ["https://www.w3.org/ns/cid/v1", "https://w3id.org/federated-ads/v0"],
  "id": "https://ads.example.com/fa/node",
  "type": "Node",
  "name": "Example News selling node",
  "roles": ["publisher", "selling"],
  "operator": { "legalName": "Example Media Ltd", "jurisdiction": "IN", "contact": "ads@example.com" },
  "verificationMethod": [{
    "id": "https://ads.example.com/fa/node#key-2026",
    "type": "Multikey",
    "controller": "https://ads.example.com/fa/node",
    "publicKeyMultibase": "z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2"
  }],
  "assertionMethod": ["https://ads.example.com/fa/node#key-2026"],
  "authentication": ["https://ads.example.com/fa/node#key-2026"],
  "endpoints": {
    "inbox": "https://ads.example.com/fa/inbox",
    "inventory": "https://ads.example.com/fa/inventory",
    "policy": "https://ads.example.com/fa/policy",
    "log": "https://ads.example.com/fa/log/",
    "adfree": "https://example.com/subscribe"
  },
  "surfaces": ["surface:web", "surface:email"],
  "settlement": ["settle:invoice", "settle:prepaid"],
  "jurisdictionProfiles": ["jp:in", "jp:eu"],
  "conformance": ["federated-ads-core/0.2"],
  "critical": []
}
```

### 15.4 Core objects

| Object | Issued by | Purpose |
|---|---|---|
| `Node` | Any node | Identity, keys, endpoints, roles, profiles |
| `Policy` | Seller / buyer | What is accepted or required, in taxonomy terms |
| `Inventory` | Seller | Placements, forecasts, rate card |
| `Offer` / `StandingOffer` / `RFP` | Buyer | Proposed terms |
| `Claim` / `Acceptance` / `CounterOffer` / `Decline` | Seller (Claim, Acceptance); either party (CounterOffer, Decline) | Responses to offers; an Acceptance carries creative approvals ([§7.2](#72-objects)) |
| `Deal` | Both (two-signature chain) | Agreed terms, budget, approved creative hashes, fees, verification levels, settlement |
| `CreativeManifest` | Advertiser | Assets, hashes, metadata, C2PA reference |
| `Licence` | Advertiser | Right to display: manifest hash, licensee, deal, surfaces, TTL |
| `Revocation` / `RevocationAck` | Advertiser / licensee | Withdraw a licence; prove receipt |
| `SpendReport` | Seller | Near-real-time pacing counters |
| `ReceiptBatch` | Seller | Signed aggregate delivery cells with a Merkle root and log inclusion |
| `Statement` / `PaymentNotice` | Both / payer | Settlement |
| `Dispute` | Either | Contest a batch or statement |
| `Report` | Seller (aggregating users) | User reports |
| `Label` | Labeler | A signed judgement about a node, domain or creative |
| `KeyRotation` / `KeyRevocation` | Any node | Key lifecycle |

### 15.5 Example: Licence (separate from the manifest)

```json
{
  "@context": ["https://w3id.org/federated-ads/v0", "https://w3id.org/security/data-integrity/v2"],
  "type": "Licence",
  "id": "https://ads.acme-bikes.example/fa/licences/7d41",
  "manifest": "https://ads.acme-bikes.example/fa/creatives/etour-v3",
  "manifestHash": "sha256-l/CpsGkeGlPK62GeqemLcWH9HRMXJO/lbCmDtsgPL8k=",
  "licensee": "https://ads.example.com/fa/node",
  "deal": "https://ads.acme-bikes.example/fa/deals/3d9e",
  "surfaces": ["surface:web"],
  "tier": "pointer",
  "issuedAt": "2026-10-05T10:00:00Z",
  "expiresAt": "2026-10-05T10:15:00Z",
  "revocationLog": "https://ads.acme-bikes.example/fa/log/",
  "proof": { "type": "DataIntegrityProof", "cryptosuite": "eddsa-jcs-2022", "…": "…" }
}
```

### 15.6 State machines

```mermaid
stateDiagram-v2
  direction LR
  state "Offer" as O {
    [*] --> Sent
    Sent --> Countered
    Countered --> Countered
    Countered --> Sent
    Sent --> Accepted
    Countered --> Accepted
    Sent --> Declined
    Countered --> Declined
    Sent --> Expired
    Countered --> Expired
    Sent --> Withdrawn
    Countered --> Withdrawn
  }
  state "Deal" as D {
    [*] --> Active
    Active --> Paused
    Paused --> Active
    Active --> Exhausted
    Active --> Ended
    Paused --> Ended
    Exhausted --> Active
    Exhausted --> Ended
    Active --> Terminated
    Paused --> Terminated
  }
  state "Licence" as L {
    [*] --> Issued
    Issued --> Expired_
    Issued --> Revoked
  }
  state "Statement" as S {
    [*] --> Proposed
    Proposed --> Countersigned
    Countersigned --> Paid
    Proposed --> Disputed
    Countersigned --> Disputed
    Disputed --> Countersigned
  }
  state "Dispute" as DS {
    state "Withdrawn" as DWithdrawn
    [*] --> Open
    Open --> DWithdrawn
    Open --> Resolved
    Open --> Escalated
    Escalated --> Resolved
  }
```

Every transition is a signed message referencing the previous state's object. A Deal is marked **Disputed** while a Dispute about it is open or escalated. That pauses settlement of the disputed amount but not delivery, unless a party also pauses the deal. A Dispute is resolved bilaterally by the disputing party, or by the arbiter named in the deal after escalation ([§10.8](#108-disputes)).

### 15.7 Messaging, errors and delivery semantics

- **Inbox model.** Each node has one inbox endpoint that receives signed objects. It answers `202 Accepted` with a signed acknowledgement, and processes asynchronously where needed.
- **Idempotency.** The object `id` is the deduplication key. Receivers keep IDs for at least the object's lifetime plus 7 days.
- **Delivery.** At least once, with exponential back-off. `429` with `Retry-After` for rate limiting.
- **Errors.** RFC 9457 Problem Details with `type` URIs under `https://w3id.org/federated-ads/errors/`, e.g. `licence-expired`, `policy-mismatch`, `budget-exhausted`, `signature-invalid`, `unknown-critical-extension`.
- **Clocks.** Allowed clock skew is ±60 seconds. Signatures older than their `expires` are rejected.
- **Pagination.** Cursor-based, for logs and lists.
- **Extensions.** Unknown fields are ignored *unless* they are listed in the object's `critical` array. A receiver that does not understand a critical extension must reject the object. This keeps new brand-safety constraints from being silently dropped.
- **Versioning.** Nodes advertise supported protocol versions. A new major version requires negotiation. Minor versions are additive.

### 15.8 Transparency logs

Every node keeps an **append-only Merkle log** in the C2SP tlog-tiles format, the same family used by Certificate Transparency and Sigstore. The log records:
- receipt batch commitments;
- revocations and revocation acknowledgements;
- statements;
- key rotations.

**Checkpoints.**
- Each checkpoint records tree size and root hash, and is signed with the signed-note format.
- **Witnesses** (auditors, cooperatives, other nodes) cosign checkpoints after verifying consistency proofs.
- This makes it impossible for a node to show different histories to different counterparties without being detected.
- Witness cosignatures also give approximate time anchoring, which supports the rule that revocations cannot be backdated.

**Proofs.**
- Buyers fetch inclusion proofs for their batches and consistency proofs between the checkpoints they have seen.
- Tiles are immutable and can be cached on CDNs, so logs are cheap to serve.

### 15.9 Example: Receipt Batch

```json
{
  "@context": ["https://w3id.org/federated-ads/v0", "https://w3id.org/security/data-integrity/v2"],
  "type": "ReceiptBatch",
  "id": "https://ads.example.com/fa/receipts/2026-10-05T10",
  "deal": "https://ads.acme-bikes.example/fa/deals/3d9e",
  "window": { "start": "2026-10-05T10:00:00Z", "end": "2026-10-05T11:00:00Z" },
  "kThreshold": 50,
  "totals": { "impression": 18240, "viewable": 12011, "click": 97 },
  "cells": [
    { "creative": "sha256-LJpNdR1icOVWU9oFx6AudeMrsiNfhqPDpjdn2UZhUJQ=", "context": "sports:cycling",
      "region": "IN-KL", "event": "impression", "count": 11020 },
    { "creative": "sha256-LJpNdR1icOVWU9oFx6AudeMrsiNfhqPDpjdn2UZhUJQ=", "context": "technology",
      "region": "IN-KA", "event": "impression", "count": 7220 },
    { "creative": "sha256-LJpNdR1icOVWU9oFx6AudeMrsiNfhqPDpjdn2UZhUJQ=", "context": "*",
      "region": "*", "event": "click", "count": 97 }
  ],
  "cellTree": { "alg": "rfc6962-sha256", "size": 7, "root": "sha256-…" },
  "measurementModule": "sha256-…",
  "attestation": { "tokenType": "0x0002", "issuer": "https://issuer.example", "count": 2104,
                   "tokenTree": { "size": 2104, "root": "sha256-…" } },
  "log": { "origin": "ads.example.com/fa/log", "index": 48213 },
  "proof": { "type": "DataIntegrityProof", "cryptosuite": "eddsa-jcs-2022", "…": "…" }
}
```

The `cells` array is abridged. The full batch has seven cells, including the viewable counts.

### 15.10 Registries

The specification will define registries with explicit registration policies for:
- event types;
- pricing models;
- surface profiles;
- settlement profiles;
- jurisdiction profiles;
- revocation reasons;
- error types;
- taxonomy versions;
- critical extensions.

Initially the editors maintain the registries in the repository. They will move to the eventual standards body.

### 15.11 Conformance levels

| Level | Includes |
|---|---|
| **federated-ads-core** | Discovery; Node Descriptor; Policy; Direct Offer → Deal; Licence (pointer tier); revocation (push, log, acknowledgement); aggregated Receipt Batches in a witnessed log; why-this-ad; GPC; Report; contextual matching; native and static display formats |
| **federated-ads-extended** | Core + Standing Offers and RFPs; signed-cache tier; Spend Reports; Statements and at least one settlement profile; ad-free endpoint; HTML5 sandbox; dispute flow |
| **federated-ads-verified** | Extended + V3 client attestation and/or V4 audit attestation from an auditor or labeler the counterparty trusts |

The `/0.2` suffix in conformance tokens is the protocol version, which is versioned independently of this whitepaper. Surface profiles add rendering, labelling and measurement requirements. A public conformance suite and test vectors (signatures, Merkle proofs, canonicalisation) ship with each version.

---

## 16. End-to-end worked example

**Scenario.** Acme Bikes, a Kerala e-bike retailer, wants to reach cycling and technology readers in Kerala and Karnataka for October. It uses a hosted buying node. *Example News* runs its own selling node. Every name is fictional.

```mermaid
sequenceDiagram
  autonumber
  participant B as Buying node (Acme)
  participant S as Selling node (Example News)
  participant C as Creative host (Acme)
  participant W as Witness / auditor
  B->>S: GET /.well-known/federated-ads → Node, Policy, Inventory
  B->>S: POST inbox: Offer (CPM ₹350, budget ₹1,25,000, Oct 5–31, cycling+tech, IN-KL/KA)
  S->>B: CounterOffer (CPM ₹380, creative approval required)
  B->>S: Offer v2 (CPM ₹370)
  S->>B: Acceptance (+ approves creative hash)
  B->>S: Deal (countersigned chain) + Licence (pointer, 15 min)
  S->>C: Fetch manifest + assets (signed request), cache ≤ TTL
  loop every ≤15 min
    S->>B: SpendReport
    S->>C: Renew licence ahead of expiry
  end
  S->>W: Log checkpoint → witness cosigns
  S->>B: ReceiptBatch (hourly, aggregated, log index)
  B->>W: Fetch inclusion + consistency proofs
  Note over B,C: Oct 12: pricing error found on landing page
  B->>B: Append Revocation to own log (effectiveAt = now)
  B->>S: POST Revocation
  S->>B: RevocationAck (signed, logged) — stops serving within 60 s
  B->>S: New manifest v4 + approval request + new Licence
  Note over B,S: Oct 31: campaign ends
  S->>B: Statement (signed)
  B->>S: Statement countersigned
  B->>S: PaymentNotice (settle:invoice, bank transfer)
```

**What each step shows:**

- **Steps 2–5:** negotiation is ordinary and auditable.
- **Step 6:** the deal records the approved creative hash, the declared fees (here a 6% hosted buying-node fee, visible to both parties) and the verification levels: V0 + V1 + V2.
- **Steps 7–9:** creative control without tracking. The selling node fetches the creative, people's devices never contact Acme's server, and licences renew in the background.
- **Steps 10–12:** delivery is verifiable without per-user data. Receipts are aggregated cells, and the log is witnessed.
- **Steps 13–16:** revocation is fast and provable. Impressions after `effectiveAt` + 60 s are not billable, and both sides hold signed evidence.
- **Steps 17–19:** settlement uses whatever rail the parties chose, based on a statement both have signed.

---

## 17. Security considerations

### 17.1 Trust assumptions

- A node's identity is rooted in control of its domain and TLS. Domain takeover means identity takeover. Logged key history limits the damage to past records.
- Witnesses are assumed not to all collude with the node they witness.
- Privacy Pass attesters are assumed not to collude with the selling node.

### 17.2 Threats and mitigations

| Threat | Mitigation |
|---|---|
| **Impression inflation** by a seller | Verification levels V2–V4; witnessed logs make inflated numbers permanent and attributable; price reflects verification |
| **Backdated receipts or revocations** | Log inclusion plus witness cosignatures anchor time; `effectiveAt` ≥ log time; signed acknowledgements |
| **Equivocation** (different histories for different parties) | Witness cosigning and consistency proofs |
| **Replay** | RFC 9421 `created`/`expires`; object `id` deduplication |
| **Seller + relay collusion** | Relays cannot alter signed objects; fees declared in the deal; buyers may require direct delivery of receipts |
| **Seller + sock-puppet advertiser** (laundering, fake demand) | know-your-business (KYB) attestations from labelers; settlement through regulated providers with their own checks |
| **Sybil publishers** farming Standing Offers | Per-seller caps; minimum verification levels for unknown sellers; labeler reputation; prepaid or holdback for new sellers |
| **Click fraud** through the seller's own redirect | V2 landing-page corroboration; invalid-traffic filtering; CPC deals can require V3 |
| **Malvertising** | Restricted formats ([§13.1](#131-web-display-and-native-surfaceweb)); hash pinning; approval of exact hashes; sandbox profile; Report flow |
| **Landing-page cloaking** | Pinned CTA; re-crawls; labelers; approval voided on change |
| **Server-side request forgery (SSRF)** through the seller fetching advertiser URLs | Fetch only from the creative host declared in the advertiser's Node Descriptor; block private address ranges; size and type limits |
| **Revocation flooding** | Revocations must come from the licence issuer's key; rate limits; relays authenticate before giving priority |
| **Report-channel abuse** | Reports aggregated and rate-limited; no automatic takedown except for scam categories with verification |
| **Key compromise** | Short-lived subkeys; offline root; logged revocation |
| **Attester centralisation** | V3 is optional; multiple issuers allowed; an open question on community attesters |

### 17.3 Implementation requirements

The reference implementation will include safe defaults for:
- signature verification;
- canonicalisation (RFC 8785);
- log verification;
- fetch sandboxing;
- key storage.

ads.cert showed that weak reference code stalls adoption [20].

---

## 18. Privacy considerations

### 18.1 Data inventory

| Data | Where processed | Retention | Leaves the node? |
|---|---|---|---|
| IP address, user agent | Selling node (coarse region lookup, invalid-traffic filtering) | Transient (seconds to hours) | No |
| Page, post or episode context | Selling node | As for the content | Only as a category in aggregate cells |
| Conversation context (AI) | AI provider's node, in session | Session only, unless the user opts in | No |
| Frequency counters | Selling node (first party) or the user's device | Campaign duration | No |
| Aggregate receipt cells | Selling node → buyer, auditor | Contract and legal retention | Yes, aggregated with k ≥ 50 |
| Report content | Selling node → aggregate to the advertiser | As required for moderation | Aggregated |
| Privacy Pass tokens | Client → selling node → auditor | Batch retention | Yes, unlinkable |

### 18.2 Re-identification risk

Combinations of fine context, language, region and time can single out individuals, especially on small fediverse instances. Federated Ads limits this with:
- **aggregation** into cells;
- **k-thresholds**, with small cells merged;
- hourly or coarser windows;
- coarse regions only;
- salted Merkle leaves;
- a ban on per-click unique identifiers.

Small nodes whose volume falls below thresholds report daily or weekly instead of hourly.

### 18.3 Device access

Viewability scripts, on-device profiles and Privacy Pass tokens all involve reading from or storing on the user's device. EU guidance treats this broadly as access to terminal equipment, which may require consent unless strictly necessary. **Core** Federated Ads billing therefore works **server-side**: impressions, sends, deliveries and clicks. Device-side features are optional profiles that come with their own consent requirements ([§19](#19-legal-and-regulatory-considerations)).

### 18.4 The standards body and controllership

The CJEU's *IAB Europe* judgment (C-604/22, March 2024) held that a standards body can be a joint controller when its rules shape how personal data is processed, even if it never receives the data. Federated Ads therefore:
- operates **no central infrastructure** that handles user signals;
- keeps user-side signals (opt-outs, blocks, reports) local or aggregated;
- will publish a template allocation of controller responsibilities for node operators.

---

## 19. Legal and regulatory considerations

> This section is a map of considerations, not legal advice. Several 2026 developments rest on secondary sources and must be verified against primary texts before reliance.

### 19.1 European Union

| Instrument | Relevance | Federated Ads response |
|---|---|---|
| **GDPR**; CJEU *Meta v Bundeskartellamt* (C-252/21, 2023) | Personalised ads generally require consent | Contextual default that needs no profiling; profiling only through opt-in profiles |
| **EDPB Opinion 08/2024** ("consent or pay") | A bare pay-or-consent choice rarely gives valid consent for large platforms; a free, less-personalised alternative is recommended | Free contextual tier always available alongside ad-free payment |
| **ePrivacy Art. 5(3)**; EDPB Guidelines 2/2023 | Device access (pixels, local storage, identifiers) generally needs consent | Server-side core; device features opt-in |
| **CJEU *IAB Europe* (C-604/22, 2024)** | Joint-controllership risk for standard-setters | No central user-signal infrastructure ([§18.4](#184-the-standards-body-and-controllership)) |
| **Digital Services Act**: Art. 26 (ad transparency), Art. 28 (no profiling ads to minors), Art. 39 (repositories for very large platforms) | Required disclosures; minors; record-keeping | Why-this-ad matches Art. 26; minor-safe default; repository export API |
| **Digital Markets Act** Arts. 5–6 | Price, fee and verification transparency for gatekeepers' business users | Federated Ads offers this transparency to everyone by design |
| **Political advertising Regulation (EU) 2024/900** (applies from 10 October 2025) | Labels, transparency notices, strict targeting limits, record retention. Google and Meta withdrew political ads in the EU rather than comply | Political and issue ads **off by default**; enabled only by a dedicated jurisdiction profile; archive retention |
| **AI Act**: Art. 5 (manipulative practices), Art. 50 (transparency; applicable from 2 August 2026) | AI-chat ads and synthetic creatives | AI surface rules ([§13.5](#135-ai-and-chat-surfaces-surfaceai)) |
| **Pending:** Digital Omnibus (machine-readable consent signals), Digital Fairness Act | May change consent and dark-pattern rules | Regulatory watch; signal handling designed to map onto machine-readable signals |

### 19.2 United Kingdom

- **Data (Use and Access) Act 2025:** relaxed some cookie-consent rules for analytics, not for advertising measurement, and raised PECR fines to UK GDPR levels.
- **Online Safety Act:** Ofcom is consulting on codes for fraudulent advertising.
- **FCA financial promotions regime:** applies to crypto advertising.

### 19.3 United States

- **FTC 2015 Enforcement Policy Statement on Deceptively Formatted Advertisements** and the **2023 Endorsement Guides:** they apply directly to sponsored posts, newsletter placements, podcast reads and AI answers. Disclosures must be clear and hard to miss.
- **Revised COPPA Rule:** compliance required by April 2026.
- **State privacy laws:** at least a dozen states require businesses to honour universal opt-out signals such as GPC (per secondary trackers). California's AB 566 requires browsers to offer an opt-out signal from 2027.

### 19.4 India

The lead contributor's home jurisdiction.

- **Digital Personal Data Protection Act 2023 and DPDP Rules 2025:** phased in, with most obligations applying from May 2027.
  - **Section 9 bars tracking, behavioural monitoring and targeted advertising directed at children (under 18).** This supports Federated Ads' contextual-only minor-safe default.
  - The consent-manager framework is a possible integration point for opt-in signals.
- **CCPA Guidelines for Prevention and Regulation of Dark Patterns, 2023:** these list "disguised advertisement", which supports strict labelling.
- **ASCI codes:** influencer and AI-generated content disclosure.
- **Promotion and Regulation of Online Gaming Act 2025:** bans advertising of online money games. This is a hard block in the India jurisdiction profile.
- **Stablecoins:** the regulatory position is uncertain. Stablecoin settlement is off by default for India-based nodes, and INR settlement uses regulated rails.

### 19.5 Other jurisdictions (brief)

- **Brazil (ECA Digital, 2025):** profiling-based ads to children prohibited.
- **China (PIPL Art. 24):** a non-personalised option is required, which contextual matching satisfies.
- **Canada and Australia:** privacy reform bills are pending.

### 19.6 Jurisdiction policy profiles

Federated Ads carries legal variation as **machine-readable profiles**: `jp:eu`, `jp:eu-political`, `jp:uk`, `jp:us-<state>`, `jp:in`, `jp:br` and others. Each profile defines:
- blocked and allowed categories;
- required labels and disclosures;
- targeting limits;
- age gating;
- archive retention periods;
- advertiser licence attestations required, e.g. a financial-promotion approval reference.

Nodes declare which profiles they enforce. Creatives carry category tags and signed advertiser attestations.

### 19.7 Payments

| Area | Consideration |
|---|---|
| **Holding funds** | Generally requires licensing: EU payment or e-money licences; US money-transmitter rules, with the narrow FinCEN payment-processor exemption |
| **Stablecoins** | EU MiCA (stablecoin rules applying since June 2024); the US GENIUS Act (signed July 2025, rules in progress) |
| **Compliance checks** | KYC, KYB, sanctions screening and the crypto Travel Rule apply to whoever onboards advertisers or moves money |
| **Tax** | Cross-border ad services are typically taxed through reverse-charge VAT or GST, e.g. India's 18% GST on imported digital services. India's equalisation levy on online advertising was abolished in 2025 |

### 19.8 Competition law

Standard-setting is generally lawful under the EU's 2023 Horizontal Guidelines when four conditions hold:
- participation is unrestricted;
- the procedure is transparent;
- compliance is voluntary;
- access is effective.

Exchanging price information has no safe harbour. Federated Ads governance therefore:
- adopts antitrust guidelines;
- publishes agendas and minutes;
- never shares forward-looking or node-level pricing through project channels;
- leaves price indices to independent parties under the constraints in [§6.4](#64-price-discovery).

---

# Part IV: Making it real

## 20. Economics: a worked example

> All numbers in this section are **hypothetical assumptions** chosen to illustrate the fee structure, not market data or forecasts.

**Scenario.** A regional advertiser spends **$5,000** through a hosted buying node across:
- 60 newsletters (flat-fee sponsorships);
- 30 fediverse and community instances (CPM);
- 20 independent websites (CPM).

### 20.1 Fee stack (illustrative)

| Layer | Assumed fee | Amount | Notes |
|---|---|---|---|
| Hosted buying node | 6% | $300 | Campaign tools, creative hosting, consolidated invoicing |
| Relay (discovery and curation) | 0–3% (assume 2% on half the spend) | $50 | Optional; declared in deals |
| Payment processing | ~3% | $150 | Depends on rail; bank transfer is lower |
| Verification (auditor sampling, labelers) | ~1% (assumed across all spend) | $50 | In practice incurred only by deals that require V3 or V4 |
| Hosted selling node or cooperative (for publishers who don't self-host) | 0–8% (assume 5% on 60% of spend) | $150 | Self-hosting publishers pay infrastructure costs instead |
| **Total intermediation** | **~14%** | **$700** | Every line declared in signed deals |
| **Publisher net** | **~86%** | **$4,300** | Compare with ISBA/PwC's 65% (2023 study; 57% restated for 2020, originally reported as 51%) [1][2] |

### 20.2 What this does and does not show

- **The structural point** is that every fee is declared and verifiable. The "unknown delta" cannot exist, because no unsigned hop exists.
- **Contextual inventory without identifiers is likely to sell at lower CPMs** than identity-based inventory in today's market ([§20.3](#203-the-evidence-on-revenue-without-tracking)). Publishers' gains come from a larger *share* and from the levers in [§20.4](#204-improving-publisher-revenue), not from a higher price per impression. The net effect is an empirical question for the pilot ([§24](#24-roadmap-and-success-metrics)).
- **Verification has a cost.** V3 and V4 add cost, so they suit larger deals. Small deals use V0–V2 with prepaid settlement.
- **Node operating costs** are modest under the pointer tier. The selling node serves cached assets alongside its own content. Logs are static, cacheable tiles. The heavier costs are media bandwidth for audio and video and operating a public HTTP endpoint securely. Hosted cooperatives exist to spread those costs.

### 20.3 The evidence on revenue without tracking

Reviewers will rightly ask what publishers lose by giving up cross-site tracking. The evidence points in different directions, and we present it side by side.

| Study | Finding | Notes |
|---|---|---|
| Gu, Johnson & Kobayashi, *PNAS* (2026) [51] | In a regulator-overseen Chrome field experiment (over 200 million impressions, over 5,000 publishers), removing third-party cookies cut publisher revenue by **29.1%**, and by **66% in the EU**. Privacy Sandbox recovered only **4.2%**. | The strongest and most recent evidence. Measures today's programmatic market, where buyers are built around identifiers. |
| Ravichandran & Korula, Google (2019) [50] | Top publishers lost **52%** of revenue on average without cookies. | Company study by the largest ad seller. |
| Johnson, Shriver & Du, *Marketing Science* (2020) [53] | Impressions from users who opted out of tracking sold for about **52% less**. | Peer-reviewed. Opted-out users may differ from others. |
| Laub, Miller & Skiera (2024) [52] | Prices for untrackable users fall **18–23%**, and **premium, niche and smaller publishers lose less**. | Directly relevant to the segment Federated Ads targets first. |
| UK CMA market study (2020) [85] | On Google's data, UK publishers earned around 70% less revenue from non-personalised ads. | Based on data from the largest ad seller. |
| Marotta, Abhishek & Acquisti, WEIS (2019) [49] | Cookies raised publisher revenue by only about **4%** per ad. | Suggests much of the value of tracking goes to intermediaries. |
| NPO / Ster, Netherlands (2020) [54] | After moving to contextual-only ads, the public broadcaster reported revenue up 61% and 76% year on year in two months. | Self-reported, not peer-reviewed, and from a large publisher with unusual inventory. A case study only. |
| European Commission study (2023) [58]; Germanwatch (2025) [55] | Little independent evidence that tracking-based models outperform non-tracking ones; contextual advertising has strong potential if "contextual" is defined narrowly. | Policy research. |

**What we conclude.** In today's market, publishers who drop identifiers should expect lower prices per impression, plausibly in the range of 20–30% for the kind of publishers Federated Ads targets, and more for large general-interest sites. Federated Ads does not pretend otherwise. Its case rests on three things: a much larger share of each advertiser dollar reaching the publisher ([§20.1](#201-fee-stack-illustrative)); revenue levers that do not need tracking ([§20.4](#204-improving-publisher-revenue)); and the fact that identity-based revenue is itself shrinking under regulation, browser changes and ad blocking ([§1](#1-the-problem)).

### 20.4 Improving publisher revenue

Federated Ads cannot make the price effect in [§20.3](#203-the-evidence-on-revenue-without-tracking) disappear. It gives publishers several levers that do not depend on tracking. The evidence behind them varies a lot in strength, and we say which is which.

**Keep more of each dollar.** The 2023 ISBA/PwC study found publishers received about 65% of programmatic spend [2]. In Federated Ads every fee is declared in the signed Deal. If a publisher's share rises from 65% to 80–86%, its revenue rises 23–32% at the same advertiser spend. At a 65% share, each percentage point of intermediary fee removed adds about 1.5% to publisher revenue. This is the largest and best-evidenced lever, but it only works if buyers bring their spend.

**Sell formats that already command a premium.** Host-read podcast ads are listed at roughly $24–26 CPM, against $12–15 for programmatic audio [83]. Newsletter sponsorships typically price at $15–30 per thousand opens [84]. Under Federated Ads, opens are informational only, so such deals would be priced per `send` or as `flat`. These formats are contextual by nature and already sold direct. The protocol lowers the cost of selling them: standard deals, Standing Offers that many advertisers can claim, and verifiable delivery.

**Show fewer, better ads.** Long-run experiments show that ad load drives audiences away more than short tests suggest:
- On Pandora, each extra ad per hour cut listening by about 2%, and the long-run effect was three times the short-run effect [67].
- Google halved the ad load on mobile search, with long-term neutral or positive business impact [66].
- Annoying ads impose a measurable cost on users [68].
- Users who stop seeing ads read 21–43% more articles [69].

Buyers increasingly measure clutter and the ratio of ads to content [4]. Selling nodes can declare ad density in their Inventory ([§6.1](#61-inventory-and-rate-cards)), and buyers can pay more for low-clutter placements.

**Price attention where it can be measured without identity.** The IAB and MRC *Attention Measurement Guidelines* (November 2025) accept time-in-view signals and state that attention measurement does not require identifying anyone [65]. Federated Ads adds an optional `cpvh` pricing model (cost per viewable hour). The open measurement module computes it, and it appears only in aggregate receipts. We have found no independent evidence yet that attention pricing raises publisher revenue, so it is offered as an option, not a promise.

**Prove quality.** Advertisers are concentrating spend on inventory that is verified, viewable, free of fraud and not made-for-advertising:
- In late 2025, private deals made up over 92% of median programmatic spend in the ANA benchmark [4].
- Most of the largest made-for-advertising sites lost almost all their volume within 18 months of the ANA's 2023 study [71].

Verification levels, signed labeler attestations and declared ad density let small publishers show the same quality signals that today only large publishers can afford.

**Use first-party context, not cross-site profiles.** A selling node may offer cohorts built from its own users' opt-in data. Each cohort is labelled with standard taxonomy IDs, following the IAB Tech Lab's Curated Audiences approach [74], and is never smaller than the receipt threshold (k = 50). Matching ads to content raises purchase intent, unless the format is obtrusive [72]. Research also finds that contextual signals recover only part of the click-through value of behavioural targeting. The same research found that ad-network revenue can be highest when behavioural targeting is not allowed, because more buyers compete for each impression [73].

**Sell together.** Cooperatives such as Ozone in the UK, Wemass in Spain and the Local Media Consortium in the US show that publishers can pool their sales [75][76][77]. Public evidence on how this affects yield is thin. Federated Ads provides a cooperative selling-node profile (`profile:coop`):
- a signed member list;
- a declared revenue split for each member;
- receipts for each member;
- competition-law guardrails, so members never exchange prices ([§19.8](#198-competition-law)).

**Do not rely on ads alone.** The Guardian earned £126 million in digital reader revenue in 2025/26 from 1.4 million recurring supporters [78], but most publishers will not match that. Where sites have asked users to either pay or accept tracking, only about 1% paid [79]. Shared passes such as contentpass show another route: one subscription, ad-free across hundreds of sites [80]. Each selling node can advertise subscription, contribution and ad-free options through a standard endpoint. A cooperative ad-free pass can be proven with Privacy Pass tokens, without identifying the reader.

| Lever | Protocol support | Evidence | Indicative effect on publisher revenue |
|---|---|---|---|
| Higher fee share | Fees declared in signed Deals | Audits [1][2][4] | +23% to +32% against a 65% share |
| Premium formats | `sponsorship`, `flat`, `cpad`; Standing Offers | Rate cards [83][84] (vendor-published) | About 1.6–2.2× programmatic CPM |
| Lower ad density | Inventory `adDensity`, `adsPerHour`, `saturationLimit` | [66][67][68][69] (peer-reviewed or field experiments) | Short-run revenue may fall; long-run retention gain (size unknown) |
| Attention pricing | `cpvh`; viewable seconds in receipts | Standard [65]; outcome data vendor-only | Unknown |
| Verified quality | V0–V4; labeler attestations | [4][71] | Keeps spend; premium unproven |
| First-party cohorts | Seller cohorts, k ≥ 50 | [72][73][74] | Partial recovery |
| Cooperatives | `profile:coop` | [75][76][77] | Unknown |
| Reader revenue | Support-options endpoint; ad-free tokens | [78][79][80] | Highly variable |

*All effects are indicative and derived from the cited sources. They are not additive and will be tested in the pilot.*

**Can these levers close the gap?** It depends on the publisher.

- **Independent web publishers:** plausibly yes, but mainly through one lever. Fee recapture is the only one with evidence of the right size. Combining the PNAS revenue loss (−29%) with a share rise from 65% to 86% leaves publishers about 6% worse off. Using the smaller loss Laub et al. found for niche publishers (−18% to −23%) leaves them about 2–8% better off. Both results assume buyers actually move spend to Federated Ads at contextual prices. **Demand, not price, is the dominant risk.**
- **Newsletters and podcasts:** the gap barely applies, because they are already sold contextually and direct. The protocol mainly lowers their cost of sales and opens them to Standing Offers.
- **Fediverse and community instances:** they have no advertising revenue today, so anything is upside. Community norms will cap ad density, and the protocol encodes those caps instead of fighting them.

**What remains uncertain:**
- Whether contextual prices rise if tracking becomes scarce across the whole market. Advocates argue they would [86], but the field experiments measured cookieless traffic competing against tracked traffic, so they cannot answer this.
- Whether attention pricing benefits sellers.
- How cooperatives affect yield.
- How many people pay for ad-free options when the free tier is already untracked.
- Whether verification costs eat the fee gain on small deals.

### 20.5 Where value comes from for each side

| Party | Value |
|---|---|
| **Publishers** | Higher share; direct relationships; choice of intermediaries; standard tooling instead of manual sponsorship sales |
| **Advertisers** | Creative control and fast revocation; brand-safe, contextual, community placements; full fee transparency; regulatory comfort (no profiling, ready-made disclosures) |
| **Users** | Non-tracking ads; real explanations; opt-outs that work; an ad-free option |
| **Intermediaries** | A legitimate role competing on service (curation, credit, tooling, verification), not on information asymmetry |

---

## 21. Comparison with existing systems

| | **Federated Ads** | **OpenRTB + Prebid** | **Brave Ads** | **EthicalAds / Carbon** | **Newsletter marketplaces** | **AI-assistant ads (e.g. ChatGPT)** |
|---|---|---|---|---|---|---|
| Open protocol | Yes | Yes (OpenRTB); open source (Prebid) | No | No | No | No |
| Federated / multi-operator | Yes | Multi-vendor, but concentrated | Single operator | Single operator each | Single operator each | Single operator |
| Tracking-free by default | Yes | No | Yes (on-device) | Yes | Mostly | Self-declared |
| Advertiser creative revocation | Protocol-level, provable | No standard | Operator-controlled | Operator-controlled | Manual | Operator-controlled |
| Verifiable delivery | Signed, witnessed logs + optional attestation | Third-party verification vendors | Anonymous tokens | Operator reports | Publisher reports | Operator reports |
| Fee transparency | Declared in signed deals | Partial (schain, studies) | Operator-set | Published rev share | Varies | Opaque |
| Surfaces | Web, social, email, audio, AI | Web, app, CTV, audio | Browser | Web | Email | AI chat |
| Cross-publisher frequency | No (by design) | Yes (with identifiers) | On-device | No | No | Within platform |

---

## 22. Adoption strategy

Two-sided networks fail when they try to launch everywhere at once. Federated Ads starts narrow.

### 22.1 The first niche

Start where the pain is highest and identity matters least:

1. **Newsletters and podcasts.** Already sold as flat-fee sponsorships, already contextual, and today run by email and spreadsheet. Federated Ads gives them standard deals, verifiable delivery and simple payment.
2. **Developer, open-source and technical sites.** EthicalAds has shown tracking-free demand exists here [19].
3. **Fediverse and community instances that opt in.** These come with community governance: users vote, revenue is shared, and the instance publishes its policy.

### 22.2 Seeding demand

- **Values-aligned anchor advertisers:** privacy-focused software companies, developer tools, open-source sponsors, non-profits.
- **Sponsorship pools:** sponsors fund open-source or public-interest communities through Federated Ads deals.
- **House and cross-promotion ads** between participating publishers, so inventory is never empty.
- **The OpenRTB bridge,** for modest additional demand.

### 22.3 Making adoption cheap

- A reference **selling node** that runs on a small server, plus a **hosted cooperative** option.
- **Plugins** for popular publishing tools (WordPress, Ghost), newsletter platforms, podcast hosts and fediverse server software.
- A **self-serve buying tool** for small advertisers.
- Libraries for signing, logs and canonicalisation in several languages.

### 22.4 The email lesson

DKIM and DMARC spread fastest once major receivers required them of bulk senders. Federated Ads needs a small number of important participants, such as a large cooperative, a podcast host or a well-known advertiser, who **require** signed, logged receipts from their counterparties.

---

## 23. Governance, IPR and funding

### 23.1 What the "Federated Ads Initiative" is today

Today the initiative is **two individual contributors, Suneesh Rajan and Arjun Krishna, working with an AI assistant**. It has no legal entity, no members and no funding. We say so plainly because a standards effort must earn trust by being transparent about its origins. The governance below describes how that changes.

### 23.2 Phases

| Phase | Trigger | Structure |
|---|---|---|
| **1. Community incubation** (now) | Publication of this paper | Public repository and issue tracker; a FEP-style proposal process (proposal → discussion → editor's draft → last call); named editors; open calls with published notes; an individual Internet-Draft for IETF feedback via DISPATCH; a **W3C Community Group** for incubation once at least five supporters, most from outside the project, commit to take part |
| **2. Standards track** | Two or three independent interoperable implementations | Seek formal standardisation: IETF working-group adoption (or a BoF) for the wire protocol and/or a W3C Working Group for the vocabulary and profiles. Liaison with the W3C Private Advertising Technology groups (PATCG/PATWG) and IAB Tech Lab. A v1.0 core candidate. |
| **3. Neutral home** | Material adoption; need to hold trademarks or fund the conformance suite | An independent non-profit, or a project under an existing open-source foundation, with a multi-stakeholder board: publishers, advertisers, implementers and civil society, **with no single company holding a majority** |

### 23.3 Change control

- **Two independent interoperable implementations** before any feature is marked stable.
- **At least 90 days' notice** for breaking changes, with a migration path.
- Every decision is recorded in public with its rationale.
- Each working group includes publisher, advertiser and user-advocacy participants.

### 23.4 Intellectual property

- **Specification text:** CC BY 4.0 while incubated in this repository. **Code:** Apache-2.0.
- **Before a Community Group exists,** contributors make a royalty-free patent commitment modelled on the W3C Community Contributor License Agreement.
- **Once a Community Group is formed,** specification contributions are made under the W3C CLA and published under the licences in the W3C Community Group licence file, and the Final Specification Agreement applies to final reports. Text written before the group remains available under CC BY 4.0. Reference implementations developed outside the group stay Apache-2.0.
- **Internet-Draft text** is subject to the IETF Trust Legal Provisions and the IPR disclosure rules of BCP 78 and BCP 79.
- **Trademark:** the name will be held for the community, not for any company. Before public launch, a trademark search will be done on the name "Federated Ads Protocol".

### 23.5 Funding

- **Early funding** should come from public-interest technology grants and in-kind contributions from implementers.
- **Later:** capped implementer membership dues and conformance-testing fees, with caps so that no funder gains control.
- **The foundation must not operate critical network infrastructure.** Relays, labelers and witnesses are run by independent parties, so the network survives a funding gap. Matrix's funding difficulties are the cautionary example [33].

---

## 24. Roadmap and success metrics

| Milestone | Deliverables |
|---|---|
| **M0: Whitepaper v0.3** (this document) | Public comment; outreach to W3C, IETF, IAB Tech Lab and civil society |
| **M1: Internet-Draft -00 and schemas** | `draft-rajan-federated-ads-protocol-00`; JSON Schemas; test vectors; taxonomy mapping v0.1 |
| **M2: Reference implementation** | Selling node, buying node and creative host; log and witness tooling; WordPress/Ghost plugin; a fediverse integration; conformance suite |
| **M3: Pilot** | 50+ publishers (newsletters, podcasts, technical sites, opt-in instances) and 10+ advertisers on `settle:invoice` / `settle:prepaid` |
| **M4: Bridges and profiles** | OpenRTB and VAST bridges; audio profile; AI-surface pilot with at least one assistant provider; agent binding |
| **M5: Standards track** | Second independent implementation; v1.0 candidate; IETF or W3C working-group adoption sought |

**Pilot success metrics (M3):**

| Metric | Target |
|---|---|
| Independent interoperating implementations | ≥ 2 |
| Publisher net share of advertiser spend | ≥ 80% |
| Revocation: post-deadline billable impressions | 0 |
| Revocation acknowledgement latency (p99) | ≤ 60 s for pointer-tier licences |
| Disputed spend | < 2% |
| Receipt batches with valid witnessed inclusion | 100% |
| Publishers and advertisers retained after 3 months | ≥ 70% |

---

## 25. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Cold start**: too little demand or supply | High | High | Narrow first niche; anchor advertisers; sponsorship pools; house ads; bridge |
| **Adverse selection**: premium publishers stay with direct sales, low-quality supply joins | Medium | High | Labelers; verification levels; curation by relays and cooperatives; start with high-quality niches |
| **Lower contextual CPMs** | Medium | Medium | Higher publisher share; lower fees; brand-safety and compliance premium; honest positioning |
| **Relay centralisation**: one dominant relay | Medium | Medium | Multi-homing; portable reputation and deal history; declared fees; norms on fee caps |
| **Verification seen as insufficient by agencies** | High (early) | Medium | V3/V4; work with auditors; align with MRC definitions; target direct-buying advertisers first |
| **Regulatory change** | Medium | Medium | Jurisdiction profiles; regulatory watch; privacy-maximal default |
| **Governance capture** | Low (early) to medium | High | Phased neutral governance; no majority holder; public process |
| **Maintainer concentration** | Medium (two maintainers since October 2026) | High | Recruit co-editors from other organisations and implementers before M2; keep everything public |
| **Name and trademark** | Medium | Medium | Renamed from "OpenAds"; trademark search before launch |
| **Security incident in reference code** | Medium | High | Security review before pilot; safe defaults; disclosure policy |

---

## 26. Open questions

1. **Attesters.** Who should issue client-attestation tokens without recreating platform dependency? Could cooperatives or browser vendors play this role?
2. **On-device profile.** Which clients will implement it? Should Federated Ads define its own catalogue format or align with an existing design (e.g. Brave's)?
3. **Dispute resolution.** Is arbitration by an auditor named in the deal enough, or is a standing panel needed? What evidence decides a case?
4. **AI agents.** Should agents be allowed to *act on* sponsored offers at all, or only display them?
5. **Revocation and archives.** Exactly which record-retention duties apply to small nodes in each jurisdiction?
6. **Taxonomy governance.** Who maintains the "sensitive versus unsafe" distinction, and how are disputes resolved?
7. **Small advertisers.** Can a local business buy through a hosted buying node without recentralising the network?
8. **Price discovery.** Will posted prices plus Standing Offers converge on fair prices? Are independent price indices needed?
9. **Agency acceptance.** What would large agencies need before accepting V3/V4 verification in place of incumbent vendors?
10. **C2PA.** Should Federated Ads define a C2PA assertion for licences and revocation status?
11. **Measurement module.** Who maintains and audits the open-source viewability module?
12. **Funding.** Which funders can support early stewardship without compromising neutrality?

---

## 27. Frequently asked questions

**Is this a blockchain or crypto project?**
No. Federated Ads uses ordinary signatures and Merkle logs, the same technology as Certificate Transparency. Stablecoin settlement is one optional payment profile among several.

**Does Federated Ads replace OpenRTB or Prebid?**
No. It is a different model, based on deals and federation, for parties who want it. A bridge lets existing buyers participate.

**Does Federated Ads track users?**
No. Matching is contextual. Receipts are aggregated. Cross-site identifiers are prohibited in protocol messages.

**Can large companies participate?**
Yes, as nodes on equal terms. Governance prevents any single company from controlling the standard.

**Is this related to "federated learning"?**
No. Some advertising research uses "federated" to mean federated machine learning, where models are trained across devices or servers (for example AdFL, 2026 [91]). Here "federated" means independent servers interoperating through an open protocol, as email and ActivityPub do.

**Who runs Federated Ads?**
Nobody runs "the network". Independent operators run nodes. The initiative maintains the specification only.

**How is this different from The Trade Desk's OpenAds?**
It is unrelated. That product is a header-bidding wrapper. Federated Ads is a federated protocol for deals, licences, revocation and receipts.

**How does it relate to AdCP and IAB Tech Lab's agentic protocols?**
They are complementary. Agent protocols describe how software agents plan and buy. Federated Ads can be the federated identity, licence and receipt layer underneath.

**What about video and connected TV?**
Deferred to v2. A VAST bridge offers a partial path in v1.

**Why would an advertiser accept less precise targeting?**
For creative control, brand-safe community placements, transparent fees, verifiable delivery and lower regulatory risk. Contextual targeting is also improving quickly with content classification.

---

## 28. AI-assistance disclosure

This whitepaper was **authored with Claude**, an AI model developed by Anthropic.

- **Human direction.** Suneesh Rajan initiated the project. In a structured requirements interview, he decided the federation model, tiered creative licensing and revocation, rail-agnostic settlement, signed-receipt measurement, the end-user rights, the v1 surfaces, the governance approach, the authorship form and the rename. He is accountable for the contents.
- **AI contribution.**
  - Claude proposed alternatives and trade-offs, drafted the text, tables, diagrams and example protocol objects, and made recommendations where asked.
  - For version 0.2, Claude coordinated AI research agents that searched the web for industry data, prior art, technical standards and regulation, and a separate agent that red-teamed version 0.1 from seven expert perspectives.
  - Their findings were incorporated with citations.
  - For version 0.3, further AI research agents searched for similar papers and proposals and for evidence on publisher revenue. Search limits meant some requested sources could not be checked; those were left out rather than cited unverified.
- **Verification.** AI-assisted research can be wrong. Figures and legal points are cited to sources, and items resting only on secondary sources are flagged as such or omitted. Readers should check primary sources before relying on any figure, legal statement or standard reference. Example protocol objects are illustrative and non-normative.
- **Contributors.** Arjun Krishna joined as a contributor after version 0.3 was published and has since contributed corrections, including to the offer, deal and dispute state machines, the HTML5 creative policy and the Internet-Draft. The design decisions and drafting described above were made before they joined.
- **Why we disclose this.** A proposed open standard should be open about how it was made.

---

## Appendix A. Glossary

| Term | Meaning |
|---|---|
| **Node** | A server that speaks Federated Ads in one or more roles |
| **Deal** | Agreed terms between a buying and a selling node, signed by both |
| **Standing Offer** | A campaign that any eligible seller may claim a slice of |
| **Creative Manifest** | A signed description of a creative's assets and metadata |
| **Licence** | A time-limited, scoped, revocable right to display a creative |
| **Revocation / acknowledgement** | A signed withdrawal of a licence, and the receiver's signed proof of receipt |
| **Receipt Batch** | A signed set of aggregated delivery cells committed to a log |
| **Transparency log** | An append-only Merkle log whose checkpoints are cosigned by witnesses |
| **Witness** | An independent party that cosigns log checkpoints after checking consistency |
| **Labeler** | An independent service publishing signed judgements (brand safety, fraud, identity) |
| **Verification level (V0–V4)** | The evidence a deal requires for billing |
| **Jurisdiction profile** | Machine-readable legal rules for a jurisdiction |
| **Surface profile** | Rendering, labelling and measurement rules for a medium |
| **Bridge** | A node translating between Federated Ads and a legacy protocol |

---

## Appendix B. References

*Industry and market data*

1. ISBA & PwC, *Programmatic Supply Chain Transparency Study* (2020). Summary: https://www.thedrum.com/news/2020/05/06/big-hole-the-value-chain-one-third-adtech-costs-unattributable-finds-isba
2. ISBA & PwC, *Programmatic Supply Chain Transparency Study II* (January 2023). https://www.isba.org.uk/system/files/media/documents/2023-01/ISBA%20%20PwC%20programmatic%20supply%20chain%20study%20II%20(summary)-%2018%20January%202023.pdf
3. ANA, *Programmatic Media Supply Chain Transparency Study* (December 2023). https://www.ana.net/
4. ANA / TAG TrustNet, *Programmatic Transparency Benchmark*, Q4 2025 (February 2026). https://www.ana.net/content/show/id/pr-2026-02-programatic
5. IAB & PwC, *Internet Advertising Revenue Report, Full Year 2025* (April 2026). https://www.iab.com/wp-content/uploads/2026/04/IAB_PwC_Internet_Ad_Revenue_Report_Full_Year_2025_April_2026.pdf
6. WPP Media, *This Year Next Year, 2026 Midyear Forecast* (June 2026). https://www.wppmedia.com/news/report-this-year-next-year-midyear-2026
7. *United States v. Google LLC* (E.D. Va.), liability opinion 17 April 2025; remedies decision September 2026. Coverage: https://www.adexchanger.com/antitrust/google-wont-have-to-break-up-its-ad-tech-business-judge-brinkema-rules/
8. European Commission, Case AT.40670 (Google adtech), decision of 5 September 2025. Coverage: https://www.cnbc.com/2025/09/05/google-slapped-by-eu-with-3point45-billion-antitrust-fine.html
9. Competition Bureau Canada, application against Google (November 2024). https://www.canada.ca/en/competition-bureau/news/2024/11/competition-bureau-sues-google-for-anti-competitive-conduct-in-online-advertising-in-canada.html
10. Google, "Update on plans for Privacy Sandbox technologies" (17 October 2025). https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies
11. eyeo, *2026 Ad Blocking Report* (May 2026). https://eyeo.com/wp-content/uploads/2026/05/eyeo_2026-ad-blocking-report.pdf
12. Juniper Research ad fraud estimate (September 2023). Coverage: https://www.mediapost.com/publications/article/389594/22-of-all-digital-ad-spend-30-of-mobile-lost-to.html
13. OpenAI, "Our approach to advertising and expanding access" (January 2026). https://openai.com/index/our-approach-to-advertising-and-expanding-access/
14. Campaign, "Perplexity pulls plug on ads citing trust concerns" (2026). https://www.campaignlive.com/article/perplexity-pulls-plug-ads-citing-trust-concerns-ai/1949142
15. IAB & PwC, US podcast advertising revenue 2025 (April 2026). Coverage: https://radioink.com/2026/04/16/iab-digital-audio-grew-10-in-2025-as-podcasts-near-3b/
16. Mastodon. https://joinmastodon.org/
17. TechCrunch, interview with Bluesky CEO Jay Graber (December 2024). https://techcrunch.com/2024/12/05/bluesky-ceo-jay-graber-is-reshaping-social-media-but-advertising-isnt-off-the-table
18. Brave, "100M monthly active users" (October 2025). https://brave.com/blog/100m-mau/
19. EthicalAds newsletter (July 2026). https://www.ethicalads.io/blog/2026/07/ethicalads-newsletter-july-2026/

*Prior art and standards bodies*

20. IAB Tech Lab, ads.cert. https://iabtechlab.com/ads-cert/
21. BidSwitch, "OpenRTB 3.0: what is it and why is almost nobody using it yet" (2024). https://blog.bidswitch.com/openrtb-3.0-what-is-it-and-why-is-almost-nobody-using-it-yet
22. AdExchanger, "Prebid.org is at a crossroads" (October 2025). https://www.adexchanger.com/publishers/prebid-org-is-at-a-crossroads-and-must-now-decide-whose-interests-it-serves/
23. The Trade Desk, OpenAds announcement (2025). https://www.thetradedesk.com/press-room/the-trade-desk-execs-share-new-details-about-how-sell-side-solution-openads-will-work
24. W3C PAT WG, *Attribution Level 1* (Working Draft). https://www.w3.org/TR/attribution/
25. W3C, *Global Privacy Control* (Working Draft). https://www.w3.org/TR/gpc/
26. W3C Tracking Protection Working Group (closed 2019). https://www.w3.org/2011/tracking-protection/
27. Coil. https://coil.com/
28. AgenticAdvertising.org, Ad Context Protocol (AdCP). https://adcontextprotocol.org/
29. IAB Tech Lab, Agentic advertising standards. https://iabtechlab.com/standards/agentic-advertising-and-ai/
30. Fediverse Enhancement Proposals. https://codeberg.org/fediverse/fep
31. AT Protocol, Labels specification. https://atproto.com/specs/label
32. Mastodon 4.7 release notes (August 2026). https://blog.joinmastodon.org/2026/08/mastodon-4.7/
33. Matrix.org Foundation, "The Matrix.org Foundation at a crossroads" (February 2025). https://matrix.org/blog/2025/02/crossroads/
34. C2PA Specifications. https://spec.c2pa.org/specifications/specifications/2.4/index.html
35. Media Rating Council, *Viewable Ad Impression Measurement Guidelines*. https://www.mediaratingcouncil.org/sites/default/files/Standards/081815%20Viewable%20Ad%20Impression%20Guideline_v2.0_Final.pdf
36. IAB Tech Lab, *Podcast Measurement Technical Guidelines v2.2* (2024). https://iabtechlab.com/wp-content/uploads/2024/02/PodcastMeasurement_v2.2_final.pdf

*Related research and proposals (added in v0.3)*

37. V. Toubiana, A. Narayanan, D. Boneh, H. Nissenbaum, S. Barocas, "Adnostic: Privacy Preserving Targeted Advertising," NDSS 2010. https://www.ndss-symposium.org/ndss2010/adnostic-privacy-preserving-targeted-advertising/
38. S. Guha, B. Cheng, P. Francis, "Privad: Practical Privacy in Online Advertising," USENIX NSDI 2011. https://www.usenix.org/conference/nsdi11/privad-practical-privacy-online-advertising
39. M. Backes, A. Kate, M. Maffei, K. Pecina, "ObliviAd: Provably Secure and Practical Online Behavioral Advertising," IEEE S&P 2012. https://www.ieee-security.org/TC/SP2012/papers/4681a257.pdf
40. G. Pestana, I. Querejeta-Azurmendi, P. Papadopoulos, B. Livshits, "THEMIS: A Decentralized Privacy-Preserving Ad Platform with Reporting Integrity," arXiv:2106.01940 (2021). https://arxiv.org/abs/2106.01940
41. MediaPost, "Are Bluesky Feeds The Future Of Decentralized Media Advertising?" (23 April 2025). https://www.mediapost.com/publications/article/405169/are-bluesky-feeds-the-future-of-decentralized-medi.html
42. Nostr NIPs, pull request #955, "NOSTR Decentralized Advertising Network (NOSTR-DAN)" (December 2023). https://github.com/nostr-protocol/nips/pull/955
43. NostrGameEngine, nostrads. https://github.com/NostrGameEngine/nostrads
44. R. Chairattana-Apirom, S. Tessaro, N. Tyagi, "Fraud Mitigation in Privacy-Preserving Attribution," IACR ePrint 2025/1891. https://eprint.iacr.org/2025/1891
45. M. Thomson, "DAP Extensions for the Attribution API," draft-thomson-ppm-dap-attribution-01 (2026). https://datatracker.ietf.org/doc/html/draft-thomson-ppm-dap-attribution-01
46. M. Goldin, A. Soleimani, J. Young, "The AdChain Registry" (May 2017); MetaX, "Learnings from launching the first token-curated registry." https://medium.com/metax-publication/learnings-from-metax-on-launching-the-first-token-curated-registry-c30140d5052c
47. Kochava, "Kochava introduces first blockchain-based digital advertising platform" (2017). https://www.kochava.com/blog/kochava-introduces-first-blockchain-based-digital-advertising-platform/
48. Brave Software, "Basic Attention Token (BAT): Blockchain Based Digital Advertising" (2017). https://basicattentiontoken.org/static-assets/documents/BasicAttentionTokenWhitePaper-4.pdf
49. V. Marotta, V. Abhishek, A. Acquisti, "Online Tracking and Publishers' Revenues: An Empirical Analysis," WEIS 2019. https://weis2019.econinfosec.org/wp-content/uploads/sites/6/2019/05/WEIS_2019_paper_38.pdf
50. D. Ravichandran, N. Korula, "Effect of disabling third-party cookies on publisher revenue," Google (2019). https://services.google.com/fh/files/misc/disabling_third-party_cookies_publisher_revenue.pdf
51. Z. Gu, G. A. Johnson, S. J. Kobayashi, "Can privacy technologies replace cookies? Ad revenue in a field experiment," PNAS 123(19) (May 2026). https://www.pnas.org/doi/10.1073/pnas.2603752123
52. R. Laub, K. M. Miller, B. Skiera, "The Economic Value of User Tracking for Publishers," arXiv:2303.10906 (2024). https://arxiv.org/abs/2303.10906
53. G. A. Johnson, S. K. Shriver, S. Du, "Consumer Privacy Choice in Online Advertising: Who Opts Out and at What Cost to Industry?" Marketing Science 39(1) (2020). https://pubsonline.informs.org/doi/10.1287/mksc.2019.1198
54. Nieman Lab, "A Dutch public broadcaster got rid of targeted digital ads, and its revenues went way up" (2020). https://www.niemanlab.org/reading/a-dutch-public-broadcaster-got-rid-of-targeted-digital-ads-and-its-revenues-went-way-up/
55. J. Graf, L. Probst, L. Steltzner, L. Wellmer, "The Potential of Contextual Advertising Compared with Tracking-based Personalised Advertising," Germanwatch (August 2025). https://www.germanwatch.org/en/93232
56. K. Iwańska, "To Track or Not to Track? Towards privacy-friendly and sustainable online advertising," Panoptykon Foundation (November 2020). https://panoptykon.org/sites/default/files/publikacje/panoptykon_to_track_or_not_to_track_final.pdf
57. Norwegian Consumer Council (Forbrukerrådet), "Time to Ban Surveillance-Based Advertising" (June 2021). https://storage02.forbrukerradet.no/media/2021/06/20210622-final-report-time-to-ban-surveillance-based-advertising.pdf
58. European Commission, "Study on the impact of recent developments in digital advertising on privacy, publishers and advertisers" (January 2023). https://op.europa.eu/en/publication-detail/-/publication/8b950a43-a141-11ed-b508-01aa75ed71a1/language-en
59. European Parliament (IMCO), "Online advertising: the impact of targeted advertising on advertisers, market access and consumer choice" (June 2021). https://www.europarl.europa.eu/RegData/etudes/STUD/2021/662913/IPOL_STU(2021)662913_EN.pdf
60. EFF, "Privacy First: A Better Way to Address Online Harms" (November 2023). https://www.eff.org/wp/privacy-first-better-way-address-online-harms
61. J. Qiu, Q. Mei, "Generative AI Advertising as a Problem of Trustworthy Commercial Intervention," arXiv:2605.18673 (2026). https://arxiv.org/abs/2605.18673
62. M. Hajiaghayi, S. Lahaie, K. Rezaei, S. Shin, "Ad Auctions for LLMs via Retrieval Augmented Generation," NeurIPS 2024. https://neurips.cc/virtual/2024/poster/94948
63. K. A. Dubey, Z. Feng, R. Kidambi, A. Mehta, D. Wang, "Auctions with LLM Summaries," KDD 2024. https://arxiv.org/abs/2404.08126
64. P. Dütting, V. Mirrokni, R. Paes Leme, H. Xu, S. Zuo, "Mechanism Design for Large Language Models," WWW 2024. https://dl.acm.org/doi/10.1145/3589334.3645511

*Publisher revenue evidence (added in v0.3)*

65. IAB & Media Rating Council, *Attention Measurement Guidelines*, Version 1.0 (November 2025). https://www.mediaratingcouncil.org/sites/default/files/Standards/IAB_MRC_Attention_Measurement_Guidelines_November_2025.pdf
66. H. Hohnhold, D. O'Brien, D. Tang, "Focusing on the Long-term: It's Good for Users and Business," Proc. KDD (2015). https://doi.org/10.1145/2783258.2788583
67. A. Goli, J. Huang, D. Reiley, N. Riabov, "Measuring Consumer Sensitivity to Audio Advertising: A Long-Run Field Experiment on Pandora Internet Radio," working paper (revised August 2024). https://www.davidreiley.com/papers/PandoraListenerDemandCurve.pdf
68. D. G. Goldstein, R. P. McAfee, S. Suri, "The Cost of Annoying Ads," Proc. WWW (2013). https://doi.org/10.1145/2488388.2488429
69. S. Yan, K. M. Miller, B. Skiera, "How Does the Adoption of Ad Blockers Affect News Consumption?" Journal of Marketing Research (2022). https://doi.org/10.1177/00222437221076160
70. Coalition for Better Ads, "The Initial Better Ads Standards." https://www.betterads.org/standards/
71. Jounce Media, *The State of the Open Internet 2025* (2025). https://jouncemedia.com/build/resources/2025_Jounce_Media_State_Of_The_Open_Internet_2afe364829.pdf
72. A. Goldfarb, C. Tucker, "Online Display Advertising: Targeting and Obtrusiveness," Marketing Science 30(3) (2011). https://doi.org/10.1287/mksc.1100.0583
73. O. Rafieian, H. Yoganarasimhan, "Targeting and Privacy in Mobile Advertising," Marketing Science 40(2) (2021). https://doi.org/10.1287/mksc.2020.1235
74. IAB Tech Lab, "Curated Audiences (formerly Seller Defined Audiences)" (updated August 2025). https://iabtechlab.com/sda/
75. Ozone Project. https://www.ozoneproject.com/
76. Wemass. https://www.wemass.com/
77. Local Media Consortium. https://www.localmediaconsortium.com/
78. Guardian Media Group, "Guardian Media Group publishes 2025/26 statutory accounts" (10 September 2026). https://www.theguardian.com/gnm-press-office/2026/sep/10/guardian-media-group-publishes-202526-statutory-accounts
79. T. Müller-Tribbensee, K. M. Miller, B. Skiera, "Paying for Privacy: Pay-or-Tracking Walls," arXiv:2403.03610 (2024). https://arxiv.org/abs/2403.03610
80. contentpass. https://www.contentpass.net/
81. EthicalAds, Publisher Policy and Advertiser Pricing (2026). https://www.ethicalads.io/publisher-policy/ ; https://www.ethicalads.io/advertisers/pricing/
82. Graze, "Sponsored Posts" documentation. https://www.graze.social/docs/sponsored-posts
83. AdvertiseCast, "Podcast Advertising Rates" (vendor rate card, accessed October 2026). https://www.advertisecast.com/podcast-advertising-rates
84. Passionfroot, "Newsletter Advertising 101: A Brand's Guide" (June 2024). https://www.passionfroot.me/blog/newsletter-advertising-101-a-brands-guide-to-newsletter-ads
85. UK Competition and Markets Authority, *Online platforms and digital advertising: Market study final report* (1 July 2020). https://assets.publishing.service.gov.uk/media/5fa557668fa8f5788db46efc/Final_report_Digital_ALT_TEXT.pdf
86. J. Ryan, A. Toner (ICCL), "The True Cost of RTB" (October 2025). https://www.iccl.ie/digital-data/the-true-cost-of-rtb/
*Other sources (added in v0.3)*

87. Accountable Tech, "Ban Surveillance Advertising" campaign (March 2021). https://accountabletech.org/campaign/ban-surveillance-advertising/
88. U.S. House of Representatives, H.R. 6416, *Banning Surveillance Advertising Act of 2022* (introduced January 2022). https://www.congress.gov/bill/117th-congress/house-bill/6416
89. Google, "How we're increasing transparency for gen AI content with the C2PA" (September 2024). https://blog.google/technology/ai/google-gen-ai-content-transparency-c2pa/
90. Digiday, "OpenAI's ChatGPT ads business hits $1 billion run rate as Europe gets self-serve access" (August 2026). https://digiday.com/media-buying/openais-chatgpt-ads-business-hits-1-billion-run-rate-as-europe-gets-self-serve-access/
91. A. Alemari, S. Sen, C. Borcea, "AdFL: In-Browser Federated Learning for Online Advertisement," arXiv:2602.06336 (February 2026). https://arxiv.org/abs/2602.06336


*Technical specifications*

- RFC 2119 / RFC 8174 (BCP 14), Requirement keywords
- RFC 3339, Timestamps
- RFC 6962 / RFC 9162, Certificate Transparency
- RFC 7033, WebFinger
- RFC 8032, EdDSA
- RFC 8615, Well-Known URIs
- RFC 8785, JSON Canonicalization Scheme
- RFC 9110, HTTP Semantics
- RFC 9421, HTTP Message Signatures
- RFC 9457, Problem Details for HTTP APIs
- RFC 9458, Oblivious HTTP
- RFC 9530, Digest Fields
- RFC 9576 / 9577 / 9578, Privacy Pass
- W3C, Verifiable Credential Data Integrity 1.0; Data Integrity EdDSA Cryptosuites v1.0; Controlled Identifiers 1.0; ActivityPub; WebSub; JSON-LD 1.1
- C2SP, tlog-tiles, tlog-checkpoint, signed-note, tlog-witness. https://c2sp.org/
- IETF, Distributed Aggregation Protocol (draft-ietf-ppm-dap)
- IAB Tech Lab, OpenRTB 2.6, AdCOM, VAST 4.x, Content Taxonomy 3.1, Ad Product Taxonomy 2.0, GPP, ads.txt, sellers.json

*Law and regulation (primary texts should be consulted)*

- Regulation (EU) 2016/679 (GDPR); CJEU C-252/21 *Meta v Bundeskartellamt*; CJEU C-604/22 *IAB Europe*
- EDPB Opinion 08/2024 on consent-or-pay; EDPB Guidelines 2/2023 on the technical scope of Art. 5(3) ePrivacy Directive
- Regulation (EU) 2022/2065 (Digital Services Act); Regulation (EU) 2022/1925 (Digital Markets Act); Regulation (EU) 2024/900 (political advertising); Regulation (EU) 2024/1689 (AI Act); Regulation (EU) 2023/1114 (MiCA)
- European Commission, Guidelines on horizontal co-operation agreements (2023)
- US FTC, Enforcement Policy Statement on Deceptively Formatted Advertisements (2015); Guides Concerning Endorsements and Testimonials (2023); COPPA Rule amendments (2025)
- California AB 566 (2025); GENIUS Act (2025); FinCEN ruling FIN-2014-R012
- India: Digital Personal Data Protection Act 2023 and DPDP Rules 2025; CCPA Guidelines for Prevention and Regulation of Dark Patterns 2023; Promotion and Regulation of Online Gaming Act 2025
- UK: Data (Use and Access) Act 2025; Online Safety Act 2023
- Brazil: Law 15.211/2025 (ECA Digital)

---

## Appendix C. Change history

### After v0.3

- Arjun Krishna added as a contributor; governance ([§23.1](#231-what-the-federated-ads-initiative-is-today)) and risk ([§25](#25-risks-and-mitigations)) updated to reflect two maintainers.

### Changes in v0.3 (5 October 2026)

- **Prior art:** added academic privacy-preserving ad systems, THEMIS, Graze on Bluesky, Nostr ad proposals and privacy-preserving attribution research, plus a cautious statement of what appears to be new.
- **Economics:** new [§20.3](#203-the-evidence-on-revenue-without-tracking) presenting the evidence on revenue without tracking, including the 2026 PNAS field experiment, and new [§20.4](#204-improving-publisher-revenue) on publisher revenue levers.
- **Protocol additions:** Inventory quality signals (ad density, saturation limits), floors and support options; the `cpvh` attention pricing model; the cooperative selling-node profile.
- **AI surfaces:** licensed creatives may not be paraphrased or blended into generated answers by default.
- **FAQ:** clarified that "federated" does not mean federated learning.
- **Problem framing:** added civil-society and policy calls for alternatives to surveillance advertising ([§1.4](#14-surveillance-as-infrastructure-and-the-collapse-of-its-replacement)).
- **Creative provenance:** noted Google's use of C2PA metadata in ad policy ([§7.2](#72-objects)).
- **Governance:** the W3C Community Group and the individual Internet-Draft move into the incubation phase; licensing now covers W3C and IETF terms ([§23](#23-governance-ipr-and-funding)).
- **References:** 55 new references (37–91).

### Changes in v0.2 (from v0.1)

- **Renamed** from "OpenAds" to the Federated Ads Protocol (identifier `federated-ads`) to avoid confusion with The Trade Desk's OpenAds and other projects.
- **Added** sourced industry data, a prior-art review, a market-design section (inventory, Standing Offers, pricing models, price discovery, budgets, pacing, frequency, ad decisioning), an end-to-end worked example, security and privacy considerations, a legal and regulatory map, an economics example, a comparison table, an adoption strategy, risks, success metrics and a FAQ.
- **Rebuilt measurement:** aggregated receipts with k-thresholds; verification levels V0–V4; corrected the claim that fetch logs corroborate volume; correct use of Privacy Pass; IAB podcast definitions; opens made non-billable.
- **Rebuilt revocation:** Licence separated from the manifest; creative approval by hash; logged, non-backdatable revocations with signed acknowledgements; honest per-surface guarantees; evidence archive.
- **Fixed the protocol design:**
  - the invented proof type replaced with W3C Data Integrity `eddsa-jcs-2022`;
  - Multikey keys;
  - correct RFC 9421 parameters and response signing;
  - valid SHA-256 hashes;
  - state machines, error model, idempotency, critical extensions, registries;
  - transparency logs with witnesses;
  - corrected OpenRTB bridge direction;
  - normative text moved to a separate Internet-Draft.
- **Governance:** stated plainly what the initiative is today; change control; IPR path; funding principles; competition-law safeguards.

---

*The Federated Ads Protocol · Whitepaper v0.3 · The Federated Ads Initiative · Authored with Claude (Anthropic) · Comments: https://github.com/federated-ads/spec/issues*
