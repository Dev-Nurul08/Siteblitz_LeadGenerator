ChatGPT said:
SiteBlitz email engine v2: point-by-point response to Claude Code

My overall position: agree with building a one-click, AI-assisted conversation engine; disagree with treating the current plan as ready to send. The system should optimise for qualified conversations and profitable website projects, not the number of emails dispatched.

The supplied documents describe missing sending infrastructure, reply handling, verification, sender identity and a truthful production website. Consequently, the presently approved sendable number is zero until those launch gates pass. This is a readiness decision, not a rejection of the vision. I have reviewed the supplied material, not audited the repositories or independently confirmed their feature claims. 
Pasted text

External rules below were checked on 12 November 2026. Citations link to the source URLs. “High confidence” means the primary source clearly supports the stated rule; whether a particular campaign satisfies it still requires application-specific review. Legal conclusions are design inputs for counsel, not legal advice.

1. Personas — agree with the framework; disagree with treating simulated reactions as evidence

The ten personas are useful hypotheses. However, industry, inbox reader, device and legal status should be separate attributes, not one assumed personality. A receptionist might screen a salon’s email; an owner might personally read a restaurant’s info@ inbox.

The table below is a reasoned simulation, not observed customer research. Behavioural confidence is low until tested. Samples A, B and C are salon-specific, so they are unsuitable verbatim for the other industries; those rows assess their structures after truthful adaptation. The samples and personas come from the supplied position paper. 
Pasted text
 
Pasted text

Persona	Who reads; likely device hypothesis	First three-second question	Delete / spam trigger	Forward / reply trigger	Verdict on A / B / C
P1: Salon owner	Owner or family member; phone	“Is this about my business, and is it useful?”	Criticism, generic compliments, a meeting request before explaining value	A recognisable observation and a simple services/enquiry-page offer	A: strongest starting structure, but soften “anywhere.” B: reject unsupported claims about prices. C: test later, with optional audio.
P2: Coaching centre	Administrator first, owner second; phone or desktop	“Should I forward this to the owner?”	Unsupported claims about lost admissions or a vague redesign pitch	Exact page/problem plus a sentence explaining the proposed fix	A: adapt around verified usability evidence. B: summary structure useful; present wording unsuitable. C: screenshot may help forwarding.
P3: Retail showroom with an unavailable site	Owner or manager; phone	“Is this real, or someone trying to frighten me?”	“Your domain expired” inferred from one failed request	Dated, repeatable observation with an acknowledgement that it may be temporary	A: use precise diagnostic wording. B: accusatory framing is risky. C: evidence can help, but must not resemble a security scare.
P4: US clinic practice manager	Practice manager or receptionist; desktop/phone	“Who is this, and why should the dentist see it?”	Patient-related assumptions, unverifiable claims, pressure or sensitive information	Clear business purpose, verifiable sender and narrow non-clinical scope	A: requires US-compliant identity/advertising treatment. B: reject overclaims. C: possible later, excluding patient information.
P5: Restaurant shared inbox	Staff, manager or owner; mixed devices	“Is this a booking, supplier matter or advertisement?”	A subject that disguises a pitch as a customer enquiry	A self-contained, forwardable explanation	A: adapt and identify the commercial offer. B: concise summary could work after correction. C: useful only when understandable without earlier context.
P6: UK/Australian trades business	Owner or office administrator; phone	“Will this help, and how much work is responding?”	Marketing jargon, false urgency, compulsory call booking	A specific improvement and an easy reply	A: adapted structure is plausible. B: avoid criticism. C: optional, not audio-dependent. Legal eligibility must come first.
P7: Business with a working website and no relevant problem	Any reader	“Why are you contacting me?”	Invented shortcomings	No qualifying trigger under the current offer	A/B/C: do not send. Do not manufacture a problem to fill the batch.
P8: Digital agency owner	Owner or delivery lead; desktop/phone	“What capability, terms or capacity do you offer?”	A consumer-style website pitch	Clear white-label scope, ownership, handover and commercial terms	A/B: wrong offer as written. C: a relevant capability example may work, but belongs in a separate campaign.
P9: Assistant / gatekeeper	EA, receptionist or family member; mixed devices	“Can I explain this to the decision-maker?”	Ambiguous request, missing identity, reliance on opening a link	A sentence containing business name, observation, offer and requested action	A: fairly forwardable. B: best summary concept, weakest factual discipline. C: email must remain meaningful without clicking.
P10: Mailbox filtering system	Technical system, not a human persona	Not applicable	Authentication, reputation, policy or content problems	Not applicable	A/B/C: inbox placement cannot be predicted by role-play. Test authentication, rendering, provider responses and real campaign outcomes.
What I would change in the samples

