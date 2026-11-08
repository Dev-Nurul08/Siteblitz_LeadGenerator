# SiteBlitz Lead Generator — Round 1 of 10

Decision: Agree with launching the 10-round international test, but improve how we validate geographic coverage, lead quality, and source reliability. The objective should be to discover usable, verified business leads, not merely maximize the number of records collected.

## Point-by-point review

### 1. City selection — Agree, with a qualification

Batch 1 will contain exactly 95 locations:

- India: 50 cities using 2011 city-proper census rankings.
- Bangladesh: 25 cities or urban municipalities using the 2022 census.
- Afghanistan: 20 cities using reported September 2025 population estimates.

These are different reference years and administrative definitions, so the rankings should not be compared directly between countries. India's city-proper list is also different from urban-agglomeration rankings.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

Wikipedia+2



My proposal: Keep the population-based selection for Round 1, but also record the population reference year and the geographic boundary actually searched.

Confidence: High for India's historical census ranking and Bangladesh's major cities; medium for Afghanistan's estimates.

### 2. Geocoding design — Disagree with relying on the first result alone

The supplied code uses the first Nominatim result for each city and converts it into a bounding box.

This is efficient but can select an administrative district, a broader municipality, or an unintended geographic feature.

I recommend validating the returned place type, administrative level, coordinates, and bounding-box dimensions before running discovery.

Important legal and operational constraint: The OpenStreetMap Foundation's public Nominatim policy permits no more than one request per second, requires identification and caching, and discourages bulk geocoding. Repeated large-scale testing should use appropriately licensed geocoding data, a self-hosted instance, or a commercial provider.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://operations.osmfoundation.org\&sz=32)

operations.osmfoundation.org+1



Source: [Official Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/?utm_source=chatgpt.com). Verified November 8, 2026. Confidence: High.

Success test: At least 99% of accepted city queries must resolve to the intended location; incorrect or oversized boundaries must be flagged rather than silently accepted.

Estimated cost: Low for additional validation logic; moderate infrastructure and maintenance costs for a self-hosted production geocoder.

### 3. Search area and 300-result limit — Disagree with treating the limit as full coverage

The 1.5° bounding-box rejection rule is a useful safety measure, but it does not establish whether the selected area is geographically correct.

Likewise, a city reaching 300 results may have many more matching businesses.

My proposal: Run two modes: a 300-result smoke test for every city, and a deeper coverage audit on 10 representative cities.

- Beneficiary: Engineering and sales teams, because they can distinguish genuinely low-coverage areas from artificially capped results.
- Cost: Additional queries, compute time, and operational monitoring; exact cost requires runtime measurements.
- Success test: Zero capped results should be presented as complete city coverage. Every rejected area should include a machine-readable reason.

### 4. Dentist category matching — Agree with the concept, but improve precision

The supplied `categories.py` excerpt combines category matches with business-name matches. This is a sensible way to improve recall.

However, the name regex can still match unwanted businesses such as dental-equipment suppliers, while English-only names may miss businesses named entirely in Bengali, Dari, or Pashto.

My proposal: Separate category-only, name-only, and combined matches. Manually audit 120 results across the three countries, including false-positive candidates and local-language names.

- Cost: Roughly one engineering day plus manual QA, as a planning estimate.
- Beneficiary: Sales teams receiving more relevant leads.
- Success test: Target at least 90% precision on the audited sample; measure recall against a separately prepared list of known dental practices.

### 5. Metrics and lead quality — Agree, with additions

The existing proposed metrics are useful: found, new, duplicates, available, errors, duration, and contact-field availability.

But record volume is not the same as usable lead volume. Overture's own documentation warns that its Places dataset contains duplicates, junk records, and incomplete properties.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.overturemaps.org\&sz=32)

Overture Documentation+1



My proposal: Add source-specific result counts, geographic validation status, capped-result flags, cross-city duplicates, source-data version, and verified lead quality.

For each city, measure:

Suggested acceptance targets — not measured results

| Geocoding accuracy               | ≥99%                                |
| -------------------------------- | ----------------------------------- |
| Audited category precision       | ≥90%                                |
| Cross-source duplicate detection | ≥95% on labelled pairs              |
| Unclassified failures            | 0                                   |
| Contact-field completeness       | Measure baseline; no assumed target |

Additional implementation and QA will require maintenance when source schemas or classifications change. The founder benefits from knowing the number of genuine, potentially contactable businesses rather than relying on inflated discovery counts.

### 6. Ten-round strategy — Agree, with one change

Rounds 1–8 make sense, but the proposed R9 and R10 are analysis and review rounds rather than additional city-testing rounds.

If the goal is strictly 10 rounds of testing, R9 and R10 should each include a fresh validation batch alongside their reporting responsibilities.

