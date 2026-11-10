ChatGPT said:
SiteBlitz — Complete Lead-to-Payment Growth System

Strategic review | 10 November 2026 | ChatGPT response to Claude Code and the founder

Overall verdict: Agree with the seven-point agenda, but challenge parts of the existing outreach infrastructure plan.

The objective should not be to contact the maximum number of businesses. It should be to identify businesses with a genuine need, reach them through an appropriate and permitted channel, communicate like a credible human professional, and convert them into paying customers through a repeatable system.

SiteBlitz has a potentially valuable global business database, but that does not automatically translate into a usable sales database.

According to the supplied project context, the current position is:

86.75 million business records across 247 countries.

Approximately 30.97 million records with an email address.

Approximately 41.96 million with a phone number but no email.

Approximately 13.83 million with neither email nor phone.

No paying customers yet.

Existing website offers of ₹7,999 and ₹17,999, plus custom quotations.

A known defect producing guessed rather than discovered email addresses.

These are project-reported figures, not independently audited database measurements.

Two corrections before approving the system

1. Disagree with treating multiple Google Workspace inboxes as an automatically acceptable cold-email scaling strategy.

Google Workspace's Acceptable Use Policy, last modified on 13 October 2025, prohibits unsolicited mass email. Gmail's program policies also restrict unsolicited commercial messages. Six inboxes instead of one do not eliminate this risk. 
Google Workspace
+1

I would retain the previously agreed pilot budget as a financial estimate, but make the sending-provider's explicit policy approval a mandatory requirement before activating any campaign.

2. Disagree with using publicly listed mobile numbers for unsolicited WhatsApp messages.

WhatsApp's Business Messaging Policy, updated 23 September 2026, requires both contact information provided by the recipient and opt-in permission. The requirement applies to the Business App as well as the Business Platform. A number appearing in Overture data is not sufficient permission. 
WhatsApp for Business

The opportunity is not lost. Those numbers can still support verification, qualification, and legally permitted alternative contact routes.

The following seven points define the proposed system. Legal interpretations are design guidance requiring jurisdiction-specific confirmation, not legal advice.

1. Data hygiene and fake email verification

Verdict: Agree — this must be completed before outreach begins.

The lead-generation application's reported practice of creating addresses such as info@companydomain.com is a serious defect. Those are plausible email patterns, not discovered contacts.

For a business with no verified email, having a guessed email is actually worse than showing no email: it creates false confidence and risks delivery failures.

Exact verification ladder

Step

	

Test

	

Required action




1

	

Duplicate business or contact

	

Merge into one company record; preserve existing suppression decisions




2

	

Email syntax invalid

	

Reject the address




3

	

Address was generated or guessed

	

Mark GUESSED; never send without independent confirmation




4

	

Domain or email service invalid

	

Reject when DNS confirms no valid delivery route




5

	

MX or mail-routing check

	

Continue only if a viable receiving route exists




6

	

SMTP or verification-provider check

	

Classify as valid, invalid, temporary error, or unknown




7

	

Catch-all domain

	

Hold for manual review; do not classify the mailbox as verified




8

	

Same email on many businesses

	

Investigate whether it is a real group address, franchise address, directory contact, or bad data




9

	

Source confirmation

	

Recheck against the business's official website or another credible first-party source




10

	

Legal and opt-out eligibility

	

Send only if this recipient, channel and country pass the compliance rules

Two technical qualifications matter. A domain without an MX record is not automatically invalid because SMTP can fall back to an A/AAAA record; an explicit null MX indicates that the domain does not accept email. SMTP acceptance also does not always prove that a specific person's mailbox exists. These distinctions are documented in RFC 7505 and RFC 5321 (2015 and 2008 respectively; high confidence).

Final contact statuses

I propose retaining six operational statuses:

Status

	

Meaning

	

Send?




CONFIRMED

	

Reply, reliable first-party confirmation, or equivalent direct proof

	

Only if legally permitted




VALID

	

Reputable verification reports deliverable; provenance recorded

	

Eligible for compliance review




RISKY

	

Catch-all, shared mailbox, or conflicting verification

	

Manual review




UNKNOWN

	

Verification inconclusive

	

No automatic send




INVALID

	

Rejected, nonexistent, or known permanently failed

	

No




SUPPRESSED

	

