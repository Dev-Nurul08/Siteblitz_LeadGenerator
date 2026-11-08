# SiteBlitz Lead Generator — Round 5 of 10

## 1. Coverage results — Agree: the international differences are significant

Cities tested

# 56

Cities with results

# 54

Unique saved

# 10,563

Agree: The results support an important product hypothesis: Indian secondary cities may provide stronger website-development prospecting opportunities than the three tested US cities.

The reported Indian medians show:

| Segment                                     | Website present | Social link, no website |
| ------------------------------------------- | --------------- | ----------------------- |
| Indian cities with ≥300 available dentists  | 66%             | 22%                     |
| Indian cities with fewer than 300 available | 37%             | 59%                     |
| Three US cities                             | 94–96%          | 2–3%                    |

This is valuable for deciding where to sell, not merely where to collect leads.

Need data: We still need audited business-level records to establish how many truly lack a website, have an active social presence, and are willing to buy website services.

I recommend retaining these metrics as the initial prioritization baseline, not yet converting them into predicted revenue.

## 2. Overpass connectivity — Agree with stopping public API requests

The decision to use Overture only while public Overpass is unavailable is appropriate.

Disagree with treating the cause as proven. Three processes sharing one IP may have contributed, but the observed connection failures alone cannot distinguish server-side blocking from network egress restrictions, routing problems, or service failures.

No further public-server testing is necessary to make the production decision.

Proposal: Replace public Overpass dependence with locally processed OSM extracts. I detail the costs and architecture after Batch 5.

## 3. Geocoding corrections — Agree with the fix; one safeguard is necessary

The five-result selection and fallback to an unqualified city search address the demonstrated cases of Beijing and Ho Chi Minh City resolving to unrelated features.

Partially disagree with treating a trimmed bounding box as equivalent to the original city boundary.

A center-based crop is a legitimate way to get useful results, but it represents only a defined search area, not necessarily the entire municipality.

Keep the following separate:

- `requested_city`
- `resolved_place`
- `original_boundary_km2`
- `searched_area_km2`
- `coverage_mode`: actual boundary, bounding box, or trimmed area

Acceptance test: Every trimmed search must be identifiable in the output; no geographically partial search should be described as exhaustive city coverage.

Cost: Small additional engineering and reporting work. Benefit: trustworthy coverage comparisons between cities.

## 4. China and DR Congo — Need data before declaring the markets empty

Shanghai's 13 records and Kinshasa's five records demonstrate very low discovery coverage in the tested open sources and areas, not an absence of dental businesses.

I agree with recording these as source-coverage gaps. The next step is to compare a sample of known local dental practices against the downloaded data.

For China, I would also separately evaluate whether non-English naming and local category tags are causing additional missed matches. That is a testable hypothesis.

Do not spend substantial engineering time improving China-specific discovery until an independent benchmark establishes the recoverable opportunity.

## 5. Cross-city deduplication — Agree; implementation should be preserved

The Pimpri-Chinchwad/Pune and Cuttack/Bhubaneswar results establish why cross-city deduplication matters when the database is shared.

The earlier suggestion that this was optional can now be closed: it is required for this implementation.

One additional data-quality issue: Indore's new row reports 300 found and 0% across every contact field, whereas the earlier Indore audit contained 177 email-bearing records among 448 businesses.

Because this run reportedly matched 300 previously saved records, the zero percentages may reflect the current job's insert/update accounting rather than the saved businesses' actual fields.

Need data: Check the denominator and query used for those percentages. Prefer reporting field completeness for returned unique businesses separately from newly inserted businesses.

## 6. Batch 5 — Agree: 30 cities in countries 21–30

10 countries · 3 cities each · ISO country codes · No repeats from earlier batches

The selection uses city-proper or municipal population figures, not metropolitan agglomerations. Important exceptions and boundary risks are explained below the JSON.

Uganda deserves particular attention: its 2024 census places Nansana and Kira municipalities above Gulu and Jinja in city/municipality population. They are included rather than automatically choosing the more familiar regional cities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer+1



