# HANDOFF — SiteBlitz Lead Generator — Phase 1 (pipeline repair) + audit

Session date: 2026-11-08 · Branch: `phase-01-pipeline-repair` (from `main` @ 2705aca)

## Done
- Full audit of every file, verified by running the code: `docs/AUDIT-2026-11-08.md`.
- ChatGPT review round (2 rounds, all agenda points agreed/rejected):
  `docs/debate/2026-11-08-lead-generator-audit-website-need-logic-ui-flow/RESULT.md`.
- Phase 1 fixes, all acceptance boxes in `docs/spec/phase-01-pipeline-repair.md` verified:
  - `pip install -e ".[dev]"` exits 0 in a fresh venv; app imports.
  - Live OSM discovery works again (Pune restaurants 20 new, Hyderabad dentists 16 new,
    Munich cafes 20 new; through the old UI: Nagpur dentists 36 new, card = API numbers).
  - CSV: each file imports its own rows; re-import = duplicates.
  - Qualify (was HTTP 500) and Enroll (would crash) work; enrol twice = 0 the second time.
  - `GET /api/v1/qualification/unsubscribe` works (was 405).
  - 138/138 tests pass (136 old + 2 new real-API integration tests).
- Complete target flow diagram: `docs/flow/siteblitz-flow.mmd` (+ viewer `docs/flow/index.html`).
- Spec drafts waiting for approval: `docs/spec/website-intelligence.md` (phase 2),
  `docs/spec/ui-redesign.md` (phase 4).

## Files changed
- `pyproject.toml` — valid build backend; dnspython + aiosqlite core deps; package discovery limited to `backend*`.
- `backend/app/engines/discovery/osm.py` — User-Agent; city = admin relation inside country → area; QL escaping.
- `backend/app/engines/discovery/csv_import.py` — external id = hash of identity fields.
- `backend/app/services/qualification_service.py` — eager-load locations/categories.
- `backend/app/services/campaign_service.py` — eager-load contact/business; skip already-enrolled leads.
- `backend/app/api/v1/qualification.py` — GET unsubscribe.
- `frontend/src/pages/DiscoveryPage.jsx` — result card reads `new/duplicate/errors`.
- `backend/tests/test_integration/test_pipeline_api.py` — new end-to-end API tests.

## Decisions made this session
- See `docs/DECISIONS.md` (2026-11-08 block).

## Known broken / deliberately skipped
- Website-need logic still the old one (false HOT leads) — phase 2, waits for `go` on its spec.
- Fabricated `info@domain` contacts, fake pitch claims, fake sender, fake SENT — phase 5.
- Discovery still runs inside the HTTP request; Overpass public endpoint sometimes rate-limits
  (job #2 in today's screenshots = PARTIAL, 1 error) — phase 3 adds retries/background jobs.
- UI not redesigned yet — phase 4, waits for `go` on `docs/spec/ui-redesign.md`.
- Not pushed if the push step below failed — check `git status` / the final chat message.

## Next session starts here
- Phase 2: Website Intelligence Engine, exactly as `docs/spec/website-intelligence.md` (after `go`).
- First commands (PowerShell, repo root):
  `python -m venv .venv` · `.venv\Scripts\python -m pip install -e ".[dev]"` ·
  (this PC only, Smart App Control) `$env:DISABLE_SQLALCHEMY_CEXT="1"; .venv\Scripts\python -m pip install --force-reinstall --no-deps --no-binary sqlalchemy sqlalchemy` ·
  `.venv\Scripts\python -m pytest -q`
- Run locally without Postgres: `$env:DATABASE_URL="sqlite+aiosqlite:///./dev.db"; .venv\Scripts\python -m uvicorn backend.app.main:app --port 8000`, then `cd frontend; npm install; npm run dev` → http://localhost:5173
- Watch out for: Overpass rate limits when running several searches back to back (wait ~60 s).
