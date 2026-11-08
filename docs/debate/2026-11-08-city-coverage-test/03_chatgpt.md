# SiteBlitz Lead Generator — Round 3 of 10

## 1. Batch 1 results — Agree: arithmetic is consistent

Cities tested

# 4/95

Unique businesses

# 1,743

Duplicates removed

# 105

The four rows total 1,848 returned records, 1,743 unique businesses, and 105 merged duplicates. All four completed successfully, and no `Found` count exceeds the theoretical 600-result maximum across two sources.

This validates the reported arithmetic, not yet the authenticity of the businesses or correctness of the searched geographic areas.

## 2. Wrong-area or suspicious-count assessment — Need data

No count conclusively demonstrates a wrong geographic area. However, I see three things worth checking.

| City      | Observation                                          | Assessment                                                   |
| --------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| Mumbai    | 2,397 available; 350 unique returned; 69% have email | High email coverage deserves verification                    |
| Delhi     | 3,276 available; 474 unique                          | Plausible for a large region, but geographic scope unknown   |
| Bengaluru | 590 found from a theoretical 600 maximum             | Both sources may be near their caps; need source breakdown   |
| Hyderabad | 82% phone, 60% email, 69% website                    | Strong completeness relative to Bengaluru; verify source mix |

My main concern is field quality rather than record count. An email-presence rate of 69% for Mumbai dentists and 60% for Hyderabad dentists is unusually strong for what I would conservatively expect from open geographic business data. That is an audit hypothesis, not proof of error.

I would inspect whether these are genuine business emails, shared aggregator contacts, duplicate contact values, or incorrectly parsed fields.

For geographically confirming the results, please retain four items per city: resolved Nominatim display name, bounding-box coordinates and dimensions, source-specific counts, and a small randomized sample of returned addresses.

Proposed test: Audit 20 randomly selected records per city (80 total), separating contact-field presence from verified contact accuracy. This is a lightweight QA recommendation, not a blocker for Batch 3.

Cost: Approximately 2–4 hours of review, assuming the records are readily accessible. Benefit: confidence that the eventual lead list is commercially useful.

## 3. Batch 3 — Agree: use a fixed 2026 population baseline

The country order uses the UN World Population Prospects 2024 revision, projected for 2026, excluding India, Bangladesh, and Afghanistan. This gives a stable ranking for Rounds 3–7.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.populationpyramid.net\&sz=32)

PopulationPyramid.net+1



City selection uses city-proper or comparable municipal populations rather than metropolitan populations wherever possible. Sources include the 2020 Chinese census, 2025 US Census estimates, Indonesia's city census data, Pakistan's 2023 census, and Brazil's 2022 census.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer+4



Batch 3 · 30 cities · 10 countries · ISO 3166-1 alpha-2

```

{
  "batch": 3,
  "cities": [
    {"city":"Shanghai","country_code":"CN","admin":"Shanghai"},
    {"city":"Beijing","country_code":"CN","admin":"Beijing"},
    {"city":"Shenzhen","country_code":"CN","admin":"Guangdong"},

    {"city":"New York City","country_code":"US","admin":"New York"},
    {"city":"Los Angeles","country_code":"US","admin":"California"},
    {"city":"Chicago","country_code":"US","admin":"Illinois"},

    {"city":"Jakarta","country_code":"ID","admin":"Jakarta"},
    {"city":"Surabaya","country_code":"ID","admin":"East Java"},
    {"city":"Bekasi","country_code":"ID","admin":"West Java"},

    {"city":"Karachi","country_code":"PK","admin":"Sindh"},
    {"city":"Lahore","country_code":"PK","admin":"Punjab"},
    {"city":"Faisalabad","country_code":"PK","admin":"Punjab"},

    {"city":"Lagos","country_code":"NG","admin":"Lagos"},
    {"city":"Kano","country_code":"NG","admin":"Kano"},
    {"city":"Ibadan","country_code":"NG","admin":"Oyo"},

    {"city":"São Paulo","country_code":"BR","admin":"São Paulo"},
    {"city":"Rio de Janeiro","country_code":"BR","admin":"Rio de Janeiro"},
    {"city":"Brasília","country_code":"BR","admin":"Distrito Federal"},

    {"city":"Moscow","country_code":"RU","admin":"Moscow"},
    {"city":"Saint Petersburg","country_code":"RU","admin":"Saint Petersburg"},
    {"city":"Novosibirsk","country_code":"RU","admin":"Novosibirsk Oblast"},

    {"city":"Addis Ababa","country_code":"ET","admin":"Addis Ababa"},
    {"city":"Mekelle","country_code":"ET","admin":"Tigray"},
    {"city":"Dire Dawa","country_code":"ET","admin":"Dire Dawa"},

    {"city":"Mexico City","country_code":"MX","admin":"Mexico City"},
    {"city":"Tijuana","country_code":"MX","admin":"Baja California"},
    {"city":"Ecatepec de Morelos","country_code":"MX","admin":"State of Mexico"},

    {"city":"Tokyo","country_code":"JP","admin":"Tokyo"},
    {"city":"Yokohama","country_code":"JP","admin":"Kanagawa"},
    {"city":"Osaka","country_code":"JP","admin":"Osaka"}
  ]
}

```

