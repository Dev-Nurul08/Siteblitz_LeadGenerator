# Claude subagent persona panel on the final pilot templates (gate h) - 2026-11-12
Synthetic pre-send filter (one model role-playing six personas); not evidence of real reply, trust or spam rates.
Input: docs/outreach/pilot-templates.md only.

| Persona | T1 SOCIAL_ONLY | T1 NO_VIEWPORT | T1 SITE_DOWN | T2 | T3 |
|---|---|---|---|---|---|
| P1 salon, Surat | NYYN T3 S2 Ignore | NNYN T2 S2 Ignore | NYYN T3 S2 Maybe | NNYY T3 S2 Maybe | NNYY T4 S1 Ignore |
| P2 coaching admin | YYYY T3 S2 Ignore | YYYY T3 S2 Maybe | YYYY T3 S2 Maybe | YYYY T3 S2 Ignore | YNYY T4 S1 Ignore |
| P3 showroom, site down | n/a | n/a | YYYY T3 S2 Reply | YYYY T3 S2 Maybe | YNYY T4 S1 Ignore |
| P5 restaurant info@ | YYYN T2 S3 Ignore | YNYN T2 S3 Ignore | YYYN T3 S3 Maybe | NNYN T2 S4 Ignore | NNYN T2 S3 Ignore |
| P9 son/daughter | YYYY T3 S2 Maybe | YYYY T3 S2 Maybe | YYYY T3 S2 Ignore | YYYY T3 S2 Maybe | YYYY T4 S1 Ignore |
| P10 Gmail, content only | S2 Inbox | S2 Inbox | S2 Inbox | S1 Inbox | S1 Inbox |
(cells: who / why me / offer / next step in 5 s as Y/N, T = trust 1-5, S = spam-likeness 1-5, verdict)

Findings:
- NO_VIEWPORT sentence only partly understood; "phone screen" and "very small" overstate a 390 px emulated render.
  Proposed: "On [date], in our check on a phone-size screen, the homepage at [domain] showed its computer-size layout
  shrunk to fit, so the text was small."
- Changes proposed: NO_VIEWPORT subject "[Business]: homepage not sized for phones"; SITE_DOWN "the last one at
  [HH:MM] on [date]" unless the send step re-checks; T2 opener names the sender ("[Sender] from SiteBlitz again, ...");
  identity "website studio" instead of "web studio" (P1/P5 read "studio" as photo studio); T3 opener "I won't write to
  [Business] about this again." instead of "I'll close this today ..." (can read as an offer ending today).
- Risks: SOCIAL_ONLY sent to an own-domain address implies "no website" while that domain may host one; replies and
  "stop" sent on WhatsApp never reach the IMAP loop, so T2/T3 would still go (most likely real complaint) - a manual
  "replied elsewhere / stop" mark is needed; "charged separately" reads as hidden charges (answer in replies); a home
  postal address is exposed to strangers (PO box / virtual office safer).
