# Federated Ads Protocol

An open, federated, owner-controlled protocol for advertising on the open web.

The Federated Ads Protocol lets independent servers ("nodes") run by publishers, advertisers, agencies or cooperatives:

- find each other by domain;
- agree deals using signed offers;
- serve creatives that the advertiser **still owns and can revoke at any time**;
- prove delivery with signed, aggregated receipts recorded in witnessed transparency logs;
- settle payment on any payment rail.

Matching is contextual by default, and the protocol carries no cross-site identifiers. People who see ads get an explanation, an opt-out, an ad-free option and a way to report abuse. One protocol covers websites, fediverse and social feeds, newsletters, podcasts and AI/chat surfaces.

> **Status:** Discussion draft for public comment (whitepaper v0.3, October 2026). This is not a standard and has not been endorsed by any standards body.

> **Authored with Claude.** The whitepaper and specification drafts were researched and drafted with Claude (Anthropic) under the direction of a human contributor, who is accountable for their contents. See §28 of the whitepaper.

## Read

| Document | Description |
|---|---|
| [Whitepaper v0.3](docs/whitepaper/federated-ads-whitepaper.md) | Problem, prior art, design, market design, measurement, legal map, economics, governance, roadmap, publisher revenue |
| [Internet-Draft](docs/ietf/) | Normative wire protocol: `draft-rajan-federated-ads-protocol` |
| [Draft W3C Community Group charter](docs/governance/w3c-community-group-charter-draft.md) | Proposed home for the specification work |
| [Whitepaper v0.1 (archived)](docs/whitepaper/archive/openads-whitepaper-v0.1.md) | First draft, under the earlier working name |

## Get involved

Feedback is the point of this draft. In particular:

- Is the problem framed correctly?
- Are the trade-offs acceptable, especially the absence of cross-publisher frequency capping and the verification levels?
- Would you implement, pilot or help govern this?

Please open an [issue](https://github.com/federated-ads/spec/issues) for specific problems or start a [discussion](https://github.com/federated-ads/spec/discussions) for broader questions. See [CONTRIBUTING.md](CONTRIBUTING.md).

Contact: Suneesh Rajan · suneeshtr@gmail.com

## Naming

This project is unrelated to The Trade Desk's "OpenAds" header-bidding wrapper, to the "Open Ads Protocol" Web3 project, and to the historical "Openads" ad server. Version 0.1 used "OpenAds" as a working name, and the project was renamed to avoid confusion. Identifiers use `federated-ads`.

## Licence

- Specification and documentation text: [CC BY 4.0](LICENSE-docs)
- Code (when published): [Apache-2.0](LICENSE)
- Contributions are subject to the patent commitment in [CONTRIBUTING.md](CONTRIBUTING.md).
