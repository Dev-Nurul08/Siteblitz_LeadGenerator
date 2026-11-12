"""
Email engine v2, phase E1 - build an eligibility pool (one polite run) and evaluate it.

Steps (run in this order; each one can be re-run):
  select     Indian businesses in the three demo verticals (the phase-14 category mapping) with their own website,
             exact city match on 11 Gujarat cities, from countries/IN India/IN_businesses.zip. Brands (Overture
             `brand`), social-only websites and website-intelligence rule 9 are left out, as in phase 14; hosts the
             phase-14 run already visited are skipped. Writes <out>/leads.csv + select.json.
  visit      `site_visit.visit_site` exactly as phase 14 (robots.txt, homepage + 4 contact paths, 12 s, 2 MB,
             5 redirects, SSRF guard, 10 hosts in parallel, one request per host at a time). Resumable through
             <out>/visits.jsonl. Surat + Navsari first, then the other cities round-robin; --max-minutes stops the
             run (the ~4 h limit), --max-hosts caps it, --min-free-mb (default 500) stops it cleanly when the
             machine runs low on RAM, --write-only writes the outputs of a stopped run without visiting.
             Writes sites.csv, emails.csv, summary.json.
  recapture  The phase-14 leads whose homepage had no viewport tag and showed an email were visited before the
             extractor kept the page excerpt; they are visited once more the same way (<out>/recapture_phase14/) so
             their addresses can have Tier 1 provenance.
  import     phase-14 folder, recapture folder and pool folder into the app database (DATABASE_URL), idempotent.
  render     rendered 390 px phone check (scripts/render_check.cjs) of every business whose latest homepage check
             found no viewport tag and that has an address read on its own pages. Screenshots go to
             E:/SiteBlitz-World-Business-Data/_work/evidence/<date>/.
  evaluate   eligibility rules + verifier ladder (MX lookups; Bouncer only if BOUNCER_API_KEY is set).
  report     counts per vertical and city -> <out>/report.json (business data stays outside the repo).
Nothing is sent, submitted or logged into. Never calls a contact-guessing function (there is none left).

Usage: python scripts/pool_e1.py <step> [--out DIR] [--max-hosts N]
"""

import argparse
import asyncio
import csv
import ctypes
import io
import json
import re
import sys
import time
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.app.engines.intelligence.rules import Facts, skip_reason  # noqa: E402
from scripts.email_finder import (  # noqa: E402
    SOCIAL,
    has_address,
    host_of,
    load_done,
    normal_url,
    run_visits,
    write_outputs,
)

DATA = Path("E:/SiteBlitz-World-Business-Data")
ZIP = DATA / "countries" / "IN India" / "IN_businesses.zip"
PHASE14 = DATA / "_work" / "email_finder" / "2026-11-10"
DEFAULT_OUT = DATA / "_work" / "pool_e1" / "2026-11-12"
CITIES = ("Surat", "Navsari", "Ahmedabad", "Vadodara", "Rajkot", "Bharuch", "Valsad", "Anand", "Gandhinagar",
          "Bhavnagar", "Jamnagar")
# The phase-14 category mapping (scripts/email_finder.py SELECTION), unchanged.
VERTICALS = (("salon_beauty", re.compile(r"salon|beauty|spa|nail|barber|hair")),
             ("coaching_tuition", re.compile(r"tutor|coach|education|school|training|college")),
             ("retail_showroom", re.compile(r"store|shop|retail|showroom|boutique")))
SOCIAL_RE = re.compile(SOCIAL)
HOSTS_PER_MINUTE = 82   # measured in phase 14: 1,230 hosts in 15 minutes
LEAD_FIELDS = ["id", "name", "town", "vertical", "basic_category", "website", "state", "address", "postcode", "lat",
               "lon", "phones", "emails", "brand", "facebook", "instagram", "linkedin", "tiktok", "youtube",
               "twitter", "whatsapp", "linktree"]


def vertical_of(category: str):
    text = (category or "").lower()
    return next((name for name, pattern in VERTICALS if pattern.search(text)), None)


def phase14_hosts() -> set[str]:
    hosts = set()
    for record in load_done(PHASE14 / "visits.jsonl").values():
        for url in (record.get("listed_url"), record.get("final_url")):
            if url and host_of(url):
                hosts.add(host_of(url))
    return hosts


