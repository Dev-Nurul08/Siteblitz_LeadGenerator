# SiteBlitz Lead Intelligence OS — Technical Review and Response to Claude Code

Review date: 8 November 2026\
Decision: Agree with the direction of rebuilding SiteBlitz, but challenge several important architectural and scoring decisions.

The audit identifies a more fundamental problem than a broken scraper or confusing UI: SiteBlitz currently confuses discovering a business with proving that the business needs a website.

Those must become two separate operations.

The future system should be designed around five principles:

- Discovery: Find real businesses in a selected country, city and industry.
- Verification: Establish their actual website and social presence using evidence.
- Intelligence: Determine whether a website would solve a genuine business problem.
- Qualification: Identify commercially worthwhile opportunities with a lawful contact route.
- Conversion: Help SiteBlitz turn verified opportunities into customers.

I am treating Claude Code's reported live probes and code audit as evidence supplied for this review. I have not independently executed the repository.

## 1. Data sources — Google Places, OSM, CSV and social platforms

Verdict: Partially agree. Disagree with making Google Places API the unconditional primary source.

Claude is correct that the present OSM implementation is unreliable. The supplied audit identifies an HTTP 406 error, incorrect city-area filters, missing business exclusions and defective import deduplication.

However, fixing coverage by moving everything to Google Places introduces a serious architectural risk.

### The Google Places licensing problem

Google Places API (New) provides valuable business information, including website URLs, phone numbers and business status. But official API access does not automatically grant permission to build a permanent independent prospecting database from Google's information.

Google's current Maps Platform terms restrict exporting, storing and creating content based on Maps data beyond permitted uses. Its Places policies make specific exceptions for identifiers such as Place IDs, but not general unrestricted business-record retention.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://cloud.google.com\&sz=32)

Google Cloud+1



For an internal sales-intelligence system that permanently stores businesses and enriches them for outreach, this is material.

My proposal:

Use a source-agnostic discovery architecture:

| Source                          | Recommended role                                                                      |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| OpenStreetMap                   | Foundational open-data discovery                                                      |
| Licensed business-data provider | Commercial-scale discovery, if CRM and outreach use are contractually permitted       |
| Official business registries    | Supplemental evidence, where licensing permits                                        |
| Business-owned websites         | Primary verification of business identity, services and published contact information |
| Google Places API               | Conditional enrichment or verification only within a reviewed, permitted use case     |
| CSV                             | Import from lawful external sources with source tracking                              |
| Social platforms                | Authorized APIs, permitted public links or manual review                              |

Google Places should remain an optional adapter, not a dependency the entire product cannot operate without.

Also, website and phone fields can invoke higher-cost Places API SKUs. Pricing is based on fields requested, so field masks and monthly billing caps matter.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.google.com\&sz=32)

Google for Developers+1



### Immediate technical corrections

Fix the OSM city queries, set an identifiable User-Agent, correct category mappings, repair CSV identifiers and replace name-plus-country deduplication with location-aware identity matching.

Keep OSM usage limits and its ODbL attribution and database-license obligations in mind.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wiki.openstreetmap.org\&sz=32)

OpenStreetMap Wiki+1



Cost: Low incremental API expenditure for open-data discovery; moderate development and data-maintenance effort. Licensed commercial sources introduce variable fees.

Risk: Data licensing, incomplete geographic coverage, duplicate businesses.

Acceptance test: Import and evaluate 500 businesses from two different sources. Demonstrate zero incorrectly merged businesses in a manually reviewed sample of 100, correct source attribution and a documented lawful basis for retaining the records.

Confidence: High on the technical direction and Google's published restrictions; legal applicability to the intended implementation needs counsel or provider confirmation.

## 2. Social presence — Instagram, Facebook, LinkedIn and TikTok

Verdict: Agree with using lawful discovery signals, but disagree that three signal types are sufficient for comprehensive coverage.

The proposed sources — business-provided social URLs, OSM contact tags and links from business-owned websites — form a sensible minimum viable implementation.

However, many businesses without websites are active primarily on social platforms. Relying only on those three sources will miss a meaningful part of the target market.

I recommend adding permitted search-engine APIs, business directories with suitable licenses, owner-submitted profiles and manual researcher verification.

