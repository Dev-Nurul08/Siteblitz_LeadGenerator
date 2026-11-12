ChatGPT said:
Q1. Free-mail recipients

Agree with the two-tier approach, subject to the existing eligibility checks. I withdraw the blanket free-mail HOLD. I cannot cite a rule that prohibits an Indian business contact solely because the business publishes a Gmail address rather than an address on its own domain.

Your distinction between sending through Gmail and sending to Gmail is substantially correct. Google’s current Program Policies prohibit using Gmail to distribute unsolicited commercial mail, while directing external senders to its separate sender guidelines. Those incoming-mail guidelines advise against contacting people who did not sign up. That is not, by itself, an Indian statutory prohibition. It remains an explicit receiving-provider expectation, with filtering, blocking and reputation consequences. Policy text checked 12 November 2026; high confidence. 
Google Help
+2

The eligibility rule I would lock
Tier	Decision	Required evidence
Tier 1: business-published contact	Eligible for the India pilot, regardless of free-mail versus custom domain, after all other gates pass	Address visibly published on the business’s verified website or genuinely controlled public profile; source URL, capture date and supporting excerpt; business relevance; no conflicting contact restriction; successful verification; no suppression
Tier 2: listing-only contact	HOLD	Address exists only in Overture or another third-party listing, without sufficient first-party publication evidence
Uncertain identity or publication	HOLD	Unclear profile ownership, an employee’s apparently personal address, stale ownership, or conflicting business identities

“Eligible” means eligible for selection and review, not automatically READY. Publication is evidence of provenance; do not record it as consent.

The supplied specification says the finder stores source URLs from the business’s own website. That supports the first part of Tier 1, but it does not independently establish current business ownership or the legal significance of publication. 
Pasted text
 
Pasted text

DPDP: your date is correct, but preserve the precise exclusion

The commencement notification schedules the principal processing provisions for eighteen months after publication. MeitY’s subsequent official statement identifies 13 May 2027 as the full-enforcement date. High confidence on the date. 
meity.gov.in
+1

Section 3(c)(ii) excludes personal data made public by, or at the direction of, the individual concerned, or by someone legally obliged to publish it. Consequently, an owner publishing their own business contact is a stronger case than a company publishing an employee’s personal address without evidence of that employee’s involvement. High confidence on the statutory wording; application to particular records requires legal review. 
meity.gov.in

Do not encode “all data on a business website is outside DPDP.” Encode the actual publication circumstances.

One important limitation to “we measure and stop”

We cannot assume that the pilot will reveal all complaints or spam placement. Google says low-volume Postmaster data may be omitted. It also explains that a low reported-spam rate can coexist with poor delivery because messages are already being filtered into spam. 
Google Help

Therefore, I accept Tier 1 free-mail recipients for a bounded, supervised pilot with documented receiving-provider risk acceptance. I do not accept “no complaint appeared” as proof that Gmail considers the campaign acceptable.

Cost and test: this adds provenance review, not another mandatory subscription. Audit the first 30 selected records: every one must have reproducible first-party publication evidence. Track free-mail and custom-domain outcomes separately.

Q2. The mailbox operator

A concrete qualifying operator exists: Mailforge. “None exists” would be incorrect.

The specific permission

Mailforge’s Terms, §3.4(1), Sending Policy, state:

“The Services may be used for lawful commercial email outreach, including unsolicited business-to-business outreach where permitted by applicable law.”

The page is labelled “Last Updated 29th Dec 2025” and was checked on 12 November 2026. High confidence in the published permission; this is not a guarantee of campaign legality or delivery. 
Mailforge

The surrounding clauses require an unsubscribe link, prompt opt-out handling, clear identity, reasonable address verification and compliance with applicable law. Their wording does not turn public availability into consent or exempt a sender from jurisdiction-specific requirements. 
Mailforge

It is actual mailbox infrastructure, not merely a sequencer

The operator documents Mailforge and Infraforge as SMTP mailbox hosting on their own servers, rather than Google Workspace or Microsoft 365 mailboxes. It also documents SMTP/IMAP credential export. These are vendor-documented capabilities, not independently tested capabilities in this project. 
Salesforge
+1

Keeping the domains with the founders

Use this procurement arrangement:

Founders’ registrar account and registrant details → Mailforge mailbox hosting → founders’ application as the scheduler.