def step_select(out: Path) -> dict:
    wanted = {c.lower(): c for c in CITIES}
    seen_hosts = phase14_hosts()
    totals, by_city, leads, ids = Counter(), Counter(), [], set()
    with zipfile.ZipFile(ZIP) as archive:
        for name in sorted(archive.namelist()):
            with archive.open(name) as raw:
                for row in csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig")):
                    totals["rows_scanned"] += 1
                    city = wanted.get((row.get("city") or "").strip().lower())
                    if not city:
                        continue
                    totals["exact_city_rows"] += 1
                    state = (row.get("state") or "").strip().lower()
                    if state and "gujarat" not in state:
                        totals["excluded_state_not_gujarat"] += 1
                        continue
                    vertical = vertical_of(row.get("category"))
                    if not vertical:
                        continue
                    totals["in_three_verticals"] += 1
                    if (row.get("brand") or "").strip():
                        totals["excluded_brand"] += 1
                        continue
                    website = (row.get("website") or "").strip()
                    if not website or not host_of(website):
                        totals["excluded_no_website"] += 1
                        continue
                    if SOCIAL_RE.search(website.lower()):
                        totals["excluded_social_website"] += 1
                        continue
                    if host_of(website) in seen_hosts:
                        totals["excluded_phase14_host"] += 1
                        continue
                    if row["overture_id"] in ids:
                        continue
                    ids.add(row["overture_id"])
                    leads.append({"id": row["overture_id"], "name": row.get("name") or "", "town": city,
                                  "vertical": vertical, "basic_category": row.get("category") or "",
                                  "website": website, **{k: row.get(k) or "" for k in LEAD_FIELDS[6:]}})
                    by_city[f"{city}/{vertical}"] += 1
    leads.sort(key=lambda l: (l["town"], l["vertical"], l["id"]))
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "leads.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=LEAD_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(leads)
    skipped = sum(1 for l in leads if rule9(l))
    hosts = {host_of(normal_url(l["website"])) for l in leads if not rule9(l)}
    summary = {**dict(totals), "selected": len(leads), "rule9_skipped": skipped, "hosts_to_visit": len(hosts),
               "estimated_minutes": round(len(hosts) / HOSTS_PER_MINUTE), "by_city_vertical": dict(sorted(
                   by_city.items())), "note": "IN_businesses.zip has no operating_status column, so permanently "
                                             "closed places cannot be filtered here (phase 14 could)"}
    (out / "select.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def rule9(lead: dict):
    facts = Facts(name=lead["name"], categories=[lead["basic_category"]], phone=None, email=None,
                  social_platforms=[], raw_records=[{"basic_category": lead["basic_category"]}])
    return skip_reason(facts)


def read_leads(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


FOUNDER_AREA = ("Navsari", "Surat")   # visited completely first (pilot area, CLAUDE.md)


def visit_order(urls_by_host: dict, leads: list[dict]) -> list[str]:
    """Hosts in visiting order: the founder's area first, then the other cities round-robin, so a time limit
    cuts every other city by about the same number of hosts instead of dropping whole cities."""
    order = {c: i for i, c in enumerate(CITIES)}
    city_of = {}
    for lead in leads:
        host = host_of(normal_url(lead["website"]))
        if order.get(lead["town"], 99) < order.get(city_of.get(host), 99):
            city_of[host] = lead["town"]
    by_city = defaultdict(list)
    for host in sorted(urls_by_host):
        by_city[city_of.get(host, "?")].append(host)
    first = [h for city in FOUNDER_AREA for h in by_city.pop(city, [])]
    rest, queues = [], [by_city[c] for c in CITIES if c in by_city] + [by_city[c] for c in by_city if c not in CITIES]
    while any(queues):
        for queue in queues:
            if queue:
                rest.append(queue.pop(0))
    return first + rest


def free_ram_mb() -> Optional[int]:
    """Free physical memory in MB (Windows; None elsewhere)."""
    if sys.platform != "win32":
        return None

    class MemoryStatus(ctypes.Structure):
        _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong), ("total_phys", ctypes.c_ulonglong),
                    ("avail_phys", ctypes.c_ulonglong), ("total_page", ctypes.c_ulonglong),
                    ("avail_page", ctypes.c_ulonglong), ("total_virtual", ctypes.c_ulonglong),
                    ("avail_virtual", ctypes.c_ulonglong), ("avail_extended", ctypes.c_ulonglong)]

    status = MemoryStatus()
    status.length = ctypes.sizeof(MemoryStatus)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        return None
    return status.avail_phys // (1024 * 1024)


async def _memory_low(min_free_mb: int, every_seconds: float = 30) -> int:
    """Returns once free RAM falls below min_free_mb (checked every 30 s). The 2026-11-12 crawl ended in a
    MemoryError while other programs left ~500 MB free; this stops the run cleanly first."""
    while True:
        await asyncio.sleep(every_seconds)
        free = free_ram_mb()
        if free is not None and free < min_free_mb:
            print(f"free RAM {free} MB < {min_free_mb} MB: stopping the visit", flush=True)
            return free