Do not implement automated logged-in browser extraction, account rotation or CAPTCHA avoidance.

LinkedIn explicitly restricts unauthorized scraping and automated browser activity. TikTok's ordinary Display API requires account authorization and is not a general-purpose directory of every local business.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.linkedin.com\&sz=32)

LinkedIn Help+1



### Important distinction

A business may have:

- Instagram and no website.
- Facebook and a website not listed on its profile.
- A link-in-bio directing visitors to an independent domain.
- A booking platform that meets its immediate needs.
- Several unofficial profiles unrelated to the actual owner.

Therefore, finding a social profile must never automatically mean the business needs a website.

Create a `SocialIdentity` record containing the platform, URL, evidence source, observed date and identity-match status.

The system should distinguish profile discovered from profile confirmed to belong to the business.

Cost: Low to moderate for permitted link discovery; higher where paid search APIs or manual verification are needed.

Risk: False identity matches, restricted platform data and missing profiles.

Acceptance test: On 100 manually researched businesses, target at least 95% precision for confirmed social-profile ownership. Measure discovery recall separately rather than pretending all profiles are findable.

Confidence: High regarding documented platform limitations; medium regarding achievable social-profile coverage, which needs market testing.

## 3. Verify whether a business actually needs a website

Verdict: Agree with replacing the current detector. Disagree with some of Claude's verification assumptions.

This is the most important business-logic decision in the entire project.

The current implementation makes two mistakes:

1. An empty website field is interpreted as proof that no website exists.
2. A business category is interpreted as proof that a particular digital service is needed.

Neither inference is reliable.

### My proposed Website Intelligence Engine

Implement the following process:

Business discovered

Normalized identity, location, category and source

Business verification

Operating status, independent owner, exclusions, duplicates

Website investigation

Published domains → permitted search → redirects → website audit

Website verified

Check improvement needs

No site identified

Assess a new website

Website inaccessible

Retest or investigate

Evidence insufficient

Manual review required

Evidence-based opportunity decision

Opportunity type, reason, confidence and next action

### Challenge to Claude's verification rules

A missing website in Places, OSM or CSV is not proof of absence. It is merely missing information. Even searching several sources cannot prove that no website exists anywhere. The accurate verdict is no independent website identified after specified checks.

Similarly:

- An unregistered or unresolvable guessed domain does not prove that the business has no website.
- A domain that resolves does not establish that it belongs to the business.
- HTTP 403 may indicate bot protection, not a broken website.
- A timeout or single HTTP 5xx may be temporary.
- A social profile linked from a business listing may belong to another business with a similar name.
- A `business.site` URL must be checked for its actual present behavior, not automatically declared dead.

For inaccessible websites, use bounded retries, preferably across separate observation times, followed by manual review if the result remains ambiguous.

### Business activity and exclusions

I agree with excluding permanently closed establishments, ATMs, government offices and businesses outside the studio's service market.

I disagree with using the same business name appearing three times as proof of a chain. Generic local names repeat across cities.

Use verified brand identity, location relationships and ownership evidence. A franchise may also be independently owned and capable of purchasing its own website, so the exclusion rule should be configurable.

### Final website-status model

| Status                 | Meaning                                                               |
| ---------------------- | --------------------------------------------------------------------- |
| `OWN_SITE_VERIFIED`    | Business-owned website established                                    |
| `SOCIAL_ONLY_VERIFIED` | Social presence found, no independent website identified after checks |
| `NO_SITE_VERIFIED`     | Investigation completed with no identifiable independent website      |
| `SITE_DOWN_CONFIRMED`  | Repeated, corroborated website failure                                |
| `UNKNOWN`              | Evidence insufficient or contradictory                                |
| `SKIP`                 | Excluded or unsuitable business                                       |

I would keep the historical evidence separate from the current verdict, so future rechecks can explain why a classification changed.

Cost: Moderate engineering effort and ongoing verification requests.

Who benefits: The sales team, which avoids pitching websites to businesses that already have them; potential customers, who receive more relevant approaches.

Acceptance test: Build a manually verified benchmark of at least 200 businesses from multiple categories. Require at least 90% precision in the `NO_SITE_VERIFIED` and `SOCIAL_ONLY_VERIFIED` groups before allowing automatic HOT qualification. Ambiguous cases must remain `UNKNOWN`.

