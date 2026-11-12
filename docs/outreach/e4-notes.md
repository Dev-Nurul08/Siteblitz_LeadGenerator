# Email engine v2 - E4 reply loop, daily brief, `/start-day`: decisions and notes (2026-11-12)

Spec: `docs/spec/email-engine-v2.md` rows 11, 13-16, 19 and the E4 criterion (founder `go for all`, 2026-11-12).
Inputs: `docs/debate/2026-11-12-email-engine-personas/RESULT.md` rows 18-20, `01_chatgpt.md` section 6, `02_chatgpt.md`
Q3, the lifecycle reply table in `docs/debate/2026-11-10-outreach-lifecycle-to-payment/RESULT.md` section D, the
contract `docs/spec/email-engine-v2-contracts.md`, and E2 (`docs/outreach/e2-notes.md`). This file records what E4
decided where those were silent.

## What was built
| Part | Where |
|---|---|
| Tables `imap_folder_states`, `mailbox_reconciles`, `inbound_messages`, `reply_drafts`, `reply_suppressions`, `opportunity_snapshots`, `brief_runs` | `backend/app/models/replies.py` |
| IMAP reader (imaplib, SSL / STARTTLS, read-only) | `backend/app/engines/replies/imap_client.py` |
| Message parser: quotes, signature, auto-reply / OOO, DSN, ARF, return dates | `backend/app/engines/replies/parsing.py` |
| Safety labels (stop, complaint_legal), commitment requests, draft rules | `backend/app/engines/replies/labels.py` |
| Sanitizer (emails, phones, links) | `backend/app/engines/replies/sanitizer.py` |
| Commercial labels from the model (strict JSON schema) | `backend/app/engines/replies/classifier.py` |
| Snapshot client + payload (contract) | `backend/app/engines/replies/snapshot_client.py` |
| Reconcile, processing, stop, OOO, drafts, approval, backlog | `backend/app/services/reply_service.py` |
| 24 h inbox guard (also run by the worker each cycle) | `backend/app/services/inbox_guard.py` |
| Daily brief | `backend/app/services/brief_service.py` |
| API | `backend/app/api/v1/outreach_replies.py` |
| Scheduler script / task registration (NOT run) | `scripts/outreach_reconcile.py`, `scripts/register_outreach_tasks.ps1` |
| `/start-day` | `.claude/commands/start-day.md` |
| Labelled reply set (87 cases) | `backend/tests/test_replies/fixtures/reply_eval_set.json` |

Run once: `.venv/Scripts/python.exe scripts/outreach_reconcile.py` (exit 0 = every mailbox read, 1 = a mailbox
failed and stays paused, 2 = refused: another run busy / no mailbox). Register the Task Scheduler jobs (daily 08:30,
Tue-Thu 08:55-16:30 every 30 min) once, by hand: `powershell -ExecutionPolicy Bypass -File scripts\register_outreach_tasks.ps1`.
API routes: `POST /api/v1/outreach/reconcile`, `GET /outreach/inbound`, `POST /outreach/inbound/{id}/close`,
`GET /outreach/drafts`, `POST /outreach/drafts/{id}/approve | reject | regenerate`, `GET /outreach/brief?date=`.
No new environment variables: IMAP uses the same `MAILBOX_<SLUG>_PASSWORD`; host / port / TLS come from the mailbox row.

## Decisions (E4)
1. **Folders.** INBOX and the junk folder (`\Junk` special-use or a usual name such as Junk / Spam): a "stop" the
   provider filed as spam still counts. SELECT is read-only and FETCH uses `BODY.PEEK[]` (no \Seen flag), at most
   1 MB per message. The raw message is not stored; its size and SHA-256 are.
2. **UIDVALIDITY change** = every UID changed: the folder is read again from the mailbox's first send minus 1 day (or
   30 days back); messages already stored are recognised by Message-ID (else SHA-256), never stored twice.
3. **Complete read.** At most 300 new messages per folder per run; more left = the run is incomplete (no success
   time), the next run continues. A mailbox without IMAP host / port / TLS can never be read, so it is always paused.
