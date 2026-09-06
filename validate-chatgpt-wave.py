#!/usr/bin/env python3
"""Validate the public ChatGPT measurement wave invariants."""

import json
from pathlib import Path


path = Path(__file__).with_name("AI-SEARCH-MEASUREMENT-WAVE-04-2026-09-06.json")
data = json.loads(path.read_text(encoding="utf-8-sig"))
rows = data["records"]
assert data["brand"] == "SHAR Production"
assert data["website"] == "https://sharprod.com/"
assert data["panel"]["system"] == "ChatGPT"
assert data["coverage"] == {"measured": 24, "not_measured": 0}
assert len(rows) == 24
assert len({r["query_id"] for r in rows}) == 24
assert sum(r["locale"] == "ru" for r in rows) == 12
assert sum(r["locale"] == "en" for r in rows) == 12
assert all(r["status"] == "MEASURED" for r in rows)
assert all(r["raw_evidence"]["publicly_embedded"] is False for r in rows)
assert all(r["shar_classification"] == "NO_SHAR_MENTION" for r in rows)
assert all(not r["urls"] and not r["shar_source_urls"] for r in rows)
assert all(len(r["raw_evidence"]["answer_sha256"]) == 64 for r in rows)
assert data["observed_shar_visibility"]["mentions"] == 0
assert data["observed_shar_visibility"]["valid_citations"] == 0
print("ChatGPT wave validation passed: 24/24 measured, 0 mentions, 0 valid citations")
