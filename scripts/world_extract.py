"""
World business extract - every Overture place of every country, organised by country / state / city,
compressed, in one folder that can be shared.

Why a bulk extract instead of one app search per city (2026-11-08): one search takes 40-150 s and the
world has tens of thousands of cities; reading the whole Overture Places release once (16 files,
~90 M places) covers every city the source knows in a few hours.

Passes (each resumable - finished outputs are skipped):
  download  S3 release -> <out>/_work/raw/part-NNNNN.parquet      (selected columns, flattened)
  split     raw -> <out>/_work/by_country/country=XX/*.parquet     (one pass, partitioned)
  export    per country -> <out>/countries/<CC> <Name>/            (ZIP of Excel-sized CSV parts + indexes)
  summary   <out>/world_summary.csv

Licence: Overture Places is CDLA Permissive 2.0 / Apache 2.0 / CC0 (no OpenStreetMap data, no ODbL); the
output keeps a LICENSE / attribution file. Query values are parameters or fixed column lists.

Usage:  python scripts/world_extract.py <pass> [--out E:/SiteBlitz-World-Business-Data] [--release 2026-10-21.0]
"""

import argparse
import csv
import re
import shutil
import sys
import time
import unicodedata
import zipfile
from pathlib import Path

import duckdb

DEFAULT_OUT = "E:/SiteBlitz-World-Business-Data"
DEFAULT_RELEASE = "2026-10-21.0"

# Social hosts - the same platforms the app recognises (overture.py SOCIAL_HOSTS).
SOCIAL = {
    "facebook": r"(^|\.)(facebook\.com|fb\.com|fb\.me)$",
    "instagram": r"(^|\.)instagram\.com$",
    "linkedin": r"(^|\.)linkedin\.com$",
    "tiktok": r"(^|\.)tiktok\.com$",
    "youtube": r"(^|\.)(youtube\.com|youtu\.be)$",
    "twitter": r"(^|\.)(twitter\.com|x\.com)$",
    "whatsapp": r"(^|\.)(wa\.me|whatsapp\.com)$",
    "linktree": r"(^|\.)linktr\.ee$",
}
# Listing pages are not the business's own website (checks.py LISTING_HOSTS, short form).
LISTING = (r"(^|\.)(g\.co|google\.[a-z.]+|goo\.gl|business\.site|justdial\.com|practo\.com|zomato\.com|"
           r"swiggy\.com|tripadvisor\.[a-z.]+|yelp\.[a-z.]+|booking\.com|foursquare\.com)$")
HOST = r"^[a-zA-Z]+://(www\.)?([^/:?#]+)"

ROWS_PER_PART = 1_000_000      # Excel opens at most 1,048,576 rows per sheet
BOM = b"\xef\xbb\xbf"          # so Excel reads the CSV as UTF-8 (names in any script)


# Codes outside ISO 3166-1 that the source uses (Kosovo) or that this extract uses (ZZ).
EXTRA_NAMES = {"XK": "Kosovo", "ZZ": "Unclear country in source"}


def _country_names(out: Path) -> dict[str, str]:
    names = {r["code"]: r["name"] for r in csv.DictReader(open(out / "countries_A_to_Z.csv", encoding="utf-8"))}
    return {**names, **EXTRA_NAMES}


def connect() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")
    con.execute("SET preserve_insertion_order = false;")
    return con


def log(msg: str) -> None:
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def download(out: Path, release: str) -> None:
    raw = out / "_work" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    con = connect()
    files = [r[0] for r in con.execute(
        "SELECT file FROM glob(?) ORDER BY file",
        [f"s3://overturemaps-us-west-2/release/{release}/theme=places/type=place/*"]).fetchall()]
    log(f"{len(files)} source files")
    for i, src in enumerate(files):
        dest = raw / f"part-{i:05d}.parquet"
        if dest.exists():
            continue
        tmp = raw / f"part-{i:05d}.tmp"
        tmp.unlink(missing_ok=True)
        t = time.time()
        # One file at a time so an interrupted run resumes at the next file. `src` comes from the
        # glob above (S3 listing), not from user input.
        con.execute(f"""
            COPY (
              SELECT id,
                     names.primary AS name,
                     basic_category,
                     taxonomy.primary AS category,
                     confidence,
                     operating_status,
                     websites, socials, emails, phones,
                     brand.names.primary AS brand,
                     upper(addresses[1].country) AS country,
                     addresses[1].region AS state,
                     addresses[1].locality AS city,
                     addresses[1].postcode AS postcode,
                     addresses[1].freeform AS address,
                     round((bbox.ymin + bbox.ymax) / 2, 6) AS lat,
                     round((bbox.xmin + bbox.xmax) / 2, 6) AS lon
              FROM read_parquet('{src}')
              WHERE names.primary IS NOT NULL
                AND coalesce(operating_status, '') <> 'permanently_closed'
            ) TO '{tmp.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)""")
        tmp.rename(dest)
        log(f"file {i + 1}/{len(files)} done in {time.time() - t:.0f}s ({dest.stat().st_size / 1e6:.0f} MB)")