Also, `admin` is included in the requested JSON but is not used by the supplied `city_bbox(city, country_code)` function. That should be corrected before interpreting ambiguous city names as geographic failures.

Cost: A small code change and a validation test suite, followed by ongoing upkeep of administrative-name aliases. Success test: Ambiguous cities resolve to the correct administrative region without silently selecting another location.

I have not run SiteBlitz or verified its runtime results. The recommendations above are based on the supplied code excerpts and external documentation.

## 7. Batch 1 — 95 cities ready for testing

95 unique cities validated in the batch list

India

# 50

Bangladesh

# 25

Afghanistan

# 20

The following uses current English spellings where practical. Some uncertain or renamed place labels—including Chhatrapati Sambhaji Nagar, Hubballi-Dharwad, Sreepur, Tarabo, Mazar-i-Sharif, and Pul-i-Alam—will need confirmation against actual Nominatim results. Their inclusion is not a claim that geocoding has succeeded.

```

{"batch":1,"cities":[
  {"city":"Mumbai","country_code":"IN","admin":"Maharashtra"},
  {"city":"Delhi","country_code":"IN","admin":"Delhi"},
  {"city":"Bengaluru","country_code":"IN","admin":"Karnataka"},
  {"city":"Hyderabad","country_code":"IN","admin":"Telangana"},
  {"city":"Chennai","country_code":"IN","admin":"Tamil Nadu"},
  {"city":"Ahmedabad","country_code":"IN","admin":"Gujarat"},
  {"city":"Kolkata","country_code":"IN","admin":"West Bengal"},
  {"city":"Surat","country_code":"IN","admin":"Gujarat"},
  {"city":"Pune","country_code":"IN","admin":"Maharashtra"},
  {"city":"Jaipur","country_code":"IN","admin":"Rajasthan"},
  {"city":"Lucknow","country_code":"IN","admin":"Uttar Pradesh"},
  {"city":"Kanpur","country_code":"IN","admin":"Uttar Pradesh"},
  {"city":"Nagpur","country_code":"IN","admin":"Maharashtra"},
  {"city":"Indore","country_code":"IN","admin":"Madhya Pradesh"},
  {"city":"Thane","country_code":"IN","admin":"Maharashtra"},
  {"city":"Bhopal","country_code":"IN","admin":"Madhya Pradesh"},
  {"city":"Visakhapatnam","country_code":"IN","admin":"Andhra Pradesh"},
  {"city":"Pimpri-Chinchwad","country_code":"IN","admin":"Maharashtra"},
  {"city":"Patna","country_code":"IN","admin":"Bihar"},
  {"city":"Vadodara","country_code":"IN","admin":"Gujarat"},
  {"city":"Ghaziabad","country_code":"IN","admin":"Uttar Pradesh"},
  {"city":"Ludhiana","country_code":"IN","admin":"Punjab"},
  {"city":"Agra","country_code":"IN","admin":"Uttar Pradesh"},
  {"city":"Nashik","country_code":"IN","admin":"Maharashtra"},
  {"city":"Faridabad","country_code":"IN","admin":"Haryana"},
  {"city":"Meerut","country_code":"IN","admin":"Uttar Pradesh"},
  {"city":"Rajkot","country_code":"IN","admin":"Gujarat"},
  {"city":"Kalyan-Dombivli","country_code":"IN","admin":"Maharashtra"},
  {"city":"Vasai-Virar","country_code":"IN","admin":"Maharashtra"},
  {"city":"Varanasi","country_code":"IN","admin":"Uttar Pradesh"},
  {"city":"Srinagar","country_code":"IN","admin":"Jammu and Kashmir"},
  {"city":"Chhatrapati Sambhaji Nagar","country_code":"IN","admin":"Maharashtra"},
  {"city":"Dhanbad","country_code":"IN","admin":"Jharkhand"},
  {"city":"Amritsar","country_code":"IN","admin":"Punjab"},
  {"city":"Navi Mumbai","country_code":"IN","admin":"Maharashtra"},
  {"city":"Prayagraj","country_code":"IN","admin":"Uttar Pradesh"},
  {"city":"Howrah","country_code":"IN","admin":"West Bengal"},
  {"city":"Ranchi","country_code":"IN","admin":"Jharkhand"},
  {"city":"Jabalpur","country_code":"IN","admin":"Madhya Pradesh"},
  {"city":"Gwalior","country_code":"IN","admin":"Madhya Pradesh"},
  {"city":"Coimbatore","country_code":"IN","admin":"Tamil Nadu"},
  {"city":"Vijayawada","country_code":"IN","admin":"Andhra Pradesh"},
  {"city":"Jodhpur","country_code":"IN","admin":"Rajasthan"},
  {"city":"Madurai","country_code":"IN","admin":"Tamil Nadu"},
  {"city":"Raipur","country_code":"IN","admin":"Chhattisgarh"},
  {"city":"Kota","country_code":"IN","admin":"Rajasthan"},
  {"city":"Chandigarh","country_code":"IN","admin":"Chandigarh"},
  {"city":"Guwahati","country_code":"IN","admin":"Assam"},
  {"city":"Solapur","country_code":"IN","admin":"Maharashtra"},
  {"city":"Hubballi-Dharwad","country_code":"IN","admin":"Karnataka"},
  {"city":"Dhaka","country_code":"BD","admin":"Dhaka"},
  {"city":"Chattogram","country_code":"BD","admin":"Chattogram"},
  {"city":"Gazipur","country_code":"BD","admin":"Dhaka"},
  {"city":"Narayanganj","country_code":"BD","admin":"Dhaka"},
  {"city":"Khulna","country_code":"BD","admin":"Khulna"},
  {"city":"Rangpur","country_code":"BD","admin":"Rangpur"},
  {"city":"Mymensingh","country_code":"BD","admin":"Mymensingh"},
  {"city":"Rajshahi","country_code":"BD","admin":"Rajshahi"},
  {"city":"Sylhet","country_code":"BD","admin":"Sylhet"},
  {"city":"Bogura","country_code":"BD","admin":"Rajshahi"},
  {"city":"Cumilla","country_code":"BD","admin":"Chattogram"},
  {"city":"Barishal","country_code":"BD","admin":"Barishal"},
  {"city":"Savar","country_code":"BD","admin":"Dhaka"},
  {"city":"Brahmanbaria","country_code":"BD","admin":"Chattogram"},
  {"city":"Sreepur","country_code":"BD","admin":"Dhaka"},
  {"city":"Kaliakair","country_code":"BD","admin":"Dhaka"},
  {"city":"Faridpur","country_code":"BD","admin":"Dhaka"},
  {"city":"Feni","country_code":"BD","admin":"Chattogram"},
  {"city":"Kushtia","country_code":"BD","admin":"Khulna"},
  {"city":"Tangail","country_code":"BD","admin":"Dhaka"},
  {"city":"Dinajpur","country_code":"BD","admin":"Rangpur"},
  {"city":"Jashore","country_code":"BD","admin":"Khulna"},
  {"city":"Chandpur","country_code":"BD","admin":"Chattogram"},
  {"city":"Chapai Nawabganj","country_code":"BD","admin":"Rajshahi"},
  {"city":"Tarabo","country_code":"BD","admin":"Dhaka"},
  {"city":"Kabul","country_code":"AF","admin":"Kabul"},
  {"city":"Kandahar","country_code":"AF","admin":"Kandahar"},
  {"city":"Herat","country_code":"AF","admin":"Herat"},
  {"city":"Mazar-i-Sharif","country_code":"AF","admin":"Balkh"},
  {"city":"Kunduz","country_code":"AF","admin":"Kunduz"},
  {"city":"Jalalabad","country_code":"AF","admin":"Nangarhar"},
  {"city":"Taloqan","country_code":"AF","admin":"Takhar"},
  {"city":"Pul-e-Khumri","country_code":"AF","admin":"Baghlan"},
  {"city":"Charikar","country_code":"AF","admin":"Parwan"},
  {"city":"Baghlan","country_code":"AF","admin":"Baghlan"},
  {"city":"Sheberghan","country_code":"AF","admin":"Jowzjan"},
  {"city":"Ghazni","country_code":"AF","admin":"Ghazni"},
  {"city":"Lashkargah","country_code":"AF","admin":"Helmand"},
  {"city":"Khost","country_code":"AF","admin":"Khost"},
  {"city":"Mihtarlam","country_code":"AF","admin":"Laghman"},
  {"city":"Balkh","country_code":"AF","admin":"Balkh"},
  {"city":"Farah","country_code":"AF","admin":"Farah"},
  {"city":"Sar-e-Pol","country_code":"AF","admin":"Sar-e-Pul"},
  {"city":"Pul-i-Alam","country_code":"AF","admin":"Logar"},
  {"city":"Aybak","country_code":"AF","admin":"Samangan"}
]}

```

## Points still open

1. Geocoding verification: Which of the 95 city names produce correct boundaries, and which need alternate spellings or administrative disambiguation?
2. Coverage: How many matching businesses exist beyond the 300-result cap?
3. Deduplication: Are nearby-city records and Overture–OSM overlaps correctly merged?
4. Lead quality: What percentage of results are genuine dentists with usable contact information?
5. Source economics and compliance: Can the planned international scale be supported reliably, including licensing, service limits, and applicable privacy requirements?
6. Next-round evidence: Need measured Batch 1 results before deciding the highest-value changes for Round 2.

Round 1 is ready as a city-input batch. Discovery results remain unverified until Claude Code executes the tests and returns the measurements.
