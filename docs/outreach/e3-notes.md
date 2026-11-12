# Email engine v2 - E3 batch screen + pilot templates: decisions and notes (2026-11-12)

Spec: `docs/spec/email-engine-v2.md` rows 5, 6, 9, 10, 14, 17, 19 and the E3 criterion (founder `go for all`,
2026-11-12). Reference texts: `docs/debate/2026-11-12-email-engine-personas/RESULT.md` rows 13, 16 and section C.
Builds on E1 (eligibility) and E2 (`docs/outreach/e2-notes.md`). Nothing here sends mail: approved sequences wait for
E2's worker in the supervised windows. No real model call was made in this phase (tests and screenshots use a stub).

## What was built
| Part | Where |
|---|---|
| Pilot templates T1 (SOCIAL_ONLY salon, NO_VIEWPORT coaching, SITE_DOWN retail, `other`), T2, T3 + the validator rule table | `docs/outreach/pilot-templates.md` (attached to every writer request as PILOT_EMAIL_TEMPLATES) |
| Pilot task (E1 sentence, identity, price, question, vertical page), v2 signature block, assembly | `backend/app/engines/writer/writer.py` (`pilot_task`, `assemble_pilot_email`) |
| Pilot validator rules + checks on the assembled text | `backend/app/engines/writer/validator.py` (`pilot_email_errors`, `assembled_pilot_errors`) |
| Tables `outreach_batches`, `outreach_batch_leads` (new, `create_all`, no migration) | `backend/app/models/outreach_batch.py` |
| Batch service: allowance, candidates, create, write, approve, reject | `backend/app/services/batch_service.py` |
| API `/api/v1/outreach/batches*` | `backend/app/api/v1/outreach_batches.py` |
| E2 fix: SMTP 4xx cap (3 per window, 3 windows, then FAILED soft + sequence HELD) | `delivery_rules_service.record_temporary_refusal`, `sending_service.move_to_next_window` / `hold_sequence`, worker 4xx branch |
| E2 fix: slots admitted inside an open window no longer collapse onto one time | `backend/app/engines/sending/scheduler.py` (`DayLoad.last_at`) |
| Batch screen (Outreach -> "Email batch"; manual outreach behind the switch) | `frontend/src/pages/BatchScreen.jsx`, `OutreachPage.jsx`, `services/api.js` (lines added only), `index.css` |
| Stub model for tests and screenshots | `backend/tests/pilot_fakes.py` |

API: `GET /outreach/batches/allowance?date=`, `GET /outreach/batches/candidates?status=&reason=`,
`GET /outreach/batches`, `POST /outreach/batches` (202), `GET /outreach/batches/{id}`,
`POST /outreach/batches/{id}/write` (continue after a restart), `POST /outreach/batches/{id}/approve`
(`{"lead_ids": [..] | "all_ready", "approved_by"}`), `POST /outreach/batches/{id}/reject`
(`{"lead_ids", "reason", "rejected_by"}`). Refusals are HTTP 409 with `{code, message, refused, allowance?}`.

## Decisions (E3)
1. **The AI still writes every touch.** The templates are anchors plus validator rules. The app passes the fixed
   lines in `TASK.pilot` (E1's stored observation sentence, the identity line, the exact price line, the question);
   the model writes the subject, the vertical sentence, T2 and T3; the validator checks the fixed lines word for word.
2. **E1's sentence is used as stored** ("when we checked its bio", "in our checks", "the last one shortly before this
   email"), not RESULT C's "I checked" wording (brief: do not invent new wording). The SITE_DOWN sentence is true only
   because E2 rechecks the site right before sending.
3. **T1 shape = RESULT C exactly:** no greeting (line 1 is the observation), no sign-off, no opt-out line from the
   model. The app adds `<sender> | SiteBlitz` / `<reply> | <postal>` / `WhatsApp: +91 92744 90242` and
   `Reply "stop" or unsubscribe here: <link>`. A model sign-off or opt-out line is a validator error.
4. **Subject** = `<Business>: <fact>`, fact 3-8 words, no `?` / `!` / `Re:`. The phase-13 rule (3-7 words, business
   name counted once) would reject RESULT C's own SITE_DOWN subject (`[domain] did not load in our checks` = 7 words
   + the name).