Opt-out, objection, or explicit do-not-contact

	

Never for marketing

A verification vendor's valid result is not proof of inbox placement, owner identity, or permission.

Important challenge: Do not automatically delete Gmail, Yahoo or other free-domain addresses. According to the supplied database counts, 79% of Indian businesses with an email have a free-mail address as their first email. Deleting them would discard a large portion of the Indian market. Verify the business association instead.

Data worth keeping

Keep a lean company record containing business identity, country, category, location, official website/social links, useful contact information, provenance URL, verification status/date, language evidence, channel permission, observed website need, and CRM state.

Keep interaction history, quotation/payment references and the suppression record separately.

Discard irrelevant personal attributes, old generated addresses, excessive raw scrape metadata, and redundant contact duplicates. Keep an auditable reason for rejection rather than silently deleting evidence.

The Overture Places data is published under different open-data licences depending on source; its openness does not itself provide consent for marketing. 
Overture Documentation

Cost and success test: Budget approximately 2–4 engineering days for the initial verification/suppression pipeline, subject to the existing code quality. The supplied pilot budget already includes ₹3,686 for a 10,000-address verification package, but that price should be rechecked. Audit 100 randomly selected accepted addresses manually before sending.

Proceed to the pilot only if the observed valid-email yield is at least 20%, with a hard-bounce rate of no more than 1% during controlled sending. These are proposed business thresholds, not legal standards.

2. Channel routing: email, phone, social, and unreachable businesses

Verdict: Agree, but disagree that WhatsApp is the default for phone-only records.

Channel selection must follow two independent tests: can we technically reach this business? and are we allowed to contact it this way?

Recommended routing

Lead condition

	

First route

	

Alternative

	

Avoid




Verified email

	

Relevant, compliant business email

	

Referral or permitted call

	

Generic mass blasts




Mobile number only

	

Check local calling rules and any existing opt-in

	

Consent-based WhatsApp, referrals, advertising

	

Unsolicited WhatsApp broadcasts




Social profile only

	

Organic engagement, allowed paid advertising, genuine relationship-building

	

Appropriate manual DM where permitted

	

Automated bulk DMs




Website/contact form only

	

Check whether the form permits commercial proposals

	

Relevant public business channel or referral

	

Mass contact-form submissions




Neither digital contact nor social

	

High-value manual research, local networking or permitted postal outreach

	

Inbound advertising

	

Expensive endless enrichment




Suspect email

	

Reverify and locate another published contact

	

Reclassify into the appropriate bucket

	

Sending to guessed addresses

A real mobile number is not the same thing as permission for WhatsApp, SMS or a marketing call.

WhatsApp: App versus API

Both the WhatsApp Business App and Platform require opt-in for business-initiated contact. The API additionally requires approved message templates for business-initiated conversations and uses a 24-hour customer-service window for ordinary free-form replies. 
WhatsApp for Business

My route is to acquire permission through customer enquiries, website forms, referrals, events, or properly labelled advertisements that invite people to contact SiteBlitz.

A suitable opt-in example on a lead form is:

I agree to receive messages from SiteBlitz about website services and quotations on WhatsApp. I can opt out at any time.

Make the checkbox optional, unchecked by default, and store its timestamp and disclosure text.

Once someone opts in, a simple first WhatsApp message can be:

Writing

Hello [Name], this is [Your Name] from SiteBlitz.

Thank you for agreeing to discuss your business website with us.

Could you tell me whether you need a new website or want to improve an existing one?

I can then suggest a suitable option and share the price.

Legal differences matter

United States: CAN-SPAM applies to commercial B2B email, including single messages; it requires truthful sender details, a genuine postal address, an opt-out mechanism, and honoring requests within 10 business days. This does not automatically authorize calls or texts. FTC official guidance, existing law verified November 2026, high confidence. 
Federal Trade Commission

United Kingdom: PECR generally permits marketing emails to corporate subscribers without prior opt-in, but sole traders and certain partnerships have different protections. Personal data use still needs an appropriate UK GDPR basis. Check TPS/CTPS before live marketing calls. ICO guidance, checked November 2026, high confidence. 
ico.org.uk
+1

India: Under TRAI's TCCCPR framework, commercial calls/SMS face sender-registration, preference and related telecom rules. Ordinary personal SIMs are not an acceptable route for unsolicited bulk telemarketing. 
Government of India
+1

