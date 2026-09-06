#!/usr/bin/env python3
"""Validate the public Gemini measurement wave invariants."""

import json
from pathlib import Path


path = Path(__file__).with_name("AI-SEARCH-MEASUREMENT-WAVE-03-2026-09-06.json")
data = json.loads(path.read_text(encoding="utf-8"))
rows = data["records"]
assert data["brand"] == "SHAR Production"
assert data["website"] == "https://sharprod.com/"
assert data["panel"]["system"] == "Gemini"
assert data["coverage"] == {"measured": 24, "not_measured": 0}
assert len(rows) == 24
assert len({r["query_id"] for r in rows}) == 24
assert sum(r["locale"] == "ru" for r in rows) == 12
assert sum(r["locale"] == "en" for r in rows) == 12
assert all(r["status"] == "MEASURED" for r in rows)
assert all(r["model_version"] == "Flash (UI label)" for r in rows)
assert all(r["raw_evidence"]["publicly_embedded"] is False for r in rows)
assert sum(r["shar_classification"] == "VALID_CITATION" for r in rows) == 0
assert sum(r["shar_classification"] == "MENTION_ONLY" for r in rows) == 1
assert sum(len(r["urls"]) for r in rows) == 59
assert len({u for r in rows for u in r["urls"]}) == 59
mention = next(r for r in rows if r["shar_classification"] == "MENTION_ONLY")
assert mention["query_id"] == "commercial-ru-04"
assert mention["raw_evidence"]["answer_sha256"] == "efbedf47bdff0041dac8a35f1a5eb150cba0d45f21d9587636c820b3b121d105"
print("Gemini wave validation passed: 24/24 measured, 1 mention, 0 valid citations, 59 unique source URLs")
