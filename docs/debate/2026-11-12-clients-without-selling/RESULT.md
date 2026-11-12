# Review - getting paid work when the founders are developers, not salespeople - 2026-11-12 - 2 rounds - prompt: dev-studio-client-acquisition-partner

Prompt: `~/.claude-os/prompts/debate/dev-studio-client-acquisition-partner.md` (new, written for this topic and saved
to the library). Context sent: topic.md, claude-position.md, CLAUDE.md, docs/PHASES.md (round 1, 17,520 bytes, nothing
truncated); round 2 carried Claude's verdicts and the two research passes. No secrets, no customer data, no names,
emails or phones of any business. Stop reason: after round 2 every agenda point is agreed or has a stated reason;
what remains open is data only the founders have.

Inputs: research-marketplaces.md and research-agency-market.md (two Claude Code research passes, vendor claims
marked), agency counts from the founders' own Overture extract (`E:\tmp\_strategy\agency_count.py`, counts only).
Nothing was sent to any business, bought, deployed or changed in code.

## Verification of the previous sessions' work (Claude Code, 2026-11-12)
| Claim | How checked | Result |
|---|---|---|
| Lead generator backend 338/338 tests | `pytest backend/tests` | **true** - 338 passed |
| Phase 14: 2,162 leads, 499 with an email, 619 addresses, 0 without a source URL | `summary.json` of the run | **true**. But 1,704 of 2,162 are Surat retail showrooms, 797 sit on 115 chain store-locator hosts, 136 of the 499 email leads are chains (363 independent remain), and all were selected because they already HAVE a website |
| Live site to be fixed (withdrawn prices, bouncing email) - flagged 2026-11-09 | fetched siteblitz.vercel.app | **not fixed, and worse than recorded**: "Studio Mumbai, India"; 5 invented named testimonials ("Rohan Mehta, Restaurant Owner, Mumbai", "Dr. Anjali Kapoor, Clinic Director, Pune", "Sameer Khan", "Priya Nair, Boutique Owner, Kochi", ...); 4 invented results ("2.4x more table bookings in 60 days", "38% lift in catalogue enquiries", ...); "indexing ... guaranteed"; Rs 14,999 / 24,999; hello@siteblitz.in x6. Production deployment dates from 2026-07-10 (CLI deploy, website repo docs/DEPLOY.md) |
| siteblitz.in unregistered | NIXI RDAP | **true** - still unregistered, so the address on the live site cannot receive mail |
| Demo pages | fetched /demo/salon | 404 live; exist only on branch v2-redesign |
| Truthful site exists | `git grep` on v2-redesign HEAD | **true** - 0 hits for the invented strings; branch is 50 commits ahead of origin, not pushed; a production build also needs NEXT_PUBLIC_SITE_URL in Vercel |
| Lead generator pushed | `git status -sb` | 29 commits ahead of origin (guard hook blocks Claude's push) |
| Outreach engine ready | docs/PHASES.md | phases 14b, 15, 16 not built; sender name / reply address / postal address blank; no sending domain |

## Decision table
| # | Point | Proposed by | Evidence | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | Diagnosis: building more lead tooling was the wrong priority; leads were available but intent, decision-maker access and trust were not; the live site with invented testimonials, wrong city and two price lists broke trust at the moment prospects checked; delivery management is unproven (no paid project yet) | Claude R1, ChatGPT R1 refined | verification table above | agreed | closed |
| 2 | Primary route: **white-label website implementation for agencies** - the agency owns the client, approved design, content and all client communication; SiteBlitz builds, tests and hands over under the agency's name | Claude R1, ChatGPT R1 | Gujarat 3,797 agency-type listings / 2,849 with a published email (Surat 813 / 641, Ahmedabad 1,399 / 1,059); India 43,401 / 31,284 (own Overture extract, unverified listings) | agreed | closed |
| 3 | Secondary route: **one founder takes contract development work** (existing team, backlog, someone else owns priorities) for cash; marketplaces, referral schemes and a commission-only salesperson are not run as programmes now; Framer Experts parked (different stack, still direct clients) | ChatGPT R1, Claude R2 | Upwork 6-16 Connects/proposal at $0.15, Fiverr 20 %, Webflow/Shopify/Wix/Codeable need history or are closed; Framer Experts page (updated 2026-10-02, checked by Claude) | agreed | closed |
| 4 | Offer: landing page (1 page, up to 6 sections) or 3-page site (up to 12 sections), one form, responsive, basic metadata, staging; staging target 3 / 5 working days, handover 5 / 7; ready-to-build gate (approved design, copy, assets, access, named approver, advance received); 50 % advance / 50 % before final handover; one consolidated revision round; 14-day defect window; exclusions listed; one founder is the delivery owner; fixed written update format; reply within one business day | ChatGPT R1 | market norm 40/40/20 (codingclave.com, 2026-10-25) | agreed | closed |
| 5 | Test prices for agencies: landing Rs 8,000-10,000; 3-page Rs 16,000-22,000; extra page Rs 3,000-5,000; changes Rs 750-1,000/h; review after 3 paid projects | ChatGPT R1 | 24siteshop partner base Rs 10,000 resold at Rs 20,000 (illustrative); Surat IndiaMART retail Rs 5,000-30,000; PortOrchard Surat Rs 6,999/year for 5 pages incl. hosting (Claude fetched) | agreed as test bands, not market value | closed |
| 6 | **Public site becomes agency-first**: remove the public retail package list; direct enquiries by quotation only; written no-poaching commitment (contract wording reviewed) | Claude R2, ChatGPT R2 | channel conflict: public Rs 7,999 vs wholesale Rs 8-10k | agreed | closed - founder approval needed (changes offer.ts) |
| 7 | Agency page, 8 sections: hero / who does what / 2 labelled concept demos / scope / indicative agency prices / delivery process / working terms / send a brief (no call needed). No testimonials, no "trusted", no guarantees | ChatGPT R2 | 02_chatgpt.md Q4 | agreed | closed |
| 8 | Finding the first agencies: qualify 50 by hand first (real client work, stack fit, source URL, one recipient per agency); 5 new approaches a day, 10 only if replies can be handled; follow-ups ~day 5 and ~day 12, then stop; built with the provenance-keeping extractor only, never `discover_contacts()` | ChatGPT R1, Claude R2 | CLAUDE.md rule | agreed | closed |
| 9 | Sending identity: real brand domain is fine for one-to-one business mail, but Google's Gmail / Workspace policies ban unsolicited commercial mail with no volume exemption; prefer agencies' own partner / vendor / contact routes; for wider cold email use a provider whose terms allow it (2026-11-10 RESULT row 10); SPF/DKIM/DMARC + suppression list | ChatGPT R2 | Google policy cited by ChatGPT; 2026-11-10 RESULT rows 8, 10 (Claude read Workspace AUP then) | agreed - risk flagged | open: founders pick the route |
| 10 | Brand: decide whether "SiteBlitz" survives before buying siteblitz.in (a French "SiteBlitz" in the same business, found 2026-06-16); one working day for an IP India search; rename now if the clash is real - there are no clients to migrate; never delay removing the invented claims while deciding | ChatGPT R2 | 2026-11-09 RESULT row 1; ChatGPT could not load siteblitz.ai | agreed | open: founder decision |
| 11 | Overseas: from week 3 (26 Nov) up to 2 of the daily approaches go to **US** agencies only (UK and AU later); readiness gate = truthful page + demos + stack fit + written quote + approved receiving account + named contracting party + permitted outreach method; no "2-4x" multiplier in any forecast; collection costs inside the quote (Skydo $19 + 18 % GST per payment = $44.84 on two payments = 22 % of a $200 job) | Claude R2, ChatGPT R2 | Codingclave $200-800 / $300-1,200 and PageTraffic from $799 (advertised); Skydo fees (xflowpay.com 2026-10-28) | agreed | closed |
| 12 | GST: the Rs 20 lakh test is aggregate turnover under one PAN (domestic + exports), not exports alone; CA confirms | ChatGPT R2 (corrects Claude) | CBIC, cited by ChatGPT | agreed | closed |
| 13 | Contract channels: LinkedIn Jobs, Cutshort, Flexiple; starting band Rs 800-1,200/h (open at about Rs 1,000); 4-6 h/week searching, then at most 20 billable h/week + 4 h admin; a full-time contract = a deliberate change of model | ChatGPT R2 | CompanyBench May 2026 Rs 6,000-10,000/day (gross C2C, 3-6 yrs Next.js); Flexiple Aug 2026 - both cited by ChatGPT, **not opened by Claude** | agreed as a negotiating band | closed (rates unverified) |
| 14 | Existing assets: website truth release first (pause website phase Q8 performance); founders push both branches; phase 5 is a gate for sending from the app, not for a hand-sent sheet; QA-1b triage only for the chosen workflow; pause 14b, 15, 16; archive the 2026-11-10 SMB playbook (kept, not deleted) | ChatGPT R1-R2, Claude R2 | 01/02_chatgpt.md s6 | agreed | closed |
| 15 | Gates (day 1 = 12 Nov): **18 Nov** commercial setup works (truthful site, demos, working mailbox, scope + quote templates, 50 qualified agencies); **2 Dec** first paid deposit, else more contract effort and review objections - never more outreach software; **11 Dec** one pilot delivered, accepted and fully paid; **26 Dec** no deposit after ~100-150 qualified contacts and two message/offer revisions -> pause the agency offer, contract work becomes primary; **10 Jan 2027** continue only with paid demand, workable hours per project and a path to the founders' minimum income | ChatGPT R1 | 01_chatgpt.md s7 | agreed | closed |

## Recommended next steps (not started - waiting for your go)
1. **Founders, today:** push both branches by hand (`git push origin phase-01-pipeline-repair` in this repo,
   `git push origin v2-redesign` in `E:\Temp\SiteBlitz`); set `NEXT_PUBLIC_SITE_URL=https://siteblitz.vercel.app` in
   Vercel Production.
2. **Website repo (one session):** truthful production release - deploy the v2-redesign truth pass, remove the
   retail price list (agency-first), add the 8-section agency page, make the 2 demos live with "Concept
   demonstration - not client work" labels, replace hello@siteblitz.in with a working address. Pause Q8.
3. **Founders, 1 day:** IP India trademark search for "SITEBLITZ" (classes 35, 42) + look at the French operator;
   keep or rename; then buy the domain and one mailbox.
4. **Lead generator (one session):** agency list - run the extractor on agency categories for Surat, Ahmedabad,
   Vadodara, Mumbai, Pune with the email finder on their own sites, output a qualification sheet (agency, domain,
   source URL, relevant work, stack fit, status) outside the repo; founders qualify 50 by hand.
5. **Templates (same session as 2 or 4):** scope sheet, brief form, quotation, handover checklist, written-update
   message, first agency email (01_chatgpt.md s4, honest identity and real demo link).
6. **Second founder:** profiles on LinkedIn Jobs / Cutshort / Flexiple, 4-6 h/week, Rs 800-1,200/h band.

## Points still open (founders' data)
- Cash runway, each founder's minimum monthly income, whether both are full-time, who owns agency communication and
  collections, who takes contract work, whether contract income goes into the studio.
- Notes from the past calls: why each prospect said no (no need / wrong person / budget / unclear scope / distrust /
  slow follow-up / price) - and which website version they saw.
- Brand decision (keep or rename) after the trademark search.
- Outreach route for agencies (their partner/contact forms and hand-sent LinkedIn notes first; a provider whose terms
  allow B2B cold email for anything wider) and the US message checklist.
- Contracting and receiving identity (which founder's PAN, Skydo approval), CA advice on GST registration and export
  documents; lawyer review of the no-poaching clause.
- Real build hours per package (timed demo builds) before the prices are trusted.
