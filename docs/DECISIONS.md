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
