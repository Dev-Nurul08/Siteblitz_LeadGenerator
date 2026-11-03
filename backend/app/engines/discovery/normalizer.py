"""
Business name normalization and deduplication utilities.

Handles:
- Name normalization (case, punctuation, legal suffixes)
- Category mapping from source-specific to normalized taxonomy
- Duplicate detection using name + location matching
"""

import re
import unicodedata
from typing import Optional

import structlog

logger = structlog.get_logger(__name__)

# Common business legal suffixes to strip for comparison
LEGAL_SUFFIXES = [
    r"\bllc\b", r"\bltd\b", r"\blimited\b", r"\binc\b", r"\bincorporated\b",
    r"\bcorp\b", r"\bcorporation\b", r"\bco\b", r"\bcompany\b",
    r"\bplc\b", r"\bgmbh\b", r"\bag\b", r"\bsa\b", r"\bsarl\b",
    r"\bsrl\b", r"\bbv\b", r"\bnv\b", r"\bpty\b", r"\bpvt\b",
    r"\bpte\b", r"\bs\.?a\.?\b", r"\bs\.?r\.?l\.?\b",
]

# ─── Category Normalization ──────────────────────────────────────

# Maps source-specific categories to our normalized taxonomy
CATEGORY_MAP = {
    # Food & Beverage
    "restaurant": ("Food & Beverage", "Restaurant"),
    "cafe": ("Food & Beverage", "Cafe"),
    "bar": ("Food & Beverage", "Bar"),
    "pub": ("Food & Beverage", "Pub"),
    "fast_food": ("Food & Beverage", "Fast Food"),
    "bakery": ("Food & Beverage", "Bakery"),
    "food_court": ("Food & Beverage", "Food Court"),
    "ice_cream": ("Food & Beverage", "Ice Cream Shop"),
    "coffee_shop": ("Food & Beverage", "Coffee Shop"),

    # Accommodation
    "hotel": ("Accommodation", "Hotel"),
    "motel": ("Accommodation", "Motel"),
    "hostel": ("Accommodation", "Hostel"),
    "guest_house": ("Accommodation", "Guest House"),
    "bed_and_breakfast": ("Accommodation", "B&B"),
    "resort": ("Accommodation", "Resort"),
    "apartment": ("Accommodation", "Serviced Apartment"),

    # Retail
    "shop": ("Retail", "General Shop"),
    "supermarket": ("Retail", "Supermarket"),
    "convenience": ("Retail", "Convenience Store"),
    "clothes": ("Retail", "Clothing Store"),
    "electronics": ("Retail", "Electronics Store"),
    "furniture": ("Retail", "Furniture Store"),
    "hardware": ("Retail", "Hardware Store"),
    "jewelry": ("Retail", "Jewelry Store"),
    "bookshop": ("Retail", "Book Store"),
    "florist": ("Retail", "Florist"),
    "gift": ("Retail", "Gift Shop"),
    "toys": ("Retail", "Toy Store"),
    "pet": ("Retail", "Pet Store"),
    "sports": ("Retail", "Sports Store"),
    "beauty": ("Retail", "Beauty Store"),
    "pharmacy": ("Retail", "Pharmacy"),

    # Health & Wellness
    "clinic": ("Health & Wellness", "Clinic"),
    "dentist": ("Health & Wellness", "Dental Clinic"),
    "doctors": ("Health & Wellness", "Medical Practice"),
    "hospital": ("Health & Wellness", "Hospital"),
    "veterinary": ("Health & Wellness", "Veterinary"),
    "optician": ("Health & Wellness", "Optician"),
    "physiotherapy": ("Health & Wellness", "Physiotherapy"),
    "gym": ("Health & Wellness", "Gym"),
    "spa": ("Health & Wellness", "Spa"),
    "salon": ("Health & Wellness", "Salon"),
    "hairdresser": ("Health & Wellness", "Hair Salon"),

    # Professional Services
    "lawyer": ("Professional Services", "Law Firm"),
    "accountant": ("Professional Services", "Accounting"),
    "insurance": ("Professional Services", "Insurance"),
    "estate_agent": ("Professional Services", "Real Estate"),
    "architect": ("Professional Services", "Architecture"),
    "consulting": ("Professional Services", "Consulting"),
    "marketing": ("Professional Services", "Marketing Agency"),
    "it_services": ("Professional Services", "IT Services"),

    # Automotive
    "car_repair": ("Automotive", "Auto Repair"),
    "car_dealer": ("Automotive", "Car Dealership"),
    "car_wash": ("Automotive", "Car Wash"),
    "fuel": ("Automotive", "Gas Station"),
    "car_rental": ("Automotive", "Car Rental"),

    # Education
    "school": ("Education", "School"),
    "university": ("Education", "University"),
    "college": ("Education", "College"),
    "driving_school": ("Education", "Driving School"),
    "language_school": ("Education", "Language School"),
    "music_school": ("Education", "Music School"),
    "training": ("Education", "Training Center"),

    # Construction & Trades
    "construction": ("Construction & Trades", "Construction"),
    "plumber": ("Construction & Trades", "Plumbing"),
    "electrician": ("Construction & Trades", "Electrical"),
    "painter": ("Construction & Trades", "Painting"),
    "carpenter": ("Construction & Trades", "Carpentry"),
    "landscaping": ("Construction & Trades", "Landscaping"),
    "roofing": ("Construction & Trades", "Roofing"),
    "hvac": ("Construction & Trades", "HVAC"),

    # Entertainment & Leisure
    "cinema": ("Entertainment & Leisure", "Cinema"),
    "theatre": ("Entertainment & Leisure", "Theatre"),
    "museum": ("Entertainment & Leisure", "Museum"),
    "nightclub": ("Entertainment & Leisure", "Nightclub"),
    "bowling": ("Entertainment & Leisure", "Bowling"),
    "amusement": ("Entertainment & Leisure", "Amusement"),
    "zoo": ("Entertainment & Leisure", "Zoo"),
    "aquarium": ("Entertainment & Leisure", "Aquarium"),

    # Other Services
    "cleaning": ("Other Services", "Cleaning"),
    "laundry": ("Other Services", "Laundry"),
    "locksmith": ("Other Services", "Locksmith"),
    "moving": ("Other Services", "Moving Service"),
    "printing": ("Other Services", "Printing"),
    "photography": ("Other Services", "Photography"),
    "travel_agency": ("Other Services", "Travel Agency"),
    "event_planning": ("Other Services", "Event Planning"),
}


