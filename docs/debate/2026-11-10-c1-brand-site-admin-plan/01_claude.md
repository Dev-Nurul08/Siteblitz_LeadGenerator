name: edtech-startup-build-plan
use_when: Planning the brand, public website, ad / lead tracking and admin panel for a small online-classes startup (live small-group classes, independent teachers, parents as payers, children as learners) before Claude Code builds it - exact pages, data model, admin modules, stack, phases, compliance and child safety.

You and Claude Code are two equal partners planning a real startup's digital system before Claude Code
builds it. Claude Code writes the code, checks every claim you make with web search and its own tools, and
will build exactly what we agree - so vague advice is useless. Your job is to make the plan correct,
buildable and honest, not to agree.

The founder is a beginner in business and in software. The founder cannot debug clever code. Prefer the
boring, standard, well-documented option over the clever one, and say why in one line.

Rules for the plan:
- Every recommendation must be concrete enough to build: page names and sections, field names and types,
  status values, admin screens and what each shows, exact third-party products and the plan / tier needed.
- Separate what must exist on day 1 of a 30-day paid test from what can wait. A founder with no customers
  needs the smallest system that lets them take a lead, form a batch, take a payment and run classes.
- Honest marketing only: no invented reviews, student counts, teacher counts, awards or guarantees. Say what
  the site may truthfully claim at launch.
- Children are the learners. Child safety and parents' data rights are design inputs, not footnotes. Name
  the law (India DPDP Act 2023 and Rules 2025; for parents abroad, the UAE PDPL, UK GDPR, US COPPA where it
  applies) and say what the product must do.
- Third-party facts (prices, API limits, approval requirements, fees) need a source URL, the date and your
  confidence. Say "I don't know" freely.
- Nothing illegal, no scraping of private data, no messaging people who did not opt in.

Format of every reply:
- Answer each agenda point by number: "agree", "disagree because ...", or "need data: <what>", then add
  your own proposals under that point.
- End with the list of points still open.

<project_context>
<file path="E:/tmp/Siteblitz_LeadGenerator/docs/debate/2026-11-10-c1-brand-site-admin-plan/c1-research-RESULT.md">
# Review - Navsari, totally digital, consumer-only business - 2026-11-10 - 1 round - prompt: consumer-gap-hunter

Prompt: `~/.claude-os/prompts/debate/consumer-gap-hunter.md`. Context sent: `founder-context.md` and
`previous-RESULT.md` (8,480 bytes total, nothing truncated). No code, no customer data, no secrets.
Why one round: the founder asked for "a round" and a result. ChatGPT committed to one pick and its maths
re-ran correctly; the corrections below change details, not the pick. A second round is optional (see open points).

**Headline:** ChatGPT's single pick is **C1 - live online Gujarati conversation classes for children (7-12) of
Gujarati families abroad**, run from Navsari with independent Gujarati teachers paid per class. It is a paid
experiment, not a company yet. No idea in 18 has all 7 gates proven, and none earns a 5-year scale score above 3.

