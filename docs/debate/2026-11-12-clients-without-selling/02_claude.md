# Claude Code - round 2 - verdicts on your round 1, new evidence, 5 questions

I checked your claims against the repos, the live site and two research passes (sources in the notes below).

## Verdicts
| # | Your point | Verdict |
|---|---|---|
| 1 | "Leads were never the bottleneck" too absolute; availability is not intent; classify past losses from call notes | agreed. Call notes go to the founders as an open item |
| 1 | Live homepage shows "Mumbai", named testimonials and claimed outcomes | **agreed and confirmed, worse than I wrote.** Fetched today: "Studio Mumbai, India"; 5 named quotes ("Rohan Mehta, Restaurant Owner, Mumbai", "Dr. Anjali Kapoor, Clinic Director, Pune", "Sameer Khan, Founder, D2C Brand", "Priya Nair, Boutique Owner, Kochi", ...); 4 invented results ("2.4x more table bookings in 60 days - Spice Route Kitchen", "First page of Google for 8 local keywords - Meadow Health Clinic", "38% lift in catalogue enquiries", "Consultation requests up 3x"); "indexing ... guaranteed"; "No advance until you approve the direction"; Rs 14,999 / 24,999. The production deployment dates from 2026-07-10 (a CLI deploy, website repo docs/DEPLOY.md), so prospects who looked during most of the calling period saw this. The truthful version exists on branch v2-redesign (0 hits for these strings), 50 commits ahead of origin, not deployed; a production build now also needs NEXT_PUBLIC_SITE_URL set in Vercel. The website repo's planned next phase is tap-latency performance work (Q8) - I will propose pausing it |
| 2 | Marketplaces rejected as a programme; contract development as secondary cash route | agreed. Research: Upwork proposals cost 6-16 Connects at $0.15 (skydo.com, 2026-11-03); Fiverr keeps 20 %; Webflow/Shopify/Wix/Codeable directories need client history or are closed. One exception I checked first-hand: Framer Experts (framer.com help, updated 2026-10-02) is instant, needs 2 published Framer sites on custom domains, and Framer routes client requests. I propose to park it (different stack, still a direct-client relationship) - agree? |
| 3 | Scope sheet, ready-to-build gate, 50/50 payments, one consolidated revision round, 14-day defect window, one delivery owner, written update format | agreed. Market reference: 40/40/20 (codingclave.com, 2026-10-25), partner 30/40/30 while the client pays 50/30/20 (abbacustechnologies.com, about Oct 2026). 50/50 kept for pilots |
| 4 | Qualify 50 agencies by hand first; 5 -> 10 new emails a day; 2 follow-ups; email law needs its own check, DPDP phased | agreed |
| 5 | Wholesale bands Rs 8-10k landing / Rs 16-22k three pages; Rs 550/h minimum rate model; review after 3 paid projects | agreed as test bands. Consistent with what we found: 24siteshop partner base Rs 10,000, agency resells at Rs 20,000 ("illustrative"); Surat IndiaMART retail Rs 5,000-30,000; PortOrchard (Surat) Rs 6,999/year for 5 pages incl. hosting (fetched today). Your Appna Studio and Site Easy figures: not verified by me |
| 6 | Asset table (site first, preserve unpushed work, phase 5 safety, QA-1b triage, pause 14b/15/16, archive SMB playbook) | agreed, one change: phase 5 is a gate for any sending FROM the app, not for a manually qualified sheet sent by hand. The agency list will be built with the provenance-keeping extractor only |
| 7 | Gates Day 7 / 21 / 30 / 45 / 60 with dates; stop rules | agreed. Week-1 items that only the founders can do (push, Vercel env var, domain, mailbox) are listed for them |

## Questions for round 2 (answer by number)
Q1. **Channel conflict.** The public site sells direct at Rs 7,999 (1 page). The proposed wholesale landing price is
Rs 8,000-10,000. An agency checking SiteBlitz sees it selling cheaper straight to end clients - and may fear
poaching. My proposal: make the public site agency-first ("development partner for agencies"), remove the public
retail price list, and take direct clients by quote only. Alternative: raise retail above wholesale. Which, and why?

Q2. **Abroad timing.** Overseas white-label prices are 2-4x India: Codingclave (India) advertises $200-800 per site
from the agency's design and $300-1,200 custom (2026-10-25); PageTraffic from $799 for 5 pages. Getting paid works for
an unregistered individual: Skydo $19 + GST per payment up to $2,000, personal PAN, free FIRA (xflowpay.com,
2026-10-28; skydo.com/help); exports below Rs 20 lakh need no GST registration (Notification 10/2017-IT; CA to
confirm). US CAN-SPAM, UK corporate subscribers and AU inferred consent are already coded in the lead generator.
Outreach is written and async - the founders' strength. I propose a small overseas cohort (2 of the daily 5-10)
from week 3 once a Skydo account exists, instead of waiting for India proof. Agree or not, with the risk you see.

Q3. **Sending identity.** On 2026-11-09 we agreed the brand-domain mailbox is never used for cold first touches -
that was for 1,000/day volume. For 5-10 hand-written emails a day to agencies, I propose: register one domain,
one Google Workspace mailbox with SPF/DKIM/DMARC, send by hand from it, no sequencer. siteblitz.in is still
unregistered (NIXI RDAP 404 today), and a French company called SiteBlitz (same business) owns siteblitz.ai.
Is sending from the brand domain acceptable at this volume, and should they buy siteblitz.in now or first decide
whether the brand survives?

Q4. **The agency page.** Give the exact sections of a one-page "for agencies" page (max 8 sections, one line each),
using only true claims: no clients, no reviews, two labelled concept demos, the scope sheet, the process, prices.

Q5. **Contract work.** Where exactly should the second founder look for contract development that comes with a
backlog and a project manager (name the channels), what day rate or hourly band is realistic for a mid-level
Next.js/React developer in India in 2026 (with sources), and how many hours a week can go there without
starving the agency test?

End with the list of points still open.
