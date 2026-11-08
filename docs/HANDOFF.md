# HANDOFF — SiteBlitz Lead Generator — Phases 1, 1b–1f, 2, 4a–4d + city coverage test

Session date: 2026-11-08 · Branch: `phase-01-pipeline-repair` (from `main` @ 2705aca) · **not pushed**

## Done (verified)
- **City coverage test (5th request)**: 357 population-ranked cities in 53 countries (India 150, Bangladesh 38,
  Afghanistan 22, 3 each in the 50 most populous other countries) + 39 re-check / validation searches, 10 ChatGPT
  rounds. Full write-up: `docs/debate/2026-11-08-city-coverage-test/RESULT.md`.
- Bugs the test found and fixed (each with a live before / after):
  - repeat / overlapping searches listed nothing they had found before (job sightings) — Pimpri-Chinchwad 19 → 287;
  - results not limited to the chosen country — "Shenzhen, CN" was 479 Hong Kong dentists of 522 → 43 CN;
  - geocoder: Beijing → a business district, Ho Chi Minh City → a TV station, Tokyo → Hachioji, Nanded → a village,
    Hubli-Dharwad → municipal offices; now name-checked settlements, city beats village, landmark = not found,
    whole-municipality boxes trimmed to 1.5° and labelled, province-only names rejected — 20 / 20 on a validation
    batch with expected answers;
  - Find screen offered 10 countries (Bangladesh, Afghanistan impossible) → all 249;
  - a city name outside cp1252 (Wrocław, Łódź) crashed the job through a log line on Windows → UTF-8 output.
- Backend 221 tests pass; frontend `npm run build` passes; Find screen "Searched area" line screenshotted.
- Earlier this session (phases 1–4d): see `docs/PHASES.md` and `docs/DECISIONS.md`.

## Decisions made this session
- `docs/DECISIONS.md` — five 2026-11-08 blocks (the last two are the city test).

## Known broken / deliberately skipped
- **Public Overpass (OpenStreetMap) refuses connections from this PC** since the test ran several processes at
  once; "All sources" still returns Overture rows (status PARTIAL). Use "Overture Places" until it recovers.
  Production fix proposed: phase 11 (Geofabrik extracts, needs budget approval + ODbL review).
- Overture is near-empty for dentists in China, DR Congo, Madagascar, Niger, Afghanistan outside Kabul, Iran outside
  Tehran and secondary African cities — a source gap. Phase 12 (Foursquare OS Places) proposed; needs the founder to
  create a free Places Portal token.
- Nominatim does not forgive spelling: "Bamyan" not found, "Bamiyan" works; "Dhamsona" not found.
- Open founder decisions: SOCIAL_ONLY / NEITHER_LISTED reporting labels (ChatGPT's #1 by value per cost), social-only
  Hot cap (a / b), dead domain = Website down immediately (both reviewers: no), widen area, admin-centre search mode,
  ODbL legal review.
- Old Contacts / Qualification / Campaigns **APIs** still contain the fabricated `info@` contact, template pitches and
  fake SENT (removed from the UI) — phase 5.
- Discovery + checks still run inside HTTP requests (no background worker) — phase 3. No Alembic migration for the
  new tables (`source_job_sightings`, intelligence tables); `create_all` creates them at startup — phase 3.
- The API has no authentication; keep it on 127.0.0.1.
- **Not pushed** — the Claude OS guard hook blocks `git push` from Claude. Run:
  `git push -u origin phase-01-pipeline-repair`, then open a PR into `main`.

## Next session starts here
- Push the branch and open the PR.
- Answer the open founder decisions above, then phase 6 pilot (ChatGPT R10 suggests India + Bangladesh + France,
  60 labelled businesses each) or phase 3 (background jobs).
- First commands (PowerShell, repo root):
  `.venv\Scripts\python -m pip install -e ".[dev]"` ·
  (this PC only) `$env:DISABLE_SQLALCHEMY_CEXT="1"; .venv\Scripts\python -m pip install --force-reinstall --no-deps --no-binary sqlalchemy sqlalchemy` ·
  `.venv\Scripts\python -m pytest -q` (expect 221 passed) · `cd frontend; npm install; npm run build`
- Run: `docs/USER-GUIDE.md` §0 (English) or `docs/GUIDE-ROMAN-HINDI.md`.
- Re-run the city test: `scripts/city_coverage.py <cities.json> <results.json> --api http://127.0.0.1:8001 --source overture`
  against a backend on a separate test database.
- Watch out for: one search at a time against public Overpass; Nominatim 1 request / s; after stopping a background
  worker on Windows, kill the leftover `python.exe` (uvicorn) by command line or the port stays taken.
