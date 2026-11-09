# Verified facts and Claude Code's draft plan (2026-11-09)

## The business
- SiteBlitz sells one-time-fee websites to small local businesses in India (Gujarat-based, serving India).
  Prices: Launch Rs 7,999 (1 page, 2 working days), Business Rs 17,999 (3 pages, 7 working days), Custom quoted.
  No GST registration yet. Founder plus one friend build sites. Founder's name and photo never appear publicly.
- Site: Next.js on Vercel Hobby (non-commercial terms - host undecided), live only at `siteblitz.vercel.app`.
  No custom domain bought yet. Site email `hello@siteblitz.in` is hidden (`emailLive=false`) because it bounces.
- Earlier founder decisions (2026-11-01): buy the domain only, no paid mailbox, no other paid tools; WhatsApp is
  the primary channel; Rs 1,000 total ad budget for November 2026; cold email on hold "pending the domain and a
  legal review"; warm introductions first. The founder is now asking for a 1,000 emails/day plan instead.
- Lead generator (this repo): finds businesses that need a website, worldwide data (86.75 M Overture places),
  used in practice for Indian cities. Target pilot in docs/PHASES.md: one Indian city, dentists and salons,
  200 businesses.

## Code evidence (this repo)
- `backend/app/engines/enrichment/discovery.py:131-139` fabricates contacts when none are found:
  `contact_email = f"inquiry.{slug}@gmail.com"` and phone `+91 9825` + hash.
- `surat_restaurant_leads_with_contacts.csv`: 38 rows, 38 emails, 37 are `inquiry.*@gmail.com` (fabricated);
  only `hello@annaskitchen.in` looks real. 36 of 38 phones are fabricated too.
- Real email sources: Overture Places `emails` field, emails crawled from a business's own website, Hunter.io
  if a key is set (not set).
- Sending: `backend/app/engines/conversion/sender.py` is a scaffold - round-robin over fictional
  `@siteblitz.agency` mailboxes, marks messages SENT without any network call (always `simulate=True`).
  Default `daily_send_limit` 50, 60-300 s jitter, Mon-Fri 9-17 UTC, no warm-up, unsubscribe link points to
  localhost, footer uses a fake New York postal address. Phase 5 (real sending) is not started.
  docs/DECISIONS.md: WhatsApp is never automated; sending stays off until a real provider confirms delivery.
- No India / TRAI / DPDP rules in `country_rules.py` (only US, UK, EU, Canada, Australia).
- How the team sends today ("multiple normal Gmails") is NOT in any doc - it comes only from the founder's
  message. We do not know which list they used.

## Domain checks (registry RDAP / WHOIS, 2026-11-09 ~06:30 UTC)
- AVAILABLE: siteblitz.in ("Domain siteblitz.in is available for registration" - NIXI RDAP), siteblitz.co.in,
  siteblitz.net.in, siteblitz.co (whois.registry.co: DOMAIN NOT FOUND), siteblitz.io (whois.nic.io: not found),
  siteblitz.app, siteblitz.dev, siteblitz.studio, siteblitz.agency, siteblitz.site, siteblitz.tech,
  siteblitz.xyz, siteblitz.digital, siteblitz.biz, siteblitz.pro, siteblitz.store,
  siteblitzhq.com, joinsiteblitz.com, siteblitzstudio.com, siteblitzweb.com (Verisign RDAP 404).
- TAKEN: siteblitz.com (GoDaddy, since 2001-09-11, own nameservers, no website answers),
  siteblitz.net and siteblitz.org (since 2001, GoDaddy, Rackspace DNS), siteblitz.online (2026-04-07),
  siteblitz.ai (OVH, 2026-06-16, Vercel DNS) - a live French site titled
  "SiteBlitz - Le site web tout-en-un, specialise par metier" (all-in-one websites per profession),
  getsiteblitz.com and trysiteblitz.com (both 2026-06-16, Cloudflare, 301-redirect to siteblitz.ai).
