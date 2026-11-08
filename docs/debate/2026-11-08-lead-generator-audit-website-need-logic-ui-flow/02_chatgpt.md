# Round 2 — SiteBlitz: My Decisions for Claude Code

Date: 8 November 2026\
Overall verdict: The P0 repairs and architectural decisions are accepted based on Claude Code's reported tests. No reason to reopen A1–A9 unless integration tests reveal regressions.

I recommend proceeding with the Website Intelligence Engine, subject to the four decisions below.

## Q1. Is web search mandatory before classifying a lead as HOT?

Verdict: AGREE — search-level verification should be mandatory for automatic HOT. DISAGREE that an API key must be mandatory, or that domain guessing proves website absence.

For the 200-business pilot, either a permitted search API or a documented manual search by the founder should qualify.

### My corrections to the checklist

| Check                                   | Decision                | Reason                                                                  |
| --------------------------------------- | ----------------------- | ----------------------------------------------------------------------- |
| (a) No website in linked source records | Agree                   | Missing fields are weak negative evidence, not proof of absence         |
| (b) Inspect linked social profiles      | Agree                   | A profile that cannot be inspected must be marked unchecked             |
| (c) Guess domains and inspect DNS/pages | Modify                  | Useful for discovering candidates, not proving the absence of a website |
| (d) Search top 10 results               | Agree with modification | Require search for HOT, with API or recorded manual review              |
| (e) Evidence younger than 30 days       | Agree                   | Reasonable initial freshness policy; not a guarantee of correctness     |

Critical correction to (c): A legitimate business website might not contain its city or exact registered name on its homepage. It might use a brand name, regional language, or JavaScript-rendered content.

Therefore, `domain resolves but name + city not found` must never automatically mean the domain is unrelated.

Match candidates using several identity signals: business name, phone, address, branding, links from an owner-controlled profile, and other independent evidence.

For (d), I would search both business name + city and business name + a distinguishing identifier, when available. The first 10 results are a practical search boundary, not proof that no other website exists.

### Final classification rule

- Full checks passed, including search: `NO_SITE_VERIFIED`, high evidence confidence, HOT-eligible.
- Source and social checks passed, but no search performed: `NO_SITE_VERIFIED` with medium confidence, capped at WARM, provided there is no contradictory evidence. Display it as "No website identified — limited verification."
- Mandatory checks blocked, ambiguous ownership, or conflicting website evidence: `UNKNOWN` → REVIEW, no score.
- Independent website positively identified: `OWN_SITE_VERIFIED`, regardless of missing website fields elsewhere.

This deliberately changes the proposed "all checks or UNKNOWN" wording so that the agreed medium-confidence WARM state remains possible.

Implementation decision for Claude Code: Make search verification mandatory for automatic HOT, but allow a human-verified equivalent. Do not require a paid search API to launch the pilot.

Cost: Additional search requests or manual reviewer time. Risk: Missed websites and incorrect identity matches. Benefit: Fewer false HOT leads. Test: Zero automatically promoted HOT leads without documented search verification; assess the resulting website-status accuracy against founder-reviewed cases.

Confidence: High in this decision. The 30-day freshness window is a proposed policy to validate.

## Q2. Are Claude's four observable business-problem signals acceptable?

Verdict: PARTIALLY DISAGREE. Two are useful, one needs stronger evidence, and one would double-count the website gap.

| Proposed signal                                                  | My decision                                                                                                     | Problem points |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------- |
| Dead, parked or expired listed domain                            | Count under website-gap score, not again as a business problem                                                  | 0 additional   |
| Social-only profile directs customers exclusively to WhatsApp/DM | Accept if the business owns the profile and the contact path is explicit                                        | 5–10           |
| Booking category with no booking channel found                   | Insufficient by itself; require explicit phone-only booking evidence or another verified operational limitation | 0–10           |
| Menu/catalog available only on third-party aggregators           | Accept if independently verified and an owned alternative was checked                                           | 5–8            |

I recommend two additional signals:

- Broken inquiry or booking journey: Up to 15–20 points, where a real customer-facing workflow has been tested and the failure recorded.
- Explicit business-owner statement that a website is needed or unavailable: Up to 20 points, if attributable, recent and directly relevant.

Use the strongest applicable independent evidence, with a total cap of 20 points. Do not award multiple sets of points for the same underlying fact.

### Claude's mathematical objection is correct, but does not require filling all 20 points

Under my proposed model:

| Component                     | Example  |
| ----------------------------- | -------- |
| Verified website gap          | 60       |
| Demonstrable business problem | 0        |
| Confirmed recent activity     | 10       |
| Commercial service fit        | 10       |
| Total                         | 80 — HOT |

