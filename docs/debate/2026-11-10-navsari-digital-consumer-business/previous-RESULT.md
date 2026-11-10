# Review - India consumer gaps, round 2: aggregator and offline-to-online - 2026-11-10 - 3 rounds - prompt: consumer-gap-hunter

Prompt: `~/.claude-os/prompts/debate/consumer-gap-hunter.md`. Context sent: `founder-context.md` (2,070 bytes) and
`previous-RESULT.md` (7,664 bytes), nothing truncated. No code, no customer data, no secrets.
Founder constraints (answered after the 2026-11-09 round): consumer only, no B2B, no own field team at start
(aggregating independent providers is allowed), fresher founder, India first.
Stop reason: every agenda point is agreed or rejected; ChatGPT gave a closing decision in round 3 and another round
would only rotate the pick (it changed its first pilot every round: ironing -> occasion rentals -> adult hobby cohort).

**Headline:** no idea on any list passes all seven gates AND has a five-year scale score of 4 or more
(03_chatgpt.md, section A). Safe-for-a-beginner and big-enough-for-a-brand are different ideas. The only
evidence-based next step is a small paid experiment; no app should be built.

| # | Point | Proposed by | Evidence (file / round) | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | Zomato / Blinkit / OYO / Uber / Rapido built five things, not "app + marketing": supply, dense demand in one area, a fixed standard, failure resolution, positive money per order | ChatGPT R1 | Verified: Eternal 28.0 M monthly transacting customers Q2 FY27; Blinkit 2,751 stores 30 Sep 2026; PRISM FY26 GBV Rs 30,683 cr, PAT Rs 994 cr (about Rs 600-680 cr of it a deferred-tax credit); Rapido FY25 revenue Rs 934 cr, loss Rs 258 cr, subscriptions Rs 275 cr; Swiggy Instamart FY26 GOV Rs 28,496 cr, about -2.75% contribution (weighted, Claude calc). Wrong in R1 and corrected: Urban Company "500+ trainers" (own IR: 280-300+), Zomato "300,000+ restaurants" (unsourced) | agreed | closed |
| 2 | Offline-to-online cases: ScrapUncle, The Kabadiwala, Urban Company, DriveU, 99Pandit, Tumbledry (alive); DoorMint 2016, Doodhwala 2019, Dunzo 2025, Otipy May 2025 (dead) | ChatGPT R1 + Claude | ScrapUncle FY25 revenue Rs 15.5 cr, expenses Rs 17.5 cr, loss Rs 2.0 cr, buys and resells scrap (indianstartuptimes.com); The Kabadiwala FY25 Rs 10.1 cr (-21.5%), loss Rs 2.7 cr (Inc42); closures verified (YourStory, Inc42). FreshToHome did not acquire Doodhwala | agreed - even the Shark Tank scrap examples lose money | closed |
| 3 | Long list: 23 chores (R1) + 7 bigger categories (R2): occasion rentals, recreational sports, monthly parking, relocation + storage, used two-wheelers, adult hobby sessions, family-event packages | both | 01_chatgpt.md s3, 02_chatgpt.md s3. Competitors verified live: My Press Wala, BookMyDarzi (Delhi NCR), FixMyCycle (Rs 799), Hoora, Bento, Tifstay, DriveU, 99Pandit, Tumbledry (1,600+ claimed). Not found: "SnapPro", "Kadam's LunchBox" | agreed | closed |
| 4 | Scoring: 7 dimensions + 7 gates + new S (5-year ceiling). Ironing cut to W2 D1 S2 | Claude R2, accepted R2 | Local press-wala about Rs 10/piece (low confidence) vs model Rs 16 = 60% premium; Snabbit sells home help in Thane from Rs 99/hour | agreed | closed |
| 5 | Money models with founder pay (Rs 25k-30k example), Thane bottom-up size (734,496 households, TMC May 2026 - verified), bypass table | Claude R2, ChatGPT R2 | All calculations re-run by Claude and correct. One city: rentals at 100% capture give at most about Rs 1.59 cr platform revenue a year. Funded-chores warning: Snabbit FY26 loss Rs 167.75 cr on Rs 12.25 cr revenue (YourStory, Oct 2026); three instant-help players burned about Rs 140-150 cr in June 2026 | agreed | closed |
| 6a | First pilot = society ironing (R1) | ChatGPT R1 | low price premium evidence, high bypass, Snabbit in same micro-market | rejected (ChatGPT withdrew) | closed |
| 6b | First pilot = Rs 6,000 occasion-rental package (R2) | ChatGPT R2 | 7eventzz Rs 3,499 / Silverstone about Rs 4,999 packages with setup already exist; 1.2 bookings a year; overlaps round-1 graveyard | rejected (ChatGPT withdrew) | closed |
| 6c | First pilot = adult beginner hobby cohort, Thane West, 4 sessions at an assumed Rs 2,800, studio collects money, platform takes 15% referral fee, max Rs 12,000 budget; pass 12 full-price buyers + 4 re-buy; kill under 5 buyers after 60 conversations | ChatGPT R3 | Maths correct (Rs 33,600 / 5,040 / 2,040; budget Rs 12,000). Competitor prices (BookMyShow Rs 700 Bhangra, District Rs 1,050 pottery) NOT verified by Claude | agreed only as a learning experiment, not as the business choice - its contribution (about Rs 2,040) cannot pay a founder | founder decision |
| 6d | PG meals: research only until FSSAI route is clear - the 18 Mar 2026 order requires a central licence for a platform that lists food businesses and facilitates orders | ChatGPT R3 | FSSAI order verified (ONDC context) | agreed | closed |
| 7 | Graveyard adds generic society-chore bundle, generic sports-slot booking, generic parking listings, generic scrap clone; glossary (principal vs agent, founder salary vs profit, GMV vs revenue) | both | 01_chatgpt.md s7, 02_chatgpt.md s7 | agreed | closed |

## Recommended next steps (not started - waiting for your go)
1. Founder decides between: (a) the Rs 12,000 hobby-cohort learning experiment, or (b) a field week first - visit
   3 offline activities in Thane (press-wala, kabadiwala, tiffin kitchen) and ask 30 households what fails.
2. Whatever is picked, no app; one landing page + WhatsApp number only after a provider signs written terms.
3. Claude writes the one-page test plan and checklist for the chosen option.

## Points still open
- Founder: run the hobby-cohort test, the field week, or neither?
- Field data no desk research can give: real local prices, whether studios / vendors accept a 15% referral fee,
  real CAC, how many customers bypass after the first order.
- No national-scale winner exists yet; S scores are opinions, not measurements.

## Checks run and not run
- Run: all calculations in 3 replies re-computed; about 40 claims checked (one fact-check subagent + about 12
  Claude searches). Errors found and corrected in the next round: Urban Company trainers, Zomato restaurants,
  PRISM date, SnapPro, Kadam's LunchBox, BookMyDarzi fit guarantee, Doodhwala acquisition wording.
- Not verified: Thane hobby class prices (BookMyShow / District), ScrapUncle 45% gross margin, local ironing rate.
- No market research with real customers was done; every price, CAC and repeat rate is an assumption.