4. **Inbox guard** ("reconciliation incomplete"): MAILBOX-scope pause `INBOX_NOT_RECONCILED` for a mailbox whose
   inbox was not read completely in 24 h (E2's helper raises a GLOBAL pause; the task asked for "that mailbox"). A
   complete read clears it automatically: the condition itself is resolved, it is not a time-based restart. Checked
   by every reconcile and by the sender worker each cycle (`OutreachWorker(inbox_guard=...)`, on by default; the E2
   worker tests pass `None`). So a laptop that skipped reconciling never sends.
5. **Matching:** In-Reply-To, then References (newest first) against every Message-ID we sent (campaign steps and
   replies); else the From / Reply-To address + the same mailbox (newest sequence). Unmatched human mail is flagged.
6. **First action** for a person's reply: E2 `stop_sequence(STOPPED_REPLY)`, committed before labels, model or
   drafts. A stop then refines the state to STOPPED_SUPPRESSED.
7. **Kinds:** our own copies, read receipts and list / bulk mail are ignored; an ARF feedback report is a credible
   complaint; a DSN goes to E2's `record_bounce` (suppress / pause); auto-replies are out-of-office.
8. **Out of office:** detected by `Auto-Submitted` (not "no"), `X-Autoreply`, `X-Autorespond`,
   `Precedence: auto_reply`, a typical subject (English, Hindi, Gujarati) or a short opening such as "I am out of
   the office" without a question. Sequence PAUSED_OOO (its follow-ups are kept and held by the worker). Resume at
   00:00 India time 2 business days (Mon-Fri) after the return date; a date before the message or > 90 days later
   is ignored; no date = 14 days after it arrived. "Resume" makes the sequence ACTIVE again; every follow-up still
   needs the founder's approval, which is the review. Never answered, no model call.
9. **Stop rules** (full list in the docstring of `labels.py`): English, Hinglish, Hindi and Gujarati (romanised and
   script). "Not interested" (also "not interested right now"), "no thanks" and a reply that is only "no" / "nahi"
   are stops (lifecycle table: "No / stop / unsubscribe -> SUPPRESSED"). "Don't stop", "one-stop", "stop by",
   "stopped working" are not. "Unsubscribe" on a newsletter-footer line or below a `-- ` signature is not. A
   deletion request is a stop + flagged. Stop wins over every commercial label: no model call, no draft. When the
   new text is empty (written under the quote), the rules read the whole body without `>` lines and our footer.
10. **Stop handling:** website first (`POST /api/outreach/suppressions`, reason `reply_stop`, through E2's
    `DeliveryRulesService.suppress`), then locally: display mirror, an `opt_outs` row (E1 reads it), every live
    sequence of the address stopped. Both the sequence's recipient and a different replying address are suppressed.
    Website write failed: `reply_suppressions` row PENDING (retried by every reconcile) and E2's global pause
    `SUPPRESSION_WRITE_FAILED` (E2's reason for a failed write; `SUPPRESSION_UNAVAILABLE` is its reason for a failed
    check). A person clears that pause after the retry shows WRITTEN: E2's own bounce writes have no retry row, so
    clearing it automatically would be unsafe.
11. **Stop confirmation:** default no reply. One fixed line from the lifecycle table ("Understood, thank you for
    letting me know.") + the sender name is stored as an OPTIONAL draft: not in the default list, never part of
    `send`, sent only when the founder approves that draft by id. It is the one reply that skips the suppression
    check (the address is suppressed by design) and E2's integrity audit skips it (key prefix
    `reply:stop-confirmation:`). Only one per sequence.
12. **Complaints:** credible = a spam report or a legal threat (report you, marked as spam, lawyer, legal notice,
    police complaint, cyber cell, consumer court, DPDP / GDPR, harassment, shikayat, ...) -> E2 `record_complaint`
    (suppress + GLOBAL pause). Weak = only "spam" / "scam" / "fraud" / "is this legal" -> label complaint_legal,
    suppressed (E2: complaints always suppress), no global pause. An unmatched sender's complaint is never credible.
    "How did you get my email?" -> flagged, no draft. Benign: "in my spam folder", "no complaints".
13. **Model labels:** through the writer's client and model (`claude-sonnet-5-5`, same request options). The schema
    allows only the six commercial labels + `other`, a language, a summary, and three flags the model can RAISE
    (possible opt-out, possible complaint, asks for a commitment): a raised flag means no draft and the founder
    looks. Anything else in the answer is dropped. Text sent: sanitized subject + new text (max 4,000 characters)
    inside JSON; the system text says it is data. No key or no valid answer -> `needs_review`, no draft.
14. **Drafts:** the phase-13 writer, unchanged: task `{channel: email, touch: null, inbound_message: <sanitized>,
    attachments_allowed: [snapshot URL], reply_labels, sample_page_url}`; lead thread = last 6 messages (our accepted
    mail, their replies), sanitized. On top of the writer's validator, the model's own text (never the app's
    signature) must not offer a discount, name a date / weekday / month / festival / today / tomorrow / kal, a
    duration that is not word-for-word in company facts ("2 working days" and "within 60 days" are), a guarantee
    ("we cannot guarantee" is allowed), a refund or contract terms; a snapshot link must be present when one was
    made. Breaking a rule = BLOCKED draft (kept for audit, never listed for approval). An inbound request for a
    discount, date, guarantee, refund or contract = no draft, flagged. A newer reply supersedes the older draft.
15. **Snapshot:** only for interested / sample_requested, once per sequence (reused until 1 day before it expires).
    Evidence image only when it is a PNG / JPEG of at most 400 KB; `concept_demo` left out for vertical `other`
    (no demo page exists); offer = the Launch row of company facts (price, 5 inclusion lines, delivery line) and the
    first two "Not included" items; no recording. A URL other than `<OUTREACH_PUBLIC_BASE_URL>/s/<slug>` is refused.
    Snapshot failed = no draft, flagged `SNAPSHOT_FAILED` (regenerate later).
16. **Approval** sends at once through E2's builder and SMTP adapter: same mailbox as the sequence; GLOBAL, DOMAIN
    and MAILBOX pauses block (NEW_CONTACTS, SOURCE and SOURCE_BATCH do not: a reply is not a new contact); a fresh
    suppression check for the reply address and the sequence's recipient (website down = 503 + E2 pause, nothing
    sent; suppressed = draft REJECTED). Ceiling: all messages of that mailbox on the recipient-local day, scheduled
    campaign mail included, must be < 30 (E2 caps campaign mail at 25, so 5 always stay for replies). Record kind
    REPLY, key `reply:draft:<id>`. Headers: In-Reply-To = their Message-ID, References = their References + their
    Message-ID (last 10), the E2 List-Unsubscribe headers and body line. Outcomes as in the worker: 2xx SENT; 5xx
    FAILED + E2 refusal rules; 4xx / connection trouble back to WAITING (mailbox pause on connection trouble); a lost
    answer after DATA = UNCERTAIN + E2 `SEND_RESULT_UNKNOWN` (resolve with E2's endpoint; the draft follows).
17. **Backlog rule:** the oldest matched person's message labelled interested / question / price /
    sample_requested / needs_review that is not handled. Handled = an approved answer was SENT (or UNCERTAIN) - it
    covers earlier messages of the same thread - or the founder rejected with `close_thread`, or closed the message.
    E2's rule then pauses / clears NEW_CONTACTS (Mon-Fri business days, India time). Checked by reconcile, approve,
    reject and close.
18. **E2 integrity audit:** duplicates are counted for campaign steps only (replies have step NULL, and SQL's GROUP BY
    put every reply to one person into one "duplicate" group).
19. **Brief:** India-time days; "since the last brief" from the previous brief run (each GET records one); unique
    human replies = distinct senders of matched human messages; `replies_by_label` counts distinct senders per
    label; complaints_received = complaint events; provider complaint rate `"unknown"`; quotes, deposits, payments,
    paid projects `null` with `not_tracked: true`.
20. **Times:** everything stored is UTC; a reply's `Date: ... +0530` is converted (SQLite drops the offset - the
    backlog test found it).