Register the domains independently. Retain registrar login, renewal control and recovery credentials. Connect the domains through the documented DNS/nameserver process rather than handing over the registrar account. Mailforge documents changing nameservers from the customer’s existing GoDaddy account, and its ownership explanation says domains remain the customer’s. 
SalesForge Help
+1

The distinction is:

The founders control the domains and application. They rent the mailbox service.

Before purchase, verify that the chosen arrangement permits the Vercel website records to coexist with the mail records, and test mailbox export and DNS recovery. Do not interpret an “Export to Instantly” button as proof that historical mailbox contents are backed up.

Cost and remaining acceptance tests

Mailforge currently publishes $3 per mailbox slot per month with a minimum of ten slots. That implies a $30/month mailbox minimum, before taxes, domains and extras, even when only six mailboxes are active. Pricing checked 12 November 2026. 
Mailforge

My proposed acceptance tests are:

Send through the application, receive through IMAP, and reconcile a controlled failure.
Confirm that both unsubscribe headers survive transport and are covered by a valid DKIM signature.
Confirm the founders retain registrar control and can preserve the website’s DNS records.

Two alternatives do not pass the same test: Mailreef’s §27(1) requires express permission despite its cold-email positioning. Maildoso’s published guidance specifically excludes personal/consumer-domain recipients such as Gmail, so it does not fit the proposed Tier 1 free-mail segment. 
Mailreef
+1

Decision: Mailforge is the documented default candidate. There is no need to accept Instantly-owned domains or self-host SMTP merely because no permissible operator can be named. A self-run server would also introduce maintenance and hosting-policy questions rather than remove them.

Q3. Hosting split for the pilot

Agree with a supervised laptop sender. Disagree that an unsubscribe endpoint, snapshot pages and a downloaded suppression list are sufficient by themselves.

The split can work without moving the whole application to a server immediately.

What must be authoritative in the cloud

MongoDB should hold the authoritative suppression state, including unsubscribe, complaint and manual do-not-contact decisions. The laptop may cache information for display, but it must not authorise a send from a cached “not suppressed” result.

Immediately before each submission, the worker must obtain a fresh, uncached eligibility result. An unavailable suppression service means no send, not “use yesterday’s list.”

Keep suppression independent of the local campaign database. Restoring an old laptop backup must never restore permission to contact someone.

Incoming replies need an explicit offline rule

“Reply stop” must work as well as the unsubscribe link.

Where the operator provides suitable events, receive and persist reply, bounce and complaint events on the always-on side. Where only IMAP is available, the supervised pilot needs:

A complete reconciliation before each sending session, continuous reconciliation while sending, and at least one reconciliation every 24 hours even on non-sending days.

That 24-hour interval is my proposed operational maximum, not a claim about a universal statutory deadline. If the founders cannot guarantee it, add a small always-on inbox poller from day one. That does not require moving the sender itself.

Simply checking inboxes on Tuesday, Wednesday and Thursday could leave a Thursday-night opt-out unprocessed until Tuesday.

RFC 8058 and Vercel routing

The endpoint must accept the prescribed HTTPS POST without requiring login, cookies or browser interaction. It must not redirect the POST. RFC 8058 also requires the relevant headers to be covered by a valid DKIM signature. Source: RFC 8058, January 2017; high confidence. 
RFC Editor
+1

My implementation requirements are:

Persist before success. Return success only after suppression is durably recorded; repeated requests must be harmless.

Separate GET from POST. A link scanner fetching the URL must not accidentally unsubscribe someone. A human-facing GET can show an unsubscribe control; the RFC POST performs the action directly.

Test the exact public URL. Domain forwarding, trailing-slash redirects, deployment authentication or bot challenges must not interfere.

Preserve mail and web DNS together. A mailbox provider’s automatic domain forwarding must not swallow the unsubscribe or snapshot paths.

The unavoidable send race

A fresh suppression check followed by an SMTP submission is not one atomic operation.

Use one outbound worker for the pilot, minimise the gap between check and submission, and cancel queued messages wherever cancellation remains possible. But an email already accepted for delivery cannot be assumed recallable.

The honest guarantee is:

No new submission after the worker observes a suppression. A message already in flight may still arrive.

Do not describe a simple list-pull design as guaranteeing zero messages after the exact instant someone clicks unsubscribe.

Vercel has two relevant conditions

