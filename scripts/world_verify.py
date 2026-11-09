"""
Check a reference list of states / cities (from ChatGPT, `CC|state|city|lat|lon|kind` lines) against the
extracted world data: is there business data at each city?

A city counts as covered when the extracted places of its country include businesses within RADIUS_KM of the
given point, or businesses whose address city has the same name. The count near the point is reported, so a
wrong coordinate shows up as "0 near, N by name".

Usage:  python scripts/world_verify.py <reply.md> <round-number> [--out E:/SiteBlitz-World-Business-Data]
Writes  <out>/verification/round_NN.csv, appends to <out>/verification/all_reference_cities.csv,
and prints a short summary (used as feedback in the next ChatGPT message).
"""

import argparse
import csv
import math
import re
import sys
import unicodedata
from pathlib import Path

import duckdb

RADIUS_KM = 10.0
LINE = re.compile(r"^\s*([A-Z]{2})\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|\s*([A-Za-z]*)\s*$")


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", (text or "").casefold())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[\W_]+", " ", text).strip()


def parse(reply: str) -> list[dict]:
    rows = []
    for line in reply.splitlines():
        m = LINE.match(line.strip().strip("`"))
        if not m:
            continue
        cc, state, city, lat, lon, kind = (g.strip() for g in m.groups())
        try:
            la, lo = float(lat), float(lon)
        except ValueError:
            la = lo = None
        rows.append({"cc": cc, "state": state, "city": city, "lat": la, "lon": lo, "kind": kind or ""})
    return rows


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    ap = argparse.ArgumentParser()
    ap.add_argument("reply")
    ap.add_argument("round", type=int)
    ap.add_argument("--out", default="E:/SiteBlitz-World-Business-Data")
    a = ap.parse_args()
    out = Path(a.out)
    by_country = out / "_work" / "by_country"
    rows = parse(Path(a.reply).read_text(encoding="utf-8"))
    con = duckdb.connect()
    loaded: set[str] = set()
    results = []
    for r in rows:
        cc = r["cc"]
        part = by_country / f"country={cc}"
        near = by_name = 0
        if r["city"] in ("", "-") or r["kind"] == "none":
            status = "no city (uninhabited)"
        elif not part.exists():
            status = "NO DATA FOR COUNTRY"
        else:
            if cc not in loaded:
                con.execute(f"CREATE OR REPLACE TABLE t_{cc} AS SELECT lat, lon, city FROM read_parquet('{(part / '*.parquet').as_posix()}')")
                loaded.add(cc)
            if r["lat"] is not None:
                dlat = RADIUS_KM / 111.0
                dlon = RADIUS_KM / (111.0 * max(math.cos(math.radians(r["lat"])), 0.1))
                near = con.execute(f"SELECT count(*) FROM t_{cc} WHERE lat BETWEEN ? AND ? AND lon BETWEEN ? AND ?",
                                   [r["lat"] - dlat, r["lat"] + dlat, r["lon"] - dlon, r["lon"] + dlon]).fetchone()[0]
            wanted = norm(r["city"])
            names = con.execute(f"SELECT city, count(*) FROM t_{cc} WHERE city IS NOT NULL GROUP BY 1").fetchall() \
                if wanted else []
            by_name = sum(n for c, n in names if norm(c) == wanted)
            status = "covered" if (near or by_name) else "NOT COVERED"
        results.append({**r, "businesses_within_10km": near, "businesses_with_city_name": by_name, "status": status})
    vdir = out / "verification"
    vdir.mkdir(exist_ok=True)
    fields = ["cc", "state", "city", "lat", "lon", "kind", "businesses_within_10km", "businesses_with_city_name", "status"]
    with open(vdir / f"round_{a.round:02d}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)
    all_path = vdir / "all_reference_cities.csv"
    new_file = not all_path.exists()
    with open(all_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["round"] + fields)
        if new_file:
            w.writeheader()
        w.writerows({"round": a.round, **r} for r in results)
    cities = [r for r in results if r["status"] in ("covered", "NOT COVERED", "NO DATA FOR COUNTRY")]
    covered = [r for r in cities if r["status"] == "covered"]
    print(f"Round {a.round}: {len(rows)} reference lines, {len(cities)} cities, {len(covered)} with business data "
          f"({100 * len(covered) / max(len(cities), 1):.0f} %).")
    by_cc: dict[str, list] = {}
    for r in cities:
        by_cc.setdefault(r["cc"], []).append(r)
    for cc, rs in sorted(by_cc.items()):
        miss = [r["city"] for r in rs if r["status"] != "covered"]
        print(f"- {cc}: {sum(r['status'] == 'covered' for r in rs)}/{len(rs)} cities covered, "
              f"{sum(r['businesses_within_10km'] for r in rs):,} businesses near them"
              + (f"; no data at: {', '.join(miss[:12])}" if miss else ""))


if __name__ == "__main__":
    main()
