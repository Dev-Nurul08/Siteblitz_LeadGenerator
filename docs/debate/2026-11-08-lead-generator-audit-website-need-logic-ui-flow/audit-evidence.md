# Verified audit evidence — SiteBlitz Lead Generator (commit 2705aca, 2026-11-08)

Stack: FastAPI + SQLAlchemy async (Postgres default, SQLite supported) backend, React 19 + Vite
frontend (no router, no CSS framework; one page uses Tailwind class names but Tailwind is not
installed). 5 "engines": discovery → opportunity → enrichment → qualification → conversion.
136 unit tests pass, all mocked; no integration test. Redis/RQ declared but never used.

## A. Confirmed by running the code (live probe 2026-11-08)
| # | What happens | Root cause |
|---|---|---|
| A1 | `pip install -e ".[dev]"` (README step) fails: `No module named 'setuptools.backends'` | pyproject.toml:3 build-backend is invalid |
| A2 | App import crashes: `ModuleNotFoundError: dns` | engines/enrichment/verifier.py:12 imports dnspython, which is only in the optional `phase3` extra |
| A3 | Every OSM discovery returns 0 results (job PARTIAL, 1 error) | Overpass answers HTTP 406 to httpx's default User-Agent (osm.py:244 sends none). Live: default UA → 406; custom UA → 200 |
| A4 | Even with a User-Agent, a city search returns 0 elements | osm.py:96 builds `area["name"="Pune"]["ISO3166-1"="IN"]`; city areas never carry ISO3166-1. Live: buggy query 0 elements, `area["name"="Pune"]["boundary"="administrative"]` 5 elements |
| A5 | Second CSV import of a DIFFERENT file: new row counted as "duplicate", 0 imported | csv_import.py:236 external_id = `csv:row:{n}`; unique (source, external_id) → row 1 of every later file collides |
| A6 | Discovery result card always shows 0 new / 0 dup / 0 errors | DiscoveryPage.jsx:305-307 reads `records_new` etc.; API returns `new`, `duplicate`, `errors` |
| A7 | Qualify a business that has a website → HTTP 500 `MissingGreenlet` | ai_personalizer.py:52-53 uses `business.city` / `business.category` properties that lazy-load relationships in async SQLAlchemy |
| A8 | Campaign enrollment would crash the same way | scheduler.py:128,157 `lead.contact`, `lead.business.name` lazy loads |
| A9 | Unsubscribe link in every email → HTTP 405 | qualification.py:367 is POST only; a clicked link is GET |
| A10 | A dentist with a working website gets "Mobile App" CRITICAL 83.5 + "Online Booking" | detector.py:161-185 adds MOBILE_APP for every restaurant/clinic/gym/salon with a reachable site |
| A11 | A business with no website field gets "New Website" CRITICAL 88 without any check | detector.py:74-78; scorer gives 38 + 25 base → every such business is HIGH/CRITICAL |
| A12 | Enrichment invents `info@<domain>` contacts | enrichment/discovery.py:95-104 "synthesize corporate inbox" |

## B. Confirmed by reading (file:line)
- OSM "all categories" query pulls every named amenity/shop/office/tourism: ATMs, banks, fuel, schools, hospitals, places of worship become leads (osm.py:30-41,157-169). No brand/chain exclusion (OSM `brand`, `brand:wikidata` ignored).
- OSM gym/spa/salon mapping wrong: `amenity=gym` deprecated (real tag `leisure=fitness_centre`); "salon"/"shop" fall back to a name regex search (osm.py:143-152). Values interpolated into Overpass QL / SPARQL unescaped (osm.py:96-100, wikidata.py:90).
- Wikidata source returns notable companies that already have websites — useless for "needs a website" (wikidata.py:93-114).
- normalize_website drops any URL containing "x.com" (fedex.com, box.com …) as "social" (normalizer.py:243-251). Category partial matching maps "it" → Hospital, "barber" → Bar (normalizer.py:206-208).
- Dedup: same normalized name in the same country with no coordinates on the stored side → merged (confidence 0.60 ≥ 0.50 threshold): two different "Sharma Sweets" in Pune and Delhi become one (discovery_service.py:303-337, normalizer.py:301).
- Resolver: Cloudflare/bot 403 → BROKEN; timeouts → treated as "no website" (resolver.py:117-118,164-170; detector.py:77). No detection of website-that-redirects-to-Facebook, link-in-bio, or dead Google `business.site` URLs.
- Auditor false positives: any page containing the word "appointment" = has online booking; "basket"/"/cart" = e-commerce; any `class="…flex…"` = Tailwind (auditor.py:61-95,180-189).
- Scorer confidence is a hard-coded 0.92 (scorer.py:120).
- batch_evaluate re-audits businesses that produced zero opportunities forever; runs up to 100 sequential 12 s HTTP fetches inside one HTTP request (opportunity_service.py:198-218).
- Re-evaluation never deletes stale opportunities (a business that got a website keeps "New Website").
- Hunter.io integration always returns [] — passes `first_name`/`last_name` to a dataclass without those fields, exception swallowed (enrichment/discovery.py:203-205).
- Sync DNS lookups block the event loop (verifier.py:104).
- Compliance defaults unknown country to "US" CAN-SPAM AUTOMATED (compliance_evaluator.py:97). India falls to GENERAL_B2B.
- "AI personalizer" is fixed templates with fabricated claims: "I was impressed by your reviews", "we recently built a preview concept", "I was browsing from my smartphone" (ai_personalizer.py:64-160). Fake sender "Marcus Vance", fake postal address "100 Innovation Way, New York" (ai_personalizer.py:32-45, sender.py:34-43). Address validator passes any text containing "st" (output_validator.py:80-83).
- Campaign "dispatch" never sends anything: it only flips status to SENT (sender.py:79-107). Re-enrolling duplicates messages for the same leads (campaign_service.py:86-117).
- Only phase-1 tables are in the Alembic migration; phases 2–5 rely on create_all at startup.

## C. UI (frontend/src)
- 8 pages named after internal engines (Discovery Engine, Opportunity Engine, Enrichment Engine …) with no guided order; sidebar still says "Phase 1 — Build & test before Phase 2" while all phases exist.
- Discovery defaults to London/GB; category list mixes OSM tags and free words.
- Discovery is a blocking request (up to 90 s) with a spinner and no progress; no link from a finished job to its businesses.
- OpportunitiesPage uses Tailwind classes that render unstyled.
- Generic dark-indigo gradient dashboard with emoji icons.
