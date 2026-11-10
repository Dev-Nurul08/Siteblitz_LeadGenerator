# HANDOFF — SiteBlitz Lead Generator — Phase 13 (AI outreach writer) — 2026-11-10

Branch: `phase-01-pipeline-repair`. Earlier phases (1–4d, 2026-11-08) are on `docs/PHASES.md`; the outreach
strategy debate of the same day is in `docs/debate/2026-11-10-outreach-lifecycle-to-payment/RESULT.md`.

## Done
- Founder approved the 18-row spec `docs/spec/outreach-engine.md` ("go for it"). Phase 13 of it is built.
- The writer `OutreachWriter.write(lead, task)` in `backend/app/engines/writer/writer.py` does the following:
  - It holds a lead by the rules before any model call: country not listed or not PILOT, no opt-in, no
    observation, missing `.env` facts, suppressed.
  - It sends Claude Sonnet 5.5 an allow-listed lead in which emails and phone numbers are redacted and the lead id
    is left out. The request also carries server-side `fallbacks: "default"`, a cached system prompt and a JSON
    schema for the answer.
  - It validates the answer and asks for one rewrite when a check fails. A lead that fails twice becomes
    `VALIDATION_FAILED` for the founder.
  - It adds the signature and the addresses itself. The model never writes them.
- The validator `backend/app/engines/writer/validator.py` checks:
  - declared country and language against `docs/outreach/country-language.csv`, with the language confirmed by
    `langdetect`;
  - Roman Hindi only after the owner wrote in Roman Hindi;
  - word counts per channel and touch, one closing question and no link in first messages;
  - that the highest-priority observation is used, with its evidence word for word;
  - that every number and domain in the message comes from the inputs;
  - banned phrases and characters, and no unresolved placeholders;
  - opt-out line and sign-off.
- `build_observations()` turns stored website checks (≤ 30 days old) into the 7 observation types (BROKEN_FORM is
  never produced, see below).
- A missing country is now a hold in `country_rules.py`. It used to be treated as the US.
- Acceptance results:
  - 30 fixture leads (10 per vertical, Surat/Navsari): 27 READY on the first attempt and 3 held by the rules.
  - One test per validator rejection.
  - A test proves no email or phone reaches the request.
  - Full suite: **322 passed**.

## Files changed
- `backend/app/engines/writer/{__init__,validator,writer}.py`: the writer and its validator (new).
- `backend/tests/test_writer/test_validator.py` and `test_writer.py`: 40 tests.
- `backend/tests/test_writer/test_fixtures_dryrun.py`, `fixtures_30.json` and `dryrun_outputs.json`: the 30-lead
  acceptance run.
- `backend/app/engines/qualification/country_rules.py` and its test: missing country = hold.
- `backend/app/config.py` and `.env.example`: add `ANTHROPIC_API_KEY` and the `SITEBLITZ_SENDER_NAME` /
  `_REPLY_EMAIL` / `_POSTAL_ADDRESS` settings.
- `pyproject.toml`: add `anthropic>=2.7.0` and `langdetect>=1.0.9`.
- `docs/outreach/*`: the system prompt, company facts, country-language table, reference messages and
  `count_words.py`. The model's output fields are now body / signoff / opt_out_line.
- `docs/spec/outreach-engine.md`, `docs/PHASES.md`, `docs/DECISIONS.md` and `CLAUDE.md`: approval, phases 13–16,
  decisions, location rule.
- `docs/debate/2026-11-10-outreach-lifecycle-to-payment/RESULT.md`: "Mumbai" corrected to Gujarat / Navsari+Surat.

## Decisions made
- These are in `docs/DECISIONS.md` under the two 2026-11-10 blocks:
  - The AI writes every message.
  - The studio is described as "based in Gujarat".
  - No automated WhatsApp Web sending and no social bots.
  - The signature is assembled by the app.
  - Personal facts stay in `.env`.
  - Holds are decided before the model is called.
  - Server-side fallback is on.
  - jiter must be pinned to 0.8.2 on this PC.

## Known broken / deliberately skipped
- **No live API run yet**, because there was no `ANTHROPIC_API_KEY`. The 27 recorded answers came from Claude Code's
  own model (Opus 5.5) standing in for `claude-sonnet-5-5` on the exact same prompt. Re-record the run once the key
  is set.
- Every real lead is held (`MISSING_COMPANY_FACT`) until the founder sets the three `SITEBLITZ_*` values in `.env`.
- BROKEN_FORM is never produced, because no form-test check type exists yet.
- Demo links stay `TO FILL`: `siteblitz.vercel.app/demo/*` returns 404 because the SiteBlitz repo's `v2-redesign`
  branch is not deployed (that is the SiteBlitz site session's job, not this repo).
- Nothing is sent anywhere. Sending, the batch screen and the 100/day cap are phase 15.
- Phases 14–16 were not started (one phase per session).
- `E:\tmp\_writer_dryrun\` (scratch dry-run inputs) and `E:\tmp\_jiter_probe\` (a downloaded wheel) are left on
  disk outside the repo. Deleting them was not permitted in this session.

## Next session starts here
- Phase 14: the email finder for the 2,162 phone-only Navsari/Surat sites in the 3 demo verticals. It must respect
  robots.txt, take emails only from the business's own pages and record the viewport / HTTPS / site-down checks on
  the same visit (spec rows 9–12).
- First command: `/boot`, then `go`.
- Watch out for: never call `ContactDiscoveryEngine.discover_contacts()`, because it fabricates gmail addresses and
  `+91 9825…` phone numbers. Reuse only `_crawl_contact_pages` / `_extract_from_html`.
- After setting the key: `.venv/Scripts/python.exe -m backend.app.engines.writer.writer
  backend/tests/test_writer/fixtures_30.json` (live run, spends API credit).
