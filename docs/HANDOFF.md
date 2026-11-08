# HANDOFF — SiteBlitz Lead Generator — Phases 1, 1b–1f, 2, 4a–4d

Session date: 2026-11-08 · Branch: `phase-01-pipeline-repair` (from `main` @ 2705aca) · **not pushed**

## Done (verified)
- Phase 1f (data volume): All sources search, name matching, phone dedup, OSM by city box, retries, savepoints, up to 5,000 per search. Live: Udaipur dentists 100 new, cafés 370, salons 392; Pune salons 4,065 new, 0 errors. 208 tests pass.
- Backend: 208/208 tests (pipeline repair, Overture source, input validation, SSRF guard, CSV/PDF export,
  website intelligence: verdicts + evidence checks + need score + tiers + labels + contact log).
- New UI (spec v2, approved): Find (live map, businesses land with a ring, automatic website checks),
  Review (evidence drawer, labels, J/K/1/2/3), Hot leads (score builds from reasons), Outreach (fact-linked
  draft, copy only after "I checked every fact", sending honestly off, contact log, do-not-contact), Settings
  (live source health, do-not-contact list).
- Verified in Chrome: 5 screens × populated / empty / error / loading at 1280, populated at 390, no horizontal
  overflow at 1280 / 390 / 320, axe colour-contrast 0 violations on all screens, 2 px orange focus ring,
  reduced motion (drawer transform none, spinner off), no emoji, no hex outside `:root`, initial JS 129 KB gzip
  with MapLibre (290 KB gzip) lazy. Screenshots: `docs/screenshots/ui/` (local only — they show real businesses).
- Live run: Udaipur dentists on Overture → 75 found / 70 new; checks → 40 social-only, 15 own site, 14 needs
  review, 1 skipped.

## Decisions made this session
- See `docs/DECISIONS.md` (three 2026-11-08 blocks).

## Known broken / deliberately skipped
- Two data decisions open (DECISIONS.md, fourth block): dead-domain = immediate "Website down"?, widen area beyond the city?
- **Open founder decision:** a social-only business with a phone tops out at 75 (Warm) under the approved
  weights — see DECISIONS.md "Open (founder)". Nothing changed until you choose (a) or (b).
- Old Contacts / Qualification / Campaigns **APIs** still contain the fabricated `info@` contact, template
  pitches and fake SENT (removed from the UI) — phase 5.
- Discovery + checks still run inside HTTP requests (no background worker yet) — phase 3. Leaving Find while
  checks run stops them; Review → "Check websites for 25 businesses" continues.
- The API has no authentication; keep it on 127.0.0.1.
- `npx oxlint` cannot run on this PC (native binding missing); `npm run build` passes.
- `ui_shots.db` (local, git-ignored) holds two demo HOT leads + a demo label used only for screenshots;
  `dev_preview.db` is untouched by those demo actions.
- **Not pushed** — the Claude OS guard hook blocked `git push` earlier. Run:
  `git push -u origin phase-01-pipeline-repair`, then open a PR into `main`.

## Next session starts here
- Answer the calibration question (a / b), then phase 3 (background jobs) or phase 5 (remove old fabricated APIs).
- First commands (PowerShell, repo root):
  `.venv\Scripts\python -m pip install -e ".[dev]"` ·
  (this PC only) `$env:DISABLE_SQLALCHEMY_CEXT="1"; .venv\Scripts\python -m pip install --force-reinstall --no-deps --no-binary sqlalchemy sqlalchemy` ·
  `.venv\Scripts\python -m pytest -q` (expect 201 passed) · `cd frontend; npm install; npm run build`
- Run: `docs/USER-GUIDE.md` §0.
- Watch out for: Overpass / Nominatim rate limits; OpenFreeMap tiles are free "as-is" (map shows an error
  state with Retry if they fail; every list still works).
