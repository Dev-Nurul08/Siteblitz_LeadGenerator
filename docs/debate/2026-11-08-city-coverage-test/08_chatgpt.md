# SiteBlitz Lead Generator — Round 8 of 10

## 1. Results review — Agree

The Bangladesh results strengthen the case for prioritising website-development prospects there, especially outside Dhaka. The reported social-profile-without-listed-website rates are promising, but they should remain source-data signals, not verified proof that a business has no website.

Agree: Sreepur, Kaliakair, Kandahar and Mbuji-Mayi should not be classified as geocoding failures. Their locations resolved correctly; the available Overture dentist data returned zero matches.

I also agree with keeping the existing `NO_SITE_VERIFIED` scoring specification unchanged until the founder approves any reporting-segment changes.

## 2. Batch 8 — Population reference and count

The selection follows India's 2011 municipal/city-proper census, Bangladesh's 2022 census and Afghanistan's September 2025 city estimates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

Wikipedia+2



India

# 50

Bangladesh

# 15

Afghanistan

# 6

Afghanistan: The reference ranking ends at rank 26, covering cities estimated to have more than 100,000 residents. I will supply ranks 21–26 and will not invent ranks 27–30.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

Wikipedia



India ranking adjustment: Tiruppur was already supplied in Batch 2, although some 2011 city-proper lists place it around rank 101. Udaipur and Maheshtala were not included earlier. To preserve 50 new Indian cities, Batch 8 will fill those earlier omissions and continue through the next distinct ranked cities. The batch is therefore a deduplicated continuation of the intended top-150 coverage, rather than an exact reproduction of a single source's rank numbers.

Batch 8 · 71 locations · No city repeats from Batches 1–7

```

{
  "batch": 8,
  "cities": [
    {"city":"Udaipur","country_code":"IN","admin":"Rajasthan"},
    {"city":"Maheshtala","country_code":"IN","admin":"West Bengal"},
    {"city":"Davanagere","country_code":"IN","admin":"Karnataka"},
    {"city":"Kozhikode","country_code":"IN","admin":"Kerala"},
    {"city":"Kurnool","country_code":"IN","admin":"Andhra Pradesh"},
    {"city":"Akola","country_code":"IN","admin":"Maharashtra"},
    {"city":"Rajpur Sonarpur","country_code":"IN","admin":"West Bengal"},
    {"city":"Bokaro","country_code":"IN","admin":"Jharkhand"},
    {"city":"Ballari","country_code":"IN","admin":"Karnataka"},
    {"city":"Patiala","country_code":"IN","admin":"Punjab"},
    {"city":"South Dum Dum","country_code":"IN","admin":"West Bengal"},
    {"city":"Rajarhat-Gopalpur","country_code":"IN","admin":"West Bengal"},
    {"city":"Agartala","country_code":"IN","admin":"Tripura"},
    {"city":"Bhagalpur","country_code":"IN","admin":"Bihar"},
    {"city":"Muzaffarnagar","country_code":"IN","admin":"Uttar Pradesh"},
    {"city":"Bhatpara","country_code":"IN","admin":"West Bengal"},
    {"city":"Latur","country_code":"IN","admin":"Maharashtra"},
    {"city":"Panihati","country_code":"IN","admin":"West Bengal"},
    {"city":"Dhule","country_code":"IN","admin":"Maharashtra"},
    {"city":"Rohtak","country_code":"IN","admin":"Haryana"},
    {"city":"Korba","country_code":"IN","admin":"Chhattisgarh"},
    {"city":"Bhilwara","country_code":"IN","admin":"Rajasthan"},
    {"city":"Brahmapur","country_code":"IN","admin":"Odisha"},
    {"city":"Muzaffarpur","country_code":"IN","admin":"Bihar"},
    {"city":"Ahilyanagar","country_code":"IN","admin":"Maharashtra"},
    {"city":"Mathura","country_code":"IN","admin":"Uttar Pradesh"},
    {"city":"Kollam","country_code":"IN","admin":"Kerala"},
    {"city":"Avadi","country_code":"IN","admin":"Tamil Nadu"},
    {"city":"Kadapa","country_code":"IN","admin":"Andhra Pradesh"},
    {"city":"Rajamahendravaram","country_code":"IN","admin":"Andhra Pradesh"},
    {"city":"Bilaspur","country_code":"IN","admin":"Chhattisgarh"},
    {"city":"Kamarhati","country_code":"IN","admin":"West Bengal"},
    {"city":"Shahjahanpur","country_code":"IN","admin":"Uttar Pradesh"},
    {"city":"Vijayapura","country_code":"IN","admin":"Karnataka"},
    {"city":"Rampur","country_code":"IN","admin":"Uttar Pradesh"},
    {"city":"Shivamogga","country_code":"IN","admin":"Karnataka"},
    {"city":"Chandrapur","country_code":"IN","admin":"Maharashtra"},
    {"city":"Junagadh","country_code":"IN","admin":"Gujarat"},
    {"city":"Thrissur","country_code":"IN","admin":"Kerala"},
    {"city":"Alwar","country_code":"IN","admin":"Rajasthan"},
    {"city":"Bardhaman","country_code":"IN","admin":"West Bengal"},
    {"city":"Kulti","country_code":"IN","admin":"West Bengal"},
    {"city":"Kakinada","country_code":"IN","admin":"Andhra Pradesh"},
    {"city":"Nizamabad","country_code":"IN","admin":"Telangana"},
    {"city":"Parbhani","country_code":"IN","admin":"Maharashtra"},
    {"city":"Tumakuru","country_code":"IN","admin":"Karnataka"},
    {"city":"Hisar","country_code":"IN","admin":"Haryana"},
    {"city":"Ozhukarai","country_code":"IN","admin":"Puducherry"},
    {"city":"Bihar Sharif","country_code":"IN","admin":"Bihar"},
    {"city":"Darbhanga","country_code":"IN","admin":"Bihar"},

    {"city":"Cox's Bazar","country_code":"BD","admin":"Chattogram"},
    {"city":"Sirajganj","country_code":"BD","admin":"Rajshahi"},
    {"city":"Narsingdi","country_code":"BD","admin":"Dhaka"},
    {"city":"Naogaon","country_code":"BD","admin":"Rajshahi"},
    {"city":"Pabna","country_code":"BD","admin":"Rajshahi"},
    {"city":"Jamalpur","country_code":"BD","admin":"Mymensingh"},
    {"city":"Bhairab","country_code":"BD","admin":"Dhaka"},
    {"city":"Saidpur","country_code":"BD","admin":"Rangpur"},
    {"city":"Jhenaidah","country_code":"BD","admin":"Khulna"},
    {"city":"Satkhira","country_code":"BD","admin":"Khulna"},
    {"city":"Kishoreganj","country_code":"BD","admin":"Dhaka"},
    {"city":"Dhamsona","country_code":"BD","admin":"Dhaka"},
    {"city":"Lakshmipur","country_code":"BD","admin":"Chattogram"},
    {"city":"Maijdee","country_code":"BD","admin":"Chattogram"},
    {"city":"Sherpur","country_code":"BD","admin":"Mymensingh"},

    {"city":"Firozkoh","country_code":"AF","admin":"Ghor"},
    {"city":"Tarinkot","country_code":"AF","admin":"Uruzgan"},
    {"city":"Spin Boldak","country_code":"AF","admin":"Kandahar"},
    {"city":"Maimana","country_code":"AF","admin":"Faryab"},
    {"city":"Gardez","country_code":"AF","admin":"Paktia"},
    {"city":"Bamyan","country_code":"AF","admin":"Bamyan"}
  ]
}

```