Germany: Section 7 of the UWG generally requires prior express consent for advertising by email, subject to its narrow existing-customer exception. 
UWG)

Canada: CASL requires consent or a legally valid exception/implied-consent basis, identification, and unsubscribe. Merely finding an address in a dataset is insufficient. 
CRTC

Australia: The Spam Act requires express or properly inferred consent. Relevant publication may be a factor, but consent must be defensible. ACMA guidance, checked November 2026, high confidence. 
ACMA
+1

LinkedIn explicitly restricts unauthorized automated messaging and scraping. Do not build automation that impersonates human platform interactions. 
LinkedIn

What to do with the 13.83 million records lacking email and phone

The supplied counts separate them into three useful groups:

Social profile only

10,057,454

Website only

1,551,632

No listed contact channel

2,216,744

Shares of the 13.83 million with neither email nor phone, calculated from supplied project counts.

The social-only group is not worthless. It is potentially valuable for a website studio: many businesses may already be using social media as their only online storefront.

But a 1–2-person team should not manually research all 10 million. Build a qualification score that prioritizes visible commercial activity, no verified website, suitable business type, location, and a permitted way to engage.

Cost and success test: Start with 50 manually reviewed leads per channel. Record time per qualified conversation, percentage that replies positively, and paid conversions. Kill any channel whose acquisition cost and time consistently exceed the expected contribution from a sale.

3. Cold email content: how to sound human and earn replies

Verdict: Agree. The content deserves more attention than sending volume.

I disagree with the idea that the best way to sound human is to make AI writing deliberately imperfect.

Human-sounding writing comes from three things: a true observation, an offer relevant to that specific business, and a reasonable request. Artificial spelling mistakes, exaggerated friendliness, and fabricated familiarity reduce trust.

Recommended format

Element

	

Recommendation




Subject

	

4–8 meaningful words, clear and truthful




Greeting

	

"Hello [Name]," or simply "Hello,"




First sentence

	

One specifically verified observation about their business




Body

	

Introduce SiteBlitz and explain the business benefit




Offer

	

Fixed-scope website with a price quoted before work




CTA

	

One simple question that can be answered in one sentence




Length

	

Approximately 70–120 words before signature




Signature

	

Real sender, SiteBlitz identity, working reply channel, genuine postal address




Opt-out

	

Easy and clear in every marketing message

Don't use invented testimonials, false claims about leads or Google rankings, fake deadlines, or a Re: prefix on the first email.

Touch 1 — Day 1: Introduction

Use this version only where the business's social profile or listing has been checked and genuinely does not show an official website.

A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

I came across [Business Name] through [Facebook / Instagram / business listing].

I noticed that [specific, verified observation]. I couldn't find an official website linked there, so I thought I'd reach out.

I'm [Your Name] from SiteBlitz. We build simple, professional websites that help customers find business details, understand services, and get in touch.

Would you be interested in seeing a suitable website option and its fixed price?

Best regards,
[Your Name]
SiteBlitz
[Working website or business contact]
[Actual business postal address]

If you'd prefer no further emails, simply reply "stop".

Why this version: It opens with genuine context, says what is being offered, and asks permission to discuss rather than demanding a meeting.

Touch 2 — Day 6: Useful follow-up

Reply in the original email thread.

Re: A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

Just following up on my earlier message.

For [Business Name], a simple website could bring together [services / products], location details, and a clear way for customers to contact you.

It wouldn't need to be complicated. We could start with the essential pages and agree on the price before any work begins.

Would you like me to send a short outline?

Best regards,
[Your Name]
SiteBlitz
[Working business contact]
[Actual business postal address]

If you'd prefer no further emails, reply "stop".

The bracketed details must be selected from actual facts. Do not invent products or services.

Touch 3 — Day 14: Final follow-up
Re: A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

I'll leave this with you after this message.

I thought a straightforward website might be useful for [Business Name], especially for customers who want to find your business information in one place.

If it's something you're considering, you're welcome to reply whenever convenient. I can share the options and price.

Thank you for your time.

Best regards,
[Your Name]
SiteBlitz
[Working business contact]
[Actual business postal address]

I won't send further follow-ups. You can also reply "stop" at any time.

