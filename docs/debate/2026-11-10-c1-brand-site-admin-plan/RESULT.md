# Review - C1 brand, website, ad tracking and admin panel - 2026-11-10 - 2 rounds - prompt: edtech-startup-build-plan

Prompt: `~/.claude-os/prompts/debate/edtech-startup-build-plan.md` (new, written for this topic and saved to the
library). Context sent: c1-research-RESULT.md + C1-operating-plan.md (round 1, 15,938 bytes); round 2 carried the
founder decisions and four Claude research passes (facts-checked.md, uae-law-checklist.md). No secrets, no customer data.
Stop reason: ChatGPT accepted every founder decision and Claude's rejections (Netlify, MongoDB, 8 phases) in round 2
and issued a locked decision table; another round would only repeat it.

| # | Point | Proposed by | Evidence (file / round) | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | Brand VaatKadi (વાતકડી = "vaat" talk + "kadi" link; coined word), backup VaatoNest; tagline "From 'Kem cho?' to real conversations at home"; palette #163A4A / #F4A340 / #228F83 / #FFF8EE / #E5C7B5; Plus Jakarta Sans + Noto Sans Gujarati; no fake reviews / counters / credentials | ChatGPT R1-R2 | Claude web check 10 Nov 2026: no business / app / social identity named VaatKadi, GharVaat or VaatoNest; RDAP: vaatkadi.com, vaatkadi.in, vaatonest.com unregistered (HTTP 404) | agreed - native-speaker check (3 people) + trademark check before buying the domain | closed (founder check open) |
| 2 | Public site: home, program, schedule, pricing, how-it-works, safety, faq, enquire, contact, privacy, terms, refunds, service-delivery, cookies, thank-you + imprint, complaints, complaints/track, feedback; reserve -> pay flow with reservationExpiresAt | ChatGPT R1 + Claude R2 | UAE e-commerce law 14/2023 Arts 5-9 (official text read by subagent) | agreed | closed |
| 3 | Stage-A price USD 29 / child / 8 classes via PayPal (about AED 106.50 shown as estimate); Stage-B AED 99 via Razorpay | ChatGPT R2 | Claude re-ran: 29 x 93.3767 = Rs 2,708; fee 4.4% + 0.30 = USD 1.58; 3% conversion USD 0.82; net about Rs 2,484; USD 27 nets about Rs 2,311; AED 99 Razorpay fees about Rs 89 each | agreed | closed |
| 4 | Ads: campaigns, UTM builder, manual + CSV daily spend (one record per campaign per day, import hash), CPL / CAC per family / CAC per child / ROAS / contribution; ad buying stays in Meta / Google; pixel only after consent; no child data to ad platforms | ChatGPT R1-R2 | facts-checked.md #8 | agreed | closed |
| 5 | Admin: 30 MongoDB collections, unique indexes, 5-seat rule via transaction on batchCycles.allocatedSeats, outbox pattern for external calls, scheduling engine (weekly pattern -> exactly 8 sessions, holidays, 15-minute teacher slot locks, reschedule history, substitutes), 15 email templates via Resend + scheduled function, manual WhatsApp with draft-opened vs sent-confirmed, tasks, consent ledger, privacy inbox, complaints, breach register, suppression list, send-window guard | ChatGPT R2 on Claude R2 request | Transactions on a local MongoDB 8.2.6 replica set verified by Claude; Atlas Free = 3-node replica set, MongoDB 8.0 (MongoDB docs) | agreed | closed |
| 6 | Stack: Netlify Personal + Next.js 16 (>= 16.4.5) + adapter >= 5.16.6 + TypeScript + Tailwind + MongoDB Atlas Free + Better Auth (founder TOTP mandatory, invited teachers, no public staff signup) + Resend + Google Meet + PayPal -> Razorpay + manual transfer | Claude R2 (ChatGPT withdrew Vercel + Postgres) | facts-checked.md H1-H8, P1-P7; Atlas docs: Free backups can be enabled (daily snapshot, 4 kept); ChatGPT's USD 0.10/day price not verified | agreed | closed |
| 7 | 8 phases: 1 foundation + deploy; 2 public site + legal; 3 DB + auth + CRM + consent; 4 teachers, batches, scheduling; 5 payments + invoicing; 6 operations + communications; 7 teacher portal; 8 ads, finance, reports. Gate A (first payment) = 1-6 + merchant approval + backups; Gate B (first class) = 7; Gate C (paid ads) = all | ChatGPT R2 | 02_chatgpt.md s6 | agreed | closed |
| 8 | Compliance mapped to pages / collections (UAE PDPL, e-commerce 14/2023, Child Digital Safety 26/2025, India DPDP); recording off; no ethnicity / religion fields; legal + tax review remain launch blockers | both | uae-law-checklist.md | agreed | closed |

Running cost at pilot scale (ChatGPT R2, Claude checked): Netlify Personal about Rs 840 / month; Atlas Free Rs 0
(+ up to about Rs 280 if backups are billed); Resend, Meet, Better Auth Rs 0. Payment fees for 10 children: PayPal
about Rs 2,240, Razorpay about Rs 890. Revised test budget Rs 23,440 of Rs 25,000.

## Recommended next steps (not started - waiting for your go)
1. Founder approves the spec-lock table (sent in chat) -> Claude writes it to the new project's docs/spec and builds Phase 1.
2. Founder in parallel: PayPal Business "Individual" KYC; Udyam registration; ask 3 Gujarati speakers about "VaatKadi";
   buy the domain after that; create Netlify + MongoDB Atlas accounts.

## Points still open
- Native-speaker + trademark clearance of VaatKadi; domain purchase.
- PayPal approval and a real guest-card test; Razorpay sole-proprietor approval; AED charging.
- Lawyer: KHDA / ADEK, UAE VAT, parental verification method, PDPL transfer ground. CA: GST export / LUT.
- Batch policy: start with 4 children?, reservation expiry, refund cutoff (48 h proposed), make-up classes.
- Atlas Free backup availability and price on the founder's account.
