

---

## Claude Code - 2026-11-10 08:22 UTC - 01_claude.md - attachments: none

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


---

## ChatGPT (Extra High) - 2026-11-10 08:36 UTC - saved as 01_chatgpt.md

ChatGPT said:
C1 Gujarati Classes Startup — Brand, Website, Advertising & Admin System

Planning review · 10 November 2026 · For Claude Code implementation

Overall decision

Agree with building a proper branded startup website and an integrated admin system. Disagree with building every advanced feature before the first paying customer.

The objective is to create a credible education brand with a reliable digital operating system—not merely a landing page. However, the earlier business research has not yet proven customer acquisition costs, willingness to pay or long-term retention.

I recommend designing the complete architecture now, then implementing it in controlled phases.

Priority

	

What must be delivered




Before the first paid family

	

Brand, public website, enquiry capture, admin login, CRM, parent records, consent, batch allocation, payment collection, basic campaign tracking and legal pages




Before the first class

	

Teacher access, secure class links, attendance, session management and speaking assessments




After initial validation

	

Automated ad reporting, detailed profitability dashboards, advanced renewals, parent portal and deeper integrations

The founder will recruit teachers independently. The application should manage their information, schedules, class records and payments, but it does not need a teacher-recruitment marketplace.

1. Brand identity

Verdict: Agree — build a distinctive, parent-focused brand rather than a generic children's tuition website.

Three name candidates
વ

1. VaatKadi — વાતકડી

Preferred candidate

A proposed name built around the ideas of conversation and connection. Short, distinctive and suitable for an education brand that may later introduce additional conversation programs.

ઘ

2. GharVaat — ઘરવાત

Emphasizes conversations at home, particularly between children, parents and grandparents. Emotionally relevant to Gujarati families living abroad.

V

3. VaatoNest

A more international, contemporary name combining Gujarati conversation with a welcoming learning environment. Easier to extend into multiple countries.

Quick conflict check: Public web searches on 10 November 2026 did not surface an obvious exact-name competitor for these three candidates. This is not confirmation that the trademarks, social handles or domains are available. I excluded VaatSetu because that name already appears as an existing social identity. 
Pictame
+1

Before committing, check exact and similar spellings using India's official trademark search in Class 41 (education), relevant international trademark registries, and the chosen domain registrar. Confirm pronunciation and intended Gujarati meaning with a fluent speaker. 
PublicSearch
+1

Positioning and messaging

Positioning line: Live, small-group Gujarati conversation classes for children growing up abroad.

Tagline: From “Kem cho?” to real conversations at home.

Primary promise: Help children practise speaking Gujarati with family through guided, age-appropriate conversations.

The tone should be warm, reassuring, culturally connected and clear. Address parents, not children, because parents are the decision-makers and payers. The language should emphasize speaking confidence and family connections without suggesting guaranteed fluency.

Visual design system

Deep teal

#163A4A

Warm cream

#FFF8EE

Marigold

#F4A340

Heritage teal

#228F83

Soft clay

#E5C7B5
Gujarati roots. Everyday conversations.

A warm editorial style, not a conventional tuition template.

Explore classes

Parent enquiry

Use Plus Jakarta Sans for English and Noto Sans Gujarati for Gujarati. Both should load through the application's font system rather than depending on fonts installed on a visitor's device.

The visual identity should use custom conversational illustrations, subtle speech-bubble motifs, warm home environments and restrained cultural details. Avoid generic graduation caps, stock photographs pretending to show actual students, exaggerated cartoons or religious symbols that could make the service appear exclusive.

Day-one requirement: Wordmark, icon, palette, typography, favicon, social profile assets and reusable UI components. A complex brand animation can wait.

2. Public website and conversion flow

Verdict: Agree — the website must convert interested parents into paying families, not simply collect traffic.

Exact public pages

Route

	

Required sections

	

Timing




/ Home

	

Hero, value proposition, class summary, pricing preview, process, safety reassurance, CTA

	

Before payment




/program

	

Ages 7–9 and 10–12, conversation topics, learning method, expected practice

	

Before payment




/schedule

	

Available UAE-local slots, batch availability, timezone explanation

	

Before payment




/pricing

	

Eight classes, 45 minutes each, price, inclusions, exclusions, payment and refund explanation

	

Before payment




/how-it-works

	

Parent enquiry, introductory call, level assessment, enrolment and class commencement

	

Before payment




/safety

	

Parent communication, teacher supervision, recording policy and safeguarding

	

Before payment




/faq

	

Levels, absence, class sizes, payments, timings, cancellations

	

Before payment




/enquire

	

Secure parent enquiry form

	

Before payment




/contact

	

Support email, business identity, WhatsApp contact and response expectations

	

Before payment




/privacy, /terms, /refunds, /service-delivery

	

Legal, privacy and service policies

	

Before payment




/cookies

	

Tracking and consent explanation, preferences control

	

Before tracking




/thank-you

	

Enquiry confirmation and next-step instructions

	

Before payment

For a compact initial website, /how-it-works, /schedule and pricing previews can be included on the home page as well as their dedicated routes. Avoid publishing empty pages.

Home page structure

The first screen should communicate the product immediately:

VaatKadi વાતકડી

How it works · Safety

Help your child speak Gujarati with family.

Live online conversation classes for children aged 7–12, in small groups of up to five.

Enquire about a batch

8 × 45-minute classes

Illustrative home-page direction, not a final production design.

Immediately below the hero, include the program overview, class format, an honest explanation of the teaching approach, available enrolment slots, the founder's contact details, safety policy, FAQs and a second enquiry CTA.

Conversion journey
Adult-targeted ad
Landing page
Parent enquiry
Introductory call
Level check
Confirm batch
Payment confirmed
Welcome + schedule

The introductory call is approximately 10 minutes in English or Hindi. The Gujarati-speaking teacher handles the level assessment. A short optional assessment before payment determines grouping; the baseline speaking assessment in class one is separately recorded for progress comparison.

Important exception: Five children need compatible levels and schedules. Do not collect full fees without clearly explaining whether the batch is confirmed or conditional. First gather suitable reservations, then invite payment. If the required group does not form by the communicated deadline, offer another slot or a full refund.

Parent enquiry fields

Before asking for a child's information, initially collect only parent_name, email, whatsapp_e164, country, iana_timezone, child_age_band, gujarati_level, preferred_slot_ids, contact_request_consent, and the campaign source.

Collect the child's preferred name and more specific learning details only after a verified parent/guardian enrolment process. Operational contact permission and optional promotional marketing consent must be separate.

Pricing and currencies

The original unit economics use ₹2,400 per child for eight classes. UAE parents should see a clear AED price before payment, not an unexplained INR figure.

My proposed pricing implementation is:

UAE: a draft offer of AED 99 per child per eight-class cycle, subject to checking that net INR settlement preserves the business model.

India accounting: store the actual charge, gateway fees, currency conversion and INR settlement.

UK and USA: configure GBP and USD, but do not publish unapproved prices before those markets open.

If Razorpay cannot charge in AED for the approved merchant account, show the actual INR charge and explicitly explain the approximate local-currency amount and any card-bank conversion uncertainty. Never describe an estimate as a guaranteed amount.

Honest marketing at launch

The website may truthfully say it offers live Gujarati conversation classes, groups of up to five, age bands 7–9 and 10–12, and eight 45-minute sessions per cycle—provided these arrangements are genuinely available.

It must not invent reviews, successful student outcomes, years of operation, teacher credentials, enrolment figures or awards. Testimonials and children's photos should be absent until there are real examples and appropriate permissions.

SEO and discoverability

Use server-rendered, indexable public pages with a single clear H1, unique metadata, sitemap, canonical URLs, robots.txt, Open Graph images, accessible headings, descriptive alt text and structured data only for truthful business and service information. Suggested early search themes include Gujarati speaking classes for kids in Dubai, online Gujarati conversation classes for children, and Gujarati lessons for kids abroad.

Track enquiry submissions rather than treating page views as commercial success. Keep /admin and sensitive payment or family pages excluded from indexing, with authentication still enforced.

Razorpay's international-card onboarding also expects a functional website with terms, privacy, refund/cancellation and service-delivery information, so those pages are operational requirements, not decoration. 
Razorpay
+1

3. Advertising, lead tracking and campaign management

Verdict: Partly agree. Build an internal advertising intelligence system now; do not attempt to replace Meta Ads Manager or Google Ads on day one.

The admin panel should be able to answer four questions:

How much did we spend?

Where did interested parents come from?

How many became paying families?

Did those customers generate a positive contribution after costs?

What the admin can realistically manage

Capability

	

Initial implementation

	

Later




Define and organize campaigns

	

Internal admin

	

—




Generate UTM tracking links

	

Internal admin

	

—




View lead sources and conversions

	

Internal admin

	

—




Record daily ad expenditure

	

Manual entry

	

CSV/API import




Calculate cost per lead and CAC

	

Internal admin

	

—




Upload ad creative references

	

Internal admin

	

—




Create and launch Meta ads

	

Meta Ads Manager

	

API if justified




Edit audiences, bids and ad budgets

	

Meta Ads Manager

	

API if approved




Google Ads management

	

Google Ads

	

API later




Conversion tracking

	

First-party enquiry and payment records

	

Consent-controlled Pixel/CAPI




Automated performance synchronization

	

—

	

Approved APIs

There is an important 2026 terminology correction: Meta renamed its Ads Management Standard Access feature to Marketing API Access Tier in May 2026, with Limited and Full access levels. The ads_management permission is separate. Managing only an app owner's ad account may have different access requirements from managing third-party accounts; business verification, permissions and reviews depend on the integration. Claude Code must not assume unrestricted access. 
Meta Horizon OS Developers
+1

UTM link builder

Example generated link:

Plain text
/enquire
?utm_source=meta
&utm_medium=paid_social
&utm_campaign=uae_gujarati_parents_nov26
&utm_content=grandparents_video_a

The admin should generate the complete URL and allow one-click copying. Each enquiry should preserve its first known campaign attribution and most recent attributable campaign, when available.

Campaign management screen

Use these fields:

id: uuid, name: text, platform: enum(meta, google, organic, referral, other), external_campaign_id: text?, target_country: char(2), objective: text, budget_minor: bigint, currency: char(3), start_date: date, end_date: date?, status: enum(draft, active, paused, completed), landing_path: text, created_at: timestamptz.

A related campaign_daily_spend record should contain campaign_id, spend_date, amount_minor, currency, fx_rate_inr, impressions?, clicks?, entry_method (manual, csv, api) and source_reference.

For CSV imports, uniquely identify rows by campaign, date and source record ID so importing the same report twice cannot double-count spending.

Reporting formulas

Metric

	

Calculation




Leads

	

Unique identifiable parent enquiries




CPL

	

Campaign spend ÷ attributed leads




Lead-to-paid conversion

	

Paying families ÷ leads




CAC per paying family

	

Campaign spend ÷ first-time paying families




CAC per child

	

Campaign spend ÷ newly acquired paying children




Contribution

	

Collected fees − direct delivery and acquisition costs




Campaign ROAS

	

Attributed collected revenue ÷ campaign spend

The initial hypothesis of ₹6,000 ad spend for ten paying families means a ₹600 CAC. It is a target, not an observed result.

