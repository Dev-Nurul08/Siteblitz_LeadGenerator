ChatGPT said:
SiteBlitz — Round 2: Decisions for Claude Code

10 November 2026 · Seven agenda points · Questions A–E

Overall verdict: Agree with the direction. Four of the five proposed changes are acceptable, with operating safeguards. Question A has a useful new finding: a more suitable sending-infrastructure option exists.

My decisions are:

Question

	

Decision




A. Cold-email provider

	

Partially agree. Instantly's native infrastructure expressly supports direct B2B sales/marketing, but not an unrestricted right to send unsolicited emails.




B. India B2B cold email

	

Agree conditionally. I found no general Indian statutory prohibition on the narrowly described email pilot. The provider's rules and other applicable laws still matter.




C. Physical mail + WhatsApp QR

	

Agree. This is worth a 100-piece experiment.




D. 15–20-minute preview

	

Agree. Three qualification gates and five per week are sensible.




E. Parallel 30-day pilot

	

Agree with changes. Warm-up, eligible India email and printed cards can run together, but not from newly purchased domains before they meet the sender's rules.

Legal conclusions below are research findings for counsel to review, not a legal opinion. Costs and conversion assumptions are identified separately from established facts.

1. Data hygiene and fake emails

Verdict: Agree with Claude Code's proposed changes. No additional debate required.

Exclude addresses shared by five or more places from the pilot rather than spending founder time investigating them. Keep catch-all addresses as RISKY and exclude them from sending. Remove guessed-email generation at the three identified code locations and preserve the original 86.75 million-record source database.

One safeguard: exclude does not mean invalidate. An address shared across several branches may be genuine. Its exclusion is a pilot-efficiency decision, not a verified finding that the address is fake.

The resulting rule is:

Eligible email = verified business + real sourced address + acceptable verification result + no suppression + country/channel permission.

For the initial sample, use a 100-record manual audit. Record how many fail because of wrong business, outdated contact, guessed address, invalid email, shared-address threshold or legal/channel restrictions.

Who benefits: Founder, engineering and deliverability. Cost: existing verification budget plus engineering time. Test: audit agreement of at least 95 out of 100 manually reviewed eligibility classifications, with any incorrectly approved guessed address treated as a blocking defect. The 95% threshold is a proposed internal quality gate.

No new feature is needed until these classifications work reliably.

2. Channel routing — Questions A, B and C
A. Is there a provider that permits B2B first-touch marketing?

Verdict: Partially agree with replacing my earlier provider-approval gate.

Claude Code is correct that demanding individual written preapproval from Google is impractical. But I disagree that accepting suspension risk makes any use compliant with the provider's terms.

A significant new finding is in Instantly's current contract.

Instantly — native sending infrastructure

Conditional fit

Terms of Service, updated 4 November 2026

Section 1.10 defines the permitted purpose to include the customer's own direct B2B sales, marketing, recruiting and business-development activities.

Section 4.6 addresses Instantly-operated sending infrastructure, including its done-for-you accounts. The platform describes native AirMail accounts as infrastructure for cold outreach.

Official Terms of Service · Official Sending Policy · Sending-account documentation

Source confidence: high for the contractual wording; medium for interpreting its suitability for a specific first-touch campaign. 
instantly.ai
+2

This is an explicit contractual purpose covering direct B2B marketing, not an express statement that every non-opt-in cold email is permitted. Instantly separately requires compliance with applicable law and its own anti-spam policy, and reserves suspension rights.

The critical comparison:

Provider

	

Verified policy position

	

Decision




Google Workspace

	

Prohibits unsolicited mass email

	

Use primary inbox for clients and replies; do not assume 30/day is a safe harbour




Zoho Mail

	

October 13, 2026 usage policy explicitly excludes promotional and marketing emails

	

Reject for this campaign




Microsoft 365

	

Online Services AUP prohibits spam; Exchange Online is not designed for bulk marketing

	

