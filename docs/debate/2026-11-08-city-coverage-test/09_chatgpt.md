# SiteBlitz Lead Generator — Round 9 of 10

## 1. Market findings — Agree, with one qualification

The results across 246 tested cities show two distinct problems that SiteBlitz should solve separately:

Commercial opportunity: Iraq, Bangladesh, Myanmar, Sudan and several secondary Indian cities have high proportions of businesses with social profiles but no listed websites. These are promising markets for website-development prospecting.

Data-source weakness: China, DR Congo, Iran outside Tehran, Afghanistan outside Kabul, and several smaller African cities have low Overture dentist coverage. These are not necessarily weak commercial markets; the dataset is insufficient to judge them.

I agree with keeping country-level discovery coverage separate from commercially qualified lead counts.

One important finding from the latest research: Foursquare Open Source Places is a potentially useful additional dataset, and Overture does not include all of it. Overture's October 2026 documentation reports about 3.76 million Foursquare-sourced records, while Foursquare's September 2026 release reports approximately 109.4 million POIs worldwide. These numbers are not directly comparable proof of incremental coverage, because Overture combines and deduplicates provider records.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.overturemaps.org\&sz=32)

Overture Documentation+1



The next step is an actual incremental-coverage comparison rather than assuming every Foursquare record will be new.

## 2. Resolver failures — Agree: validate against actual OSM names

I checked the two Afghanistan failures and Butterworth against OSM-derived place records.

| Earlier failed/requested name | Batch 9 spelling | Expected OSM settlement                         |
| ----------------------------- | ---------------- | ----------------------------------------------- |
| Pul-e-Khumri                  | Puli Khumri      | OSM city node `312781022`, Baghlan, Afghanistan |
| Lashkargah                    | Lashkar Gah      | OSM city node `312368833`, Helmand, Afghanistan |
| Butterworth                   | Butterworth      | OSM city node `205623582`, Penang, Malaysia     |

The two Afghanistan city nodes explicitly carry the English names `Puli Khumri` and `Lashkar Gah`. Butterworth is also a documented OSM city node, distinct from the broader Seberang Perai municipality.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://af.geoview.info\&sz=32)

Map & Info+2



Confidence: High that these are genuine mapped city objects; medium that the current public Nominatim instance will return them through the exact structured query. That remains the purpose of Batch 9.

## Part A — Batch 9: 20-city resolver validation

20 test inputs · 8 countries · Expected place specified

This batch deliberately includes repeated city names with different state qualifiers, older city names, province/city collisions, and international-border cases. Unlike the population batches, previously tested places are intentionally reused to validate the resolver.

