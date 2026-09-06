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
| Google | Search results | **MEASURED** | 24/24 | Wave 01 used exact queries in the current consumer UI with `udm=14` and `pws=0`; accessibility evidence, screenshots, timestamps and inspected SHAR URLs are recorded. |
| Yandex | Search results | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Bing | Search results | **PARTIAL** | 9/24 | Nine exact queries have complete rendered evidence. The tenth returned no parseable results, so the run stopped and the remaining 15 slots stayed `NOT_MEASURED`. |
| ChatGPT | AI answer | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Claude | AI answer | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Gemini | AI answer | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Perplexity | AI answer | **NOT_MEASURED** | 0/24 | Clean session; exact query; date/time; locale and geography; model/version and search mode when applicable; full result/answer; all cited URLs inspected. |
| Alice | AI answer | **MEASURED** | 24/24 | Signed-in free consumer UI, `Intelligence: Auto`; exact queries; dated full-answer hashes, AX hashes, screenshots, conversation URLs and source URLs retained. Seven SHAR mentions and five valid linked citations were observed. |

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

`SEARCH-MEASUREMENT-WAVE-01-2026-09-06.json` records all 72 search-engine/query slots: Google 24 `MEASURED`, Bing 9 `MEASURED` plus 15 `NOT_MEASURED`, and Yandex 24 `NOT_MEASURED` after an access block. Five Google rows contain inspected valid SHAR citations: four observed rank 1 and one observed rank 2.

`AI-SEARCH-MEASUREMENT-WAVE-02-2026-09-06.json` records Alice at 24/24 `MEASURED` in the signed-in free consumer UI with `Intelligence: Auto`. Seven answers mentioned SHAR and five supplied a direct sharprod.com source; all four unique citation targets returned HTTP 200 with exact self-canonical URLs and the brand present. These dated observations do not establish stable rank, traffic, leads, causation or visibility in another geography or product surface. ChatGPT, Claude, Gemini and Perplexity remain `NOT_MEASURED` until their named consumer surfaces are accessible and identifiable under this protocol.

