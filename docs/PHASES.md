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
| 3 | Background jobs + SSRF guard (incl. DNS-rebinding fix: connect to the checked IP, QA-031) + Alembic for all tables + SQLite WAL default | ⬜ | — | 1 | Start a discovery, restart the API mid-run, job resumes with no duplicate businesses |
| 4a | UI contract (verdicts, checks, labels, tiers, 3 indicators, map points, contact log, source health in the API) | ✅ | same | 2 | Every field the new screens read exists in an API response |
| 4b | UI-1: design tokens + app shell/stepper + Find screen with live map (taste skill, spec v2) | ✅ | same | 4a | `docs/spec/ui-redesign.md` criteria for Find + shell, 5 states screenshotted |
| 4c | UI-2: Review screen + evidence drawer + founder labels | ✅ | same | 4b | Review criteria + drawer screenshots |
| 4d | UI-3: Hot leads + Outreach + Settings (honest outreach: no sending, contact log, do-not-contact) | ✅ | same | 4c | Remaining criteria; all 5 screens × 5 states at 1280 + 390 |
| 5 | Honest outreach backend: remove the old fabricated `info@` contacts, template pitches and fake SENT (old Contacts/Campaigns APIs, no longer in the UI); unsubscribe confirmation page + signed unsubscribe token (QA-006); also QA-008, 009, 011, 013, 019, 021 in the old APIs (`docs/qa/ISSUES.csv`) | ⬜ | — | 2 | Zero generated addresses; no message marked SENT without a provider event |
| 6 | Pilot: one Indian city, dentists + salons, 200 businesses, 100 calibration / 100 holdout labels | ⬜ | founder | 2, 4 | HOT precision ≥ 90 % on ≥ 30 holdout HOT predictions |
| 7 | Google Places live verification adapter (place ID only stored) | ⬜ | — | 2, API key + counsel | Live `businessStatus` shown on a lead, nothing but place ID persisted |
| 8 | Search verification via API (replaces manual search step) | ⬜ | — | 2, founder picks provider | HOT without manual search, search result stored as a check |
| 10 | Calibration: social-only + phone tops out at 75 (Warm) under the approved weights — founder decision needed | ⛔ | founder | 6 | Decision recorded in DECISIONS.md |
| 11 | OpenStreetMap from Geofabrik country extracts processed locally (no public Overpass); per-country refresh ≤ 7 days | ⬜ | — | 3, founder approves cost | 10 tested cities: 0 public Overpass requests, OSM adds measurable unique businesses over Overture |
| 12 | Foursquare Open Source Places as a third source (Apache 2.0) — incremental-coverage test in 7 thin countries first | ⬜ | — | founder creates a Places Portal token | Same city boxes: ≥ 20 % more verified unique businesses than Overture, or ≥ 20 in a near-empty city |
| 13 | AI outreach writer: system prompt + company facts + 33-country language table + validator (langdetect, facts guard, banned phrases, counts) + Claude API call; no email/phone sent to the model | ✅ (live API run waits for ANTHROPIC_API_KEY; QA 2026-11-10 fixed TASK redaction QA-016 and missing-country=US QA-015) | 2026-11-10 outreach session | 2, founder blanks in `.env` (sender, reply address, postal address) | `docs/spec/outreach-engine.md` phase-13 criteria |
| 14 | Email finder for phone-only leads with own website: Navsari + Surat, 3 demo verticals, 2,162 sites; robots.txt; emails only from own pages, never guessed; same visit records viewport/HTTPS/site-down checks. QA-040 fixed in the reused crawler (`site_visit.py`), QA-038 landed first | ✅ (2026-11-10: 499 leads with an email, 619 addresses, 0 without a source URL; `docs/outreach/email-finder-run-2026-11-10.md`) | 2026-11-10 phase-14 session | 2, QA-038 | Every stored email has a source URL; totals reported |
| 14b | Email-finder follow-up: second check ≥ 6 h later for the 701 failed sites (SITE_DOWN_CONFIRMED); drop chain store-locator hosts (115 hosts / 797 leads) and head-office addresses; email ladder status (CONFIRMED/VALID/RISKY/...); import kept rows into the app DB (businesses, `website_checks`, contacts) for phase 15 | ⬜ → folded into E1 (2026-11-12) | — | 14 | Re-check log; chain filter counts; the phase-15 screen lists the imported leads |
| 15 | Outreach batch screen: 100/day ceiling, select + one click Write, READY/HOLD list, email queue, WhatsApp chat link only for opted-in leads (full international number, QA-025), social draft + open profile (hand send) | ⬜ → replaced by E3 (2026-11-12) | — | 13, sending provider chosen | Cap refusal at 101; screenshots of 5 states at 1280 + 390 |
| 16 | Letter + QR pack (PDF, 25 per batch) for phone-only / social-only Navsari + Surat leads | ⬜ paused (email first, 2026-11-12) | — | 13, India Post class + price | Scanned QR opens WhatsApp to +91 92744 90242 with the business name typed |
| E0 | Email engine v2: deploy the truthful SiteBlitz website (branch v2-redesign; `NEXT_PUBLIC_SITE_URL` in Vercel) | 🔒 | — | founder `go` on `docs/spec/email-engine-v2.md` | No invented reviews/results, Gujarat only, working contact route; screenshots 1280 + 390 |
| E1 | Eligibility: Tier 1 provenance (source URL + date + excerpt), verifier ladder, observation rechecks incl. rendered 390 px phone check, phase-14 import (old 14b), fabricated-contact code removed (old 5) | 🔒 | — | E0, verifier account | Spec v2 E1 criterion; listing-only = HOLD |
| E2 | Sending core: send records, scheduler (Tue-Thu windows, caps 30/25/5), Mailforge SMTP adapter, RFC 8058 headers, cloud suppression + unsubscribe endpoint, bounce parsing, pause/stop rules | 🔒 | — | E1, Mailforge + 2 domains | 0 duplicates, 0 sends after suppression in race tests, crash recovery, headers on raw received mail |
| E3 | Batch screen: select, write, validate, review, approve and schedule (replaces 15) | 🔒 | — | E2 | 11th contact on a 10/day day refused; 6 states at 1280 + 390 |
| E4 | Reply loop: IMAP every <= 24 h, multi-label classifier, AI drafts with approval, daily Roman-Hindi brief, `/start-day` command | 🔒 | — | E2 | Labelled reply set: 0 missed stop; brief counts match the DB |
| E5 | Opportunity Snapshot pages (after a positive reply) + the founder's recorded overviews | 🔒 | — | E2, recordings | 3 layers, concept label, transcript, no autoplay, expiry |
| E6 | Launch gates (seed tests, unsubscribe incl. laptop-off, failure tests, 30/30 provenance, 10-reader test, persona review, founder reads 20) and pilot week 1 (10 new/day, India) | 🔒 | — | E1-E5 | Every gate in spec v2 row 17 has a log |
| QA-1 | QA audit of phases 1–13 + Lead Radar; fix the high-severity bugs (launcher, default DB, 422 text, IST dates, gmail-wide unsubscribe, writer TASK redaction, missing country = US, Lead Radar sample label) | ✅ | 2026-11-10 QA session | — | `docs/qa/QA_REPORT.md`; 325/325 tests; UI sweep 6 screens × 1280/390 + backend-down |
| QA-1b | QA remediation of the open medium/low bugs not owned by another phase: API 007/010/014/017/018/044, UI 022/023/024/026/027/028/045, writer hardening 032–036/043, intelligence 037 (038 fixed in phase 14), discovery 039/042, country table 041 (founder decision) | ⬜ | — | QA-1 | Every listed ID in `docs/qa/ISSUES.csv` FIXED with a before/after log, or moved with a reason |
| LR | Lead Radar (colleague Dev-Nurul08's code from main): real places instead of 100 generated ones (QA-012), Navsari + Surat defaults instead of Mumbai (QA-029), 422 instead of 500 on bad input (QA-020), 390 px layout (QA-030) — agree with the colleague first | ⬜ | — | colleague | Funnel runs on stored businesses; default city Surat; no 500 on null/strings |
| 9 | Later: moment-of-need triggers, evidence-based micro-proposals, outcome learning | ⬜ | — | 6 | Defined after pilot results |

## Now
Phases 1, 1b–1f, 2, 4a–4d done (2026-11-08); phase 13 AI writer, QA-1 audit and phase 14 email finder done
(2026-11-10). Branch `phase-01-pipeline-repair`.

2026-11-12: two review rounds - agency route (`docs/debate/2026-11-12-clients-without-selling/RESULT.md`, kit in
`docs/agency/`) and email engine v2 (`docs/debate/2026-11-12-email-engine-personas/RESULT.md`, spec lock
`docs/spec/email-engine-v2.md`, waiting for the founder's `go`).

## Next 3
E0 (truthful website live), E1 (eligibility + verification + import), E2 (sending core) - all 🔒 until the founder
approves `docs/spec/email-engine-v2.md`. QA-1b writer hardening runs inside E1/E3 where it touches the writer.
