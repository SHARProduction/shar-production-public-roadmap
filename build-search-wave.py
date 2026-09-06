#!/usr/bin/env python3
"""Build a public-safe 72-slot search measurement record from retained evidence."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def load_queries(path: Path) -> list[dict]:
    pattern = re.compile(
        r"^\| `(?P<id>commercial-(?P<lang>ru|en)-\d{2})` \| `(?:ru|en)` \| `(?P<cluster>[^`]+)` \| (?P<query>.*?) \|"
    )
    rows = [match.groupdict() for line in path.read_text(encoding="utf-8").splitlines() if (match := pattern.match(line))]
    if len(rows) != 24:
        raise RuntimeError(f"Expected 24 queries, found {len(rows)}")
    return rows


def public_record(record: dict) -> dict:
    keep = (
        "query_id", "query", "system", "surface", "model_version", "search_mode", "locale",
        "geography", "physical_egress_location", "tested_at_utc", "repetition", "cost",
        "request_url", "status", "unavailable_reason", "raw_evidence", "urls", "organic_results",
        "shar_classification", "shar_rank", "citation_verification", "nonpersonalized_notice",
    )
    item = {key: record.get(key) for key in keep if key in record}
    if "raw_evidence" in item:
        item["raw_evidence"]["retention"] = "private local checkpoint; filenames and SHA-256 retained in this public record"
        item["raw_evidence"]["publicly_embedded"] = False
        item["raw_evidence"].pop("mobile_runtime", None)
    return item


def expand(panel: dict, queries: list[dict], block_reason: str) -> list[dict]:
    by_id = {row["query_id"]: public_record(row) for row in panel.get("records", [])}
    records = []
    for query in queries:
        if query["id"] in by_id:
            records.append(by_id[query["id"]])
        else:
            records.append({
                "query_id": query["id"],
                "query": query["query"],
                "system": panel["engine"],
                "locale": query["lang"],
                "status": "NOT_MEASURED",
                "unavailable_reason": block_reason,
                "raw_evidence": None,
                "urls": [],
                "shar_classification": "UNASSESSED",
                "shar_rank": None,
            })
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", type=Path, required=True)
    parser.add_argument("--google", type=Path, required=True)
    parser.add_argument("--bing", type=Path, required=True)
    parser.add_argument("--yandex", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    queries = load_queries(args.queries)
    panels = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in {
        "Google": args.google, "Bing": args.bing, "Yandex": args.yandex,
    }.items()}
    reasons = {
        "Google": "none; all 24 slots measured in the in-app consumer UI",
        "Bing": "run stopped after the tenth page returned no parseable results; remaining slots were not assigned zero values",
        "Yandex": "run stopped after the first browser request timed out; an independent HTTP preflight redirected to showcaptcha",
    }
    records = []
    for name in ("Google", "Bing", "Yandex"):
        records.extend(expand(panels[name], queries, reasons[name]))
    measured = [row for row in records if row["status"] == "MEASURED"]
    valid = [row for row in records if row.get("shar_classification") == "VALID_CITATION"]
    result = {
        "schema_version": "1.0.0",
        "brand": "SHAR Production",
        "website": "https://sharprod.com/",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "license": "MIT for this measurement schema and authored documentation; search-result facts and third-party pages retain their original rights",
        "panel": {"queries": 24, "languages": {"ru": 12, "en": 12}, "systems": 3, "total_slots": 72},
        "coverage": {
            "measured_slots": len(measured),
            "not_measured_slots": 72 - len(measured),
            "by_system": {
                name: {
                    "measured": sum(row["system"] == name and row["status"] == "MEASURED" for row in records),
                    "not_measured": sum(row["system"] == name and row["status"] != "MEASURED" for row in records),
                }
                for name in ("Google", "Bing", "Yandex")
            },
        },
        "observed_shar_visibility": {
            "valid_google_citations": len(valid),
            "rank_1": sum(row.get("shar_rank") == 1 for row in valid),
            "rank_2": sum(row.get("shar_rank") == 2 for row in valid),
            "queries": [{"query_id": row["query_id"], "query": row["query"], "rank": row["shar_rank"], "url": next(url for url in row["urls"] if "sharprod.com" in url)} for row in valid],
            "scope_note": "One dated requested-locale observation per query. This does not prove stable rank, traffic, leads, causation, or visibility in another geography or product surface.",
        },
        "methodology": {
            "google": "Current in-app Google Search consumer UI, web-only udm=14, pws=0; complete accessibility tree and desktop screenshot retained for every query.",
            "bing": "Clean Chrome headless consumer search surface; rendered DOM and desktop screenshot retained for every attempted query; RU01 and EN01 also captured at a 390x844 viewport.",
            "yandex": "Clean Chrome headless consumer search surface; stopped on the first timed-out run after direct HTTP preflight redirected to showcaptcha.",
            "cost": "USD 0; free public surfaces only.",
        },
        "limitations": [
            "Requested locale/country parameters are recorded; physical egress location was not independently verified.",
            "Google was signed in but used pws=0; a non-personalized notice was preserved in 23 of 24 accessibility captures.",
            "Lower Google URLs compacted to an ellipsis in some accessibility captures; screenshots preserve the rendered page and only parseable URLs are ranked.",
            "Bing and Yandex inaccessible slots are NOT_MEASURED, not zero visibility.",
            "IndexNow acceptance and an indexable page are not evidence of indexing or rank.",
        ],
        "records": records,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"slots": len(records), **result["coverage"], **result["observed_shar_visibility"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
