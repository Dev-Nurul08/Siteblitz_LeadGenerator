# SiteBlitz Lead Generator — Round 7 of 10

## 1. Batch 4/5 results — Agree: a useful new lead segment has emerged

The French results reveal a distinction that SiteBlitz should preserve in its future lead-quality scoring.

| City      | Website listed | Social, no website | Neither listed |
| --------- | -------------- | ------------------ | -------------- |
| Paris     | 91%            | 3%                 | 6%             |
| Marseille | 39%            | 7%                 | 54%            |
| Lyon      | 40%            | 4%                 | 56%            |

The last column is calculated from the supplied percentages, assuming all metrics use the same business denominator.

Agree: Businesses without either a listed website or a social profile deserve their own segment, rather than automatically receiving the lowest website-opportunity score.

I recommend three separate prospect categories: `SOCIAL_ONLY`, `NEITHER_LISTED`, and `WEBSITE_LISTED`. The second category should be labelled no online presence found in source data, not confirmed offline.

Need data: Manually verify a sample before assuming the second category is commercially less attractive. Some businesses without social profiles may still be interested in a website.

## 2. Round 6 fixes — Agree; no additional discovery changes required now

The repeat-search fix is adequately tested and can remain closed. The cross-border filter has also passed a meaningful audit of 7,834 Overture records across six boxes, with zero missing address-country values.

That finding supports the current Overture implementation; it does not establish completeness for every country or for future OSM extracts.

I also agree with retaining strict geographic name matching and rejecting province-only matches. The Tokyo/Hachioji issue demonstrates why this safeguard matters.

One caution: The results for Kenya outside Nairobi, Iran and DR Congo should remain labelled as limited Overture source coverage, not limited actual business populations.

## 3. Batch 7 — Countries ranked 41–50

30 cities · 10 countries · No previous-batch repeats

I used census-based city or municipality rankings, with a few important definition choices. Malaysia follows its 2020 local-authority population ranking; Peru includes Callao as a separate city, rather than treating it solely as part of metropolitan Lima. Cameroon follows its 2005 city-proper ranking, while Niger follows its 2012 census rather than the newer urban-agglomeration estimates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.dosm.gov.my\&sz=32)

Department of Statistics Malaysia+3



Other selections are supported by Mozambique's 2017 census figures, Ghana's 2021 census analysis, Saudi Arabia's 2022 census, Madagascar's 2018 census, Côte d'Ivoire's 2021 census and Nepal's 2021 census.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wiki.jamain.dev\&sz=32)

Kiwix Server+5



```

{
  "batch": 7,
  "cities": [
    {"city":"Maputo","country_code":"MZ","admin":"Maputo City"},
    {"city":"Matola","country_code":"MZ","admin":"Maputo Province"},
    {"city":"Nampula","country_code":"MZ","admin":"Nampula Province"},

    {"city":"Kuala Lumpur","country_code":"MY","admin":"Kuala Lumpur"},
    {"city":"Kajang","country_code":"MY","admin":"Selangor"},
    {"city":"Seberang Perai","country_code":"MY","admin":"Penang"},

    {"city":"Accra","country_code":"GH","admin":"Greater Accra Region"},
    {"city":"Kumasi","country_code":"GH","admin":"Ashanti Region"},
    {"city":"Tamale","country_code":"GH","admin":"Northern Region"},

    {"city":"Riyadh","country_code":"SA","admin":"Riyadh Region"},
    {"city":"Jeddah","country_code":"SA","admin":"Makkah Region"},
    {"city":"Mecca","country_code":"SA","admin":"Makkah Region"},

    {"city":"Lima","country_code":"PE","admin":"Lima Province"},
    {"city":"Callao","country_code":"PE","admin":"Callao"},
    {"city":"Arequipa","country_code":"PE","admin":"Arequipa"},

    {"city":"Antananarivo","country_code":"MG","admin":"Analamanga"},
    {"city":"Toamasina","country_code":"MG","admin":"Atsinanana"},
    {"city":"Antsirabe","country_code":"MG","admin":"Vakinankaratra"},

    {"city":"Abidjan","country_code":"CI","admin":"Abidjan"},
    {"city":"Bouaké","country_code":"CI","admin":"Gbêkê"},
    {"city":"Korhogo","country_code":"CI","admin":"Poro"},

    {"city":"Douala","country_code":"CM","admin":"Littoral"},
    {"city":"Yaoundé","country_code":"CM","admin":"Centre"},
    {"city":"Bamenda","country_code":"CM","admin":"Northwest Region"},

    {"city":"Kathmandu","country_code":"NP","admin":"Bagmati Province"},
    {"city":"Pokhara","country_code":"NP","admin":"Gandaki Province"},
    {"city":"Bharatpur","country_code":"NP","admin":"Bagmati Province"},

    {"city":"Niamey","country_code":"NE","admin":"Niamey"},
    {"city":"Maradi","country_code":"NE","admin":"Maradi Region"},
    {"city":"Zinder","country_code":"NE","admin":"Zinder Region"}
  ]
}

```