Commercial use requires an appropriate paid plan; Vercel’s Hobby plan is restricted to non-commercial personal use. Its fair-use page was updated 14 September 2026. 
Vercel

Its AUP, updated 21 April 2026, also prohibits sending or creating unsolicited mass messages. Keep email generation and dispatch out of Vercel in this proposal. Ordinary website and suppression hosting should not be misrepresented as permission to run the outreach engine there; clarify scope with Vercel before expanding that role. 
Vercel

Migration trigger

Accept before 41 new first contacts per sending day, or before any unattended sending, as a project governance rule. Forty is not a technical safety boundary.

Move earlier when supervision, inbox reconciliation or recovery becomes unreliable. Assess total messages, not just new contacts: Q5 shows that 20 new contacts per sending day can eventually produce 120 scheduled campaign messages on a Tuesday.

Cost and test: this reuses the website stack but still requires monitoring, backups and the correct hosting plan. Acceptance test: switch the laptop off, submit an unsubscribe, restart the laptop, and prove that the pending message is blocked. Also test database failure, stale inbox state and restart after an uncertain SMTP result.

Q4. Final India touch-1 templates

Agree with B’s observation-first structure after removing its overclaims. The independent panel strengthens that design hypothesis; it does not establish a winning subject line or actual country-level response behaviour.

I am retaining ₹7,999 from the supplied examples. Before activation, the approved offer must confirm that price, scope, tax treatment and separate domain/hosting charges. The examples themselves are not price authorisation. 
Pasted text

The body word counts below exclude the signature and opt-out, with each placeholder counted as one word. Validate again after substitution.

A. SOCIAL_ONLY salon

Subject: [Business]: no website link in Instagram bio

On [date], the Instagram profile for [Business] showed no website link when I checked its bio.

I’m [Sender] from SiteBlitz, a small web studio in Gujarat. We build simple pages showing salon services, prices, opening hours and appointment enquiries.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

[Sender] | SiteBlitz
[Reply address] | [Postal address]
WhatsApp: [WhatsApp]

Reply “stop” or unsubscribe here: [unsubscribe URL].

Body: 62 words. Use only when the specific Instagram bio was checked. Do not substitute an Instagram observation for an unrelated social profile.

B. NO_VIEWPORT coaching

Subject: [Business]: homepage viewport setting

On [date], the homepage at [domain] had no mobile viewport setting in the page source I checked. That alone does not prove a display problem.

I’m [Sender] from SiteBlitz, a small web studio in Gujarat. We build mobile-friendly pages showing courses, timings and enquiry details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

[Sender] | SiteBlitz
[Reply address] | [Postal address]
WhatsApp: [WhatsApp]

Reply “stop” or unsubscribe here: [unsubscribe URL].

Body: 68 words. This subject is less compelling than “your site is difficult to use,” but the available observation does not support that stronger claim. A documented visual problem would justify a different, more understandable subject and opening.

C. SITE_DOWN retail

Subject: [Business]: [domain] did not load in our checks

On [date], the homepage at [domain] did not load in two checks from separate connections. The interruption may be temporary.

I’m [Sender] from SiteBlitz, a small web studio in Gujarat. If you need a replacement, we build pages showing your showroom, products and enquiry details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

[Sender] | SiteBlitz
[Reply address] | [Postal address]
WhatsApp: [WhatsApp]

Reply “stop” or unsubscribe here: [unsubscribe URL].

Body: 68 words. This requires two actual checks from separate connections, not two retries through the same crawler. Recheck immediately before dispatch. A block or challenge page is not sufficient evidence for this wording.

The price here is explicitly for a possible replacement website, not a promise to repair an unknown outage for ₹7,999.

Three implementation decisions

One primary action: keep “make a sample and send it here.” This avoids asking the recipient to choose a channel before expressing interest. [WhatsApp] is the studio’s number, not the prospect’s scraped number.

WhatsApp remains recipient-initiated: an inbound request supports responding to that request; it is not blanket permission for future marketing. WhatsApp’s policy requires appropriate permission and respect for opt-outs. 
WhatsApp for Business

The unsubscribe URL is mandatory for the proposed operator: the no-promotional-link rule must not remove it. Also preserve RFC 8058 headers outside the visible body.

Treat SITE_DOWN and MAIL_UNDELIVERABLE as separate eligibility results. An unavailable website should trigger fresh mailbox and identity checks, not an automatic conclusion that every address on that domain will bounce.

