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