Risk: Incomplete public information and false ownership matches.

Confidence: High that evidence-based classification is necessary. The proposed 90% target is an initial engineering acceptance criterion, not a demonstrated performance result.

## 4. Website Need Score and HOT / WARM / COLD / SKIP tiers

Verdict: Disagree with Claude's current scoring formula. Agree with the need for explainable tiers.

The proposed 45 + 25 + 15 + 15 model looks structured, but it combines unrelated things.

There are four specific weaknesses.

First: Reviews and ratings are not reliable proof of operational activity. A business might have 100 historical reviews and be permanently inactive.

Second: Having a phone number does not mean a business needs a website. Contactability is a separate question.

Third: A category does not establish purchasing power. A dentist may have no budget, while a small furniture manufacturer may be ready to invest heavily.

Fourth: Assigning exact scores and a fixed 92% confidence creates an appearance of certainty without a validated model.

### My revised model

Separate the need score from the decision about whether the sales team can contact the business.

Website Need Score

## 100 pts

Verified website gap

60

Demonstrable business problem

20

Recent business activity

10

Commercial service fit

10

Proposed pilot weights, to be validated against human-reviewed leads and actual sales outcomes.

For the website-gap component, I suggest provisional values of 60 for no independent website identified after thorough checks, 55 for verified social-only presence, 50 for repeated confirmed website failure, 10–35 for demonstrable major problems with a functioning site, and zero for a functioning site without an established need.

Unknown website status must remain unscored, not treated as a negative or a positive result.

The 20-point business-problem component should reflect concrete friction such as appointment inquiries handled manually, an inaccessible product catalog or a broken inquiry process. It should not be assigned just because a business belongs to a category.

### Proposed initial thresholds

HOT

80–100

Strong website-need evidence, confirmed activity, identifiable business problem and lawful outreach route.

WARM

60–79

Plausible opportunity; additional verification or qualification required.

COLD

0–59

Low current priority or no convincing evidence of need.

REVIEW

No score

Missing, outdated or contradictory evidence. Human review required.

SKIP

Excluded

Outside target, duplicate, permanently closed, or suppressed.

A HOT score must additionally pass hard eligibility gates: active business, verified identity, substantial website gap, sufficient evidence freshness, and an outreach method allowed by the applicable rules.

A phone number must not be mandatory for HOT. An appropriate verified email, permitted business contact form or other lawful route could be sufficient.

I would also store three independent indicators:

| Indicator           | Purpose                                             |
| ------------------- | --------------------------------------------------- |
| Website Need Score  | How strong is the website opportunity?              |
| Evidence Confidence | How much trustworthy evidence supports the verdict? |
| Outreach Readiness  | Can and should SiteBlitz contact this business now? |

In other words, HOT means a strong evidence-based sales opportunity, not that the owner has confirmed an intention to buy.

Cost: Moderate initial rule-engine effort; ongoing benchmark review. No expensive AI model is required for the first version.

Who benefits: Sales representatives can concentrate on justified prospects, and the founder can audit every decision.

Acceptance test: Have independent reviewers label 200 leads. Require at least 90% HOT precision as an initial target, inspect false positives individually, and compare sales-qualified lead rates against the old scoring model.

Risk: Arbitrary weights and bias toward categories or countries with better public data.

Confidence: High in separating the three indicators; medium in the proposed weights and thresholds until calibrated.

## 5. Qualification pipeline — phone, WhatsApp and email

Verdict: Agree with making phone a first-class contact channel. Disagree with treating WhatsApp as an automatically available alternative.

Claude has identified a real contradiction: the businesses most likely to need a new website may have neither a domain nor a domain-based email address.

The current email-first pipeline therefore eliminates precisely the businesses SiteBlitz wants to find.

### Proposed contact strategy

The system should separate commercial qualification from contact availability.

A business can be a good opportunity even when no contact method has yet been verified.

Create a contact-channel registry with these states:

| Channel         | Conditions for use                                                           |
| --------------- | ---------------------------------------------------------------------------- |
| Phone           | Published, verified number; lawful marketing call                            |
| Email           | Actual discovered address; relevant consent or other applicable lawful basis |
| WhatsApp        | Valid recipient opt-in and compliant business messaging                      |
| Social DM       | Platform-permitted contact route and applicable marketing permissions        |
| Contact form    | Genuine form available and use for solicitation permitted                    |
| Manual research | No compliant channel currently established                                   |

Important legal limitation: WhatsApp's Business Messaging Policy, updated September 23, 2026, requires an appropriate recipient opt-in before business-initiated messages. A published phone number alone is not permission to send a WhatsApp sales message.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://whatsappbusiness.com\&sz=32)

WhatsApp for Business



This is particularly relevant to a business selling internationally.

For example, the UK distinguishes corporate subscribers from sole traders under PECR, and marketing calls require screening against relevant preference and suppression lists. The US CAN-SPAM Act also applies to commercial B2B email. India's TRAI framework regulates unsolicited commercial calls and messages.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://ico.org.uk\&sz=32)

Information Commissioner's Office+3



These are requirements for legal review by country, not one universal permission rule.

### Recommended changes

Eliminate generated `info@domain` addresses completely. A guessed address is not a contact.

Add channel-specific outreach eligibility, verified sender identity, opt-out tracking, country policies and a central suppression list.

Keep sending disabled until real integrations and status reconciliation are tested. The current behavior of marking an unsent message as SENT is unacceptable.

The unsubscribe endpoint also needs repair. A normal GET link should reach a usable page; any confirmation or unsubscribe action should be handled safely, including protection against automated link scanners.

Cost: Moderate development, plus variable email, messaging or calling expenditure.

Who benefits: SiteBlitz gains access to genuine website opportunities without relying on fictional email addresses.

Risk: Regulatory violations, spam complaints and poor deliverability.

Acceptance test: Zero fabricated contacts; zero WhatsApp messages initiated without recorded qualifying permission; 100% of opt-outs reflected in the suppression list; every SENT status supported by an actual provider event.

Confidence: High on the architectural recommendation and the cited official policies.

## 6. Reliability — background processing, databases and API execution

Verdict: Agree with background jobs. Partially agree with SQLite as the default.

The supplied audit shows that SiteBlitz currently mixes interactive HTTP requests with long-running network operations.

That is an architectural problem, not simply an API timeout problem.

### Proposed architecture

React Frontend

Start search, view progress, review evidence

FastAPI

Validate request, create job, return job ID

Persistent Job Queue + Worker

Restart recovery, retries, checkpoints and rate limits

Discovery adapters

Website verifier

Lead evaluator

Database + Evidence Store

Jobs, businesses, observations, verdicts, contacts

### Database recommendation

SQLite can be the zero-setup default for local development and single-instance pilots, with WAL mode, bounded writing and one durable worker.

For multi-user deployments, several concurrent workers or significant write throughput, PostgreSQL should become the recommended production database.

Do not introduce Redis merely because it is declared in the dependency list. Choose a persistent job mechanism that matches deployment needs. FastAPI's in-process background tasks alone are not a durable queue.

### Non-negotiable reliability features

- Every job gets a persistent ID and explicit state: queued, running, completed, partial, failed or cancelled.
- Every stage is retryable and idempotent.
- Errors are recorded per source and business rather than silently swallowed.
- Source adapters have bounded concurrency, rate limits and exponential backoff.
- Jobs can recover after worker restart without duplicating records.
- Import and discovery deduplication use stable source identities and actual business-identity checks.
- External website fetching has protection against SSRF, unsafe redirects, private-network destinations and unbounded downloads.
- Database migrations cover all five phases; production correctness must not rely on `create_all`.
- Integration tests use real API/database interactions, with controlled external-source fixtures and separately monitored live smoke tests.

The existing 136 passing mocked unit tests are useful, but they do not establish end-to-end reliability.

Cost: Moderate one-time backend refactoring; small but ongoing worker and database hosting costs.

Who benefits: Every operator, because long searches no longer freeze the interface or lose progress.

Acceptance test: Process 1,000 imported businesses, forcibly restart the worker halfway through, and verify that all jobs recover without duplicate business records or lost results. Target a 99%+ successful completion rate for valid test jobs, excluding documented external-source outages.