Day 21: If there is no response, close the prospecting sequence and do not automatically start another campaign against the same business.

This keeps the previously agreed pilot at three messages per prospect.

Content personalisation rules

Only personalise what can be supported by a source. Useful variables are the company's actual business activity, a real location or service, evidence that customers currently depend on social media, and a verified website problem.

A weak opener is: "I was extremely impressed by your amazing business."

A better opener, when factually true, is: "I found your menu on Instagram, but couldn't find a website link with your opening hours."

The second sentence demonstrates relevant research without pretending there is a relationship.

Cost and test: Expect roughly 3–5 minutes of human review per qualified first-touch lead initially, plus automated drafting. At 1,000 prospects, that is about 50–83 hours of review. This is an operational estimate, not measured SiteBlitz performance.

Measure positive replies and paid deposits, not open rates. Google's guidance explicitly notes that third-party open-rate measurements may be inaccurate. 
Gmail Help

Keep the better-performing template only if it increases qualified conversations without higher complaint or bounce rates.

4. Complete lifecycle: from discovered business to final payment

Verdict: Agree. This is the central operating system SiteBlitz needs.

A lead should never sit in an undefined status such as "follow-up pending" without a next action, owner, and due date.

Recommended CRM state machine

FOUND → DEDUPLICATED → QUALIFIED

CONTACT VERIFIED → CHANNEL APPROVED

TOUCH 1 → TOUCH 2 → TOUCH 3

Stop immediately if the recipient replies or opts out

Positive reply

Discovery

No / opt-out / bounce

Closed or suppressed

SCOPE AGREED → QUOTE ACCEPTED → DEPOSIT PAID

READY TO BUILD → BUILD → REVIEW → BALANCE PAID

LAUNCH → HANDOVER → AFTER-DELIVERY SUPPORT

Proposed state sequence, not a claim about implemented code. Each state change should be recorded with its time and responsible person.
Day-by-day sales schedule

Day

	

Condition

	

Action




Day 0

	

New business discovered

	

Deduplicate, verify business and contact, check country rules




Day 1

	

Qualified and outreach permitted

	

Send first message




Day 2–5

	

No reply

	

Wait; don't chase across multiple channels




Day 6

	

No reply

	

Send first follow-up




Day 7–13

	

No reply

	

Wait




Day 14

	

No reply

	

Send final follow-up




Day 21

	

Still no reply

	

Close sequence




Any day

	

Positive reply

	

Pause all scheduled marketing and enter sales discussion




Any day

	

Rejection or opt-out

	

Stop, suppress and record




Any day

	

Hard bounce

	

Suppress that address

The day numbers are a recommended experiment, not evidence that a 5-day interval is universally optimal.

Every common reply branch

The system should classify replies and prepare these next messages for human review.

Customer reply

	

Proposed next message/action




Interested

	

"Thank you. Is this for a new website or an existing one? And what is the main thing customers should be able to do on it?"




How much?

	

"For clients in India, our Launch package is ₹7,999 for one page, and Business is ₹17,999 for three pages. Domain and hosting are separate. If you tell me what pages you need, I can confirm the suitable option." For other countries, send an approved local-currency quote instead.




Send details

	

"Of course. We offer a one-page Launch website and a three-page Business website, with scope and price agreed before starting. Could you tell me your business type and preferred pages so I send the relevant details?"




We already have a website

	

"Thank you for clarifying. Are you satisfied with it, or is there something specific you'd like improved? If it's working well, I won't take more of your time."




Not now

	

"Understood, thank you. Would you prefer that I close this for now, or is there a particular month when you'd welcome another message?" No scheduled recontact unless they request it.




No / not interested

	

"Understood. Thank you for letting me know." Stop further marketing to that contact.




Wrong person

	

"Thank you for telling me. Is there a public business contact for website-related enquiries, or would you prefer I leave this here?"




Hard bounce

	

No customer message. Mark invalid, investigate the source, and suppress the failed address.




Unsubscribe / stop

	

Suppress immediately. Do not wait for the legal maximum or send a new sales message.




Budget too low

	

"I understand. We can review the scope and see whether a smaller website fits. I wouldn't want to promise features that don't fit the price."




Please call me

	

Confirm the preferred time, telephone number and permission to call; log the request.

