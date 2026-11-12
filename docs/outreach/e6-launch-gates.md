# E6 launch gates - status log (spec `docs/spec/email-engine-v2.md` row 17) - 2026-11-12

Rule: the first real email goes out only when every row below says PASS. Claude Code filled in what can be proven
without the founders' accounts; the rest waits for the steps in `docs/outreach/email-engine-setup.md`.

| Gate | What it needs | Status | Evidence |
|---|---|---|---|
| (a) truthful website live | production shows no invented reviews/results, Gujarat only, working contact route | **PASS** (2026-11-12) | deployed by the website session (website commit fa3cd13, build aa116dc); Claude re-checked the live home page: 0 hits for the invented names/results, "Studio Mumbai", Rs 14,999 / 24,999 and the bouncing address; "Gujarat" 41 times. Outreach routes live but 503 until O2's two secrets are set |
| (b) sender facts | real sender name(s), reply address, postal address in `.env` | **WAITING (founder)** | the writer returns HOLD `MISSING_COMPANY_FACT` until set (E3 tests) |
| (c) domains + Mailforge + seed tests | SPF / DKIM / DMARC pass and both unsubscribe headers DKIM-covered on raw messages received by Gmail, Outlook, Yahoo | **WAITING (founder)** | headers are built and checked on raw messages from a local SMTP test server (E2 `test_worker.py`); DKIM is applied by Mailforge, so only a real seed test can prove coverage |
| (d) unsubscribe end to end incl. laptop off | click / one-click POST suppresses; a queued message to that address never leaves | **PARTLY PASS** - code and local tests; live test waits for (a) + (c) | website: 68 outreach route tests incl. GET never suppresses, one-click idempotent, DB down = 503 (Claude re-ran them); lead generator: fresh check before every submission, website down = no send + pause (E2 race tests); token byte-for-byte equal in Node and Python (known-answer vector) |
| (e) failure tests | opt-out between approval and send, reply before follow-up, duplicate / out-of-order events, timeout after acceptance, restart, missing timezone, stale evidence, unknown country, model down, blank facts, auto-reply loop, prompt injection | **PASS (automated)** | E2 `test_races.py`, `test_worker.py`, `test_pause_rules.py`; E3 `WRITER_UNAVAILABLE` / `MISSING_COMPANY_FACT`; E4 87-reply labelled set (0 missed stop, 0 missed complaint, OOO never answered, 2 injections change nothing); full suite 795+ passed on the merged branch |
| (f) provenance audit of the first leads | every selected lead has source URL + capture date + excerpt, reproducible | **PASS for the 26 available** (gate asked 30; only 26 exist) | 26/26 have source URL, excerpt, capture date and the phone screenshot file; live re-fetch 2026-11-12: 25/26 pages still show the address (3 Cloudflare-encoded, decoded), 1 site did not answer today - it is re-checked before any send (`E:\tmp\_strategy\provenance_audit.py`) |
| (g) 10 consenting business readers, >= 8 / 10 understand sender, reason, offer, next step in 5 s | **WAITING (founder)** | the synthetic reviews say P1 (slow English) and P5 (shared inbox) are the weak readers - include them |
| (h) synthetic persona review of every template | ChatGPT + Claude | **PASS** | `docs/debate/2026-11-12-pilot-template-review/RESULT.md`; 3 template changes applied (commit 80977be), 2 more fixes from it (039fccc, 64a6d4d) |
| (i) founder reads the first 20 written emails | outreach spec row 6 | **WAITING (founder)** | the batch screen shows the full three texts per lead before "Approve" |

Also before the ramp leaves stage 0: verify the 26 addresses (`{"verify": true}`, about $0.21); Bouncer key needed.