### 4. Geographic and administrative warnings

These are risks to check in the job's `resolved_place` metadata, not confirmed Nominatim failures.

| Cities                  | Issue to watch                                                                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| Maputo                  | Maputo City is administratively separate from Maputo Province                                           |
| Nampula                 | City and province share the same name                                                                   |
| Kuala Lumpur            | City and Federal Territory share the name                                                               |
| Kajang                  | The municipal council covers a much wider area than Kajang's central settlement                         |
| Seberang Perai          | High risk — an extensive local-authority area, not one compact urban settlement                         |
| Riyadh, Mecca           | City and province/region share names                                                                    |
| Lima, Callao, Arequipa  | Names overlap with provincial or regional units; Lima and Callao are also adjoining urban jurisdictions |
| Antananarivo, Toamasina | Names also occur in historical province classifications                                                 |
| Abidjan                 | Distinguish the urban city from the larger Autonomous District                                          |
| Bouaké, Korhogo         | City and department names overlap                                                                       |
| Kathmandu               | City and district names overlap                                                                         |
| Niamey, Maradi, Zinder  | City and region-level names overlap                                                                     |

Most important case: Seberang Perai. Malaysia's official statistics rank the Seberang Perai local authority among the country's largest, but the municipal government describes a 738 km² jurisdiction covering multiple towns, including Butterworth and Bukit Mertajam. OSM-derived data identifies Seberang Perai as an administrative boundary.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.dosm.gov.my\&sz=32)

Department of Statistics Malaysia+2



If the strict settlement-name resolver rejects it, do not silently replace it with Butterworth. Record the failed query, and use Butterworth as a separately labelled city test in Round 8 if needed.

### Cross-border warning

Maradi, Niger: The nearest identified Nigerian town, Jibia, is approximately 47 km away—outside a strict 40 km city-to-city threshold. However, Maradi lies in a border-trade region, so its search box still deserves a country-filter check.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://database.earth\&sz=32)

database.earth+1



I did not verify any Batch 7 city pair across an international border within 40 km. That conclusion is provisional, not the result of a complete GIS border-distance audit.

## 5. Points still open

1. Complete and reconcile the remaining Batch 1–6 results, including corrected geocoding cases.
2. Test all 30 Batch 7 names and flag administrative-only resolutions, especially Seberang Perai.
3. Recheck cross-border contamination for Maradi and other flagged search boxes.
4. Keep the `SOCIAL_ONLY` and `NEITHER_LISTED` prospect segments separate for later commercial validation.
5. Complete the 120-record category precision audit and business-level website verification pilot.
6. Make the founder's production-budget decision for Geofabrik/local OSM processing.
7. Review source-licensing obligations before any public redistribution of merged datasets.
8. Prepare Round 8's alternate-spelling and geographic-failure retests, plus the next 50 Indian cities.
9. Preserve fresh test batches in Rounds 9–10 alongside the final coverage and production reviews.

Round 7 delivered: 30 additional city inputs. Cumulative planned inputs: 295 cities across seven batches.
