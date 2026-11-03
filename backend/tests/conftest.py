"""
Test configuration and fixtures for Phase 1 tests.
"""

import pytest


@pytest.fixture
def sample_osm_element():
    """Sample OSM element as returned by Overpass API."""
    return {
        "type": "node",
        "id": 123456789,
        "lat": 51.5074,
        "lon": -0.1278,
        "tags": {
            "name": "The Best Restaurant",
            "amenity": "restaurant",
            "cuisine": "italian",
            "addr:street": "High Street",
            "addr:housenumber": "42",
            "addr:city": "London",
            "addr:postcode": "EC1A 1BB",
            "addr:country": "GB",
            "phone": "+44 20 7123 4567",
            "website": "https://bestrestaurant.co.uk",
            "opening_hours": "Mo-Sa 11:00-23:00",
            "facebook": "https://facebook.com/bestrestaurant",
        },
    }


@pytest.fixture
def sample_osm_element_no_website():
    """OSM element with no website — key opportunity signal."""
    return {
        "type": "node",
        "id": 987654321,
        "lat": 40.7128,
        "lon": -74.0060,
        "tags": {
            "name": "Joe's Pizza",
            "amenity": "fast_food",
            "cuisine": "pizza",
            "addr:street": "Broadway",
            "addr:housenumber": "7",
            "addr:city": "New York",
            "addr:country": "US",
            "phone": "+1 212 555 0100",
            "instagram": "https://instagram.com/joespizza",
        },
    }


@pytest.fixture
def sample_csv_content():
    """Sample CSV content for import testing."""
    return """name,address,city,country,phone,email,website,category
Acme Corp,123 Main St,Springfield,US,555-0100,info@acme.com,https://acme.com,consulting
Best Bakery,456 Oak Ave,Portland,US,555-0200,hello@bestbakery.com,,bakery
City Hotel,789 Pine Rd,London,GB,+44 20 1234 5678,reservations@cityhotel.co.uk,https://cityhotel.co.uk,hotel
Empty Row,,,,,,,,
Good Plumber,321 Elm St,Sydney,AU,+61 2 9876 5432,,,plumber
"""


@pytest.fixture
def sample_csv_missing_headers():
    """CSV with non-standard headers for field mapping test."""
    return """Company Name,Street Address,Town,Country Code,Telephone,Contact Email,Homepage,Industry
Tech Solutions,100 Tech Park,Berlin,DE,+49 30 12345,info@techsolutions.de,https://techsolutions.de,it_services
"""