Not an affirmative cold-outreach solution




Instantly + connected Workspace inboxes

	

Instantly permits B2B campaigns, but the underlying Workspace terms still apply

	

Underlying risk remains




Instantly-native AirMail / eligible native infrastructure

	

Purpose-built for direct B2B outreach, subject to law and Instantly's policy

	

Preferred option to investigate

Sources: Google Workspace AUP (2025-10-13), Zoho Mail policy (2026-10-13), and Microsoft Online Services AUP (checked 2026-11-10). High confidence in the stated restrictions. 
Google Workspace
+2

New technical constraint: domain age

Instantly's October 13, 2026 Sending Policy says sending domains should be at least one month old. It also requires accurate sender identification and a clear opt-out in each campaign. 
instantly.ai

That matters:

New domains purchased on November 10 should not be assumed eligible for cold sending on November 17.

Warm-up alone does not eliminate the domain-age requirement.

Instantly offers pre-warmed accounts, but the actual domain age and account status still need checking.

Instantly-provisioned infrastructure may remain owned and controlled by Instantly; there is a portability trade-off. 
Instantly Help Center

My final A decision: Replace "obtain provider approval" with "select a provider/product whose published terms cover the intended activity; verify the actual underlying sending infrastructure; comply with its policy; accept documented residual suspension risk."

Choose native infrastructure over purchasing extra Google Workspace inboxes solely for cold first touches. Recalculate the previously approved ₹12,239 pilot budget before switching: I have not verified a comparable current AirMail quote.

Thirty messages per inbox per day remains an internal risk limit, not a provider guarantee or legal permission.

B. Can India B2B email begin now?

Verdict: Agree conditionally with the proposed 20-new-contact/day ceiling. I would not limit India to referrals and inbound enquiries.

Claude Code's challenge is valid: a startup with no customers cannot rely on an unspecified network of five warm introductions every day.

I checked India's position more closely.

Linklaters' India data-protection guide and CMS's India privacy-law guide identify no standalone comprehensive Indian law generally prohibiting direct marketing by email. That does not remove the relevance of other privacy, consumer-protection or provider requirements. 
linklaters.com
+1

The government's November 13, 2025 commencement notification schedules the main DPDP data-processing duties, including Sections 3–5, for May 13, 2027. The Act's other provisions have different commencement dates. 
MeitY

I therefore cannot name a specific current Indian statute that categorically prohibits a carefully targeted, individual B2B sales email to an official company-published role address under all circumstances.

I also cannot certify every address in the dataset as lawful for marketing. A contact copied from a third-party listing is not necessarily published by the business itself, and a named employee's address can involve personal data. The future Section 3(c)(ii) public-data exception should not be treated as blanket consent.

Approved-for-design pilot criteria

Control

	

Decision




Recipient source

	

Official business website or otherwise independently confirmed business-owned contact




Priority

	

info@, contact@, or another genuine relevant company role address




Named employee

	

Manual review; do not automatically treat business employment as consent




Daily volume

	

Up to 20 new contacts/day, conditional on provider and eligibility gates




Identification

	

Actual founder name, SiteBlitz, working reply address, genuine postal address




Content

	

Relevant, truthful, 100 words or fewer




Opt-out

	

Clear reply-based opt-out; immediate suppression




Compliance record

	

Source URL, review date, recipient class, applicable country rule and send history




Recontact

	

Maximum three touches unless the person engages; objections stop marketing

This permits a more commercially realistic experiment without pretending the upcoming privacy requirements do not matter.

Cost: Human qualification, verification and suitable email infrastructure. Benefit: A revenue opportunity independent of the founder's personal contacts. Test: deliverability and paid deposits by contact-source category.

Important distinction: the India email route remains a manually reviewed pilot until the code's India rule is implemented and legal review is completed. It is not permission to activate the default worldwide sender.

C. Physical mail with a personalised WhatsApp QR code

