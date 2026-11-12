# Email engine v2 - E2 sending core: decisions and notes (2026-11-12)

Spec: `docs/spec/email-engine-v2.md` rows 5, 8-13, 16, 18, 19 (founder `go`, 2026-11-12). Contract with the website:
`docs/spec/email-engine-v2-contracts.md` (token, hashes, suppression API, headers) - implemented exactly; the
known-answer vector is a test (`backend/tests/test_sending/test_tokens.py`). This file records what E2 decided where
the spec was silent. Nothing here changes E1 behaviour; E2 calls `EligibilityService.recheck_before_send`.

## What was built
| Part | Where |
|---|---|
| Tables `mailboxes`, `email_sequences`, `send_records`, `pause_flags`, `ramp_settings`, `delivery_events`, `suppression_mirror` (display only) | `backend/app/models/sending.py` |
| Token / hash (contract) | `backend/app/engines/sending/tokens.py` |
| Scheduler (pure, fake-clock tests) | `backend/app/engines/sending/scheduler.py` |
| Message builder (plain text, headers, threading) | `backend/app/engines/sending/message.py` |
| SMTP adapter (smtplib, STARTTLS / SSL, 30 s) | `backend/app/engines/sending/smtp.py` |
| Suppression client (check / add / list) | `backend/app/engines/sending/suppression_client.py` |
| Bounce / DSN parser (module only; E4 wires IMAP) | `backend/app/engines/sending/dsn.py` |
| Pause / stop rule helpers | `backend/app/engines/sending/pause_rules.py` |
| Service: sequences, capacity, ramp, pauses, missed windows, UNCERTAIN resolution | `backend/app/services/sending_service.py` |
| Rules applied to the database (bounces, complaints, policy, integrity, backlog) | `backend/app/services/delivery_rules_service.py` |
| Worker loop | `backend/app/services/outreach_worker.py`, CLI `scripts/outreach_worker.py` |
| API | `backend/app/api/v1/outreach_sending.py` |

Worker: `.venv/Scripts/python.exe scripts/outreach_worker.py` (loops until 16:30 India time today, a cycle every
60 s), `--once` (one cycle), `--check` (start-up checks only). Exit code 2 = refused to start.

## Decisions (E2)
1. **Names.** The sequence model is `EmailSequence` (`Sequence` clashes with `sqlalchemy.Sequence`), matching
   `EmailEligibility` / `EmailCapture`.
2. **Pause flags** have a scope (GLOBAL, NEW_CONTACTS, DOMAIN, MAILBOX, SOURCE, SOURCE_BATCH) and a level (PAUSE,
   STOP). NEW_CONTACTS and SOURCE were added to the brief's four scopes because spec row 11 needs "no new first
   contacts" and "stop that source". A flag blocks until a person clears it with `POST /outreach/pauses` (who + note).
   Raising the same active flag twice returns the existing one.