An AI classifier can propose the branch, but ambiguous replies, objections and commercial negotiations should go to a human.

Requirements to collect after genuine interest

Do not ask for 20 fields in the first message. Use a short discovery conversation first.

At the quotation stage, collect the legal/business name, decision-maker, country, purpose of website, preferred pages, required functions, expected delivery schedule, available budget and whether it is a new build or redesign.

After the client accepts the quote, collect the logo, approved text and images, products/services, address/contact details, preferred design references, domain/hosting information, authorised access and any legal content requirements.

Do not ask clients to email passwords. Use secure delegated access where possible.

Exactly when to request payment

Moment 1 — The scope and price are accepted

Send the written agreement and deposit invoice. Do not begin design or development until payment is confirmed.

LAUNCH DEPOSIT

₹4,000
₹7,999 total

BUSINESS DEPOSIT

₹9,000
₹17,999 total

Moment 2 — Ready-to-build is confirmed

Start the delivery clock only after the agreed pages/features, required content, access, deposit and start date are all confirmed. The stated targets are two working days for Launch and seven for Business.

Moment 3 — Staging review is accepted

Show the working site in a review environment. Complete the one included consolidated revision round, obtain written approval and issue the balance invoice.

LAUNCH BALANCE

₹3,999

BUSINESS BALANCE

₹8,999

Moment 4 — Final payment is confirmed

Publish the website, transfer or document agreed access, deliver handover information, and close the delivery milestone.

The client agreement should explicitly say that the remaining payment is due before public launch and final handover, that customer-caused content delays pause the delivery clock, and that additional features require a new written quotation.

Custom projects continue to use the milestones defined in their individual quotations.

After-delivery lifecycle

On launch, provide a handover email covering the website URL, agreed features, access/ownership, domain and hosting arrangements, and any written support terms.

Check for genuine delivery defects within the agreed warranty/support window. Do not silently promise unlimited ongoing changes. Invite a factual review only after a real successful delivery, and ask permission before using the work publicly as a case study.

Cost and success test: Track time from positive reply to scope agreement, scope agreement to deposit, deposit to ready-to-build, and ready-to-build to launch. The most important sales metric is quote-to-deposit conversion, not a CRM stage called "interested."

5. Countries, languages, local timing and international pricing

Verdict: Agree with international expansion. Disagree with automatically translating messages based on country alone.

A business's country tells us which legal rules to investigate. It does not reliably tell us which language its owner prefers.

Country permission matrix

Market

	

Recommended initial policy

	

Confidence




India

	

Prioritise permission-based contact, referrals, inbound enquiries and established business relationships

	

High for TRAI restrictions; legal review needed for email/data




US

	

Target relevant businesses through compliant B2B email, with CAN-SPAM controls and compatible provider terms

	

High




UK

	

Start with verified limited companies/LLPs; exclude uncertain sole-trader records from automatic cold outreach

	

High




France

	

Relevant professional B2B email may be permissible with notice, lawful basis and effective objection rights

	

High




Germany

	

No first-touch cold marketing email without a qualifying permission or narrow legal exception

	

High




Austria / Greece

	

Manual legal review before outreach

	

Medium




Canada

	

Only where CASL consent or a properly documented exception/implied-consent basis exists

	

High




Australia

	

Only with evidence supporting express or valid inferred consent

	

High




Other countries

	

Hold until the applicable country/channel rules are reviewed

	

Not yet assessed

The French regulator CNIL clarified B2B electronic prospecting conditions on 10 June 2026. German UWG Section 7, as amended in February 2026, imposes stricter prior-consent requirements. These are materially different approaches despite both countries being in the EU. 
CNIL
+1

The EU GDPR's legitimate-interest basis is not a universal override of national electronic-marketing rules. 
European Data Protection Board

India also has a transitional privacy-law issue: the November 13, 2025 DPDP notification introduced a phased commencement. Major personal-data processing provisions are scheduled for May 13, 2027, with another group scheduled for November 13, 2026. This should be reviewed now rather than waiting until the final phase. 
E-Gazette

Language selection algorithm

Use this priority:

Language evidence hierarchy

1. Business's own communication language

Highest confidence

2. Language of its official website and recent social posts

3. Explicit recipient preference

4. Region and local language evidence

5. Country-level language default

6. Manual review if confidence is insufficient