A missing website plus verified activity and strong agency fit can legitimately reach 80 without inventing an additional problem. But a business with uncertain activity or weak fit should remain WARM, even if no website is identified.

The 20-point category is intended to distinguish stronger opportunities, not to create mandatory points for every no-website lead.

Implementation decision: Retain the 60/20/10/10 scoring model for the pilot. Apply the revised signal definitions, store evidence for each awarded point, and forbid double-counting.

Cost: Low for deterministic scoring; moderate additional work for link and workflow verification. Risk: Weak negative evidence inflating scores. Benefit: More defensible HOT classifications. Test: Manually audit 50 scored records and require every awarded business-problem point to have a separate supporting observation.

Confidence: High regarding double-counting; medium on exact point values pending pilot calibration.

## Q3. Is OSM edit recency reliable evidence that a business is active?

Verdict: DISAGREE with awarding 5 activity points for an OSM edit within 24 months. AGREE that `check_date` can provide limited supporting evidence.

The distinction matters:

- `check_date=*` indicates when information or the existence of an OSM feature was checked.
- An OSM object's last-edit timestamp indicates a mapping edit, not a business operation.
- `opening_hours=*` may have been entered years ago.
- A phone or email field demonstrates potential contactability, not present-day activity.

The OpenStreetMap documentation explicitly distinguishes the feature-existence check from checks of individual properties.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wiki.openstreetmap.org\&sz=32)

OpenStreetMap Wiki



### My recommended activity scoring

| Evidence                                                                                  | Activity points | Interpretation                  |
| ----------------------------------------------------------------------------------------- | --------------- | ------------------------------- |
| Recent direct confirmation that business operates                                         | 10              | Strong                          |
| Recent verifiable owner-controlled business activity (e.g., a public post within 90 days) | 7               | Strong supporting evidence      |
| Credible recent independent verification of operations                                    | 5               | Moderate                        |
| OSM `check_date` within 180 days                                                          | 2               | Weak evidence of existence only |
| OSM object edited within 24 months                                                        | 0               | Not evidence of operation       |
| Opening hours listed without recent verification                                          | 0               | Metadata only                   |
| Phone or email listed                                                                     | 0               | Belongs to Outreach Readiness   |

These are provisional weights, not measured statistical probabilities. Multiple observations should not be added indiscriminately; cap the total at 10.

I also recommend a negative-status gate. OSM's `disused:*`, `abandoned:*`, `was:*` and `shop=vacant` can indicate that a business is no longer operating. Such records should be excluded or sent to REVIEW until the status is resolved.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wiki.openstreetmap.org\&sz=32)

OpenStreetMap Wiki+1



### What about Google Places?

Google defines `OPERATIONAL` as an establishment that is operating, but not necessarily open at the current moment. That is useful verification evidence.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.google.com\&sz=32)

Google for Developers



However, there is one unresolved licensing issue.

Google's Places policies restrict not only storage of Places content but also certain derived uses. Using a live Places status to persistently increase a lead's activity score is therefore not automatically safe merely because the original status was never stored. The precise use requires confirmation against Google's terms or a suitable license.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.google.com\&sz=32)

Google for Developers



### Final answer to Claude's question

If OSM is the only source, activity should normally remain UNKNOWN.

That does not force the website-status verdict itself to UNKNOWN. Website existence and business operation are separate facts.

An OSM record can receive weak existence evidence, but it should not automatically establish operational status or pass the HOT activity gate.

Google Places is optional. Recent owner-controlled activity or documented manual confirmation can provide the necessary evidence without it.

Cost: Low for OSM checks; manual verification effort for HOT candidates. Risk: Old business listings being treated as active. Benefit: Reduces outreach to closed or inactive businesses. Test: Compare inferred activity status with manual verification on 100 businesses; target at least 95% precision for those classified as confirmed active.

Confidence: High that OSM edit timestamps are unsuitable operational evidence; medium regarding the proposed weights.

## Q4. India pilot — one city, dentists and salons, 200 businesses

Verdict: AGREE with both categories and the 200-business pilot. DISAGREE with using the same founder-labeled dataset both to tune and approve automatic HOT scoring.

Dentists and salons are strong pilot choices for an Indian web-development studio because they provide contrasting business models.

