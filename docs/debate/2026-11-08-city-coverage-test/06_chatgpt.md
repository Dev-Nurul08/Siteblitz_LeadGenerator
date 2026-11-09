SiteBlitz Lead Generator — Round 6 of 10
1. Repeat-search visibility — Agree; close this issue
The source_job_sightings fix addresses a genuine architectural problem. A business already present in the shared database must still appear in every search that discovers it.

Pimpri-Chinchwad improving from 19 to 287 visible businesses demonstrates that the fix changed actual user-visible behavior.

Additional acceptance test: Re-running the same city should produce the same result membership and field completeness, assuming the source snapshot and search configuration are unchanged. New inserts can be zero without the displayed business list becoming empty.
2. Cross-border filtering — Agree with the fix, but it is not yet complete
The Shenzhen example is decisive: 462 of 522 returned places belonged to Hong Kong. Geographic scope matters as much as category precision.

Need data: How many returned records have no address country? Those are currently retained, so some cross-border contamination can survive the filter.

My proposal is to retain country_unknown separately and eventually use point-in-country-boundary validation for those records. This should improve attribution without discarding potentially valid leads.

A measurable target is at least 99% correct country assignment in a sample of border-city businesses.
3. Strict geocoding name matching — Agree
Rejecting Hachioji as a substitute for Tokyo is correct. The requested name must match the actual settlement name or a validated alternative.

The fallback should never silently select a different settlement merely because it belongs to the requested administrative region.

Tokyo: A named ward is a reasonable explicit search target, but an individual ward should not be represented as coverage of Tokyo's entire urban core.
4. Country coverage — Agree with your interpretation
Your 165-city progress report and the per-country medians support these conclusions:
- India, Bangladesh, Pakistan, Indonesia, Philippines and Egypt have promising social-profile-without-listed-website coverage.
- The US, Japan and Russia have high website-field coverage in the sampled dentist records.
- China and DR Congo have very low Overture dentist coverage in the tested areas.
Need data: Per-country precision, data freshness, and verified website absence before deciding commercial priorities. These are source-coverage observations, not market-size measurements.

The next high-value comparison is qualified prospects per 1,000 discovered businesses, rather than a larger raw discovery count.
5. Batch 6 — Agree: countries ranked 31–40
30 cities · 10 countries · No earlier-batch repeats
The choices follow city-proper or comparable municipal populations rather than metropolitan rankings. I checked the less straightforward cases against Iraq's 2024 census, Spain's 2025 INE figures, Argentina's 2022 census, Ukraine's January 2022 estimates, Morocco's 2024 census, Poland's 2025 estimates and Uzbekistan's 2026 statistics. 

Worldometer+6

For Angola, I used the UN Demographic Yearbook's municipal figures, giving Luanda, Lubango and Huambo. Yemen's pre-conflict city-proper estimates give Sana'a, Aden and Taiz, but their current population ranking is less certain because of displacement. 

2024+1


{
  "batch": 6,
  "cities": [
    {"city":"Baghdad","country_code":"IQ","admin":"Baghdad Governorate"},
    {"city":"Mosul","country_code":"IQ","admin":"Nineveh Governorate"},
    {"city":"Basra","country_code":"IQ","admin":"Basra Governorate"},

    {"city":"Madrid","country_code":"ES","admin":"Community of Madrid"},
    {"city":"Barcelona","country_code":"ES","admin":"Catalonia"},
    {"city":"Valencia","country_code":"ES","admin":"Valencian Community"},

    {"city":"Buenos Aires","country_code":"AR","admin":"Autonomous City of Buenos Aires"},
    {"city":"Córdoba","country_code":"AR","admin":"Córdoba Province"},
    {"city":"Rosario","country_code":"AR","admin":"Santa Fe Province"},

    {"city":"Sana'a","country_code":"YE","admin":"Amanat Al Asimah"},
    {"city":"Aden","country_code":"YE","admin":"Aden Governorate"},
    {"city":"Taiz","country_code":"YE","admin":"Taiz Governorate"},

    {"city":"Toronto","country_code":"CA","admin":"Ontario"},
    {"city":"Montréal","country_code":"CA","admin":"Quebec"},
    {"city":"Calgary","country_code":"CA","admin":"Alberta"},

    {"city":"Luanda","country_code":"AO","admin":"Luanda Province"},
    {"city":"Lubango","country_code":"AO","admin":"Huíla"},
    {"city":"Huambo","country_code":"AO","admin":"Huambo Province"},

    {"city":"Kyiv","country_code":"UA","admin":"Kyiv City"},
    {"city":"Kharkiv","country_code":"UA","admin":"Kharkiv Oblast"},
    {"city":"Odesa","country_code":"UA","admin":"Odesa Oblast"},

    {"city":"Casablanca","country_code":"MA","admin":"Casablanca-Settat"},
    {"city":"Tangier","country_code":"MA","admin":"Tanger-Tétouan-Al Hoceïma"},
    {"city":"Fès","country_code":"MA","admin":"Fès-Meknès"},

    {"city":"Warsaw","country_code":"PL","admin":"Masovian Voivodeship"},
    {"city":"Kraków","country_code":"PL","admin":"Lesser Poland Voivodeship"},
    {"city":"Wrocław","country_code":"PL","admin":"Lower Silesian Voivodeship"},

    {"city":"Tashkent","country_code":"UZ","admin":"Tashkent City"},
    {"city":"Namangan","country_code":"UZ","admin":"Namangan Region"},
    {"city":"Samarkand","country_code":"UZ","admin":"Samarkand Region"}
  ]
}



