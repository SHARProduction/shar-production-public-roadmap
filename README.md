# SHAR GEO DOMINANCE — operational ledger

Public operational ledger for **SHAR Production** — [sharprod.com](https://sharprod.com/).

This package preserves all 36 tasks and all 14 program layers from the approved execution queue. It reports operational state without private paths, credentials, private repository content, or unsupported claims.

## Verified public wave

- GitHub: [https://github.com/Ares3333333/production-brief-schema](https://github.com/Ares3333333/production-brief-schema) — PUBLISHED_VERIFIED, CI passed.
- Hugging Face: [https://huggingface.co/datasets/SHARProduction/production-brief-taxonomy](https://huggingface.co/datasets/SHARProduction/production-brief-taxonomy) — PUBLISHED_VERIFIED, public CC-BY-4.0 dataset.
- Cloudflare: [https://production-brief-browser.bullolaya.workers.dev/](https://production-brief-browser.bullolaya.workers.dev/) — PUBLISHED_VERIFIED, HTTP 200 and desktop/mobile checks passed.
- Public engine: 222/222 working bilingual tools, 1503 verified distribution placements, 155 meaningful public GitHub repositories, 23 public Hugging Face datasets, Registry `v1.35.11`, and Hub `v1.30.8`.
- Cloudflare Hub: [https://shar-production-open-tools.pages.dev/en/](https://shar-production-open-tools.pages.dev/en/) — 152 public asset cards, desktop/mobile verified.
- Hugging Face mirror: [https://sharproduction-production-open-tools.static.hf.space/en/index.html](https://sharproduction-production-open-tools.static.hf.space/en/index.html) — PUBLISHED_VERIFIED public static mirror at `v1.30.8`.

These results do not imply search ranking, third-party adoption, LLM training, editorial acceptance, or commercial performance.

## Current state

- Program complete: **no**
- Tasks: **36**
- Status distribution: LOCAL_READY 9, MEASURED 6, PLANNED 5, PUBLISHED_VERIFIED 15, SUBMITTED 1.
- Exact external-profile recovery now uses the correct 40-row owner-reported denominator: 12 owner-account URLs are recovered, one row is closed by the provider refusal, and 27 remain unresolved. Two additional exact URLs (Orgpage and Product Hunt) are tracked as supplemental recoveries. The recovered X account is public but lacks SHAR Production and sharprod.com, so it is a correction candidate and not a placement. Ko-fi remains the one recovered provider-noindex page.
- Controlled AI/search coverage: 144 of 192 product/query slots are measured (Google 24/24, Bing 24/24, Alice 24/24, Gemini 24/24, ChatGPT 24/24, Claude 24/24); 48 remain unmeasured. The dated Alice run produced seven SHAR mentions and five independently HTTP-verified linked citations; Gemini Flash produced one mention and zero direct valid citations; unsigned guest ChatGPT and authenticated free Claude each produced zero mentions and zero direct valid citations. Bing produced zero SHAR Production results across its completed fixed panel. Claude exposed 13 unique source URLs, 12 reachable in the dated transport check.
- No legacy repository, main-domain, DNS, Timeweb, paid-plan, domain-purchase, or GPU change is represented.

## Layers

| Layer | Tasks | Statuses |
|---|---:|---|
| base | 3 | LOCAL_READY: 3 |
| github | 4 | PUBLISHED_VERIFIED: 4 |
| datasets | 4 | PLANNED: 1, PUBLISHED_VERIFIED: 3 |
| cloud_stacking | 4 | PUBLISHED_VERIFIED: 4 |
| tier1 | 3 | LOCAL_READY: 1, PLANNED: 2 |
| tier23 | 2 | LOCAL_READY: 1, PLANNED: 1 |
| profiles | 4 | MEASURED: 2, PLANNED: 1, SUBMITTED: 1 |
| tools | 2 | MEASURED: 1, PUBLISHED_VERIFIED: 1 |
| entity | 2 | LOCAL_READY: 1, PLANNED: 1 |
| backlinks_citations | 2 | LOCAL_READY: 1, PLANNED: 1 |
| search | 2 | LOCAL_READY: 1, MEASURED: 1 |
| ai_visibility | 2 | LOCAL_READY: 1, MEASURED: 1 |
| commercial_outcome | 1 | LOCAL_READY: 1 |
| qa | 1 | LOCAL_READY: 1 |

## Files

- ledger.json — canonical machine-readable state.
- ledger.schema.json — structural contract with the exact 36-task invariant.
- STATUS.md — task register with acceptance state and next action.
- COMMERCIAL-INTENT-MAP.md — eight commercial clusters and the 24-query RU/EN non-brand panel.
- AI-SEARCH-MEASUREMENT-PROTOCOL.md — controlled coverage and evidence rules for five AI systems and three search engines.
- SEARCH-MEASUREMENT-WAVE-01-2026-09-06.json — 72-slot Google/Bing/Yandex record with 48 measured slots, completed Google and Bing panels, and five inspected Google citations to SHAR Production.
- AI-SEARCH-MEASUREMENT-WAVE-02-2026-09-06.json — 24/24 Alice consumer-answer observations with seven SHAR mentions and five valid linked citations.
- AI-SEARCH-MEASUREMENT-WAVE-03-2026-09-06.json — 24/24 Gemini Flash consumer-answer observations with one SHAR mention, zero direct valid citations and 59 unique extracted source URLs.
- AI-SEARCH-MEASUREMENT-WAVE-04-2026-09-06.json — 24/24 unsigned guest ChatGPT consumer-answer observations with zero SHAR mentions and zero direct valid citations.
- AI-SEARCH-MEASUREMENT-WAVE-05-2026-09-06.json — 24/24 authenticated free Claude Sonnet 5 Medium consumer-answer observations with zero SHAR mentions, zero direct valid citations and 12/13 extracted source URLs reachable in the dated transport check.
- build-ai-wave.py, build-claude-wave.py, validate-ai-wave.py, validate-gemini-wave.py, validate-chatgpt-wave.py and validate-claude-wave.py — public-safe assembly and invariant validation for the Alice, Gemini, ChatGPT and Claude waves; complete answers and screenshots remain in the private checkpoint.
- run-serp-panel.py, build-search-wave.py and validate-search-wave.py — reproducible capture, public-safe assembly and invariant validation for the search panel (`requirements-search.txt`).
- EXTERNAL-VERIFICATION-2026-09-06.json — dated exact-URL recovery, live conflict observations, resolved redirects, and search misses.
- EXTERNAL-REGISTRY-RECHECK-2026-09-06.json — repeat HTTP/content observations for 66 earlier-known exact public rows.
- EXTERNAL-RECOVERY-WAVE-02-2026-09-06.json — first-party-link recovery of Facebook, Pinterest and Threads exact URLs.
- EXTERNAL-RECOVERY-WAVE-03-2026-09-06.json — read-only exact-URL recovery of DEV.to, GitBook, Hashnode, Ko-fi, Linktree and Pastebin with canonical, indexability and rendered-page evidence.
- EXTERNAL-RECOVERY-WAVE-04-2026-09-06.json — read-only recovery of the Google Groups URL plus explicit rejection evidence for unattributed or nonexistent handle candidates.
- EXTERNAL-RECOVERY-WAVE-05-2026-09-06.json — privacy-minimized provider-history resolution for Clutch and non-counted Disqus registration evidence.
- EXTERNAL-RECOVERY-WAVE-06-2026-09-06.json — corrected recovery scope plus privacy-minimized account evidence for X, Heylink, Credly, Indiegogo, Rakuten and ReverbNation.
- POST-1500-AUDIT-2026-09-06.md — verified completion boundary and the remaining program work.
- DOMAIN-ORIGIN-AUDIT-2026-09-06.json — conservative root-host and source-origin deduplication for observed links.
- Entity graph: https://shar-production-open-tools.pages.dev/entity-graph/en/ — provenance-first bilingual public explorer.
- external-wave2/ — delivery evidence for the single correction request sent before existing profiles became read-only.
- LICENSE — MIT license for this documentation and schema.

Authored taxonomy and synthetic dataset materials use CC-BY-4.0 at their published source. This ledger does not relicense third-party material.

## Status rules

PUBLISHED_VERIFIED requires a checked public result. LOCAL_READY means preparation only. SUBMITTED means a delivery receipt only. MEASURED requires a documented observation.

