"""
City coverage test — runs a real search for every city in a list against the running API and
records what came back (counts, available, errors, time, phone / email / website / social share).

Usage (backend must be running, e.g. on a separate test database):
    python scripts/city_coverage.py cities.json results.json --api http://127.0.0.1:8001 \
        --category dentist --max 300 --source all_sources

cities.json = [{"city": "Pune", "country_code": "IN"}, ...]
Each city is searched one after another (no parallel load on the free OpenStreetMap / Nominatim
servers). Results are appended to results.json after every city, so an interrupted run keeps them.
"""

import argparse
import csv
import io
import json
import time
from pathlib import Path

import httpx


def completeness(api: str, job_id: int) -> dict:
    """Field coverage of one job's businesses, from the CSV export (same data the user downloads)."""
    response = httpx.get(f"{api}/api/v1/businesses/export", params={"format": "csv", "job_id": job_id}, timeout=120)
    rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8-sig"))))
    social = ("facebook", "instagram", "linkedin", "tiktok", "youtube", "twitter", "whatsapp", "linktree")
    n = len(rows) or 1
    has_social = [any(r.get(k) for k in social) for r in rows]
    return {
        "businesses": len(rows),
        "phone_pct": round(100 * sum(bool(r["phone"]) for r in rows) / n),
        "email_pct": round(100 * sum(bool(r["email"]) for r in rows) / n),
        "website_pct": round(100 * sum(bool(r["website_url"]) for r in rows) / n),
        "social_pct": round(100 * sum(has_social) / n),
        "social_no_website_pct": round(100 * sum(s and not r["website_url"] for s, r in zip(has_social, rows)) / n),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cities")
    ap.add_argument("results")
    ap.add_argument("--api", default="http://127.0.0.1:8001")
    ap.add_argument("--category", default="dentist")
    ap.add_argument("--max", type=int, default=300)
    ap.add_argument("--source", default="all_sources")
    args = ap.parse_args()

    cities = json.loads(Path(args.cities).read_text(encoding="utf-8"))
    out_path = Path(args.results)
    done = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else []
    # A city whose request never reached the API (server restarted / network) is tried again.
    done = [d for d in done if d.get("http") is not None]
    seen = {(d["city"], d["country_code"]) for d in done}

    for item in cities:
        key = (item["city"], item["country_code"])
        if key in seen:
            continue
        started = time.time()
        record = {"city": item["city"], "country_code": item["country_code"], "category": args.category}
        try:
            response = httpx.post(f"{args.api}/api/v1/discovery/run", timeout=900, json={
                "source_slug": args.source, "country_code": item["country_code"], "city": item["city"],
                "category": args.category, "max_results": args.max,
                # state / province disambiguates same-named cities (geocode.py passes it to Nominatim)
                **({"region": item["admin"]} if item.get("admin") else {})})
            body = response.json()
            record.update({
                "http": response.status_code, "status": body.get("status"), "found": body.get("found"),
                "new": body.get("new"), "duplicate": body.get("duplicate"), "available": body.get("available"),
                "errors": body.get("errors"), "error": (body.get("error") or str(body.get("detail") or ""))[:300],
                "job_id": body.get("job_id"),
                "resolved_place": body.get("resolved_place"),
            })
            if body.get("job_id") and (body.get("found") or 0) > 0:
                record.update(completeness(args.api, body["job_id"]))
        except Exception as exc:  # keep going; one city must not stop the run
            record.update({"http": None, "status": "CLIENT_ERROR", "error": str(exc)[:300]})
        record["seconds"] = round(time.time() - started)
        done.append(record)
        out_path.write_text(json.dumps(done, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"{record['city']},{record['country_code']}: {record.get('status')} found={record.get('found')} "
              f"available={record.get('available')} {record.get('error', '')[:80]} ({record['seconds']}s)", flush=True)


if __name__ == "__main__":
    main()