```

{
  "batch": 9,
  "cities": [
    {
      "city": "Puli Khumri",
      "country_code": "AF",
      "admin": "Baghlan",
      "expect": "Puli Khumri city, Baghlan Province, Afghanistan; OSM node 312781022, not Puli Khumri District"
    },
    {
      "city": "Lashkar Gah",
      "country_code": "AF",
      "admin": "Helmand",
      "expect": "Lashkar Gah city, Helmand Province, Afghanistan; OSM node 312368833, not Lashkargah District"
    },
    {
      "city": "Butterworth",
      "country_code": "MY",
      "admin": "Penang",
      "expect": "Butterworth city, Penang, Malaysia; OSM node 205623582, not all Seberang Perai"
    },
    {
      "city": "Aurangabad",
      "country_code": "IN",
      "admin": "Maharashtra",
      "expect": "Chhatrapati Sambhajinagar (formerly Aurangabad), Maharashtra, India; not Aurangabad, Bihar"
    },
    {
      "city": "Allahabad",
      "country_code": "IN",
      "admin": "Uttar Pradesh",
      "expect": "Prayagraj (formerly Allahabad) city, Uttar Pradesh, India"
    },
    {
      "city": "Ahmednagar",
      "country_code": "IN",
      "admin": "Maharashtra",
      "expect": "Ahilyanagar (formerly Ahmednagar) city, Maharashtra, India"
    },
    {
      "city": "Gurgaon",
      "country_code": "IN",
      "admin": "Haryana",
      "expect": "Gurugram (formerly Gurgaon) city, Haryana, India"
    },
    {
      "city": "Bilaspur",
      "country_code": "IN",
      "admin": "Chhattisgarh",
      "expect": "Bilaspur city, Chhattisgarh, India; not Bilaspur, Himachal Pradesh"
    },
    {
      "city": "Bilaspur",
      "country_code": "IN",
      "admin": "Himachal Pradesh",
      "expect": "Bilaspur town, Himachal Pradesh, India; not Bilaspur, Chhattisgarh"
    },
    {
      "city": "Springfield",
      "country_code": "US",
      "admin": "Illinois",
      "expect": "Springfield city, Illinois, United States; capital of Illinois"
    },
    {
      "city": "Springfield",
      "country_code": "US",
      "admin": "Massachusetts",
      "expect": "Springfield city, Massachusetts, United States; not Springfield, Illinois"
    },
    {
      "city": "Portland",
      "country_code": "US",
      "admin": "Maine",
      "expect": "Portland city, Maine, United States; not Portland, Oregon"
    },
    {
      "city": "Portland",
      "country_code": "US",
      "admin": "Oregon",
      "expect": "Portland city, Oregon, United States; not Portland, Maine"
    },
    {
      "city": "Riyadh",
      "country_code": "SA",
      "admin": "Riyadh Region",
      "expect": "Riyadh city, Saudi Arabia; not the full Riyadh Region"
    },
    {
      "city": "Nairobi",
      "country_code": "KE",
      "admin": "Nairobi County",
      "expect": "Nairobi city, Kenya; not an unrelated county or administrative feature"
    },
    {
      "city": "Tijuana",
      "country_code": "MX",
      "admin": "Baja California",
      "expect": "Tijuana city, Baja California, Mexico; exclude San Diego businesses across the international border"
    },
    {
      "city": "San Diego",
      "country_code": "US",
      "admin": "California",
      "expect": "San Diego city, California, United States; exclude Mexican businesses across the international border"
    },
    {
      "city": "Goma",
      "country_code": "CD",
      "admin": "Nord-Kivu",
      "expect": "Goma city, North Kivu, DR Congo; not Gisenyi in Rwanda across the border"
    },
    {
      "city": "Zaranj",
      "country_code": "AF",
      "admin": "Nimruz",
      "expect": "Zaranj city, Nimruz Province, Afghanistan; exclude Iranian places across the border"
    },
    {
      "city": "Abadan",
      "country_code": "IR",
      "admin": "Khuzestan",
      "expect": "Abadan city, Khuzestan Province, Iran; not Iraqi places across the Shatt al-Arab border"
    }
  ]
}

```

### How to score this batch

Suggested resolver acceptance tests

| Correct settlement and jurisdiction   | 20/20 target                         |
| ------------------------------------- | ------------------------------------ |
| Incorrect city accepted silently      | 0                                    |
| Wrong-country records after filtering | 0 in audited sample                  |
| Unresolved input                      | Report explicitly; do not substitute |

An exact-name rejection is preferable to returning the wrong city, but it should not score as a successful resolution.

Special test: The old-name queries (`Aurangabad`, `Allahabad`, `Ahmednagar`, `Gurgaon`) may fail if the resolver's name aliases have not been mapped to the corresponding modern settlements. Those failures are useful evidence for a controlled alias dictionary.

I did not run the 20 Nominatim requests. The `expect` values specify the intended geographic targets; they do not assert that live matching has succeeded.

## Part B — Lawful supplementary sources for low-coverage countries

## 3. Source recommendation — Agree: prioritize reusable open datasets

I recommend two sources for the next coverage experiment:

1. Foursquare Open Source Places — potentially adds points not present in Overture and provides names, locations, categories, phone, email, website and social fields.
2. Geofabrik OpenStreetMap country extracts — captures OSM businesses without depending on public Overpass servers.