## 3. Alternate spellings — only where resolution may be uncertain

| JSON name         | Alternate spelling or name                |
| ----------------- | ----------------------------------------- |
| Rajpur Sonarpur   | Rajpur-Sonarpur                           |
| Rajarhat-Gopalpur | Rajarhat Gopalpur; Gopalpur (West Bengal) |
| Ballari           | Bellary                                   |
| South Dum Dum     | South Dumdum                              |
| Brahmapur         | Berhampur (Odisha)                        |
| Ahilyanagar       | Ahmednagar                                |
| Rajamahendravaram | Rajahmundry                               |
| Vijayapura        | Bijapur (Karnataka)                       |
| Tumakuru          | Tumkur                                    |
| Ozhukarai         | Oulgaret                                  |
| Bhairab           | Bhairab Bazar                             |
| Jhenaidah         | Jhenida                                   |
| Dhamsona          | Dhamsona Ganakbari; Ganakbari             |
| Maijdee           | Maijdi; Maijdee Court                     |
| Firozkoh          | Chaghcharan                               |
| Tarinkot          | Tarin Kot; Tirin Kot                      |
| Maimana           | Maymana                                   |
| Bamyan            | Bamiyan                                   |

Two naming decisions warrant attention.

Rajarhat-Gopalpur: The 2011 census municipality was incorporated into Bidhannagar Municipal Corporation in 2015. Its former boundaries may no longer exist as a matching settlement object.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wbxpress.com\&sz=32)

WBXPress+1



Maijdee: This is the urban centre associated with Noakhali Municipality, which occupies Bangladesh's rank 39 in the reference list. Searching simply for Noakhali risks selecting the district rather than the municipal settlement.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://nsds.bbs.gov.bd\&sz=32)

NSDS



The 2022 ranking's Dhamsona Ganakbari is an urban place, not confirmed here as an independent municipality. `Dhamsona` is a candidate lookup label, not a verified exact geographic equivalent.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



Verification status: The 71 JSON entries have been selected from population references, but their individual Nominatim results have not been tested live. Apply your existing exact-name, administrative-level and geographic-boundary checks.

## 4. Points still open

1. Complete the outstanding results from Batches 1–7 and reconcile final counts after the source-job-sightings and geocoding fixes.
2. Validate Batch 8's 71 geographic inputs, especially Rajarhat-Gopalpur, Dhamsona and Maijdee.
3. Keep population rankings and actual geographic search coverage separate where historic municipal boundaries have changed.
4. Continue measuring Overture source gaps rather than treating zero records as an absence of businesses.
5. Complete the approved website-verification pilot and 120-record dentist-category precision audit.
6. Decide whether the founder wants separate `SOCIAL_ONLY` and `NEITHER_LISTED` reporting labels without changing the approved scoring rules.
7. Obtain budget approval for Geofabrik-based local OSM processing and complete the relevant licensing review.
8. Round 9: Run a fresh validation batch, alongside country coverage patterns and lawful supplementary source recommendations.
9. Round 10: Conduct another validation batch and the final production-readiness review.

Round 8 delivered: 71 new inputs. Cumulative total: 366 planned city inputs across eight batches.