5. **No 100-words-with-signature cap for pilot emails.** Spec v2 row 5 fixes the body at 60-85 words and adds the
   WhatsApp and unsubscribe lines; the old cap would depend on the postal address length.
6. **T2** must mention the sample page, have exactly one question at the end, and use none of "just following up",
   "following up", "checking in", "circling back", "bumping", "my last email", "my previous email", "did you get a
   chance", "did you see my". **T3** has no question rule. **Pressure words** (prompt P8: limited, last chance, hurry,
   urgent, only this week, act now, offer ends, deadline, discount, don't miss) are rejected in every touch.
7. **Unsubscribe line:** until a send record exists the stored text ends with
   `Reply "stop" or unsubscribe here: [unsubscribe link added when sent]`; E2's message builder always replaces that
   line with the real per-message link (test: `test_e2_message_builder_replaces_the_placeholder_with_the_real_link`).
   The blank line E2 puts before it is kept in the preview so the preview matches the sent text. It is the only link
   allowed in T1-T3.
8. **Sender per mailbox.** The texts name the planned mailbox's founder: `[Sender]` = the mailbox display name and
   `[Reply address]` = the mailbox address, so the From line, "I'm <name> from SiteBlitz", the signature and Reply-To
   all name the same person (spec row 8: each mailbox under a real founder name). `SITEBLITZ_SENDER_NAME`,
   `SITEBLITZ_REPLY_EMAIL` and `SITEBLITZ_POSTAL_ADDRESS` stay required (E2's worker checks them); any blank one makes
   every lead HOLD `MISSING_COMPANY_FACT` before a model call. Approval pins the planned mailbox (E2
   `create_sequences` items gained an optional `mailbox_id`).
9. **Writer down never fakes text.** No `ANTHROPIC_API_KEY`, a refused key, a rate limit, an API error or no network =
   HOLD `WRITER_UNAVAILABLE` (the writer no longer returns status `ERROR`). A privacy check failure = HOLD
   `PRIVACY_BLOCKED`; an unexpected exception while writing = HOLD `WRITE_FAILED`.
10. **A lead is READY only when T1, T2 and T3 all pass** (each gets the phase-13 one rewrite). The first touch that
    fails gives the lead's HOLD code and the validator's messages.
11. **Create is all or nothing.** Any id that is not eligible, suppressed, unknown, already in a live sequence or in an
    open batch -> 409 `NOT_ELIGIBLE` listing each id with its reason. More ids than the allowance -> 409
    `CAP_REACHED`: "Only 10 new first contacts are left for <day>, you selected 11. ..." with the ids beyond the
    allowance. No partial batch is made and nothing is written.
12. **Allowance** for a sending day = ramp limit - step-1 records already scheduled that day - leads of open batches
    for that day (PENDING / WRITING / READY), never more than the free campaign slots of the usable mailboxes. It is 0,
    with the reason shown, on a non-campaign day, after the day's last window, at ramp stage 0, under a GLOBAL or
    NEW_CONTACTS pause, or with no usable mailbox. HOLD and REJECTED leads give their place back.
13. **Default sending day** = today in India time while today's last window is still open, else the next Tue-Thu.
14. **Dry run.** The proposed mailbox and times come from E2's own `create_sequences(..., dry_run=True)`: same checks,
    the batch's items see each other, nothing is written. Before approval the screen says "Proposed"; after approval
    it shows the real send records as "Scheduled" (admission runs again at approval time, so a time can move by a few
    minutes).
15. **Writing** runs in a FastAPI background task with its own session, one commit per lead; the screen polls every
    1.5 s. The request's read transaction is closed before the task starts (SQLite would otherwise lock the writer).
    If the server stops mid-batch, the leads stay WRITING and the screen offers "Continue writing".
16. **Approve** = E2 `create_sequences` (step 1 text + who/when) then `approve_follow_up` for steps 2 and 3 with their
    texts; `content_version` `pilot-v1:T1..T3`. A refusal by E2 (pause, capacity, date passed, mailbox gone) keeps the
    lead READY with `approval_refusal` {code, message, at}, so it can be approved again after the cause is fixed.
    **Reject** needs a reason (3+ characters) and a name; an APPROVED lead cannot be rejected here (stopping a
    sequence is E2 / E4's job).
17. A HOLD lead can be selected again in a later batch (a rewrite may pass). The "Eligible" view lists only leads that
    can still be selected and says how many are already in a sequence or an open batch.
18. **4xx cap** (answers E2 open question 3): every 4xx answer at RCPT / DATA is a `SOFT_BOUNCE` delivery event
    (origin `smtp`) carrying the record's window start, so no new column is needed on existing databases. 3 refusals in
    one window -> the record moves to the next permitted window with capacity (never later in the same window);
    3 refusals in each of 3 windows (or a refusal in a 4th window, when an earlier window closed before its third
    attempt) -> the record is FAILED with `hold_reason = SOFT_BOUNCE_LIMIT`, later steps are CANCELLED and the
    sequence is HELD (new `SequenceState.HELD`, not a stopped state) with the reason. No pause flag: it is about one
    recipient. Connection / TLS / login trouble still pauses the mailbox as in E2.
19. **Scheduler fix** found on the batch dry run: prospects admitted while a window was already open all got
    "now + 1 min" on a mailbox and would have left in one burst (against E2 decision 6). The capacity book now keeps
    the latest slot time per window (loaded from `send_records.scheduled_for` too) and the next slot is 6 minutes later.
20. **Screen.** Outreach opens on "Email batch"; the phase-UI manual workspace is behind the switch (`#/outreach?mode=
    manual`; old `?lead=` links still open it). "Your name" is kept in the browser and recorded on create, approve,
    reject and pause clears. Existing tokens, components and motion only; no new colour or font.

## Tests (2026-11-12, worktree `E:\tmp\_lg_e3`)
- Writer: `backend/tests/test_writer/test_pilot_templates.py` (one test per pilot rule, every template x observation x
  vertical passes, assembled text, unsubscribe URL allowed and the only link, E2 builder replaces the placeholder,
  missing fact / missing key / model down holds).
- Batch API: `backend/tests/test_batches/test_batch_api.py` (create + three texts + evidence + proposed schedule, no
  email address reaches the model, the 11th on a 10-a-day day refused with its message, ineligible / busy ids refused,
  approve all ready into E2 with three approved texts, approve selected + reject with reason, VALIDATION_FAILED hold,
  MISSING_COMPANY_FACT without a call, WRITER_UNAVAILABLE without text, stage 0, pause, approval refused by a later
  pause, bad input).
- E2 fixes: `backend/tests/test_sending/test_soft_retry_cap.py`, `test_scheduler_open_window.py`.
- Full backend suite: 642 passed (`backend/tests`, 3 min 56 s). Frontend: `npm run build` passes (node_modules
  reused from the main checkout through a directory junction).

## Screenshots
`docs/screenshots/e3-batch/` at 1280 x 800 and 390 x 844: empty (`empty-*`), selecting (`selecting-*`), cap reached
(`cap-reached-*` = the 11th row refused at selection, `cap-reached-zero-left-*` = nothing left for the day), writing
(`writing-*`), ready / hold list (`ready-hold-*`, `card-hold-1280`, `card-day6-1280`, `card-day14-1280`),
approved / scheduled (`approved-*`, `approved-in-page-1280`, `card-approved-1280`), paused banner (`paused-*`,
`pause-resolve-form-1280`). Data: a copy of `dev_preview.db` with fictional businesses only (`.example` domains,
`sb_fixture_` Instagram handles); the copy's real businesses had their social links removed so no real profile is
listed. The email texts in the screenshots come from the stub writer (`backend/tests/pilot_fakes.py`), not from the
model.

## Not done / limits
- No real model call: the real model's pass rate on the pilot rules and the API cost per batch (spec row 20, "measured
  in E3") are not measured yet. Measure on the first real batch (one lead first).
- `oxlint` could not run on this PC (its native binding is blocked, like other DLLs under Smart App Control).
- A batch is written for one sending day. Approving after that day's windows are over is refused by E2
  (`DATE_IN_PAST` / no slot); the founder writes a new batch.
- A HELD sequence has no "release" route yet: the founder decides outside the app (or E4/E6 adds one).

## Open questions for the founder
1. Signature sender = the mailbox's display name and address (used, decision 8). Keep, or one fixed sender name for
   all mailboxes?
2. Should a lead that failed validation twice be retried automatically in the next batch, or only when selected
   (used: only when selected)?
3. 4xx cap values: 3 attempts per window, 3 windows (brief). Keep?