Both provide downloadable datasets under published open licences. Foursquare OS Places uses Apache 2.0; Geofabrik's OSM-derived extracts use ODbL 1.0.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://opensource.foursquare.com\&sz=32)

Foursquare Open Source+2



### Country-by-country choices

| Country          | Recommended source                                                                                                 | Data fee | Important licence condition                                                     |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------- |
| Afghanistan `AF` | [Geofabrik Afghanistan](https://download.geofabrik.de/asia/afghanistan.html?utm_source=chatgpt.com)                | Free     | ODbL: attribution and derivative-database share-alike obligations on public use |
| Iran `IR`        | [Foursquare OS Places](https://docs.foursquare.com/data-products/docs/access-fsq-os-places?utm_source=chatgpt.com) | Free     | Apache 2.0: preserve licence, notices and applicable change notices             |
| China `CN`       | Foursquare OS Places                                                                                               | Free     | Same Apache 2.0 requirements; country coverage unverified                       |
| DR Congo `CD`    | [Geofabrik DR Congo](https://download.geofabrik.de/africa/congo-democratic-republic.html?utm_source=chatgpt.com)   | Free     | ODbL attribution and applicable share-alike obligations                         |
| Kenya `KE`       | [Geofabrik Kenya](https://download.geofabrik.de/africa/kenya.html?utm_source=chatgpt.com)                          | Free     | ODbL attribution and applicable share-alike obligations                         |
| Tanzania `TZ`    | [Geofabrik Tanzania](https://download.geofabrik.de/africa/tanzania.html?utm_source=chatgpt.com)                    | Free     | ODbL attribution and applicable share-alike obligations                         |
| Mozambique `MZ`  | [Geofabrik Mozambique](https://download.geofabrik.de/africa/mozambique.html?utm_source=chatgpt.com)                | Free     | ODbL attribution and applicable share-alike obligations                         |

Licences and download availability verified against provider documentation on November 8, 2026. Data fees exclude hosting, bandwidth and processing.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://download.geofabrik.de\&sz=32)

Geofabrik Download Server+5

Why these choices? Afghanistan and the four African countries have directly downloadable country extracts suitable for local processing. Iran and China are candidates for testing the independent Foursquare OS dataset against Overture.

These are legally reusable source candidates, not demonstrated coverage improvements. Each needs a record-level comparison.

### Actual download sizes and operating cost

Geofabrik country-extract sizes

0 MB200 MB400 MB600 MB800 MBAfghanistanDR CongoKenyaTanzaniaMozambique

Approximate compressed PBF download size, MB

Approximate published sizes from Geofabrik's country download pages.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://download.geofabrik.de\&sz=32)

Geofabrik Download Server+4

For a small pilot, the following is a reasonable infrastructure budget based on published DigitalOcean Basic Droplet prices. Actual required capacity must be measured.

| Infrastructure      | Monthly price |
| ------------------- | ------------- |
| 4 GiB RAM / 2 vCPU  | $24           |
| 8 GiB RAM / 4 vCPU  | $48           |
| 16 GiB RAM / 8 vCPU | $96           |

Source: [DigitalOcean official pricing](https://www.digitalocean.com/pricing/droplets?utm_source=chatgpt.com). Prices effective under the provider's 2026 schedule; confidence high. Memory and storage suitability remain untested.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.digitalocean.com\&sz=32)

DigitalOcean



For the first country tests, temporary compute billed by usage may be cheaper than running a dedicated server continuously.

### Important Foursquare licensing distinction

Foursquare's open-source dataset is published under Apache 2.0, which permits copying, modification, storage and commercial reuse subject to licence conditions. The provider requires preservation of its NOTICE and relevant attribution.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://opensource.foursquare.com\&sz=32)

Foursquare Open Source



However, Foursquare's separate subscription-based Data Authorization Agreement, dated June 23, 2022, prohibits lead generation from the subscription Places Data unless expressly authorized.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://foursquare.com\&sz=32)

Foursquare



Therefore, SiteBlitz should obtain the explicitly Apache-licensed FSQ OS Places dataset, not assume that a commercial Foursquare Places API subscription grants equivalent rights. The applicability of any additional access terms should be confirmed before production prospecting.

Foursquare currently offers free account access through its Places Portal and gated access through Hugging Face. The Hugging Face route also asks for consent concerning the organization name and logo.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.foursquare.com\&sz=32)

docs.foursquare.com+1



Confidence: High on the published open-source licence; medium on the precise interaction of access-platform terms until reviewed.

### Additional official sources worth knowing about

Two national health registries are particularly relevant:

- [Kenya Master Health Facility Registry](https://kmhfr.health.go.ke/public/about?utm_source=chatgpt.com) — includes a developer API, facility identities, locations and services.
- [Tanzania Health Facility Registry](https://hfrportal.moh.go.tz/web/?utm_source=chatgpt.com) — publishes registered facility information, including clinics.

These could be valuable for verifying genuine healthcare businesses. However, I could not confirm an explicit licence authorizing SiteBlitz to bulk-store and commercially reuse their records. Do not bulk-import them until the operator grants or confirms that permission.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://kmhfr.health.go.ke\&sz=32)

KMHFR+1



## 4. Recommended source experiment — Agree: test incremental coverage before integration

Run the alternative sources in the same city search areas already used for Overture.

Suggested pilot design

Use seven countries, with the existing three tested cities per country where possible. Keep Overture records as the reference dataset.

| Original source    | Overture                                                   |
| ------------------ | ---------------------------------------------------------- |
| Alternative source | Foursquare OS or local OSM                                 |
| Geography          | Same tested box and country filter                         |
| Matching           | Business identity + name, location, phone, website         |
| Quality audit      | 20 newly discovered businesses per country where available |
| Primary KPI        | Additional verified unique dentist businesses              |

Define incremental coverage as:

\\[ \text{Incremental coverage}=\frac{\text{Verified new businesses}}{\text{Verified Overture baseline}}\times100 \\]

For locations with zero baseline businesses, report the absolute number of new verified businesses rather than a percentage.

My proposed acceptance threshold: Prioritize production ingestion where a source supplies at least 20% additional verified unique businesses or fills a previously near-empty city with at least 20 verified businesses. These are decision thresholds, not forecasts.

Beneficiary: The founder can compare actual additional leads against infrastructure and upkeep costs. Engineering can avoid building a large global extraction pipeline that delivers little incremental value.

## 5. Production constraints — Agree: data licence alone is not enough

Even if a dataset permits local storage, SiteBlitz must separately comply with applicable privacy, electronic-marketing and cross-border data rules.

Keep business identity and location data separate from any individual contact information. Preserve provenance, suppression preferences, and a process for correcting or removing inaccurate records.

The source licence does not itself authorize unsolicited marketing to every contact in that source.

## Points still open

1. Batch 9 resolver validation: Run all 20 inputs, score correct-settlement resolution, and record failures without substituting another locality.
2. Afghanistan aliases: Confirm `Puli Khumri` and `Lashkar Gah` against live Nominatim results.
3. Old names: Validate controlled historical-name aliases such as Allahabad/Prayagraj and Gurgaon/Gurugram.
4. Border filtering: Audit Tijuana, San Diego, Goma, Zaranj and Abadan after country filtering.
5. Source coverage: Test country extracts and Foursquare OS against Overture; report incremental verified unique businesses.
6. Licensing: Confirm Foursquare open-source access terms and obtain legal review for ODbL-derived data redistribution.
7. Website verification: Finish the approved business-level website checks and 120-record dentist precision audit.
8. Infrastructure decision: Founder approval remains necessary before launching a production country-ingestion pipeline.
9. Remaining geographic results: Reconcile the outstanding Batch 7 and Batch 8 tests and distinguish geocoder failures from source-data gaps.
10. Round 10: Final validation batch, consolidated country ranking, geographic QA, lead-quality analysis and production-readiness decision.

Round 9 delivered: 20 resolver-validation inputs, including the three specifically requested locations, and seven country-level lawful data-source recommendations.

Cumulative planned inputs: 386 across nine batches, including intentional resolver retests.
