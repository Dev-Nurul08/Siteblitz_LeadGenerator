# QA report: SiteBlitz Lead Generator, 2026-11-10

Scope: everything built so far (phases 1–1f, 2, 4a–4d, 13, plus the Lead Radar page merged from main).
Branch `phase-01-pipeline-repair`. The audit started at 834cdb9 and the fixes run through 7b3ac9a.

## Verdict
The app is **partially verified**:
- The core flow works on this PC: Find → Review → Hot leads → Outreach → Settings.
  - All 34 GET routes answer.
  - All 6 screens render at 1280 and 390 px with no page errors.
  - Error states show when the backend is down.
- 8 bugs were fixed (6 high, 2 medium). For QA-012 only the label is fixed; showing real data is still open.
- 37 other bugs are open. Each one is assigned to a phase in `docs/PHASES.md`.
- The app is **not ready to contact real businesses**:
  - Two writer gaps are open: the phone redactor misses some formats (QA-032), and the validator can be bypassed (QA-033–036).
  - The SSRF guard can be bypassed by DNS rebinding (QA-031).
  - The unsubscribe link has no token (QA-006).
  - Nothing sends messages yet anyway; sending is phase 15.

## Stages
| Stage | Result |
|---|---|
| Backend tests | 322/322 before the fixes, 325/325 after (3 new regression tests) |
| Frontend build + lint | Pass. Lint gives warnings only. |
| Fresh start and launcher | Failed, fixed (QA-001, QA-002), and verified by running `run_all.bat` |
| API sweep: GET routes, 404 and 422 probes, CSV/PDF export | Pass |
| UI sweep, Playwright, 6 screens × 1280/390 + backend down | Pass. One exception: Lead Radar overflows at 390 px (QA-030). |
| Phase 13 writer claims | 2 claims were incomplete, both fixed: QA-015 (missing country) and QA-016 (privacy). The live API run is BLOCKED because there is no key. |
| Code review by 3 read-only subagents (API, frontend, engines) | 43 findings, deduplicated into ISSUES.csv. The parent session re-checked the code for the fixed ones. |

## Fixed this session
| ID | Bug | Commit |
|---|---|---|
| QA-001 | No `.env` meant the app used PostgreSQL by default, so every API call returned 500. The default is now a SQLite file, as the README says. | 315d5f9 |
| QA-002 | `run_all.bat` pointed at `venv\` but the virtual environment is `.venv\`, so the launcher failed. | 315d5f9 |
| QA-003 | Rejected input showed "[object Object]". It now shows the field and the reason. | 5d71712 |
| QA-004 | Every date was 5 h 30 min early, and "just now" showed as "6 h ago". | 17440c6 |
| QA-005 | One unsubscribe from a gmail address blocked **every gmail business**. | ff94ae8 |
| QA-012 | The Lead Radar funnel showed 100 made-up places as real data. It is now labelled as sample data; showing real data is still open. | dd0eb28 |
| QA-015 | A lead with no country was evaluated as US and approved for automated sending. | 7b3ac9a |
| QA-016 | The owner's reply, including their phone number and email, was sent to the AI model unredacted. | e84fe33 |

Every fix has a log in `evidence/2026-11-10/fix-*.log`. Each log shows the failure before the fix and the pass after it.

## Open, by owner phase
These are in `docs/PHASES.md`.
- **QA-1b (new remediation phase):**
  - API: 007, 010, 014, 017, 018, 044
  - UI: 022, 023, 024, 026, 027, 028, 045
  - Writer hardening: 032–036, 043
  - Intelligence: 037, 038
  - Discovery: 039, 042
  - Country table: 041, which needs a founder decision on which table wins
- **Phase 3:** 031 (DNS rebinding in the SSRF guard)
- **Phase 5 (old Contacts/Campaigns/qualification APIs):** 006, 008, 009, 011, 013, 019, 021
- **Phase 14:** 040. The contact-page extractor and resolver break spec rows 9–12: no robots.txt check, emails read from placeholders and scripts, no 2 MB or 5-redirect limit.
  - Phase 14 should also land QA-038 first. Otherwise coaching/tuition businesses, one of the 3 demo verticals, are skipped.
- **Phase 15:** 025 (wa.me links built from local-format numbers)
- **LR, Lead Radar (colleague Dev-Nurul08's code):** 012 (real data), 020, 029 (Mumbai defaults against the Navsari + Surat rule), 030

## Limitations
- Not run:
  - Live discovery (external network)
  - The Postgres path (no Postgres on this PC)
  - Empty and loading UI states (the 2026-11-08 screenshots are the only evidence)
  - The live writer run (no `ANTHROPIC_API_KEY`)
- The subagents' probe scripts are outside the repo, in `E:\tmp\_qa_scratch\`. Open findings marked "subagent probe" have not been re-run by the parent session.
- The runtime checks used a copy of `dev_preview.db` (`E:\tmp\_qa_scratch\qa_runtime.db`), not a live database.
- A full ISSUES.csv does not mean no other bugs exist.

## Re-run
- `.venv/Scripts/python.exe -m pytest backend/tests -q`
- `docs/qa/tools/ui_sweep.cjs`:
  - Needs Playwright. The npx cache has it at `%LOCALAPPDATA%\npm-cache\_npx\e41f203b7505f1fb\node_modules\playwright`; pass that path as `PW_PATH`.
  - Run: `node ui_sweep.cjs <out dir>`.
  - Optional environment variables: `WIDTHS=1280,390` and `PREFIX=`.
- `docs/qa/tools/api_get_smoke.py` hits every GET route on a running backend.
