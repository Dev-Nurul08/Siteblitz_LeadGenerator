# PILOT_EMAIL_TEMPLATES - email engine v2, India controlled pilot (phase E3)

Status: built in phase E3 (founder `go for all`, 2026-11-12). Sources: `docs/spec/email-engine-v2.md` rows 4-6,
`docs/debate/2026-11-12-email-engine-personas/RESULT.md` rows 13 and 16 and section C (reference touch-1 texts),
`company-facts.md` (price, demo table, WhatsApp). The observation sentences are the ones E1 stores
(`backend/app/engines/eligibility/rules.py`: `social_only_text`, `site_down_text`, `no_viewport_text`), copied word
for word by the writer; nothing here re-words them.

How it is used:
- The AI writer still writes every message. The block below is attached to every writer request as
  PILOT_EMAIL_TEMPLATES, next to the system prompt, COMPANY_FACTS, COUNTRY_LANGUAGE and REFERENCE_MESSAGES.
- The batch screen (`POST /api/v1/outreach/batches`) sends one TASK per touch with a `pilot` object (below). For a
  pilot task these rules replace STEP 5 "email, touch 1/2/3" of the system prompt and the email examples in
  `reference-messages.md`. Every other rule stays (language, banned phrases, punctuation, facts, honesty).
- The validator (`backend/app/engines/writer/validator.py`, `pilot_email_errors` and `assembled_pilot_errors`)
  re-checks every rule listed at the end of this file. A failure gets one rewrite, then HOLD `VALIDATION_FAILED`.
- The app, not the model, adds the signature block and the unsubscribe line. The unsubscribe URL is made by E2's
  message builder at send time (`backend/app/engines/sending/message.py`); until then the stored text carries the
  placeholder `[unsubscribe link added when sent]`, which the builder always replaces.

---

```text
PILOT EMAIL TEMPLATES (India controlled pilot). They apply when TASK.pilot is set. For that task they replace
STEP 5 "email, touch 1/2/3" and the email examples in REFERENCE_MESSAGES. Every other rule above still applies.

TASK.pilot carries:
  "template": "T1" | "T2" | "T3"
  "observation_type": SOCIAL_ONLY | SITE_DOWN | NO_VIEWPORT
  "observation_sentence": the dated observation, checked and written by the app. Copy it word for word.
  "identity_line": "I'm <sender> from SiteBlitz, a small web studio in Gujarat."
  "price_line": "Website setup starts at ₹7,999, with domain and hosting charged separately."
  "question": "Shall I make a sample page for <Business> and send it here?"
  "vertical": salon_beauty | coaching_tuition | retail_showroom | other
  "vertical_page": what a page shows for this vertical (COMPANY_FACTS demo table), and "customer_word".
For T2 and T3, LEAD.thread holds the touches already written for this business, oldest first.

A pilot email has no greeting, no sign-off and no opt-out line of its own: set "signoff" and "opt_out_line" to
null. The app adds this block under every pilot email:
  <sender> | SiteBlitz
  <reply address> | <postal address>
  WhatsApp: <studio WhatsApp>

  Reply "stop" or unsubscribe here: <unsubscribe link>
There is no other link in a pilot email: no demo link, no website link, no shortener.

T1 (Day 1). "body" has 60-85 words.
  subject: "<Business>: " followed by a neutral fact the owner can check in ten seconds, 3-8 words, plain, no "?"
  or "!", no "Re:" or "Fwd:". Business name exactly as in LEAD.
  body, in this order, paragraphs separated by one blank line:
    1. observation_sentence, word for word. It is line 1; nothing comes before it.
    2. identity_line, word for word, then one sentence on what we build for this vertical, made from
       vertical_page in plain words. For SITE_DOWN start that sentence with "If you need a replacement, ". For
       NO_VIEWPORT say "mobile-friendly pages".
    3. price_line, word for word.
    4. question, word for word. It is the only question and the last sentence.
  Nothing else: no second offer, no other price, no claim about results.

T2 (Day 6, same thread; the app sends it as "Re: <touch 1 subject>"). "body" has 40-70 words.
  Start with identity_line, word for word (T2 is often read without touch 1). Text only. Offer the sample page again and add one new, useful piece of information that touch 1 did not give:
  what the sample page would show for this vertical (vertical_page), and the WhatsApp and call buttons that the
  Launch package includes. Do not say "just following up", "checking in", "circling back", "bumping" or refer to
  "my last email". Exactly one question, at the end, offering to make and send the sample page.

T3 (Day 14, same thread). "body" has 30-50 words.
  A polite close: you will close this and not write again, they can reply here any time for the sample page and
  the prices, thank them for their time, and a last line meaning "No further follow-ups are planned." No pressure,
  no deadline, no discount, no question needed.

Reference texts. Words in [brackets] are filled from LEAD and TASK. Match the shape, do not copy the vertical
sentence word for word for another vertical.

T1, SOCIAL_ONLY, salon_beauty (body 64 words with a one-word name and a date such as "12 November 2026")
Subject: [Business]: no website link in Instagram bio
On [date], the Instagram profile for [Business] showed no website link when we checked its bio.

I'm [Sender] from SiteBlitz, a small web studio in Gujarat. We build simple pages showing salon services, prices, opening hours and appointment enquiries.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

T1, NO_VIEWPORT, coaching_tuition (body 63 words, same counting)
Subject: [Business]: small homepage text in our check
On [date], the homepage at [domain] showed small text when we checked it at a phone-screen size.

I'm [Sender] from SiteBlitz, a small web studio in Gujarat. We build mobile-friendly pages showing courses, timings and enquiry details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

T1, SITE_DOWN, retail_showroom (body 74 words, same counting)
Subject: [Business]: [domain] did not load in our checks
On [date], the homepage at [domain] did not load in our checks, the last one shortly before this email. The interruption may be temporary.

I'm [Sender] from SiteBlitz, a small web studio in Gujarat. If you need a replacement, we build pages showing your showroom, products and enquiry details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

T1, SOCIAL_ONLY, other (body 62 words, same counting)
Subject: [Business]: no website link in Instagram bio
On [date], the Instagram profile for [Business] showed no website link when we checked its bio.

I'm [Sender] from SiteBlitz, a small web studio in Gujarat. We build simple pages showing your services, location and contact details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

T2, salon_beauty (46 words)
I'm [Sender] from SiteBlitz, a small web studio in Gujarat. The sample page for [Business] would show your salon services, prices, opening hours and an appointment request. It would include WhatsApp and call buttons. Shall I make a sample page for [Business] and send it here?

T3, any vertical (39 words)
I'll close this today so I don't keep writing. If a website becomes useful for [Business] later, just reply here and I'll send the sample page and the prices. Thank you for your time. No further follow-ups are planned.
```