[About Us | Dr.Ekta's Dental Care Clinic- Dental Clinic Ravet | Leading Root Canal Specialist and Aesthetic Dentist in Pune](https://images.openai.com/static-rsc-4/Ckm6LK51liJfJbuoWMFroAdHx09muqhV_xlB03RYXZdYxnvV_BsF8GFzteOcgofpIAXoCHOyS-guuuRothRO4cL0L30c9rRo2u7yg-ht_fGx02yJxU3gtSMs2bF7NkRid37zGvqIKvSj_q9CzatREDgy75jM6Y7dZpzCqn_Pzxs?purpose=inline)

Dentists — 100 businesses

Appointment-focused services, location-based discovery, treatment information and patient inquiries. Useful for testing whether a missing website represents a meaningful opportunity.

[Bellezza Skin & Hair Salon in Chembur, Mumbai Book Now @ ₹35](https://images.openai.com/static-rsc-4/WmWvKNcXxX5FXHt8CvLXdXYpn51ajxOBKpNyopgF4numcD3W09QbSdQ0l6z6feWaQ1GO3GJW9oliw72oljcaDPrYyNmZBl06yoLg0c4CgIRlxursdB4i3aTZY6XqnjD3ba4rz4faf0eHP-e2IPWvg91A1ZFoSZ-_cNb1q1Kki4A?purpose=inline)

Salons — 100 businesses

Often social-media-oriented, with appointment, pricing, service-menu and portfolio needs. Useful for testing social-only classification without assuming it means website demand.

For this experiment, exclude obvious national chains and large institutional providers, while retaining independent multi-location businesses where ownership and buyer identity can be established.

One city is appropriate initially because it reduces variations in geography and data coverage. Choose a city where the founder can independently verify doubtful records.

### The improvement I insist on: separate calibration from validation

Pilot evaluation

200 businesses

100 calibration

Review results and adjust rules

100 holdout

Test frozen rules without tuning

Stratify both groups across dentists and salons, and select holdout businesses randomly.

The Review screen should allow Correct / Wrong / Unsure, but those buttons alone are insufficient for useful training data.

Each review should identify what was correct or wrong: website ownership, business activity, business identity, exclusion status or website-need classification. A WRONG result should require a short reason or corrected evidence.

For the validation sample, the founder should assess the underlying evidence before seeing the model's suggested HOT tier, where practical. Otherwise, the label may be influenced by the system's own conclusion.

### Automatic HOT approval rule

I recommend:

| Gate              | Requirement                                                  |
| ----------------- | ------------------------------------------------------------ |
| HOT precision     | ≥ 90% on untouched holdout cases                             |
| Minimum sample    | At least 30 evaluated HOT predictions; 50 preferable         |
| Category coverage | Both dentists and salons represented                         |
| Evidence          | Every HOT has documented website and activity verification   |
| Unsure cases      | Adjudicate before counting them as correct                   |
| False negatives   | Audit a sample of WARM/COLD records for missed opportunities |

If the 100-business holdout does not produce enough HOT cases, expand the pilot rather than lowering the sample requirement.

The 90% precision gate should authorize a supervised automatic HOT classification pilot, not unrestricted automated outreach or worldwide deployment.

Cost: Manual review of at least 200 businesses plus additional holdout cases if necessary. Risk: Founder-label bias, category imbalance and overfitting to one city. Benefit: A real measurement of whether the system's classifications can be trusted. Test: Apply frozen scoring rules to previously unseen businesses, meet the precision and sample-size gates, and separately track lead-to-conversation conversion.

Confidence: High in the experimental design; actual commercial performance remains unknown.

## Final Round-2 decisions

| Question                      | Decision                                                                    |
| ----------------------------- | --------------------------------------------------------------------------- |
| Q1 — Web search for HOT       | Required, but manual verification can substitute for an API                 |
| Q2 — Business-problem signals | Accept with revised evidence rules and no double-counting                   |
| Q3 — OSM activity proxy       | Reject edit recency as operational proof; weak existence signal only        |
| Q4 — India pilot              | Approve dentists + salons, 200 businesses, with separate holdout validation |

Claude Code can implement these decisions without another broad architecture debate.

## Points still open

1. Google Places licensing: Confirm whether the proposed use of live business-status information in a persisted score is permitted.
2. Search verification: Define the exact evidence fields and manual-review procedure that substitute for a search API.
3. Website identity matching: Finalize the rule for confirming that a candidate domain belongs to the discovered business.
4. Business-problem weights: Keep the proposed values provisional until scored examples have been reviewed.
5. Activity verification: Finalize which non-Google evidence types satisfy the HOT activity gate.
6. Pilot location: Select the initial Indian city and define independent-business inclusion criteria.
7. HOT validation: Determine whether the first holdout produces enough HOT cases; expand it if necessary.
8. Commercial effectiveness: After website-need precision passes, separately measure whether HOT businesses actually respond, request proposals and become customers.

My final recommendation: Proceed with the Website Intelligence Engine and the 200-business pilot. The highest-priority engineering principle is to preserve the distinction between what the system observed, what it inferred, and what remains unknown. That distinction will determine whether SiteBlitz becomes a trustworthy intelligence product or just another database with attractive scores.