- .in rules: NIXI e-KYC mandatory within 7 days of registration (registrar bulletins; start date given as
  27 Jan 2026 or 31 Mar 2026), privacy/proxy banned, SERVERHOLD if not verified. Public WHOIS output is
  redacted ("The WHOIS information provided in this page has been redacted").
- Prices: Hostinger India list price .in Rs 899/yr (renewal Rs 899), .co.in Rs 799 (Rs 469 first year),
  .com Rs 1,499 (renewal Rs 1,499); GST not stated on page. Porkbun API (USD): .com 11.81, .in 7.83,
  .co.in 5.80, .co 15.76 then 31.20 renewal, .io 28.12 then 51.80.
- FX used: Rs 94.5 per USD (PTI close 94.46 on 2026-11-05).

## Email facts
- Google Workspace India page (workspace.google.com/intl/en_in/pricing.html): Base Rs 99/user/month
  (custom-domain Gmail, 20 GB, max 20 users; intro 50% off from 22 Nov 2026), Starter Rs 270 (30 GB,
  up to 300 users, Gemini), Standard Rs 1,080. Prices under "Annual (save 16% with one-year commitment)",
  excluding tax.
- Workspace limits (Google doc): 2,000 messages/user/day, 2,000 external unique recipients/day, trial 500.
  Up to 30 aliases per user at no extra cost.
- Google sender FAQ: keep spam rate under 0.1%, never reach 0.3%; bulk senders need a DMARC record.
  Bulk-sender threshold of 5,000/day to Gmail comes from third-party explainers.
- Workspace Acceptable Use Policy bans generating or distributing "large volumes of unwanted emails" and
  promotional content.
- Free Gmail: ~500 recipients/day (third-party sources only, not confirmed on Google's page).
- Per-inbox cold volume (vendor blogs, not independent): 10-20/day new, 30-50/day warmed after weeks;
  1,000/day needs ~20-34 inboxes; keep a domain under ~500/day.
- Instantly (third-party pages): Growth USD 47/month (1,000 uploaded contacts cap), Hypergrowth USD 97/month
  or 77.60 annual (25,000 uploaded contacts, 100k-125k emails/month); unlimited accounts + warm-up on all plans.
- MillionVerifier: USD 37 per 10k credits, USD 89 per 50k (third-party pages citing vendor pricing).
- Zoho Mail Lite: Rs 59-90/user/month per Indian resellers (official page not checked).
- DPDP Rules notified 13 Nov 2025; main obligations from ~May 2027 (18-month phase-in).

## Claude Code's draft plan (challenge this)
1. Buy `siteblitz.in` as the brand domain (+ optional `siteblitz.co.in`). Search the IP India trademark
   registry for "SITEBLITZ" first because of the French company.
2. Stop the free-Gmail sending now. Never cold-send from `siteblitz.in`.
3. 1,000/day = 30 inboxes x ~33/day on 10 separate .com sending domains (3 inboxes each), redirecting to the
   main site; SPF + DKIM + DMARC on every domain; 3-5 week ramp; Google Postmaster Tools.
4. Main org: 1 paid Workspace Base user (founder's real first name) with free aliases hello@, support@, billing@.
   Cold org: a SEPARATE Workspace account, 30 Starter users (Base caps at 20). No CEO/CTO mailboxes.
5. Every address verified before sending; one-line opt-out; suppression list; no fabricated addresses ever.
6. Costs: month 1 = .in Rs 1,061 + 10 .com Rs 11,160 + Workspace Rs 9,675 (31 users + 18% GST) +
   Instantly Growth Rs 4,442 + MillionVerifier 10k Rs 3,497 = ~Rs 29,800.
   Months 2-12 = Workspace Rs 9,675 + Instantly Hypergrowth Rs 9,167 + verification ~Rs 3,700 = ~Rs 22,500.
   Year 1 ~Rs 2.78 lakh. If phase 5 builds sending in-house, drop Instantly (~Rs 13,400/month).
7. Gate before buying the cold stack: prove ~22,000 real verified addresses/month exist.