Cost and test: producing samples becomes a delivery obligation once accepted. Approve the sample scope before activating this CTA. Run the already-agreed ten-reader comprehension test; retain the eight-of-ten threshold.

Q5. Exact pilot numbers for the spec lock

Agree to a numerical lock, but distinguish a small technical ramp from evidence-based commercial scaling. The following numbers are proposed operating rules, not provider guarantees or statistically proven optimums.

A. Infrastructure and capacity
Setting	Locked proposal
Sending domains at launch	2 founder-controlled domains
Active mailboxes	6 total, 3 per domain
Identity	Real founders or clearly identified role mailboxes; no invented employees
Sender continuity	One business remains with one sender throughout its sequence
Per-mailbox hard ceiling	30 outbound messages per calendar day, including first touches, follow-ups, replies and tests
Reply reserve	5 messages per mailbox per day, unavailable to campaign scheduling
Maximum scheduled campaign messages	25 per mailbox; 150 across six
Automatic warm-up traffic	None in this pilot
Campaign sending days	Tuesday–Thursday
Campaign windows	09:00–11:30 and 14:00–16:30 recipient time
Cadence	Day 1 / 6 / 14, moved to the next permitted window with capacity
Catch-up behaviour	Never exceed a cap to clear missed sends

A reply reserve is not a limit on the number of replies the founder may handle. If replies need more capacity, reduce campaign sending while retaining the 30-message ceiling.

Buying ten Mailforge slots does not authorise ten active senders; the pilot starts with six.

B. Weeks 1–4

“Week 1” begins only after the launch gates pass. These are ceilings, not quotas.

Pilot week	New first contacts per sending day, app-wide	Maximum new contacts that week	Busiest scheduled campaign day, assuming no replies or stops*
1	10	30	10 messages
2	15, only after the first ramp gate	45	45 messages
3	20, only after the second ramp gate	60	85 messages
4	20; no automatic increase	60	110 messages

*Calculated using Day 1/6/14, Tuesday–Thursday sending and no holidays. Replies would cancel subsequent cold touches.

Maximum first contacts in four weeks: 195. A failed gate holds the current stage or pauses sending; the calendar does not force an increase.

C. Minimum evidence before either initial increase

For 10 → 15 and 15 → 20, require:

At least 30 distinct first-contact recipients from the immediately preceding stage, each observed for at least 72 hours, with:

Zero observed hard bounces, complaints or policy rejections in that ramp cohort.
No unresolved delivery uncertainty, suppression failure or inbox-reconciliation gap.
Successful authentication/header checks and explicit founder approval.

These two increases are technical calibration, not evidence of commercial success.

A 21-day positive-reply gate cannot honestly govern a week-two increase. Therefore, the 3% commercial gate begins before increasing beyond 20, not before the initial calibration steps.

D. Exact pause and stop rules

Here, pause means stop the affected activity pending review. Stop means retire or rebuild the affected campaign/source configuration before restarting. Neither permits switching domains to evade the failure.

Signal	Automatic pause	Stop / rebuild condition
Hard bounce: invalid recipient	First confirmed hard bounce: suppress the address and pause the affected sourcing batch	2 hard-bounced recipients within the latest 100 distinct recipients attempted, including an initial window smaller than 100
Complaint	1 credible complaint, or an available provider-reported spam rate ≥0.10%: pause the pilot and investigate	2 credible complaints within 30 days, or provider-reported spam rate ≥0.30%: stop the current pilot campaign
Permanent authentication/policy rejection	1 rejection: pause the affected sending domain or receiving-provider route; do not classify it as an invalid address	3 policy rejections within 24 hours, or an explicit operator suspension: stop the affected configuration
Suppression or send-integrity failure	1 known submission to an already-observed suppressed recipient, 1 duplicate, or 1 unapproved submission: pause all campaign sending	Root-cause fix and regression tests required before restart
Unavailable/stale state	Suppression lookup unavailable, inbox reconciliation incomplete, or previous SMTP result unresolved: zero further affected sends	No time-based automatic restart
Sales-handling backlog	An interested enquiry remains unhandled for more than one business day: pause new first contacts	Resume only after the backlog is cleared

Count a recipient once for hard-bounce-rate purposes; follow-ups must not inflate the denominator and make the rate look better. Update the recipient’s outcome when a delayed bounce arrives.