```

{
  "batch": 5,
  "cities": [
    {"city":"Paris","country_code":"FR","admin":"Île-de-France"},
    {"city":"Marseille","country_code":"FR","admin":"Provence-Alpes-Côte d'Azur"},
    {"city":"Lyon","country_code":"FR","admin":"Auvergne-Rhône-Alpes"},

    {"city":"Johannesburg","country_code":"ZA","admin":"Gauteng"},
    {"city":"Cape Town","country_code":"ZA","admin":"Western Cape"},
    {"city":"Durban","country_code":"ZA","admin":"KwaZulu-Natal"},

    {"city":"Roma","country_code":"IT","admin":"Lazio"},
    {"city":"Milano","country_code":"IT","admin":"Lombardia"},
    {"city":"Napoli","country_code":"IT","admin":"Campania"},

    {"city":"Nairobi","country_code":"KE","admin":"Nairobi County"},
    {"city":"Mombasa","country_code":"KE","admin":"Mombasa County"},
    {"city":"Nakuru","country_code":"KE","admin":"Nakuru County"},

    {"city":"Yangon","country_code":"MM","admin":"Yangon Region"},
    {"city":"Mandalay","country_code":"MM","admin":"Mandalay Region"},
    {"city":"Naypyidaw","country_code":"MM","admin":"Naypyidaw Union Territory"},

    {"city":"Bogotá","country_code":"CO","admin":"Bogotá D.C."},
    {"city":"Medellín","country_code":"CO","admin":"Antioquia"},
    {"city":"Cali","country_code":"CO","admin":"Valle del Cauca"},

    {"city":"Omdurman","country_code":"SD","admin":"Khartoum"},
    {"city":"Khartoum","country_code":"SD","admin":"Khartoum"},
    {"city":"Khartoum North","country_code":"SD","admin":"Khartoum"},

    {"city":"Kampala","country_code":"UG","admin":"Central Region"},
    {"city":"Nansana","country_code":"UG","admin":"Central Region"},
    {"city":"Kira","country_code":"UG","admin":"Central Region"},

    {"city":"Seoul","country_code":"KR","admin":"Seoul"},
    {"city":"Busan","country_code":"KR","admin":"Busan"},
    {"city":"Incheon","country_code":"KR","admin":"Incheon"},

    {"city":"Algiers","country_code":"DZ","admin":"Algiers"},
    {"city":"Oran","country_code":"DZ","admin":"Oran"},
    {"city":"Constantine","country_code":"DZ","admin":"Constantine"}
  ]
}

```

The population choices were cross-checked against France's INSEE, Italy's ISTAT-based municipal figures, South Africa's 2022 metropolitan figures, Kenya's 2019 census, Myanmar's 2024 census-based lists, South Korea's September 2026 resident-registration figures, Algeria's 2008 census, and Sudan's 2008 census.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.insee.fr\&sz=32)

374+7



Confidence: High for France, Italy, Kenya and South Korea; medium for South Africa's city-versus-metropolitan definitions, Uganda's municipal classifications and Myanmar; low-to-medium for Sudan's current population ordering due to the age of its census and subsequent displacement.

### Geographic-boundary warnings

| City or group                      | Risk when using Nominatim                                                                    |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| Johannesburg, Cape Town, Durban    | Large metropolitan municipalities can contain extensive areas outside the dense urban core   |
| Roma                               | Commune extends significantly beyond central Rome                                            |
| Nairobi                            | Nairobi City County is larger than the central built-up business area                        |
| Nakuru                             | City and county names overlap; reject a county-only result                                   |
| Naypyidaw                          | Union Territory is vastly larger than the central city and contains separated settlements    |
| Bogotá                             | Bogotá D.C. contains extensive rural territory                                               |
| Omdurman, Khartoum, Khartoum North | Adjacent urban areas; overlapping boxes and accidental metropolitan resolution are likely    |
| Kampala, Nansana, Kira             | Distinct municipalities within the Greater Kampala urban area; high duplicate potential      |
| Seoul, Busan, Incheon              | City-level administrative jurisdictions include peripheral areas and, in some cases, islands |
| Algiers, Oran, Constantine         | Province/wilaya and city share names; avoid selecting the province                           |

