# SiteBlitz Lead Generator — Round 4 of 10

## 1. Coverage results — Agree, with one important qualification

Cities tested

# 21

Unique businesses

# 5,202

Complete / Partial

# 9 / 12

Agree: SiteBlitz is demonstrating useful discovery capability. All 21 tested cities returned records, including those where the OpenStreetMap source failed.

Need data: A successful result is not necessarily complete coverage. Twelve cities returned partial results, so they should remain explicitly marked `PARTIAL` in the report.

One reporting issue also needs checking: the displayed `Unique` values sum to 5,660, not 5,202. The lower figure may reflect a different aggregation snapshot or additional global deduplication, but that cannot be established from the table. Please reconcile the summary with the rows.

## 2. Public Overpass overload — Agree with fail-fast; disagree with depending on public mirrors

The 66-second timeout is a practical improvement. Keeping Overture results when Overpass is unavailable protects the primary test from total failure.

However, using additional public mirrors as a scaling solution is not robust. OpenStreetMap's documentation explicitly describes public Overpass instances as limited, shared infrastructure intended for relatively small workloads.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wiki.openstreetmap.org\&sz=32)

OpenStreetMap Wiki



My proposal: Have all three workers share a single global Overpass request queue, with backoff when the server reports overload. Do not allow each worker to independently retry multiple public mirrors.

For the current test, retain three separate outcomes: `OVERTURE_COMPLETE`, `ALL_SOURCES_COMPLETE`, and `OSM_DEFERRED`.

| Measure                                            | Target                   |
| -------------------------------------------------- | ------------------------ |
| Overture results preserved during Overpass failure | 100%                     |
| Public Overpass requests                           | Globally rate-controlled |
| Retry attempts after overload                      | Bounded and logged       |
| Partial results incorrectly labelled complete      | 0                        |

Cost: Low-to-moderate engineering work; no additional data-provider subscription is required. The benefit is more reliable results and more considerate use of shared infrastructure. Validate effectiveness by measuring completion rates and rate-limit errors across subsequent batches.

## 3. Email audit — Agree that the original concern is substantially reduced

The audit provides useful evidence against a simple shared-email or aggregator-address problem.

Across the six audited cities, there are 1,363 records with an email, and only 10 within-city repetitions beyond the number of distinct emails.

However, distinct addresses do not by themselves prove that those addresses are active, belong to the listed businesses, or were collected from Facebook.

My proposal: Keep three different fields:

- `email_present`
- `email_unique_within_city`
- `email_verified`

Only mark an address verified after an appropriate verification process. The immediate goal is data integrity, not sending emails.

## 4. Claude's Gmail/Yahoo inference — Disagree because it is not conclusive

> A business whose only email is Gmail/Yahoo has no own domain → a strong extra "needs a website" signal.

The first implication is not logically valid.

A dentist can operate a legitimate business website and still use a Gmail address for all enquiries. Conversely, a business can register a custom email domain without operating a public website.

What the audit actually establishes is that many businesses use free email providers.

I recommend introducing a new signal:

`free_email_provider = true`

This can be useful for prioritization, but it must not be equated with `website_absent`.

A suitable scoring test would compare independently verified website absence among 50 free-email businesses and 50 custom-domain businesses, controlling for whether the original listing contains a website field.

Cost: Approximately 100 website-presence checks plus a small scoring-rule change. Success criterion: Demonstrate a meaningful improvement in verified website-absence precision over using the missing-website field alone.

## 5. Email-based deduplication — Partially disagree

Using email as a supporting match is sensible. Using it as an unconditional merge key is risky.

For example, two dental clinic branches may share one central email address but remain separate physical locations and separate business opportunities.

Proposal: Treat an exact email match as strong evidence, then evaluate business name, phone, address, and geographical proximity before merging. Keep organization-level identity separate from location-level identity.

Target: No verified distinct business locations should be merged incorrectly in a labelled sample.

Correction to Point 1: On recalculation, the 21 `Unique` values sum to exactly 5,202. The supplied summary is correct; there is no aggregation discrepancy. The earlier 5,660 figure was my arithmetic error.

## 6. Batch 4 — Agree: 30 cities across countries ranked 11–20

30 cities · 10 countries · Batch 4

For the city-proper selection, I cross-checked national or official statistical sources where available, including the Philippines' 2024 census, Tanzania's 2022 city-proper census, Thailand's municipal population records, and the UK government's city population list.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://psa.gov.ph\&sz=32)

Philippine Statistics Authority+4



In particular, Tanzania uses Dar es Salaam, Dodoma, Arusha because the UN's city-proper figures place Arusha ahead of Mwanza. Thailand uses Bangkok, Nonthaburi, Pak Kret rather than urban-agglomeration rankings. These distinctions are important for a consistent test.