For example, a business in Mumbai may use English, Hindi or Marathi. A business in Quebec may prefer French, while another Canadian business may prefer English. A UAE business's professional communication may be English or Arabic.

Do not infer language only from a telephone country code, and do not assume gender or an honorific.

AI can draft translations, but the first 10–20 messages for each new language/market should receive native or professionally proficient review. Preserve the meaning and formality of the original rather than translating words mechanically.

Proposed local send-time test: Tuesday–Thursday, 9:00–11:30 AM and 2:00–4:30 PM in the recipient's timezone. This is a test hypothesis, not a verified universal best time. Avoid local public holidays and prohibited calling hours.

Cost: initial local-language QA and timezone/country-rule maintenance. Benefit: fewer embarrassing errors and more relevant conversations. Test using positive replies and translation corrections, separated by language.

Pricing outside India

The founder context correctly says SiteBlitz has no approved international price list.

I see three choices.

Option

	

Mechanism

	

Main weakness




A. Currency conversion

	

Convert approved INR package prices and add actual fees

	

Local support and currency risk may be underpriced




B. Country-specific prices

	

Set fixed local prices after market and delivery-cost research

	

More administration and pricing maintenance




C. Quote-only initially

	

Evaluate each international request and send an approved fixed quotation

	

Slower than showing an instant price

Recommendation: Option C for the first international clients. After 5–10 genuine quotations and completed projects, evaluate whether country-specific fixed prices make economic sense.

Do not publish arbitrary GBP, USD or EUR prices to make the site appear international.

For international payments, verify the actual processor's eligibility and required documentation before quoting a payment method. Stripe, for example, currently describes Indian account creation as invite-only, with additional requirements for international transactions. 
support.stripe.com

The Reserve Bank of India's new export/import framework took effect on October 1, 2026. An accountant and authorised bank should confirm SiteBlitz's international invoice, foreign-receipt and applicable tax treatment under the current rules. 
Reserve Bank of India

6. The unique hook: what will make the business owner pay attention?

Verdict: Agree that a distinctive approach matters. Disagree with making AI-cloned voice the primary hook.

A unique presentation is useful only when it increases trust or makes the business problem clearer.

A synthetic voice note received unexpectedly from a stranger could instead create suspicion.

Evaluate the options

Idea

	

Effort per prospect (estimate)

	

Main benefit

	

Main concern

	

Decision




Personalised text observation

	

2–5 minutes

	

Low-friction relevance

	

Poor facts ruin trust

	

Use first




Mini business website assessment

	

5–10 minutes

	

Demonstrates understanding

	

Research workload

	

Test




Human-recorded voice message

	

1–3 minutes

	

Genuine personal connection

	

Intrusive if unsolicited

	

After engagement




AI-cloned founder voice

	

Initial setup plus review

	

Can be produced at scale

	

Authenticity and disclosure concerns

	

Not first




Short annotated screen video

	

5–10 minutes

	

Visual explanation of a specific problem

	

Higher production cost

	

Test on interested leads




Free homepage concept

	

Up to 3 hours based on existing cap

	

Tangible demonstration

	

Free-work burden

	

Restrict




Before/after illustration

	

15–45 minutes if genuinely tailored

	

Shows possible design improvement

	

Must not misrepresent previous work

	

Qualified leads only

These are planning estimates, not measured production times.

What the evidence actually supports

Mailchimp's guidance states that most email clients do not reliably play embedded audio or video; linking to externally hosted media is the more dependable approach. Therefore, an "audio note inside every email" is technically weak. 
Mailchimp
+1

There is some research support for personalised visual content. A published study of generative-AI video advertisements found improved engagement compared with alternative ad formats. But that was an advertising experiment, not a study of cold B2B website-development emails. Its result cannot establish that cloned voice or personalised video will increase SiteBlitz's paid orders. 
DOI

I have not found convincing independent evidence that a cloned founder voice outperforms an authentic recording for this specific use case.

If synthetic voice is later tested, use only an authorised voice, clearly label synthetic recordings when appropriate, and never imply a personal recording or relationship that did not occur.

My proposed differentiator: The SiteBlitz Opportunity Snapshot

Instead of sending every business a generic pitch, create a small evidence-based assessment.

ILLUSTRATIVE SALES CONCEPT

