# Founder context (written by Claude Code from the repositories and data - no customer data)

## Who and what
- SiteBlitz: a 1-2 person web studio in Mumbai, India. Sells small-business websites. Founder is not a
  native English writer; works with Claude Code (has the repos and data open) and ChatGPT as equal partners.
- **No paying client yet.** Everything done so far was free. The founder now wants paid work only.
- Strategy only in this conversation. Nothing is sent or built until the founder approves.

## The offer today (source: SiteBlitz repo `src/lib/offer.ts`, prices in INR, no GST - not GST-registered)
| Package | Price | Payments | Delivery |
|---|---|---|---|
| Launch | Rs 7,999 | Rs 4,000 deposit + Rs 3,999 balance | 1 page, 2 working days after "ready-to-build" |
| Business (recommended) | Rs 17,999 | Rs 9,000 + Rs 8,999 | 3 pages, 7 working days after "ready-to-build" |
| Custom | quoted | milestones in the quotation | e-commerce, bookings, more pages |
- "Ready-to-build" = pages/features confirmed in writing + content, images, business details received + access
  (domain, accounts) shared + first payment received + start date agreed.
- One consolidated revision round. Excluded: domain and hosting fees, paid plugins/stock, e-commerce, ad spend,
  guaranteed rankings/enquiries, unlimited redesigns, ongoing edits.
- Free personalised homepage concepts exist, capped at 3 per week (or 9 hours), decision FD-26.
- No prices exist yet for clients outside India (no USD / EUR / GBP / AED price list). Hard rule: no invented
  testimonials, client names, results or case studies - there are none.

## The lead data (source: `E:\SiteBlitz-World-Business-Data\README.md`, Overture Maps Places 2026-10-21.0, open data)
- 86,751,626 businesses (permanently closed removed), 247 countries. Largest: US 17.8 M, Brazil 5.8 M,
  Germany 4.7 M, India 4.7 M, UK 4.2 M, Italy 3.6 M, France 3.6 M, Mexico 3.3 M, Japan 3.0 M, Spain 2.5 M.
- With a phone 82 %, with an email 36 %, with their own website 54 %, social profile but no website 38 %
  (the best website leads), no website and no social 8 %.
- Fields per business: name, category, state, city, address, lat/lon, phones, emails, website, Facebook /
  Instagram / LinkedIn / TikTok / YouTube / X / WhatsApp links, Overture confidence 0-1.
- Emails and phones are what the business (or its listing source) published; nothing is verified yet.
- Measured today by Claude Code (DuckDB over all 86.75 M rows, counts only):

| Reachability bucket | World | % | India | US | Germany | UK |
|---|---|---|---|---|---|---|
| email + phone | 29,008,537 | 33.4 | 1,618,943 | 6,223,051 | 1,030,816 | 842,739 |
| email only | 1,957,523 | 2.3 | 120,300 | 284,226 | 59,538 | 80,264 |
| phone only | 41,959,736 | 48.4 | 1,818,700 | 9,402,584 | 3,178,607 | 2,736,673 |
| social profile only (no email, no phone) | 10,057,454 | 11.6 | 1,083,879 | 873,953 | 149,165 | 217,250 |
| website only | 1,551,632 | 1.8 | 22,108 | 512,748 | 89,804 | 143,193 |
| nothing | 2,216,744 | 2.6 | 10,018 | 510,733 | 173,615 | 146,397 |

| Email signal (first email per business) | World | India | Germany |
|---|---|---|---|
| businesses with an email | 30,966,060 | 1,739,243 | 1,090,354 |
| free-mail domain (gmail, yahoo, ...) | 16,742,936 (54 %) | 1,380,188 (79 %) | 168,632 (15 %) |
| same domain as their own website | 9,014,891 (29 %) | 242,417 (14 %) | 646,577 (59 %) |
| role address (info@, contact@, ...) | 5,967,866 (19 %) | 199,307 (11 %) | 550,183 (50 %) |
| same address listed on >= 5 places | 1,004,152 (3.2 %) | 14,442 (0.8 %) | 114,330 (10.5 %) |
| same address listed on >= 50 places | 602,721 (1.9 %) | 5,468 | 68,140 |
| invalid syntax | 12,483 | 459 | 4,985 |
- A separate lead-generator app (Python/FastAPI) finds and scores businesses by city and category.
  **Known defect:** its enrichment step generated guessed addresses such as info@<domain> - in one Surat export
  37 of 38 emails were generated, not found. These must be treated as fake/unverified.
- The team has been sending from several free Gmail accounts and landing in spam (founder report, 2026-11-09).

## Email infrastructure already agreed (2026-11-09 review, 2 ChatGPT rounds)
- Level 0: brand domain siteblitz.in (after a trademark search) + 1 Google Workspace inbox hello@ for replies and
  clients - never used for cold first touches.
- Level 1 pilot: separate org, 2 .com sending domains x 3 inboxes, Instantly Growth, MillionVerifier;
  3,000 sends = 1,000 verified contacts x 3 touches; 3-week warm-up 5 -> 25/day per inbox.
- Gates before scaling (level 2, 1,000/day): verified-email yield >= 20 %, hard bounce <= 1 %, Gmail spam
  < 0.10 %, positive replies >= 3 %, >= 3 paid orders per 3,000 sends.
- Bulk ESPs (SendGrid, Brevo) rejected: they ban non-consented first-touch mail.

## Compliance rules already coded (lead generator `qualification/country_rules.py`)
- US CAN-SPAM (postal address, opt-out, honour within 10 days), UK PECR (corporate subscribers no opt-in),
  EU GDPR legitimate interest with opt-out, Germany / Austria / Greece = manual review only, Canada CASL
  (conspicuous publication, role-relevant), Australia Spam Act (inferred consent by publication), default = opt-out.
- India-specific rules: not coded yet. DPDP Act legal review: open.

## What the founder asked for now (2026-11-10, translated from Roman Hindi)
1. What to send to businesses that have an email: content, structure, tone - it must read as written by a
   respectful human, never AI-generated, and get the maximum result from cold email.
2. Businesses with only a mobile number: how to message them - WhatsApp or something else.
3. Businesses with neither email nor phone: what to do.
4. Businesses whose email may be fake: what to do.
5. A complete lifecycle for every business, day by day: day 1 first mail, wait N days, follow-up, what to do
   when they reply, which requirements to collect, all the way to the exact moments payment is taken.
   Target is websites, but any paid service is fine for now.
6. Leads are in many countries: detect the country and write in that country's language, very respectful tone.
7. Something unique that makes the owner think "oh my god, these people found a new way" - for example a
   generated voice audio message inside the email or WhatsApp. Research whether that works.
8. Use only the necessary data; drop the rest.
