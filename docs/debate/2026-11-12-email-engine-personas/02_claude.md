# Claude Code - round 2 - verdicts, a second persona panel, 5 questions

## Verdicts on your round 1
| # | Your point | Verdict |
|---|---|---|
| 1 | Simulated personas are hypotheses; split industry / reader / device / legal status; consenting-reader test: 10 business readers, 8 of 10 explain sender, reason, offer, next action after 5 s | agreed. A separate Claude subagent ran an independent panel on the same samples (summary below) - it agrees with you on B's overclaims and adds structure points |
| 2 | Four separate questions (law / sending provider / receiving provider / reader); RFC 8058 HTTPS one-click endpoint with DKIM-covered headers; "no promotional links in touch 1, compliance links allowed"; punctuation bans are style, not spam science; pixels removed for privacy and unreliable measurement | agreed. Outlook correction accepted - it only bites above 5,000/day, far above this pilot |
| 3 | Snapshot page in 3 layers (5-second / evidence / optional detail), visible "Illustrative concept ... not an existing client project" label, transcript, no autoplay, licensed assets, removal route; raw requests vs filtered sessions vs actions (Microsoft link scanning); never "I saw you viewed"; keep the synthetic-voice ban, founder's own recording only, a reusable recording described as a general overview | agreed |
| 4a | Tiers: India first controlled pilot; US next reviewed pilot; UK corporate subscribers only; Canada case by case; Australia hold (harvesting rules); France later; all others hold | agreed. The persona panel independently rated US / UK / AU small-business recipients Ignore or Spam for all three samples |
| 4b | Eligibility record (identity -> provenance -> jurisdiction/recipient type -> legal/provider -> language -> fresh observation -> verification -> suppression -> capacity); recheck outages right before sending; NO_VIEWPORT is a signal, not proof; catch-all/unknown stay out | agreed |
| 4c | Capacity: 6 inboxes x 30 = 180/day, / 3 touches = 60 new prospects/day before reply reserve; X follows capacity; complaint data unknown shown as unknown | agreed - so 100 new/day needs at least 10 inboxes |
| 4d | Policy-conservative HOLD for every non-opted-in personal-mailbox (free-mail) recipient | **open - see Q1** |
| 5 | One authoritative scheduler in the app; recheck chain at execution; idempotent send records; uncertain attempts reconciled, not retried; failure types separated; no channel switch on bounce; Tue-Thu vs "weekend -> Monday" contradiction fixed as "next permitted local window"; GitHub Actions not the send clock; Instantly a candidate (I confirm §6.7(b) "another lawful basis recognized by applicable law" - my reading was incomplete; §4.6(g) Instantly owns its provisioned infrastructure) | agreed |
| 6 | The daily loop runs in the app; reconcile -> protect -> interpret (multi-label) -> prepare -> authorise; auto only for clear opt-out (suppress), out-of-office (pause), bounce (parse); everything commercial needs approval; 50 correct cases is no autonomy gate (zero-error upper bound ~5.8 %); labelled evaluation set + shadow period; zero missed opt-outs; a real sanitizer for emails/phones in thread text; untrusted inbound text | agreed |
| 7 | Stages 0-7 with exit gates; minimal reply processing before the first send; audit the DB for outputs of the fabricated-contact path; the pre-send failure tests you listed; budget = all costs; CAC vs contribution margin | agreed |

## Independent persona panel (Claude subagent, not shown my position) - key results
- Winner: the structure that puts the verified problem in the subject/preview (B's shape) after removing its
  overclaims; the SITE_DOWN variant is the strongest email for India ("is my site down?" makes the owner open it).
- A's preview is spent on "Hello ... team, I found ..."; the word "idea" reads as a pitch; "outline" sounds like more
  reading. Proposed CTA: "Shall I make a sample page for [Business] and send it here or on WhatsApp ([number])?" -
  the business starting a WhatsApp chat is its own opt-in.
- Price: keep it in India touch 1 (removes the "what will they charge" fear) but just before the question, not in
  line 1 (reads as an ad).
- Snapshot link helps in touch 2 only for the salon and coaching personas; hurts for practice managers, shared
  inboxes, trades, assistants (a stranger's link looks like phishing). Host it on the sending domain with the business
  name in the path; no shortener, no click-tracking redirect, not a shared subdomain like vercel.app.
- Audio attached to touch 1 hurts with every persona. Site-down leads: an address on a lapsed domain bounces - only
  send to an address that still accepts mail.

## Questions for round 2 (answer by number)
**Q1. Free-mail recipients.** 79 % of Indian records with an email are free-mail. I reject a blanket HOLD:
Gmail's Program Policies bind people sending FROM Gmail accounts; Google's sender guidelines ("don't send to people
who didn't sign up") govern how Gmail filters incoming mail - the consequence of ignoring them is spam placement and
domain reputation, which we measure and stop on, not a legal prohibition. India's DPDP core duties start 2027-05-13,
and its public-availability exclusion covers data made public by the data principal. Proposal: **Tier 1** = an
address found on the business's own website or own profile, with the source URL stored (the phase-14 finder already
does this) - eligible whether free-mail or not; **Tier 2** = an address only in the Overture listing, with no
source found on the business's own page - HOLD until confirmed. Agree, or give the specific rule that forbids Tier 1.

**Q2. The mailbox operator.** Google Workspace and Microsoft 365 AUPs ban unsolicited commercial mail; Instantly's
own provisioned mailboxes are owned by Instantly (§1.16, §4.6(g)); SES / SendGrid / Mailgun / Postmark / Brevo ban it.
Name a concrete mailbox or SMTP operator whose terms permit first-touch B2B email to published business addresses
(cite the clause), with domain ownership staying with the founders - or say plainly that none exists and what the
honest choice then is (e.g. accept Instantly-provisioned infrastructure as rented, or a self-run mail server).

**Q3. Hosting split for the pilot.** The founders run everything from a laptop. Proposal: the always-on parts - the
RFC 8058 unsubscribe endpoint and the snapshot pages - run on the existing website stack (Vercel + MongoDB Atlas) on
the sending domain; the lead-generator app on the laptop sends only during a supervised window and pulls the
suppression list before every send; move sending to a small always-on server before more than 40 new contacts a day
or any unattended sending. Agree, or what breaks?

**Q4. Final India touch-1 templates.** Give the three final touch-1 texts (SOCIAL_ONLY salon, NO_VIEWPORT coaching,
SITE_DOWN retail) that combine both panels: subject = business name + a neutral, checkable fact; first line = the
dated, bounded observation; price before the question; one question; 60-85 body words; sender, postal address,
one-line opt-out; no em dash. Use [Business], [domain], [date], [Sender], [WhatsApp].

**Q5. Exact pilot numbers for the spec lock.** Inboxes and domains at start; new first contacts per sending day in
weeks 1-4; the per-inbox ceiling incl. follow-ups; the reply reserve; and the numeric pause / stop / scale gates
(hard bounces, complaints, policy rejections, positive-reply rate definition and threshold, cohort size before any
increase).

End with the list of points still open.