### Geographic qualifications

- Japan: Tokyo is included as the practical urban core comprising 23 special wards, not a single legally incorporated city. Nominatim could resolve it to the much larger Tokyo Metropolis; flag this rather than treating the result as Tokyo's urban core.&#x20;

  [image](https://www.google.com/s2/favicons?domain=https://www.english.metro.tokyo.lg.jp\&sz=32)

  都庁総合英語サイト

- Nigeria: Lagos, Kano, and Ibadan follow a city-based ranking. The newer UN urban-area methodology places Onitsha higher, but that measures a different geographic unit.&#x20;

  [image](https://www.google.com/s2/favicons?domain=https://datacommons.org\&sz=32)

  Data Commons+1

- Ethiopia: Addis Ababa, Mekelle, and Dire Dawa follow available 2025 city estimates. Confidence in the exact ranking is medium because population estimates and administrative definitions differ.&#x20;

  [image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

  Wikipedia

- Mexico: Ecatepec de Morelos is selected using city/locality population, not the municipality-wide ranking.&#x20;

  [image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

  Wikipedia



These 30 entries are proposed inputs, not verified geocoding results.

## 4. Fixed ranked list — all 50 countries for Rounds 3–7

The following country order is frozen to the 2026 UN-based population ranking, after removing India, Bangladesh, and Afghanistan.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.populationpyramid.net\&sz=32)

PopulationPyramid.net



Round 3 — Ranks 1–10

Batch supplied

1\. China `CN` · 2. United States `US` · 3. Indonesia `ID` · 4. Pakistan `PK` · 5. Nigeria `NG` · 6. Brazil `BR` · 7. Russia `RU` · 8. Ethiopia `ET` · 9. Mexico `MX` · 10. Japan `JP`

Round 4 — Ranks 11–20

11\. Egypt `EG` · 12. Philippines `PH` · 13. DR Congo `CD` · 14. Vietnam `VN` · 15. Iran `IR` · 16. Türkiye `TR` · 17. Germany `DE` · 18. Tanzania `TZ` · 19. Thailand `TH` · 20. United Kingdom `GB`

Round 5 — Ranks 21–30

21\. France `FR` · 22. South Africa `ZA` · 23. Italy `IT` · 24. Kenya `KE` · 25. Myanmar `MM` · 26. Colombia `CO` · 27. Sudan `SD` · 28. Uganda `UG` · 29. South Korea `KR` · 30. Algeria `DZ`

Round 6 — Ranks 31–40

31\. Iraq `IQ` · 32. Spain `ES` · 33. Argentina `AR` · 34. Yemen `YE` · 35. Canada `CA` · 36. Angola `AO` · 37. Ukraine `UA` · 38. Morocco `MA` · 39. Poland `PL` · 40. Uzbekistan `UZ`

Round 7 — Ranks 41–50

41\. Mozambique `MZ` · 42. Malaysia `MY` · 43. Ghana `GH` · 44. Saudi Arabia `SA` · 45. Peru `PE` · 46. Madagascar `MG` · 47. Côte d'Ivoire `CI` · 48. Cameroon `CM` · 49. Nepal `NP` · 50. Niger `NE`

## 5. Additional proposal — use the first results to assess commercial opportunity

Agree with preserving `Social-no-website %` as a separate field, because it directly identifies the founder's target segment.

Across the first four cities, the rounded percentages imply approximately 174 unique businesses with social profiles but no listed website.

That is a promising candidate pool, but not yet 174 qualified leads. A business might have an unlisted website, an outdated social profile, or unreliable contact data.

My proposal: After the discovery test, sample 50 such businesses and manually check whether they have an active social presence, genuinely lack an official website, and are relevant prospects. This would give the founder an early commercial-quality measure without changing the present coverage-testing workflow.

## Points still open

1. Batch 1: Complete all 95 city tests and inspect geographic-resolution failures.
2. Batch 2: Obtain results for the additional 50 Indian cities.
3. Batch 3: Confirm that the 30 international cities resolve to the intended geographic areas.
4. Contact quality: Investigate Mumbai's and Hyderabad's unusually high email-field coverage.
5. Precision audit: Test the 120-record category-matching sample separately.
6. Commercial validation: Audit a small sample of social-only, no-website businesses.
7. Production geocoding: Founder decision on a self-hosted or licensed solution.
8. Round 8: Retest spelling failures and incorrect administrative boundaries.
9. Rounds 9–10: Retain fresh validation batches alongside final coverage analysis.

Round 3 delivered: 30 international city inputs, plus a fixed 50-country sequence for Rounds 3–7.

Total cities supplied so far: 175 across three batches.