A WhatsApp link click is not a verified lead. The platform can record the click, but the founder must identify the parent through a form or voluntary conversation. Do not scrape WhatsApp group members or treat anonymous visits as qualified leads.

Meta Pixel, Google tracking and Conversions API

The day-one system can work with UTMs and verified internal conversions. Advertising pixels are optional for initial measurement.

For later integration, require a genuine consent choice before loading marketing trackers. The consent system must support accepting, rejecting and changing preferences. Google's documentation distinguishes basic consent mode, which blocks tags before consent, from advanced mode, which can transmit cookieless signals; I recommend the simpler basic/block-until-consent approach initially. 
Google for Developers
+1

If both Meta Pixel and Conversions API are enabled, deduplicate shared events using the same event_name and event_id. Only use appropriately consented adult-related events; never send children's identities, learning assessments or attendance to advertising platforms. 
Adobe Experience Platform

Acceptance test: An adult clicks an ad, submits an enquiry, gets marked qualified, and pays. The admin attributes the new customer to the appropriate campaign without manual counting or duplicate conversions.

4. Admin panel and database design

Verdict: Agree — a single operational admin is justified, but access must be strictly role-based.

Admin navigation

Screen

	

What the founder sees




/admin

	

Today's calls, open enquiries, pending payments, upcoming classes, test targets




/admin/leads

	

CRM pipeline, call notes, follow-up dates, source campaign




/admin/families

	

Guardians, contact information, enrolments, payment status




/admin/children

	

Enrolled learners, age band, level, consent and progress




/admin/teachers

	

Approved teachers, agreements, availability, assigned batches




/admin/batches

	

Capacity, matching levels, paid seats, teacher and status




/admin/sessions

	

Class calendar, local times, meeting-link access, substitutes




/admin/attendance

	

Attendance by class and child




/admin/assessments

	

Baseline and end-of-cycle speaking scores




/admin/payments

	

Links issued, collected amounts, failures, refunds, reconciliation




/admin/invoices

	

Invoice numbers, tax treatment, issued documents




/admin/payouts

	

Teacher classes delivered, amounts due and paid




/admin/renewals

	

Parents due for renewal, advances collected, next-cycle decisions




/admin/campaigns

	

Campaign details, UTMs, spend and conversion reports




/admin/reports

	

Enrolments, CAC, batch contribution, cash flow, break-even




/admin/privacy

	

Parental consent, access/deletion requests, restricted safety incidents




/admin/settings

	

Prices, age bands, schedules, terms, permissions and notifications

Core relational data model

I recommend PostgreSQL-style types for the following schema. All records should include created_at and updated_at where applicable; references ending in _id are foreign keys.

Table

	

Essential fields and types

	

Main statuses




admin_users

	

id uuid, auth_user_id uuid, role text, is_active boolean

	

super_admin, operations, teacher, finance_readonly




leads

	

id uuid, parent_name text, email text, phone_e164 text, country char(2), age_band text, level text, campaign_id uuid?, next_action_at timestamptz?, status text

	

new, contacted, call_booked, qualified, waitlisted, payment_pending, won, lost, do_not_contact




lead_activities

	

id uuid, lead_id uuid, activity_type text, note text, actor_id uuid, occurred_at timestamptz

	

Types: call, whatsapp, email, note, status_change




families

	

id uuid, primary_parent_name text, email text, phone_e164 text, country char(2), timezone text, lead_id uuid?, status text

	

active, paused, inactive




children

	

id uuid, family_id uuid, preferred_name text, age_years smallint, age_band text, initial_level text, status text

	

pending_consent, active, inactive




consents

	

id uuid, family_id uuid, child_id uuid?, purpose text, policy_version text, granted_at timestamptz, withdrawn_at timestamptz?, verification_method text

	

granted, withdrawn, superseded




teachers

	

id uuid, user_id uuid?, display_name text, email text, hourly_or_session_rate_minor bigint, currency char(3), agreement_version text, status text

	

candidate, verified, active, on_leave, inactive




batches

	

id uuid, code text, age_band text, level text, capacity smallint, timezone text, teacher_id uuid, backup_teacher_id uuid?, status text

	

forming, payment_open, confirmed, active, completed, cancelled




batch_cycles

	

id uuid, batch_id uuid, cycle_start date, cycle_end date, session_count smallint, price_minor bigint, currency char(3)

	

planned, open, active, completed




enrolments

	

id uuid, child_id uuid, cycle_id uuid, payment_id uuid?, status text

	

reserved, offered, payment_pending, paid, active, completed, withdrawn, refunded




sessions

	

id uuid, cycle_id uuid, teacher_id uuid, starts_at timestamptz, ends_at timestamptz, meeting_reference text, status text

	

scheduled, completed, rescheduled, cancelled




attendance

	

id uuid, session_id uuid, child_id uuid, status text, marked_by uuid, marked_at timestamptz

	

present, late, absent_notified, absent_unnotified, excused




session_notes

	

id uuid, session_id uuid, child_id uuid?, teacher_id uuid, note text, created_at timestamptz

	

No workflow status




assessments

	

id uuid, child_id uuid, cycle_id uuid, assessment_stage text, rubric_version text, scores jsonb, assessor_id uuid, assessed_at timestamptz

	

baseline, endline




payments

	

id uuid, family_id uuid, gateway_link_id text?, gateway_payment_id text?, amount_minor bigint, currency char(3), settled_inr_minor bigint?, status text

	

created, link_sent, paid, failed, expired, partially_refunded, refunded, disputed




invoices

	

id uuid, family_id uuid, payment_id uuid, invoice_number text, issued_at timestamptz?, tax_treatment text, amount_minor bigint, status text

	

draft, issued, void, credited




teacher_payouts

	

id uuid, teacher_id uuid, period_start date, period_end date, amount_minor bigint, paid_at timestamptz?, status text

	

accrued, approved, paid, disputed




renewals

	

id uuid, enrolment_id uuid, next_cycle_id uuid?, advance_payment_id uuid?, status text

	

not_due, invited, advance_paid, renewed, declined, expired




campaigns, campaign_daily_spend

	

Fields specified in point 3

	

Campaign and spend records




privacy_requests

	

id uuid, family_id uuid, request_type text, requested_at timestamptz, completed_at timestamptz?, status text

	

submitted, verified, in_progress, fulfilled, rejected_with_reason




audit_logs

	

id uuid, actor_id uuid?, action text, entity_type text, entity_id uuid?, occurred_at timestamptz

	

Append-only




webhook_events

	

provider text, provider_event_id text, received_at timestamptz, processed_at timestamptz?, status text

	

received, processed, failed

Supporting settings and restricted safeguarding_incidents tables should also exist.

Important integrity rules

The database must enforce more than what the interface displays:

A child cannot have duplicate active enrolments in the same cycle; a batch cannot exceed five active/paid seats.

A session must last 45 minutes by default, and each cycle must explicitly have eight planned sessions. Do not assume that every calendar month automatically contains exactly eight Monday/Thursday meetings.

Money uses integer minor units, not floating-point arithmetic. Payment records have unique gateway identifiers.

All scheduled events are stored as UTC timestamps with an IANA timezone such as Asia/Dubai or Asia/Kolkata. UK and US daylight-saving changes must be handled automatically.

A payment changes to paid only after server-side verification and reconciliation, not just because a user returned from checkout.

The same webhook or CSV import must never create duplicate financial records.

Speaking assessment rubric

Each child receives a short, teacher-scored assessment at the beginning and end of the cycle.

Criterion

	

Score




Understanding a simple Gujarati prompt

	

0–3




Producing an appropriate spoken response

	

0–3




Understandability of speech

	

0–3




Confidence and conversational participation

	

0–3




Total

	

0–12

The teacher should use the same rubric at both assessments and include brief observational notes. The founder can review consistency, attendance and parent feedback, but should not pretend to independently assess Gujarati speaking proficiency.

Should teachers have their own login?

Agree — yes, but limited to assigned work.

A teacher's dashboard should show their upcoming classes, assigned learners' preferred names, relevant levels, attendance entry, notes and assessment forms.

Teachers must not see full parent contact databases, advertising results, payment information, unrelated batches, other teachers' records, or financial settings. A teacher cannot create a new account or select the teacher role themselves; an administrator must invite and authorize the account.

Full teacher access is required before live classes, but the complete teacher management portal does not need to be finished before the first parent pays.

Dashboard KPIs

The founder's main dashboard should prioritize:

Paid test target

10
Unrelated paying families

CAC ceiling

₹600
Per paying family

Attendance target

80%
Across scheduled classes

Renewal target

5
Paid month-two advances
These are pilot targets, not actual operating results.

The dashboard must also show collected revenue, outstanding fees, teacher payment liabilities, campaign spending and contribution by batch.

Using the previously agreed example, one full batch produces ₹12,000 revenue and approximately ₹2,975 first-cycle contribution after the assumed acquisition and delivery costs, before fixed overhead.

The earlier estimate of 30 children breaking even is a steady-state scenario that assumes only one-third need replacing each cycle. It is not first-month break-even when all 30 students have to be acquired.

5. Technology stack and architecture

Verdict: Agree with Next.js, TypeScript, Tailwind and Vercel. Disagree with MongoDB Atlas as the default database for a brand-new implementation.

My preferred stack is:

Next.js App Router + TypeScript + Tailwind CSS

Public website · Founder admin · Restricted teacher portal

Server Actions + Route Handlers

Validation · Authorization · Payments · Consent · Business rules

Supabase

PostgreSQL · Auth · Row-level security · Backups

Vercel Pro

Hosting · SSL · Deployment · Runtime

Razorpay

Payment links · International cards · Webhooks

Resend

Transactional emails · Notifications

Manual integrations initially

Google Meet · WhatsApp Business · Meta Ads Manager

Class delivery · Parent communication · Advertising
Why PostgreSQL rather than MongoDB?

The proposed system has relationships between families, children, enrolments, batches, sessions, assessments, invoices and payments. PostgreSQL naturally supports foreign keys, transactions, uniqueness constraints and financial reconciliation.

Supabase also provides an established authentication service, reducing the amount of custom authentication code.

MongoDB Atlas is still a valid choice. If Claude Code already has a tested MongoDB implementation, I would not insist on rewriting it. In that case, use strict schema validation, unique indexes, appropriate transactions and verified backups.

For a new project with no existing code, I prefer Supabase PostgreSQL because its structure better matches this business.

Verified third-party pricing

Official vendor information checked 10 November 2026. High confidence in published base prices; account-specific eligibility, taxes and future pricing remain unconfirmed.

Service

	

Recommended tier

	

Published price




Next.js, TypeScript, Tailwind

	

Open-source stack

	

$0 license




Vercel

	

Pro, one deploying seat

	

$20/month, plus possible usage/taxes 
Vercel




Supabase

	

Free for development; Pro preferred for production

	

Free $0; Pro from $25/month 
Supabase




MongoDB Atlas, if retained

	

Flex for low-traffic production

	

Approximately $8–30/month, usage dependent 
MongoDB Docs




Resend

	

Free transactional email

	

$0, 3,000 emails/month, maximum 100/day 
Resend




Razorpay

	

Standard international-card payments

	

Published 3% platform fee; applicable GST additional 
Razorpay




Google Meet

	

Personal-account free meetings

	

Up to 60 minutes for groups of three or more 
Google Meet Help




WhatsApp Business

	

Manual app and click-to-chat

	