Verdict: Agree. This is the strongest new proposal in Round 2 for phone-only and no-contact India leads.

India Post explicitly offers direct advertising and direct mail to businesses. Its official service description covers printed sales messages intended to generate responses. This makes ordinary addressed commercial post a credible channel, provided the material complies with postal restrictions and general law. 
India Post

There is one important operational distinction: India Post's Direct Post service is for unaddressed mail and requires at least 1,000 pieces. It is not the correct product for 100 individually addressed SiteBlitz letters. 
India Post

For the first 100 businesses, use ordinary addressed letters or appropriately classified printed postcards.

Realistic cost per piece in India

Item

	

Published postage or estimated cost




Ordinary letter up to 20 g

	

₹5 postage




Each additional 20 g or part thereof

	

₹5 additional postage




Commercial printed postcard

	

₹6 listed in India Post's published postal compilation; confirm current classification at counter




One-page colour print

	

₹5–₹12 estimated




Envelope and addressing supplies

	

₹2–₹4 estimated




Personalised preparation labour

	

Approximately 4–8 minutes per business

India Post's domestic tariff confirms ordinary letter postage. Its published administrative compilation lists printed postcards at ₹6, although the current general postcard tariff page does not clearly separate that commercial category. Postal confirmation is advisable before printing all 100.

100 LETTERS — CASH COST

₹1,200–₹2,100
Planning range; excludes founder time and one-time design

RESEARCH + PREPARATION

7–14 hrs
Estimated labour for 100 businesses, including address checking

If all 100 are produced at a cash cost of ₹15 each, the test costs ₹1,500. Add a value for founder labour when calculating actual acquisition cost.

These are estimates, not supplier quotations.

Will the QR establish WhatsApp opt-in?

Yes for responding to a specific owner-initiated request; no for unrestricted future marketing.

Meta explicitly recommends using customer mailings and QR codes to let customers initiate WhatsApp conversations. Its Business Platform policy then permits ordinary replies within a 24-hour service window. 
WhatsApp for Business
+1

The correct sequence is:

SiteBlitz posts a genuine business proposal to a verified business address.

The owner scans the QR, reviews the prefilled text and actively presses Send.

SiteBlitz records that the business initiated contact and responds to the requested website idea.

A real founder-recorded voice note can be sent as part of that requested conversation if useful.

Any unrelated or later business-initiated marketing requires a separate valid opt-in and the appropriate WhatsApp messaging mechanism.

The 24-hour template rule specifically applies to the Business Platform. It should not be confused with a general right to message someone indefinitely through the Business App.

My suggested QR text
Writing

Hello SiteBlitz, I received your website idea for [Business Name].

Please show me the suggested design and price. You may reply here on WhatsApp about this request.

The QR must be generated using the actual SiteBlitz WhatsApp number. The owner must initiate the message themselves; simply scanning a QR or opening a prefilled chat is not sufficient.

Expected response rate

I did not verify a reliable independent India-specific response rate for this exact kind of personalised B2B postal campaign. I would not import direct-mail industry averages from a different country and present them as a forecast.

Instead, use scenarios:

Responses from 100

	

Observed response rate

	

Meaning




0

	

0%

	

Possible channel or offer mismatch; investigate delivery and message




1

	

1%

	

One conversation; insufficient to prove viability




3

	

3%

	

Encouraging for a small experiment




5

	

5%

	

Strong early signal, still needing replication

At ₹1,500 cash cost, one genuine enquiry means ₹1,500 cash cost per enquiry, whereas three mean ₹500 each, before labour.

C decision: Approve a controlled 100-piece test, but only for one defined business category initially. The personalised Opportunity Snapshot and owner-initiated WhatsApp conversation are the real differentiators—not the QR technology itself.

3. Cold email copy — revised human-first approach

Verdict: Agree with both changes.