These are review flags, not confirmed errors.

For Sudan, the specified three cities follow the historical 2008 city-proper census. Current urban population rankings cannot be regarded as reliable without newer comparable data, given the ongoing conflict and displacement documented in July 2026.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.gov.uk\&sz=32)

GOV.UK



For Uganda, the municipal boundaries of Nansana and Kira are the intended targets; do not substitute Kampala's full metropolitan boundary.

## 7. Production architecture — Recommend Geofabrik regional extracts processed locally

Decision: Use Geofabrik + Pyosmium as the primary OSM ingestion method. Keep self-hosted Overpass as an optional future capability, not the starting architecture.

This is the strongest fit for a small engineering team building a global, repeatable lead-generation product.

### Compare the three practical options

Option A — Geofabrik extracts + local filtering

Recommended

Best for country-wide business discovery and predictable recurring costs.

| Data download        | Free                                                          |
| -------------------- | ------------------------------------------------------------- |
| Cloud infrastructure | Approx. $24–$96+/month for a staged deployment                |
| Initial engineering  | Estimated 3–5 developer days                                  |
| Maintenance          | Estimated 1–3 hours/week after stabilization                  |
| Main risks           | Data freshness, storage capacity, geometry parsing, licensing |

Geofabrik provides free country and regional `.osm.pbf` downloads, normally updated daily, with change files for incremental updates. The data is subject to ODbL conditions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.geofabrik.de\&sz=32)

geofabrik.de



Option B — Self-hosted Overpass

Best if SiteBlitz later requires complex, arbitrary OSM queries without constructing its own query/indexing layer.

| Software license cost         | $0                                                              |
| ----------------------------- | --------------------------------------------------------------- |
| Example infrastructure budget | Approximately $96–$336+/month for a moderately sized deployment |
| Initial engineering           | Estimated 3–10 developer days                                   |
| Maintenance                   | Higher: database updates, tuning, monitoring, backups           |
| Main risks                    | RAM, disk I/O, database size, operational complexity            |

The official Overpass installation guidance highlights SSD performance and memory requirements. Full-planet deployments are substantially larger than the country-scale estimates above.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wiki.openstreetmap.org\&sz=32)

OpenStreetMap Wiki



Option C — Commercial OSM-based Places API

Best for a quick integration, supplementary lookups, or when the team wants managed availability instead of infrastructure ownership.

Example: Geoapify Places API.

| Free tier           | 3,000 credits/day                                               |
| ------------------- | --------------------------------------------------------------- |
| Paid starting tier  | $59/month, 10,000 credits/day                                   |
| Higher example      | $109/month, 25,000 credits/day                                  |
| Initial engineering | Estimated 1–2 developer days                                    |
| Main risks          | Provider dependency, usage costs, limits on exhaustive coverage |

A Places API call costs one credit per 20 returned places. Importantly, the provider explicitly says the API is not an exhaustive country-wide bulk-export service.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.geoapify.com\&sz=32)

Geoapify Location Platform+2



Cloud estimates use published DigitalOcean VM prices: $24/month for 4 GiB RAM, $48/month for 8 GiB, $96/month for 16 GiB. Additional block storage is $0.10/GiB/month. Prices verified November 8, 2026; engineering time and capacity requirements are my estimates, not vendor quotations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.digitalocean.com\&sz=32)

DigitalOcean+1

&#x20;Confidence: high on published prices, medium on projected infrastructure requirements.

### How I would implement Option A

Recommended data flow. Process each country snapshot once, then execute many city searches against the local index rather than repeatedly querying public services.

