# Claude Code's position (written before ChatGPT replies) - 2026-11-12

## The founders' situation (their own words, translated from Hinglish)
"SiteBlitz is a startup I started with a friend. We are both developers. Our sales experience is very bad. For
the last 6 months to a year we cold-called personally: we scraped data ourselves, called businesses and asked
about a website. We did not get even 1 client, and the few we reached did not like our management, did not like
the pricing, and we could not pitch well. If someone brought us clients and their requirements and said 'don't
worry, all communication is ours, you just develop', that would be perfect - we would deliver immediately,
effectively, reliably and extraordinarily. You and ChatGPT are partners: think as hard as you can, verify what the
previous sessions did, and tell us what to do."

Location: Navsari, South Gujarat. Public identity "based in Gujarat". Speak Hindi and English; Gujarati not fluent.

## The offer today (source: SiteBlitz repo src/lib/offer.ts, INR, not GST-registered)
| Package | Price | Payments | Delivery |
|---|---|---|---|
| Launch | Rs 7,999 | Rs 4,000 + Rs 3,999 | 1 page, 2 working days after ready-to-build |
| Business | Rs 17,999 | Rs 9,000 + Rs 8,999 | 3 pages, 7 working days after ready-to-build |
| Custom | quoted | milestones | e-commerce, bookings, more pages |
One consolidated revision round. Domain and hosting extra. No clients, reviews or case studies exist.

## What I verified today (2026-11-12) about the previous sessions' work
| Claim in the handoff / memory | Checked how | Result |
|---|---|---|
| Lead generator backend 338/338 tests | ran pytest | 338 passed |
| Email finder: 2,162 Surat/Navsari leads, 499 with an email, 619 addresses, 0 without a source URL | read summary.json of the run | matches. But 1,704 of the 2,162 are "retail_showroom" in Surat, 797 leads sit on 115 chain store-locator hosts, 136 of the 499 email leads are chain stores; 363 independent leads with an email remain. These businesses already HAVE a website (the run selected leads with a website) |
| Live site was to be fixed (withdrawn prices, bouncing email) since 2026-11-09 | fetched https://siteblitz.vercel.app today | NOT fixed: home page shows Rs 14,999 and Rs 24,999 (withdrawn) next to Rs 7,999, and hello@siteblitz.in 6 times |
| siteblitz.in is unregistered | NIXI RDAP today | still unregistered (404) - so the address printed on the live site cannot receive mail, and anyone could register the domain and receive it |
| Demo pages exist | fetched /demo/salon | 404 live; they exist only on the undeployed branch |
| Work is pushed | git status | lead generator 29 commits ahead of origin; website 50 commits ahead (guard blocks Claude's push; the founders push by hand) |
| Outreach engine (phases 15, 16) ready to send | docs/PHASES.md | not built; sender name, reply address and postal address still blank; no sending domain bought |

## My diagnosis (agenda point 1)
1. Leads were never the bottleneck. The founders had leads and called them. Phases 1-14 built better and more
   leads (86.75 M places, a website-need engine, an AI writer, an email finder) - good engineering, but it scales
   the part that was not broken. Every channel in the 2026-11-10 playbook (cold email, letters + QR) still ends
   with the founders qualifying, quoting and closing by themselves - the exact skills they say they lack.
2. The segment is the hardest one: small local shops in Navsari/Surat without a website (or with a broken one).
   They often do not feel the need (Instagram, WhatsApp Business and listings work "well enough"), they compare
   on price, and they buy from people they know.
3. Trust breaks at the moment a prospect checks: the live site shows two different price lists and a contact
   address that bounces, on a vercel.app address, with demo links that 404 and no past work. That alone can
   explain "pricing did not feel right" and "management did not feel right".
4. A phone pitch is a skill. Developers can learn it, but the founders' stated wish is to not do it.

## My recommendation (agenda points 2-7)
- **Primary: white-label build partner for digital agencies, India first.** Marketing, social-media,
  advertising, branding and graphic-design agencies already own small-business clients who need websites, and
  many have no in-house developer. The agency does all client communication; SiteBlitz builds under the agency's
  name. One relationship = repeated projects. The conversation with an agency is about speed, quality,
  reliability and price - the founders' strengths. B2B email to an agency's published address is legal and
  agencies publish emails: in the founders' own Overture extract, Gujarat has 3,797 agency-type businesses with
  2,849 published emails (Surat 813 / 641, Ahmedabad 1,399 / 1,059, Mumbai 2,519 / 1,696, Pune 1,365 / 997);
  India 43,401 / 31,284. Abroad (US 110,398 agency-type listings, UK 59,708, AU 12,217) comes later, after
  India proof and a foreign-payment route.
- **Secondary: one inbound marketplace listing** (a fixed-scope "business website in N days" gig) so that buyers
  arrive with a written brief and communication stays written. Which platform: research pending.
- **Not now:** a commission-only salesperson (hard to recruit and keep, they still need collateral and
  management), more local cold calling, the SMB email/letter campaign of 2026-11-10.
- **Offer for agencies:** a one-page wholesale price sheet by page type, a written brief form, turnaround from a
  complete brief, one consolidated revision round, staging link, white-label (no SiteBlitz branding), NDA and
  non-solicit, deposit before build for the first projects, an agreed daily/weekly status message. The first
  project as a small paid trial, never free. Exact prices wait for research.
- **Proof without clients:** 3 live demo sites (already built on the undeployed branch), a "for agencies" page,
  a screen recording of a build, the process document itself.
- **Existing assets:** fix the live site first (deploy the branch, one price list, a working contact address,
  register or drop siteblitz.in). Pause 14b / 15 / 16 (SMB outreach). Repurpose the lead generator: run it on
  agency categories in Gujarat + Mumbai + Pune and the email finder on their sites, to get a clean list of a few
  hundred agencies with source URLs. Keep QA-1b / phase 5 (remove fabricated contacts) because any sending
  needs it.
- **30-day gates (my proposal, to be argued):** week 1 site fixed + partner page + price sheet + brief form;
  weeks 2-4 about 20 personalised agency emails per working day (founders write the first line, an AI drafts the
  rest, a person sends); target 10 replies, 3 trial projects, 1 paid by day 30; stop rule: 300 agencies
  contacted and 0 trials -> change the offer or the route.

## Where I am unsure (please challenge)
- Whether Indian agencies pay enough per site for two developers to make a living, versus agencies abroad.
- Whether a marketplace is realistic for new sellers with no reviews in 2026.
- Whether one founder should take contract development work now for cash while the other runs the partner
  route.
