# E1 eligibility run - 2026-11-12

Email engine v2, phase E1 (`docs/spec/email-engine-v2.md` rows 2-4). Scripts: `scripts/pool_e1.py` (select, visit,
recapture, import, render, evaluate, report) and `scripts/render_check.cjs`. Nothing was sent, submitted or logged
into; the only network use was polite GET visits, the rendered phone checks of 46 homepages and DNS (MX) lookups.

Outputs (business data, outside the repository): `E:\SiteBlitz-World-Business-Data\_work\pool_e1\2026-11-12\`
(`leads.csv`, `visits.jsonl`, `sites.csv`, `emails.csv`, `summary.json`, `select.json`, `render*.json`,
`evaluate.json`, `report.json`, logs) and the phone screenshots in `...\_work\evidence\2026-11-12\`. Imported into the
app database `siteblitz_leads.db` (it was empty; a backup of every stage is in the `backup\` folder there).

## Result in one line
**0 addresses are eligible today, because no verifier key is configured. 26 would be eligible once a verifier says
VALID** (24 from the new pool, 2 from the phase-14 run). All 26 carry a NO_VIEWPORT observation backed by a phone
screenshot. That is far below 100.

## The crawl stopped at 9,205 of 13,185 hosts
| Run | Time (IST) | What happened |
|---|---|---|
| 1 | 10:54-11:05 | Started in alphabetical city order at ~39 hosts/min, too slow for the ~4 h limit; stopped by hand and restarted with Navsari + Surat first, then the other cities round-robin |
| 2 | 11:06-12:48 | 101 minutes, ~5,250 hosts, then a **MemoryError** inside the viewport check (`WebsiteAuditor.audit_html` lowercasing a page) while the machine had ~500 MB free RAM |
| 3 | 13:57-13:58 | Resumed after the memory fixes (5 hosts in parallel, 1,738 MB free at start); the new guard stopped it after ~1 minute when free RAM fell to 422 MB (the crawl process itself used 173 MB) |
| 4 | 14:00-14:58 | Resumed with 1,224 MB free; ran the full 58-minute limit with no memory trouble |

In all: 9,866 URLs on 9,205 hosts (27,312 requests), 10,725 of the 15,300 visitable leads. Navsari and Surat were
visited completely; the other 9 cities in part (round-robin, so each lost about the same number of hosts). 3,980
hosts / 4,575 leads were not visited. The crawl was not continued further: the eligible-but-unverified pool grows by
about 2-3 per 1,000 hosts, so the rest would not get it near 100.

The memory fixes and the reasons are in `docs/DECISIONS.md` (2026-11-12, "E1 pool crawl: MemoryError").

## Selection (`IN_businesses.zip`, exact city name, Gujarat)
| Step | Count |
|---|---|
| Rows scanned | 4,673,948 |
| Exact city match on the 11 cities (state Gujarat or blank) | 221,478 (297 more rows had another state) |
| In the three verticals (phase-14 category mapping) | 64,626 |
| Left out: Overture brand / no website / social-media "website" / host already visited in phase 14 | 2,944 / 39,114 / 93 / 5,136 |
| **Selected** | **17,339** leads on 13,185 hosts |
| Website-intelligence rule 9 (schools, colleges ...), recorded, not visited | 2,039 |

`IN_businesses.zip` has no `operating_status` column, so permanently closed places could not be left out (phase 14
could).

## Per city and vertical (pool only)
"Selected" includes the rule-9 leads (all of them coaching: e.g. Surat 374, Navsari 27), which are never visited.
"With an email" = leads whose own pages showed at least one address. "NO_VIEWPORT" = reachable HTML homepages with no
viewport tag in the source (a signal only; the observation needs the phone check).

| City | Vertical | Selected | Visited | With an email | NO_VIEWPORT | Eligible once verified |
|---|---|---|---|---|---|---|
| Navsari | salon_beauty | 4 | 4 | 3 | 0 | 0 |
| Navsari | coaching_tuition | 47 | 20 | 12 | 2 | 1 |
| Navsari | retail_showroom | 83 | 83 | 22 | 2 | 0 |
| Surat | salon_beauty | 295 | 295 | 91 | 8 | 0 |
| Surat | coaching_tuition | 978 | 604 | 217 | 27 | 2 |
| Surat | retail_showroom | 2,898 | 2,898 | 846 | 93 | 4 |
| Ahmedabad | salon_beauty | 603 | 153 | 64 | 13 | 0 |
| Ahmedabad | coaching_tuition | 2,442 | 1,023 | 414 | 29 | 1 |
| Ahmedabad | retail_showroom | 4,027 | 1,062 | 363 | 48 | 4 |
| Vadodara | salon_beauty | 208 | 168 | 49 | 5 | 0 |
| Vadodara | coaching_tuition | 924 | 531 | 244 | 16 | 2 |
| Vadodara | retail_showroom | 1,153 | 938 | 275 | 43 | 0 |
| Rajkot | salon_beauty | 106 | 105 | 35 | 4 | 0 |
| Rajkot | coaching_tuition | 491 | 255 | 97 | 8 | 0 |
| Rajkot | retail_showroom | 1,132 | 1,106 | 382 | 54 | 5 |
| Bharuch | salon_beauty | 17 | 16 | 3 | 0 | 0 |
| Bharuch | coaching_tuition | 77 | 28 | 12 | 2 | 0 |
| Bharuch | retail_showroom | 104 | 100 | 26 | 5 | 1 |
| Valsad | salon_beauty | 3 | 3 | 1 | 0 | 0 |
| Valsad | coaching_tuition | 43 | 24 | 11 | 3 | 0 |
| Valsad | retail_showroom | 75 | 71 | 18 | 6 | 2 |
| Anand | salon_beauty | 23 | 23 | 6 | 0 | 0 |
| Anand | coaching_tuition | 138 | 91 | 36 | 1 | 0 |
| Anand | retail_showroom | 158 | 150 | 38 | 4 | 0 |
| Gandhinagar | salon_beauty | 38 | 35 | 12 | 1 | 0 |
| Gandhinagar | coaching_tuition | 393 | 206 | 72 | 7 | 0 |
| Gandhinagar | retail_showroom | 217 | 204 | 76 | 7 | 1 |
| Bhavnagar | salon_beauty | 20 | 20 | 6 | 0 | 0 |
| Bhavnagar | coaching_tuition | 125 | 61 | 24 | 4 | 0 |
| Bhavnagar | retail_showroom | 184 | 176 | 57 | 5 | 0 |
| Jamnagar | salon_beauty | 13 | 13 | 5 | 0 | 0 |
| Jamnagar | coaching_tuition | 114 | 61 | 22 | 3 | 1 |
| Jamnagar | retail_showroom | 206 | 198 | 48 | 11 | 0 |
| **Total** | | **17,339** | **10,725** | **3,587** | **411** | **24** |

With the 2 phase-14 leads (both Surat: 1 coaching, 1 retail), eligible once verified = **26**: by vertical salon 0,
coaching 8, retail 18; by city Surat 8, Ahmedabad 5, Rajkot 5, Vadodara 2, Valsad 2, Navsari 1, Bharuch 1,
Gandhinagar 1, Jamnagar 1, Anand 0, Bhavnagar 0.

## Visits (pool)
| Measure | Count |
|---|---|
| Outcomes of the 10,725 visited leads | ok 5,740 · failed 4,383 · robots-blocked 346 · protected (401/403/429 or a challenge page) 200 · SSRF-blocked 26 · listing 20 · social 10 |
| Failed, by reason (per URL) | no DNS record 2,779 · timeout 794 · connect 167 · HTTP 404 189 · HTTP 500/503 42 · parked 30 · other 105 (4,106 URLs) |
| Leads with an email on their own pages | 3,587 (4,662 lead-address rows, 3,841 distinct addresses) |
| Address methods | mailto 2,974 · visible text 1,163 · Cloudflare 520 · "[at] [dot]" 5 |
| Free-mail addresses / on the site's own domain | 1,691 / 2,474 |
| Every address has its page excerpt (<= 300 characters) | 4,662 of 4,662 sightings |
| NO_VIEWPORT (source) / no HTTPS | 411 / 889 |
| Hosts carrying 3+ leads (chain store locators) | 169 hosts, 969 leads, 385 of them with an email |

## Rendered phone checks (390 x 844, deviceScaleFactor 3)
Only NO_VIEWPORT sites that showed an address were rendered: 44 from the pool and the 2 from phase 14 = **46 sites**.
Latest result per site: **ZOOMED_OUT 28**, fits 16 (the page source had no viewport tag, but the page still fitted
the phone), error 2 (failed twice; they stay HOLD `PHONE_CHECK_PENDING`). All 46 URLs passed the SSRF guard. 50
render checks in all (2 retries of the errors, and 2 sites rendered twice because of the time-zone bug below).

## Eligibility (all imported leads: phase 14 + recapture + pool)
12,428 address rows on 9,646 businesses. Tiers: Tier 1 4,664 · Tier 2 (listing only) 6,927 · HOLD (provenance
incomplete) 837. Recipient type: business 9,462 · unknown 2,761 · employee-like 205. Verifier status: UNVERIFIED
12,428 (no key; 26 candidates passed the free MX check).

| HOLD reason (a row can have several) | Rows |
|---|---|
| NOT_VERIFIED | 12,428 |
| NO_PILOT_OBSERVATION | 8,714 |
| LISTING_ONLY | 6,927 |
| SITE_DOWN_NEEDS_RECHECK | 3,379 |
| NOT_PRIMARY_RECIPIENT | 2,782 |
| CHAIN_OR_DIRECTORY | 1,352 |
| PROVENANCE_INCOMPLETE | 837 |
| DUPLICATE_RECIPIENT | 797 |
| PHONE_CHECK_PENDING | 293 |
| EMPLOYEE_LIKE_ADDRESS | 205 |
| SYSTEM_ADDRESS | 21 |

The 26 rows eligible once verified: all NO_VIEWPORT with a phone screenshot; methods mailto 13, visible text 10,
Cloudflare 3; recipient type business 22, unknown 4.

## Phase-14 import (old board row 14b)
2,014 visited leads -> 2,014 businesses, 2,014 website checks, 839 address rows (as in phase 14), 148 leads not
imported (69 rule-9 skips, 79 empty website fields). A second import added nothing. Because phase 14 kept no page
excerpts, 837 rows are HOLD `PROVENANCE_INCOMPLETE`; they have no pilot observation either. The 2 phase-14 leads
that could qualify (no viewport tag + an address) were visited once more (2 sites, 6 requests) to capture excerpts,
and both opened zoomed-out. Result: 499 businesses, 2 eligible once verified.

## What the numbers mean
- **The verifier key is the next blocker.** With `BOUNCER_API_KEY` set, `POST /api/v1/outreach/eligibility/evaluate`
  with `{"verify": true}` checks only the 26 candidates (about $0.21 at $8 per 1,000).
- **26 is far below the 100 the pilot needs.** NO_VIEWPORT is rare among sites that show an address (44 of the 3,587 pool leads with an address).
  Other observation types would need their own route:
  - SITE_DOWN cannot come from this pool: a site that is down shows no pages, so it gives no Tier 1 address. The 3,379
    rows on sites that failed once all have only a listing address (Tier 2) anyway.
  - SOCIAL_ONLY needs businesses without a website and the founder's Instagram check; the database holds none yet
    (the pool selected businesses with a website), so `GET /api/v1/outreach/confirmations/pending` is empty.
- 6,927 listing-only rows show how much of the Overture contact data cannot be used under spec row 3.

## Problems found and fixed during the run
- Memory: see the DECISIONS entry (viewport check ~97 MB -> ~0 MB per 2 MB page, scripts cut before parsing, bodies
  released, queue workers, a free-RAM guard at 500 MB).
- Time zone: imported visit times were kept in IST and read back as UTC (5 h 30 min late). Fixed in the importer;
  the rows already imported were corrected once (backup kept).

## Not done
- No second homepage check (>= 6 h later) of the sites that failed once - neither the 701 phase-14 sites (old 14b)
  nor the pool's. None of them has a Tier 1 address, so it cannot change eligibility; it only matters for the letter
  route later.
- 3,980 hosts of the selection were not visited (see above).
- No paid verification (no key).
