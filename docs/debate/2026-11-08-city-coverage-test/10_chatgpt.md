# SiteBlitz Lead Generator — Final Review (Round 10/10)

Overall verdict: SiteBlitz has passed a substantial discovery-engine validation, but it has not yet passed a lead-quality or commercial-readiness validation.

Population-ranked cities tested

# 357

Countries

# 52

Records found

# 46,734

The strongest achievement is not the number of leads. It is that the test exposed and led to fixes for real product defects in search visibility, country attribution, geocoding, Unicode handling and geographic transparency.

The 20/20 resolver validation is encouraging. However, these are 20 selected test cases, not proof of perfect resolution across every city in the world.

## 1. Review of all six implemented changes

| Change                                   | Verdict                          | What is still needed before founder reliance                                                                                                                     |
| ---------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Job sightings and repeat searches     | Agree — ready for controlled use | Verify consistent results across API, list, map, export and website checks after retries and cross-city deduplication.                                           |
| 2. Country filtering                     | Agree — strong improvement       | Keep a regression suite for border cities, disputed/mismatched country codes and records whose source address country is wrong.                                  |
| 3. Geocoder and bounding-box corrections | Agree — conditionally ready      | Preserve exact-name checks and explicit trim labels; test historic aliases, large/irregular cities and incorrect source geometries beyond the 20 selected cases. |
| 4. All 249 countries selectable          | Agree — UI improvement           | Ensure selectable does not imply available business data; test country-code handling throughout the API and report unsupported/empty coverage honestly.          |
| 5. UTF-8 logging                         | Agree — fix verified             | Test Unicode end-to-end in production-like Windows execution, database storage, JSON, CSV exports and background worker logs.                                    |
| 6. Searched area and trim displayed      | Agree — necessary transparency   | Ensure every result view and export preserves actual searched area, trim status and partial-coverage meaning.                                                    |

Decision: I would not reopen these six implementations as major development tasks. Add their remaining checks to a small release-acceptance suite.

The 221 passing tests support engineering confidence, but I have not inspected the committed code or independently executed the suite.

## 2. What the 10-round test does not prove

Agree with all five limitations you identified. I would add six more.

| Unproven item            | Why it matters                                                                                                    |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| Category precision       | A result matched as a dentist may be a supplier, a hospital department or an unrelated business.                  |
| Real website absence     | Missing website fields do not establish that the business has no functioning official website.                    |
| Contact accuracy         | Phone/email presence and uniqueness do not establish that a contact works or belongs to the business.             |
| OSM coverage             | Public Overpass was unavailable, and local OSM extraction has not yet been evaluated.                             |
| Foursquare OS increment  | No measured evidence yet that it supplies new, valid businesses beyond Overture.                                  |
| Business freshness       | The test does not establish how many records are open, closed, relocated or outdated.                             |
| Global unique lead count | The 46,734 found records are not necessarily 46,734 different businesses across overlapping city searches.        |
| True market coverage     | The 190,872 available matches are source records, not an independent count of all dentists in those cities.       |
| Operational reliability  | Local DNS failures and source outages remain possible; city-level retries and recovery need validation.           |
| Commercial value         | No verified conversion rate, customer willingness to pay or acquisition cost has been demonstrated.               |
| Compliance readiness     | Data licences, personal-data handling and permitted outreach need assessment before production commercialization. |

### One important counting correction

You reported 316 cities with businesses and 41 without returned businesses. Since eight Bangladesh cities failed due to DNS resolution, I would report them separately rather than placing them under confirmed zero-data results.

Assuming those eight are included in the 41:

Returned records

# 316

Confirmed zero

# 33

Network failures

# 8

I would also reconcile why 49 of the intended 50 additional countries are represented. This is an accounting issue, not a reason to repeat the completed test.

## 3. Founder decisions — Ranked by value relative to cost

The ranking below considers expected commercial benefit, engineering effort, maintenance, legal exposure, and the risk of damaging lead-quality scores.

Planning estimates for a small engineering team, not verified implementation quotations

| Rank | Decision                               | Relative effort                                 | Verdict and reason                                                                                                                                                              |
| ---- | -------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | SOCIAL_ONLY / NEITHER reporting labels | Very low, \~0.5–1 day                           | Approve: Makes two commercially different prospect groups visible without changing the approved scoring rules.                                                                  |
| 2    | Foursquare OS Places — Phase 12        | Medium, \~2–5 days for a pilot                  | Approve a limited test: Could add meaningful records in undercovered markets and uses a relatively permissive Apache 2.0 licence, but incremental coverage is unproven.         |
| 3    | ODbL legal review                      | Moderate, external counsel                      | Approve before commercial OSM integration: Prevents costly mistakes in licensing and redistribution of merged business datasets.                                                |
| 4    | Geofabrik OSM — Phase 11               | Medium–high, \~3–7 days for a pilot plus upkeep | Approve a small pilot after the legal review: Replaces unreliable public Overpass access with repeatable local queries, provided additional coverage justifies operating costs. |
| 5    | Social-only Hot cap                    | Low coding cost; moderate validation            | Defer: Social-only status is not enough to prove purchase readiness, but an arbitrary cap could hide valuable prospects.                                                        |
| 6    | Admin-centre search mode               | Low–medium, \~1–2 days                          | Defer: Useful for exceptional geographic queries, but low priority and capable of searching the wrong market if misunderstood.                                                  |
| 7    | Dead domain = Website down immediately | Low coding cost; high accuracy risk             | Reject the immediate classification: DNS problems, timeouts and temporary outages do not establish that a website is permanently down.                                          |

Foursquare's published OS Places dataset uses Apache 2.0 with licence and NOTICE requirements, and its current access process uses a Places Portal/Iceberg catalog.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.foursquare.com\&sz=32)