The Hunter dataset is useful directional evidence, but the reported reply-rate differences should not be interpreted as proof that 20–39 words is optimal for SiteBlitz. A message needs enough information to establish credibility, particularly when the business has never heard of the sender.

I approve a 100-word maximum including the signature and opt-out, with a working target of 60–85 words.

Opening with a verified observation is stronger than repeatedly using "I came across your business."

Revised Touch 1 — India
A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

Your [verified public page] shows [specific service], but I couldn't find a website linked there.

I'm [Your Name] from SiteBlitz. We build simple websites that put services, location and contact details in one place. Our India packages start at ₹7,999, excluding domain and hosting.

Would you like a short outline for [Business Name]?

Regards,
[Your Name] | SiteBlitz
[Reply email] | [Business postal address]

If not relevant, reply "stop" and I won't contact you again.

This message only works when the website observation is true. Do not substitute fabricated compliments when the observation is unavailable.

Revised Touch 2 — Day 6
Re: A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

One thought on [Business Name]: a simple website could help customers find [verified service], business hours and the right contact number without searching through several posts.

Would you like me to send a suggested page structure and fixed quotation?

Thanks,
[Your Name]
SiteBlitz
[Reply email] | [Business postal address]

Reply "stop" if you'd prefer no further emails.

Revised Touch 3 — Day 14
Re: A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

I'll close this enquiry after this message.

If a website becomes useful for [Business Name] in the future, you're welcome to contact us. I'd be happy to explain the options and pricing.

Thank you for your time.

Regards,
[Your Name]
SiteBlitz
[Reply email] | [Business postal address]

No further follow-ups are planned. You can reply "stop" at any time.

For the follow-ups, use Re: only when the message is genuinely being sent in the original thread.

Copy decision for Claude Code: Keep these as three distinct templates. Require observation_source_url, verified_observation and a human approval flag before Touch 1 becomes eligible for sending. Do not let the AI invent observations when those fields are empty.

Cost: approximately 3–5 minutes of combined investigation and approval per prospect after the tooling is usable. Benefit: relevance without fabricated familiarity. Test: positive replies, objections, and paid conversions by copy variant.

4. Complete lead-to-payment lifecycle

Verdict: Agree with Claude Code's additions. No change to the payment milestones.

The Day 1 / 6 / 14 schedule and Day 21 closure remain the default for nonresponders.

I approve these additional state transitions:

Event

	

CRM state

	

Next action




Out-of-office with return date

	

PAUSED_OOO

	

Resume with the next unsent touch two business days after the stated return date




Out-of-office without return date

	

PAUSED_OOO_UNKNOWN

	

Hold 14 calendar days, then review; close if no clear return or engagement




"Please call me"

	

CALL_REQUESTED

	

Record number and time preference; allow a call about the stated enquiry




Genuine interest

	

QUALIFYING

	

Pause every outbound sequence and collect initial requirements




Three preview conditions met

	

PREVIEW_ELIGIBLE

	

Allow one capped preview




Written quotation accepted

	

AWAITING_DEPOSIT

	

Send deposit invoice




Deposit received, requirements incomplete

	

DEPOSIT_PAID_NOT_READY

	

Collect content/access; do not start delivery clock




Scope, content, access and deposit complete

	

READY_TO_BUILD

	

Confirm agreed start date




Staging and agreed revision approved

	

AWAITING_BALANCE

	

Invoice balance before public launch




Final payment received

	

PAID_READY_TO_LAUNCH

	

Publish and hand over

The requested phone call creates permission for the requested conversation, not an unrestricted subscription to future marketing calls or WhatsApp promotions.

Payment remains fixed

Package

	

After written scope acceptance

	

After staging approval, before launch




Launch

	

₹4,000

	

₹3,999




Business

	

₹9,000

	

₹8,999




Custom

	

As individually quoted

	

As individually quoted

One important distinction: the preview in Point 6 is a sales demonstration, not the beginning of the contracted website build. The two-day/seven-working-day delivery commitment only starts once all ready-to-build conditions are satisfied.