A needs bounded observation language. “I couldn’t find a website anywhere” implies a more exhaustive search than the system can establish. Prefer: “Your Instagram profile had no website link when checked,” provided that exact observation exists.

B should not launch. Finding no website does not establish that customers cannot find prices. Instagram might already contain them. Saying the new page “shows up when someone searches your name” also promises an outcome not established by the evidence.

C needs consistency. It promises to send the price later even though A already gives a starting price and the proposed snapshot contains pricing. Change the next step to scope and delivery details. A reusable vertical recording must be described as a general recorded overview—not a bespoke voice message.

Proposed test

Use the two models to find contradictions and confusing wording, then show variants to 10 consenting business readers. After five seconds, ask them to explain the sender, reason for contact, offer and next action.

My proposed acceptance threshold is 8 of 10 correctly explaining all four, with no material misunderstanding of price. That is a usability gate, not proof of conversion.

Cost and upkeep: no additional specialist software is necessary; recruitment and review require human effort. Refresh the hypotheses from actual replies. Beneficiaries: recipients and founders. Main risk: optimising for simulated preferences instead of real behaviour.

2. Email anatomy — agree with simplicity; disagree that a particular format can guarantee inbox placement

There are four separate questions:

Is sending lawful? Does the sending provider permit it? Will the receiving provider accept it? Will the reader find it worthwhile?

Passing one does not establish the others. Google explicitly states that an email provider cannot guarantee passage through Gmail’s spam filters. 
Google Help

Provider requirements: corrections and launch baseline
Provider	Verified requirement or correction	Date and confidence
Personal Gmail	All senders need SPF or DKIM, valid forward/reverse DNS, TLS and low spam rates. Bulk senders need SPF and DKIM, DMARC/alignment and one-click unsubscribe for marketing/subscribed messages. Implement the stronger authentication configuration from the beginning.	Baseline effective 1 February 2024; current guidance checked. High. 
Google Help

Yahoo	Its published requirements cover authentication, complaint rates and easy unsubscribe; bulk requirements include SPF, DKIM and DMARC. Yahoo does not publish a simple numerical definition of “bulk” in its FAQ.	Current, undated guidance. High on these requirements; do not invent a volume exemption. 
senders.yahooinc.com
+1

Outlook.com consumer accounts	The research attachment’s “noncompliant mail goes to Junk” statement is outdated. Microsoft’s updated announcement says qualifying high-volume authentication failures are rejected, with error 550 5.7.515.	Enforcement from 5 May 2025. High. 
TECHCOMMUNITY.MICROSOFT.COM

“Plain text,” “no links” and “under 100 words” should be testing defaults—not claims about universal spam-filter rules. The supplied research itself says it found no provider statement or controlled test demonstrating that tracking pixels necessarily damage inbox placement. Remove pixels for privacy and unreliable measurement; do not present a universal deliverability penalty as established. 
Pasted text

