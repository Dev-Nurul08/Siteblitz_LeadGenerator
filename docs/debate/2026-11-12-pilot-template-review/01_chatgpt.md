ChatGPT said:
SiteBlitz pilot: point-by-point pre-send review

My verdict: agree with the overall template approach, but not with an unconditional launch approval yet. I recommend three copy changes. The more important release questions concern observation freshness, the no-link rule, suppression after opt-out or T3, and the sending provider’s policy.

I am reviewing the supplied document, not the implementation. Its statements that checks, validators and unsubscribe replacement are built remain documented claims, not verified code behaviour. The document itself describes this as a synthetic review, with a real ten-reader test still to follow. 
Pasted text
 
Pasted text

1. Persona-by-template review

Agree — a synthetic review is useful for identifying comprehension and trust problems. Disagree that it can establish actual reply rates or predict Gmail placement.

How to read the scores

These are my qualitative predictions, not observed reader responses. Confidence is medium in the relative weaknesses and low in any individual person’s predicted action.

“Who?” means identifying SiteBlitz as a website studio, not merely spotting a sender’s name. “Next?” means understanding the requested action; for T3, understanding that no response is required unless they want the sample.

I assume each observation genuinely applies and that the writer receives an appropriate vertical_page. That is a stated template requirement, not an inspected output. The missing COMPANY_FACTS demo table prevents verification of every vertical-specific version. For restaurant staff, I assume only the documented other fallback, not invented menu, ordering or reservation features. 
Pasted text
 
Pasted text

Each T1 variant is a separate hypothetical. They are not three allegations about the same business. For T2 and T3, I do not assume the recipient read T1 or expanded the older messages.

Trust: 1 = very low, 5 = very high. Spam-likeness: 1 = low, 5 = high.

Persona	Template	Who in 5 seconds?	Why?	Offer?	Next?	Trust	Spam-likeness	Predicted action
P1: Surat salon owner, slow English reader	T1 SOCIAL_ONLY	No	Yes	No	No	3	3	Maybe
P1	T1 NO_VIEWPORT	No	No	No	No	2	3	Ignore
P1	T1 SITE_DOWN	No	Yes	No	No	2	4	Ignore
P1	T2	No	No	Yes	Yes	3	3	Maybe
P1	T3	No	Yes	Yes	Yes	3	2	Ignore
P2: Coaching admin who forwards to owner	T1 SOCIAL_ONLY	Yes	Yes	Yes	Yes	3	2	Maybe
P2	T1 NO_VIEWPORT	Yes	Yes	Yes	Yes	3	2	Maybe
P2	T1 SITE_DOWN	Yes	Yes	Yes	Yes	3	3	Maybe
P2	T2	No	Yes	Yes	Yes	3	3	Maybe
P2	T3	No	Yes	Yes	Yes	3	2	Ignore
P3: Showroom owner whose site lapsed	T1 SOCIAL_ONLY	Yes	Yes	Yes	Yes	3	3	Maybe
P3	T1 NO_VIEWPORT	Yes	Yes	Yes	Yes	3	3	Maybe
P3	T1 SITE_DOWN	Yes	Yes	Yes	Yes	4	2	Reply
P3	T2	No	Yes	Yes	Yes	3	3	Maybe
P3	T3	No	Yes	Yes	Yes	3	2	Ignore
P5: Restaurant staff, shared info@ inbox	T1 SOCIAL_ONLY	Yes	Yes	Yes	Yes	2	4	Ignore
P5	T1 NO_VIEWPORT	Yes	No	Yes	Yes	2	4	Ignore
P5	T1 SITE_DOWN	Yes	Yes	Yes	Yes	2	4	Spam
P5	T2	No	No	Yes	Yes	2	4	Ignore
P5	T3	No	Yes	Yes	Yes	2	3	Ignore
P9: Owner’s son/daughter managing inbox	T1 SOCIAL_ONLY	Yes	Yes	Yes	Yes	3	2	Maybe
P9	T1 NO_VIEWPORT	Yes	Yes	Yes	Yes	4	2	Reply
P9	T1 SITE_DOWN	Yes	Yes	Yes	Yes	3	3	Maybe
P9	T2	No	Yes	Yes	Yes	3	3	Maybe
P9	T3	No	Yes	Yes	Yes	3	2	Ignore
P10: Gmail filtering	T1 SOCIAL_ONLY	N/A	N/A	N/A	N/A	N/A	Unknown	Need data
P10	T1 NO_VIEWPORT	N/A	N/A	N/A	N/A	N/A	Unknown	Need data
P10	T1 SITE_DOWN	N/A	N/A	N/A	N/A	N/A	Unknown	Need data
P10	T2	N/A	N/A	N/A	N/A	N/A	Unknown	Need data
P10	T3	N/A	N/A	N/A	N/A	N/A	Unknown	Need data
What the human-persona review suggests