No Cloud API integration initially




Domain

	

Commercial registrar

	

Price and availability to confirm

Important hosting correction: Vercel Hobby is restricted to non-commercial personal use. A paid education business should use an appropriate commercial plan, such as Pro. 
Vercel

At full recommended tiers, Vercel Pro plus Supabase Pro has a published base cost of $45/month, before applicable taxes, extra usage or domain costs.

The earlier pilot allocated only ₹1,500 for landing-page and tools costs. This budget line is not sufficient to assume both paid services are covered. The total ₹25,000 pilot cap must be recalculated before approving paid infrastructure.

Supabase Free is an option during development, but its published limitations include project pausing after a week of inactivity. Pro includes daily backups. For a real service handling children's information, I prefer a maintained paid production database rather than relying on free-tier behavior. 
Supabase

Classroom platform decision

Use Google Meet for the pilot after verifying the host account's access controls. Forty-five-minute lessons fit within the published 60-minute group limit for eligible free Meet use.

Do not use Zoom Basic for the 45-minute sessions: its published meeting limit is generally 40 minutes. 
Zoom

Each batch should have a secure meeting reference. Keep the link in authenticated staff systems and send it only to the enrolled guardians and assigned teacher. The meeting provider should enforce joining controls.

Payment architecture

Razorpay Payment Links are suitable for the first version because the founder can collect payment without building a custom card checkout. Razorpay advertises international payment links, but foreign-card acceptance requires merchant approval, so feasibility must be established before live enrolment. 
Razorpay
+1

The payment process should be:

Founder approves an enrolment offer and creates a payment request.

Razorpay generates the payment link.

The admin stores the gateway link ID and the expected amount/currency.

A verified Razorpay webhook confirms payment.

The system marks the enrolment paid, records an invoice/receipt according to the approved accounting process, and triggers the welcome email.

Failed, expired or refunded payments remain separately identifiable.

Webhook handlers must verify authenticity, handle duplicate deliveries and avoid assuming events arrive in order. Razorpay documents at-least-once delivery and recommends idempotency based on event identifiers. 
GitHub
+1

Do not store payment card details or gateway secrets in the browser.

Maintenance and security requirements

Claude Code should implement this as one Next.js application, not microservices. Use stable libraries, database migrations, environment variables, role-based authorization, validation, rate limiting, error logging and automated tests.

Every deployment should run linting, type checks, tests and a production build. Create a staging environment without real child records. Require multi-factor authentication for the founder's administrator account, test backups and restoration, and keep an audit trail for sensitive changes.

6. Implementation phases for Claude Code

Verdict: Agree — implementation must be divided into small independently verifiable sessions.

Each phase should modify no more than approximately eight files, including tests and migrations. If the work does not fit, split it; do not omit testing to satisfy the file limit.

Proposed build schedule

Phase

	

Deliverable

	

Gate




0

	

Finalize specification, branding assumptions, project structure, hosting constraints

	

Before payment




1

	

Next.js project, UI design tokens, navigation, fonts, responsive layout

	

Before payment




2

	

Home, program and how-it-works pages, basic SEO

	

Before payment




3

	

Pricing, FAQ, safety and contact pages

	

Before payment




4

	

Legal pages, privacy preferences and consent controls

	

Before payment




5

	

Database schema, migrations, authentication and authorization tests

	

Before payment




6

	

Parent enquiry form, field validation, source attribution and confirmation emails

	

Before payment




7

	

Founder CRM pipeline, notes, follow-up dates and lead search

	

Before payment




8

	

Family/child profiles, parental consent records, privacy permissions

	

Before payment




9

	

Teacher records, batch allocation, capacity enforcement

	

Before payment




10

	

Batch cycles, scheduled sessions and timezone handling

	

Before payment




11

	

Razorpay payment-link generation and admin payment tracking

	

Before payment




12

	

Payment webhook verification, idempotency, reconciliation and invoice foundation

	

Before payment




13

	

UTM builder, campaign register, daily spend and basic CAC reporting

	

Before paid ads




14

	

Security tests, mobile QA, accessibility, staging review and production launch checklist

	

Before payment




15

	

Restricted teacher login and assigned-session screen

	

Before first class




16

	

Attendance, absence reporting and teacher notes

	

Before first class




17

	

Baseline/endline rubric and progress summaries

	

Before first class




18

	

Teacher payouts, renewal advances and finance reconciliation

	

During pilot




19

	

Contribution per batch, break-even and cohort reporting

	

During pilot




20

	

CSV ad imports, consent-based Pixel/CAPI events and extended analytics

	

After validation




21

	

Optional Meta/Google API integrations, improved automations and parent portal

	

After validation

These are deliverable boundaries rather than promises that an entire phase can always be completed in a single attempt. Some phases, especially the database and payment work, may need subdivision to maintain the eight-file constraint.

Required verification gates

Before accepting the first payment, demonstrate a complete test journey with sample data:

An ad-tagged enquiry creates exactly one CRM lead, retaining campaign attribution.

A founder can qualify the lead and assign a compatible batch without exceeding its capacity.

Family information is inaccessible to unauthenticated users and unrelated staff.

A simulated successful payment updates the enrolment once, even if the webhook is delivered twice.

Failed payments and refunds do not appear as collected revenue.

Child data cannot be submitted without the required guardian-consent workflow.

No marketing Pixel fires when marketing consent has been rejected.

Dubai and India schedule displays agree on the same actual class time.

The public site works on mobile, publishes accurate fees and policies, and passes basic accessibility checks.

Before the first class, verify the teacher can log in, access only their assigned batch, mark attendance and record an assessment. Test meeting admission controls and backup-teacher reassignment.

Every completed phase should produce: a short change summary, modified-file list, migration record where relevant, test results, screenshots of applicable screens and any unresolved risks. Claude Code should not mark a phase complete while relevant tests fail.

Production release policy

Use a protected main branch and separate staging deployment. Keep credentials out of Git. Production changes should require passing tests, and database migrations must have a documented rollback or recovery procedure.

This creates a repeatable workflow the founder can manage without debugging complex infrastructure.

7. Compliance, child safeguarding and financial policies

Verdict: Agree — these requirements must be built into the first release. Several are launch blockers, not later enhancements.

India: DPDP Act 2023 and Rules 2025

India's Digital Personal Data Protection Act, 2023 and the notified DPDP Rules, 2025 are relevant because the business operates from India.

The rules were notified in November 2025 with phased commencement. Several substantive obligations, including children's verifiable parental-consent requirements, are scheduled for the later commencement period around May 2027. Design for them now rather than relying on the transition window. 
MeitY
+1

The application should keep a versioned record of the privacy notice, consent purpose, guardian verification method and withdrawal status. A simple unchecked/checked consent field alone must not be assumed to satisfy every legal requirement for verifiable parental consent.

UAE: launch-market requirements

UAE Federal Decree-Law No. 45 of 2021 (Personal Data Protection Law) is relevant to handling customer information from the UAE.

There is also an important additional rule: UAE Federal Decree-Law No. 26 of 2025 on Child Digital Safety. Official UAE guidance states that collecting or using personal data from children under 13 requires the applicable safeguards, including clear parental consent, withdrawal capability, a stated purpose and restrictions on targeted advertising involving children's data. Educational-service exemptions may exist under specific legal conditions, but they must not be assumed automatically. 
U.AE
+2

For this UAE-first service, use parent-controlled enrolment and obtain appropriate verified consent before creating operational child profiles.

UK expansion

When actively serving UK families, assess UK GDPR, the Data Protection Act 2018 and the Information Commissioner's Children's Code. The ICO explains that the code can apply to education-related online services likely to be accessed by children, including providers outside the UK. 
ico.org.uk
+1

Conduct an appropriate privacy-impact assessment before launching direct UK child-facing functionality.

United States expansion

For American families with children under 13, assess the Children's Online Privacy Protection Act and Rule (COPPA). Requirements can include parental notice, verifiable consent, access/deletion rights, security and data minimization. 
Federal Trade Commission

Do not enable a US-targeted enrolment campaign solely by adding USD pricing. Complete the market-specific legal review first.

Safeguarding rules to implement

Requirement

	

Implementation




Parent-controlled enrolment

	

Guardian authorization before collecting child learning details




No child direct messaging

	

All logistical communication goes through the parent




No private teacher-child contact

	

No private WhatsApp, email or unsupervised messaging




Safe video classes

	

Controlled admission, approved participants and restricted meeting links




No recording by default

	

Disable recording and screenshots as part of teacher operating rules




Class supervision

	

Parent present for initial setup; documented safeguards for one-to-one situations




Teacher verification

	

Founder confirms identity, references and suitability before activation




Substitutes

	

Only pre-approved backup teachers may access classes




Restricted learning notes

	

Teacher can view only assigned learners' necessary information




Incident handling

	

Restricted report, escalation procedure, responsible adult and audit trail




Privacy requests

	

Guardian can request access, correction, withdrawal or deletion as applicable

Do not collect a child's full date of birth, home address, school details, ID documents or photograph unless a defined operational or legal need is established. For this pilot, age in years and age band should be enough.

The retention policy should distinguish educational records from invoices and statutory financial records. Delete or anonymize unnecessary learning information when it is no longer required, while retaining records that must legally be kept.

Refund and cancellation policy

Proposed policy for legal review, not yet an agreed commercial term:

Scenario

	

Proposed treatment




Required batch does not form by the promised deadline

	

Full refund or guardian-approved alternative




Parent cancels sufficiently before the first class

	

Full refund under a clearly disclosed cutoff




Business cancels a class

	

Reschedule with agreement or refund the undelivered lesson




Child misses a class

	

Offer a makeup opportunity when feasible under the disclosed policy




Parent withdraws mid-cycle

	

Clearly stated treatment of undelivered classes, consistent with applicable consumer law




Month-two ₹500 advance

	

Credited toward the next fee; refund conditions disclosed before collection

I suggest an initial 48-hour pre-class cancellation cutoff, subject to legal review and parent feedback. Do not use vague statements such as "all payments non-refundable."

Also publish a complaint-response process, a delivery-of-services policy, and support contact details.

GST, invoices and payments from abroad

This item requires a chartered accountant before launch.

Indian GST law provides a zero-rated framework for qualifying exports of services, but whether this specific tutoring arrangement qualifies requires confirmation of the statutory conditions, including location of supplier and recipient, place of supply, payment realization and the relationship between the parties. Export status must not be assumed merely because a parent lives abroad. 
taxinformation.cbic.gov.in
+1

The system should therefore support configurable tax treatment rather than hardcoding zero GST.

Invoices should record seller identity, invoice number and date, recipient information where required, service description, amount, currency, applicable tax treatment and the relevant payment reference. Actual foreign-currency settlement and gateway charges must be reconcilable.

The founder must also confirm which legal form and KYC documentation the chosen payment provider will accept. A private limited company may not be necessary for a small test, but that does not mean an unverified individual automatically qualifies for international-card processing.

Final implementation recommendation

I would approve the VaatKadi-style branded website with a single founder admin and restricted teacher portal, built around the full data architecture described above.

I would not approve building the advanced ad-management API integration, a student-facing app, or a large parent portal during the first paid test. Those add cost and risk without addressing the primary uncertainty: whether unrelated Gujarati families abroad will pay and renew.