21. **One reconcile at a time:** OS file lock `outreach_reconcile.lock` next to the SQLite file (API answers 409,
    the script exits 2).

## Labelled set (acceptance)
87 written replies (no real people): 27 stops incl. Hinglish / Hindi / Gujarati and odd places, 13 look-alikes that
are not stops (quoted stop line, "don't stop", signature / footer unsubscribe, one-stop, stopped working), 12
complaints, 8 out-of-office (Hindi, Gujarati, header-less), 2 DSNs, 25 commercial incl. discount / date / guarantee
/ refund / contract requests and two prompt injections. Rules result: 0 missed stop, 0 missed complaint_legal, 0
false stop, 0 false complaint; every OOO recognised with the right return date and never answered; the injections
change nothing (same outcome as a plain question, nothing sent, no suppression, no pause).

## Limits
- The commercial labels of the real model were not measured (tests never call it). RESULT row 19: a shadow period
  with real replies is still needed before trusting them; 87 cases is not a safety proof for the model.
- A reply that arrives between the worker's last check and the SMTP submission cannot stop that message (E2's honest
  limit).
- Implicit stops without a stop phrase ("if you mail again I will ...") are caught only when they also match a
  complaint phrase.
- Mailforge IMAP host, port and TLS mode are not on its pricing page; confirm in the Mailforge acceptance test.

## Open questions for the founder
1. Stop confirmation: off by default, one fixed English line (not model-written). Keep, or write it in the owner's
   language with the model?
2. "Not interested right now" is treated as a stop (suppressed for good). Keep, or treat it as not_now?
3. Vertical `other` has no demo page: send the snapshot without `concept_demo` (the website must handle it), or no
   snapshot at all?
4. A weak complaint ("Is this a scam?") is suppressed without a global pause. Keep?
5. At the E3 merge: `/start-day`'s `send batch` should call E3's batch approval once that route exists.