def split(out: Path) -> None:
    """raw -> by_country/country=XX/pNNNNN_*.parquet, one raw file at a time.

    Why per file (2026-11-09): one COPY of all 86.7 M rows partitioned by country spilled 16.4 GB to
    disk and failed with "Out of Memory". One raw file (~5.5 M rows) at a time stays small. A marker
    per finished raw file makes the pass resumable; an interrupted file's outputs are removed first.
    """
    raw = out / "_work" / "raw"
    dest = out / "_work" / "by_country"
    marks = out / "_work" / "split_done"
    dest.mkdir(parents=True, exist_ok=True)
    marks.mkdir(parents=True, exist_ok=True)
    con = connect()
    con.execute(f"SET temp_directory = '{(out / '_work' / 'duckdb_spill').as_posix()}'")
    con.execute("SET memory_limit = '6GB'")
    # The source's country field holds 158 values that are not ISO codes (30,093 of 86.7 M places:
    # "IN-MH", "MUMBAI", postcodes, ' NASHIK"' ...). A state-style code keeps its country ("IN-MH" -> IN);
    # the rest go to ZZ, so no folder is named after junk (and no quote reaches a Windows path).
    valid = sorted(_country_names(out))
    assert all(re.fullmatch(r"[A-Z]{2}", c) for c in valid)
    in_list = ", ".join(f"'{c}'" for c in valid)
    files = sorted(raw.glob("part-*.parquet"))
    for f in files:
        idx = f.stem.split("-")[1]
        mark = marks / f"{idx}.done"
        if mark.exists():
            continue
        for old in dest.glob(f"country=*/p{idx}_*.parquet"):
            old.unlink()
        t = time.time()
        con.execute(f"""
            COPY (SELECT * REPLACE (
                    CASE WHEN country IN ({in_list}) THEN country
                         WHEN left(country, 2) IN ({in_list}) AND substr(country, 3, 1) = '-' THEN left(country, 2)
                         ELSE 'ZZ' END AS country)
                  FROM read_parquet('{f.as_posix()}'))
            TO '{dest.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD, PARTITION_BY (country),
                                    APPEND, FILENAME_PATTERN 'p{idx}_{{uuid}}')""")
        mark.write_text("ok", encoding="utf-8")
        log(f"split {f.name} done in {time.time() - t:.0f}s")
    log(f"split done: {len(list(dest.iterdir()))} countries")


def _host(col: str) -> str:
    return f"lower(coalesce(regexp_extract({col}, '{HOST}', 2), ''))"


def _export_sql(src: str, cc: str) -> str:
    """Flatten one country's places to the CSV columns (own website, one column per social platform).

    A place without a state gets the state most other places of the same city carry (Overture gives the
    city for ~99 % of places but the state for ~1 in 3); `state_from` says which it is.
    """
    social_cols = ",\n".join(
        f"list_filter(coalesce(websites, []) || coalesce(socials, []), "
        f"lambda x: regexp_matches({_host('x')}, '{rx}'))[1] AS {name}"
        for name, rx in SOCIAL.items())
    any_social = "|".join(f"({rx})" for rx in SOCIAL.values())
    return f"""
        WITH p0 AS (
          SELECT *, nullif(trim(state), '') AS st_raw, nullif(trim(city), '') AS ci
          FROM read_parquet('{src}')
        ),
        p AS (
          SELECT p0.*, coalesce(m.state_name, p0.st_raw) AS st,
                 list_filter(coalesce(websites, []),
                             lambda x: NOT regexp_matches({_host('x')}, '{any_social}|{LISTING}')) AS own_sites
          FROM p0 LEFT JOIN state_map m
            ON m.cc = '{cc}' AND m.k = regexp_replace(lower(strip_accents(p0.st_raw)), '\s+', ' ', 'g')
        ),
        city_state AS (SELECT ci, mode(st) AS st_guess FROM p WHERE st IS NOT NULL AND ci IS NOT NULL GROUP BY ci)
        SELECT id AS overture_id, name, coalesce(category, basic_category) AS category, brand,
               coalesce(p.st, city_state.st_guess, '(state not given)') AS state,
               CASE WHEN p.st IS NOT NULL THEN 'address' WHEN city_state.st_guess IS NOT NULL THEN 'same city'
                    ELSE '' END AS state_from,
               coalesce(p.ci, '(city not given)') AS city,
               postcode, address, lat, lon,
               array_to_string(coalesce(phones, []), ' | ') AS phones,
               array_to_string(coalesce(emails, []), ' | ') AS emails,
               own_sites[1] AS website,
               {social_cols},
               CASE WHEN len(own_sites) > 0 THEN 'has website'
                    WHEN len(coalesce(socials, [])) > 0 OR len(coalesce(websites, [])) > 0 THEN 'social only, no website'
                    ELSE 'no website, no social' END AS online_presence,
               round(confidence, 3) AS confidence
        FROM p LEFT JOIN city_state USING (ci)
    """