The first production release is successful when a parent can discover the service, enquire, speak to the founder, be matched into a suitable group, pay safely, and receive the correct class schedule—and when the founder can account for every lead, payment and class.

Points still open

1. Final brand and domain: Select one of the proposed names, confirm native Gujarati pronunciation, complete trademark checks and purchase an available domain.

2. Legal seller and payment approval: Confirm the merchant's legal identity, bank account, Razorpay KYC, international-card approval, accepted currencies and settlement terms.

3. Pilot pricing: Decide whether the UAE price will be a fixed AED amount or an INR charge with a displayed AED estimate. Recalculate margins using actual expected settlement.

4. Production budget: Confirm whether the ₹25,000 overall test cap remains strict. It must cover the chosen hosting/database tiers, payment charges, contingency and any external development costs.

5. Batch policy: Decide whether a group requires five paid children or may begin with four, the reservation deadline, refund cutoff and make-up lesson rules.

6. Safeguarding and consent: Obtain review of the parental verification method, teacher safeguards and privacy policies for the UAE-first model.

7. Teacher and classroom readiness: Founder to provide verified teacher details, confirmed per-session quotes, available time slots, backup arrangements and the approved meeting-host setup.

8. Unproven business assumptions: Real cost to acquire paying families, willingness to pay versus lower-cost community classes, attendance, and renewal conversion remain unknown until the pilot runs.

Final position: Agree with the startup direction and core system, with the modifications and conditions above. The plan is suitable as an implementation specification for Claude Code; it is not evidence that the business is validated or that payment and regulatory approvals have already been obtained.


---

## Claude Code - 2026-11-10 08:54 UTC - 02_claude.md - attachments: none

# Round 2 - Claude Code's verdicts, the founder's decisions, and verified facts

Strong reply. I checked your numbers (Rs 12,000 / Rs 2,975 per batch; your note that 30 children is a
steady-state break-even, not first-month, is correct) and ran four research passes (hosting, payments,
UAE law, third-party limits). Below: founder decisions first, then per point agreed / rejected / open.
Please reply so that Claude Code can turn your answer directly into a locked build spec.

## Founder decisions received after your reply (binding)
1. Teachers: the founder recruits them. No recruitment funnel needed; teacher records, agreements,
   availability, assignments and payouts are needed.
2. Video: founder leaves the choice to Claude Code -> Google Meet (free personal account: 60 minutes for
   3+ participants on a computer; Zoom Basic stops at 40 minutes). One fixed Meet link per batch, stored
   in the admin, sent only to enrolled parents and the assigned teacher.
3. Hosting: **Netlify, not Vercel.** Verified: Netlify Free allows commercial use (Self-Serve Agreement
   s.5, updated 4 Nov 2026; AUP item 13 only requires card data to be collected by a PCI-DSS provider -
   hosted checkout is fine); custom domain + free Let's Encrypt HTTPS on Free; Next.js 16 App Router, route
   handlers, middleware supported via the OpenNext adapter; synchronous functions 60 s, scheduled
   functions 30 s. Risk: Free = 300 credits / month hard cap (production deploy = 15 credits) and when
   credits run out ALL sites pause, including the payment webhook endpoint -> move to Personal
   (USD 9 / month, 1,000 credits, auto-recharge) before taking real payments. Netlify security advisory
   3 Nov 2026: next >= 16.4.5 with adapter >= 5.16.6.
4. Payments: the founder is an individual today. Verified: Razorpay "Individual" accounts must use
   PayPal for international payments; international cards need a registered business (sole
   proprietorship: any 2 of Udyam, GST, Shop & Establishment, IEC, postpaid bill), then bank approval
   (reply within 5 working days; if rejected, reapply after 90 days). Plan:
   - Stage A (first payment within 7 days): **PayPal India Business account as "Individual"** (PAN +
     Aadhaar + video KYC). Guest card checkout; Orders / Invoicing API with webhooks. **AED is not a
     PayPal currency** -> UAE parents pay in USD (AED is pegged at 3.6725 per USD). Fees 4.40% + USD 0.30
     + 3.0% conversion = about 8.5-9.5% all-in on USD 25-30. Purpose code P1107 (educational services).
     Free monthly digital FIRA.
   - Stage B (2-3 weeks): founder registers Udyam (free, same day) + Gujarat Shops & Establishments
     Form D intimation (Form E receipt, online) -> **Razorpay** sole-proprietor account with international
     cards; Payment Links + webhooks (payment_link.paid, .cancelled, .expired); 3% + 18% GST on the fee;
     AED supported; automatic e-FIRA. Cashfree (2.99%) is the fallback.
   - Ruled out (verified): Payoneer (no consumer payers), Wise (no card acceptance for India), Skydo
     (B2B, USD 9 minimum), Lemon Squeezy / Paddle / Dodo (prohibit human services), Outschool (teachers
     must live in listed countries), Teachable (needs Stripe; Stripe India invite-only).
   -> The system needs a **provider-agnostic payment model** (paypal, razorpay, manual bank transfer).
5. Laws: the founder asked that the UAE laws be verified and implemented. Findings (law-firm notes +
   official texts of Decree-Law 14/2023 and Res. 66/2023 read in full):
   - **Applies:** PDPL 45/2021 (Art 2(1)(c) reaches controllers outside the UAE; executive regulations
     still not issued; no adequacy list - transfer to India on contract necessity + express consent,
     Art 23). **E-commerce law 14/2023** (Art 2(1)(b) covers trading received from outside the UAE):
     publish prices, fees, T&Cs; seller identity, address, phone, website; complaint channel with
     tracking; a public rating box; customer chooses marketing channel; an electronic detailed invoice
     per purchase; refund when the service is not as described / defective / too late; no arbitration
     clause under AED 50,000; no sharing consumer data without consent. **Child Digital Safety
     Decree-Law 26/2025** (likely for the under-13 data rule; in force 1 Jan 2026, compliance about
     1 Jan 2027): explicit, documented, verifiable parental consent before collecting a child's data,
     quick withdrawal, access limited to authorised staff, no targeted ads / tracking of children.
   - **Does not apply directly (use as the standard):** Consumer Protection Law 15/2020 (excludes
     foreign e-commerce sellers), TDRA spam policy and telemarketing Res. 56/2024 (we still follow:
     opt-in only, calls 09:00-18:00, messages 07:00-21:00 UAE time, opt-out within 24 h), Advertiser
     Permit (own-page ads exempt), Private Teacher Work Permit (tutors live in India).
   - **Open for a lawyer / tax adviser:** KHDA / ADEK position; UAE VAT on live classes (leaning outside
     scope; recorded content would need UAE VAT registration from the first sale - so live classes only);
     whether "Gujarati heritage" data counts as sensitive (ethnic origin).
   - Cybercrime Law 34/2021 Art 44: recording / publishing a person's image or voice without consent -
     AED 150,000-500,000. Recording stays off.
6. Admin: the founder wants to manage **everything** from the admin panel - all management and
   scheduling.
7. Build: plan with you, then Claude Code builds it completely.

## Point 1 - Brand: agreed, one check
Claude searched the exact names on 10 Nov 2026: no business, app or social identity found for
VaatKadi, GharVaat or VaatoNest. Your palette and fonts are agreed. Open: give the literal meaning of
"વાતકડી" word by word, whether a native speaker would find it natural or odd, and any unwanted meaning.
The founder does not speak Gujarati, so we will also ask the teachers - but choose one final name and one
backup now.

## Point 2 - Website: agreed, with three changes
- Pages: agreed. Add **/imprint** (seller identity per e-commerce law Art 6(8)-(9)), **/complaints**
  (form -> ticket ID -> status page by ticket ID + email) and a **feedback / rating** box.
- Reserve-then-pay flow: agreed.
- Price: AED 99 at 25.6-25.9 INR per AED (early Nov 2026 reference rates) is about Rs 2,535-2,565 gross;
  after Razorpay's 3.54% about Rs 2,445-2,475 - keeps the Rs 2,400 model. Under PayPal (USD, about 9%
  all-in) AED 99 = USD 26.96 would net about Rs 2,320. Propose the Stage-A USD price and the rule for
  showing "AED 99 (charged as USD xx)".

## Point 3 - Ads: agreed
UTM builder, campaign register, manual daily spend, CSV import with dedup, CPL / CAC / ROAS, pixel only
after consent, never child data to Meta. Verified: reading your own ad account's insights needs only
standard ads_read access without App Review; Conversions API for your own pixel needs no App Review.
I could not verify your "Marketing API Access Tier, May 2026" rename - out of scope for v1 anyway.

## Point 4 - Admin: agreed, but extend for "manage everything"
Please add the concrete design for:
1. **Scheduling engine**: a batch has a weekly pattern (e.g. Mon + Thu 17:30 Asia/Dubai); "generate cycle"
   creates exactly 8 sessions, skipping founder-entered holidays; reschedule one session; assign a
   substitute; teacher double-booking detection across batches; every time shown in parent zone, India
   zone and the viewer's zone; a calendar (week / month) view for the founder and a list for teachers.
2. **Communications**: email templates (welcome, schedule, reminder 24 h + 1 h before class, payment
   link, receipt, renewal invite) sent through a transactional provider; WhatsApp = pre-filled wa.me
   links opened by the founder and logged as activities (no WhatsApp API in v1). A send-window guard and
   the marketing suppression list are checked before any marketing message.
3. **Tasks / follow-ups**: due-today list on the dashboard.
4. **UAE-law modules**: consent ledger (purpose, wording version, timestamp, IP, channel, withdrawal),
   rights inbox, complaints with ticket tracking, breach register, retention settings, receipts.
5. **Payments**: provider enum (paypal, razorpay, manual), stored fees, FX and INR settlement, idempotent
   webhooks for both providers, manual payment entry with proof reference.

## Point 5 - Stack: partly rejected
- Hosting: rejected Vercel - founder decision 3 (Netlify).
- Database: **rejected Supabase / PostgreSQL** for this founder. Reasons: (1) the founder's known stack is
  TypeScript + MongoDB, and the founder's standing rule is "prefer the boring, standard approach I can
  debug"; PostgreSQL is listed as unfamiliar; (2) Supabase Free pauses after a week of inactivity;
  (3) you wrote that MongoDB Atlas is valid with strict schema validation, unique indexes, transactions
  and backups. Atlas M0 free: 0.5 GB, 500 connections, replica set (transactions available), paused only
  after 30 days with no connections, no automated backups. Please give the MongoDB version of your
  model: collections, embedded vs referenced documents, the exact unique / compound indexes that enforce
  your integrity rules (5 paid seats per batch, one active enrolment per child per cycle, unique gateway
  ids, idempotent webhooks, CSV dedup), which writes need a multi-document transaction, and the backup
  plan on M0 (or when to move to a paid tier).
- Auth: Claude proposes **Better Auth** (email + password, TOTP two-factor for the founder, admin-invited
  teacher accounts, roles super_admin / teacher) with its MongoDB adapter, instead of hand-written auth.
  Agree or name a better boring option.
- Email: Resend free (3,000 / month, 100 / day) - agreed.

## Point 6 - Phases: open
22 phases is too many for a founder who wants the complete system. Consolidate into **at most 8 phases**,
each a demo-able unit Claude Code can build and verify in one session (generated framework files do not
count against the ~8 hand-written-file guideline; tests do). Mark which must be live before the first
paid family, which before the first class. Each phase needs 3-5 binary acceptance checks.

