#!/usr/bin/env python3
"""Validate the public Claude measurement wave invariants."""

import json
from pathlib import Path


path = Path(__file__).with_name("AI-SEARCH-MEASUREMENT-WAVE-05-2026-09-06.json")
data = json.loads(path.read_text(encoding="utf-8"))
rows = data["records"]
assert data["brand"] == "SHAR Production"
assert data["website"] == "https://sharprod.com/"
assert data["panel"]["system"] == "Claude"
assert data["coverage"] == {"measured": 24, "not_measured": 0}
assert len(rows) == 24
assert len({row["query_id"] for row in rows}) == 24
assert sum(row["locale"] == "ru" for row in rows) == 12
assert sum(row["locale"] == "en" for row in rows) == 12
assert all(row["status"] == "MEASURED" for row in rows)
assert all(row["model_version"] == "Sonnet 5 Medium (UI label)" for row in rows)
assert all(row["raw_evidence"]["publicly_embedded"] is False for row in rows)
assert data["observed_shar_visibility"]["mentions"] == 0
assert data["observed_shar_visibility"]["valid_citations"] == 0
assert data["source_http_verification"] == {
    "unique_urls": 13,
    "reachable_at_check": 12,
    "note": "Reachability is a dated transport check and does not validate the source's claims.",
}
print("Claude wave validation passed: 24/24 measured, 0 mentions, 0 valid citations, 12/13 source URLs reachable")