Implementation requirement: Every state needs an event log, owner, next action and, where applicable, due date. Payment status must come from a verified payment or bank reconciliation—not from an email being sent or an invoice being marked issued.

Success test: No project enters BUILDING without the deposit, and no project enters LAUNCHED without the agreed balance or a documented founder-approved contractual exception.

5. Countries, language and international pricing

Verdict: Agree. I also accept the correction on Germany.

My previous statement connecting the February 2026 UWG amendment to a new, stricter Section 7 email-consent rule was incorrect. I retract it. Germany remains on hold because of its existing consent rules, not because of a newly introduced February restriction.

I agree that the country-language hierarchy should remain evidence-based. Since the dataset does not include social-post text, the founder must verify the actual communication language before approving translated first-touch copy.

Country-code changes

Country

	

Current decision

	

Required implementation




IN

	

Manually reviewed India email pilot only

	

Implement country-specific eligibility, provenance and privacy review




NL

	

Hold

	

Confirm Dutch electronic-marketing requirements




ES

	

Hold

	

Confirm Spanish electronic-marketing requirements




ZA

	

Hold

	

Confirm POPIA and electronic direct-marketing requirements




AE

	

Hold

	

Confirm UAE marketing and privacy requirements




SG

	

Hold

	

Implement Spam Control Act rules, including the advertisement-label requirement when applicable




DE

	

Hold

	

Maintain existing strict prior-consent controls

Singapore's current Spam Control Act requires the <escape><ADV></escape> advertisement prefix for covered unsolicited bulk commercial email and establishes specific bulk thresholds. The source is the Spam Control Act 2007 and Second Schedule (current legislation checked 10 November 2026; high confidence). 
Singapore Statutes Online
+1

Do not automatically apply a default "opt-out" classification to every unrecognised country. Unknown country rules should return HOLD_LEGAL_REVIEW.

I also agree with quote-only international pricing. India remains on its approved package amounts, while overseas prospects receive a reviewed scope and quotation. The founder should not publish arbitrary converted prices or promise a payment processor that has not been configured.

Success test: Zero automatically sent messages from an unknown, held or unreviewed country rule.

6. Unique hook — Question D: the 20-minute preview

Verdict: Agree with the exact proposal, subject to one wording change.

Replace the three-hour free bespoke homepage concept with a capped 15–20-minute illustrative preview.

I distinguish working for free on a client project from spending a controlled amount of time demonstrating a product before a sale. The latter is ordinary sales acquisition cost.

The qualification gate

Preview eligibility

0/3 confirmed

The respondent is the decision-maker or has explicit authority to commission the website
They acknowledge the ₹7,999–₹17,999 India package range and understand exclusions
They intend to launch within approximately 60 days

Send the standard Opportunity Snapshot, but do not start a custom preview yet.

Approved preview workflow

Use the three existing industry demos: salon and beauty, coaching and tuition, and retail and showroom.

Personalise only the business name, category, location, approved images, real service descriptions and appropriate contact method. Do not create new architecture, animations, integrations or special features for this free demonstration.

The preview should display "Illustrative concept — not a completed customer website." Use customer photographs only with suitable permission.

At most five previews per week, each capped at 20 minutes. That is:

MAXIMUM PREVIEW LABOUR

100 min/week

MAXIMUM IN 4 WEEKS

20 previews

The commercial rule is simple: one preview, one opportunity to discuss it, then a written quote and deposit request. Further design changes belong in the paid project.

The founder's already agreed "review before you pay" promise should refer to reviewing this illustrative preview and the proposed scope. It must not imply that SiteBlitz will complete a usable website before payment.

Success test: Track preview-to-deposit conversion separately from Snapshot-to-deposit conversion. If five qualified previews produce no further progress, diagnose why before creating another five. A sample of five is not enough for a statistical conclusion, but it is enough to expose common objections or a weak sales explanation.

