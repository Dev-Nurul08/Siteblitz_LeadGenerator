# Review - SiteBlitz Lead Generator audit, website-need logic, UI flow - 2026-11-08 - 2 rounds - prompt: lead-intelligence-vision-partner

Context sent: verified audit evidence (`audit-evidence.md`), `detector.py`, `scorer.py`, `README.md` (24.7 KB, nothing truncated).
Stopped after round 2: every agenda point agreed or rejected with a reason; the remaining open items are founder decisions or need pilot data.

| # | Point | Proposed by | Evidence (file:line / round) | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | OSM stays the stored source; Google Places only an optional key-gated **verification** adapter (only place ID may be stored); CSV with source tracking; no Maps HTML scraping | Claude R1, narrowed by ChatGPT R1 | Maps Platform terms (ChatGPT R1, matches Claude's reading); `osm.py` fixed in phase 1 | agreed | agreed |
| 2 | Social presence only from lawful links (listing tags, own website, link-in-bio); `SocialIdentity` record with discovered/confirmed/rejected; a social profile alone never means "needs a website"; no logged-in scraping | Claude R1 + ChatGPT R1 | LinkedIn/TikTok platform rules (ChatGPT R1) | agreed | agreed |
| 3 | 6-status website verdict: OWN_SITE_VERIFIED, SOCIAL_ONLY_VERIFIED, NO_SITE_VERIFIED, SITE_DOWN_CONFIRMED, UNKNOWN, SKIP; history kept separate from current verdict | ChatGPT R1 | `detector.py:74-78` (empty field ≠ absence) | agreed | agreed |
| 3a | Chain = OSM `brand` / `brand:wikidata` / `operator` tag + per-run "include franchises" toggle (NOT "same name ≥ 3 times") | ChatGPT R1 | R1 §3 | agreed — Claude's own rule rejected | agreed |
| 3b | 403 = bot protection, not broken; timeout/5xx need a 2nd observation ≥ 6 h later before SITE_DOWN_CONFIRMED | ChatGPT R1, numbers by Claude R2 | `resolver.py:117,164` | agreed | agreed |
| 3c | NO_SITE_VERIFIED + HOT requires a search check (search API **or** a recorded manual search by the founder); without it: "No website identified — limited verification", medium confidence, max WARM; domain guesses only *find candidates*, never prove absence | ChatGPT R2 Q1 | R2 Q1 | agreed | agreed |
| 3d | Negative-status gate: OSM `disused:*`, `abandoned:*`, `was:*`, `shop=vacant` → SKIP/REVIEW | ChatGPT R2 Q3 | OSM wiki lifecycle prefixes | agreed | agreed |
| 4 | Three separate indicators: Website Need Score (0–100), Evidence Confidence (low/medium/high), Outreach Readiness. UNKNOWN → REVIEW, unscored. Phone not mandatory for HOT | ChatGPT R1 | `scorer.py:120` fake 0.92 | agreed | agreed |
| 4a | Need score weights (pilot, provisional): website gap 60 (no site 60 / social-only 55 / site down 50 / functioning site with major problem 10–35 / fine 0) + business problem 20 (strongest single observed signal, no double counting) + activity 10 + service fit 10. HOT 80–100, WARM 60–79, COLD 0–59 | ChatGPT R1–R2; Claude's 45/25/15/15 rejected | R1 §4, R2 Q2 | agreed (Claude's own formula rejected: mixed contactability into need) | agreed |
| 4b | Activity: OSM edit date = 0 points; `check_date` ≤ 180 days = 2; real confirmation (call / Places live status / owner post ≤ 90 days) up to 10. With OSM only, activity stays UNKNOWN → HOT needs a human "verified active" action | ChatGPT R2 Q3 | R2 Q3 | agreed | agreed |
| 5 | No generated addresses (delete `info@domain`); channel registry (phone, email, social DM, contact form, manual); WhatsApp never automated (opt-in policy); sending disabled until a real provider confirms delivery; unsubscribe GET → confirmation page + POST | Claude R1 + ChatGPT R1 | `enrichment/discovery.py:95`, `sender.py:79` | agreed | agreed |
| 6 | DB-backed job table + one worker loop, resumable after restart; SQLite WAL default, Postgres for multi-user; SSRF guard (block private/loopback/link-local after DNS, ≤ 2 MB, ≤ 5 redirects); all tables in Alembic | Claude R1 + ChatGPT R1 | `discovery.py:17-45` sync run; `001_phase1_discovery.py` only phase-1 tables | agreed | agreed |
| 7 | UI: Find → Review → Hot leads → Outreach; zero-result job shows the source error; every lead answers "who / has website? / what was checked / why HOT / how to reach / next action"; delete fake pitch claims, fake sender, Wikidata, auto Mobile-App opportunities | Claude R1 + ChatGPT R1 | `frontend/src/App.jsx`, `ai_personalizer.py:64-160` | agreed | agreed |
| 8 | Pilot: India, one city, dentists + salons, 200 businesses, split 100 calibration / 100 untouched holdout; review labels say *what* was wrong; HOT auto-approval only if ≥ 90 % precision on ≥ 30 holdout HOT predictions | Claude R2 + ChatGPT R2 Q4 | R2 Q4 | agreed | agreed |
| 9 | Later ideas: moment-of-need triggers, evidence-based micro-proposals, learning from sales outcomes | ChatGPT R1 | R1 "additional proposals" | agreed as later phases, not now | parked |

## Recommended next steps (not started - waiting for your go)
Phase 1 (pipeline repair) is already built and verified on branch `phase-01-pipeline-repair` — the founder's request pre-authorised fixing broken APIs. Everything below waits for approval of the spec-lock tables:
1. Phase 2 — Website Intelligence Engine (points 3, 3a–3d, 4, 4a, 4b): `docs/spec/website-intelligence.md`.
2. Phase 3 — Background jobs + SSRF guard + full migrations (point 6).
3. Phase 4 — UI redesign, 4-step workflow (point 7): `docs/spec/ui-redesign.md`.
4. Phase 5 — Honest outreach: channel registry, delete fabricated contacts/claims/SENT (point 5).
5. Phase 6 — Pilot run + labelling (point 8).

## Points still open (founder decisions or pilot data)
1. Pilot city (one Indian city the founder can personally verify).
2. Search verification: search API (which, budget) or manual search only for the pilot.
3. Google Places: get an API key + confirm with counsel whether a persisted score may use live Places status.
4. Which non-Google evidence satisfies the activity gate besides a phone call.
5. Outreach channels allowed per launch country (TRAI / PECR / CAN-SPAM) and who signs off.
6. Monthly volume, budget per verified HOT lead.