def _plain(text: str) -> str:
    """Accent-free text: ISO writes "Mahārāshtra", maps and people write "Maharashtra"."""
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def _key(text: str) -> str:
    return re.sub(r"\s+", " ", _plain(text).lower()).strip()


# Replaced ISO 3166-2 codes -> current code (Odisha, Uttarakhand, Telangana, Chhattisgarh).
OLD_SUBDIVISION_CODES = {"IN-OR": "IN-OD", "IN-UT": "IN-UK", "IN-TG": "IN-TS", "IN-CT": "IN-CG"}


def build_state_map(out: Path) -> Path:
    """country, key -> state name, from ISO 3166-2 (pycountry), so "MH", "IN-MH", "Maharashtra" and
    "maharashtra" all become "Maharashtra", and "Dhaka Division" becomes "Dhaka".

    Why (2026-11-09): the source gives the state as a code for some places and a name for others (India's
    index had "MH" 568,802 rows next to "Maharashtra"), so one state appeared as several.
    Top-level subdivisions win; a lower-level one (district) maps to its top-level parent only when that key
    is not already taken.
    """
    import pycountry  # imported here: only the export pass needs it

    dest = out / "_work" / "state_map.csv"
    by_code = {s.code: s for s in pycountry.subdivisions}

    def top(sub):
        while getattr(sub, "parent_code", None) and sub.parent_code in by_code:
            sub = by_code[sub.parent_code]
        return sub

    rows: dict[tuple[str, str], str] = {}
    for level in ("top", "child"):
        for sub in pycountry.subdivisions:
            is_top = not getattr(sub, "parent_code", None)
            if (level == "top") != is_top:
                continue
            cc, suffix = sub.code.split("-", 1)
            canonical = _plain(top(sub).name)
            keys = {suffix, sub.code, sub.name, f"{sub.name} {sub.type}"}
            for k in keys:
                rows.setdefault((cc, _key(k)), canonical)
    # Older ISO 3166-2 codes the source still uses (India's index kept "OR" 22,398, "UT", "TG", "CT").
    for old_code, new_code in OLD_SUBDIVISION_CODES.items():
        cc, suffix = old_code.split("-", 1)
        if new_code in by_code:
            rows.setdefault((cc, _key(suffix)), _plain(top(by_code[new_code]).name))
            rows.setdefault((cc, _key(old_code)), _plain(top(by_code[new_code]).name))
    with open(dest, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cc", "k", "state_name"])
        for (cc, k), v in rows.items():
            w.writerow([cc, k, v])
    return dest


def _copy_with_bom(con, sql: str, dest: Path, tmp_dir: Path) -> None:
    tmp = tmp_dir / (dest.name + ".tmp")
    con.execute(f"COPY ({sql}) TO '{tmp.as_posix()}' (HEADER)")
    with open(dest, "wb") as f, open(tmp, "rb") as src:
        f.write(BOM)
        shutil.copyfileobj(src, f, 1 << 20)
    tmp.unlink()


def export(out: Path, only: list[str] | None = None, redo: bool = False) -> None:
    by_country = out / "_work" / "by_country"
    tmp_dir = out / "_work" / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    names = _country_names(out)
    dest_root = out / "countries"
    dest_root.mkdir(exist_ok=True)
    con = connect()
    con.execute(f"SET temp_directory = '{(out / '_work' / 'duckdb_spill').as_posix()}'")
    con.execute("SET memory_limit = '8GB'")
    state_map = build_state_map(out)
    con.execute(f"CREATE OR REPLACE TABLE state_map AS SELECT * FROM read_csv('{state_map.as_posix()}', header=true, all_varchar=true)")
    for part in sorted(by_country.iterdir()):
        cc = part.name.split("=", 1)[1]
        if only and cc not in only:
            continue
        name = re.sub(r'[<>:"/\\|?*]', "", names.get(cc, "Unknown country" if cc == "ZZ" else cc))
        folder = dest_root / f"{cc} {name}"
        done_flag = folder / ".done"
        if done_flag.exists() and not (redo and "v2" not in done_flag.read_text(encoding="utf-8")):
            continue
        folder.mkdir(exist_ok=True)
        src = (part / "*.parquet").as_posix()
        t = time.time()
        con.execute("CREATE OR REPLACE TEMP TABLE c AS SELECT *, row_number() OVER (ORDER BY state, city, name) AS rn "
                    f"FROM ({_export_sql(src, cc)})")
        total = con.execute("SELECT count(*) FROM c").fetchone()[0]
        parts = max(1, -(-total // ROWS_PER_PART))
        with zipfile.ZipFile(folder / f"{cc}_businesses.zip", "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            for k in range(parts):
                tmp = tmp_dir / f"{cc}_{k}.csv"
                con.execute(f"COPY (SELECT * EXCLUDE (rn) FROM c WHERE rn > {k * ROWS_PER_PART} "
                            f"AND rn <= {(k + 1) * ROWS_PER_PART} ORDER BY rn) TO '{tmp.as_posix()}' (HEADER)")
                entry = f"{cc}_businesses.csv" if parts == 1 else f"{cc}_businesses_part{k + 1:02d}_of_{parts:02d}.csv"
                with zf.open(entry, "w", force_zip64=True) as dst, open(tmp, "rb") as srcf:
                    dst.write(BOM)
                    shutil.copyfileobj(srcf, dst, 1 << 20)
                tmp.unlink()
        _copy_with_bom(con, """
            SELECT state, city, count(*) AS businesses,
                   count(*) FILTER (WHERE phones <> '') AS with_phone,
                   count(*) FILTER (WHERE emails <> '') AS with_email,
                   count(*) FILTER (WHERE online_presence = 'has website') AS with_website,
                   count(*) FILTER (WHERE online_presence = 'social only, no website') AS social_only_no_website,
                   count(*) FILTER (WHERE online_presence = 'no website, no social') AS no_website_no_social
            FROM c GROUP BY ALL ORDER BY state, businesses DESC""", folder / f"{cc}_states_and_cities.csv", tmp_dir)
        _copy_with_bom(con, """
            SELECT category, count(*) AS businesses,
                   count(*) FILTER (WHERE phones <> '') AS with_phone,
                   count(*) FILTER (WHERE online_presence = 'social only, no website') AS social_only_no_website,
                   count(*) FILTER (WHERE online_presence = 'no website, no social') AS no_website_no_social
            FROM c GROUP BY ALL ORDER BY businesses DESC""", folder / f"{cc}_categories.csv", tmp_dir)
        con.execute("DROP TABLE c")
        done_flag.write_text(f"{time.strftime('%Y-%m-%d %H:%M:%S')} rows={total} v2", encoding="utf-8")
        log(f"{cc} {name}: {total:,} businesses in {parts} part(s), {time.time() - t:.0f}s")


def summary(out: Path) -> None:
    con = connect()
    rows = []
    names = _country_names(out)
    present = set()
    for folder in sorted((out / "countries").iterdir()):
        idx = next(folder.glob("*_states_and_cities.csv"), None)
        if not idx:
            continue
        r = con.execute(f"""SELECT count(DISTINCT state), count(DISTINCT city), sum(businesses), sum(with_phone),
                                   sum(with_email), sum(with_website), sum(social_only_no_website), sum(no_website_no_social)
                            FROM read_csv('{idx.as_posix()}', header=true)""").fetchone()
        cc = folder.name.split(" ", 1)[0]
        present.add(cc)
        rows.append([cc, names.get(cc, folder.name[3:]), *r])
    for cc, name in names.items():
        if cc not in present:
            rows.append([cc, name, 0, 0, 0, 0, 0, 0, 0, 0])
    rows.sort(key=lambda r: r[1])
    with open(out / "world_summary.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["code", "country", "states", "cities", "businesses", "with_phone", "with_email",
                    "with_website", "social_only_no_website", "no_website_no_social"])
        w.writerows(rows)
    log(f"summary: {len(present)} countries with data, {sum(r[4] or 0 for r in rows):,} businesses")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["download", "split", "export", "summary"])
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--release", default=DEFAULT_RELEASE)
    ap.add_argument("--only", nargs="*", help="export only these country codes")
    ap.add_argument("--redo", action="store_true", help="export again every country not yet in the v2 layout")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    {"download": lambda: download(out, a.release), "split": lambda: split(out),
     "export": lambda: export(out, a.only, a.redo), "summary": lambda: summary(out)}[a.step]()