P1: the main weakness is comprehension speed, not insufficient persuasion. The observation-first rule delays the introduction, and “opened zoomed-out” adds an unfamiliar concept before the reader knows who is writing. Simpler English should help, but it cannot establish that the English version works for this language profile. I would not translate the locked English lines ad hoc; a Gujarati or Hindi version needs a consistent, separately validated language configuration.

P2 and P5: comprehension does not equal decision-making authority. They may understand the offer perfectly but be unable to approve a sample. P2 has an obvious forwarding role; P5 may consider the message unrelated to their work. I would not add a second referral question and break the locked CTA. Instead, distinguish direct-owner inboxes from shared operational inboxes when interpreting pilot results.

P3: SITE_DOWN is the strongest situational match. The temporary-interruption caveat and conditional replacement offer are valuable. Keep both. An outage observation does not prove that replacement is necessary, however. The current wording appropriately avoids making that unconditional claim. 
Pasted text

P9: precision matters more than additional sales language. A narrowly accurate observation could earn attention. An exaggerated diagnosis could lose it. Do not turn “no website link in Instagram bio” into “you have no website,” or one rendered view into a claim about every phone.

T3 being ignored is not necessarily failure. Its purpose is to close the sequence respectfully, not manufacture another reply. The current text accomplishes that, provided the system honours its promise. 
Pasted text
 
Pasted text

P10: what can actually be reviewed

The copy contains no obvious fabricated results, countdowns or discounts. Those are favourable editorial characteristics, not a Gmail inbox-placement prediction.

Authentication and low volume do not supply the missing information about reputation, recipient reactions, message construction and delivery behaviour. Google’s published sender requirements include infrastructure and formatting requirements beyond authentication. Its requirements for personal Gmail accounts began on 1 February 2024. Confidence: high in the published requirements; unknown for this pilot’s placement. Source: Google’s sender guidelines. 
Google Help

Proposal and test: use the planned ten-reader test as a diagnostic screen, with two readers matching each human persona. Randomise first exposure to T1 variants, then ask the four comprehension questions after five seconds. My proposed screening threshold is at least 8/10 correct on each dimension, with any shared misunderstanding investigated. This is not statistical validation of every persona–variant combination. Cost: participant recruitment, optional honoraria and manual scoring; no new software required. Benefit: fewer confusing messages. Upkeep: repeat after material wording or language changes.

2. Is the NO_VIEWPORT wording understandable?

Disagree — it is understandable to some readers, but unnecessarily difficult for the slow-English persona.

The phrase combines a rendering mechanism, a device description and a visual consequence:

“opened zoomed-out on a phone screen in our check, so the text showed very small”

The useful observation is very small text in the checked phone-sized view. The recipient does not need to understand why the page appeared that way.

My one proposed replacement

On [date], the homepage at [domain] showed very small text when we checked it at a phone-screen size.

This removes “zoomed-out” while preserving the limited scope of the observation. It does not claim that a physical phone was used, that all phones are affected, or that the business is losing customers. The supplied context supports a rendered check at a 390-pixel phone viewport with a stored screenshot, not those broader conclusions. 
Pasted text

Implementation condition: change the upstream E1 observation template and version its fixtures. Do not instruct the writer to paraphrase the existing observation, because the contract requires verbatim copying. Regenerate affected unsent tasks against the approved observation version rather than silently editing historical sent records. 
Pasted text
 
Pasted text

Cost and test: no additional vendor spend is expected from this wording change; it requires a maintained observation constant and regression tests. The risk is evidence/text drift. Pass conditions: exact E1-to-email equality, valid body length and improved comprehension in the reader test.

3. Concrete changes that preserve the locked rules

Agree — make three changes, not five. Keep the price, permission question, observation-first structure and T3 unchanged.

Change 1: simplify the NO_VIEWPORT observation

Before

On [date], the homepage at [domain] opened zoomed-out on a phone screen in our check, so the text showed very small.

After

On [date], the homepage at [domain] showed very small text when we checked it at a phone-screen size.

Apply this through E1 as described above, not through writer discretion.

Change 2: make the NO_VIEWPORT subject state the observed fact

Before

[Business]: your homepage on a phone

After

[Business]: small homepage text in our check

The new fact portion contains six words, stays within the 3–8-word rule and describes the observation rather than merely naming a topic. It does not claim the site is broken. The original subject and subject constraints are documented in the attachment. 
Pasted text
 
Pasted text

Benefit: faster recognition of the reason for contact, especially for P2 and P9.
Cost/upkeep: one subject reference and its tests; no additional vendor spend expected.
Risk/test: the subject must only accompany the matching verified observation. Test exact business-name preservation, six-word fact portion and absence of prohibited punctuation.

Change 3: identify SiteBlitz again in T2 and split the long sentence