```

{
  "batch": 4,
  "cities": [
    {"city":"Cairo","country_code":"EG","admin":"Cairo Governorate"},
    {"city":"Alexandria","country_code":"EG","admin":"Alexandria Governorate"},
    {"city":"Giza","country_code":"EG","admin":"Giza Governorate"},

    {"city":"Quezon City","country_code":"PH","admin":"Metro Manila"},
    {"city":"Manila","country_code":"PH","admin":"Metro Manila"},
    {"city":"Davao City","country_code":"PH","admin":"Davao Region"},

    {"city":"Kinshasa","country_code":"CD","admin":"Kinshasa"},
    {"city":"Lubumbashi","country_code":"CD","admin":"Haut-Katanga"},
    {"city":"Mbuji-Mayi","country_code":"CD","admin":"Kasaï-Oriental"},

    {"city":"Ho Chi Minh City","country_code":"VN","admin":"Ho Chi Minh City"},
    {"city":"Hanoi","country_code":"VN","admin":"Hanoi"},
    {"city":"Hai Phong","country_code":"VN","admin":"Hai Phong"},

    {"city":"Tehran","country_code":"IR","admin":"Tehran"},
    {"city":"Mashhad","country_code":"IR","admin":"Razavi Khorasan"},
    {"city":"Isfahan","country_code":"IR","admin":"Isfahan"},

    {"city":"Istanbul","country_code":"TR","admin":"Istanbul"},
    {"city":"Ankara","country_code":"TR","admin":"Ankara"},
    {"city":"Izmir","country_code":"TR","admin":"Izmir"},

    {"city":"Berlin","country_code":"DE","admin":"Berlin"},
    {"city":"Hamburg","country_code":"DE","admin":"Hamburg"},
    {"city":"Munich","country_code":"DE","admin":"Bavaria"},

    {"city":"Dar es Salaam","country_code":"TZ","admin":"Dar es Salaam Region"},
    {"city":"Dodoma","country_code":"TZ","admin":"Dodoma Region"},
    {"city":"Arusha","country_code":"TZ","admin":"Arusha Region"},

    {"city":"Bangkok","country_code":"TH","admin":"Bangkok"},
    {"city":"Nonthaburi","country_code":"TH","admin":"Nonthaburi"},
    {"city":"Pak Kret","country_code":"TH","admin":"Nonthaburi"},

    {"city":"London","country_code":"GB","admin":"England"},
    {"city":"Birmingham","country_code":"GB","admin":"England"},
    {"city":"Glasgow","country_code":"GB","admin":"Scotland"}
  ]
}

```

The country sequence is unchanged from Round 3. Names are intended as English Nominatim search inputs; their actual resolutions remain untested.

## 7. Geographic ambiguity — Need data from Nominatim

The following cities should receive special attention when examining the returned display name, place type and bounding box.

| City                 | Risk      | Recommended check                                                            |
| -------------------- | --------- | ---------------------------------------------------------------------------- |
| Ho Chi Minh City     | Very high | The 2025 merger expanded the centrally governed city to roughly 6,773 km²    |
| Hai Phong            | Very high | The 2025 merger incorporated Hai Duong province, producing roughly 3,195 km² |
| Hanoi                | High      | Administrative municipality extends well beyond the dense urban core         |
| Kinshasa             | High      | City-province includes extensive non-urban territory                         |
| Istanbul             | High      | Metropolitan municipality/province extends far beyond the central urban area |
| Ankara, Izmir        | High      | Province-level boundaries can include substantial rural territory            |
| Cairo, Giza          | High      | Governorate boundaries may differ sharply from city boundaries               |
| Manila               | Medium    | Must resolve to the City of Manila, not all Metro Manila                     |
| Dodoma               | High      | Must resolve to the city, not the much larger Dodoma Region                  |
| London               | High      | Distinguish Greater London from the tiny City of London                      |
| Nonthaburi, Pak Kret | Medium    | Must resolve to separate municipalities, not the whole Nonthaburi province   |

Vietnam is particularly important: its June 2025 administrative reform formally merged Ho Chi Minh City with Bình Dương and Bà Rịa–Vũng Tàu, and Hai Phong with Hai Duong. These are genuine changes in boundaries, not just possible geocoder mistakes.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://sav.gov.vn\&sz=32)

Kiểm toán nhà nước Việt Nam



Recommended rule: Accept a resolved city only when its place type and geographic extent match the intended municipality. A bounding box passing the 1.5° limit is not sufficient proof.

For oversized or ambiguous cities, retain the original query and mark `GEOGRAPHY_REVIEW_REQUIRED` rather than silently treating a province as a city.

Source: [Nominatim Search API documentation](https://nominatim.org/release-docs/develop/api/Search/?utm_source=chatgpt.com). Reviewed November 8, 2026. Confidence: High on documented parameters; medium on which returned boundaries will actually be selected.

## 8. Points still open

1. Complete Batch 1 and Batch 2 coverage tests, including their partial and failed geocoding cases.
2. Receive Batch 3 results for the first 10 international countries.
3. Validate Batch 4 geographic boundaries, especially Vietnam, Kinshasa, Turkish metropolitan cities and London.
4. Keep Overpass calls globally controlled across workers; decide whether to use regional extracts or self-hosted infrastructure for production.
5. Complete the separate 120-record dentist-category precision audit.
6. Check the accuracy of contact information, not only email uniqueness.
7. Test whether free-email-provider status genuinely improves the ability to identify businesses needing websites.
8. Implement email-assisted deduplication without merging separate clinic locations incorrectly.
9. Make the production geocoding cost and provider decision.
10. Continue Round 5 with the next 10 fixed countries: France, South Africa, Italy, Kenya, Myanmar, Colombia, Sudan, Uganda, South Korea and Algeria.

Round 4 delivered: 30 new city inputs. Cumulative total: 205 city inputs across four batches.