7. Thirty-day pilot — Question E

Verdict: Agree with running the three workstreams in parallel, but revise the sequencing and volume logic.

The first deposit is a legitimate 30-day objective. It is not a guaranteed outcome from 250–300 cold first touches.

At a hypothetical 3% positive-reply rate:

ILLUSTRATIVE FUNNEL — NOT ACTUAL SITEBLITZ PERFORMANCE

275
First touches
8.3
Positive replies at 3%
4.1
Quotes if half progress
1.0
Expected deposits if 25% accept
Assumptions are illustrative. The 3% positive-reply rate, 50% quote progression and 25% quote-to-deposit rate are not yet measured SiteBlitz results.

This is enough to justify a careful attempt at the first paid order, but not enough to validate a scalable acquisition business.

The three concurrent workstreams

Workstream 1 — Sending infrastructure: Begin setup and warm-up immediately. Keep the permanent client-reply mailbox separate. Do not use newly bought sending domains prematurely. Prefer an eligible native sending product over extra Workspace mailboxes bought only for cold outreach.

Workstream 2 — India email: Begin only once there is a compliant and operational sending account. If a suitable provider supplies an account with a genuinely aged, ready-to-send domain, the schedule below can start in week two. Otherwise, email first touches remain at zero until eligible.

Workstream 3 — Physical mail: Print and post 100 individually addressed letters to one India business category, divided into batches. This can proceed without waiting for email-domain maturity.

Exact first-30-day schedule

November 10 to December 9, 2026 · Weekdays only for planned outreach

Dates

	

New eligible email prospects

	

Posted cards/letters

	

Main work




Nov 10–13

	

0

	

0

	

Repair website and contact details, audit contacts, create card and QR design, configure infrastructure




Nov 16

	

0

	

Included in week's first batch

	

Final compliance and sending-account eligibility check




Nov 17–20

	

10/day × 4 = 40

	

25 across Nov 16–20

	

First eligible email test, replies and discovery




Nov 23–27

	

15/day × 5 = 75

	

25

	

Continue first touches, scheduled follow-ups and quotes




Nov 30–Dec 4

	

20/day × 5 = 100

	

25

	

Continue outreach, previews and deposit collection




Dec 7–9

	

20/day × 3 = 60

	

25

	

Final first-touch batch and preliminary pilot review




Total

	

275 first touches

	

100 letters

	

Subject to eligibility and operational capacity

The email figures are conditional maximums. If there is no eligible sending infrastructure, the corresponding email total is zero—not a reason to send from a prohibited or unready account.

Also, 20 new first touches per day does not mean 20 total outgoing messages. On mature campaign days, first touches plus scheduled follow-ups could approach 60 messages across the sending accounts. The 30/day-per-inbox proposed ceiling must include every touch.

Any follow-up falling on a weekend moves to the next working day. A reply, opt-out or OOO pause removes or reschedules all remaining touches.

Exact daily founder schedule

Standard working-day allocation

5 hr 30 min

09:00–09:30

Check replies, bounces, opt-outs and suppression

30 min

09:30–11:00

Qualify 15–20 leads and verify their observations

90 min

11:00–12:00

Review and send eligible emails; queue due follow-ups

60 min

12:00–12:30

Prepare, address and log physical letters

30 min

14:00–14:45

Respond to enquiries and hold discovery calls

45 min

14:45–15:30

Prepare quotations, previews and payment requests

45 min

15:30–16:00

Update CRM, measure metrics and set next actions

30 min

This is founder sales time, not the full business workload. It excludes initial engineering fixes and the hours needed to build paid websites. If a customer pays, fulfilling that promise takes priority over sending new first touches.

For a 1–2-person operation, that is essential. Otherwise the team can create more work than it can deliver.

Explicit stop rules

Signal

	

Decision




Unresolved platform or legal incompatibility

	

Stop the affected channel immediately




A guessed address enters the send queue

	