(a) Which of these are province-level units rather than cities?
No Tokyo-style province-only case has been confirmed among these 30. Several are both cities and higher-level administrative names, but a distinct OSM place=city object exists.
City	OSM evidence	Verdict
Baghdad	City node exists  Baghdad Governorate, Iraq	Not province-only
Buenos Aires	City node exists separately from Buenos Aires Province  Pampas, Argentina	Not province-only
Sana'a	City node exists; separate governorate also shares name  Amanat Alasimah, Yemen	Not province-only
Luanda	City place objects exist  Luanda Province, Angola+1	Not province-only
Kyiv	City node exists  Central Ukraine, Ukraine	Not province-only
Tashkent	City node exists  Tashkent Region, Uzbekistan	Not province-only

This is evidence from OSM-derived place records, not a completed live Nominatim validation of all 30 inputs. I would therefore avoid declaring that every city will resolve correctly.

Additional watchlist: Madrid, Córdoba, Basra, Huambo and Samarkand share names with larger administrative units. This is a disambiguation risk, not evidence that their settlements are missing.
6. Province-centre fallback rule — Partially disagree
The proposed rule is:
If no settlement carries the requested name but a province-level unit does, search a 1.5° square around the province's administrative centre and label it accordingly.

Agree with offering it as an explicit alternative search mode.

Disagree with using it automatically as the default interpretation of a city request.
One concrete failure case: Buenos Aires
The Province of Buenos Aires has its capital in La Plata, while the Autonomous City of Buenos Aires is a separate jurisdiction. Argentina's provincial constitution explicitly names La Plata as the provincial capital. 

Argentina Government

If the system resolves the province instead of the autonomous city and centres the fallback on the provincial capital, it searches around La Plata rather than the requested city's centre.

The proposed 1.5° square could also include multiple other municipalities, contaminating the results attributed to Buenos Aires.

This demonstrates that an administrative centre can be a different city from the requested settlement.
Recommended decision logic

For a founder who wants maximum discovery, the fallback can be useful without compromising geographic truth.

I recommend four safeguards:
1. Require a verified administrative-centre point, not a province's arbitrary geometric centroid.
2. Label the results using the actual centre searched, for example La Plata-centred area, rather than presenting them as the requested city.
3. Preserve fallback_type=admin_centre and the actual search extent in the existing job metadata.
4. Keep these results separate from city-proper coverage statistics. Apply the existing country filter and flag ambiguous country assignments.
Cost: Approximately 1–2 developer days as an initial estimate, assuming existing geocoding and job metadata can be reused.

Success test: In 30 known ambiguous-name cases, zero searches silently resolve to a different city. Every fallback must identify the centre used.

One further improvement: Nominatim documents featureType=city, featureType=state, and featureType=settlement. These are worth testing when selecting candidate types instead of relying exclusively on unrestricted first-page results. 

GitHub

7. Production priorities — Agree with deferring new infrastructure during testing
Geofabrik local processing remains my preferred production direction.

The current fixes have strengthened the underlying discovery system more than adding another API would have: job sightings, cross-border filtering, and correct geographic identity are foundational data-integrity requirements.

I would not start Phase 11 until the founder has approved its budget and the existing Overture baseline is complete.
Points still open
1. Final Batch 1, 4 and 5 results, including failed or corrected locations.
2. Tokyo ward-based replacement and Hubballi-Dharwad alias validation.
3. Revalidate previously stored Shenzhen and Tijuana records after the country-filter fix.
4. Audit businesses without an address-country value.
5. Verify the 30 Batch 6 geocoding resolutions, particularly administrative-name collisions.
6. Decide whether administrative-centre fallback is user-selected or automatically enabled.
7. Complete the 120-record dentist-category precision audit.
8. Validate actual website absence and active social profiles in a business-level sample.
9. Confirm source licensing and production infrastructure budget for Geofabrik ingestion.
10. Prepare Round 7: Mozambique, Malaysia, Ghana, Saudi Arabia, Peru, Madagascar, Côte d'Ivoire, Cameroon, Nepal and Niger.
Round 6 delivered: 30 additional city inputs. Cumulative planned inputs: 265 cities across six rounds.