## Point 7 - Compliance: agreed, merge the UAE findings above
Turn the UAE findings into product requirements in the data model and pages. India DPDP: design now for
verifiable parental consent (core rules from 13 May 2027).

## What I need in this reply
A. Final brand name + backup, with the meaning check.
B. The MongoDB data model (collections, fields, enums, indexes, transactions).
C. The scheduling engine and communications design above.
D. At most 8 phases with acceptance checks and the before-payment / before-class marks.
E. The Stage-A USD price rule.
F. Monthly running cost at test scale with Netlify Personal, Atlas M0, Resend free, Google Meet free,
   PayPal then Razorpay.
End with the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-10 09:07 UTC - saved as 02_chatgpt.md

ChatGPT said:
C1 Startup — Round 2 Final Planning Response

10 November 2026 · Technical decisions for Claude Code

Overall verdict: Agree with the founder's decisions, with implementation safeguards and several important corrections.

This response is intended to become the implementation specification for the Gujarati children's online conversation-class startup.

The accepted technology direction is:

Brand: VaatKadi, with VaatoNest as backup.

Hosting: Netlify Personal for production.

Application: Next.js App Router, TypeScript and Tailwind CSS.

Database: MongoDB Atlas, initially Free (M0).

Authentication: Better Auth with restricted teacher access.

Payments: PayPal first, Razorpay after merchant approval, with manual bank transfer available.

Classes: Google Meet, eight 45-minute sessions per cycle.

Communications: Resend for email; manual WhatsApp Business initially.

No teacher-recruitment marketplace, student mobile app, advanced ad-management API or general-purpose LMS is required.

The founder should manage all routine operations through the admin panel without editing source code, database records or deployment settings.

1. Brand — Agree, with a naming qualification
Final name: VaatKadi — વાતકડી

Decision: Select VaatKadi. Backup: VaatoNest.

The intended Gujarati word construction is:

Part

	

Gujarati

	

Meaning




Vaat

	

વાત

	

Conversation, talk or something being said




Kadi

	

કડી

	

Link, connection or a link in a chain




VaatKadi

	

વાતકડી

	

An invented compound intended to mean a link through conversation

The full name is a coined brand word, not an established dictionary word that I can verify.

It should be understood as connecting families through conversation, not as the literal translation of a familiar Gujarati phrase.

My concern is that some native speakers could find it slightly unusual. The pronunciation is roughly Vaat-ka-di, with the last part corresponding to કડી, not કઢી (the Gujarati dish).

I have not found a clearly established offensive meaning, but a web search cannot confirm how the name feels to Gujarati speakers. Ask at least three native speakers, preferably including teachers and parents, whether the meaning is intuitive and pleasant.

The backup, VaatoNest, combines vaato (conversations) with nest (a warm place of belonging). It is more immediately international but less distinctly Gujarati.

Brand approval rule: Proceed with VaatKadi as the working name. Before buying the domain or finalizing printed assets, complete the native-speaker, trademark and domain checks. The absence of an obvious exact-match business online is not trademark clearance.

Locked identity direction

Positioning: Live Gujarati conversation classes for children growing up abroad.

Tagline: From “Kem cho?” to real conversations at home.

Primary color: Deep teal #163A4A.

Secondary colors: Marigold #F4A340, heritage teal #228F83, warm cream #FFF8EE, soft clay #E5C7B5.

Fonts: Plus Jakarta Sans for English and Noto Sans Gujarati for Gujarati.

Voice: Warm, credible, respectful, parent-focused and never exaggerated.

No fabricated testimonials, guaranteed fluency claims, artificial enrolment counters or invented teacher credentials.

Status: Agreed for implementation; native-language and legal clearance remain open.

2. Website — Agree with all three changes
2.1 Additional public pages

Add the requested pages to the previously agreed website structure.

Route

	

Exact purpose




/imprint

	

Legal seller name, operating address, business status, applicable registration/licence details, phone, support email and website




/complaints

	

Complaint form, acknowledgement, ticket number and follow-up instructions




/complaints/track

	

Complaint status lookup using ticket number plus verified parent email/one-time verification




/feedback

	

Genuine experience ratings and feedback, with privacy controls

The complaint tracking page must not reveal information based on a ticket number alone.

Use an unguessable public tracking token or ticket ID together with a verified email/one-time code. Rate-limit attempts. Never display children's names, private teacher notes or other personal details publicly.

2.2 Public rating box

Agree to implement an authentic rating feature.

Use the following data fields:

feedbackId, familyId, parentVerified, overallRating (integer 1–5), feedbackText, publicationConsent, moderationStatus, submittedAt, publishedAt.

Moderation statuses:

pending, approved, rejected_privacy, rejected_abuse, withdrawn.

Only genuine customers should be described as verified customers. Publishing is optional and separate from submitting feedback.

The public page may initially say “No customer reviews yet” and allow feedback. Never pre-populate five-star ratings, suppress genuine negative feedback simply because it is negative, or publish identifiable child information.

The UAE's e-commerce legislation includes provisions concerning an experience-rating mechanism, complaint channels, merchant identification and detailed electronic invoices. These features are therefore appropriate for the UAE-first website. 
Ministry of Economy and Tourism UAE

2.3 Reservation before payment

Agree with the sequence:

Parent enquiry → introductory call → level check → matching batch → conditional reservation → payment → confirmed place → welcome.

The platform should distinguish:

reserved: A temporary offer has been made.

payment_pending: Parent has received checkout instructions.

paid: Payment was verified.

active: Enrolment has entered a running class cycle.

Set reservationExpiresAt when offering a place. If a reservation expires, release the held seat automatically.

Do not charge for an unconfirmed group without displaying the batch-formation deadline and the applicable refund rule.

2.4 Stage-A USD price — modified proposal

Decision: Charge USD 29.00 per child for the eight-class cycle during PayPal Stage A.

Do not advertise AED 99 while actually charging USD 29. That would be misleading because USD 29 is approximately AED 106.50, not AED 99.

STAGE A — PAYPAL PRICE

$29.00

USD / child / 8 classes

Approximately AED 106.50

Actual card charge is USD 29. The AED figure is an estimate; the payer's bank may apply its own exchange rate or fees.
🇺🇸
US Dollar
$
🇦🇪
UAE Dirham
AED

The UAE dirham is pegged to the US dollar at approximately 3.6725 AED per USD. The Central Bank of the UAE publishes official intervention rates around this parity. 
Domestic Market Operations

PayPal unit economics

PayPal India's published international receiving fee is 4.40% plus USD 0.30 per transaction, with a 3% conversion spread for converting received balances into another currency in the applicable case. 
PayPal IN

Using the illustrative USD/INR reference of ₹93.3767 on 10 November 2026:

Item

	

Approximate value




Parent pays

	

$29.00




Gross INR equivalent

	

₹2,708




PayPal transaction fee

	

$1.58




Assumed conversion spread

	

$0.82




Approximate net receipt

	

₹2,484




Total effective payment cost

	

₹224

This is a modelling estimate, not a guaranteed settlement quote. Applicable taxes, provider-specific adjustments and actual PayPal exchange rates must be checked using the merchant's own transactions.

Why $29 rather than $27? USD 27 is approximately AED 99, but at the reference exchange rate and fee assumptions it nets only about ₹2,311. USD 29 leaves a modest buffer above ₹2,400 net.

Stage-B pricing

After Razorpay approves international-card payments:

Charge AED 99 if direct AED charging is supported and approved.

Disclose the actual currency on the payment screen.

Preserve the original price agreement for an already-paid cycle.

Notify parents before applying a changed price on renewal.

Keep each price in pricePlans with provider, currency, amountMinor, effectiveFrom, effectiveTo and version.

There should be no automatic price switch during a live billing cycle.

Payment-provider warning

PayPal officially supports a Business Individual classification for unregistered Indian service providers and offers PayPal-hosted guest card checkout, but actual onboarding, verification and guest-checkout presentation depend on account approval and other conditions. 
PayPal IN
+2

Stage A is an implementation path, not a guarantee that a live merchant account will be approved within seven days. International payment acceptance must be tested successfully before advertising enrolment as payable.

Status: Agreed, with USD 29 for Stage A and AED 99 as the proposed Stage-B rate.

3. Advertising system — Agree

Decision: Keep advertising execution in Meta Ads Manager and Google Ads, with performance tracking and operational control in the VaatKadi admin panel.

The first version should contain /admin/campaigns, /admin/campaigns/new, /admin/campaigns/[id], /admin/ad-spend, and /admin/reports/acquisition.

Campaign and tracking model

campaigns should contain:

_id, name, platform, externalAccountId?, externalCampaignId?, targetCountry, objective, budgetMinor, currency, landingPath, status, startDate, endDate?, utmConfig, createdAt.

Statuses: draft, active, paused, completed, archived.

The UTM builder must create URLs with source, medium, campaign and content parameters. Store first-touch and last-touch attribution on the lead without storing child information in advertising records.

The founder can enter daily spend manually or import platform CSV reports. Use one canonical spend record per campaign per day; later imports replace or reconcile that record, rather than adding it again.

Report CPL, CAC_per_family, CAC_per_child, lead_to_paid_rate, collected_revenue, ROAS, and contribution_after_acquisition.

Keep CAC_per_family and CAC_per_child separate because one family may enrol more than one child. The pilot's ₹600 target concerns acquiring one paying family.

For later Meta Pixel or Conversions API usage, track only appropriately consented adult-side conversions. Never transmit child names, levels, assessments, attendance, dates of birth or classroom identifiers.

Claude's statement about own-account ads_read access may be sufficient for an eventual integration, but that should be rechecked against the Meta application configuration when the feature is actually built. No API access is required for v1.

Status: Agreed. Manual and CSV campaign tracking are in scope; direct ad purchasing and automated API management are deferred.

4. Admin panel — Agree, with the complete extensions

Decision: The founder should control the operating workflow from one admin panel, including scheduling, payments, communications, teacher assignments, reporting and complaints.

4.1 MongoDB document model

I accept MongoDB Atlas as the project database because the founder's implementation environment is already TypeScript/MongoDB-oriented.

Use MongoDB ObjectId for application document references, Date for UTC timestamps, integer minor units for money, IANA timezone strings, and runtime validation with Zod. Better Auth manages its own user/session identifiers, which application staff records will reference using their actual adapter-compatible type.

Embed small bounded information used with its parent document. Reference growing histories and independently managed entities.

Collection

	

Required fields and relationship

	

Status values




leads

	

parentName:string, emailNormalized:string, phoneE164:string, country:string, timezone:string, ageBand:string, initialLevel:string, firstTouch:object, lastTouch:object, campaignId:ObjectId?, nextActionAt:Date?, status:string

	

new, contacted, call_booked, qualified, waitlisted, payment_pending, won, lost, do_not_contact




leadActivities

	

leadId:ObjectId, type:string, note:string, actorId:string, occurredAt:Date, channel:string

	

Types: call, email, whatsapp_draft_opened, whatsapp_sent_confirmed, note, status_change




families

	

primaryGuardian:object, additionalGuardians:object[], country:string, timezone:string, leadId:ObjectId?, status:string

	

active, paused, inactive




children

	

familyId:ObjectId, preferredName:string, ageYears:number, ageBand:string, level:string, status:string

	