Recommended anatomy by touch
Element	Touch 1	Touch 2	Touch 3
Purpose	Establish relevance and offer one small next step	Supply additional evidence or a useful example	Close respectfully
Subject	Business name plus truthful, non-alarmist topic	Actual continuation of the same thread	Same genuine thread
Opening / preview	Specific observation and its limited scope	New information, not “just following up”	Brief closure
Summary	Integrate into the first two sentences; do not repeat the whole message under “In short”	Explain the snapshot in one sentence	Usually unnecessary
Offer and price	Narrow deliverable; approved starting price and material exclusions	Same price/scope, or an explicitly explained update	No invented discount or deadline
CTA	One easy question	One next action	No pressure; optionally allow the recipient to reopen later
Media	Text-first; no promotional attachment	At most one relevant snapshot link	Usually none
Length	Retain 60–85 body words as a starting target	40–70	30–50

These proposed body lengths follow the supplied specification. Legally necessary identity, notice and unsubscribe information must not be removed to satisfy a total word limit. 
Pasted text

Corrected illustrative first touch

The following uses the document’s fictional business and sender. It is not send-ready: the observation and ₹7,999 offer must be verified and approved.

Subject: Glow Studio — a services-page idea

Hello Glow Studio team,

Your Instagram profile had no website link when I checked it. I offer a simple page that puts your services, prices and appointment-enquiry button in one place.

I’m Ravi from SiteBlitz, a small web studio in Gujarat. Website setup starts at ₹7,999; domain and hosting cost extra.

Would a short outline for Glow Studio be useful?

Ravi | SiteBlitz
[Actual reply address and postal address]
Reply “stop” to opt out.

For US campaigns, the message must also clearly disclose its advertising nature; CAN-SPAM is not limited to bulk mail and has no B2B exemption. A postal address and functioning opt-out are substantive requirements, not optional trust decorations. Source: FTC’s current compliance guide; high confidence. 
Federal Trade Commission

Unsubscribe and validator changes

Implement RFC 8058 with an HTTPS unsubscribe endpoint and the appropriate headers, covered by a valid DKIM signature. A mailto: link alone does not implement that mechanism. Source: RFC 8058, January 2017; high confidence. 
RFC Editor

Amend “no links in touch 1” to “no promotional links in touch 1; compliance links are permitted or required.” A privacy notice or unsubscribe facility must not be blocked by the writer validator.

Keep factual, identity, consent and suppression checks strict. Treat punctuation preferences—such as banning semicolons or em dashes—as style rules, not evidence-backed spam protections.

Cost and upkeep: low incremental infrastructure cost, but offer versions and legal footers need maintenance. Success test: every factual claim has supporting evidence; every seeded test message authenticates correctly; unsubscribe works end to end. Risk: technically perfect messages can still be unwanted.

3. Creative and interactive layer — agree with a snapshot; disagree with novelty for its own sake

Put the rich experience on a trustworthy page, not inside the first unsolicited email. The email must deliver enough value without requiring a click.

Option	Decision	Deliverability, trust and legal assessment	Effort / placement
One-line summary	Build now	Low complexity; useful to owners and assistants. No promised reply-rate improvement.	Low; touch 1 onward
Audio attachment	Do not use in the pilot	No demonstrated universal audio-file penalty, but it asks a stranger to download/listen before establishing trust.	Avoid initial maintenance and testing burden
Audio link	Optional within the snapshot	Give a transcript; no autoplay; accurately identify the speaker and whether the recording is generic or personalised.	Moderate; touch 2 or after a request
Opportunity Snapshot	Build a small version, then test	Strongest opportunity to show evidence, scope and a labelled concept without making the email heavy.	Moderate; touch 2 or an interested reply
AMP email	Defer	Gmail requires sender registration, authentication and an HTML/text fallback. This adds complexity without evidence of value for this pilot.	High relative to current need; later permission-based use. 
Google for Developers

GIF	Defer	An animation is not proof of relevance. Start with a static, clearly labelled comparison.	Low-to-moderate production effort; only test after a baseline
WhatsApp button	Defer with the channel	The founder explicitly prioritised email now. Do not expand the first implementation.	Later scope decision
My proposed snapshot

Use three layers:

Five-second layer: business name, one verified observation, one sentence describing the offer.

Evidence layer: date checked, a narrowly framed screenshot or observation, and a clearly labelled concept—not a claimed live website or existing client project.

Optional detail layer: scope, one-time and recurring costs, transcript/audio, and a reply action.

Include a visible statement such as:

“Illustrative concept prepared by SiteBlitz. Not your current website and not an existing client project.”

Use appropriately licensed assets. Avoid exposing private contact information. Add a correction/removal route. My proposed default is an unlisted, expiring page with no advertising trackers; a random URL and noindex are not security controls for confidential information.

Correct the measurement claim

A page request does not prove that the recipient looked. Microsoft documents automated link scanning during email processing and at click time. Consequently, raw requests can include security activity. 
learn.microsoft.com

Record separately:

Raw page requests.
Filtered, likely-human sessions.
Explicit actions such as a submitted enquiry.
Replies and qualified opportunities.

Do not automatically send “I saw you viewed our proposal.”

AI voice: narrower legal conclusions

The EU’s Article 50 rules distinguish provider marking obligations, direct AI interaction disclosure and deployer disclosure of deepfakes. They do not support the blanket statement “every AI narration has the same deepfake-disclosure obligation.” They apply from 2 August 2026. High confidence on the distinction; medium on a specific SiteBlitz implementation. 
digital-strategy.ec.europa.eu

India’s notified amendment took effect on 20 February 2026. Its relevant synthetic-media provisions impose duties on intermediaries, including audio disclosure in covered circumstances. That does not itself establish the duties of a studio sending its own email. High confidence on the text; application needs counsel. 
meity.gov.in
+1

For this version, retain the approved ban on synthetic voice. A truthful founder recording is sufficient; synthetic narration requires an explicit specification amendment. 
Pasted text

Cost and success: start with one reusable page template, not bespoke videos for every prospect. Measure incremental qualified replies and paid-project margin against the text-only control. Delete the audio feature if it adds cost without measurable value.

4. Worldwide sending — disagree with “India and US now”; agree with conditional country expansion

No country is operationally approved before the common launch gates pass. Thereafter, distinguish potentially permissible recipients from an entire country being safe to email.

Proposed jurisdiction tiers
Tier	Market	Required distinction and launch decision
First controlled pilot	India	Business relevance, original publication evidence, privacy review and provider compatibility are required. Do not treat all publicly discoverable personal addresses as cleared.
Next reviewed pilot	United States	CAN-SPAM provides requirements for commercial outreach, including truthful identity/subjects, advertising disclosure, postal address and opt-out. It does not guarantee provider permission or replace other applicable obligations. High confidence on the FTC requirements. 
Federal Trade Commission

Conditional corporate pilot	United Kingdom	PECR distinguishes corporate subscribers from sole traders and certain partnerships. Companies House registration helps establish the entity, but does not alone establish who subscribes to a particular mailbox. Personal-data processing still requires UK GDPR analysis. High confidence; ICO guidance currently notes review following legislative changes. 
ICO

Case-by-case, not bulk import	Canada	Conspicuous publication requires publication by, or caused by, the recipient; no accompanying refusal; and relevance to their business role. A third party reproducing or selling the address does not create implied consent by itself. High confidence, current CRTC guidance. 
CRTC

Hold until sourcing review	Australia	Consent may be express or inferred, but the Spam Act separately regulates address-harvesting software and harvested-address lists. “Published address” is not a sufficient clearance field. ACMA also says a marketing email cannot be sent merely to ask for consent. High confidence on these rules. 
ACMA
+1

Later, French-language pilot	France	CNIL permits relevant professional prospecting under conditions including information and objection rights. Do not translate this into a general EU rule. Guidance dated 10 June 2026; high confidence. 
CNIL

Hold	Every unreviewed jurisdiction	No sending until its recipient categories, sourcing, notices, provider constraints and language QA are approved. “Hold” does not mean the activity is necessarily illegal.