docs.foursquare.com+1



Geofabrik publishes free, generally daily OSM extracts under ODbL. The OpenStreetMap Foundation distinguishes internal use from public redistribution and derivative-database obligations, so the legal decision should examine SiteBlitz's actual commercial output model.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.geofabrik.de\&sz=32)

geofabrik.de+2



Important sequencing recommendation: Run Phase 6 before permanently changing Hot classification rules or introducing an automatic `Website down` label.

For website availability, distinguish `DNS_FAILURE`, `TIMEOUT`, `HTTP_ERROR`, `DOMAIN_EXPIRED` and `SITE_CONFIRMED_DOWN`. A domain or website should not receive the final status based on a single request.

## 4. First three countries for Phase 6

My selection is designed to validate the website-intelligence engine, not simply maximize the number of businesses with missing website fields.

[mindtrip](https://images.openai.com/static-rsc-4/niHIZTPRYoWUQCU1Iul1NV-gg_sSVsi0LEsqf58scu2LlI6zW-xsJ2V3MDHKBQtFCHbVsrGbA8fWbFdSP0rLIH7dDphbhDohh_zM37JY1gZUhUfWQhsM4aaHuuBFnlNb94WjBKpanw-95UHl9K90VBe3V9UrH9ux-KuSmFZyhiQ?purpose=inline)

1\. India

Primary test market

## 60% social, no website

150 tested cities provide the widest sample across metros, secondary cities and smaller municipalities. Use India to validate scoring accuracy, category matching and business-level deduplication at scale.

[ShopUp Sees Increase in Revenue for FY Ending in June 2023, But Can They Reach Profitability? - Business Inspection BD](https://images.openai.com/static-rsc-4/KvyZJNg1tkswObW0V2Ssf1x4hpteRTq8owVTvwBtlEOjMCsBALTZPZJgqHMRuCJhwlQfStWqpIiwdhRSckwKy5TlQbOz2jG72z6wOzti7RYOfn0C9HxmNZ-1qcBVK0bWxsmykyqWEg9DRz79lEiskR6M5zqTUy5DTOzNWdEHRwE?purpose=inline)

2\. Bangladesh

## 80% social, no website

With 38 tested cities and strong reported phone/email availability, Bangladesh is the best candidate for testing whether social-only records genuinely lack official websites and represent actionable opportunities.

[Centre dentaire Lyon Frères Lumière Docali | Dentiste Lyon 8](https://images.openai.com/static-rsc-4/vRq1G0zJxJCmg83sxAFmATeAg_ZDEZ1tbk6hLGTIhYG6mUGQEFESTX2mnPEpTUSZSy-cvMWQmtUwB4q_FgoCpk0jV9MFab1TVXqYFvJ7-4AvDi1tqEpRkrhouJgkYNuOzcuEbFkl2Pnz4Cl7WLQKb91_4C5nT25mUSLWX2kL4aY?purpose=inline)

3\. France

## 39–40% website listed in Lyon / Marseille

Lyon and Marseille have low website coverage but very few social-only records. France is the contrasting market needed to verify that the engine recognizes the `NEITHER_LISTED` scenario without falsely assuming businesses are offline.

Why not Iraq first? Its 90% social-only median makes it attractive for commercial exploration, but France tests a different classification problem that neither India nor Bangladesh covers as clearly. I would put Iraq next in the commercial-opportunity pilot.

### Phase 6 — Suggested measurement

180 manually reviewed businesses

Proposed sample

## 60

India

## 60

Bangladesh

## 60

France

For each country, sample website-listed, social-only and neither-listed businesses. Independently check the official website, business identity, activity, category relevance and available contact details.

Recommended acceptance targets for this pilot:

| Metric                                           | Proposed target                     |
| ------------------------------------------------ | ----------------------------------- |
| Precision of confirmed no-site classification    | ≥90%                                |
| Category precision                               | ≥90%                                |
| Wrong-business website matches                   | ≤2%                                 |
| Incorrect permanent website-down classifications | ≤2%                                 |
| Qualified prospects per 1,000 discovered         | Measure baseline; no assumed target |

These targets are suggested release criteria, not proven performance levels.

## Final points still open

1. Data completion: Retry the eight Bangladesh DNS failures and reconcile the final counts, including the missing country from the intended 50-country international sequence.
2. Release verification: Complete the small remaining regression checks for the six committed fixes.
3. Phase 6: Validate website absence, active social profiles, category precision, business freshness and contact accuracy using labelled business records.
4. Lead scoring: Obtain founder approval for `SOCIAL_ONLY` / `NEITHER_LISTED` reporting; validate Hot classifications before changing the approved score rules.
5. Source expansion: Measure Foursquare OS incremental unique-business coverage before adopting it.
6. OSM production: Obtain budget approval and complete the ODbL legal review before production Geofabrik integration.
7. Website status: Define evidence and retry rules for dead domains, temporary outages and genuinely unavailable websites.
8. Operational quality: Test retry recovery, export correctness, Unicode processing and production-like concurrency.
9. Commercial validation: Measure qualified leads, outreach eligibility, customer responses, conversion and cost per acquired customer before predicting revenue.

## Final decision

Discovery engine: Validated for controlled use with Overture and the tested search configurations.

Geographic accuracy: Strong evidence, including 20/20 targeted resolver cases, but not universally proven.

Lead intelligence: Promising, still awaiting Phase 6 validation.

Global multi-source completeness: Not yet established.

Commercial readiness: Conditional on lead-quality validation and compliance review.

My recommendation is to freeze the tested discovery core, finish Phase 6, and then fund source expansion based on measured additional qualified leads. That is the clearest route from a successful engineering test to a commercially reliable SiteBlitz product.
