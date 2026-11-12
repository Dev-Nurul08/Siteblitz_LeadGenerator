# Synthetic persona panel (Claude Code subagent, not anchored on claude-position.md) - 2026-11-12

A synthetic role-play panel: a pre-send filter, not evidence of how real recipients behave.
Input: the three sample emails (A plain, B "in short" first, C touch-2 snapshot + voice link) and personas P1-P10.

## 1. Panel
| Persona | Inbox view | First 3 s | Delete / spam trigger | Reply trigger | A / B / C | Why |
|---|---|---|---|---|---|---|
| P1 Salon, Surat | Gmail app between clients | "website guy, selling" | English block; "idea" = pitch | seeing her own page; a WhatsApp number to tap | Ignore / Maybe / Maybe | only her own page earns a tap |
| P2 Coaching admin | office desktop | "vendor, not a parent" | "website idea" when they have a site | a problem to forward | Ignore / Maybe / Maybe | admins forward problems, not offers |
| P3 Showroom, site down | phone, rarely opens mail | "is my site down?" | looks like a domain-renewal scam | exact URL, date, what it showed | Ignore / Reply / Maybe | best observation; A hides it; C's link smells of phishing |
| P4 US dental manager | Outlook, daily marketing pitches | "offshore agency" | India, ₹, unknown sender | none | Spam / Spam / Spam | same shape as daily vendor spam |
| P5 Restaurant info@ | shared desktop, staff | "not a booking or supplier" | any offer, any link | "website isn't opening" gets forwarded | Ignore / Maybe / Ignore | staff pass on problems, not pitches |
| P6 UK/AU trades | phone at 10 pm | "marketing" | "team" for a one-man firm; overseas | none | Spam / Spam / Spam | UK sole traders need prior consent (PECR) |
| P7 Decent website | any | "that's wrong" | a false claim | none | Spam / Spam / Spam | should never receive it |
| P8 Agency owner | desktop | "competitor pitching me" | being sold his own product | a white-label offer | Ignore x3 | wrong offer - use the agency kit |
| P9 Assistant / family | phone / desktop | "bother the owner?" | a plain offer | one line to repeat to the owner | Ignore / Maybe / Ignore | won't click links for someone else |
| P10 Gmail filter | n/a | content check | C: link to a new or shared domain | replies; complaints weigh more than wording | Pass / Pass / Risk | at 10-20/day engagement decides |

## 2. Winner
B's structure (the problem in the preview) after fixes; India SMB: B as touch 1, C as touch 2; the site-down variant
is the strongest. Abroad SMB: none - expect Ignore/Spam; keep HOLD. Agencies: filter out, use the white-label kit.
Assistant-read inbox: B.

## 3. Five changes (before -> after)
1. Subject: "A website idea for ..." / "clients can't find your prices online" -> "Glow Studio: Instagram only, no website" (site down: "[domain] isn't opening"). State only what was checked; prices were never checked.
2. First line: greeting first -> "I looked for Glow Studio online on [check date] and found your Instagram, but no website." Body 55-65 words. Move the India greeting after the fact or drop it.
3. Price: not in line 1 (reads as an ad) -> just before the question: "A one-page site with your services, timings, and WhatsApp and call buttons costs ₹7,999 (domain and hosting separate)." Keep the price in India touch 1; no price abroad.
4. Call to action: "send a short outline?" -> "Shall I make a sample page for Glow Studio and send it here or on WhatsApp (+91 92744 90242)?"
5. Sender and opt-out: From "Ravi, SiteBlitz" (the founder's real name); sign-off with "web studio in Gujarat" + WhatsApp + postal line; short opt-out; a List-Unsubscribe header so leaving is a button, not "Report spam".

Spec conflicts found in the samples: B contains ";" (validator rejects it), promises "a booking button" (bookings are
excluded from ₹7,999) and implies search visibility (rankings excluded). C offers "the price" again (use "the steps and
a start date") and the voice must be the founder's own recording (synthetic voice is out of scope). Site-down leads:
an address on a lapsed domain bounces - send only to an address that still works.

## 4. Personalised page and voice
Helps in touch 2 for P1 and P2 (and P3 only if it shows the dated error). Hurts for P4, P5, P6, P8, P9. Host it on the
sending domain, business name in the path; no shortener, no click-tracking redirect, not a shared subdomain like
vercel.app. Never in touch 1. Voice: the only trust signal (no clients) - optional, after the visual; most will not
press play. Audio attached to touch 1 hurts with every persona (filter scrutiny, malware look, mobile data).

## 5. "Worth reading in 5 seconds"
P1 her salon's name + a picture of her own page + WhatsApp · P2 "your fees page on a phone" + one screenshot · P3 URL,
date, what it showed, "check with whoever registered it" · P4/P6 nothing cold - do not send · P5 "your website isn't
opening" in the subject · P7 nothing - send only with a verified observation · P8 white-label price per page, days,
his brand only · P9 a one-line problem in the subject · P10 plain text, no link in touch 1, steady low volume, replies.