Important India correction: most core DPDP processing provisions are scheduled to commence on 13 May 2027, following the phased notification of 13 November 2025. The Act’s public-availability exclusion is specifically framed around publication by the data principal or someone legally obliged to publish—not every third-party listing. Build for that distinction now. High confidence on the statutory text and commencement schedule. 
India Code
+1

The Gmail problem needs an explicit decision

Google’s receiving guidelines advise against sending to people who did not sign up. Sending through a different SMTP service does not remove that guidance. 
Google Help

The attachment reports that 79% of its Indian email-containing records use free-mail addresses; it does not say all of those are Gmail. That makes recipient-provider policy a major pilot constraint, not a footnote. 
Pasted text

For a policy-conservative launch, put non-opted-in personal-mailbox recipients on HOLD where receiving-provider guidance requires permission. Use a voluntary audit-request form, a properly authorised partner introduction or another reviewed acquisition channel. A “permission request” email is not a universal workaround.

Which records qualify?

The reported 86.75 million places are a discovery inventory, not a permissioned prospect list. Overture’s source-specific licensing also needs preserving; a data licence does not itself establish marketing permission. 
Pasted text
 
Overture Maps

I propose a mandatory eligibility record covering:

business identity → source/provenance → jurisdiction and recipient type → legal/provider eligibility → language → fresh observation → email verification → suppression → capacity

Important rules:

Identity: deduplicate businesses, branches, shared mailboxes and franchises. Do not email several branches about the same central website.

Evidence: recheck an outage shortly before sending. A crawler timeout or access block is not proof that a website is down. NO_VIEWPORT is a technical signal, not conclusive proof of bad mobile usability.

Contact: record the exact original source and publication context. A verifier’s VALID result is neither consent nor proof that the address belongs to the intended business.

Language: use business evidence and native-reviewed wording. Do not assume Gujarati, Hindi or English from city alone.

Uncertainty: HOLD is a valid outcome. Catch-all and unknown verification results stay out of the initial pilot.

Choose X from capacity—not ambition

The specification’s 100 new first contacts/day is a ceiling. Its 10/15/20 email ramp must not silently become a per-inbox allowance. Until clarified, I would interpret it conservatively as an app-wide campaign-send allowance. The 30-per-inbox limit includes follow-ups. 
Pasted text

With six inboxes:

6
×
30
=
180
 total messages per permitted sending day
6×30=180 total messages per permitted sending day

If every prospect receives three touches:

180
÷
3
=
60
 sustainable new prospects per sending day
180÷3=60 sustainable new prospects per sending day

That is before reserving capacity for replies. Therefore, six inboxes cannot sustain 100 new prospects per sending day under the worst-case three-touch sequence.

Admit new prospects only after reserving future follow-up capacity. Reduce X when delivery work or unanswered sales conversations accumulate.

Scaling gates

Retain the proposed bounce and complaint targets as conservative operating targets, not guarantees. Google recommends staying below 0.1% reported spam and avoiding 0.3%. 
Google Help

For the small pilot, my proposed rules are: investigate the first hard bounce; pause the affected cohort on a credible complaint or policy rejection; and show unavailable complaint data as unknown, not zero.

A 3% positive-reply target is provisional. Define it as positive human replies divided by distinct, accepted first-contact recipients in a mature cohort, excluding auto-replies. Paid projects and margin ultimately decide whether to scale.

Cost: verify only qualified candidates. Bouncer currently advertises $8 for 1,000 verification credits, not a guarantee of deliverability or legal eligibility. Price checked 12 November 2026; high confidence as an advertised price. 
Usebouncer

5. Admin-panel sending — agree with an owned queue; disagree that SMTP alone solves permission or reliability
Provider selection

The infrastructure must pass both the outreach tool’s terms and the underlying mailbox/relay provider’s terms.