active, paused, inactive




teachers

	

authUserId:string?, name:string, email:string, availability:object[], agreement:object, rateMinor:number, currency:string, status:string

	

pending, verified, active, unavailable, inactive




batches

	

name:string, ageBand:string, level:string, timezone:string, weeklyPattern:object[], primaryTeacherId:ObjectId, backupTeacherId:ObjectId?, capacity:5, meetLinkEncrypted:string, status:string

	

forming, confirmed, active, paused, closed




batchCycles

	

batchId:ObjectId, cycleNumber:number, plannedSessionCount:8, allocatedSeats:number, capacity:5, priceSnapshot:object, startsAt:Date, endsAt:Date, status:string

	

draft, booking_open, confirmed, active, completed, cancelled




enrolments

	

childId:ObjectId, cycleId:ObjectId, familyId:ObjectId, status:string, reservationExpiresAt:Date?, paymentRequestId:ObjectId?

	

reserved, payment_pending, paid, active, completed, cancelled, refunded




sessions

	

cycleId:ObjectId, ordinal:number, startsAtUtc:Date, endsAtUtc:Date, teacherId:ObjectId, status:string, rescheduleHistory:object[]

	

scheduled, completed, cancelled




teacherSlotLocks

	

teacherId:ObjectId, sessionId:ObjectId, slotStartUtc:Date

	

Active locks only




attendance

	

sessionId:ObjectId, childId:ObjectId, status:string, markedBy:string, markedAt:Date

	

present, late, absent_notified, absent_unnotified, excused




sessionNotes

	

sessionId:ObjectId, teacherId:ObjectId, childId:ObjectId?, note:string

	

No status




assessments

	

childId:ObjectId, cycleId:ObjectId, stage:string, rubricVersion:string, scores:object, assessorId:ObjectId, assessedAt:Date

	

baseline, endline




paymentRequests

	

enrolmentId:ObjectId, provider:string, providerOrderId:string?, amountMinor:number, currency:string, checkoutUrl:string?, expiresAt:Date?, status:string

	

created, sent, pending, paid, expired, cancelled




payments

	

paymentRequestId:ObjectId, provider:string, providerTransactionId:string?, grossMinor:number, feeMinor:number?, chargedCurrency:string, settlementInrMinor:number?, fxRate:number?, status:string

	

pending, paid, paid_unallocated, failed, partially_refunded, refunded, disputed




webhookEvents

	

provider:string, providerEventId:string, payloadHash:string, receivedAt:Date, processedAt:Date?, status:string, retryCount:number

	

received, processed, failed, ignored




invoices

	

invoiceNumber:string, familyId:ObjectId, paymentId:ObjectId, sellerSnapshot:object, taxTreatment:string, lineItems:object[], issuedAt:Date?, status:string

	

draft, issued, void, credited




teacherPayouts

	

teacherId:ObjectId, sessionIds:ObjectId[], rateSnapshot:object, amountMinor:number, paymentReference:string?, status:string

	

accrued, approved, paid, disputed




renewals

	

enrolmentId:ObjectId, nextCycleId:ObjectId?, advancePaymentId:ObjectId?, status:string

	

not_due, invited, advance_paid, renewed, declined, expired




tasks

	

ownerUserId:string, leadId:ObjectId?, familyId:ObjectId?, type:string, dueAt:Date, status:string

	

open, completed, cancelled




emailJobs

	

familyId:ObjectId?, templateKey:string, dedupKey:string, scheduledAt:Date, status:string, providerMessageId:string?, attempts:number

	

queued, processing, sent, failed, cancelled




emailTemplates

	

key:string, subject:string, body:string, variables:string[], version:number, active:boolean

	

Active/inactive




consentLedger

	

familyId:ObjectId, childId:ObjectId?, purpose:string, noticeVersion:string, method:string, channel:string, ipEncrypted:string?, action:string, recordedAt:Date

	

granted, withdrawn, superseded




privacyRequests

	

familyId:ObjectId, requestType:string, status:string, requestedAt:Date, resolvedAt:Date?

	

submitted, identity_check, in_progress, fulfilled, rejected_with_reason




complaints

	

ticketCode:string, trackingTokenHash:string, familyId:ObjectId?, type:string, description:string, status:string, openedAt:Date, closedAt:Date?

	

open, acknowledged, investigating, resolved, closed




feedback

	

Verified family reference, rating, publication permission and moderation information

	

As defined in point 2




safeguardingIncidents

	

Restricted incident type, relevant batch/session references, reporter, actions and closure records

	

reported, triaged, escalated, resolved, closed




breachRegister

	

incidentDate:Date, discoveredAt:Date, dataTypes:string[], affectedCount:number?, actions:object[], notificationStatus:string

	

investigating, contained, notified, closed




marketingSuppressions

	

contactHash:string, channel:string, reason:string, createdAt:Date

	

Active




campaigns, campaignDailySpend, adImports

	

Campaign definitions, one daily spend record, CSV hashes/import histories

	

As defined in point 3




settings

	

Business details, payment providers, policies, holidays, retention settings and message windows

	

Versioned




auditLogs

	

actorId:string?, action:string, entityType:string, entityId:ObjectId?, createdAt:Date

	

Append-only

Authentication collections generated by Better Auth should remain under Better Auth's control. Do not manually duplicate passwords or session tokens in application collections.

Small immutable snapshots—such as the price agreed for a cycle, teacher rate for a delivered session and seller details on an invoice—should be embedded. This prevents subsequent setting changes from altering historical financial records.

4.2 Required unique and compound indexes

Claude Code should install indexes using an idempotent initialization script before production traffic is enabled.

JavaScript
// Only one enrolment record per child per cycle.
db.enrolments.createIndex(
  { childId: 1, cycleId: 1 },
  { unique: true }
);

// One numbered cycle per batch.
db.batchCycles.createIndex(
  { batchId: 1, cycleNumber: 1 },
  { unique: true }
);

// Exactly one session record per ordinal.
db.sessions.createIndex(
  { cycleId: 1, ordinal: 1 },
  { unique: true }
);

// No two teacher assignments may reserve the same 15-minute slot.
db.teacherSlotLocks.createIndex(
  { teacherId: 1, slotStartUtc: 1 },
  { unique: true }
);

// Attendance and assessment uniqueness.
db.attendance.createIndex(
  { sessionId: 1, childId: 1 },
  { unique: true }
);
db.assessments.createIndex(
  { childId: 1, cycleId: 1, stage: 1 },
  { unique: true }
);

// Payment-provider references.
db.paymentRequests.createIndex(
  { provider: 1, providerOrderId: 1 },
  {
    unique: true,
    partialFilterExpression: {
      providerOrderId: { $type: "string" }
    }
  }
);
db.payments.createIndex(
  { provider: 1, providerTransactionId: 1 },
  {
    unique: true,
    partialFilterExpression: {
      providerTransactionId: { $type: "string" }
    }
  }
);

// One processing record for each provider webhook event.
db.webhookEvents.createIndex(
  { provider: 1, providerEventId: 1 },
  { unique: true }
);

// One authoritative spend figure per campaign and day.
db.campaignDailySpend.createIndex(
  { campaignId: 1, day: 1 },
  { unique: true }
);

// Prevent re-importing an identical CSV.
db.adImports.createIndex(
  { sha256: 1 },
  { unique: true }
);

// Prevent duplicate scheduled email jobs.
db.emailJobs.createIndex(
  { dedupKey: 1 },
  { unique: true }
);

// Unique public complaint codes.
db.complaints.createIndex(
  { ticketCode: 1 },
  { unique: true }
);

// Efficient operational queries.
db.leads.createIndex({ status: 1, nextActionAt: 1 });
db.sessions.createIndex({ startsAtUtc: 1, teacherId: 1 });
db.tasks.createIndex({ status: 1, dueAt: 1 });
db.emailJobs.createIndex({ status: 1, scheduledAt: 1 });
db.consentLedger.createIndex({ familyId: 1, recordedAt: -1 });

These indexes protect uniqueness, but indexes alone cannot enforce a maximum of five seats per batch. Capacity requires an atomic conditional operation.

4.3 Five-seat integrity rule

Keep allocatedSeats on batchCycles.

When a seat is first reserved, in a MongoDB transaction:

Verify a suitable cycle exists and the child has no enrolment in it.

Atomically update the cycle only if allocatedSeats is less than capacity.

Increment allocatedSeats by one and insert the enrolment.

Commit both changes together.

A payment for an already-reserved seat must not increment the count again.

Expired reservations and authorized withdrawals release seats through a guarded transaction. Repeated cancellation requests must not decrement the counter twice.

If two parents attempt to claim the fifth seat simultaneously, only one should succeed. If money arrives after the reservation has expired or the seat has been released, mark the payment paid_unallocated and offer an alternative or refund. Never create a sixth enrolment.

4.4 Transactions versus single-document operations

Use multi-document transactions for:

Operation

	

Records that must change atomically




Reserve/release a seat

	

batchCycles + enrolments




Confirm captured payment

	

payments + paymentRequests + enrolments + invoice/outbox record




Generate a complete cycle

	

sessions + teacherSlotLocks + cycle state




Reschedule or substitute a teacher

	

sessions + old/new slot locks




Approve a refund

	

Payment/refund records + enrolment state + capacity release if applicable




Approve teacher payout

	

Payout and session-payment ledger




Approve manual bank payment

	

Verification record + payment + enrolment + receipt job

Use single-document atomic operations for ordinary changes to a lead's next-action date, a family's non-sensitive preferences or a task's status.

Do not call PayPal, Razorpay or Resend from inside a database transaction. Record the required external action as an outbox job, commit, then process it separately. This prevents transaction retries from generating duplicate payment links or emails.

MongoDB supports multi-document transactions on replica sets, and Atlas Free uses a three-node replica set; nevertheless, Claude Code must execute a real transaction-and-rollback test against the chosen cluster before accepting it for production. 
MongoDB Docs
+1

4.5 Scheduling engine

Agree with a real scheduling engine, not a manually maintained list of meeting dates.

A batch has a recurring weekly pattern. Example:

JSON
{
  "timezone": "Asia/Dubai",
  "weeklyPattern": [
    { "weekday": 1, "localStart": "17:30" },
    { "weekday": 4, "localStart": "17:30" }
  ],
  "sessionMinutes": 45,
  "targetSessionsPerCycle": 8,
  "capacity": 5
}

weekday follows ISO numbering: Monday = 1 through Sunday = 7.

The scheduling algorithm should:

Start at the selected cycle commencement date.

Generate occurrences from the weekly pattern in the batch's IANA timezone.

Exclude holidays and founder-entered closures.

Generate exactly eight future session records, preserving ordinal numbers 1–8.

Check teacher availability and double bookings before confirmation.

Present a full preview of dates, durations and time zones.

Save the cycle and acquire teacher slot locks only after founder confirmation.

If holidays push the eighth session into a fifth or sixth week, the application must disclose that actual end date. The contractual unit is an eight-class cycle, not an unconditional promise that all sessions finish within 30 calendar days.

Time-zone display

For the example class:

Display context

	

Time




Parent — Dubai

	

Monday, 5:30 PM




Teacher — Navsari

	

Monday, 7:00 PM




Viewer

	

Converted using their saved IANA timezone

Store UTC timestamps as the source of truth; never calculate international time zones using hardcoded numeric offsets.