Risk: Queue complexity, SQLite write contention and uncontrolled API spend.

Confidence: High in the proposed design; database selection should be finalized against actual expected concurrency.

## 7. UI workflow, product simplification and deleting unreliable features

Verdict: Agree with replacing the eight engine-named pages with four steps. But this must be a workflow redesign, not merely a visual redesign.

The current interface exposes internal development terminology instead of guiding a salesperson toward a useful outcome.

An operator should not have to understand the differences between Discovery Engine, Opportunity Engine, Enrichment Engine and Qualification Engine before finding their first customer.

### Recommended SiteBlitz interface

SiteBlitz

Lead Intelligence Workspace

1

Find

2

Review

3

Hot Leads

4

Outreach

1\. Find businesses

Select country, city, industry, permitted data source and search limits. Start a job and watch its actual progress.

2\. Review evidence

Inspect website verification, active status, duplicate matches, missing fields and exceptions.

3\. Hot leads

See ranked opportunities with their website status, factual evidence, potential service and reason for qualification.

4\. Outreach

Review compliant contact routes, approve drafts, record actual sends, manage replies and track conversion.

An individual lead should answer these questions immediately:

Who is this business? Does it have a website? What evidence was checked? Why is it HOT? How can SiteBlitz lawfully reach it? What should the salesperson do next?

The interface also needs to show what went wrong. A discovery job with zero businesses must display the underlying source error, not an unexplained empty result.

### Fix or remove the following features

| Priority | Audit evidence                                  | Required action                                                     |
| -------- | ----------------------------------------------- | ------------------------------------------------------------------- |
| P0       | A1, A2: installation and imports fail           | Repair build backend and mandatory dependencies                     |
| P0       | A3, A4: OSM searches return zero                | Repair requests, area selection and category queries                |
| P0       | A5 and dedup flaw                               | Repair CSV identity and prevent cross-city false merges             |
| P0       | A7, A8: `MissingGreenlet` crashes               | Correct async relationship loading                                  |
| P0       | A9: unsubscribe HTTP 405                        | Repair the unsubscribe workflow                                     |
| P0       | A12 and fabricated sending                      | Remove invented contacts, sender identity, claims and SENT statuses |
| P1       | A10, A11: misleading opportunities              | Replace detector and scorer                                         |
| P1       | Stale opportunities remain active               | Add reevaluation and status transitions                             |
| P1       | Incomplete Alembic migrations                   | Migrate all required tables                                         |
| P1       | A6 and unstyled UI elements                     | Repair counters, styling and job navigation                         |
| P2       | Wikidata and automatic mobile-app opportunities | Remove from the initial workflow                                    |

I particularly agree with deleting the fake personalization.

SiteBlitz must never tell a buyer that it has reviewed customer feedback, built a preview or observed a problem unless the system actually has evidence for that statement.

An opportunity pitch should reference observed facts, not invented conversion improvements or unsupported statistics.

Cost: Moderate frontend and integration refactoring; lower long-term maintenance from removing unreliable features.

Who benefits: Nontechnical operators, developers diagnosing failures, and the founder evaluating lead quality.

Acceptance test: Give five first-time operators a city and industry. At least four should be able to start discovery, find a verified opportunity and understand its evidence without assistance. All actions shown in the UI must have functioning backend behavior.

Risk: Hiding unreliable modules without repairing their underlying data or state transitions.

Confidence: High.

## Three additional proposals Claude Code should consider

These go beyond repairing the current implementation.

### A. Moment-of-Need Intelligence

Instead of simply looking for businesses without websites, discover businesses experiencing a reason to purchase one.

Examples include a newly launched local business, a company expanding to another location, an independently corroborated website outage, or a business publicly requesting help with online orders.

The source must be licensed or otherwise permissible, and every trigger must be recorded.

Cost: Moderate additional discovery engineering and source subscriptions.\
Risk: Outdated announcements or wrongly linked businesses.\
Success test: Compare qualified-conversation rates for 100 trigger-based leads against 100 matched conventional leads.

### B. Evidence-Based Micro-Proposals

For a verified opportunity, generate a short, reviewable proposal based on actual findings:

- Observed digital-presence gap.
- Business-specific reason the issue matters.
- Proposed website or feature.
- Illustrative concept clearly labeled as a concept.
- Estimated project scope, with any costs identified as estimates.

This could make SiteBlitz materially different from a generic lead database. Human approval should precede sending any proposal.

Cost: Moderate implementation and ongoing proposal-generation costs.\
Risk: Inaccurate personalization or unapproved claims.\
Success test: Compare meeting-booking and proposal-acceptance rates against standard outreach.

### C. Continuous Learning From Sales Outcomes

SiteBlitz should learn which evidence actually predicts useful sales opportunities.

If 100 HOT leads produce no interested buyers, the intelligence system has not succeeded, regardless of how accurate its website detection was.

Track verification accuracy, qualified conversations, meeting bookings, proposals, wins and acquisition cost by market and industry.

Initially, improve deterministic rules from human-reviewed outcomes. Later, introduce a calibrated machine-learning ranking model once sufficient historical labels exist.

For an AI-agent-driven future, keep the evidence store structured and machine-readable so authorized research, qualification and purchasing agents can exchange verifiable facts rather than unsupported sales claims.

Cost: Low initially for event tracking, higher later for statistical modeling and maintenance.\
Risk: Learning from a small or biased sales sample.\
Success test: Demonstrate improved qualified-opportunity and win rates in a held-out evaluation before promoting a new ranking model.

One additional source worth piloting for point 2 is Meta's authorized Instagram Business Discovery capability for suitable professional accounts. It has authentication and permission constraints and is not an unrestricted local-business search engine.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.postman.com\&sz=32)

Postman API Network



## Recommended execution order

| Phase          | Delivery                                                                | Completion criterion                                        |
| -------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------- |
| 1 — Stabilize  | Make install, API, imports, migrations and current discovery functional | Real end-to-end tests pass                                  |
| 2 — Verify     | Reliable business identities, website evidence and rechecks             | At least 90% precision on the agreed verification benchmark |
| 3 — Prioritize | New scoring, exclusions, evidence confidence and HOT tiers              | At least 90% HOT precision on pilot labels                  |
| 4 — Operate    | Four-step UI, background jobs, progress and retry support               | Operators finish full workflows without guidance            |
| 5 — Convert    | Verified contact channels, compliant outreach, genuine send tracking    | Measurable qualified conversations and no fabricated sends  |
| 6 — Optimize   | Trigger intelligence, evidence-based proposals and feedback learning    | Higher qualified-lead yield than the baseline               |

These are proposed acceptance gates, not claims that the current system achieves them.

## Overall decision

Do not rebuild all five engines simultaneously. First build one small, fully functional vertical slice from lawful discovery to a verified HOT lead, then expand.

I would authorize Claude Code to proceed with the critical stability fixes, the new evidence model and the simplified UI. I would not yet authorize Google Places as the permanent CRM discovery foundation, Claude's proposed scoring weights as final, or automated outreach.

The critical difference is:

A lead generator collects business names. A lead-intelligence system proves why a business is a worthwhile prospect. SiteBlitz should become the second.

The source-policy review above reflects documentation accessible on November 8, 2026. Google's exact policy-effective date was not independently established; WhatsApp's cited messaging policy states September 23, 2026. Legal interpretations require professional confirmation.

## Points still open

1. Data-source rights: Which licensed sources explicitly permit storing and using business data for permanent prospecting and outreach?
2. Initial market: Which country, two industries and geographic area should form the first 200-business pilot?
3. Definition of HOT: Should this represent website need only, or a combined website need and sales-readiness decision?
4. Verification standard: What exact checks and freshness requirements justify `NO_SITE_VERIFIED`?
5. Scoring calibration: Will the team approve the initial proposed thresholds and adjust them using manually reviewed results?
6. Outreach permissions: Which channels can be enabled in each launch country, and who will approve the relevant compliance rules?
7. Deployment scale: How many businesses per month, concurrent users and workers are expected, and what is the API/hosting budget?
8. Existing architecture: Which database tables and services can be repaired and retained, versus deleted without migration risk?
9. Commercial success: What target cost per verified HOT lead, qualified meeting and won project will make SiteBlitz economically successful?

These nine decisions should be resolved or explicitly recorded as assumptions before the full rebuild proceeds.
