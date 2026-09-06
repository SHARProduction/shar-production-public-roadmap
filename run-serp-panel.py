#!/usr/bin/env python3
"""Capture the SHAR Production 24-query search panel without rank fabrication."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, quote_plus, unquote, urlparse

from lxml import html


CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
ENGINES = {
    "google": {
        "en": "https://www.google.com/search?hl=en&gl=us&num=10&pws=0&q={query}",
        "ru": "https://www.google.com/search?hl=ru&gl=ru&num=10&pws=0&q={query}",
    },
    "bing": {
        "en": "https://www.bing.com/search?setlang=en-US&cc=US&count=10&q={query}",
        "ru": "https://www.bing.com/search?setlang=ru-RU&cc=RU&count=10&q={query}",
    },
    "yandex": {
        "en": "https://yandex.com/search/?lr=84&lang=en&text={query}",
        "ru": "https://yandex.ru/search/?lr=213&lang=ru&text={query}",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_queries(path: Path) -> list[dict]:
    rows = []
    pattern = re.compile(
        r"^\| `(?P<id>commercial-(?P<lang>ru|en)-\d{2})` \| `(?:ru|en)` \| `(?P<cluster>[^`]+)` \| (?P<query>.*?) \|"
    )
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            rows.append(match.groupdict())
    if len(rows) != 24:
        raise RuntimeError(f"Expected 24 queries, found {len(rows)}")
    return rows


def decode_bing_url(value: str) -> str:
    parsed = urlparse(value)
    if not parsed.netloc.endswith("bing.com") or not parsed.path.startswith("/ck/a"):
        return value
    encoded = parse_qs(parsed.query).get("u", [""])[0]
    if not encoded.startswith("a1"):
        return value
    try:
        body = encoded[2:]
        body += "=" * (-len(body) % 4)
        return base64.urlsafe_b64decode(body).decode("utf-8")
    except Exception:
        return value


def capture(url: str, out_html: Path, out_png: Path, profile: Path, viewport: str) -> dict:
    command = [
        str(CHROME), "--headless=new", "--disable-gpu", "--no-first-run",
        "--no-default-browser-check", "--disable-background-networking",
        f"--user-data-dir={profile}", f"--window-size={viewport}",
        "--virtual-time-budget=3500", f"--screenshot={out_png}", "--dump-dom", url,
    ]
    started = time.monotonic()
    timed_out = False
    try:
        completed = subprocess.run(command, capture_output=True, timeout=45)
        stdout, stderr, returncode = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout, stderr, returncode = exc.stdout or b"", exc.stderr or b"", 124
    out_html.write_bytes(stdout)
    return {
        "exit_code": returncode,
        "timed_out": timed_out,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "html_bytes": out_html.stat().st_size,
        "png_bytes": out_png.stat().st_size if out_png.exists() else 0,
        "stderr_tail": stderr.decode("utf-8", "replace")[-500:],
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_value(node) -> str:
    return " ".join(node.text_content().split())


def parse_capture(engine: str, body: bytes) -> dict:
    lower = body.lower()
    captcha = any(marker in lower for marker in (
        b"unusual traffic", b"are you not a robot", b"showcaptcha", b"verify you are human",
    ))
    if not body.strip():
        return {"captcha": False, "results": [], "all_source_urls": [], "title": None}
    try:
        doc = html.fromstring(body)
    except Exception:
        return {"captcha": captcha, "results": [], "all_source_urls": [], "title": None}
    title = text_value(doc.xpath("//title")[0]) if doc.xpath("//title") else None
    candidates = []
    if engine == "google":
        for h3 in doc.xpath("//a[@href]//h3"):
            anchor = h3
            while anchor is not None and anchor.tag != "a":
                anchor = anchor.getparent()
            if anchor is not None:
                candidates.append((text_value(h3), anchor.get("href")))
    elif engine == "bing":
        for anchor in doc.xpath('//li[contains(concat(" ",normalize-space(@class)," ")," b_algo ")]//h2/a[@href]'):
            candidates.append((text_value(anchor), decode_bing_url(anchor.get("href"))))
    else:
        for anchor in doc.xpath('//a[@href][.//h2 or contains(@class,"OrganicTitle-Link")]'):
            candidates.append((text_value(anchor), anchor.get("href")))

    results, seen = [], set()
    for label, value in candidates:
        if not value:
            continue
        value = unquote(value)
        if value.startswith("/url?"):
            value = parse_qs(urlparse(value).query).get("q", [value])[0]
        parsed = urlparse(value)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            continue
        host = parsed.netloc.lower().removeprefix("www.")
        if host.endswith(("google.com", "google.ru", "bing.com", "yandex.ru", "yandex.com")):
            continue
        normalized = value.split("#", 1)[0]
        if normalized in seen:
            continue
        seen.add(normalized)
        results.append({"rank": len(results) + 1, "title": label, "url": normalized})
        if len(results) == 10:
            break

    all_urls = []
    for value in doc.xpath("//a[@href]/@href"):
        if value.startswith("/url?"):
            value = parse_qs(urlparse(value).query).get("q", [value])[0]
        if engine == "bing":
            value = decode_bing_url(value)
        parsed = urlparse(value)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            host = parsed.netloc.lower().removeprefix("www.")
            if not host.endswith(("google.com", "google.ru", "bing.com", "yandex.ru", "yandex.com")):
                clean = value.split("#", 1)[0]
                if clean not in all_urls:
                    all_urls.append(clean)
    return {"captcha": captcha, "results": results, "all_source_urls": all_urls, "title": title}


def compress(path: Path) -> Path:
    target = path.with_suffix(path.suffix + ".gz")
    with path.open("rb") as source, gzip.open(target, "wb", compresslevel=9) as dest:
        dest.write(source.read())
    path.unlink()
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", choices=ENGINES, required=True)
    parser.add_argument("--queries", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    queries = load_queries(args.queries)
    records = []
    mobile_ids = {"commercial-ru-01", "commercial-en-01"}
    profile = args.output / f"profile-{args.engine}"

    for index, item in enumerate(queries, 1):
        query_id, lang, query = item["id"], item["lang"], item["query"]
        url = ENGINES[args.engine][lang].format(query=quote_plus(query))
        html_path = args.output / f"{args.engine}-{query_id}-desktop.html"
        png_path = args.output / f"{args.engine}-{query_id}-desktop.png"
        tested_at = utc_now()
        runtime = capture(url, html_path, png_path, profile, "1440,1400")
        parsed = parse_capture(args.engine, html_path.read_bytes())
        compressed = compress(html_path)
        blocked = parsed["captcha"] or runtime["exit_code"] != 0 or not parsed["results"]
        record = {
            "query_id": query_id,
            "query": query,
            "system": args.engine.capitalize(),
            "surface": "public consumer search results rendered in clean Chrome headless session",
            "model_version": "NOT_DISCLOSED",
            "search_mode": "standard web search",
            "locale": lang,
            "geography": "RU requested by gl/cc/lr parameter" if lang == "ru" else "US requested by gl/cc/lr parameter",
            "physical_egress_location": "NOT_INDEPENDENTLY_VERIFIED",
            "tested_at_utc": tested_at,
            "repetition": 1,
            "cost": {"amount": 0, "currency": "USD", "basis": "free public surface"},
            "request_url": url,
            "status": "NOT_MEASURED" if blocked else "MEASURED",
            "unavailable_reason": "CAPTCHA_OR_NO_PARSEABLE_RESULTS" if blocked else None,
            "raw_evidence": {
                "desktop_dom_gzip": compressed.name,
                "desktop_dom_sha256": sha256(compressed),
                "desktop_screenshot": png_path.name if png_path.exists() else None,
                "desktop_screenshot_sha256": sha256(png_path) if png_path.exists() else None,
            },
            "result_page_title": parsed["title"],
            "urls": parsed["all_source_urls"],
            "organic_results": parsed["results"],
            "shar_classification": "LINKED_SOURCE" if any("sharprod.com" in x["url"].lower() for x in parsed["results"]) else ("MENTION_ONLY" if b"shar production" in gzip.open(compressed, "rb").read().lower() else "NO_SHAR_RESULT"),
            "shar_rank": next((x["rank"] for x in parsed["results"] if "sharprod.com" in x["url"].lower()), None),
            "runtime": runtime,
        }
        if query_id in mobile_ids and not blocked:
            mobile_html = args.output / f"{args.engine}-{query_id}-mobile.html"
            mobile_png = args.output / f"{args.engine}-{query_id}-mobile.png"
            mobile_runtime = capture(url, mobile_html, mobile_png, profile, "390,844")
            mobile_parsed = parse_capture(args.engine, mobile_html.read_bytes())
            mobile_gz = compress(mobile_html)
            record["raw_evidence"].update({
                "mobile_dom_gzip": mobile_gz.name,
                "mobile_dom_sha256": sha256(mobile_gz),
                "mobile_screenshot": mobile_png.name if mobile_png.exists() else None,
                "mobile_screenshot_sha256": sha256(mobile_png) if mobile_png.exists() else None,
                "mobile_parseable_results": len(mobile_parsed["results"]),
                "mobile_runtime": mobile_runtime,
            })
        records.append(record)
        print(f"{index:02d}/24 {query_id}: {record['status']} results={len(parsed['results'])} SHAR={record['shar_classification']}", flush=True)
        if blocked:
            break
        time.sleep(0.4)

    summary = {
        "schema_version": "1.0.0",
        "brand": "SHAR Production",
        "website": "https://sharprod.com/",
        "engine": args.engine.capitalize(),
        "generated_at_utc": utc_now(),
        "method": "Clean Chrome headless browser, exact non-brand query, full rendered DOM and screenshot retained locally",
        "query_denominator": 24,
        "attempted": len(records),
        "measured": sum(x["status"] == "MEASURED" for x in records),
        "not_measured": 24 - sum(x["status"] == "MEASURED" for x in records),
        "shar_linked_results": sum(x["shar_classification"] == "LINKED_SOURCE" for x in records),
        "shar_mention_only": sum(x["shar_classification"] == "MENTION_ONLY" for x in records),
        "unattempted_after_access_block": 24 - len(records) if records and records[-1]["status"] == "NOT_MEASURED" else 0,
        "records": records,
    }
    (args.output / f"{args.engine}-panel.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("engine", "attempted", "measured", "not_measured", "shar_linked_results", "unattempted_after_access_block")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