Stop that pipeline, fix the cause, re-audit




Two hard bounces among the first 50 attempts

	

Pause and investigate the list




Hard bounce exceeds 1% after at least 100 sends

	

Pause sending and verify the source




Any confirmed spam complaint

	

Pause affected sending account/campaign, investigate; do not wait for an arbitrary quota




No positive replies after 150 eligible first touches

	

Review targeting, observation quality and copy before increasing volume




Zero replies from 100 letters after an adequate delivery/response window

	

Do not automatically print another batch; inspect targeting and delivery first




Five qualified previews and no sales progress

	

Review the qualification gate and proposition




Two active paid projects exceed delivery capacity

	

Reduce or pause new outreach




Positive replies but no deposits after completed quote discussions

	

Investigate trust, price, payment process and scope—not sending volume

These thresholds are operating decisions, not statistical proof. The absolute bounce and complaint thresholds should also respect any stricter provider rule.

When to judge the pilot

December 9 is the end of the 30-day acquisition window, not the date when every sequence is complete.

A prospect first contacted on December 9 could receive Touch 2 on December 14 and Touch 3 around December 22, subject to working-day scheduling. Their no-reply closure would occur around December 29.

Likewise, physical letters posted in the final batch need time for delivery and response.

Therefore, use December 9 for the preliminary decision about list quality, founder workload, replies, quotes and any deposits already received. Evaluate completed sequence conversions at the end of December. Retain the separate, approximately eight-week gate for the originally agreed 1,000-contact/3,000-send infrastructure experiment.

My final pilot recommendation

I would not purchase six additional Google Workspace cold-outreach mailboxes and treat the risk as solved.

Instead, prepare the brand and lead systems, confirm the current cost and eligibility of a purpose-built native sending option, conduct the 100-letter test, and start India email as soon as a genuinely eligible infrastructure path is available.

If the founder chooses to fund both new-domain warm-up and a separate pre-warmed sending product, document the incremental costs and infrastructure ownership trade-off first. With zero paying customers, there is no economic justification for paying for overlapping systems without a deliberate test.

Final Round 2 decisions

Point

	

Result




1. Data hygiene

	

Agreed — implement at source, exclude suspect categories from pilot




2. Channel routing

	

Agreed conditionally — India B2B email and addressed postal test; WhatsApp only after valid user initiation/permission




3. Content

	

Agreed — 100 words max, verified observation first




4. Lifecycle

	

Agreed — OOO and call-request states added, payment gates unchanged




5. Countries

	

Agreed — Germany correction accepted; unknown countries held




6. Unique hook

	

Agreed — qualified 20-minute illustrative preview, five/week




7. Pilot

	

Agreed with revised sequencing — 275 conditional first touches and 100 postal letters across 30 days

Points still open

Founder: Select and confirm the actual sending product, including current costs, sending-domain age and account ownership.

Claude Code: Implement the hygiene changes, suppression logic and audit trail at the three identified code locations.

Legal adviser: Confirm the India B2B email procedure and the DPDP transition plan before automated expansion.

Founder: Obtain a local India Post classification and final price for the proposed personalised printed mailpiece.

Founder: Approve one business category and one geographic area for the first 100 physical letters.

Claude Code: Implement channel-specific consent, OOO, call-request, preview eligibility and payment states.

Founder: Confirm the three existing industry demos are suitable for short previews and that images used are authorised.

Claude Code: Complete country rules for IN, NL, ES, ZA, AE and SG before enabling automatic country routing.

Founder: Approve any incremental spending that departs from the November 9 infrastructure budget.

All partners: Review real deposit conversion and project delivery economics before considering the 1,000-email/day target.

Final principle: SiteBlitz should prove that it can repeatedly obtain paid deposits from verified, relevant businesses before investing in the machinery to reach thousands more. The next competitive advantage to build is not another sending account. It is a trustworthy, measurable path from a specific business observation to a signed scope and a paid deposit.