India and Dubai currently have a 90-minute time difference, but future UK/US expansion needs daylight-saving-aware conversion.

Teacher collision prevention

Require class start times to align to 15-minute increments.

A 45-minute class reserves three consecutive 15-minute slots, using teacherSlotLocks.

The compound unique index on (teacherId, slotStartUtc) prevents the same teacher from occupying overlapping slots. If a mandatory 15-minute buffer is added between classes, reserve four slots instead of three.

On rescheduling, update the original session's date/time and append its previous values to rescheduleHistory. Do not create a ninth active session. Release the old teacher locks and acquire the new locks within the same transaction.

A substitute must already be verified and active. The founder can substitute one session or change the remaining cycle schedule; all affected guardians receive an operational notice.

Calendar views

The founder receives week/month calendar views with batch, teacher, capacity, session status and country-local time.

Teachers receive only their assigned upcoming and completed sessions, with attendance and note-entry actions.

4.6 Communication system

Agree with Resend and manual WhatsApp.

The admin should contain an editable template library with these initial keys:

Template key

	

Trigger




lead_acknowledgement

	

Parent submits enquiry




call_confirmation

	

Founder schedules introduction call




payment_request

	

Founder offers an eligible seat




payment_receipt

	

Successful verified payment




welcome

	

Enrolment confirmed




cycle_schedule

	

Schedule generated or changed




class_reminder_24h

	

24 hours before a session




class_reminder_1h

	

1 hour before a session




class_rescheduled

	

Date/time changes




teacher_substituted

	

Substitute assigned




weekly_progress

	

Approved weekly parent update




renewal_invitation

	

Renewal window opens




complaint_acknowledgement

	

Complaint ticket created




refund_confirmation

	

Refund confirmed

Resend supports idempotency keys for email requests, so each logical email should have a deterministic key based on recipient, template, event and version. Resend's deduplication window is 24 hours, so application-side records must provide longer-term protection. 
Resend

For reminders, create emailJobs with exact scheduled timestamps. A Netlify Scheduled Function should poll due jobs at a short interval, claim a bounded number, send them and record outcomes. Netlify's scheduled functions run in UTC and have a 30-second execution limit. 
Netlify Docs

The dispatcher must tolerate delayed runs and retry temporary failures. The founder dashboard must show failed reminders for manual intervention.

WhatsApp workflow

For WhatsApp:

Generate a prefilled wa.me URL using the parent phone number and approved template.

Let the founder open it from the family or lead record.

Record whatsapp_draft_opened.

Record whatsapp_sent_confirmed only when the founder manually confirms sending.

Opening a WhatsApp draft does not prove that a message was delivered.

Send-window guard

Use Asia/Dubai local time and configurable contact preferences.

As a conservative internal operating policy:

Marketing phone calls: 09:00–18:00 UAE time.

Marketing messages: 07:00–21:00 UAE time.

Marketing only after opt-in, via the selected channel.

Opt-outs immediately suppress further promotional outreach.

These proposed windows are operating rules taken from the Round 2 research, not a claim that every cited UAE telemarketing rule directly applies to an India-based tutoring provider. Essential class-related notifications are separately categorized as transactional.

4.7 Tasks and follow-ups

The admin home page must show:

Leads needing action today.

Introductory calls scheduled today.

Payment requests awaiting response.

Reservations about to expire.

Classes starting soon.

Attendance not yet submitted.

Renewal requests awaiting response.

Open complaints and privacy requests.

Failed reminders and payment reconciliation issues.

Every task needs an owner, due timestamp, linked record, priority, completion status and optional internal note.

4.8 Payment-provider abstraction

Use one provider interface:

TypeScript
type PaymentProvider = "paypal" | "razorpay" | "manual";

interface PaymentGateway {
  createPaymentRequest(input: {
    enrolmentId: string;
    amountMinor: number;
    currency: string;
    idempotencyKey: string;
  }): Promise<{
    providerOrderId: string;
    checkoutUrl?: string;
    expiresAt?: Date;
  }>;

  verifyWebhook(
    rawBody: Buffer,
    headers: Headers
  ): Promise<VerifiedGatewayEvent>;

  getPaymentStatus(
    providerOrderId: string
  ): Promise<GatewayPaymentStatus>;

  refund?(
    providerTransactionId: string,
    amountMinor: number,
    idempotencyKey: string
  ): Promise<GatewayRefundResult>;
}

This is the proposed interface contract; the result types must be defined and validated separately.

The PayPal integration must verify webhook signatures, validate the captured order, compare the expected amount, currency and merchant identity, and distinguish checkout approval from completed capture. PayPal documents webhook signature verification and repeated event deliveries. 
PayPal Developer

Razorpay must verify the webhook signature against the raw body, check expected payment-link and transaction references, and handle payment_link.paid, payment_link.expired and cancellation events. 
Razorpay

Manual transfer is not automatically paid when a parent uploads a receipt. The founder must reconcile the actual bank credit before marking payment verified.

No provider should be able to update an enrolment by trusting only the parent-facing redirect URL.

Status: Agreed. The MongoDB model, scheduling requirements, communication system and payment abstraction are now specified.

5. Technology stack — Agree with Claude Code's revised choice

Decision: Lock Netlify + Next.js + TypeScript + Tailwind + MongoDB Atlas + Better Auth.

I withdraw the PostgreSQL preference for this project. MongoDB is suitable if the developer implements the integrity controls specified in point 4.

5.1 Hosting: Netlify Personal

Agree with the founder's hosting decision.

Netlify's published credit-based Personal plan starts at USD 9/month with 1,000 monthly credits, with optional additional credits. Free has 300 credits and a hard limit. 
Netlify Docs

Production configuration:

Setting

	

Requirement




Framework

	

Next.js 16, current security-patched release




Runtime

	

Netlify's supported OpenNext adapter




Plan

	

Personal




HTTPS

	

Enabled, custom domain




Environment variables

	

Server-side secrets only




Deployment

	

Protected production branch




Scheduled jobs

	

Netlify Scheduled Functions




Usage monitoring

	

Credit alerts and a controlled recharge budget




Webhooks

	

Public HTTPS routes with signature validation




Production data

	

Never used in public preview deployments

Security version floor: Netlify's 3 November 2026 advisory recommends Next.js 16.4.5 and OpenNext Netlify adapter 5.16.6 or later. The build should use those versions or newer patched compatible versions, with an exact dependency lockfile. 
netlify.com

Enable usage alerts and decide on a limited auto-recharge allowance. A paused website also means its payment webhook handlers may become unavailable. Therefore, payment-status reconciliation must be possible from the admin.

5.2 MongoDB Atlas M0 and backups

Agree to start with Atlas Free for the small test, subject to the operational tests.

Official Atlas documentation confirms approximately 512 MB storage, a 500-connection limit and automatic pausing after 30 inactive days with no connections. This is acceptable for a small proof of concept but not an unlimited production guarantee. 
MongoDB Docs

Correction to Round 2: Atlas now documents an optional backup subscription for Free clusters in private preview.

It costs $0.10/day, capped at $3/month, with daily snapshots and retention of the last four. However, availability is gradual and cannot be assumed for every account. 
MongoDB Docs

My rule is:

If M0 backup subscription is available, enable it before storing real child data and perform a test restore.

If it is unavailable, prefer Atlas Flex with its supported backup capability or another verified paid backup solution before production.

Keep an additional securely stored, encrypted recovery export where appropriate.

Upgrade when storage, performance, backup reliability or operations justify it—not only when the database is full.

Do not create an unprotected automated download of family information to a personal computer or publicly accessible storage.

5.3 Authentication: Better Auth

Agree with Better Auth and its MongoDB adapter.

Its documentation supports MongoDB and a two-factor authentication plugin with TOTP and backup codes. 
Better Auth
+1

Required setup:

Area

	

Rule




Founder

	

super_admin, mandatory TOTP




Teachers

	

teacher, invited by founder, MFA required before accessing learner records




Public signup

	

Disabled for staff accounts




Teacher account creation

	

Founder creates an invitation; teacher verifies email and sets a password




Authorization

	

Every server action and API verifies role and assigned resources




Sessions

	

Secure cookies, revocation, expiration




Account recovery

	

Secure reset workflow and controlled backup-code recovery

Use Better Auth's admin-user management rather than hand-written password hashing or custom session handling. Its admin plugin supports creating accounts and managing users. 
Better Auth

The founder's account is bootstrapped securely once; public visitors cannot select an administrative role.

Parents and children do not need application logins in v1. Parent communications and secure email-based access to specific receipts or complaint status are sufficient.

5.4 Monthly running cost at pilot scale

Reference exchange rate: $1 ≈ ₹93.38, 10 November 2026. Vendor prices checked the same day. Figures exclude applicable taxes, domain registration, development and potential overages unless noted.

Service

	

Monthly estimate




Netlify Personal

	

$9 ≈ ₹840




MongoDB Atlas Free

	

₹0




Optional Atlas M0 backup, if available

	

Up to $3 ≈ ₹280




Resend Free

	

₹0




Google Meet eligible free use

	

₹0




Better Auth

	

₹0 licence fee




PayPal merchant account

	

₹0 base monthly fee




Razorpay standard gateway

	

₹0 base monthly fee




Domain

	

Depends on domain and registrar




SMS/OTP or additional monitoring

	

Not yet quoted

Resend's published free tier allows 3,000 transactional emails per month, subject to 100 emails per day. 
Resend

Core fixed platform cost

~₹840/mo
Netlify Personal, M0 and free email/Meet tiers

With optional M0 backups

~₹1,120/mo
Assuming backup preview is available
Payment cost for ten paying children

Scenario

	

Approximate cost for 10 payments




Stage A: PayPal, $29 each

	

₹2,240




Stage B: Razorpay, AED 99 each

	

₹890

The Razorpay estimate assumes the published 3% international-card fee plus 18% GST on that fee, without additional FX or bank charges. Actual merchant terms and currency settlement must be confirmed. 
Razorpay

The PayPal scenario is more expensive, but still potentially workable for the pilot.

Revised ₹25,000 test budget

The earlier corrected test budget was approximately ₹22,050, including ₹850 of estimated Razorpay payment fees and ₹1,500 for website/tools.

Replacing those payment fees with approximately ₹2,240 of PayPal charges gives:

₹22,050 − ₹850 + ₹2,240 = ₹23,440

This leaves approximately ₹1,560 below the ₹25,000 cap.

The ₹1,500 tool allowance can cover the roughly ₹840 Netlify subscription and, if available, the roughly ₹280 optional backup subscription. It does not automatically cover domain purchases, legal advice, development charges or extra messaging costs.

This is still a conditional pilot budget, not proof of profitability. Teacher rates, CAC and actual PayPal settlements remain assumptions.

Status: Stack agreed. Production database backup and gateway approvals are operational gates.

6. Build phases — Agree with eight milestones, but not an unconditional one-session promise

Verdict: Agree to a maximum of eight top-level phases. Disagree that every complete phase can safely be guaranteed to fit one coding session and eight files.

A working admin with payments, scheduling, child-data controls and financial reconciliation is too significant to force into an arbitrary implementation size.

My compromise: exactly eight demonstrable phases, each delivered through small changes of approximately eight hand-written files or fewer per coding session, including tests. If a phase requires more, it should be broken into implementation slices without creating additional top-level milestones.

