#!/usr/bin/env python3
"""Validate the public Alice measurement wave invariants."""

import json
from pathlib import Path


path = Path(__file__).with_name("AI-SEARCH-MEASUREMENT-WAVE-02-2026-09-06.json")
data = json.loads(path.read_text(encoding="utf-8"))
rows = data["records"]
assert data["brand"] == "SHAR Production"
assert data["website"] == "https://sharprod.com/"
assert data["coverage"] == {"measured": 24, "not_measured": 0}
assert len(rows) == 24
assert len({r["query_id"] for r in rows}) == 24
assert sum(r["locale"] == "ru" for r in rows) == 12
assert sum(r["locale"] == "en" for r in rows) == 12
assert all(r["status"] == "MEASURED" for r in rows)
assert all(r["model_version"] == "NOT_DISCLOSED" for r in rows)
assert all(r["raw_evidence"]["publicly_embedded"] is False for r in rows)
assert sum(r["shar_classification"] == "VALID_CITATION" for r in rows) == 5
assert sum(r["shar_classification"] in {"VALID_CITATION", "MENTION_ONLY"} for r in rows) == 7
print("Alice wave validation passed: 24/24 measured, 7 mentions, 5 valid citations")
