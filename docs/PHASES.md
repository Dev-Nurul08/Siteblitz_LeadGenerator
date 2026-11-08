# Phases — SiteBlitz Lead Generator

Legend: ✅ done · 🔨 in progress · ⛔ blocked · ⬜ not started · 🔒 waiting for spec approval

| # | Phase | Status | Owner session | Depends on | Demo criterion |
|---|-------|--------|---------------|------------|----------------|
| 1 | Pipeline repair (install, OSM city search, CSV ids, async crashes, unsubscribe GET) | ✅ | 2026-11-08 audit session | — | `docs/spec/phase-01-pipeline-repair.md` all boxes; 138/138 tests; live Pune/Hyderabad/Munich discovery returns businesses |
| 1b | Overture Places source (lifts the 29-row OSM ceiling), location-aware dedup, job error reasons + definitions | ✅ | 2026-11-08 session, 2nd request | 1 | Udaipur cafés: OSM 29 → Overture 246 found / 225 new; 146 tests |
| 1c | Validate + sanitize every request body, query param and CSV upload; adapter import allow-list | ✅ | same | 1 | 29 new 422/400 tests; 175 tests |
| 1d | SSRF guard on every server-side website fetch (incl. redirects) | ✅ | same | 1 | internal/metadata addresses blocked; 183 tests |
| 1e | Export CSV / PDF (filters + per job), "View businesses" per job | ✅ | same | 1 | CSV + PDF downloaded through the UI for job #9; 185 tests |
| 1f | Data volume + reliability: all-sources search, name + whole-word category matching, phone dedup, shared geocoder, Overpass retries, per-record savepoints, up to 5,000 per search, re-check Needs review | ✅ | 2026-11-08, 4th request | 1b | Udaipur dentists 70→100 new, cafés 225→370, Pune salons 4,065 new / 0 errors; 208 tests |
| 2 | Website Intelligence Engine (verdicts, evidence table, SKIP rules — use Overture `brand` too —, need score, tiers) | ✅ | 2026-11-08, 3rd request | 1 | `docs/spec/website-intelligence.md` acceptance list |
| 3 | Background jobs + SSRF guard + Alembic for all tables + SQLite WAL default | ⬜ | — | 1 | Start a discovery, restart the API mid-run, job resumes with no duplicate businesses |
| 4a | UI contract (verdicts, checks, labels, tiers, 3 indicators, map points, contact log, source health in the API) | ✅ | same | 2 | Every field the new screens read exists in an API response |
| 4b | UI-1: design tokens + app shell/stepper + Find screen with live map (taste skill, spec v2) | ✅ | same | 4a | `docs/spec/ui-redesign.md` criteria for Find + shell, 5 states screenshotted |
| 4c | UI-2: Review screen + evidence drawer + founder labels | ✅ | same | 4b | Review criteria + drawer screenshots |
| 4d | UI-3: Hot leads + Outreach + Settings (honest outreach: no sending, contact log, do-not-contact) | ✅ | same | 4c | Remaining criteria; all 5 screens × 5 states at 1280 + 390 |
| 5 | Honest outreach backend: remove the old fabricated `info@` contacts, template pitches and fake SENT (old Contacts/Campaigns APIs, no longer in the UI); unsubscribe confirmation page | ⬜ | — | 2 | Zero generated addresses; no message marked SENT without a provider event |
| 6 | Pilot: one Indian city, dentists + salons, 200 businesses, 100 calibration / 100 holdout labels | ⬜ | founder | 2, 4 | HOT precision ≥ 90 % on ≥ 30 holdout HOT predictions |
| 7 | Google Places live verification adapter (place ID only stored) | ⬜ | — | 2, API key + counsel | Live `businessStatus` shown on a lead, nothing but place ID persisted |
| 8 | Search verification via API (replaces manual search step) | ⬜ | — | 2, founder picks provider | HOT without manual search, search result stored as a check |
| 10 | Calibration: social-only + phone tops out at 75 (Warm) under the approved weights — founder decision needed | ⛔ | founder | 6 | Decision recorded in DECISIONS.md |
| 11 | OpenStreetMap from Geofabrik country extracts processed locally (no public Overpass); per-country refresh ≤ 7 days | ⬜ | — | 3, founder approves cost | 10 tested cities: 0 public Overpass requests, OSM adds measurable unique businesses over Overture |
| 9 | Later: moment-of-need triggers, evidence-based micro-proposals, outcome learning | ⬜ | — | 6 | Defined after pilot results |

## Now
Phases 1, 1b–1e, 2, 4a–4d done on branch `phase-01-pipeline-repair` (2026-11-08), not pushed.

## Next 3
Phase 3 (background jobs, SSRF/size limits already partly done), phase 5 (remove old fabricated-contact APIs), phase 10 (calibration decision), then the pilot (6).
