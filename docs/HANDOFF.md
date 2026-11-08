# HANDOFF — SiteBlitz Lead Generator — Phases 1, 1b–1e

Session date: 2026-11-08 · Branch: `phase-01-pipeline-repair` (from `main` @ 2705aca) · **not pushed**

## Done (all verified, 185/185 tests)
- Phase 1 — pipeline repair (install, OSM city search, CSV ids, async crashes, unsubscribe GET).
- Phase 1b — **Overture Places** source: Udaipur cafés 29 (OSM) → 246 found / 225 new (live, via UI).
  Location-aware dedup (no more merging same-name shops in different cities). Job cards show the
  source's error reason and a definitions box.
- Phase 1c — every request body, query param and CSV upload validated + sanitized (422/400, never 500);
  `adapter_class` allow-list (blocked arbitrary module import); CSV imports keep up to 5,000 rows
  (stopped silently at 500); short CSV rows no longer rejected.
- Phase 1d — SSRF guard on all server-side website fetches incl. redirect hops.
- Phase 1e — Export CSV / PDF (Businesses header + every job card), "View businesses" per job.
- Docs: `docs/AUDIT-2026-11-08.md`, `docs/USER-GUIDE.md` (order of steps, every term, why 29, exports),
  flow `docs/flow/siteblitz-flow.mmd` + viewer `docs/flow/index.html`, ChatGPT review `docs/debate/…/RESULT.md`.

## Files changed (since main)
- Backend: `pyproject.toml`, `config.py`, `main.py`, `engines/discovery/{osm,overture,csv_import,registry}.py`,
  `engines/opportunity/resolver.py`, `engines/enrichment/discovery.py`, `services/{discovery,qualification,campaign,export}_service.py`,
  `schemas/{types,business,source,campaign,qualification,opportunity,contact}.py`, `api/v1/{businesses,discovery,sources,contacts,opportunities,qualification}.py`.
- Frontend: `services/api.js`, `pages/{DiscoveryPage,BusinessesPage}.jsx`.
- Tests: `tests/test_integration/test_pipeline_api.py`, `tests/test_discovery/test_overture.py`, `tests/test_opportunity/test_ssrf_guard.py`.

## Decisions made this session
- See `docs/DECISIONS.md` (two 2026-11-08 blocks).

## Known broken / deliberately skipped
- **UI not redesigned.** Revised award-level, motion-led spec waits for `go`: `docs/spec/ui-redesign.md`.
- Website-need logic is still the old one (false HOT leads) — phase 2, waits for `go` on `docs/spec/website-intelligence.md`.
- Fabricated `info@` contacts / pitch claims / fake SENT — phase 5.
- **The API has no authentication**; `docker-compose.yml` publishes port 8000 on all interfaces. Keep it on
  127.0.0.1 until an auth phase exists.
- Discovery still runs inside the HTTP request (Overture ≈ 20 s, OSM up to 90 s) — phase 3.
- Overture release folder is pinned (`OVERTURE_RELEASE=2026-10-21.0`); when Overture deletes it, reads fail
  with a message telling you to update it.
- `npx oxlint` cannot run on this PC (native binding missing); `npm run build` passes.
- Screenshots with real business contacts (`docs/screenshots/phase-1b/`) and debate driver files are untracked on purpose.
- **Push blocked earlier by the Claude OS guard hook** — run `git push -u origin phase-01-pipeline-repair` yourself,
  then open a PR into `main` on https://github.com/Dev-Nurul08/Siteblitz_LeadGenerator.

## Next session starts here
- Phase 4b (UI-1: tokens + shell + Find with the live map) after `go` on `docs/spec/ui-redesign.md`,
  or Phase 2 after `go` on `docs/spec/website-intelligence.md`.
- First commands (PowerShell, repo root):
  `.venv\Scripts\python -m pip install -e ".[dev]"` ·
  (this PC only) `$env:DISABLE_SQLALCHEMY_CEXT="1"; .venv\Scripts\python -m pip install --force-reinstall --no-deps --no-binary sqlalchemy sqlalchemy` ·
  `.venv\Scripts\python -m pytest -q` (expect 185 passed)
- Run: see `docs/USER-GUIDE.md` §0.
- Watch out for: Overpass and Nominatim rate limits when running many searches back to back.