Phase 1 — Foundation and deployment
Before first payment

Deliverable: A running, responsive Next.js application on Netlify Personal with brand tokens, public/admin layouts and deployment configuration.

Binary acceptance checks

Production and staging builds both succeed.

Custom domain and HTTPS work.

Mobile navigation works without layout overflow.

No secrets are exposed in client bundles or public repository files.

Required Next.js/adapter security versions are installed.

Phase 2 — Public website, trust and legal pages
Before first payment

Deliverable: The complete public website, including the imprint, pricing, safety, feedback, complaints, privacy, refunds and consent controls.

Binary acceptance checks

All agreed public routes load successfully.

Seller and pricing information is drawn from approved settings.

Marketing trackers remain blocked without consent.

A complaint creates a ticket that can be securely tracked.

Public feedback has verification, moderation and withdrawal controls.

Phase 3 — Database, authentication and CRM
Before first payment

Deliverable: MongoDB initialization, indexes, Better Auth, founder login, teacher-role restrictions, enquiries, leads, families, parental consent and follow-up tasks.

Binary acceptance checks

Founder login requires TOTP.

Public staff registration is blocked.

An enquiry creates one lead with attribution and a due follow-up.

A child profile cannot be created before the required guardian-consent workflow.

Unauthorized requests cannot access family records.

Phase 4 — Teachers, batches and scheduling
Before first payment

Deliverable: Founder-controlled teacher records, weekly availability, batch configuration, cycle generation and calendar management.

Binary acceptance checks

A weekly pattern generates exactly eight numbered sessions.

Founder-entered holidays are skipped and the resulting end date is shown.

Two overlapping teacher assignments cannot both be confirmed.

A batch cannot exceed five allocated seats under concurrent requests.

Rescheduling preserves session count and updates the relevant teacher locks.

Phase 5 — Payments and invoicing
Before first payment

Deliverable: Provider-independent payment records, working PayPal integration, manual transfer reconciliation, Razorpay adapter behind a disabled feature flag until approval, verified webhooks and digital receipts.

Binary acceptance checks

A valid simulated PayPal capture marks an enrolment paid.

Duplicate webhooks do not duplicate payment, enrolment or receipt.

A failed payment or browser redirect alone cannot activate enrolment.

A manually reported transfer requires founder verification.

Invoice and settlement records preserve the correct amount, currency and transaction reference.

Phase 6 — Operations and communications
Before first payment

Deliverable: Editable transactional templates, welcome/schedule messages, scheduled reminders, manual WhatsApp actions, privacy inbox, complaints handling and operational task alerts.

Binary acceptance checks

A verified payment queues exactly one welcome message.

Session reminders are scheduled at 24 hours and 1 hour before class.

A failed email remains visible and retryable.

Unsubscribed contacts cannot receive marketing through the admin.

Opening WhatsApp does not falsely mark a message as delivered.

Phase 7 — Teacher classroom portal
Before first class

Deliverable: Restricted teacher login, assigned classes, attendance, teacher notes, baseline/endline assessments and parent progress reporting.

Binary acceptance checks

Teachers see only their assigned batches and permitted learner details.

Attendance cannot be recorded twice for the same child/session.

Assessment rubric scores are validated within the allowed range.

A substitute can access only the sessions to which they are assigned.

No teacher can access other teachers' payout details or full parent contact information.

Phase 8 — Advertising, finance and management reporting
Before paid advertising and full pilot operation

Deliverable: UTM builder, campaigns, CSV spend imports, CAC reports, renewal management, teacher payouts, contribution reports, break-even tracker and final launch verification.

Binary acceptance checks

Importing the same ad CSV twice does not double-count spending.

Paid-family CAC and paid-child CAC are calculated separately.

Teacher payouts reconcile against completed, payable classes without duplication.

Renewals count paid advances, not merely verbal promises.

A complete enquiry-to-payment-to-class test passes, including privacy, refunds and recovery cases.

Release gates

Gate A — First paying family

Phases 1–6 completed, plus live merchant approval, verified backups and the legal/payment launch checks.

Gate B — First live class

Phase 7 completed, with functioning meeting-admission controls and teacher workflow.

Gate C — Paid ad campaign and complete 30-day test

All eight phases completed and production acceptance tests passed.

This meets the founder's requirement to build the complete system while avoiding rushed financial and child-safety features.

Status: Eight top-level phases agreed; session count must remain flexible enough for tested implementation.

7. Compliance — Agree with implementation, retain legal-review gates

Decision: Incorporate the UAE requirements into the site's information architecture, database records and admin workflows immediately.

UAE compliance-to-product mapping

Legal area

	

Product requirement

	

Location




UAE e-commerce law 14/2023

	

Published services, prices, fees and terms

	

/pricing, /terms, /program




Merchant identification

	

Actual seller identity, contacts and applicable licence information

	

/imprint




Customer complaints

	

Ticket submission, acknowledgement and secure tracking

	

/complaints, /admin/complaints




Public experience feedback

	

Authentic rating functionality

	

/feedback




Digital invoices

	

Detailed invoice/receipt for purchases

	

/admin/invoices, secure parent delivery




Service failures and refunds

	

Clear cancellation and refund workflow

	

/refunds, /admin/payments




Marketing choice

	

Per-channel opt-in and opt-out

	

Enquiry form, privacy settings, suppression list




UAE PDPL 45/2021

	

Purpose records, appropriate access, transfer assessment, rights handling

	

/privacy, /admin/privacy




Child Digital Safety Law 26/2025

	

Guardian-controlled child records, no child targeting, restricted access

	

Consent ledger, child profiles, teacher portal




Business continuity

	

Recovery documentation, backups, incident process

	

Admin settings and operating procedures




Data incidents

	

Restricted incident records and response tracking

	

/admin/privacy, breach register

The relevant obligations concerning prices, invoices, ratings, complaints, seller information, refunds and dispute resolution appear in the official English text of UAE Federal Decree-Law No. 14 of 2023. Article 9 also restricts pre-included arbitration clauses for digital contracts below AED 50,000. 
Ministry of Economy and Tourism UAE

Important child-law distinction

UAE Child Digital Safety Decree-Law No. 26 of 2025 entered into force on 1 January 2026 and includes a one-year regularization period for entities already subject to it. This should not be interpreted as permission for a newly launched service to disregard children's safeguards until January 2027. 
UAE Legislation
+1

Implement guardian verification and protective defaults before collecting identifiable child data.

Do not assume that the educational-platform exception automatically applies. Official UAE information refers to an exemption subject to further requirements and decisions. 
UAE Legislation

Guardian consent flow

The system should implement:

Parent submits contact details and an initial age-band enquiry.

Parent email or phone contact is verified.

The parent receives a versioned privacy notice and child-data consent explanation.

The system completes the approved parental verification method.

Only then is the child's identifiable enrolment profile created.

Consent events are stored append-only, including version, purpose, method and timestamp.

Withdrawal initiates a documented workflow that stops unnecessary processing and determines whether any statutory records must be retained.

The legal adviser must approve the verification method; email confirmation by itself must not be labelled legally sufficient without checking the actual requirements.

India DPDP requirements

India's Digital Personal Data Protection Act, 2023 and Rules, 2025 should be reflected in the same model.

The Ministry of Electronics and Information Technology published the Rules and an enforcement timeline in November 2025, including an eighteen-month phased compliance period for key provisions. The project should therefore be designed now for verifiable parental consent rather than waiting until the later commencement period. 
MeitY
+1

Data minimization and transfer safeguards

Store only the information needed to administer classes. There is no operational need to collect a child's Aadhaar, passport number, full home address or school name.

Avoid storing a family's ethnic origin or religion. Interest in learning Gujarati does not require an ethnicity field.

Documents and user-facing policies should explain which service providers process parent/child information, including the hosting provider, database provider, payment processors, email provider and meeting platform.

Cross-border data transfers and permitted processing grounds require legal confirmation, especially for UAE parents whose data is handled from India and potentially other cloud regions.

Recording and teacher conduct

Recording remains off by default.

The application should not provide a classroom recording button, and teachers should be prohibited from privately recording or publishing children's voices or images.

Teachers must communicate with guardians through approved channels and follow the documented safeguarding and incident-escalation procedure.

The remaining regulatory concern

The founder is currently an individual rather than a registered business.

A PayPal Business Individual account does not, by itself, establish that all educational-service licensing, merchant identification, Indian tax and UAE cross-border selling obligations have been satisfied.

Obtain a targeted legal/tax assessment covering:

Whether an India-based seller of live online Gujarati classes requires any additional UAE authorization or notification, including KHDA/ADEK considerations.

The applicable UAE VAT treatment.

Indian GST treatment and export-of-services documentation.

Whether the selected seller identity and permitted registrations meet applicable e-commerce disclosures.

Whether the proposed data transfers and parental verification workflow are sufficient.

Do not build recorded lessons or sell prerecorded content until their separate regulatory and tax implications are evaluated.

Status: Product requirements agreed; the unresolved legal questions remain launch gates rather than assumptions of compliance.

Locked decisions for Claude Code

Area

	

Final decision




Brand

	

VaatKadi, pending final language/trademark clearance




Backup brand

	

VaatoNest




Launch market

	

UAE




Learners

	

Children aged 7–12




Program

	

Eight live 45-minute classes per cycle




Batch size

	

Maximum five




Teachers

	

Founder-recruited, independent




Hosting

	

Netlify Personal




Application

	

Next.js + TypeScript + Tailwind




Database

	

MongoDB Atlas




Authentication

	

Better Auth, mandatory staff MFA




Video

	

Google Meet




Initial payments

	

PayPal Business Individual, subject to approval




Stage-A price

	

USD 29 per child per cycle




Later gateway

	

Razorpay, after approval




Proposed Stage-B price

	

AED 99, if supported




Email

	

Resend Free initially




WhatsApp

	

Manual click-to-chat initially




Advertising

	

Meta/Google interfaces, tracked in internal admin




Build organization

	

Eight milestones with testable acceptance gates




Child data

	

Guardian-controlled, minimal and access-restricted

Points still open

VaatKadi approval: Native Gujarati speaker review, trademarks, domain and social handles.

Merchant onboarding: Actual PayPal account approval, guest-card payment test, verified settlement and INR reconciliation.

Razorpay migration: Required sole-proprietor documentation, international-card activation and direct AED settlement/charging capabilities.

UAE legal assessment: Cross-border education licensing, KHDA/ADEK, VAT and actual seller disclosures.

Indian tax assessment: GST, exports of services, invoicing and foreign-payment documentation.

Parental verification: Legally appropriate method and retention/withdrawal rules.

MongoDB production recovery: M0 backup-preview availability or confirmed paid backup alternative.

Commercial batch policy: Whether four children may start a class, reservation expiration, refund cutoff and makeup-class treatment.

Final pricing validation: PayPal transaction and FX charges from real merchant settlements; whether Stage-B AED 99 provides sufficient margin.

Pilot operating assumptions: Actual teacher quotes, CAC, parent willingness to pay, attendance and paid renewals.

Final instruction to Claude Code: Treat the decisions above as the Round 2 technical specification. Do not reopen accepted platform choices without new evidence. Implement with tested safeguards, and keep unresolved legal, payment and recovery questions as explicit launch blockers rather than silently treating them as completed approvals.
