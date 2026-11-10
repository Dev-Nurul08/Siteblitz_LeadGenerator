Claude Code, round 2. I checked your claims against primary sources and our own research (two research passes
today: platform/legal and copy/tactics). Verdicts per point, then the questions I need you to settle. Keep the
same point numbers.

## Facts checked
- Google Workspace AUP (last modified 2025-10-13) does ban generating or distributing large-scale unwanted email
  ("spam"): **confirmed** (workspace.google.com/terms/use_policy, read today).
- WhatsApp Business Messaging Policy 2026-09-23 requires number given by the person AND opt-in: **confirmed**.
  Extra facts: templates cannot carry audio (headers are text, image, video, GIF, document, location only); marketing
  templates are not delivered to US +1 numbers; the plain Business app bans bulk/automated messaging.
- CNIL 2026-06-10: B2B email allowed on legitimate interest when related to the recipient's profession; generic
  addresses (info@, contact@ of a company) are not subject to those principles: **confirmed** (cnil.fr page read).
- "German UWG §7 amended February 2026, stricter": **not supported**. The February 2026 UWG amendment implements the
  EmpCo directive (greenwashing, Taylor Wessing 2026-02); §7 email consent is unchanged - prior express consent
  was already required. Decision (Germany on hold) is unchanged.
- RBI FEMA (Export and Import of Goods and Services) Regulations 2026 in force from 2026-10-01: **confirmed**
  (RBI press release).
- India TRAI TCCCPR 2nd amendment (2025-02-12): first violation bars all the sender's numbers 15 days, repeat =
  1-year disconnection + blacklist; promotional calls only from 140 series. So no cold calls/SMS from a personal SIM.
- Your email drafts show "From contact@aaziko.com". That address comes from your interface, not from us; no
  template will carry it.

## Verdicts
- **C1 Workspace AUP** - agree the risk is real; **reject "explicit provider approval" as a gate** because Google
  does not issue approvals, so the gate can never pass. Proposed replacement: 1:1 personalised, lawful, <= 30 sends
  per inbox per day, complaints < 0.1 %, sending domains in a separate org from hello@, suspension risk accepted in
  writing by the founder. Question A below.
- **C2 WhatsApp** - agreed.
- **1 Hygiene** - agreed (ladder, six statuses, keep free-mail, audit 100). One change for founder time: an address
  listed on >= 5 places is excluded in the pilot, not investigated. Catch-all = RISKY, not sent in the pilot.
  Nothing in the 86.75 M source folder is deleted; the outreach table is lean and guessed emails are removed at the
  code source (`enrichment/discovery.py`, `lead_radar_service.py`, `export_surat_leads.py`).
- **2 Routing** - agreed except India (question B) and phone-only (question C).
- **3 Copy** - agreed on structure, truthfulness, opt-out, no Re: on touch 1. Two changes: (a) <= 100 words, because
  the largest dataset we found (Hunter, 34 M emails, vendor) shows length barely moves replies (3.4-4.5 % across
  buckets, best 20-39 words) and the founder must review each one; (b) open with the observation itself, not "I came
  across" (no study proves it hurts, but it is the most templated opener in the inbox).
- **4 Lifecycle** - agreed in full: Day 1 / 6 / 14, close Day 21; reply branches; requirements in two stages;
  deposit after written scope and before any work; balance after staging approval and before launch and handover.
  Additions: an out-of-office auto-reply pauses the sequence until the return date; "please call me" = permission
  to call, logged.
- **5 Countries/language** - agreed: language evidence hierarchy (our data has no post text, so the founder confirms
  language on their social page during the review), native review of the first 10-20 messages per language, quote-
  only pricing (option C) abroad. Our code gap: `country_rules.py` has no rows for NL, ES, ZA, AE, IN and lacks the
  Singapore `<ADV>` subject rule; until added those countries are on hold.
- **6 Hook** - agreed: no AI-cloned voice in cold outreach; real voice / screen video only after engagement;
  Opportunity Snapshot is good. Question D on the free concept.
- **7 Pilot** - agreed on separating first revenue from the scale test and on the economics (3 Launch orders =
  Rs 23,997 vs ~Rs 17,499 infra over 2 months). Question E.

## Questions for you
A. Is there a sending setup whose own terms explicitly allow lawful, low-volume B2B first-touch email (dedicated
   cold-email mailbox providers, Zoho, Microsoft 365, Instantly's own infrastructure)? Name it with the clause and
   URL, or say none exists and the AUP risk must simply be accepted at low volume.
B. India. You put India on "referrals and inbound only". The founder has zero clients, so there are no referrals,
   and "5 warm introduction requests a day" has no named source - from whom? Our research: India has no anti-spam
   statute for email; DPDP core duties start ~2027-05-13; s.3(c)(ii) public-data exclusion is contested. Proposal:
   India B2B email to the business's own published address, <= 20/day in month 1, sender identity, postal address,
   one-line opt-out, provenance URL stored, permanent suppression - lawful today, with the DPDP review still open.
   Agree, or name the specific Indian rule it breaks.
C. Phone-only and no-contact businesses in India (1.82 M phone-only, 1.08 M social-only). Proposal: (1) look for an
   email on their own website/social page; (2) Mumbai walk-ins; (3) **a posted card or letter** with a printed
   Opportunity Snapshot and a QR code opening WhatsApp click-to-chat with a pre-filled message ("Hi SiteBlitz, please
   show me the website idea for <business>") - the owner messages first, so WhatsApp opt-in and the 24-hour window
   exist and a real founder voice note becomes allowed. Is physical mail to a business address lawful and sensible
   in India? Realistic cost per piece (print + India Post) and response rate? This is also our candidate for the
   "these people found a new way" effect. Judge it.
D. The free concept. The founder said: no more free work. But with zero clients and zero proof, a visual preview is
   the strongest lever, and "Review before you pay" was already agreed on 2026-11-01. Proposal: replace the 3-hour
   bespoke concept with a **15-20 minute templated preview** (their name, category, city and approved photos placed in
   one of our three existing industry demos: salon & beauty, coaching & tuition, retail & showroom), only after a
   positive reply AND the three qualifying answers (decision-maker, accepts the Rs 7,999-17,999 range, launch within
   60 days); cap 5 per week. Snapshot for every positive reply, preview only for qualified ones. Agree / disagree.
E. Pilot volume. Your caps (5-20 emails/day) give ~250-300 first touches in 30 days -> at 3 % ~8 positive replies.
   Is that enough to reach a first deposit, or should month 1 run the full 3-week warm-up on the level-1 domains
   while India email starts at 20/day and the card test runs at 100 cards? Give the exact daily plan for the founder
   (hours per day) and the stop rules.

Answer each point by number: agree / disagree because ... / need data: ... . End with the list of points still open.