async def _visit_with_deadline(urls_by_host: dict, done: dict, out: Path, parallel: int, max_minutes: float,
                               min_free_mb: int = 0) -> Optional[str]:
    """Why the run stopped early ("time_limit" / "low_memory"), or None when every host was visited.
    A visits.jsonl line is written without an await in between, so stopping never leaves half a line."""
    visit = asyncio.ensure_future(run_visits(urls_by_host, done, out, parallel))
    guard = asyncio.ensure_future(_memory_low(min_free_mb)) if min_free_mb else None
    waiting = {visit} | ({guard} if guard else set())
    finished, pending = await asyncio.wait(waiting, timeout=max_minutes * 60 if max_minutes else None,
                                           return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)
    if visit in finished:
        visit.result()   # re-raise a crash instead of hiding it
        return None
    return "low_memory" if guard in finished else "time_limit"


def visit_leads(leads: list[dict], out: Path, parallel: int, max_hosts: int = 0, max_minutes: float = 0,
                write_only: bool = False, min_free_mb: int = 0) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    skipped = {l["id"]: rule9(l) for l in leads if rule9(l)}
    urls_by_host = defaultdict(list)
    for lead in leads:
        if lead["id"] not in skipped and has_address(lead):
            url = normal_url(lead["website"])
            if url not in urls_by_host[host_of(url)]:
                urls_by_host[host_of(url)].append(url)
    ordered = visit_order(urls_by_host, leads)
    if max_hosts:
        ordered = ordered[:max_hosts]
    urls_by_host = {h: urls_by_host[h] for h in ordered}
    done = load_done(out / "visits.jsonl")
    print(f"{len(leads)} leads, {len(skipped)} skipped by rule 9, {len(urls_by_host)} hosts, "
          f"{len(done)} URLs already visited, time limit {max_minutes or 'none'} min, "
          f"free RAM {free_ram_mb()} MB", flush=True)
    # write_only: no visit at all, only the outputs of what visits.jsonl already holds (after a stopped run)
    stopped = "write_only" if write_only else asyncio.run(
        _visit_with_deadline(urls_by_host, done, out, parallel, max_minutes, min_free_mb))
    visited_urls = set(done)
    kept = [l for l in leads if l["id"] in skipped or not has_address(l)
            or normal_url(l["website"]) in visited_urls]
    summary = write_outputs(kept, skipped, done, out)
    summary["capped"] = bool(stopped or max_hosts)
    summary["stopped"] = stopped   # None | time_limit | low_memory | write_only
    summary["leads_not_visited_because_of_cap"] = len(leads) - len(kept)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def step_recapture(out: Path, parallel: int) -> dict:
    rows = read_leads(PHASE14 / "sites.csv")
    leads = [r for r in rows if r["outcome"] == "ok" and r["has_viewport"] == "False"
             and int(r["emails_found"] or 0) > 0]
    return visit_leads(leads, out / "recapture_phase14", parallel)


async def _session_run(fn):
    from backend.app.database import Base, get_async_engine, get_async_session_factory
    import backend.app.models  # noqa: F401

    async with get_async_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with get_async_session_factory()() as session:
        result = await fn(session)
        await session.commit()
    await get_async_engine().dispose()
    return result


def step_import(out: Path) -> dict:
    from backend.app.services.email_finder_import import EmailFinderImporter

    async def run(session):
        results = {}
        for folder, origin in ((PHASE14, "email_finder:2026-11-10"),
                               (out / "recapture_phase14", "recapture_phase14:2026-11-12"),
                               (out, "pool_e1:2026-11-12")):
            if (folder / "sites.csv").exists():
                started = time.monotonic()
                results[origin] = await EmailFinderImporter(session).import_folder(folder, origin)
                await session.commit()
                print(f"imported {origin} in {time.monotonic() - started:.0f} s", flush=True)
        return results

    return asyncio.run(_session_run(run))


