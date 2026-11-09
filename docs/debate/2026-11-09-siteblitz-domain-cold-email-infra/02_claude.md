# Round 2 - Claude Code's verdicts on your round-1 answer (checked 2026-11-09)

## Verdicts per point

1. Domain - AGREED: `siteblitz.in`, conditional on an IP India public trademark search (classes 35 + 42) first.
   The search is free and takes minutes, so the order is: search today -> buy `siteblitz.in` (Rs 899 + GST).
2. Spam causes - AGREED with your ranking and your qualification: fabricated recipients are the top SUSPECTED
   cause; we do not yet know which list the team actually sent. Added: Google's own help page
   (support.google.com/mail/answer/22839) gives consumer Gmail "more than 500 emails sent in a day" as the cap.
3. Inbox math - AGREED that 30 inboxes / 10 domains is not to be bought now (my draft already gated it on
   22k verified addresses/month). REJECTED: "evaluate a suitable bulk-email provider instead of multiplying
   mailboxes". Bulk ESPs forbid exactly this traffic: SendGrid lists "email lists of recipients that have not
   affirmatively consented" as prohibited (support.sendgrid.com article 4404316003483); Brevo never allows
   purchased, rented or scraped lists (brevo.com/legal/antispampolicy). Cold first-touch to scraped business
   addresses is not "permission-based", so an ESP is not an option for that traffic.
4. Provider - AGREED: Google Workspace Base, 1 user now. Note on your $100/75-day point: Google's page applies
   that threshold to trial accounts converting to paid (trial = 500 unique external recipients/day). It does
   not affect a 33/day per-inbox plan.
5. Roles - AGREED: the paid user is `hello@siteblitz.in` ("SiteBlitz Team"), aliases projects@, support@,
   billing@; a second paid seat only when the friend needs his own login. No invented people.
6. Costs - corrections ACCEPTED: Instantly Hypergrowth is now USD 107/month monthly (85.58 annual), 125,000
   emails, 25,000 uploaded contacts (instantly.ai/pricing, checked today); Growth (5,000 emails, 1,000
   contacts) cannot carry live sending; MillionVerifier 50k = USD 89 and 1M = USD 449 (vendor homepage) -
   I will budget the 10k pack at USD 39. Hosting is a real missing line: Vercel Hobby is non-commercial; Pro is
   USD 20/seat/month (third-party pages, not checked on vercel.com).
   REJECTED: "the Rs 13,400 saving is not supported". The draft said the stack COSTS ~Rs 13,400/month
   without Instantly (22,542 - 9,167 = 13,375), not that it saves 13,400.
7. Gates - AGREED with staging. Your extra finding is CONFIRMED: the live `siteblitz.vercel.app` today still
   shows Rs 14,999 and Rs 24,999 and `hello@siteblitz.in` six times - the production deploy is the old version
   while the repo's `offer.ts` says Rs 7,999 / Rs 17,999 and hides the bouncing address.

## What I still need from you (answer by letter, short)

A. Exact go/no-go numbers. Give one number each, with its source or "judgement":
   - minimum verified-email yield among discovered businesses before buying any cold inbox;
   - maximum hard-bounce rate and spam-complaint rate in the pilot;
   - minimum positive-reply rate and paid orders from the pilot that justify scaling;
   - pilot size (sends) needed before those rates mean anything.
B. If every gate passes and the founder still wants 1,000 first-touch emails/day to Indian businesses: given
   that bulk ESPs are out for non-consented traffic, is a fleet of Workspace inboxes on separate domains the
   only workable route, or would you cap the volume lower? Give your number of inboxes, domains and per-inbox
   sends, and the corrected month-1 and monthly cost in INR using: .com Rs 1,116 each, Workspace Starter
   Rs 270 + 18% GST, Hypergrowth USD 107, MillionVerifier USD 89 per 50k, Rs 94.5/USD.
C. A smaller pilot stack between "1 mailbox" and "30 inboxes" (e.g. 2 domains x 2-3 inboxes) - would you run
   the 200-business pilot from such a stack or from `hello@siteblitz.in` itself? One sentence why.

End with the points still open (if none, say "none").
