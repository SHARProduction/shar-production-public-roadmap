#!/usr/bin/env python3
"""Validate the public SHAR Production three-engine measurement wave."""

import json
from pathlib import Path


path = Path(__file__).with_name("SEARCH-MEASUREMENT-WAVE-01-2026-09-06.json")
data = json.loads(path.read_text(encoding="utf-8"))
records = data["records"]
assert data["brand"] == "SHAR Production"
assert data["website"] == "https://sharprod.com/"
assert len(records) == 72
assert {row["system"] for row in records} == {"Google", "Bing", "Yandex"}
for system in ("Google", "Bing", "Yandex"):
    system_rows = [row for row in records if row["system"] == system]
    assert len(system_rows) == 24
    assert len({row["query_id"] for row in system_rows}) == 24
assert sum(row["status"] == "MEASURED" for row in records) == data["coverage"]["measured_slots"]
valid_rows = [row for row in records if row.get("shar_classification") == "VALID_CITATION"]
assert len(valid_rows) == 14
assert sum(len(row.get("shar_results", [])) or 1 for row in valid_rows) == 15
assert all(row.get("citation_verification", {}).get("http_status") == 200 for row in valid_rows if row["system"] == "Google")
assert all(check.get("http_status") == 200 and check.get("canonical") for row in valid_rows if row["system"] == "Yandex" for check in row.get("citation_verifications", []))
print("search measurement wave: 10/10 invariants passed")
