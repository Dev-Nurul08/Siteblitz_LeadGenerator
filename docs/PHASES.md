# Phases — SiteBlitz Lead Generator

Legend: ✅ done · 🔨 in progress · ⛔ blocked · ⬜ not started · 🔒 waiting for spec approval

| # | Phase | Status | Owner session | Depends on | Demo criterion |
|---|-------|--------|---------------|------------|----------------|
| 1 | Pipeline repair (install, OSM city search, CSV ids, async crashes, unsubscribe GET) | ✅ | 2026-11-08 audit session | — | `docs/spec/phase-01-pipeline-repair.md` all boxes; 138/138 tests; live Pune/Hyderabad/Munich discovery returns businesses |
| 1b | Overture Places source (lifts the 29-row OSM ceiling), location-aware dedup, job error reasons + definitions | ✅ | 2026-11-08 session, 2nd request | 1 | Udaipur cafés: OSM 29 → Overture 246 found / 225 new; 146 tests |
| 1c | Validate + sanitize every request body, query param and CSV upload; adapter import allow-list | ✅ | same | 1 | 29 new 422/400 tests; 175 tests |
| 1d | SSRF guard on every server-side website fetch (incl. redirects) | ✅ | same | 1 | internal/metadata addresses blocked; 183 tests |
| 1e | Export CSV / PDF (filters + per job), "View businesses" per job | ✅ | same | 1 | CSV + PDF downloaded through the UI for job #9; 185 tests |
| 2 | Website Intelligence Engine (verdicts, evidence table, SKIP rules — use Overture `brand` too —, need score, tiers) | 🔒 | — | 1 | `docs/spec/website-intelligence.md` acceptance list |
| 3 | Background jobs + SSRF guard + Alembic for all tables + SQLite WAL default | ⬜ | — | 1 | Start a discovery, restart the API mid-run, job resumes with no duplicate businesses |
| 4a | UI contract: `docs/contracts/ui-api.md` (verdicts, checks, labels, tiers, 3 indicators in the API) | ⬜ | — | 2 | Every field the new screens read exists in an API response |
| 4b | UI-1: design tokens + app shell/stepper + Find screen (taste skill) | 🔒 | — | 3, 4a | `docs/spec/ui-redesign.md` criteria for Find + shell, 5 states screenshotted |
| 4c | UI-2: Review screen + evidence drawer + founder labels | 🔒 | — | 4b | Review criteria + drawer screenshots |
| 4d | UI-3: Hot leads + Outreach + Settings | 🔒 | — | 4c, 5 | Remaining criteria; all 5 screens × 5 states at 1280 + 390 |
| 5 | Honest outreach: channel registry, delete fabricated contacts / pitch claims / fake SENT, unsubscribe confirmation page | ⬜ | — | 2 | Zero generated addresses; no message marked SENT without a provider event |
| 6 | Pilot: one Indian city, dentists + salons, 200 businesses, 100 calibration / 100 holdout labels | ⬜ | founder | 2, 4 | HOT precision ≥ 90 % on ≥ 30 holdout HOT predictions |
| 7 | Google Places live verification adapter (place ID only stored) | ⬜ | — | 2, API key + counsel | Live `businessStatus` shown on a lead, nothing but place ID persisted |
| 8 | Search verification via API (replaces manual search step) | ⬜ | — | 2, founder picks provider | HOT without manual search, search result stored as a check |
| 9 | Later: moment-of-need triggers, evidence-based micro-proposals, outcome learning | ⬜ | — | 6 | Defined after pilot results |

## Now
Phases 1, 1b–1e — done on branch `phase-01-pipeline-repair` (2026-11-08). UI redesign spec revised for an award-level, motion-led direction — waiting for `go`.

## Next 3
Phase 2 (needs `go` on `docs/spec/website-intelligence.md`), Phase 3, Phase 4a → 4b (needs `go` on `docs/spec/ui-redesign.md`).