| # | Point | Proposed by | Evidence (file / round) | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | Thane prices, household counts and pilots are void; "no app first", positive money per order, founder pay in break-even and the Rs 25,000 pilot cap still hold | ChatGPT R1 | 01_chatgpt.md s1 | agreed | closed |
| 2 | "Totally digital" = digital product, live online service, online marketplace, or paid community; still needs human work. Navsari helps with Gujarati language, culture and finding Gujarati teachers; it does not help with ads, SEO or reaching people abroad | ChatGPT R1 | 01_chatgpt.md s2 | agreed. Claude adds: the real Navsari advantage for C1 is cost - a teacher paid in rupees serving a family that earns in dirhams / pounds / dollars | closed |
| 3 | 18 ideas in 3 pools (Navsari: interview prep, spoken English, senior phone help, school doubts, job alerts, scholarship guides; India: exam mock tests, budgeting, career restart, scam workshops, online Garba, nutrition; abroad: Gujarati for kids, Gujarati for adults, culture classes, cooking, family memoirs, festival calendar) | ChatGPT R1 | 01_chatgpt.md s3. Checked live: Gujutots (Zoom class for US/Canada children, no price published), Sanskar Teaching (Zoom Gujarati + Hindi school), Preply (24 Gujarati tutors, USD 11-30 / hr, average about USD 20), Alfaaz (Gujarati one of 8 languages, USD 61 / 171), PariksaPath (Rs 149 / month verified), Thangaat Garba online (Rs 699) | agreed with corrections: **Smriti Samskara teaches Hindi and Sanskrit, not Gujarati** (its Rs 2,100 / month price is right). **ExamPilot Gujarati is "still rolling out"**. **ChatGPT missed the cheapest competitor: temple and community schools abroad** - BAPS runs Gujarati classes in North America, Europe and Africa; Shree Hindu Temple Leicester charges GBP 50 a year; SKS Swaminarayan Temple London runs a Gujarati school up to GCSE | closed |
| 4 | Scores (F/I/N/U/W/D/T + S + L) and the 7 gates; none has 7 proven passes; none deserves S 4-5. Survivors: C1 Gujarati for kids abroad, A1 interview prep, C5 family memoir | ChatGPT R1 | 01_chatgpt.md s4 | agreed - scores are opinions; W for C1 should drop because near-free temple classes exist | closed |
| 5 | Money models with Rs 28,000 fixed cost (Rs 25,000 founder pay example + Rs 3,000 tools). C1 Rs 2,400 / child / month, 5 children per group, teacher Rs 600 per class: break-even 30 children. A1 needs 44 new buyers every month. C5 needs 25 families at Rs 4,999 every month | ChatGPT R1 | All sums re-run by Claude: correct. Fixes: (a) Razorpay international cards are up to 3% **plus 18% GST** = about Rs 85, not Rs 72, on Rs 2,400 - C1 still breaks even at 30 children, EBITDA Rs 1,850 instead of Rs 2,240; (b) the C1 funnel skips a step: 10,000 views x 3% = 300 clicks x 20% = 60 enquiries, and 10 buyers needs an unstated 1 in 6 to pay; (c) CAC Rs 600 for a family abroad is a guess with no evidence | agreed with fixes | closed |
| 6 | 30-day test "Gujarati Grandparents Conversation Club": UAE first, Rs 2,400 / child, 8 x 45-minute online classes, 2 groups of 5, budget Rs 21,920 (Rs 3,080 under the cap). Pass: 10 unrelated families pay full price, CAC at most Rs 600, 80% attendance, 5 commit to month 2. Kill: under 5 payers after 60 real parent conversations and Rs 6,000 of ads | ChatGPT R1 | Budget sums correct. Market size: about 189,000 people in England and Wales have Gujarati as main language (Census 2021); about 491,551 Gujarati speakers in the USA (ACS 2024); UAE about 300,000 is only a community estimate | agreed as a learning test, with 3 conditions: (1) the founder confirms whether they speak Gujarati well enough to talk to parents; (2) quote the price in the parent's currency and compare it with temple classes, not with Indian prices; (3) UAE has no official count - UK or USA have verified numbers but harder time zones | founder decision |
| 7 | Graveyard: generic Gujarati app, job-alert site, AI study PDFs, budgeting templates, festival calendar, tutor marketplace, finance / health advice, fraud-recovery help, general course marketplace. Laws: DPDP Act 2023 + Rules (notified 13 Nov 2025; children's parental-consent rule from about 13 May 2027), E-Commerce Rules amendment (in force 1 Jan 2027), GST Rs 20 lakh threshold for services from Gujarat, RBI payment-aggregator directions 15 Sep 2025 | ChatGPT R1 | DPDP phases and RBI direction verified (YourStory, AZB, rbi.org.in) | agreed | closed |

## Recommended next steps (not started - waiting for your go)
1. Founder answers one question: can you talk to Gujarati parents comfortably in Gujarati?
2. If yes: Claude writes a 1-page test plan for C1 - teacher quote checklist, a parent-call script, the price in AED / GBP / USD, and how C1 beats temple classes.
3. Do not build an app, do not register a company, and do not spend money until 2 Navsari teachers give written quotes.

## Points still open
- The founder's Gujarati ability (decides whether the founder can sell to parents).
- Real CAC to reach Gujarati parents abroad - unknown until a small ad test is run.
- Why a parent would pay Rs 2,400 a month when a temple class costs GBP 50 a year - needs real parent conversations.
- Whether C1 can grow beyond a one-person income (S = 3 today).

## Checks run and not run
- Run: every calculation in the reply re-computed; 14 claims fact-checked by a subagent (9 verified, 2 wrong,
  3 partly right) plus 3 Claude searches on Navsari population and diaspora.
- Not verified: UAE Gujarati count (community estimate only), Gujutots and Sanskar Teaching prices (not published),
  teacher rates in Navsari, any real CAC.

</file>

<file path="E:/tmp/Siteblitz_LeadGenerator/docs/debate/2026-11-10-c1-brand-site-admin-plan/C1-operating-plan.md">
# C1 operating plan - online Gujarati conversation classes for children abroad

Status: plan for a 30-day paid test. Nothing is built, registered or paid for until the founder says go.
Source of numbers: 01_chatgpt.md (round 1) and RESULT.md, with Claude's corrections. Anything marked
**[assumption]** is not verified and must be checked during the test.

## 1. The founder's role (updated 2026-11-10)
The founder does not speak Gujarati fluently; the founder speaks Hindi and English. So:
- **Founder = operator.** Finds parents, forms batches, collects money, pays teachers, checks quality,
  handles complaints. Talks to parents in English or Hindi.
- **Teacher = Gujarati expert.** Teaches the children, does the level check, and handles any parent or
  grandparent who prefers to speak only Gujarati.
- Teachers are **independent, paid per class** - not salaried employees. This keeps the test inside the
  "no payroll" gate. Salaried hiring is a later decision, only after the test passes.
- Parents abroad who want their children to learn Gujarati usually speak English themselves
  **[assumption - confirm in the first 10 parent calls]**.

## 2. Who is who
| Role | Where | What they do | Money |
|---|---|---|---|
| Parent (payer) | UAE first (UK / USA later) | Books and pays for the child | Pays Rs 2,400 per child per month |
| Child (learner), age 7-12 | At home abroad | Joins 8 online classes a month | - |
| Teacher (independent) | Navsari / Gujarat, online | Teaches a batch of 5 on a fixed schedule | Rs 600 per 45-minute class |
| Backup teacher | Navsari / Gujarat | Covers when the main teacher is absent | Rs 600 per class taken |
| Founder (operator) | Navsari | Sales, scheduling, payments, quality, support | Keeps what is left |

## 3. Tools - no app
| Need | Tool for the test |
|---|---|
| Information page | One landing page in English (price, 8 classes, timing, refund rule, contact) |
| Talking to parents | WhatsApp Business number + video call |
| Enrolment form | Google Form: child name, age, Gujarati level, preferred time slot, parental consent |
| Payment | A regulated payment gateway with international cards enabled (for example Razorpay: up to 3% + 18% GST on the fee). Check it supports UAE cards before advertising |
| Classes | Google Meet or Zoom, one fixed link per batch, waiting room on |
| Register | One Google Sheet: families, batches, attendance, payments, teacher pay, CAC |
The Rs 1,500 "landing page and tools" budget line covers these.

## 4. The flow, end to end
```
 SUPPLY (teachers)                 DEMAND (parents)
 1 Find 4-6 Gujarati teachers      4 Landing page + ads to adults in UAE
 2 Demo class + written terms      5 Parent intro call (English/Hindi)
 3 Pick 2 main + 1 backup          6 Google Form + level check by teacher
              \                      /
               7 BATCH = 5 children, same age band, same level, same slot
                              |
               8 Payment link -> paid -> welcome message + schedule + class link
                              |
               9 8 classes / month (2 a week) - teacher teaches, founder watches the register
                              |
              10 After each class: attendance + 3-line teacher note in the Sheet
                 Weekly: one WhatsApp update to each parent
                              |
              11 Day 1 and day 30: 2-minute speaking check, scored on a 4-item rubric
                              |
              12 Day 20-25: ask for month 2 (Rs 500 advance, adjusted in next fee)
                              |
              13 Pay teacher weekly from collected fees; record CAC and profit per batch
```

### Step details
1. **Find teachers.** Gujarati-medium school teachers, retired teachers, B.Ed / M.A. Gujarati students in
   Navsari and Surat. Ask for a 15-minute demo with a child (with that child's parent present).
2. **Written terms** (1 page): Rs 600 per 45-minute class; paid weekly; 24-hour notice for absence; backup
   teacher steps in; no recording; no private messages to children; teacher does not take the founder's
   families privately; materials stay with the business.
3. **Quality check without speaking Gujarati.** The founder cannot judge the Gujarati directly, so quality
   is measured by: attendance %, the rubric score from day 1 to day 30, the parent's answer to "did your
   child say something in Gujarati at home this week?", and a second teacher scoring one recorded-with-consent
   sample per batch **[optional, needs parental consent]**.
4. **Ads.** Rs 6,000 budget, shown to adults only, in the UAE, interested in Gujarati / Indian community.
   Ask community group admins before posting in their groups. Never message people who did not ask.
5. **Intro call.** 10 minutes: child's age, how much Gujarati the child understands, preferred time,
   why the parent wants it, what the temple / community class near them costs.
6. **Level check.** First 10 minutes of class 1 by the teacher. Age bands: 7-9 and 10-12.
7. **Batch rule.** A batch starts only when 5 children have paid. 4 paid children can start
   **[decision for founder]** but the teacher cost per child rises from Rs 960 to Rs 1,200.
8. **Time.** UAE is 1 hour 30 minutes behind India. Example slot: 7:00 pm in Navsari = 5:30 pm in Dubai.
9. **Renewal.** Ask on day 20-25. Count only paid advances as "renewal commitments".

## 5. Real-world example (illustrative - names and people are invented)
**Batch "Dubai A - age 7-9".** Mon and Thu, 5:30 pm Dubai / 7:00 pm Navsari, 8 classes in the month.

- **Week 1 - supply.** The founder meets 5 teachers online; 3 give a demo. Ms. Desai (main) and Mr. Joshi
  (backup) sign the 1-page terms at Rs 600 per class.
- **Week 2 - demand.** The ad sends 300 clicks to the landing page **[assumption]**. 60 parents enquire
  on WhatsApp. The founder calls them in English. Example parent: Mrs. Patel in Dubai, daughter Riya (8)
  understands Gujarati but answers her grandmother in English. She fills in the form and pays Rs 2,400.
  4 more families with children aged 7-9 pick the same slot - Batch A is full.
- **Week 3 - classes.** Class 1: Ms. Desai records each child's 2-minute level score in the Sheet. Each
  class practises one real home situation in Gujarati (greeting grandparents, food at the table, telling
  about school). The founder checks the register after each class. Thursday: Ms. Desai is unwell; Mr. Joshi
  takes the class.
- **Week 4 - result.** Riya greets her grandmother in Gujarati on a video call; Mrs. Patel writes this in the
  weekly update. On day 30 the rubric score rises **[to be measured]**. 3 of 5 families pay the Rs 500
  advance for month 2.

### Money for Batch A (one month)
| Item | Calculation | Rs |
|---|---|---|
| Fees collected | 5 x 2,400 | +12,000 |
| Teacher | 8 classes x 600 | -4,800 |
| Materials | 5 x 60 | -300 |
| Payment fees | 5 x 85 (3% + 18% GST) | -425 |
| Support | 5 x 100 | -500 |
| Ads to find these 5 (CAC) | 5 x 600 **[assumption]** | -3,000 |
| **Left for the business (contribution)** | | **+2,975** |
| Same batch in month 2 (no new ads) | 12,000 - 4,800 - 300 - 425 - 500 | +5,975 |

To pay the founder Rs 25,000 + Rs 3,000 tools a month, about **6 full batches (30 children)** are needed
when 1 in 3 children must be replaced every month (RESULT.md, point 5).

## 6. What can go wrong, and the fix
| Problem | Fix |
|---|---|
| Teacher absent | Backup teacher on the same terms; founder informs parents 2 hours before |
| Only 3-4 children for a slot | Offer the next slot, or start at 4 (lower margin) - never below 4 in the test |
| Teacher takes families directly | Several teachers, founder owns the parent relationship and the curriculum, clause in terms |
| Parent says the temple class costs GBP 50 a year | The offer is small groups of 5, fixed teacher, weekday slots, progress report - if parents still say no, that is the kill signal |
| International card fails | Test a Rs 10 payment from a UAE card before the ad goes live |
| Child safety | Fixed link with waiting room, parent present in class 1, no recording by default, no private chats |
| Child data (DPDP Act) | Parental consent in the form, collect only name / age / level, delete when the family leaves |

## 7. Test budget, pass and kill (from RESULT.md, unchanged)
Budget Rs 21,920 of the Rs 25,000 cap: ads 6,000; teachers 2 batches x 8 x 600 = 9,600; materials 600;
payment fees about 850; support 1,000; tools 1,500; contingency 2,500 (payment fees corrected from 720
to about 850, total about Rs 22,050).
- **Pass:** 10 unrelated families pay Rs 2,400; CAC at most Rs 600; attendance at least 80%;
  5 families pay the month-2 advance.
- **Kill:** fewer than 5 paying families after 60 real parent conversations and Rs 6,000 of ads.
- **In between (5-9 families):** finish the classes, find the bottleneck, build nothing.

## 8. Before spending the first rupee
1. A chartered accountant confirms GST and invoicing for fees paid from abroad.
2. Payment gateway approved with international cards.
3. Two teachers' written terms signed.
4. Landing page shows price, 8 classes, timings, refund rule and contact.

</file>
</project_context>

<topic>
# Topic - brand, website, ad tracking and admin panel for the C1 Gujarati classes startup

## The founder's words (translated from Hinglish)
"Skip finding teachers - I will do that myself. You build the ad system and the site. It should be a brand -
it can look like a startup, but it must be a proper startup. Website, ads, whatever else is needed - include
it all in the website and admin panel so that I can manage everything from the panel." Then: "Do the
complete planning using ChatGPT and build it completely."

## The business (agreed in the previous round - see c1-research-RESULT.md and C1-operating-plan.md)
- Live online Gujarati **conversation** classes for children aged 7-12 of Gujarati families living abroad.
  First market: UAE (UAE is 1 h 30 min behind India). UK and USA later.
- Batch = 5 children, same age band (7-9 or 10-12), same level, same time slot. 8 classes of 45 minutes a
  month (2 a week). Price used in the model: Rs 2,400 per child per month (to be shown in AED / GBP / USD).
- Teachers are independent Gujarati teachers in Navsari / Surat, paid Rs 600 per class, plus one backup
  teacher. The founder recruits them. The founder does not speak Gujarati fluently; the founder speaks
  Hindi and English and runs sales, scheduling, payments, quality and support.
- 30-day test: Rs 6,000 of ads, pass = 10 unrelated families pay full price, CAC at most Rs 600,
  attendance at least 80%, 5 families pay a Rs 500 advance for month 2. Kill = fewer than 5 payers after
  60 real parent conversations.
- Quality without speaking Gujarati: attendance %, a 2-minute speaking check scored on a 4-item rubric on
  day 1 and day 30, a weekly parent question ("did your child say something in Gujarati at home?").

## Competitors already checked by Claude Code (Nov 2026)
Kids Bolo (kidsbolo.com - Gujarati books + talking pen; virtual ages 3-5 sold out), Sanskar Teaching
(Zoom Gujarati school, free one-on-one trial class), Gujutots (UK, Zoom class for US/Canada children),
Outschool (Gujarati group classes, for example USD 25 per 40-minute class), Dinolingo (app, about
USD 19 a month), Preply (1:1 tutors USD 11-30 an hour, average about USD 20), temple / community schools
(BAPS in North America, Europe, Africa; Shree Hindu Temple Leicester GBP 50 a year).

## Agenda
1. Brand: 3 name candidates that do not clash with the competitors above (with a quick conflict check you can do), positioning line, tagline, tone of voice for parents abroad, and a visual direction (palette with hex values, two typefaces, illustration or photo style) that does not look like a generic template.
2. Public website: exact pages and sections, the conversion flow (ad -> landing -> enquiry -> intro call -> level check -> payment -> welcome), what it may honestly claim at launch, price display per currency, trust and child-safety elements, SEO basics.
3. Ad system: what the admin panel can realistically do itself versus inside Meta Ads Manager / Google Ads (approval needed for the Meta Marketing API, business verification), UTM link builder, campaign table, daily spend entry or import, leads per campaign, CAC per campaign, Meta Pixel / Conversions API with consent.
4. Admin panel: modules, screens and data model (field names and status values) for leads / CRM pipeline, families, children, batches with time zones, teachers, schedule, attendance, class notes, rubric scores, payments and invoices, teacher payouts, renewals, campaigns, reports (CAC, contribution per batch, break-even tracker), settings. Should teachers get a limited login to mark attendance and notes?
5. Stack and architecture a beginner can maintain: Claude Code proposes Next.js (App Router) + TypeScript + Tailwind + MongoDB Atlas + Vercel, Razorpay (payment links with international cards, webhooks), email via a transactional provider, WhatsApp click-to-chat first (WhatsApp Cloud API later), Zoom or Google Meet links. Agree or propose better, with monthly cost at test scale.
6. Phase plan: split the build into phases Claude Code can finish and verify one per session (each phase at most about 8 files of change), and mark exactly which phases must be live before the first paid family.
7. Compliance and safety built into the product: parental consent and data minimisation (DPDP Act 2023 and Rules; UAE PDPL; UK GDPR), cookie / pixel consent, refund and cancellation policy, terms, child-safeguarding rules for class links and teacher contact, invoicing for payments from abroad (GST on export of services - for a chartered accountant to confirm).

Answer each agenda point by number: agree / disagree because ... / need data: ... . End with the list of
points still open.
</topic>
