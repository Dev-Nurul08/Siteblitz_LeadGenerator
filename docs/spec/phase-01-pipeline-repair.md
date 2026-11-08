# Spec — Phase 1: Pipeline repair (make the existing API actually run)

Source: verified audit `docs/AUDIT-2026-11-08.md` (rows A1–A9). No new features, no new design values.
Every criterion below restores behaviour the existing code and README already promise.

## Scope (code files, max 8)
1. `pyproject.toml` — valid build backend; `dnspython` + `aiosqlite` become core dependencies.
2. `backend/app/engines/discovery/osm.py` — send an identifying User-Agent; build city areas without
   the `ISO3166-1` tag; escape user text inside Overpass QL strings.
3. `backend/app/engines/discovery/csv_import.py` — external id derived from the row content, not the row number.
4. `frontend/src/pages/DiscoveryPage.jsx` — read the keys the API really returns (`new`, `duplicate`, `errors`, `found`).
5. `backend/app/services/qualification_service.py` — eager-load `locations` + `categories` before the pitch template reads them.
6. `backend/app/services/campaign_service.py` — eager-load `contact` + `business` on enrolment; never enrol the same lead twice in one campaign.
7. `backend/app/api/v1/qualification.py` — `GET /qualification/unsubscribe` (a clicked email link is a GET).
8. `backend/tests/test_integration/test_pipeline_api.py` — new end-to-end API test on SQLite.

## Out of scope (recorded in docs/PHASES.md)
Website-need scoring, Google Places source, social detection, fabricated contacts/pitch text,
background jobs, UI redesign, SQLite-as-default.

## Acceptance criteria (binary)
- [ ] `pip install -e ".[dev]"` exits 0 in a fresh venv.
- [ ] `python -c "import backend.app.main"` exits 0 after that install (dnspython present).
- [ ] Live: `POST /api/v1/discovery/run` with `openstreetmap`, `IN`, `Pune`, `restaurant`, `max_results=20` returns `new > 0` and `status` `COMPLETED`.
- [ ] Two CSV imports of two different files each import their own rows (`new` = row count of each file).
- [ ] Re-importing the same file a second time reports those rows as `duplicate`, `new = 0`.
- [ ] The Discovery result card shows the same numbers as the API response.
- [ ] `POST /api/v1/qualification/qualify-business/{id}` for a business with a website and contact returns 200 (no `MissingGreenlet`).
- [ ] `POST /api/v1/campaigns/{id}/enroll` with one QUALIFIED lead returns `enrolled_count = 1`; calling it again returns `enrolled_count = 0`.
- [ ] `GET /api/v1/qualification/unsubscribe?email=a@b.com` returns 200 and the address appears in `GET /api/v1/qualification/opt-outs`.
- [ ] Full test suite passes (136 existing + new integration tests).
