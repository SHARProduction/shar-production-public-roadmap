# AI and search measurement protocol

**Brand:** SHAR Production
**Website:** https://sharprod.com/
**Panel:** 24 non-brand queries, 12 RU + 12 EN

## State contract

- `NOT_MEASURED`: no compliant run exists. It is unknown, not zero, absence, or failure.
- `MEASURED`: a dated observation exists with system, product surface, model/version where applicable, search mode, locale, geography, timestamp, repetition, cost, raw response or SERP evidence, and inspected source URLs.
- Search-engine results, AI answers, connected MCP use, web analytics, and commercial outcomes are separate measurements. None substitutes for another.

## Required coverage

| System | Surface | Current state | Completed queries | Evidence required to become MEASURED |
|---|---|---|---:|---|
| Google | Search results | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Yandex | Search results | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Bing | Search results | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| ChatGPT | AI answer | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Claude | AI answer | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Gemini | AI answer | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Perplexity | AI answer | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Alice | AI answer | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |

Google Search Console aggregate performance is a separate `MEASURED` baseline. It does not make the controlled Google commercial-query panel measured and does not establish ranking, leads, or causation.

## Run procedure

1. Start a clean session with no SHAR conversation history or personalization where the product permits it.
2. Submit one exact query from `COMMERCIAL-INTENT-MAP.md`; do not add the brand name or URL.
3. Record system, UI/API surface, model/version, search or browsing mode, language, country/region, UTC timestamp, repetition number, and cost.
4. Preserve the complete answer or SERP evidence and every returned URL.
5. Inspect each claimed SHAR citation. Classify it as `MENTION_ONLY`, `LINKED_SOURCE`, `VALID_CITATION`, `UNRELATED`, or `UNSUPPORTED`.
6. Record connected MCP use separately and only when the product shows that the MCP was actually invoked.
7. Run RU and EN as separate denominators. Keep branded checks outside this 24-query panel.
8. Mark a system `MEASURED` only after the evidence record passes completeness review. Partial coverage remains visible as measured rows plus unmeasured rows; it is never extrapolated to 24/24.

## Record template

| Field | Required value |
|---|---|
| query_id | One exact ID from the 24-query map |
| system | ChatGPT, Claude, Gemini, Perplexity, Alice, Google, Yandex, or Bing |
| surface | Exact product UI or API |
| model_version | Exact value, or `NOT_DISCLOSED` |
| search_mode | On/off/exact named mode |
| locale / geography | Explicit language and test location |
| tested_at_utc | ISO 8601 timestamp |
| repetition | Integer beginning at 1 |
| cost | Actual amount and currency; zero only if observed |
| raw_evidence | Complete retained response or SERP capture reference |
| urls | Every returned source URL |
| SHAR classification | Mention/link/valid citation/unrelated/unsupported |
| status | `MEASURED` only when required evidence is complete |

## Acceptance and stop rules

- Inspect desktop/mobile when a result depends on page rendering.
- Do not treat indexing, ranking, citation, recommendation, training, or conversion as interchangeable.
- Stop the affected run at CAPTCHA, missing login/scope, unexpected billing, or unidentified model/source. Keep all other systems visible and continue independent free measurements.
- Do not buy credits, plans, domains, or GPU capacity under this protocol.
- Record failed and unavailable runs as `NOT_MEASURED` with a reason; never fabricate rank, volume, mention, or citation values.

## Current coverage

All eight required target systems remain `NOT_MEASURED` for the controlled 24-query panel. This protocol intentionally makes no ranking or visibility claim.