A normal “not interested” or “stop” response is a suppression event, not automatically a spam complaint.

Google’s published reference points are below 0.10% reported spam and avoiding 0.30% or higher. Our first-complaint pause is deliberately stricter for this small pilot. 
Google Help

E. Positive-reply definition and commercial scaling

Use:

Positive-reply rate
=
Distinct mature prospects giving a positive human reply
Distinct mature first-contact prospects not known to have bounced
Positive-reply rate=
Distinct mature first-contact prospects not known to have bounced
Distinct mature prospects giving a positive human reply
	​


“Positive” means requesting the sample, requesting relevant price/scope details, agreeing to a substantive next step, or expressing a current relevant need.

Exclude auto-replies, acknowledgements, opt-outs, “not now,” and a gatekeeper merely supplying another address. Count each prospect once. This is a non-bounced-prospect metric, not a claim of inbox delivery.

A cohort is mature on Day 21, provided at least seven days have passed since its last actual campaign message. If capacity or calendar shifts delay the final touch, maturity shifts too.

Before any increase above 20 new contacts per sending day, require:

Gate	Requirement
Mature cohort	At least 100 distinct prospects
Positive replies	At least 3%, meaning at least 3 of 100
Hard bounces	≤1%, with all incidents investigated
Complaints	No unresolved observed complaints; available provider-reported rate <0.10%
Technical state	No unresolved policy, authentication, suppression or reconciliation issue
Capacity	Future follow-up slots and reply reserve already booked
Approval	Explicit founder approval

Then increase by at most 5 new contacts per sending day. Require a new, non-overlapping mature cohort of at least 100 before another commercial increase.

At 100 mature prospects:

Zero positive replies: stop that campaign version and revisit targeting, evidence or offer.

One or two positive replies: hold volume and test a revision at the same ceiling.

Three or more: eligible for a controlled increase only when the other gates pass. Three of 100 is a decision threshold, not proof that the underlying response rate exceeds 3%.

Unknown complaint data blocks automatic commercial scaling. It does not automatically invalidate the supervised pilot, but the dashboard must say “unknown.” A founder can authorise another bounded cohort at the existing ceiling rather than pretending the complaint-rate gate has been demonstrated. Google explicitly warns that low-volume data may be missing. 
Google Help

F. Correction to “100 new/day needs at least ten inboxes”

Ten is only a no-reserve, average-volume lower bound.

With the proposed five-message reply reserve:

⌈
100
×
3
30
−
5
⌉
=
12
 inboxes minimum on an average-capacity basis
⌈
30−5
100×3
	​

⌉=
12 inboxes minimum on an average-capacity basis
	​


There is also a calendar concentration problem. At a steady 20 new prospects every Tuesday, Wednesday and Thursday, strict next-permitted-day scheduling produces:

Day	First touches	Second touches	Third touches	Total
Tuesday	20	60	40	120
Wednesday	20	0	20	40
Thursday	20	0	0	20

This fits the proposed six-inbox capacity.

At 100 new prospects per sending day, that same strict Tuesday pattern becomes 600 campaign messages, requiring 24 inboxes at 25 campaign messages each if nothing may spill into Wednesday or Thursday.

That is not a recommendation to buy 24 inboxes. It is the reason to book follow-ups against actual future capacity. Twelve inboxes is an average-capacity minimum, not an unconditional promise that the original calendar will fit.

The pilot should lock 10 → 15 → 20 → 20, prove the conversation economics, and resolve scheduling capacity before discussing 100.

Points still open
Actual offer and identity: approved price, tax treatment, sample-page scope, sender identities, reply address and postal address.
Mailforge acceptance tests: retained domain control, coexistence with website DNS, SMTP/IMAP behaviour, header preservation and DKIM coverage.
Cloud scope: appropriate Vercel plan, its permitted role, and the authoritative suppression design.
Offline reply handling: operator events versus daily IMAP reconciliation, with an always-on poller required if the 24-hour maximum cannot be maintained.
Tier 1 evidence: verification of business-controlled publication, treatment of employee addresses, and legal review of the Indian sourcing approach.
Measurement coverage: which complaint and delivery signals are genuinely available, with missing data explicitly retained as unknown.
Commercial validation: consenting-reader results, observed results by template and mailbox family, sample-production cost, paid conversion and contribution margin.
