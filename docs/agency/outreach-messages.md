# Outreach and reply messages for agencies (2026-11-12)

Writing rules (from `docs/outreach/` and RESULT B): one true, checkable observation first; plain words; no "I hope
this email finds you well", "I came across", "elevate", "seamless", "unlock", "vibrant", "testament"; no em dashes;
no compliments you cannot prove; honest identity "based in Gujarat"; no clients, reviews or results (there are none).
A person sends every message by hand. No cold WhatsApp, no cold calls or SMS (TRAI), no automated LinkedIn.

Placeholders the founders fill once: `[Sender name]`, `[Reply address]`, `[Postal address]`.
The per-agency drafts for the first 50 are in
`E:\SiteBlitz-World-Business-Data\_work\agency_list\2026-11-12\drafts_50.md` (outside the repo: business emails).

## Which route for which agency (pick the first that applies)
1. **The agency's own contact form or "partner / work with us / vendor" page** - paste the contact-form message.
   They invite messages there.
2. **A published address on their site that invites business or partnership enquiries** - send the first email.
3. **The owner's LinkedIn profile** - send the connection note by hand.

Risk, stated once: Google's Gmail and Workspace policies prohibit unsolicited commercial email and give no
low-volume exemption (RESULT row 9). Keep it one-to-one, relevant, honest, with an opt-out, and stop at the first
"no". If an agency asks you to stop, mark it `SUPPRESSED` and never contact it again on any channel.

## 1. First email (India) - Day 1
Subject: White-label website development for [Agency name]

> Hi [Agency name] team,
>
> [One true observation from their own site, e.g. "Your site lists social media and ad campaigns for restaurants in Surat."]
>
> We are SiteBlitz, two developers based in Gujarat. We build websites for agencies under the agency's name: you keep the client, the approved design and the content; we build, test and hand over.
>
> A landing page is ₹8,000–₹10,000 and a three-page site ₹16,000–₹22,000, depending on the agreed scope. Details and two labelled demo sites: https://siteblitz.vercel.app/agencies
>
> Do you have a landing page or small website coming up that we could quote by email? No call needed.
>
> [Sender name] | SiteBlitz
> [Reply address] | [Postal address]
> If this is not relevant, reply "no thanks" and we will not write again.

## 2. Follow-up 1 - about 5 business days later, same thread
> Hi [Agency name] team,
>
> A short follow-up on white-label builds. If a client of yours needs a landing page, you can send the brief here and we will reply with a written scope and a fixed quote within one business day: https://siteblitz.vercel.app/agencies#brief
>
> [Sender name] | SiteBlitz
> [Reply address] | [Postal address]
> Reply "no thanks" and we will not write again.

## 3. Follow-up 2 - about 12 business days after the first email, same thread, then stop
> Hi [Agency name] team,
>
> I'll close this after today. If you need extra development capacity later, you're welcome to write to us and we'll quote by email.
>
> Thank you for your time.
>
> [Sender name] | SiteBlitz
> [Reply address] | [Postal address]
> No further follow-ups are planned.

No reply 5 business days after follow-up 2 -> `CLOSED_NO_REPLY`. No new campaign to the same agency.

## 4. Contact-form message (paste into the agency's own form; most forms cut long text)
> Hello, we are SiteBlitz, two developers based in Gujarat. We build websites for agencies under the agency's name: you keep the client, design and content; we build, test and hand over. Landing page ₹8,000–₹10,000, three-page site ₹16,000–₹22,000. Details and labelled demos: https://siteblitz.vercel.app/agencies. If you have a brief coming up, we can quote by email, no call needed. [Sender name], [Reply address]

## 5. LinkedIn connection note (300 characters at most; send by hand)
> Hi [First name], I'm [Sender name], one of two developers at SiteBlitz (Gujarat). We build landing pages and small sites for agencies under the agency's name. If [Agency name] ever needs extra build capacity, I'd be glad to quote by email.

Free accounts may not allow a note on every invitation. If the note option is missing, send the invitation without
a note and, only after they accept, send the note as a message. No automation tools.

## 6. First email - US agencies (from week 3, 26 Nov; only after the readiness gate in RESULT row 11)
US law (CAN-SPAM) requires an honest sender and subject, a valid postal address and a working opt-out; it applies to
one-to-one B2B email too. Price: no number in the first email; written quote in USD that already includes the
collection cost (`payments-and-tax.md`).

Subject: White-label development for [Agency name]

> Hi [First name or Agency name team],
>
> [One true observation from their own site.]
>
> We're SiteBlitz, two developers based in Gujarat, India. We build landing pages and small websites for agencies under the agency's name. You keep the client, the approved design and the content; we build in Next.js, test on phone and desktop, and hand over.
>
> Details and two labelled demo sites: https://siteblitz.vercel.app/agencies
>
> If you have a landing page coming up, could we quote it by email? We reply within one business day, India time.
>
> [Sender name] | SiteBlitz
> [Reply address] | [Postal address]
> This is a one-time business email. Reply "unsubscribe" and we won't write again.

## 7. Replies (a person sends them; paste the agency's message into a Claude Code session to adapt)
| They say | Status | Answer |
|---|---|---|
| Interested / tell me more | `QUALIFYING` | "Thank you. The quickest way is the brief form: https://siteblitz.vercel.app/agencies#brief - or reply with the page type, design status, content status, stack and deadline, and we'll send a written scope and fixed quote within one business day." |
| Price? | `QUALIFYING` | "Landing page ₹8,000–₹10,000 and three-page site ₹16,000–₹22,000, depending on the agreed sections. Domain and hosting are separate. Send the design or a reference and we'll fix the exact price in writing." |
| Send portfolio / past clients | `QUALIFYING` | "We're new as an agency partner, so we have no client work we can show. These two concept demos show how we build, clearly labelled as demos: [links]. If it helps, start with one landing page; you pay 50 % only when we start and the balance after you approve staging." |
| We have our own developers | `CLOSED` (or note for overflow) | "Understood. If they're ever fully booked, you're welcome to send us an overflow brief. Thank you." |
| Can you do WordPress / Shopify / Webflow? | `QUALIFYING` | Only say yes if the founders have built that before and can show it. Otherwise: "We build in Next.js and React. For WordPress we'd rather be honest: [yes, we have built X / it isn't our strength today]." |
| Pay when my client pays | `QUALIFYING` | "We work with a 50 % advance before we start and the balance after you approve staging, before handover. That keeps the dates firm for your client." |
| Can you talk to my client directly? | `QUALIFYING` | "We work through you. If you want us on a technical call, we join only with your written approval and under your agency's name." |
| Not now | `CLOSED` | "Understood. Is there a month when we may write again, or shall I close this?" (re-contact only if they name a month) |
| No / stop / unsubscribe | `SUPPRESSED` | "Understood, thank you for letting us know." Never contact again on any channel. |
| Out of office | `PAUSED_OOO` | Resume 2 business days after their return date. |
| Hard bounce | `SUPPRESSED` (address) | Try the contact form or LinkedIn route once; never guess another address. |
| Sends a brief | `BRIEF_RECEIVED` | Check it against `brief-form.md`, then send the quote (`quote-template.md`) within one business day. |
