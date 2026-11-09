# Review - SiteBlitz domain + cold-email infrastructure (1,000 emails/day) - 2026-11-09 - 2 rounds - prompt: none (project context only)

FX Rs 94.5/USD (PTI close 94.46, 2026-11-05). Workspace prices are Google India annual-commitment list prices + 18% GST.
USD bills (Porkbun, Instantly, MillionVerifier, Vercel) exclude card forex fees and any GST the vendor adds.

| # | Point | Proposed by | Evidence (file:line / round) | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | Brand domain `siteblitz.in`, bought only after a free IP India trademark search (classes 35 + 42) | Claude, ChatGPT conditional | NIXI RDAP "available" 2026-11-09; siteblitz.com taken since 2001; French "SiteBlitz" on siteblitz.ai + getsiteblitz.com + trysiteblitz.com (2026-06-16) | agreed | Agreed |
| 2 | Spam cause #1 (suspected): fabricated / unverified recipients; free Gmail by itself is not the root cause | Both | `backend/app/engines/enrichment/discovery.py:139`; `surat_restaurant_leads_with_contacts.csv` 37 of 38 emails generated; Google Gmail help: >500 emails/day cap | agreed - unproven until the team says which list it sent | Agreed |
| 3 | Do not buy 30 inboxes / 10 domains now; gate on data + pilot first | ChatGPT R1 (Claude draft had the gate) | R1 s3, R2 A | agreed | Agreed |
| 4 | Send through a bulk ESP instead of inboxes | ChatGPT R1 | SendGrid prohibits lists "that have not affirmatively consented"; Brevo never allows purchased/scraped lists | rejected - ESPs ban non-consented first-touch mail | Rejected |
| 5 | One paid Workspace Base user `hello@siteblitz.in` ("SiteBlitz Team") + free aliases projects@, support@, billing@; no CEO/CTO mailboxes; 2nd seat only when the friend needs his own login | Both | Google: 30 aliases/user free; Base Rs 99, max 20 users | agreed | Agreed |
| 6 | Cost corrections: Instantly Hypergrowth USD 107 (125k emails, 25k contacts; +25k contacts = USD 87/mo); Growth (5k emails, 1k contacts) cannot carry live 1k/day sending; MillionVerifier USD 89 / 50k | ChatGPT R1-R2 | instantly.ai/pricing and millionverifier.com, checked 2026-11-09 | agreed - delete finished contacts in Instantly, keep the suppression list in our DB | Agreed |
| 7 | Hosting line missing: Vercel Hobby is non-commercial; Pro USD 20/seat/month (~Rs 2,230 with 18%) | ChatGPT R1 | SiteBlitz DECISIONS D12; third-party Vercel pricing pages | agreed - separate decision (D12) | Agreed |
| 8 | Live `siteblitz.vercel.app` still shows withdrawn Rs 14,999 / Rs 24,999 and the bouncing `hello@siteblitz.in` (6x) | ChatGPT R1 | curl of the live page 2026-11-09 vs `E:\Temp\SiteBlitz\src\lib\offer.ts` | agreed - fix before any outreach | Agreed |
| 9 | Go/no-go gates: verified-email yield >= 20%, hard bounce <= 1%, Gmail spam < 0.10%, positive replies >= 3%, >= 3 paid orders per 3,000 sends | ChatGPT R2 | Google sender FAQ (0.1%); others judgement; rule of three: 0 complaints in 3,000 -> 95% bound 0.1% | agreed as judgement thresholds | Agreed |
| 10 | Pilot from `hello@siteblitz.in` at 20/day | ChatGPT R2 | R2 B, C | rejected - 3,000 sends at 20/day = 150 sending days, and cold mail would put the only real mailbox at risk; use a small separate pilot stack (below) | Rejected |
| 11 | Full 1,000/day stack (only if every gate passes): 30 inboxes x 33-34/day on 10 .com domains | Claude; ChatGPT costed it but does not approve it (Workspace AUP bans "large volumes of unwanted emails") | R2 B | agreed as the cost; the decision is the founder's after the gates, with suspension risk stated | Agreed (cost) |
| 12 | "Rs 13,400 saving is unsupported" | ChatGPT R1 | 22,542 - 9,167 = 13,375 is the cost without Instantly, not a saving | rejected - misread | Rejected |
| 13 | India DPDP (main rules from ~13 May 2027) + legal review of contact collection before scaling | Both | DPDP Rules notified 2025-11-13 | open - needs a lawyer, not a model | Open |

## The three cost levels

**Level 0 - now (business email only):** `siteblitz.in` Rs 1,061 + 1 Base user Rs 117/month.
Month 1 Rs 1,178 · year 1 Rs 2,463.

**Level 1 - pilot (3,000 sends = 1,000 verified contacts x 3 touches), separate Workspace org:**
2 .com domains Rs 2,232 one-time · 6 Base inboxes Rs 701/month · Instantly Growth Rs 4,442/month ·
MillionVerifier 10k Rs 3,686 one-time. With level 0: month 1 ~Rs 12,239, then ~Rs 5,260/month.
Timeline: 3-week ramp (5 -> 25/day per inbox), then 150/day for ~20 sending days; gate decision ~week 8.

**Level 2 - 1,000/day (only after the gates):** month 1 Rs 40,418 (10 .com Rs 11,160 + 30 Starter Rs 9,558 +
Hypergrowth Rs 10,112 + 50k credits Rs 8,411 + .in Rs 1,061 + Base Rs 117); then ~Rs 23,487/month with
verification for 22,000 addresses/month amortised; year 1 ~Rs 3.0 lakh. Add hosting ~Rs 2,230/month if Vercel Pro.
Keeping every old contact in Instantly would add USD 87/month per extra 25,000 contacts (~Rs 8.1 lakh/year) -
delete finished contacts instead.

## Recommended next steps (not started - waiting for your go)
1. Founder: IP India public trademark search for "SITEBLITZ" (classes 35, 42) - free.
2. Founder: buy `siteblitz.in` (complete NIXI e-KYC within 7 days) + Workspace Base `hello@siteblitz.in`, add
   SPF / DKIM / DMARC; stop all sending from the free Gmail accounts.
3. Code (lead generator): stop fabricating contacts (`discovery.py:122-148`, `lead_radar_service.py:309`,
   `export_surat_leads.py:139-159`); mark each contact verified / unverified / absent with its source.
4. SiteBlitz site: redeploy production from the current branch so the live prices and email match `offer.ts`
   (separate repo, `docs/DEPLOY.md`), and settle hosting (D12).
5. Phase 5 sender: real provider status instead of fake SENT, signed unsubscribe token, real postal address,
   India rules in `country_rules.py`.
6. Only after 1-5: level-1 pilot stack; level 2 only if the gates in row 9 pass.

## Points still open
- Which list the team actually sent from the free Gmail accounts, and its bounce / complaint numbers.
- Real verified-email yield of the lead generator for Indian SMBs (measured in the pilot).
- Legal review (DPDP, contact collection) and Google AUP risk acceptance for any first-touch volume.
- Trademark clearance result.
