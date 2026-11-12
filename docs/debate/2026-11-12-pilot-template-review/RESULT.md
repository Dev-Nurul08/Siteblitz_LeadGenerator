# Review - pre-send persona review of the final pilot templates (launch gate h) - 2026-11-12 - 1 round - prompt: lead-intelligence-vision-partner

Inputs: topic.md + docs/outreach/pilot-templates.md (9.6 KB, nothing truncated) to ChatGPT; the same file to an
independent Claude subagent panel (persona-panel-claude.md). Both are synthetic pre-send filters, not evidence of real
reply, trust or spam rates; the real 10-reader test (gate g) is still the founders' step.
Stop reason: one round was the gate; ChatGPT and the panel agreed on the changes below, and every other point maps to
code that already exists or to a founder step.

| # | Point | Proposed by | Evidence | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | NO_VIEWPORT sentence is hard for slow English readers and overstates the check ("zoomed-out", "phone screen", "very") -> "On [date], the homepage at [domain] showed small text when we checked it at a phone-screen size." | ChatGPT + panel | the check is a 390 px Chromium render that falls back to a desktop layout (E1 `render_check.cjs`) | agreed, "very" dropped (not measured) | done - `rules.py` `no_viewport_text`, 26 stored leads re-evaluated (26/26 carry the new text) |
| 2 | NO_VIEWPORT subject states the observed fact: "[Business]: small homepage text in our check" (panel's "not sized for phones" claims more than was checked) | ChatGPT | subject rule: a neutral fact checkable in ten seconds, 3-8 words | agreed | done - pilot-templates.md, test fakes |
| 3 | T2 starts with the identity line (often read without T1); WhatsApp and call buttons stay the new information | ChatGPT + panel | - | agreed | done - writer instruction + validator rule "touch 2 must start with the identity line" |
| 4 | Replies on WhatsApp / phone never reach the IMAP loop, so T2/T3 would still go | panel | E4 reads email only | agreed | done - `POST /outreach/sequences/{id}/replied-elsewhere` (+ stop = website suppression first), `GET /outreach/sequences?business=`, `/start-day` answers `replied` / `stop` (commit 039fccc) |
| 5 | SOCIAL_ONLY sent to an own-domain address implies "no website" while that domain may host one | panel | - | agreed | done - hold `SOCIAL_ONLY_DOMAIN_ADDRESS` (commit 64a6d4d) |
| 6 | SITE_DOWN "shortly before this email" must be true at dispatch, not at drafting (ChatGPT: within 15 min) | ChatGPT + panel | E2 worker calls E1 `recheck_before_send` right before each SMTP submission | already built | closed |
| 7 | No re-enrolment after T3 | ChatGPT | `sending_service._already_contacted` refuses "ALREADY_IN_SEQUENCE" | already built | closed |
| 8 | Domain in the observation vs "no URL": a bare domain may be auto-linked by mail apps | ChatGPT | E1's observation sentence carries the business's own domain as plain text and the validator passes it (pilot tests with NO_VIEWPORT texts pass); no authored link exists | decision: the recipient's own domain stays as plain text (it is their site, not a promotional link) | closed (decision) |
| 9 | Total messages per sending day, not only new contacts, must be capped | ChatGPT | E2 caps 30 per mailbox per day incl. everything, 25 campaign, follow-ups reserved before admission | already built | closed |
| 10 | "web studio" may read as "photo studio" to P1/P5 | panel | identity is a company fact ("a small web studio based in Gujarat") | not changed - founder may decide | open (founder) |
| 11 | T3 opener "I'll close this today" could read as a deadline | panel | ChatGPT: keep T3 unchanged, its job is a respectful close | not changed | closed |
| 12 | Price line "charged separately" may read as hidden charges; postal address at home is exposed | panel | - | answer charges in replies; founder chooses a PO box / office address | open (founder) |
| 13 | ₹7,999 package and sample-page terms must exist and be deliverable before sending | ChatGPT | `company-facts.md` / `offer.ts` Launch package | founder confirms the sample-page scope (spec row 20) | open (founder) |

Synthetic panel scores (both): P2 coaching admin, P3 showroom with a down site and P9 family inbox manager understand
T1 in 5 seconds; P1 slow-English salon owner and P5 shared-inbox staff mostly do not; Gmail placement cannot be
predicted from copy (needs real seed tests).