Gmail’s policy updated 20 October 2026 prohibits unsolicited commercial mail; Google Workspace’s AUP prohibits unsolicited mass promotions and solicitations. Connecting such mailboxes to another product does not override those terms. 
Google Help
+1

For the proposed scraped-list campaign, SendGrid’s affirmative-consent requirements, AWS’s unsolicited-mass-email prohibition and Brevo’s restrictions on scraped/third-party lists make them unsuitable defaults. These are provider restrictions, not interchangeable statements of worldwide law. 
help.twilio.com
+2

Instantly is a candidate, not an automatic approval. Its terms updated 10 November 2026 include direct B2B activities as a permitted purpose. The incomplete reading of §6.7 should be corrected: it permits consent or another applicable lawful basis, not consent alone. 
instantly.ai
+1

Two additional conditions matter:

Domain age: its sending policy dated 13 October 2026 requires domains at least one month old. Buying a domain today therefore does not allow immediate sending through that route. This is a vendor requirement, not a universal deliverability law. 
instantly.ai

Ownership: its current terms say Instantly-provisioned infrastructure remains Instantly’s property, with substantial restrictions on transfer and administrative control. For a founder who wants an owned system, prefer independently controlled domains and verify mailbox portability before purchase. 
instantly.ai

Proposed one-click flow

Select → Write → Validate → Review batch → Approve and schedule

The approval screen should show the actual messages, eligibility evidence, HOLD reasons, costs and earliest send times. Approval authorises only that validated batch; it does not override later opt-outs or fresh failures.

At execution time, recheck:

approval → suppression → reply state → observation freshness → provider status → local window → remaining capacity

Keep one authoritative scheduler. If the provider also queues messages, the app must be able to reconcile and cancel them. Do not independently schedule the same sequence in two systems.

Where it should run

A laptop is acceptable for development and a supervised pilot, but not as the sole dependency for a worldwide “works while closed” service.

I recommend a small always-on application server, with persistent storage, backups, reply/event ingestion and a functioning unsubscribe endpoint. A single-host SQLite design may remain an initial implementation choice; there is no need to add a distributed queue solely because the dataset is large.

GitHub Actions is not inherently impossible, but it is a poor primary sending clock: GitHub documents that scheduled runs can be delayed and, under sufficient load, dropped. Use it for tests and deployment rather than critical send timing. 
GitHub Docs

Reliability rules worth building before a rich UI

Store a unique logical send record, message content/version, provider identifiers and delivery state. Use provider idempotency where supported.

A transport timeout is not proof that nothing was sent. Mark uncertain attempts for reconciliation rather than blindly retrying. A repeated Message-ID alone is not a reliable deduplication strategy.

Separate failure types:

An invalid mailbox should be suppressed across email campaigns.
An authentication or policy rejection should pause the affected infrastructure—not incorrectly mark the recipient invalid.
An opt-out should stop marketing across the appropriate identity scope.
A reply should cancel the remaining cold sequence before drafting anything else.

Do not treat an email bounce as permission to switch to another channel.

Resolve the specification’s scheduling contradiction: Tue–Thu only conflicts with “weekend dates move to Monday.” My proposed rule is to move any disallowed due date to the next permitted local window. 
Pasted text

Cost: Instantly’s page currently displays a $47/month Growth outreach component, but that is not a complete implementation quote. Confirm API access, webhooks, mailboxes and domains separately. 
instantly.ai
 Success tests: no duplicate sends under retries, no post-opt-out sends in race-condition tests, and recoverable queue state after a crash.

6. “Start my day” — agree with the experience; disagree with 50 correct classifications as an autonomy gate

The daily system should run in the application. Claude Code and ChatGPT can support development and review; the business must not depend on an open chat session or a browser conversation completing.

The morning workflow

First, reconcile. Retrieve sending events and incoming messages; distinguish accepted messages, bounces, replies and unresolved send attempts.

Second, protect. Apply opt-outs and pauses before considering new sends. Stop the cold sequence on any reply.

