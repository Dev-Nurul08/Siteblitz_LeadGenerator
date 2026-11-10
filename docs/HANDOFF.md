# HANDOFF — SiteBlitz Lead Generator — Phase QA-1 (QA audit + high-severity fixes) — 2026-11-10

Branch: `phase-01-pipeline-repair`. The full report is `docs/qa/QA_REPORT.md`. Every bug, with its expected result,
the actual result, how to reproduce it and the owning phase, is in `docs/qa/ISSUES.csv`.

## Done
- **Launcher works:** double-clicking `run_all.bat` with no `.env` starts the backend and the frontend.
  - Backend on :8000, frontend on :5173.
  - It uses `.venv` and a SQLite file, and every API call answers 200.
  - Before: the launcher failed with "path not found" and every API call returned 500.
- **Error messages:** rejected input shows the field and the reason, for example
  "page_size: Input should be greater than or equal to 1". Before, it showed "[object Object]".
- **Dates:** every date shows India time. A check made a moment ago reads "just now"; it used to read "6 h ago".
- **Unsubscribe:** one person unsubscribing blocks only their own address. Before, it blocked every business on the same email
  domain, gmail.com included.
- **Writer privacy:** the owner's reply (`TASK.inbound_message`) reaches the AI model with phone numbers and emails
  removed.
- **Missing country:** a lead with no country is held for review. It is no longer approved as US for automated
  sending.
- **Lead Radar:** the funnel now says it shows 100 generated example places, not real businesses.
- **Checks:**
  - Backend tests: 325/325, including 3 new regression tests.
  - Frontend build and lint pass.
  - All 34 GET routes answer.
  - All 6 screens render at 1280 and 390 px with no page errors.
  - Every screen shows an error and a Retry button when the backend is down.

## Files changed
- `run_all.bat`, `run_all.py` — use `.venv\Scripts\python.exe` (fall back to `venv\`); the .bat runs from its own folder.
- `backend/app/config.py`, `.env.example` — default `DATABASE_URL` is `sqlite+aiosqlite:///./siteblitz_leads.db`;
  Postgres lines commented.
- `frontend/src/services/api.js` — `errorMessage()` turns FastAPI 422 lists into "field: reason".
- `frontend/src/lib/format.js` — timestamps without an offset are read as UTC.
- `backend/app/services/qualification_service.py` — `add_opt_out` stores a domain only when it is given explicitly.
- `backend/app/engines/writer/writer.py` — `model_task()` redacts and checks TASK like LEAD.
- `backend/app/engines/qualification/compliance_evaluator.py` — no "US" default; a profile that does not permit
  outreach goes to manual review.
- `frontend/src/pages/LeadRadarPage.jsx` — honest "sample data" line (only change to the colleague's page).
- Tests:
  - `backend/tests/test_integration/test_pipeline_api.py` — unsubscribe test
  - `test_writer/test_writer.py` — TASK redaction test
  - `test_qualification/test_compliance_evaluator.py` — missing-country test
- `docs/qa/` — QA_REPORT.md, ISSUES.csv (45 IDs), QA_COVERAGE.csv, `evidence/2026-11-10/*.log`,
  `screens/2026-11-10/*.png`, `tools/` (Playwright UI sweep, GET smoke, 422 probe).
- `docs/PHASES.md` (rows QA-1 ✅, QA-1b ⬜, LR ⬜; QA IDs added to phases 3/5/13/14/15) and `docs/DECISIONS.md`.

## Decisions made
- All are in `docs/DECISIONS.md` under "2026-11-10 - QA-1":
  - The app uses SQLite by default.
  - An unsubscribe suppresses that address only.
  - There is no default country.
  - The frontend reads offset-less timestamps as UTC.
  - Lead Radar is only labelled, because it is the colleague's code.
  - Fixing stopped at 13 files; the rest went onto the board.

## Known broken / deliberately skipped
- **37 open bugs** in `docs/qa/ISSUES.csv`, each assigned to a phase. Not fixed because of the ~8-file phase rule.
  The ones that matter before any real sending:
  - QA-031: the SSRF guard can be bypassed by DNS rebinding.
  - QA-032: the redactor misses landline and spaced phone formats.
  - QA-033–036: the validator can be bypassed.
  - QA-006: the unsubscribe link has no token.
- **Lead Radar still shows generated places, defaults to Mumbai and returns 500 on bad input** (QA-012/020/029/030).
  It is colleague Dev-Nurul08's code; row LR asks to agree with them first.
- **Not run:**
  - Live discovery (external network)
  - The Postgres path (no Postgres here)
  - Empty and loading screenshots (the 2026-11-08 ones remain)
  - The live writer run (no `ANTHROPIC_API_KEY` or `.env` on this PC)
- **Open findings marked "subagent probe" were not re-run by the parent session.** Their scripts are outside the repo
  in `E:\tmp\_qa_scratch\`.
- **Leftover files:**
  - `siteblitz_leads.db`: an empty, gitignored file in the repo root, created by the launcher test. It is now the
    default DB.
  - `E:\tmp\_qa_scratch\`, `E:\tmp\_writer_dryrun\` and `E:\tmp\_jiter_probe\` are still on disk.
- **Not pushed by this session.** Earlier sessions recorded that the guard hook blocks `git push` from Claude. The
  branch is ahead of origin by 14 + 9 commits.
- **Untracked `docs/debate/*/shots`, `tab.json` and `stop-awake`** are from the debate tool's sessions. They were left
  alone.

## Next session starts here
- Phase 14: an email finder for the 2,162 phone-only Navsari/Surat sites in the 3 demo verticals.
  - Fix QA-038 first, so coaching/tuition businesses are no longer skipped as "school".
  - Fix QA-040 inside it: robots.txt, emails only from mailto links / visible text / Cloudflare-encoded addresses,
    a 2 MB body limit and 5 redirects.
- First command: `/boot`, then `go`.
- Watch out for: never call `ContactDiscoveryEngine.discover_contacts()`, because it fabricates addresses. Reuse
  `_crawl_contact_pages` / `_extract_from_html` only after fixing QA-040, because `_extract_from_html` currently
  picks up `you@example.com` placeholders and Sentry keys from scripts.
- Push first, by hand: `git push origin phase-01-pipeline-repair`.