def step_render(out: Path) -> dict:
    from backend.app.engines.eligibility.render import RenderJob, evidence_dir, run_render_jobs, unsafe_reason
    from backend.app.services.eligibility_service import EligibilityService

    async def run(session):
        service = EligibilityService(session)
        candidates = await service.render_candidates()
        folder = evidence_dir()
        jobs, unsafe = [], {}
        for business_id, url in candidates:
            reason = await unsafe_reason(url)
            if reason:
                unsafe[business_id] = reason
                continue
            jobs.append(RenderJob(str(business_id), url, str(folder / f"render_{business_id}.png")))
        print(f"{len(candidates)} candidates, {len(jobs)} to render, {len(unsafe)} refused", flush=True)
        results = await asyncio.to_thread(run_render_jobs, jobs)
        stored = await service.record_render_results(results)
        return {"candidates": len(candidates), "rendered": len(jobs), "refused_by_ssrf_guard": len(unsafe),
                "stored_checks": stored, "outcomes": dict(Counter(r.outcome for r in results)),
                "evidence_dir": str(folder)}

    summary = asyncio.run(_session_run(run))
    (out / "render.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def step_evaluate(out: Path) -> dict:
    from backend.app.services.eligibility_service import EligibilityService

    async def run(session):
        return await EligibilityService(session).evaluate(verify=True)

    summary = asyncio.run(_session_run(run))
    (out / "evaluate.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def step_report(out: Path) -> dict:
    from sqlalchemy import select

    from backend.app.models.business import BusinessLocation, BusinessSourceLink
    from backend.app.models.eligibility import EmailEligibility
    from backend.app.models.source import SourceRecord

    async def run(session):
        city = {}
        for business_id, name in (await session.execute(
                select(BusinessLocation.business_id, BusinessLocation.city))).all():
            city.setdefault(business_id, name)
        origin = defaultdict(set)   # which imported folder(s) a business came from
        for business_id, raw in (await session.execute(
                select(BusinessSourceLink.business_id, SourceRecord.raw_data)
                .join(SourceRecord, SourceRecord.id == BusinessSourceLink.source_record_id))).all():
            if isinstance(raw, dict) and raw.get("import_origin"):
                origin[business_id].add(raw["import_origin"].split(":")[0])
        rows = (await session.execute(select(EmailEligibility))).scalars().all()
        report = {"generated_at": datetime.now(timezone.utc).isoformat(), "by_source": {}}
        for source in ("pool_e1", "email_finder", "all"):
            mine = [r for r in rows if source == "all" or source in origin[r.business_id]]
            groups = {"by_city": defaultdict(Counter), "by_vertical": defaultdict(Counter),
                      "by_city_vertical": defaultdict(Counter)}
            holds, observations = Counter(), Counter()
            for row in mine:
                keys = {"by_city": city.get(row.business_id) or "?", "by_vertical": row.vertical or "other"}
                keys["by_city_vertical"] = f"{keys['by_city']} / {keys['by_vertical']}"
                for group, key in keys.items():
                    groups[group][key]["rows"] += 1
                    groups[group][key]["eligible"] += int(row.eligible)
                    groups[group][key]["eligible_if_verified"] += int(row.eligible_if_verified)
                holds.update(row.hold_reasons or [])
                if row.observation_type:
                    observations[row.observation_type.value] += 1
            report["by_source"][source] = {
                "rows": len(mine), "businesses": len({r.business_id for r in mine}),
                "eligible": sum(r.eligible for r in mine),
                "eligible_if_verified": sum(r.eligible_if_verified for r in mine),
                "tiers": dict(Counter(r.tier.value for r in mine)),
                "recipient_types": dict(Counter(r.recipient_type.value for r in mine)),
                "verification": dict(Counter(r.verification_status.value for r in mine)),
                "observations": dict(observations), "holds_by_reason": dict(holds.most_common()),
                **{group: {k: dict(v) for k, v in sorted(table.items())} for group, table in groups.items()}}
        return report

    report = asyncio.run(_session_run(run))
    (out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("step", choices=["select", "visit", "recapture", "import", "render", "evaluate", "report"])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--parallel", type=int, default=10)
    parser.add_argument("--max-hosts", type=int, default=0, help="cap the visit (0 = no cap)")
    parser.add_argument("--max-minutes", type=float, default=0, help="stop visiting after N minutes (0 = no limit)")
    parser.add_argument("--min-free-mb", type=int, default=500,
                        help="stop visiting when free RAM falls below this (0 = no check)")
    parser.add_argument("--write-only", action="store_true",
                        help="visit nothing; write sites.csv / emails.csv / summary.json from visits.jsonl")
    args = parser.parse_args()
    if args.step == "select":
        result = step_select(args.out)
    elif args.step == "visit":
        result = visit_leads(read_leads(args.out / "leads.csv"), args.out, args.parallel, args.max_hosts,
                             args.max_minutes, args.write_only, args.min_free_mb)
    elif args.step == "recapture":
        result = step_recapture(args.out, args.parallel)
    elif args.step == "import":
        result = step_import(args.out)
    elif args.step == "render":
        result = step_render(args.out)
    elif args.step == "evaluate":
        result = step_evaluate(args.out)
    else:
        result = step_report(args.out)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