Third, interpret. Classify the latest relevant message using thread context. Allow multiple labels: “What is your price, but stop the follow-ups” is both a price question and a suppression instruction.

Fourth, prepare. Generate grounded reply drafts, identify missing facts, and display decisions requiring approval.

Fifth, authorise. The founder approves the safe reply batch and the next campaign batch. Unresolved commercial commitments remain held.

The Roman-Hindi brief should contain decisions, not a wall of metrics:

“Kal ke replies process ho gaye. Interested enquiries review ke liye ready hain. Stop requests suppress ho chuki hain. Aaj ke batch mein jo leads HOLD hain, unka reason saath diya hai.”

Populate it with actual counts only.

Automation boundaries
Event	Recommended initial handling
Clear opt-out / unsubscribe	Suppress automatically; cancel queued marketing
Out of office	Pause; do not initiate an automatic back-and-forth
Bounce	Parse the failure type; suppress or pause appropriately
Interested / price / scope question	Draft from approved offer facts; require approval
Wrong person	Stop that sequence; do not automatically contact a named replacement without eligibility checks
Complaint / legal request / deletion request	Stop marketing and escalate
Negotiation, refund, guarantee, contract or delivery commitment	Human approval required

This still respects AI-written messages: the founder can approve, reject or request regeneration without rewriting them.

Why 50 is insufficient

Even with zero observed errors in 50 independent representative cases, the exact one-sided 95% upper bound on the true error rate is approximately:

1
−
0.05
1
/
50
≈
5.8
%
1−0.05
1/50
≈5.8%

This calculation is not evidence that the classifier will fail at that rate; it shows why 50 successes do not establish safety.

My proposed path is a labelled evaluation set covering each important category, adversarial examples and a live shadow period. Require zero missed opt-outs in the safety test set before considering any auto-reply category. Even 300 zero-error representative cases imply an upper bound near 1%, not zero risk.

Begin eventual auto-sending only with narrowly scoped, non-binding answers grounded in approved facts. Do not let a model invent discounts, delivery dates or guarantees.

Claude and ChatGPT roles

Use a primary model for classification/drafting and an independent reviewer for high-risk threads, factual disputes and sampled QA. Do not pay for two full-model passes on every routine email without measuring the benefit.

The governing authority remains the application’s policy and approval state—not “both models agreed.”

Treat email bodies and scraped pages as untrusted input. A recipient message must not grant permission to export data, change payment instructions or execute tools. Structured outputs, limited tool authority and approval gates are consistent with OpenAI’s current agent-safety guidance. 
OpenAI Developers

The specification’s promise not to send email addresses or phone numbers to the model also needs a real sanitizer: thread text can contain them in signatures and quoted replies. Merely omitting separate contact fields does not satisfy that promise. 
Pasted text

Honest metrics

Show sent/accepted events, bounces, unique human replies, positive replies, qualified opportunities, proposals, paid projects, acquisition cost and contribution margin.

Do not call pixel events “read.” Apple states that Mail Privacy Protection can download remote content when a message arrives rather than when it is viewed. 
Apple Support

Likewise, “accepted by the receiving server” is not “landed in the inbox,” and “snapshot requested” is not “owner viewed.”

Cost and upkeep: model usage, secure message processing and regular evaluation. Beneficiaries: founders and recipients awaiting replies. Success: fewer manual decisions without missed opt-outs, unsupported commitments or deteriorating sales outcomes.

7. Build order and launch gates — agree with the truthful website first; move minimum reply handling before the first send

The supplied document reports invented testimonials/results, incorrect location claims and withdrawn prices on the live website. Those claims are not independently verified here, but the reported condition is a launch blocker until the deployed site is checked and corrected. 
Pasted text