---

## What the validator re-checks for a pilot email (on top of the phase-13 checks)
Phase-13 checks that stay: decision / hold reasons, country + declared language + `langdetect`, banned phrases,
"AI", em dash / en dash / `!` / `;`, unresolved `[..]` / `{{..}}` / `TO FILL`, the facts guard (every number and
domain must be in COMPANY_FACTS, LEAD or TASK), the observation type, and MISSING_COMPANY_FACT before any call.

| Rule | T1 | T2 | T3 |
|---|---|---|---|
| Body words | 60-85 | 40-70 | 30-50 |
| Link in the model's text (subject, body) | none | none | none |
| `signoff` / `opt_out_line` | null | null | null |
| Line 1 = the E1 observation sentence, word for word | yes | - | - |
| Identity line right after it, word for word | yes | - | - |
| A sentence on what we build for the vertical between identity and price | yes | - | - |
| Exact price line just before the question (India) | yes | - | - |
| Exactly one `?`, the question is the last sentence, word for word | yes | one `?`, last | - |
| Subject `<Business>: <fact>`, fact 3-8 words, no `?` / `!` / `Re:` | yes | (kept by the app) | (kept by the app) |
| Mentions the sample page | - | yes | - |
| Starts with the identity line, word for word (pre-send review 2026-11-12) | - | yes | - |
| No "following up" / "checking in" / "circling back" / "bumping" / "my last email" | - | yes | yes |
| No pressure words (limited, last chance, hurry, urgent, only this week, act now, offer ends, deadline, discount, don't miss) | yes | yes | yes |

The 100-words-with-signature cap of the outreach spec (row 5) is not applied to pilot emails: spec v2 row 5 fixes
the body at 60-85 words and adds two signature lines (WhatsApp, unsubscribe), so the cap would depend on the length
of the postal address. Decision recorded in `docs/outreach/e3-notes.md`.

On the assembled text the app stores for sending (`assembled_pilot_errors`): the signature block is present
(`<sender> | SiteBlitz`, `<reply> | <postal>`, `WhatsApp: ...`), the last line is
`Reply "stop" or unsubscribe here: <URL or the placeholder>` exactly once, and there is no other URL anywhere.
