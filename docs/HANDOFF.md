# HANDOFF — SiteBlitz Lead Generator — Phase E (email engine v2, E1-E6) — 2026-11-12

## Done
- **Two strategy rounds with ChatGPT** (`docs/debate/2026-11-12-clients-without-selling/`, `docs/debate/2026-11-12-email-engine-personas/`).
  - The agency kit is in `docs/agency/`.
  - The founder then chose email: spec lock `docs/spec/email-engine-v2.md` (20 rows), approved with "go for all".
- **E1 eligibility.** For each (business, email) the app decides TIER1 / TIER2 / HOLD, with reason codes. Every address keeps its source URL, capture date and an excerpt.
  - Email verification: syntax + MX, then Bouncer when a key is set.
  - A rendered 390 px phone check takes a screenshot.
  - SITE_DOWN is re-checked right before sending.
  - The founder's Instagram check is an API.
  - `discover_contacts()` and the generated-email CSVs are deleted.
  - Pool: 10,725 Gujarat businesses visited; 26 are eligible once verified.
- **E2 sending core.**
  - Scheduler: Tue-Thu, 09:00-11:30 / 14:00-16:30 IST.
  - Caps: 30 per mailbox per day; 25 campaign + 5 replies; ramp 10/15/20.
  - Worker: lock file; fresh website suppression check before every SMTP submission; RFC 8058 headers.
  - DSN parser and the pause/stop rules.
  - An UNCERTAIN send is never retried.
- **E3 batch screen** (React Outreach tab).
  - Flow: select → AI writes T1-T3 → validator → READY/HOLD cards with evidence → approve → scheduled.
  - The 11th lead on a 10-a-day day is refused.
  - Screenshots: `docs/screenshots/e3-batch/`.
- **E4 reply loop.**
  - IMAP reconcile at least every 24 h.
  - Deterministic stop / complaint / out-of-office rules; the model labels the rest.
  - AI drafts wait for approval; snapshots are created on the website.
  - Daily brief API and `/start-day` (`.claude/commands/start-day.md`).
  - 87-reply eval set: 0 missed stop.
- **E5 recordings.** The founder's recorded voice per vertical comes from `docs/outreach/recordings.json`.
- **Website (E:\Temp\SiteBlitz) O1** is built and live:
  - `/u/` unsubscribe, the suppression API and `/s/` snapshot pages; 368 tests.
  - The truthful site was deployed by the website session (fa3cd13). Claude checked production: 0 invented reviews, no Mumbai, no withdrawn prices.
- **Pre-send persona review (gate h)** with ChatGPT and a Claude panel; 5 fixes applied:
  - NO_VIEWPORT sentence and subject reworded;
  - T2 names the sender;
  - WhatsApp/phone replies can stop a sequence;
  - Instagram-only leads with an own-domain address are held.
- **Tests:** 805 passed on the final code (after the pre-send fixes); the frontend build passes; the website has 368 tests.

## Files changed
- `backend/app/engines/eligibility/`, `services/eligibility_service.py`, `models/eligibility.py`, `api/v1/outreach.py` — E1 rules, verification, render check, API.
- `backend/app/engines/sending/`, `models/sending.py`, `services/{sending,delivery_rules,outreach_worker}_service.py`, `api/v1/outreach_sending.py`, `scripts/outreach_worker.py` — E2 sending core, plus replied-elsewhere and sequence search.
- `backend/app/engines/writer/{writer,validator}.py`, `models/outreach_batch.py`, `services/batch_service.py`, `api/v1/outreach_batches.py`, `frontend/src/pages/BatchScreen.jsx` — E3 pilot templates and batch screen.
- `backend/app/engines/replies/`, `models/replies.py`, `services/{reply,inbox_guard,brief}_service.py`, `api/v1/outreach_replies.py`, `scripts/outreach_reconcile.py`, `scripts/register_outreach_tasks.ps1`, `.claude/commands/start-day.md` — E4.
- `scripts/pool_e1.py`, `scripts/render_check.cjs`; `enrichment/site_visit.py` and `discovery.py` — crawl memory fixes and UTC times.
- `docs/spec/email-engine-v2.md`, `email-engine-v2-contracts.md` — spec and the cross-repo contract, with the token known-answer vector.
- `docs/outreach/{pilot-templates,e2-notes,e3-notes,e4-notes,e1-eligibility-run-2026-11-12,email-engine-setup,e6-launch-gates}.md`, `recordings.json` — templates, decisions, the founder setup guide, the gate log.
- `docs/agency/` — the agency kit; `docs/PHASES.md`, `docs/DECISIONS.md`, `CLAUDE.md`.

## Decisions made
- India-only pilot.
  - Tier 1 addresses only: found on the business's own page, or seen by the founder.
  - Three observations: SOCIAL_ONLY / NO_VIEWPORT / SITE_DOWN.
  - Mailforge is the sending service: its Terms §3.4(1) allow unsolicited B2B outreach where the law allows it.
  - No Gmail, Workspace or Vercel sending.
- The website's suppression list is authoritative. The laptop keeps only a display copy.
- Synthetic voice stays banned; only the founder's own recording is used.
- Sample pages only after a positive reply; no tracking pixels and no "opens" count.
- Worker phases ran in separate git worktrees, then were merged; conflicts were additive only.
- Defaults for the open questions are listed in `docs/DECISIONS.md` (2026-11-12, email engine v2 build).

## Known broken / deliberately skipped
- **Website outreach routes answer 503** — `OUTREACH_API_KEY` and `OUTREACH_SIGNING_SECRET` are not set in Vercel. Claude's Vercel production change was denied by the safety classifier, so this needs the founders (O2).
- **0 leads are sendable** — there is no `BOUNCER_API_KEY`, sender facts, sending domains or Mailforge mailboxes yet. 26 leads become eligible once verified.
- **Pool too small for more than about 2 weeks** — automated Instagram reading is banned, so SOCIAL_ONLY needs the founder's checks and a separate import.
- **Real AI-writer pass rate and cost not measured** — the tests stub the model. Start with a batch of 1.
- **Seed tests, 10-reader test, "founder reads 20" (gates c, g, i) not done** — they need the founders.
- **Leftover worktrees** `E:\tmp\_lg_e2`, `_lg_e3`, `_lg_e4` (branches merged) and `.claude/worktrees/agent-a8e5388c0ea15d512` (unused) remain. `_lg_e3\frontend\node_modules` is a JUNCTION to the main checkout's folder: remove the junction with `rmdir` (no `/s`) before `git worktree remove`, never `rm -rf`.
- **Scratch folders** `E:\tmp\_strategy\`, `E:\tmp\_sb_deploy_e0\`, `E:\tmp\_lg_e3_qa\`, `E:\tmp\_sb_outreach_qa\` and `%TEMP%\lg_e2_smoke` can be deleted.

## Next session starts here
- Phase E6 (pilot launch): once the founders finish `docs/outreach/email-engine-setup.md` sections 2-4, run the remaining launch gates (seed tests, live unsubscribe, verification of the 26). Then write batch 1 with ONE lead, read it, and raise the ramp to stage 1.
- First command: `.venv\Scripts\python.exe scripts\outreach_worker.py --check`
- Watch out for: this PC often has < 1 GB free RAM. Crawls need `--min-free-mb`, and the full test suite (~5 min) can hit MemoryError while other sessions run.
