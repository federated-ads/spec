# Federated Ads Protocol error types

Errors are returned as [Problem Details (RFC 9457)](https://www.rfc-editor.org/rfc/rfc9457) with media type `application/problem+json`. Each `type` URI is `https://w3id.org/federated-ads/errors/` followed by a name below.

These are the initial entries from the Internet-Draft [`draft-rajan-federated-ads-protocol-00`](../ietf/draft-rajan-federated-ads-protocol-00.html). The draft is a discussion document and the list may change.

| Name | Suggested HTTP status | Meaning |
|---|---|---|
| <a id="malformed-object"></a>`malformed-object` | 400 | Not valid JSON, not I-JSON, or missing required members. |
| <a id="unsupported-version"></a>`unsupported-version` | 400 | Protocol version not supported. |
| <a id="unknown-critical-extension"></a>`unknown-critical-extension` | 400 | A member listed in `critical` is not understood. |
| <a id="signature-invalid"></a>`signature-invalid` | 401 | HTTP signature or object proof failed. |
| <a id="signature-expired"></a>`signature-expired` | 401 | Outside the allowed time window. |
| <a id="key-unknown"></a>`key-unknown` | 401 | `keyid` or verification method not found. |
| <a id="key-revoked"></a>`key-revoked` | 401 | Key revoked at the signing time. |
| <a id="digest-mismatch"></a>`digest-mismatch` | 400 | `Content-Digest` does not match. |
| <a id="replay-detected"></a>`replay-detected` | 401 | Signature value already used. |
| <a id="not-authorized"></a>`not-authorized` | 403 | Sender is not a party entitled to this action. |
| <a id="unknown-object"></a>`unknown-object` | 404 | Referenced object not found. |
| <a id="duplicate-conflict"></a>`duplicate-conflict` | 409 | Same `id`, different content. |
| <a id="state-conflict"></a>`state-conflict` | 409 | Transition not allowed. |
| <a id="hash-mismatch"></a>`hash-mismatch` | 409 | Referenced hash does not match the object. |
| <a id="offer-expired"></a>`offer-expired` | 410 | Offer, claim or acceptance lapsed. |
| <a id="payload-too-large"></a>`payload-too-large` | 413 | Content too large. |
| <a id="policy-mismatch"></a>`policy-mismatch` | 422 | Conflicts with the receiver's Policy. |
| <a id="budget-exhausted"></a>`budget-exhausted` | 422 | No budget remains. |
| <a id="licence-expired"></a>`licence-expired` | 403 | Licence expired. |
| <a id="licence-revoked"></a>`licence-revoked` | 403 | Licence revoked. |
| <a id="adaptation-not-permitted"></a>`adaptation-not-permitted` | 403 | The Licence does not permit the adaptation that the surface requires or that was requested. |
| <a id="k-threshold-violation"></a>`k-threshold-violation` | 422 | Receipt cells below k. |
| <a id="log-inconsistent"></a>`log-inconsistent` | 422 | Log proofs do not verify. |
| <a id="rate-limited"></a>`rate-limited` | 429 | Too many requests. |

[Back to the Federated Ads Protocol](../)