3. **"That domain"** in the policy-rejection rule = the sending domain (the mailbox's domain).
4. **Source and batch** come from the capture behind the eligibility row: batch = `EmailCapture.origin`
   (e.g. `email_finder:2026-11-10`), source = the part before `:` (`email_finder`). No capture = `unknown`.
5. **Admission** is for one recipient-local day (the E3 batch day). A prospect is admitted only when steps 2 and 3
   fit on the same mailbox: step 2 between Day 6 and Day 13 (before step 3 is due), step 3 between Day 14 and Day 21
   (Day 21 = the maturity point in RESULT row 16). Mailboxes are tried least-loaded first, then by id.
6. **Slots.** Inside a day, each new message goes to the window with fewer messages (ties: morning), 6 minutes after
   the previous one (150-minute window / 25 messages), never earlier than "now".
7. **Ramp.** No row = stage 0 = no new first contacts (week 1 starts only after the launch gates, row 17). Stages
   1-4 = 10 / 15 / 20 / 20, locked. The stage moves up one step per call (each step needs the founder's yes) and down
   freely; every change stores who, when and a note. Going above 20 needs a spec change (the commercial gate is not
   automated in E2).
8. **Follow-up text.** Steps 2 and 3 are reserved at admission without text (`Re: <step 1 subject>`). Their text and
   approval arrive through `POST /outreach/send-records/{id}/approve` (added; not in the brief's route list, but
   without it a follow-up could never be approved). An unapproved due message is held `NOT_APPROVED`.
9. **Body.** The app appends `Reply "stop" or unsubscribe here: {base}/u/{token}` as the last line; a trailing line
   already starting with `Reply "stop" or unsubscribe here:` (the writer's placeholder) is replaced. Quoted-printable
   UTF-8; header lines up to 998 characters so the List-Unsubscribe URL is never folded inside the token.
10. **SMTP outcomes.** 2xx at end of DATA = ACCEPTED. 5xx at RCPT / DATA = FAILED, classified like a DSN (5.1.x hard
    bounce, 5.7.x policy, otherwise an UNKNOWN_BOUNCE event); the later steps are cancelled. A 4xx answer, or any
    connection / TLS / login problem before the message text was sent, is NOT_SENT: the record goes back to
    SCHEDULED for 6 minutes later (it becomes "missed" and moves on at the window's end). Connection / TLS / login
    trouble or a refused envelope sender pauses that mailbox (`SMTP_UNAVAILABLE`).
11. **UNCERTAIN** (timeout or lost connection after the message text was sent): never retried; global pause
    `SEND_RESULT_UNKNOWN`. That pause cannot be cleared while any record is UNCERTAIN; resolving the last one through
    `POST /send-records/{id}/resolve` clears it. A record resolved as ACCEPTED keeps `submitted_at` as its
    acceptance time (the real one is unknown). Start-up turns every SUBMITTING record into UNCERTAIN.
12. **Integrity.** Each cycle audits submitted records: no approval = `UNAPPROVED_SEND`; the same step submitted
    twice to one recipient = `DUPLICATE_SEND`; a submission after the local mirror had already seen the suppression =
    `SUPPRESSED_SEND`. Each is a global pause; the record is marked so a cleared pause is not raised again for the
    same incident. A duplicate caught BEFORE submission is cancelled and still raises `DUPLICATE_SEND` (it means a
    bug upstream). A suppression created between the fresh check and the submission is the honest limit of spec
    row 13, not an incident.
13. **Check order** is the brief's (approval, fresh suppression check, sequence, E1 recheck, pauses, window,
    capacity, claim, submit). Before step 1 the worker also runs steps 5-7 as a local pre-filter, so a paused, full
    or out-of-window message never causes a website or homepage request every minute. A lead that is no longer
    eligible is rechecked at most once per window. `SITE_RECOVERED` cancels the message and the sequence.
14. **Complaints** always suppress the address (website first); only a credible one pauses. Provider spam rates
    are not available, so they are not used (spec row 16: unknown, never 0).
15. **Reply backlog** (`DeliveryRulesService.check_reply_backlog`, for E4): business days are Monday-Friday in India
    time; a reply that arrives on a weekend counts from Monday 00:00. The NEW_CONTACTS pause clears itself when E4
    reports no unanswered interested reply (spec: "resume only after the backlog is cleared").
16. **Suppression writes** (hard bounce, complaint) go to the website first; if that fails, the global pause
    `SUPPRESSION_WRITE_FAILED` blocks every send. The local mirror gets the hash either way (display only).
17. **One worker.** An OS file lock (`outreach_worker.lock` next to the SQLite file) is released by Windows when the
    process ends, even after a crash, so no time-out is needed. The claim is a conditional
    `UPDATE ... WHERE state = 'SCHEDULED'`; with the unique `seq:<id>:step:<n>` key this gives one submission even if
    two workers ran.
18. **Settings** ignore unknown `.env` keys now (`extra="ignore"`): pydantic-settings' default refuses to start on
    the `MAILBOX_<SLUG>_PASSWORD` lines. Passwords are read only by the SMTP adapter, never stored or returned.
19. **Mailbox rules** (spec row 8): sending hosts of Gmail / Google, Outlook / Office 365 / Hotmail / Live, Amazon SES,
    SendGrid, Mailgun, Postmark, Brevo / Sendinblue are refused; a free-mail address cannot be a sender; the display
    name cannot be a role word ("SiteBlitz", "team", ...); TLS mode `none` only for 127.0.0.1 / localhost.
20. **Dependencies.** `tzdata` (Windows has no time-zone database; `zoneinfo` needs it for Asia/Kolkata) and, for
    tests, `aiosmtpd`. Both pure-Python wheels, installed into the main `.venv` on 2026-11-12 (tzdata 2026.6,
    aiosmtpd 1.4.6, atpublic 9.0.0, attrs 26.1.0).

## Not in E2 (later phases)
- IMAP reading, reply labels, wiring the DSN parser to real bounces, the reconciliation gate before sending (E4 calls
  `record_reconciliation_incomplete`, `record_bounce`, `record_complaint`, `stop_sequence`, `check_reply_backlog`).
- Sending replies (`SendKind.REPLY` exists so replies count against the 30 a day ceiling) and seed tests (E6).
- The batch screen (E3) and launch-gate evidence (E6), including DKIM coverage of both unsubscribe headers on
  received mail - signing is the mailbox provider's job.

## Known limits
- E1's `recheck_before_send` keeps a SQLite write transaction open during the MX lookup of a SITE_DOWN lead (seconds).
- Two batch requests at the same moment could both reserve the last slots of a day; the worker's send-time caps
  (30 / 25 / ramp) are the hard guard, so the extra message waits for the next window instead of exceeding a cap.

## Open questions for the founder
1. Business day for the reply-backlog rule: Monday-Friday (used) or Monday-Saturday?
2. A duplicate caught before submission pauses everything (used). Keep, or only cancel the duplicate?
3. A 4xx answer is retried every 6 minutes inside the window, without a cap on attempts. Add a cap?
4. Mailforge SMTP host, port and TLS mode are not on its pricing page; confirm in the Mailforge acceptance test.
