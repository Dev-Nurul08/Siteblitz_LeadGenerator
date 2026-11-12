"""
Phase 14 email finder: visit the own websites of phone-only leads and keep the emails their pages show.

Scope (docs/spec/outreach-engine.md row 9): Navsari + Surat, no brand, the 3 demo verticals, leads with a
phone, no email and their own website = 2,162 sites on 2026-11-10. The selection is the same query that
produced that count. A lead that spec row 9 of website-intelligence.md never treats as a prospect (school,
college, ...) is recorded as skipped, not visited.

Each site is visited once by `site_visit.visit_site` (robots.txt, homepage + 4 contact paths, 12 s / 2 MB /
5 redirects, SSRF guard). 10 hosts run in parallel; the URLs of one host run one after another.
Never calls ContactDiscoveryEngine.discover_contacts(): it invents addresses (CLAUDE.md).

Usage:  python scripts/email_finder.py [--out DIR] [--limit N] [--parallel 10]
Writes  <out>/visits.jsonl (resumable: visited URLs are skipped on a re-run), <out>/sites.csv (one row per
lead), <out>/emails.csv (one row per lead + email, each with its source URL) and <out>/summary.json.
The output holds business contact data, so it stays outside the repository.
"""

import argparse
import asyncio
import csv
import json
import sys
import time
from collections import Counter, defaultdict, deque
from dataclasses import asdict
from pathlib import Path
from urllib.parse import urlparse

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.app.engines.enrichment.discovery import ContactDiscoveryEngine  # noqa: E402
from backend.app.engines.enrichment.site_visit import visit_site  # noqa: E402
from backend.app.engines.intelligence.rules import Facts, skip_reason  # noqa: E402

SOURCE = "E:/SiteBlitz-World-Business-Data/_work/by_country/country=IN/*.parquet"
DEFAULT_OUT = Path("E:/SiteBlitz-World-Business-Data/_work/email_finder") / time.strftime("%Y-%m-%d")
SOCIAL = (r"(instagram\.com|facebook\.com|fb\.com|linkedin\.com|tiktok\.com|youtube\.com|x\.com|twitter\.com"
          r"|wa\.me|whatsapp\.com|linktr\.ee|justdial\.com|zomato\.com|swiggy\.com|practo\.com)")
# The selection that measured 2,162 sites on 2026-11-10 (outreach-lifecycle session), unchanged.
SELECTION = f"""
WITH m AS (
 SELECT id, name, basic_category, websites[1] AS website,
  CASE WHEN lower(city) LIKE '%navsari%' THEN 'Navsari' WHEN lower(city) LIKE '%surat%' THEN 'Surat' END AS town,
  lower(coalesce(basic_category, category, '')) AS c,
  coalesce(len(emails), 0) > 0 AS has_email, coalesce(len(phones), 0) > 0 AS has_phone,
  coalesce(len(websites), 0) > 0 AND NOT regexp_matches(lower(websites[1]), '{SOCIAL}') AS own_site
 FROM read_parquet('{SOURCE}')
 WHERE coalesce(operating_status, '') <> 'permanently_closed' AND brand IS NULL
   AND (lower(coalesce(city, '')) LIKE '%surat%' OR lower(coalesce(city, '')) LIKE '%navsari%'))
SELECT id, name, town, basic_category, website,
 CASE WHEN regexp_matches(c, 'salon|beauty|spa|nail|barber|hair') THEN 'salon_beauty'
      WHEN regexp_matches(c, 'tutor|coach|education|school|training|college') THEN 'coaching_tuition'
      WHEN regexp_matches(c, 'store|shop|retail|showroom|boutique') THEN 'retail_showroom' END AS vertical
FROM m WHERE NOT has_email AND has_phone AND own_site
ORDER BY town, vertical, id
"""
FREE_MAIL = {"gmail.com", "yahoo.com", "yahoo.co.in", "yahoo.in", "hotmail.com", "outlook.com", "live.com",
             "rediffmail.com", "icloud.com", "ymail.com", "msn.com", "aol.com", "proton.me", "protonmail.com"}