Before

One more detail about the sample page for [Business]. For a salon, it would show your services with prices, an appointment request and your timings, with WhatsApp and call buttons so clients can reach you from their phone. Shall I make it and send it here?

After — salon version

I'm [Sender] from SiteBlitz, a small web studio in Gujarat.

The sample page for [Business] would show your salon services, prices, opening hours and an appointment request. It would include WhatsApp and call buttons.

Shall I make a sample page for [Business] and send it here?

The introduction is an identity sentence, not a greeting or sign-off. The WhatsApp and call buttons remain the additional useful information. The question remains the only question and the last sentence. These features and the T2 constraints are present in the supplied specification. 
Pasted text
 
Pasted text

Benefit: less dependence on the recipient remembering T1, particularly for P2 and shared-inbox readers.
Cost/upkeep: update the T2 reference and validate its vertical substitutions; no additional vendor spend expected.
Risk/test: salon wording must not leak into other verticals. Test correct vertical details, both buttons, exactly one final question and no additional offer.

Word-count check

I checked the supplied examples and these revisions using whitespace-separated words, a one-word business, a one-word sender, a one-token domain and the date 12 November 2026, matching the examples’ stated assumptions.

Body	Original	Revised	Required
T1 SOCIAL_ONLY, salon	64	Unchanged	60–85
T1 SOCIAL_ONLY, other	62	Unchanged	60–85
T1 NO_VIEWPORT, coaching	66	63	60–85
T1 SITE_DOWN, showroom	74	Unchanged	60–85
T2, salon	46	46	40–70
T3	39	Unchanged	30–50

The original reference counts are correct. The production validator must still count the fully substituted text: longer business and sender names change the result. I have not inspected its token-counting implementation.

These changes introduce no additional links, prices, questions or claims. They retain the existing [domain] reference; the ambiguity between that reference and the no-link rule remains a separate release issue below.

4. Anything untrue, risky or likely to cause a spam complaint?

Need data — the main remaining risks are whether the evidence and system behaviour support the words. I would require the following checks before unconditional approval.

4.1 Observation accuracy and freshness
Variant	What the supplied wording can support	What it must not imply	Proposed release test
SOCIAL_ONLY	No website link was visible in the checked Instagram bio at the stated time.	No website exists, or the business needs one.	Review the correct profile and relevant link area. Retain evidence supporting the exact sentence.
NO_VIEWPORT	The checked homepage displayed very small text in the specified rendered view.	Every mobile device is affected, a particular technical cause is proven, or sales are being lost.	Reviewer confirms that the stored screenshot supports the visible-text observation.
SITE_DOWN	The homepage failed in the stated checks, including a recent pre-send check.	A permanent outage, a lapsed subscription or a need to replace the site.	Record check times and recheck before dispatch. Hold if the current evidence contradicts the message.

The original observations are appropriately qualified, particularly the SITE_DOWN temporary-interruption sentence. Preserve that qualification. 
Pasted text

For “shortly before this email,” my proposed operational definition is within 15 minutes of actual dispatch, not draft generation. This is an internal test threshold, not an external standard. A delayed queue or retry must not send yesterday’s “shortly before” claim.

Cost: extra checks, evidence storage and occasional manual review; actual rupee cost is unknown without the infrastructure. Benefit: recipients and sender credibility. Pass threshold: no dispatched message with unsupported or contradicted observation text.

4.2 The domain/no-link rule is unresolved

The document simultaneously requires domains in NO_VIEWPORT and SITE_DOWN observations, and says there is no other URL anywhere in the assembled message. 
Pasted text
 
Pasted text

This is a specification ambiguity, not a demonstrated implementation bug.

Clarify whether the rule prohibits authored hyperlinks and explicit URLs, or also prohibits bare domain text that a recipient application might turn into a link. Then test the actual validator and recipient rendering.

Do not silently exempt a checked domain while continuing to claim that the stricter interpretation is enforced. Under a literal prohibition on every website link in the recipient’s view, the existing domain-bearing observations may need an upstream specification change.

Cost/test: a rule decision and regression fixtures, not another service. The test must use the final assembled email and its recipient rendering, not just the model’s JSON.

4.3 The offer needs verifiable commercial backing

The document references company-facts.md, but its contents are not supplied. Therefore I cannot verify the real package scope or economics behind ₹7,999. 
Pasted text

Before sending, establish that the advertised starting package genuinely exists at that price, and define the domain, hosting, tax and recurring-charge treatment for the subsequent quotation.

The sample page’s commercial terms are also unspecified. Do not add “free,” “no obligation,” a turnaround promise or unlimited revisions without approval and support. Conversely, do not let an interested reply unexpectedly trigger an invoice.

Keep “appointment request” distinct from any unverified promise of an automated booking system.

