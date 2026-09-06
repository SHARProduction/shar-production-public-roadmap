#!/usr/bin/env python3
"""Build the public-safe Claude consumer measurement wave from private evidence."""

import argparse
import datetime as dt
import json
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("--evidence-dir", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()

panel = json.loads((args.evidence_dir / "claude-panel.json").read_text(encoding="utf-8"))
http = json.loads((args.evidence_dir / "claude-source-http-verification.json").read_text(encoding="utf-8"))
records = []
for row in panel["records"]:
    source_urls = row.get("source_urls", [])
    shar_urls = [url for url in source_urls if "sharprod.com" in url.lower()]
    records.append(
        {
            "query_id": row["query_id"],
            "query": row["query"],
            "system": "Claude",
            "surface": panel["surface"],
            "model_version": panel["model_version"],
            "search_mode": "Claude consumer web search when invoked by the product",
            "locale": row["locale"],
            "geography": "Unknown; physical egress location not independently verified",
            "tested_at_utc": row["captured_at_utc"],
            "repetition": 1,
            "cost": row["cost"],
            "conversation_url": row["conversation_url"],
            "status": row["status"],
            "raw_evidence": {
                "answer_sha256": row["answer_sha256"],
                "visible_main_region_sha256": row["trace_sha256"],
                "retention": "private local checkpoint; hashes retained in this public record",
                "publicly_embedded": False,
            },
            "urls": source_urls,
            "shar_classification": (
                "VALID_CITATION" if shar_urls else "MENTION_ONLY" if row["shar_mentioned"] else "NO_SHAR_MENTION"
            ),
            "shar_source_urls": shar_urls,
        }
    )

mentions = [row for row in records if row["shar_classification"] != "NO_SHAR_MENTION"]
citations = [row for row in records if row["shar_classification"] == "VALID_CITATION"]
output = {
    "schema_version": "1.0.0",
    "brand": "SHAR Production",
    "website": "https://sharprod.com/",
    "generated_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "license": "MIT for this measurement schema and authored documentation; AI answers and third-party pages retain their original rights",
    "panel": {"queries": 24, "languages": {"ru": 12, "en": 12}, "system": "Claude"},
    "coverage": {"measured": len(records), "not_measured": 24 - len(records)},
    "observed_shar_visibility": {
        "mentions": len(mentions),
        "valid_citations": len(citations),
        "mention_rate": len(mentions) / len(records) if records else 0,
        "citation_rate": len(citations) / len(records) if records else 0,
        "query_ids": [row["query_id"] for row in mentions],
    },
    "source_http_verification": {
        "unique_urls": http["unique_source_urls"],
        "reachable_at_check": http["reachable"],
        "note": "Reachability is a dated transport check and does not validate the source's claims.",
    },
    "methodology": {
        "surface": panel["surface"],
        "mode": "Fresh chat per fixed non-brand query; consumer web search was allowed when Claude invoked it",
        "account_tier": "Free authenticated consumer account",
        "cost": "USD 0",
        "evidence": "Complete answer and visible main-region hashes, attributable conversation URLs and extracted exact source URLs retained per query.",
    },
    "limitations": [
        "This is one dated run per query and does not prove stable future visibility.",
        "The model name is the consumer UI label observed during the run.",
        "The physical egress location was not independently verified.",
        "A brand mention without a direct SHAR-controlled source URL is not a valid citation.",
        "Source reachability does not validate third-party claims.",
        "The observation does not prove traffic, leads, conversions, causation or visibility in another AI product.",
    ],
    "records": records,
}
args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