The practical implementation is to download country PBF files on a schedule, extract relevant OSM objects with their contact tags and coordinates, store indexed records locally, and query them by the same geographic scope used for Overture.

Pyosmium supports streaming reads and filters. Processing an entire country does not require loading every object into application memory at once, although geometries for ways and relations need special care.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.osmcode.org\&sz=32)

Pyosmium 4.3.2



Pilot acceptance test

I recommend five countries initially: India, Kenya, France, United States, and China. Compare 10 previously tested cities against identical geographic boxes.

- Public Overpass requests: 0
- OSM source availability: 100% of searches against successfully indexed country snapshots
- Data freshness: 7 days or less for the pilot
- Incremental unique businesses: measure against Overture alone
- Processing cost: report CPU time, peak memory, disk usage, and cost per 1,000 returned businesses

If locally extracted OSM produces fewer than 5% additional verified unique leads in a particular country, assess whether maintaining that country's OSM index is commercially worthwhile.

The pilot benefits engineering through reliable discovery and the founder through better information about actual cost per lead.

### Legal condition — important for merging OSM and Overture

OpenStreetMap permits commercial use under the Open Database License (ODbL), subject to attribution and applicable share-alike obligations.

Overture Places uses different licenses, including CDLA Permissive 2.0 and Apache 2.0. Its own documentation warns that joining Overture Places with OSM can create an ODbL derivative-database obligation.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://osmfoundation.org\&sz=32)

OpenStreetMap Foundation+2



Recommendation: Preserve source identifiers, source licenses, transformation history, and clear separation between source-specific records and combined outputs. Have counsel review whether a particular merged dataset is a collective database or a derivative database before public redistribution.

Primary references:

[Geofabrik — downloads and licensing](https://www.geofabrik.de/en/data/download.html?utm_source=chatgpt.com)[OSM Foundation — licensing FAQ](https://osmfoundation.org/wiki/Licence/Licence_and_Legal_FAQ?utm_source=chatgpt.com)[Overture Maps — Places and licensing](https://docs.overturemaps.org/guides/places/?utm_source=chatgpt.com)Legal references reviewed November 8, 2026. Confidence: high on the published licenses; the obligations of SiteBlitz's particular merged database require legal review.

## 8. Remaining Round 4 verdicts — Agree with keeping deferred features separate

| Previously open item         | My position                                                                      |
| ---------------------------- | -------------------------------------------------------------------------------- |
| Three source outcome labels  | Agree they can wait until the background-job phase                               |
| Email verification           | Agree; do not block discovery or claim email validity                            |
| Free-email prioritization    | Agree; retain as a weak signal pending the 50+50 audit                           |
| Email-assisted deduplication | Agree with the implemented two-evidence rule; retain the shared-head-office test |
| Trimming oversized cities    | Agree with returning useful data rather than zero; qualify geographic coverage   |
| Round 4 rerun                | Need data from the corrected geocoder before assessing the final results         |

## Points still open

1. Complete the first four batches and report final unique counts, source failures, and geographic mismatches.
2. Verify Beijing, Shenzhen and Ho Chi Minh City's results after the geocoding fix.
3. Reconcile Indore's zero contact percentages against previously stored records.
4. Measure OSM completeness by running the proposed Geofabrik local-extract pilot.
5. Decide how SiteBlitz will manage and refresh country-specific OSM indices in production.
6. Validate the 30 Round 5 cities, especially oversized administrative territories and overlapping urban municipalities.
7. Complete the 120-record category precision audit.
8. Validate the social-without-website opportunity using actual business websites.
9. Test the additional value of free-email status for prioritization.
10. Complete a legal review of source attribution, merged-database licensing, and use of business contact information.
11. Continue Round 6 with the fixed countries: Iraq, Spain, Argentina, Yemen, Canada, Angola, Ukraine, Morocco, Poland and Uzbekistan.

Round 5 delivered: 30 international city inputs and a sourced OSM production architecture recommendation.

Cumulative planned test inputs: 235 cities across five batches.