Cost/test: founder confirmation of the package and sample policy; no new marketing tooling. Pass when the team can fulfil the described offer without contradicting the email or introducing an undisclosed mandatory condition.

4.4 Opt-out, closure and final-message promises must be enforced

The supplied text promises an unsubscribe route and says no further follow-ups are planned. Its stored assembled form is allowed to contain an unsubscribe placeholder before sending. 
Pasted text
 
Pasted text
 
Pasted text

My required tests are:

Opt-out: a stop request received before a queued touch prevents that touch. Natural-language refusals receive review rather than requiring the exact word “stop.”
Closure: after T3, routine re-enrolment or an alternate-address campaign does not contradict the promise to that business.
Final assembly: the actual outgoing message contains a working unsubscribe destination and no unresolved placeholder.

Also stop the automated sequence when a person replies so that a relevant conversation is not followed by an inappropriate automated close.

Cost: suppression and queue-race tests, plus ongoing reply review. Benefit: recipient control and trust. Pass threshold: zero post-suppression sends in the tested cases. A footer alone is not sufficient.

4.5 The stated sending volume needs reconciliation

The context says 10 new businesses per sending day, Tuesday–Thursday, with three touches. P10 instead describes 10 sends a day. Those are not equivalent. 
Pasted text
 
Pasted text

Under the stated intake, with no replies or suppressions:

30 new businesses per week × 3 touches = up to 90 messages per week at steady state.

That is arithmetic from the proposed schedule, not a forecast of actual traffic. If all messages are restricted to three sending days, it averages up to 30 messages per sending day; actual peaks depend on scheduling.

Clarify whether Tuesday–Thursday restricts new starts only or all touches, and how Day 6 and Day 14 move when they fall outside the allowed window.

Cost/test: a schedule simulation covering several overlapping cohorts. Pass when the worst-case queue respects an explicitly approved total-message cap, not merely a new-business cap.

4.6 Validator claims need semantic tests, not just format tests

The listed validator checks include word counts, exact lines, questions, banned phrases and links. They do not expressly demonstrate every semantic requirement, such as whether T2 adds genuinely new information or whether the chosen vertical is correct. That absence in the table does not prove the implementation lacks those checks. 
Pasted text

Ask Claude Code for fixtures showing that the system rejects a wrong vertical, unsupported package feature, misleading observation and T2 that merely repeats T1 without the required additional detail.

Cost: additional regression cases. Benefit: preventing a formally compliant but misleading message. Pass threshold: each deliberately invalid fixture is held, and each approved reference passes.

4.7 Provider policy and Indian legal status are separate checks

Gmail as the recipient is not the same question as Gmail being the sending service.

Google’s Gmail Program Policies, last updated 20 October 2026, prohibit using Gmail to distribute unsolicited commercial mail. The page also distinguishes organisational accounts whose agreements may differ. Google Workspace’s abuse policy refers to its applicable acceptable-use agreement and possible account suspension. Authentication and small volume are not permission to ignore those terms. Confidence: high in the published policy text; the actual sending provider and applicable agreement here are unknown. Gmail policy · Workspace abuse policy. 
Google Help
+1

Indian law: do not treat “India-only” or “publicly found email” as a complete legal analysis. The DPDP Act’s section 3(c)(ii) public-availability exclusion is specifically framed around data made public by the individual concerned or by someone legally obliged to publish it; it is not an unrestricted “anything found online” exception. The commencement notification dated 13 November 2025 stages the principal processing provisions eighteen months after publication, in May 2027, rather than making the entire framework operative by this review date of 12 November 2026. Confidence: high in the cited statutory wording and staged commencement; applicability to this dataset requires counsel. DPDP Act · Commencement notification. 
MeitY
+1

Proposal: confirm the sending service’s applicable policy and retain each contact’s source and collection context for legal review. If a route is disallowed, use a consent-led route or a service whose applicable policy permits the documented lawful use—not account rotation to bypass restrictions. Legal-review cost is unknown; the benefit is avoiding a launch built on an unsupported permission assumption.

Points still open
Actual rendered messages: final sender identity, signature, vertical substitutions and language configuration have not been inspected.
NO_VIEWPORT revision: whether the simpler observation and factual subject will be adopted upstream in E1.
Domain/no-link interpretation: one consistent rule, supported by validator tests and recipient rendering.
Operational evidence: fresh SITE_DOWN checks, working unsubscribe replacement, reply/opt-out suppression and no routine re-enrolment after T3.
Commercial facts: verified ₹7,999 package scope and explicit sample-page terms.
Schedule and permission: total-message cap, follow-up date handling, sending-provider policy and contact-provenance review.
Real-reader results: whether the English templates meet the comprehension threshold, especially for P1.

Bottom line: retain the structure, make the three targeted edits, and resolve the evidence and sending-control questions. More persuasive wording is not the missing launch safeguard.
