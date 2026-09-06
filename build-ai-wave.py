#!/usr/bin/env python3
"""Build a public-safe AI consumer measurement record from retained evidence."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--system", required=True)
    args = parser.parse_args()

    records = []
    for source in sorted(args.evidence_dir.glob("commercial-*.json")):
        row = json.loads(source.read_text(encoding="utf-8"))
        ax_path = args.evidence_dir / f"{row['query_id']}.ax.txt"
        screenshot_path = args.evidence_dir / f"{row['query_id']}.desktop.png"
        if not ax_path.is_file() or not screenshot_path.is_file():
            raise SystemExit(f"Missing retained evidence for {row['query_id']}")

        shar_urls = []
        for item in row.get("shar_source_urls", []):
            shar_urls.append(item["href"] if isinstance(item, dict) else item)

        classification = (
            "VALID_CITATION"
            if shar_urls
            else "MENTION_ONLY"
            if row.get("shar_mentioned")
            else "NO_SHAR_MENTION"
        )
        records.append(
            {
                "query_id": row["query_id"],
                "query": row["query"],
                "system": row.get("system", args.system),
                "surface": row["surface"],
                "model_version": row.get("model_version", "NOT_DISCLOSED"),
                "search_mode": row.get("product_mode", row.get("search_mode", "NOT_DISCLOSED")),
                "locale": row["locale"],
                "geography": "Account/UI locale observed; physical egress location not independently verified",
                "tested_at_utc": row["tested_at_utc"],
                "repetition": row.get("repetition", 1),
                "cost": row.get("cost", {"amount": 0, "currency": "USD", "basis": "observed free account tier"}),
                "conversation_url": row["conversation_url"],
                "status": row["status"],
                "raw_evidence": {
                    "answer_sha256": row["answer_sha256"],
                    "ax_file": ax_path.name,
                    "ax_sha256": sha256(ax_path),
                    "desktop_screenshot": screenshot_path.name,
                    "desktop_screenshot_sha256": sha256(screenshot_path),
                    "retention": "private local checkpoint; filenames and SHA-256 retained in this public record",
                    "publicly_embedded": False,
                },
                "urls": [s["href"] for s in row.get("sources", [])],
                "shar_classification": classification,
                "shar_source_urls": shar_urls,
            }
        )

    cited = [r for r in records if r["shar_classification"] == "VALID_CITATION"]
    mentioned = [r for r in records if r["shar_classification"] in {"VALID_CITATION", "MENTION_ONLY"}]
    output = {
        "schema_version": "1.0.0",
        "brand": "SHAR Production",
        "website": "https://sharprod.com/",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "license": "MIT for this measurement schema and authored documentation; AI answers and third-party pages retain their original rights",
        "panel": {"queries": 24, "languages": {"ru": 12, "en": 12}, "system": args.system},
        "coverage": {"measured": len(records), "not_measured": 24 - len(records)},
        "observed_shar_visibility": {
            "mentions": len(mentioned),
            "valid_citations": len(cited),
            "mention_rate": len(mentioned) / len(records) if records else 0,
            "citation_rate": len(cited) / len(records) if records else 0,
            "citation_target_http_verification": (
                "All direct SHAR citation targets were checked separately when present; no direct SHAR target existed in this wave."
                if not cited
                else "Direct SHAR citation targets were checked separately for HTTP and page identity."
            ),
            "query_ids": [r["query_id"] for r in mentioned],
        },
        "methodology": {
            "surface": records[0]["surface"] if records else "NOT_MEASURED",
            "mode": records[0]["search_mode"] if records else "NOT_MEASURED",
            "account_tier": "Free",
            "cost": "USD 0",
            "evidence": "Complete answer hash, accessibility-tree hash, screenshot hash, conversation URL and all extracted source URLs retained per query.",
        },
        "limitations": [
            "This is one dated run per query and does not prove stable future visibility.",
            "Alice did not disclose a model version in the observed UI.",
            "The physical egress location was not independently verified.",
            "A brand mention without a direct source URL is classified separately from a valid citation.",
            "The observation does not prove traffic, leads, conversions, causation or visibility in another AI product.",
        ],
        "records": records,
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