Your online presence, simplified

Prepared for [Business Name]

What we found

One genuine, sourced observation from the business's public presence

What could improve

One specific opportunity, such as making services, service area and contact details easier to find

What SiteBlitz proposes

A simple website scope, an appropriate package and an upfront quotation

A proposed format, not an assessment of any actual business.

The snapshot should be short, accurate, and ideally produced only after a prospect expresses some interest. A sample visual can use an explicitly labelled illustrative design, not a claimed past-client result.

The founder's previous decision allowing three free homepage concepts per week or nine hours of work is potentially inconsistent with the new paid-first direction.

I recommend suspending that free-work programme until the first paid customers establish a reliable sales and delivery process. The founder must approve any change to that existing decision.

The experiment

After sufficient qualified, legally permitted conversations exist, compare a text-only explanation against the same explanation with an optional short, genuine screen video.

Randomise recipients within the same market and business type. Measure how many request a quote and ultimately pay a deposit, as well as the time required to prepare the material.

A small 25–50-person sample per approach can identify obvious practical problems, but it cannot reliably prove a modest conversion-rate advantage. Larger tests will be necessary.

Decision: Be unusually relevant, not artificially impressive.

7. A 30-day paid-first pilot

Verdict: Agree. The first 30 days should establish that real people will pay, not prove that 1,000 emails per day is possible.

Which market should come first?

I would separate the first revenue test from the first scalable international email test.

First paid-sale market

India — Mumbai-area local service businesses

Choose active, owner-operated businesses that lack a verified website and can benefit from a clear service-and-enquiry page. Begin with warm introductions, referrals and voluntary enquiries. India already has approved INR package prices and can be served without cross-border payment setup.

UK — verified limited-company home-service businesses

This is my proposed first international B2B email segment: cleaning, landscaping and property-maintenance companies with public business contact details, active trading signals and no verified website. Confirm corporate status using Companies House. Start only once the lawful basis, approved quotation process and compatible email provider are ready.

The image examples are illustrative categories, not specific recommended businesses.

This approach tests paid demand using the market SiteBlitz can currently fulfil most easily, while preparing a more repeatable international workflow.

Thirty-day execution plan

Period

	

Founder and system responsibilities

	

Target daily activity




Days 1–5

	

Fix website prices and broken contact details; confirm trademark/domain, terms, payment collection, deliverability and contact suppression

	

No new cold sends; verify first 100 records




Days 6–10

	

Build the first relevant India shortlist; request introductions; publish proof-of-process content; review permitted email candidates

	

5 warm introduction requests/day




Days 11–14

	

Hold discovery discussions, prepare fixed-scope quotes, begin approved email outreach only if infrastructure and permission gates pass

	

5–10 new eligible emails/day, 1–2 discovery conversations/day as capacity permits




Days 15–21

	

Continue qualification, first follow-ups, quotes and deposits; review early responses and objections

	

10–15 new eligible emails/day, up to 5 consented WhatsApp conversations/day




Days 22–30

	

Complete sales follow-ups, collect deposits, deliver accepted paid projects, review economics

	

15–20 new eligible emails/day if justified, plus scheduled follow-ups; 2 discovery slots/day

Email numbers are caps for this initial test, not quotas to fill with poor prospects. If no suitable sending provider and legal basis are confirmed, email volume remains zero.

All activity is manual or approval-controlled for now. Nothing has been authorised to send or deploy.

Why I would not force 3,000 sends into the first 30 days

The previously agreed Level-1 pilot involves 1,000 contacts and three touches, with a three-week sender ramp and a broader evaluation around week eight.

That is a different experiment from proving the first paid conversion in 30 days.

Trying to finish the entire 3,000-send test within the first month risks compromising verification, relevant content and reply handling. Keep the previously agreed eight-week evaluation horizon, subject to provider-policy approval.

Budget

From the supplied November 9 infrastructure review:

Cost

	

Previously estimated amount




Level 0: brand domain and primary business inbox, first month

	

₹1,178




Level 1: complete pilot stack including Level 0, first month

	

~₹12,239




Level 1: subsequent monthly cost

	

~₹5,260




Vercel Pro, if required for commercial hosting

	

~₹2,230/month

These are inherited budget estimates, not newly verified vendor quotations. They exclude founder labour, development, sales time, transaction fees and other costs not specified in the review.

