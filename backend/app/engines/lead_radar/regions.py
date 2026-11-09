"""
Lead-Radar Regional Calibration, 45-City Baselines, and State/Country Profiles.

Implements all specifications from Section 11 of the 2026-11-06 strategy:
- 4 Indian economic archetypes (Section 11.4)
- 16 Indian state profiles with priorities (↑) and discounts (↓) (Section 11.5)
- 27 Country profiles across Global tiers (Section 11.6)
- Town size calibration (Metro vs Tier-2 vs Tier-3) with empirical sample size blending (Section 11.3 & 11.7)
- Complete measured baseline dataset for 45 global cities from Overture Places release (Section 11.9)
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from backend.app.engines.lead_radar.types import (
    ConditionID,
    IndianEconomicType,
    RegionalProfile,
)


@dataclass
class CityBaseline:
    city: str
    country: str
    places: int
    confident_places: int
    meta_first_pct: float
    confident_no_website_pct: float
    phone_pct: float
    email_pct: float
    social_pct: float


# ─── SECTION 11.9: COMPLETE 45-CITY MEASURED BASELINE DATASET ──

OVERTURE_45_CITY_BASELINES: Dict[str, CityBaseline] = {
    # India (20 Cities)
    "mumbai": CityBaseline("Mumbai", "India", 148298, 48744, 85.4, 24.5, 66.1, 31.9, 93.3),
    "pune": CityBaseline("Pune", "India", 108492, 38128, 84.1, 23.3, 76.7, 42.9, 94.9),
    "nagpur": CityBaseline("Nagpur", "India", 31086, 10866, 85.5, 27.0, 81.7, 51.5, 95.8),
    "ahmedabad": CityBaseline("Ahmedabad", "India", 88495, 32052, 85.3, 26.9, 74.6, 42.5, 95.7),
    "surat": CityBaseline("Surat", "India", 53522, 16409, 89.1, 34.7, 76.1, 46.9, 95.7),
    "rajkot": CityBaseline("Rajkot", "India", 21628, 7515, 86.1, 28.7, 82.3, 52.1, 95.6),
    "delhi": CityBaseline("Delhi", "India", 183803, 65856, 81.8, 21.0, 71.1, 36.4, 92.5),
    "bengaluru": CityBaseline("Bengaluru", "India", 186881, 63571, 82.3, 18.5, 72.2, 34.3, 93.6),
    "chennai": CityBaseline("Chennai", "India", 113856, 36249, 83.6, 18.7, 73.9, 36.4, 94.3),
    "coimbatore": CityBaseline("Coimbatore", "India", 34655, 11392, 84.3, 18.8, 78.3, 45.7, 95.3),
    "hyderabad": CityBaseline("Hyderabad", "India", 130580, 42018, 83.0, 21.3, 70.8, 30.6, 94.6),
    "kolkata": CityBaseline("Kolkata", "India", 137091, 43081, 87.2, 31.5, 66.9, 39.0, 94.4),
    "jaipur": CityBaseline("Jaipur", "India", 69461, 21913, 86.0, 23.4, 78.2, 46.1, 94.9),
    "lucknow": CityBaseline("Lucknow", "India", 52294, 17987, 85.1, 27.4, 75.7, 43.6, 94.2),
    "indore": CityBaseline("Indore", "India", 39002, 12514, 85.4, 25.3, 75.9, 46.1, 94.9),
    "kochi": CityBaseline("Kochi", "India", 35445, 11956, 85.8, 21.1, 73.4, 38.5, 94.5),
    "chandigarh": CityBaseline("Chandigarh", "India", 41957, 16157, 82.6, 23.7, 74.4, 43.0, 92.5),
    "patna": CityBaseline("Patna", "India", 33091, 11625, 85.3, 26.7, 71.7, 41.8, 94.0),
    "guwahati": CityBaseline("Guwahati", "India", 20498, 7771, 85.5, 33.1, 71.9, 45.1, 95.8),
    "bhubaneswar": CityBaseline("Bhubaneswar", "India", 21845, 8317, 83.0, 23.2, 68.8, 41.6, 91.4),

    # United States & Canada
    "new york": CityBaseline("New York", "United States", 419150, 267213, 48.8, 18.4, 53.5, 7.5, 33.5),
    "dallas": CityBaseline("Dallas", "United States", 72172, 54025, 45.6, 15.9, 54.7, 11.6, 39.3),
    "toronto": CityBaseline("Toronto", "Canada", 107427, 74224, 68.4, 7.1, 67.6, 17.9, 91.0),

    # United Kingdom & Europe
    "london": CityBaseline("London", "United Kingdom", 408772, 212210, 29.0, 10.6, 57.8, 8.2, 54.7),
    "manchester": CityBaseline("Manchester", "United Kingdom", 104668, 66185, 33.6, 12.5, 63.9, 15.0, 57.8),
    "berlin": CityBaseline("Berlin", "Germany", 189936, 93613, 28.3, 9.8, 64.8, 10.4, 56.8),
    "paris": CityBaseline("Paris", "France", 378175, 149068, 34.4, 16.5, 69.3, 13.4, 62.2),
    "istanbul": CityBaseline("Istanbul", "Turkey", 212214, 112750, 91.0, 37.7, 58.2, 15.2, 89.3),

    # Middle East & Africa
    "dubai": CityBaseline("Dubai", "UAE", 71138, 32754, 87.1, 24.0, 63.2, 19.0, 96.8),
    "riyadh": CityBaseline("Riyadh", "Saudi Arabia", 34444, 17378, 75.8, 33.1, 51.8, 6.6, 87.8),
    "cairo": CityBaseline("Cairo", "Egypt", 109618, 25825, 95.2, 44.0, 72.0, 28.6, 96.5),
    "lagos": CityBaseline("Lagos", "Nigeria", 53391, 11307, 98.3, 35.0, 72.1, 45.6, 97.1),
    "nairobi": CityBaseline("Nairobi", "Kenya", 52526, 17048, 96.0, 33.3, 71.5, 42.2, 95.2),
    "johannesburg": CityBaseline("Johannesburg", "South Africa", 72104, 27078, 86.9, 28.8, 46.3, 26.6, 63.0),

    # Asia Pacific
    "karachi": CityBaseline("Karachi", "Pakistan", 34163, 13058, 97.5, 44.2, 74.3, 37.7, 98.9),
    "dhaka": CityBaseline("Dhaka", "Bangladesh", 127007, 33255, 98.9, 44.1, 61.5, 34.2, 99.7),
    "singapore": CityBaseline("Singapore", "Singapore", 126974, 54189, 90.9, 27.2, 65.8, 20.8, 97.3),
    "jakarta": CityBaseline("Jakarta", "Indonesia", 227670, 65555, 97.2, 46.8, 59.6, 14.9, 99.0),
    "manila": CityBaseline("Manila", "Philippines", 280087, 91615, 96.3, 52.9, 61.0, 30.1, 98.3),
    "ho chi minh city": CityBaseline("Ho Chi Minh City", "Vietnam", 380409, 109705, 98.8, 42.2, 81.2, 37.6, 98.3),
    "bangkok": CityBaseline("Bangkok", "Thailand", 291452, 139261, 96.1, 61.2, 60.0, 20.4, 96.4),
    "tokyo": CityBaseline("Tokyo", "Japan", 353838, 278170, 73.0, 22.3, 59.2, 4.2, 88.4),
    "sydney": CityBaseline("Sydney", "Australia", 115062, 81458, 65.1, 9.7, 62.1, 19.7, 90.5),

    # Latin America
    "são paulo": CityBaseline("São Paulo", "Brazil", 424582, 190688, 94.3, 32.7, 83.0, 32.0, 96.7),
    "mexico city": CityBaseline("Mexico City", "Mexico", 318322, 114147, 94.0, 44.9, 75.8, 34.5, 97.4),
}


# ─── SECTION 11.5: 16 INDIAN STATE PROFILES ─────────────────────

INDIAN_STATE_PROFILES: Dict[str, RegionalProfile] = {
    "IN-MH": RegionalProfile(
        region_code="IN-MH",
        region_name="Maharashtra",
        country_code="IN",
        economic_type=IndianEconomicType.METRO_SERVICES,
        baseline_no_website_percent=24.5,
        check_first=[ConditionID.W5, ConditionID.W6, ConditionID.D6, ConditionID.D8, ConditionID.D9],
        trust_less=["Mumbai assumptions applied statewide", "W1 alone without task gap"],
        local_sources=["MIDC", "MahaRERA", "MCGM Municipal"],
        local_languages=["Marathi", "Hindi", "English"],
        target_categories=["Clinics", "Professional Services", "Food Groups", "Industrial Suppliers"],
    ),
    "IN-GJ": RegionalProfile(
        region_code="IN-GJ",
        region_name="Gujarat",
        country_code="IN",
        economic_type=IndianEconomicType.MANUFACTURING_EXPORT,
        baseline_no_website_percent=34.7,
        check_first=[ConditionID.D8, ConditionID.D9, ConditionID.W7, ConditionID.W10, ConditionID.W16],
        trust_less=["Reviews for B2B factories", "IndiaMART presence as proof of exports"],
        local_sources=["GIDC", "Gujarat RERA", "District Industries Centres", "Export Councils"],
        local_languages=["Gujarati", "Hindi", "English"],
        target_categories=["Textile", "Engineering", "Ceramics", "Chemicals", "Wholesale"],
    ),
    "IN-DL": RegionalProfile(
        region_code="IN-DL",
        region_name="Delhi NCR",
        country_code="IN",
        economic_type=IndianEconomicType.METRO_SERVICES,
        baseline_no_website_percent=21.0,
        check_first=[ConditionID.W8, ConditionID.W9, ConditionID.D6, ConditionID.D8],
        trust_less=["Delhi municipality box as representative of entire NCR", "Single address listings"],
        local_sources=["Delhi Industries", "UP-RERA", "Haryana RERA"],
        local_languages=["Hindi", "English", "Punjabi"],
        target_categories=["Services", "Clinics", "Wholesale", "Logistics", "Suppliers"],
    ),
    "IN-KA": RegionalProfile(
        region_code="IN-KA",
        region_name="Karnataka",
        country_code="IN",
        economic_type=IndianEconomicType.METRO_SERVICES,
        baseline_no_website_percent=18.5,
        check_first=[ConditionID.W5, ConditionID.W6, ConditionID.W13, ConditionID.D6, ConditionID.D7],
        trust_less=["Tech-city sophistication assumed for traditional shops", "Developer hiring as agency intent"],
        local_sources=["KIADB", "Karnataka RERA"],
        local_languages=["Kannada", "English"],
        target_categories=["Clinics", "Technical Services", "Food Groups", "Specialty Suppliers"],
    ),
    "IN-TN": RegionalProfile(
        region_code="IN-TN",
        region_name="Tamil Nadu",
        country_code="IN",
        economic_type=IndianEconomicType.MANUFACTURING_EXPORT,
        baseline_no_website_percent=18.7,
        check_first=[ConditionID.W7, ConditionID.D8, ConditionID.D9, ConditionID.W5, ConditionID.W6],
        trust_less=["Initials and transliteration mismatches as separate entities"],
        local_sources=["SIPCOT", "Guidance TN", "Export Promotion Bodies"],
        local_languages=["Tamil", "English"],
        target_categories=["Engineering", "Textile Exporters", "Clinics", "Coaching", "Lodging"],
    ),
    "IN-TG": RegionalProfile(
        region_code="IN-TG",
        region_name="Telangana",
        country_code="IN",
        economic_type=IndianEconomicType.METRO_SERVICES,
        baseline_no_website_percent=21.3,
        check_first=[ConditionID.W5, ConditionID.W6, ConditionID.D6, ConditionID.W7, ConditionID.D8],
        trust_less=["Pharma and IT budget assumptions applied to all businesses"],
        local_sources=["TSIIC", "TG-RERA"],
        local_languages=["Telugu", "Urdu", "English"],
        target_categories=["Clinics", "Diagnostic Labs", "B2B Services", "Industrial Suppliers"],
    ),
    "IN-WB": RegionalProfile(
        region_code="IN-WB",
        region_name="West Bengal",
        country_code="IN",
        economic_type=IndianEconomicType.REGIONAL_TRADE_SERVICE,
        baseline_no_website_percent=31.5,
        check_first=[ConditionID.W7, ConditionID.W8, ConditionID.D11, ConditionID.D8, ConditionID.D9],
        trust_less=["Low social posting velocity interpreted as permanent closure", "Old colonial place spellings"],
        local_sources=["WBIDC", "WBRERA"],
        local_languages=["Bengali", "English", "Hindi"],
        target_categories=["Wholesale", "Clinics", "Professional Services", "Regional Suppliers"],
    ),
    "IN-RJ": RegionalProfile(
        region_code="IN-RJ",
        region_name="Rajasthan",
        country_code="IN",
        economic_type=IndianEconomicType.TOURISM,
        baseline_no_website_percent=23.4,
        check_first=[ConditionID.W5, ConditionID.W10, ConditionID.W15, ConditionID.W16, ConditionID.W7, ConditionID.D9],
        trust_less=["Statewide tourism assumption outside golden triangle", "Off-season quiet periods"],
        local_sources=["RIICO", "Rajasthan Tourism", "Raj-RERA"],
        local_languages=["Hindi", "English", "Marwari"],
        target_categories=["Hotels", "Tours", "Handicraft and Jewellery", "Industrial Suppliers"],
    ),
    "IN-UP": RegionalProfile(
        region_code="IN-UP",
        region_name="Uttar Pradesh",
        country_code="IN",
        economic_type=IndianEconomicType.REGIONAL_TRADE_SERVICE,
        baseline_no_website_percent=27.4,
        check_first=[ConditionID.W7, ConditionID.D8, ConditionID.D9, ConditionID.W5, ConditionID.D11],
        trust_less=["Lucknow baseline applied to rural ODOP clusters", "Low online footprint as no budget"],
        local_sources=["ODOP Scheme", "UPSIDA", "UP-RERA"],
        local_languages=["Hindi", "Urdu", "English"],
        target_categories=["Cluster Manufacturers", "Wholesalers", "Clinics", "Coaching", "Logistics"],
    ),
    "IN-MP": RegionalProfile(
        region_code="IN-MP",
        region_name="Madhya Pradesh",
        country_code="IN",
        economic_type=IndianEconomicType.REGIONAL_TRADE_SERVICE,
        baseline_no_website_percent=25.3,
        check_first=[ConditionID.W7, ConditionID.W8, ConditionID.D11, ConditionID.D7],
        trust_less=["Export weighting for inland trade towns", "Review count penalties"],
        local_sources=["MPIDC", "MP-RERA"],
        local_languages=["Hindi", "English"],
        target_categories=["Wholesale", "Logistics", "Food Processing", "Clinics", "Suppliers"],
    ),
    "IN-KL": RegionalProfile(
        region_code="IN-KL",
        region_name="Kerala",
        country_code="IN",
        economic_type=IndianEconomicType.TOURISM,
        baseline_no_website_percent=21.1,
        check_first=[ConditionID.W5, ConditionID.W10, ConditionID.W15, ConditionID.W16, ConditionID.D9],
        trust_less=["Monsoon off-season quietness treated as closure"],
        local_sources=["KINFRA", "Kerala Tourism", "Marine Products Export"],
        local_languages=["Malayalam", "English"],
        target_categories=["Lodging", "Ayurvedic Clinics", "Experiences", "Seafood and Spice Exporters"],
    ),
    "IN-PB": RegionalProfile(
        region_code="IN-PB",
        region_name="Punjab",
        country_code="IN",
        economic_type=IndianEconomicType.MANUFACTURING_EXPORT,
        baseline_no_website_percent=23.7,
        check_first=[ConditionID.W7, ConditionID.D8, ConditionID.D9, ConditionID.W5, ConditionID.D11],
        trust_less=["Chandigarh metrics standing in for all of Punjab"],
        local_sources=["PSIEC", "Invest Punjab"],
        local_languages=["Gurmukhi", "Hindi", "English"],
        target_categories=["Engineering", "Textile & Hosiery", "Agri Services", "Clinics"],
    ),
    "IN-BR": RegionalProfile(
        region_code="IN-BR",
        region_name="Bihar",
        country_code="IN",
        economic_type=IndianEconomicType.REGIONAL_TRADE_SERVICE,
        baseline_no_website_percent=26.7,
        check_first=[ConditionID.W7, ConditionID.W8, ConditionID.D2, ConditionID.D11],
        trust_less=["Assuming zero commercial budget", "English-only keyword search"],
        local_sources=["BIADA"],
        local_languages=["Hindi", "English", "Bhojpuri", "Maithili"],
        target_categories=["Clinics", "Coaching Institutes", "Wholesale Distributors", "Logistics"],
    ),
    "IN-AS": RegionalProfile(
        region_code="IN-AS",
        region_name="Assam",
        country_code="IN",
        economic_type=IndianEconomicType.REGIONAL_TRADE_SERVICE,
        baseline_no_website_percent=33.1,
        check_first=[ConditionID.W7, ConditionID.W8, ConditionID.D11, ConditionID.W10, ConditionID.D9],
        trust_less=["Guwahati baseline applied to entire Northeast"],
        local_sources=["AIIDC", "Assam Tourism", "Tea Board"],
        local_languages=["Assamese", "Bengali", "English", "Hindi"],
        target_categories=["Regional Trade", "Logistics", "Clinics", "Tea Plantations & Brokers"],
    ),
    "IN-OR": RegionalProfile(
        region_code="IN-OR",
        region_name="Odisha",
        country_code="IN",
        economic_type=IndianEconomicType.MANUFACTURING_EXPORT,
        baseline_no_website_percent=23.2,
        check_first=[ConditionID.W7, ConditionID.W8, ConditionID.D11, ConditionID.D8, ConditionID.D9],
        trust_less=["Low digital listing density as proof of low purchasing ability"],
        local_sources=["IDCO", "IPICOL"],
        local_languages=["Odia", "English"],
        target_categories=["Industrial Suppliers", "Clinics", "Coaching", "Logistics", "Visitor Services"],
    ),
    "IN-GA": RegionalProfile(
        region_code="IN-GA",
        region_name="Goa",
        country_code="IN",
        economic_type=IndianEconomicType.TOURISM,
        baseline_no_website_percent=24.0,
        check_first=[ConditionID.W5, ConditionID.W8, ConditionID.W10, ConditionID.W15, ConditionID.W16, ConditionID.D12],
        trust_less=["Monsoon silence as business closure"],
        local_sources=["Goa Tourism", "Panchayat Licensing"],
        local_languages=["Konkani", "Marathi", "English"],
        target_categories=["Boutique Lodging", "Water Sports & Tours", "Rentals", "Dining"],
    ),
}


# ─── SECTION 11.6: 27 COUNTRY PROFILES ──────────────────────────

GLOBAL_COUNTRY_PROFILES: Dict[str, RegionalProfile] = {
    # Tier 1: High Coverage
    "US": RegionalProfile("US", "United States", "US", None, 18.4, [ConditionID.W5, ConditionID.W6, ConditionID.W9, ConditionID.W13], ["Rare no-site as proof of need alone"], ["SEC EDGAR", "State Reg"], ["English", "Spanish"], ["Clinics", "Home Services", "Multi-Location"]),
    "GB": RegionalProfile("GB", "United Kingdom", "GB", None, 10.6, [ConditionID.W5, ConditionID.W8, ConditionID.W9, ConditionID.W13], ["Assuming filed accounts show micro revenue"], ["Companies House", "FSA Ratings"], ["English"], ["Services", "Clinics", "Hospitality"]),
    "DE": RegionalProfile("DE", "Germany", "DE", None, 9.8, [ConditionID.W5, ConditionID.W7, ConditionID.W13, ConditionID.J1], ["English-only search", "Cold email without consent (UWG §7)"], ["Handelsregister"], ["German"], ["Professional Services", "Clinics", "Mittelstand"]),
    "CA": RegionalProfile("CA", "Canada", "CA", None, 7.1, [ConditionID.W5, ConditionID.W8, ConditionID.W9, ConditionID.W13], ["Toronto baseline as representative of all Canada"], ["Corporations Canada"], ["English", "French"], ["Services", "Clinics", "Retail"]),
    "AU": RegionalProfile("AU", "Australia", "AU", None, 9.7, [ConditionID.W5, ConditionID.W6, ConditionID.W8, ConditionID.W13], ["No Google reviews as inactivity"], ["ABN Lookup"], ["English"], ["Trades", "Services", "Clinics", "Hospitality"]),
    "JP": RegionalProfile("JP", "Japan", "JP", None, 22.3, [ConditionID.W7, ConditionID.W15, ConditionID.W16, ConditionID.C6], ["Lack of own domain as zero digital presence"], ["NTA Corporate Data", "LINE Official"], ["Japanese"], ["Appointments", "Retail", "Food", "Specialty Suppliers"]),
    "SG": RegionalProfile("SG", "Singapore", "SG", None, 27.2, [ConditionID.W5, ConditionID.W9, ConditionID.W15, ConditionID.W16, ConditionID.C6], ["Assuming every company has an enterprise web team"], ["ACRA"], ["English", "Mandarin", "Malay", "Tamil"], ["Services", "Clinics", "Regional B2B"]),
    "FR": RegionalProfile("FR", "France", "FR", None, 16.5, [ConditionID.W5, ConditionID.W7, ConditionID.W13, ConditionID.W15], ["Every directory record as a separate buying unit"], ["Sirene"], ["French"], ["Clinics", "Services", "Hospitality", "Suppliers"]),

    # Tier 2: Social and Platform-Heavy
    "IN": RegionalProfile("IN", "India", "IN", None, 24.5, [ConditionID.W7, ConditionID.D8, ConditionID.D9, ConditionID.D11, ConditionID.C6], ["Social-only or WhatsApp presence as a defect"], ["MCA", "GST", "Udyam"], ["Hindi", "English", "Regional"], ["Exporters", "Services", "Clinics", "Wholesale"]),
    "ID": RegionalProfile("ID", "Indonesia", "ID", None, 46.8, [ConditionID.W7, ConditionID.W15, ConditionID.W16, ConditionID.D11], ["Marketplace presence as proof of unmet need"], ["AHU / OSS"], ["Indonesian"], ["Food", "Retail", "Suppliers", "Services"]),
    "PH": RegionalProfile("PH", "Philippines", "PH", None, 52.9, [ConditionID.W7, ConditionID.W8, ConditionID.D11, ConditionID.C6], ["High no-site share interpreted directly as buying intent"], ["DTI / SEC"], ["Filipino", "English"], ["Services", "Retail", "Food", "Suppliers"]),
    "VN": RegionalProfile("VN", "Vietnam", "VN", None, 42.2, [ConditionID.W7, ConditionID.W15, ConditionID.D9, ConditionID.D11], ["English-only matching without Vietnamese diacritics"], ["National Registry", "Zalo Official"], ["Vietnamese"], ["Suppliers", "Retail", "Services"]),
    "NG": RegionalProfile("NG", "Nigeria", "NG", None, 35.0, [ConditionID.W7, ConditionID.W8, ConditionID.D11, ConditionID.W14], ["Filled email field as verified corporate contact"], ["CAC"], ["English"], ["Trade", "Professional Services", "Clinics", "Suppliers"]),
    "KE": RegionalProfile("KE", "Kenya", "KE", None, 33.3, [ConditionID.W7, ConditionID.W8, ConditionID.D11, ConditionID.D9], ["Treating WhatsApp ordering as lack of commerce"], ["BRS"], ["English", "Swahili"], ["Trade", "Clinics", "Hospitality", "Suppliers"]),
    "PK": RegionalProfile("PK", "Pakistan", "PK", None, 44.2, [ConditionID.W7, ConditionID.D8, ConditionID.D9, ConditionID.D11], ["Social links as independent corroboration"], ["SECP"], ["Urdu", "English"], ["Suppliers", "Wholesale", "Services"]),
    "BD": RegionalProfile("BD", "Bangladesh", "BD", None, 44.1, [ConditionID.W7, ConditionID.D8, ConditionID.D9, ConditionID.W15], ["Assuming apparel factories lack international buyer sites"], ["RJSC"], ["Bangla", "English"], ["Garments & Textiles", "Trade", "Services"]),
    "EG": RegionalProfile("EG", "Egypt", "EG", None, 44.0, [ConditionID.W7, ConditionID.W10, ConditionID.W15, ConditionID.D11], ["Arabic vs English name mismatch as absence"], ["Commercial Registry"], ["Arabic", "English"], ["Services", "Trade", "Hospitality", "Suppliers"]),
    "BR": RegionalProfile("BR", "Brazil", "BR", None, 32.7, [ConditionID.W7, ConditionID.W8, ConditionID.W15, ConditionID.D11], ["Treating WhatsApp catalog as a deficiency"], ["Receita Federal (CNPJ)"], ["Portuguese"], ["Retail", "Food", "Services", "Suppliers"]),
    "MX": RegionalProfile("MX", "Mexico", "MX", None, 44.9, [ConditionID.W7, ConditionID.W8, ConditionID.W15, ConditionID.D11], ["Assuming informal storefronts buy custom web apps"], ["DENUE Official"], ["Spanish"], ["Retail", "Food", "Clinics", "Suppliers"]),
    "TH": RegionalProfile("TH", "Thailand", "TH", None, 61.2, [ConditionID.W7, ConditionID.W10, ConditionID.W15, ConditionID.W16, ConditionID.C6], ["No domain as lack of digital presence (LINE dominant)"], ["DBD", "LINE Official"], ["Thai", "English"], ["Food", "Beauty", "Lodging", "Tours"]),

    # Tier 3: Gulf & Eurasia
    "AE": RegionalProfile("AE", "United Arab Emirates", "AE", None, 24.0, [ConditionID.W8, ConditionID.W9, ConditionID.W10, ConditionID.W15, ConditionID.W16, ConditionID.D6], ["Assuming uniformly inflated budgets"], ["DED Registry"], ["Arabic", "English"], ["Clinics", "Hospitality", "Services", "B2B"]),
    "SA": RegionalProfile("SA", "Saudi Arabia", "SA", None, 33.1, [ConditionID.W7, ConditionID.W10, ConditionID.W15, ConditionID.D11, ConditionID.J1], ["English-first digital pitches"], ["Ministry of Commerce"], ["Arabic", "English"], ["Clinics", "Retail", "Services", "Suppliers"]),
    "TR": RegionalProfile("TR", "Turkey", "TR", None, 37.7, [ConditionID.W7, ConditionID.W10, ConditionID.W15, ConditionID.D9], ["English-only search", "Dotted/dotless I matching errors"], ["MERSIS"], ["Turkish"], ["Manufacturers", "Wholesale", "Hospitality"]),
    "ZA": RegionalProfile("ZA", "South Africa", "ZA", None, 28.8, [ConditionID.W7, ConditionID.W8, ConditionID.D11], ["Low social media share as low customer demand"], ["CIPC"], ["English"], ["Home & Pro Services", "Clinics", "B2B"]),
    "KR": RegionalProfile("KR", "South Korea", "KR", None, 20.0, [ConditionID.W5, ConditionID.W7, ConditionID.W15, ConditionID.W16, ConditionID.C6], ["Treating NAVER Place / Kakao as absent presence"], ["National Tax Service"], ["Korean"], ["Appointments", "Food", "Retail", "B2B"]),
    "CN": RegionalProfile("CN", "China", "CN", None, 25.0, [ConditionID.W7, ConditionID.W15, ConditionID.W16, ConditionID.J2, ConditionID.C6], ["Assuming western web stacks work without ICP license"], ["SAMR Registry"], ["Mandarin"], ["Manufacturers", "Exporters", "Retail"]),
    "RU": RegionalProfile("RU", "Russia", "RU", None, 26.0, [ConditionID.W7, ConditionID.W15, ConditionID.W16, ConditionID.J2, ConditionID.C6], ["Ignoring domestic VK/2GIS platforms"], ["FTS Registry"], ["Russian"], ["Services", "Retail", "B2B"]),
}


class RegionalCalibrationEngine:
    """
    Manages regional priority orders, town-size sample blending, and baseline lookups.
    """

    @classmethod
    def get_profile(cls, country_code: str, region_code: Optional[str] = None) -> RegionalProfile:
        """Returns the most specific regional profile available."""
        if region_code and region_code.upper() in INDIAN_STATE_PROFILES:
            return INDIAN_STATE_PROFILES[region_code.upper()]
        cc = country_code.upper()
        if cc in GLOBAL_COUNTRY_PROFILES:
            return GLOBAL_COUNTRY_PROFILES[cc]
        # Generic fallback
        return RegionalProfile(
            region_code=cc,
            region_name=cc,
            country_code=cc,
            baseline_no_website_percent=25.0,
            check_first=[ConditionID.W1, ConditionID.W2, ConditionID.W5],
            trust_less=["Single source proxies"],
        )

    @classmethod
    def get_city_baseline(cls, city_name: str) -> Optional[CityBaseline]:
        """Looks up the measured Overture baseline for one of the 45 surveyed cities."""
        key = city_name.strip().lower()
        return OVERTURE_45_CITY_BASELINES.get(key)

    @classmethod
    def calibrate_cohort_rate(
        cls,
        local_sample_size: int,
        local_positive_count: int,
        parent_rate: float,
    ) -> float:
        """
        Calculates empirical sample size blending (Section 11.3):
        - If sample >= 200: use local rate directly
        - If 50-199: blend local with parent: weight on local = n / (n + 200)
        - If < 50: use parent cohort
        Rate formula: (local_hits + 100 * parent_rate) / (local_sample_size + 100)
        """
        if local_sample_size >= 200:
            return local_positive_count / local_sample_size
        elif local_sample_size >= 50:
            weight_local = local_sample_size / (local_sample_size + 200.0)
            local_rate = local_positive_count / local_sample_size
            return (weight_local * local_rate) + ((1.0 - weight_local) * parent_rate)
        else:
            return parent_rate

