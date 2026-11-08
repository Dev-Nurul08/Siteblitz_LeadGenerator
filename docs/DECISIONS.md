# Decisions — SiteBlitz Lead Generator (append-only)

## 2026-11-08 — audit + ChatGPT review round
- **OpenStreetMap is the stored discovery source; Google Places is only an optional live verification
  adapter.** Why: the Maps Platform terms allow storing only the place ID permanently, and scraping the
  Maps website breaks Google's terms. (debate RESULT row 1)
- **No automated logged-in scraping of Instagram / Facebook / LinkedIn / TikTok.** Social links come from
  listings and the business's own pages and are recorded as discovered/confirmed/rejected. Why: platform
  terms (LinkedIn explicitly) and account bans; a social profile alone never proves need. (row 2)
- **"No website field" is not evidence of "no website".** A HOT lead needs a verified website verdict
  including a search or recorded manual search. Why: OSM is incomplete; the old rule produced mostly false
  HOT leads. (rows 3, 3c)
- **Three indicators, not one score:** Website Need Score, Evidence Confidence, Outreach Readiness.
  Why: contactability and certainty were mixed into "need", and confidence was a fake constant. (row 4)
- **Claude's 45/25/15/15 formula rejected in favour of 60/20/10/10 (provisional).** Why: reviews, phone and
  category are not proof of need; calibrate on the pilot. (row 4a)
- **WhatsApp is never automated; sending stays disabled until a real provider confirms delivery.** Why:
  WhatsApp opt-in policy; the old code marked unsent messages as SENT. (row 5)
- **CSV source ids are a hash of the row's identity fields**, not the row number. Why: row ids collided
  across files and silently dropped new data. (phase 1)
- **City search in Overpass resolves an administrative relation inside the country and maps it to an
  area.** Why: city areas never carry `ISO3166-1`; the old query always returned 0. (phase 1)
- **Phase-1 bug fixes were built before spec approval** because the founder's request explicitly
  authorised fixing broken APIs and the fixes add no new values — they restore what the code already
  promised. Website-need logic and UI redesign wait for spec-lock approval.

## 2026-11-08 — second request (why 29, validation, export)
- **Overture Maps Places is the default discovery source.** Why: OSM's Udaipur data really has only 29 named
  cafés; Overture (CDLA-Permissive-2.0 / Apache-2.0, Meta + Microsoft + Foursquare) has 246, with phones for
  83 % of places and social links for 87 %. Read with DuckDB from the public S3 GeoParquet by city bounding box
  (one Nominatim lookup per job). Release folder pinned in `OVERTURE_RELEASE` (update monthly).
- **Two records are merged only at "same city" or "within 5 km" confidence (≥ 0.70)**, not "same name in the
  same country" (0.60). Why: different shops with common names were being lost.
- **Every input limit comes from the DB column size or an existing rule** (ISO alpha-2, verifier email regex);
  free-form `query_params` are an allow-list (`min_confidence`); `adapter_class` is an allow-list. Why: no
  invented numbers; arbitrary module import was possible through POST /sources.
- **CSV upload cap 15 MB** = 5,000 rows (existing max_results limit) × ~3 KB max row at DB column sizes.
- **Exports:** CSV = all stored columns, formula-prefixed cells neutralised (OWASP CSV injection); PDF via
  fpdf2 (pure Python). Exports with real business contacts are not committed to git.

## 2026-11-08 — third request ("go … complete everything")
- **Both specs approved by the founder's "go"**: website intelligence (phase 2) and the UI redesign v2
  (dark graphite + safety orange, Mona Sans + Geist Mono, motion + MapLibre + NumberFlow + Lucide).
- **Website checks run concurrently per batch** (25 businesses ≈ 35 s instead of minutes); the DB writes stay sequential.
- **Google links (g.co, google.com, business.site) and directories (Justdial, Practo, Zomato…) are listings, not
  websites** — found live: "Dr Shweta's … Clinic" was "Has own website" because its website field was a g.co link.
- **The old Dashboard / Businesses / Opportunities / Contacts / Compliance / Campaigns screens were removed**
  from the UI; their APIs remain but are not used by the app (the Contacts API still fabricates `info@` — phase 5).
- **Screenshots containing real businesses' contact data are not committed** (`.gitignore`).
- **Open (founder):** social-only + phone can never be Hot under the approved weights (max 75). Options:
  (a) keep — only no-website businesses are Hot; (b) count "its listed web address is a social profile" as the
  10-point business-problem signal (social-only + phone + confirmed open + dentist = 85 → Hot).

## 2026-11-08 — fourth request ("as much data per run as I targeted")
- **Default source = All sources (Overture + OpenStreetMap in one job).** Overlap is merged by source id,
  phone (last 10 digits, same city / ≤ 5 km) and name + place.
- **Category = whole word-parts of the category fields OR keywords in the business name** (categories.py).
  Fixes `%dent%` → student_union and `%tax%` → taxi; adds 27–54 % real matches.
- **OpenStreetMap searches the geocoded city box**, not the named boundary (the "Udaipur" boundary matched the
  whole district + same-named villages and timed out).
- **Each discovery record runs in a SAVEPOINT** (SQLite needs SQLAlchemy's BEGIN recipe, enabled in database.py).
- **Not done, needs a decision:** (1) treat "listed domain has no DNS record, confirmed by a second resolver" as
  Website down immediately instead of waiting 6 h (changes approved spec row 6); (2) widen the area beyond the
  city when it has fewer businesses than asked (measured gain small: Udaipur dentists 102 → 112 at 3× area).

## 2026-11-08 — fifth request (city test: India, Bangladesh, Afghanistan + top 50 countries, 10 ChatGPT rounds)
- **Geocoder takes the first settlement hit** (city / town / village / municipality) of 5, retries without the
  state when the state-qualified lookup only finds a landmark, and trims a city boundary larger than 1.5° to the
  1.5° square around the city's point (inside the boundary; the job and the Find screen show it). Found live:
  Beijing → a 1 × 2 km business district, Ho Chi Minh City → a TV station building, Shenzhen → rejected; all 0.
  After: Shenzhen 0 → 522 available. A state or district hit is still rejected, never trimmed.
- **A repeat search lists what it found again** (`source_job_sightings`). Before: a job whose records an earlier
  job had saved showed nothing under "View businesses", the map, export and website checks (Pimpri-Chinchwad:
  300 found, 19 listed, because its box overlaps Pune's).
- **Find screen offers all 249 ISO countries** (it had 10 — Bangladesh and Afghanistan could not be chosen).
- **Public Overpass stopped answering this machine** after three test processes ran at once (connection refused
  for 40+ cities). The test continued with Overture only. Per-process Overpass lock is a global queue only while
  one API process runs.
- **Open (founder):** production OpenStreetMap data from Geofabrik country extracts processed locally (ChatGPT R5:
  ≈ $24–96 / month, 3–5 developer days) instead of public Overpass — proposed as phase 11.
- **Open (founder + counsel):** Overture's Places guide says joining Places with OSM "may need to carry the Open
  Database License (ODbL) if it is a derivative database". "All sources" joins them. Internal use only today;
  get advice before any merged list leaves the company.