class BusinessNormalizer:
    """
    Normalizes business data for deduplication and consistent storage.
    """

    @staticmethod
    def normalize_name(name: str) -> str:
        """
        Normalize a business name for comparison and deduplication.

        Steps:
        1. Unicode normalize (NFKD) and strip accents
        2. Lowercase
        3. Remove legal suffixes
        4. Remove punctuation
        5. Collapse whitespace
        """
        if not name:
            return ""

        # Unicode normalize
        normalized = unicodedata.normalize("NFKD", name)
        # Remove accents
        normalized = "".join(
            c for c in normalized if not unicodedata.combining(c)
        )
        # Lowercase
        normalized = normalized.lower().strip()

        # Remove legal suffixes
        for suffix_pattern in LEGAL_SUFFIXES:
            normalized = re.sub(suffix_pattern, "", normalized)

        # Remove apostrophes in contractions/possessives (e.g., Ben's -> bens, don't -> dont)
        normalized = normalized.replace("'", "")
        # Remove remaining punctuation (keep alphanumeric and spaces)
        normalized = re.sub(r"[^\w\s]", " ", normalized)

        # Collapse whitespace
        normalized = re.sub(r"\s+", " ", normalized).strip()

        return normalized

    @staticmethod
    def normalize_category(
        source_category: str,
    ) -> tuple[str, str, str]:
        """
        Map a source-specific category to normalized taxonomy.

        Returns:
            Tuple of (industry_group, normalized_category, original_source_category)
        """
        if not source_category:
            return ("Uncategorized", "Unknown", "")

        # Clean the source category
        clean = source_category.lower().strip()
        clean = clean.replace("-", "_").replace(" ", "_")

        # Look up in the map
        if clean in CATEGORY_MAP:
            industry, normalized = CATEGORY_MAP[clean]
            return (industry, normalized, source_category)

        # Try partial matching
        for key, (industry, normalized) in CATEGORY_MAP.items():
            if key in clean or clean in key:
                return (industry, normalized, source_category)

        # Unknown category — preserve original
        # Capitalize words for display
        display_name = source_category.replace("_", " ").title()
        return ("Uncategorized", display_name, source_category)

    @staticmethod
    def normalize_country_code(code: Optional[str]) -> Optional[str]:
        """Normalize country code to uppercase ISO 3166-1 alpha-2."""
        if not code:
            return None
        clean = code.strip().upper()
        if len(clean) == 2 and clean.isalpha():
            return clean
        return None

    @staticmethod
    def normalize_phone(phone: Optional[str]) -> Optional[str]:
        """Basic phone normalization — remove common formatting characters."""
        if not phone:
            return None
        # Keep digits, plus sign, and extension indicators
        cleaned = re.sub(r"[^\d+x,;]", "", phone)
        return cleaned if cleaned else None

    @staticmethod
    def normalize_website(url: Optional[str]) -> Optional[str]:
        """Normalize a website URL."""
        if not url:
            return None

        url = url.strip()

        # Skip social media and directory pages
        social_domains = [
            "facebook.com", "instagram.com", "twitter.com", "x.com",
            "linkedin.com", "tiktok.com", "youtube.com", "yelp.com",
            "tripadvisor.com", "google.com/maps",
        ]
        url_lower = url.lower()
        for domain in social_domains:
            if domain in url_lower:
                return None  # These are social profiles, not official websites

        # Add scheme if missing
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        return url

    @staticmethod
    def is_potential_duplicate(
        name1: str,
        name2: str,
        city1: Optional[str] = None,
        city2: Optional[str] = None,
        country1: Optional[str] = None,
        country2: Optional[str] = None,
        lat1: Optional[float] = None,
        lon1: Optional[float] = None,
        lat2: Optional[float] = None,
        lon2: Optional[float] = None,
    ) -> tuple[bool, float]:
        """
        Check if two business records likely represent the same entity.

        Returns:
            Tuple of (is_duplicate: bool, confidence: float)
        """
        normalizer = BusinessNormalizer

        norm_name1 = normalizer.normalize_name(name1)
        norm_name2 = normalizer.normalize_name(name2)

        if not norm_name1 or not norm_name2:
            return (False, 0.0)

        # Exact name match
        if norm_name1 == norm_name2:
            # Same name, check location
            if city1 and city2:
                if city1.lower().strip() == city2.lower().strip():
                    return (True, 0.95)
            if country1 and country2:
                if country1.upper() == country2.upper():
                    # Same country, check proximity
                    if lat1 and lon1 and lat2 and lon2:
                        distance = _haversine_distance(lat1, lon1, lat2, lon2)
                        if distance < 0.5:  # Within 500 meters
                            return (True, 0.95)
                        elif distance < 5.0:  # Within 5 km
                            return (True, 0.70)
                    return (True, 0.60)
            return (True, 0.50)  # Same name, unknown location

        # Similar name (check containment)
        if norm_name1 in norm_name2 or norm_name2 in norm_name1:
            if city1 and city2 and city1.lower().strip() == city2.lower().strip():
                return (True, 0.70)

        return (False, 0.0)


def _haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Calculate the great-circle distance between two points
    on Earth (in kilometers) using the Haversine formula.
    """
    import math

    R = 6371.0  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