def select_leads() -> list[dict]:
    rows = duckdb.connect().execute(SELECTION).fetchall()
    keys = ("id", "name", "town", "basic_category", "website", "vertical")
    return [dict(zip(keys, row)) for row in rows if row[5] is not None]


def normal_url(url: str) -> str:
    url = (url or "").strip()
    return url if url.startswith(("http://", "https://")) else f"https://{url}"


def has_address(lead: dict) -> bool:
    # 79 of the 2,162 rows list an empty string as their website (seen 2026-11-10): nothing to visit.
    return bool(host_of(lead["website"] or ""))


def host_of(url: str) -> str:
    host = (urlparse(normal_url(url)).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def chain_split(site_rows: list[dict], email_rows: list[dict]) -> dict:
    visited = [r for r in site_rows if r["outcome"] not in ("skipped", "no_address")]
    per_host = Counter(host_of(r["website"]) for r in visited)
    shared = [r for r in visited if per_host[host_of(r["website"])] >= 3]
    single = [r for r in visited if per_host[host_of(r["website"])] < 3]
    single_ids = {r["id"] for r in single}
    return {
        "hosts_with_3plus_leads": sum(1 for n in per_host.values() if n >= 3),
        "leads_on_hosts_with_3plus_leads": len(shared),
        "leads_with_email_on_hosts_with_3plus_leads": sum(1 for r in shared if r.get("emails_found")),
        "leads_with_email_on_other_hosts": sum(1 for r in single if r.get("emails_found")),
        "unique_emails_on_other_hosts": len({e["email"] for e in email_rows if e["id"] in single_ids}),
    }


def load_done(path: Path) -> dict:
    done = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                done[record["listed_url"]] = record
    return done


async def run_visits(urls_by_host: dict, done: dict, out: Path, parallel: int) -> None:
    extract = ContactDiscoveryEngine()._extract_from_html
    lock = asyncio.Lock()
    progress = {"hosts": 0, "total": len(urls_by_host), "start": time.monotonic()}
    # `parallel` workers take hosts from one queue in order: the same "10 hosts at a time, one request per host"
    # as before, without one waiting task per host for the whole run (13,185 hosts in the E1 pool).
    queue = deque(urls_by_host.values())

    async def one_host(urls: list[str]) -> None:
        for url in urls:   # one request at a time per host
            if url in done:
                continue
            visit = await visit_site(url, extract)
            record = asdict(visit)
            record["contacts"] = [asdict(c) for c in visit.contacts]
            record["visited_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            async with lock:
                done[url] = record
                with open(out / "visits.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
        progress["hosts"] += 1
        if progress["hosts"] % 50 == 0 or progress["hosts"] == progress["total"]:
            minutes = (time.monotonic() - progress["start"]) / 60
            print(f"{progress['hosts']}/{progress['total']} hosts, {minutes:.1f} min", flush=True)

    async def worker() -> None:
        while queue:
            await one_host(queue.popleft())

    await asyncio.gather(*(worker() for _ in range(parallel)))


def write_outputs(leads: list[dict], skipped: dict, done: dict, out: Path) -> dict:
    totals = Counter()
    site_rows, email_rows = [], []
    for lead in leads:
        url = normal_url(lead["website"])
        row = {**lead, "skip_reason": skipped.get(lead["id"])}
        if row["skip_reason"]:
            totals["skipped_rule9"] += 1
            site_rows.append({**row, "outcome": "skipped"})
            continue
        if not has_address(lead):
            totals["no_website_address"] += 1
            site_rows.append({**row, "outcome": "no_address", "note": "Website field is an empty string"})
            continue
        visit = done[url]
        own_hosts = {host_of(url), host_of(visit.get("final_url") or url)}
        kept = []
        for contact in visit["contacts"]:
            source = contact.get("source_url") or ""
            if not source:
                totals["emails_dropped_no_source"] += 1
                continue
            if host_of(source) not in own_hosts:
                # A contact page that redirected to another host is not the business's own site.
                totals["emails_dropped_other_host"] += 1
                continue
            kept.append(contact)
        site_rows.append({**row, "outcome": visit["outcome"], "note": visit["note"],
                          "http_status": visit["http_status"], "final_url": visit["final_url"],
                          "has_https": visit["has_https"], "has_viewport": visit["has_viewport"],
                          "robots": visit["robots"], "requests": visit["requests"], "emails_found": len(kept)})
        totals["leads_visited"] += 1
        totals[f"outcome_{visit['outcome']}"] += 1
        if visit["outcome"] in ("ok", "protected") and visit["has_https"] is False:
            totals["no_https"] += 1
        if visit["outcome"] == "ok" and visit["has_viewport"] is False:
            totals["no_viewport"] += 1
        if kept:
            totals["leads_with_email"] += 1
        site_domain = host_of(visit.get("final_url") or url)
        for contact in kept:
            domain = contact["email"].split("@", 1)[1]
            email_rows.append({"id": lead["id"], "name": lead["name"], "town": lead["town"],
                               "vertical": lead["vertical"], "email": contact["email"],
                               "source_url": contact["source_url"], "source_method": contact["source_method"],
                               "free_mail": domain in FREE_MAIL,
                               "domain_matches_site": domain == site_domain or site_domain.endswith("." + domain)})
    site_fields = ["id", "name", "town", "vertical", "basic_category", "website", "skip_reason", "outcome", "note",
                   "http_status", "final_url", "has_https", "has_viewport", "robots", "requests", "emails_found"]
    with open(out / "sites.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=site_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(site_rows)
    email_fields = ["id", "name", "town", "vertical", "email", "source_url", "source_method", "free_mail",
                    "domain_matches_site"]
    with open(out / "emails.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=email_fields)
        writer.writeheader()
        writer.writerows(email_rows)

    visits = [done[u] for u in {normal_url(l["website"]) for l in leads
                                if not skipped.get(l["id"]) and has_address(l)}]
    summary = {
        "leads_selected": len(leads),
        "by_town_vertical": dict(Counter(f"{l['town']}/{l['vertical']}" for l in leads)),
        "unique_sites_visited": len(visits),
        "unique_hosts": len({host_of(v["listed_url"]) for v in visits}),
        "requests": sum(v["requests"] for v in visits),
        "email_rows": len(email_rows),
        "unique_emails": len({r["email"] for r in email_rows}),
        "email_rows_without_source_url": sum(1 for r in email_rows if not r["source_url"]),
        "emails_free_mail": sum(1 for r in email_rows if r["free_mail"]),
        "emails_on_site_domain": sum(1 for r in email_rows if r["domain_matches_site"]),
        "email_methods": dict(Counter(r["source_method"] for r in email_rows)),
        "robots": dict(Counter(v["robots"] for v in visits)),
        "failed_notes": dict(Counter((v["note"] or "") for v in visits if v["outcome"] == "failed").most_common(12)),
        # Chain store-locator hosts (stores.amaron.in, cakeshops.monginis.net, ...) carry many leads that have
        # no Overture brand; their emails are head-office addresses, not the shop owner's.
        **chain_split(site_rows, email_rows),
        **{k: totals[k] for k in sorted(totals)},
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--limit", type=int, default=0, help="only the first N leads (smoke run)")
    parser.add_argument("--parallel", type=int, default=10)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    leads = select_leads()
    if args.limit:
        leads = leads[: args.limit]
    skipped = {}
    for lead in leads:
        facts = Facts(name=lead["name"] or "", categories=[lead["basic_category"] or ""], phone=None, email=None,
                      social_platforms=[], raw_records=[{"basic_category": lead["basic_category"]}])
        reason = skip_reason(facts)
        if reason:
            skipped[lead["id"]] = reason
    urls_by_host = defaultdict(list)
    for lead in leads:
        if lead["id"] not in skipped and has_address(lead):
            url = normal_url(lead["website"])
            if url not in urls_by_host[host_of(url)]:
                urls_by_host[host_of(url)].append(url)
    done = load_done(args.out / "visits.jsonl")
    print(f"{len(leads)} leads, {len(skipped)} skipped by rule 9, {len(urls_by_host)} hosts, "
          f"{len(done)} URLs already visited", flush=True)
    asyncio.run(run_visits(urls_by_host, done, args.out, args.parallel))
    summary = write_outputs(leads, skipped, done, args.out)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