Recommended order
Stage	Build / decision	Exit gate
0. Truth and identity	Deploy truthful website; confirm sender, business identity, address, reply mailbox and offer	Production pages checked; no fabricated claims; all identity fields complete
1. Data integrity	Remove fabricated-contact paths; quarantine previously generated dummy data; retain source provenance	No eligible contact without provenance; fixtures cannot enter production
2. Eligibility engine	Country/subscriber rules, provider policy, language, evidence freshness and verification	Unknown or failed requirements produce HOLD
3. Safety infrastructure	Authentication, unsubscribe, suppression, bounce handling and minimum incoming-reply processing	End-to-end tests pass before any prospect email
4. Batch and scheduler	AI writing, validation, review, approval, queue and reconciliation	No unapproved, duplicate or out-of-window sends
5. Pre-send evaluation	Synthetic persona review, consenting-reader test and seeded mailbox tests	Factual and comprehension gates pass
6. Controlled pilot	One small, well-defined segment	Mature outcomes reviewed before increasing volume
7. Expansion	Snapshot experiment, limited reply automation and additional markets	Each addition passes its own economic, safety and legal gate

The specification explicitly identifies a discovery function that invents contact data. Removing it is not enough: audit whether its outputs already entered the database. 
Pasted text

Pre-send tests that must exist

Test opt-out arriving between approval and execution; reply arriving before a scheduled follow-up; duplicate/out-of-order provider events; timeout after possible provider acceptance; restart recovery; missing timezone; stale evidence; unknown country; unavailable model; and blank company facts.

Verify authentication and unsubscribe headers on received raw messages, not merely in the app’s outgoing payload.

Also test mobile batch screens, quoted unsubscribe text, auto-reply loops and malicious instructions embedded in inbound messages. The supplied 338-test count and writer dry-run results do not establish that these cases are covered. 
Pasted text

What the public website must show

Real business identity and location; a working contact route; accurate package scope; one-time versus recurring costs; ownership and handover terms; and appropriate privacy information.

Use genuine portfolio work with permission, or clearly labelled demonstrations. No fabricated client names, testimonial quotations, results or claims that a demo is a delivered customer project.

Budget and economic gate

Do not approve a complete operating budget from the vendor subscription price alone. The budget must include sending software, mailboxes/domains, verification, hosting/backups, model usage, legal review and human handling.

Measure:

Customer acquisition cost
=
all attributable outreach and sales-handling costs
paid customers acquired
Customer acquisition cost=
paid customers acquired
all attributable outreach and sales-handling costs
	​


Compare that with contribution after website-delivery and support costs, not headline revenue. A high positive-reply rate with unprofitable delivery is not a successful engine.

For future AI-managed inboxes, my proposed extension is a structured offer record—identity, evidence, scope, price, exclusions and next action—used to generate both the email and snapshot. That gives human assistants and software agents consistent facts. It is an architectural proposal, not a prediction that any particular standard will dominate.

Final decision: approve the direction, but revise the specification before implementation. The next milestone should be a truthful, policy-reviewed, reliably stoppable pilot, not a 100-email button.

Points still open
Sender and offer: actual sender name, business/legal identity, reply address, postal address, approved pricing, recurring charges and delivery capacity.
Provider route: exact mailbox/SMTP operator, applicable terms, API/webhook plan, cancellation behaviour, domain ownership and portability.
Eligible inventory: how many records survive identity, provenance, recipient-policy, legal, language, evidence and verification checks—not merely how many contain an email.
Spec contradictions: app-wide versus per-inbox ramp; campaign sends versus new contacts; Tue–Thu versus Monday rescheduling; compliance-link exceptions; ongoing human QA.
Legal sign-off: Indian sourcing/privacy approach, treatment of personal mailboxes, overseas subscriber categories, cross-border processors and later synthetic-media use.
Evidence quality: recheck standards for outages, mobile usability and forms; treatment of crawler blocks; contamination from fabricated discovery outputs.
Autonomy evidence: representative labelled replies, critical-error tests, permitted auto-reply categories and escalation rules.
Commercial validation: actual qualified-reply rate, paid conversion, acquisition cost, delivery margin and the incremental value of snapshots/audio.