Success criteria

Retain the earlier deliverability and conversion gates, while making them more precise.

Metric

	

Proposed decision threshold




Verification

	

At least 20% valid-email yield from the defined candidate pool




Hard bounce

	

No more than 1% of attempted messages




Gmail user-reported spam

	

Target below 0.10% when a sufficiently meaningful measurement is available




Positive replies

	

At least 3% of unique eligible contacts reached, measured by the end of their response window




Paid conversions

	

Earlier gate of at least 3 paid orders per 3,000 sends, evaluated after the full pilot




Compliance

	

No knowingly unauthorised messaging or policy-violating send method




Contribution margin

	

Target at least 30% after attributable acquisition, delivery labour and direct costs; proposed business threshold




First 30 days

	

Aim for the first genuine paid deposit and completed customer discovery, without treating a small sample as statistically conclusive

Google's sender recommendations distinguish the target of keeping spam below 0.10% from its requirement to remain below 0.30%. A missing Postmaster measurement must not be interpreted as zero complaints. 
Gmail Help

Why the existing three-order target is not enough

Using the current INR packages, three customers would generate:

3 LAUNCH ORDERS

₹23,997
Gross sales, not profit

3 BUSINESS ORDERS

₹53,997
Gross sales, not profit

If acquisition infrastructure costs approximately ₹17,499 across the first two months under the supplied estimates, three Launch orders leave only ₹6,498 before delivery labour, hosting and other expenses.

That is why "three paid orders" alone cannot justify scaling.

The pilot must also reveal delivery time, scope creep, quotation acceptance, failed-payment rates and whether the founders have enough hours to fulfil new orders.

Go / change / stop decisions

Continue: Qualified positive replies meet the 3% target over a meaningful sample, real deposits arrive, compliance is maintained, and project contribution is positive.

Change: Delivery is healthy but positive replies remain weak, or replies are positive but quotes do not convert. Revise the business segment, offer or price proposal one variable at a time.

Stop the affected channel immediately: Legal or platform-policy failure, a material suppression failure, repeated harmful complaints, or bounce rates above the agreed safety gate.

Final decision for Claude Code

I recommend a paid-first, compliance-gated, research-supported sales system, with these priorities:

Stop fabricated emails and retain contact provenance.

Make eligibility for each country and channel a hard requirement, not merely a lead-score adjustment.

Fix SiteBlitz's live website, pricing and reply channel before outreach.

Use short, genuine, context-specific email and a maximum three-touch sequence.

Route every reply into a clearly defined CRM action, quotation and payment milestone.

Make deposits mandatory before website production.

Prefer evidence-based opportunity snapshots over unsolicited synthetic voice or excessive free concepts.

Validate the first paid conversions before pursuing the previously discussed 1,000-email/day capacity.

The strongest competitive advantage is not the size of the database. It is the ability to turn reliable observations about real businesses into commercially useful proposals at a delivery cost that makes sense.

Points still open

#

	

Unresolved decision

	

Responsible party




1

	

Confirm actual code-level source of guessed emails and implement verification statuses

	

Claude Code




2

	

Audit which previously used list produced spam or bounces

	

Founder + Claude Code




3

	

Obtain jurisdiction-specific advice on data collection, India DPDP and international prospecting

	

Legal adviser




4

	

Confirm email provider terms explicitly permit the intended sending behaviour

	

Founder




5

	

Clear the SiteBlitz trademark, purchase approved domain and correct production website

	

Founder + Claude Code




6

	

Approve quote-only international pricing and a working overseas payment route

	

Founder + accountant




7

	

Decide whether to suspend the existing free-homepage-concept allowance

	

Founder




8

	

Measure real production hours and direct cost per Launch and Business website

	

Founder + Claude Code




9

	

Approve the India paid-sale segment and conditional UK corporate email segment

	

Founder




10

	

Decide whether the first 30 days will use the full paid outreach stack or only the lower-cost permission-based routes

	

Founder




11

	

Implement the actual CRM states, suppression checks, quote/deposit triggers and audit trail

	

Claude Code




12

	

Collect genuine pilot results before approving the later volume-scaling decision

	

All partners

Status: Strategy proposed and externally researched. No messages sent, tools purchased, code changed or workflows deployed.
