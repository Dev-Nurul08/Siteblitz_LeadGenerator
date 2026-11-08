"""
End-to-end API tests for the discovery → opportunity → contact → qualification → campaign
pipeline, run against a throw-away SQLite database through the real FastAPI app.

The unit tests mock every engine; these tests exist because the 2026-11-08 audit found
crashes (MissingGreenlet, 405 on unsubscribe, silent CSV data loss) that only appear when
the real routes, services and database run together. Network access is stubbed so the
tests are deterministic: website fetches, contact-page crawls and DNS lookups.
"""

import pytest
from fastapi.testclient import TestClient

import backend.app.database as database
from backend.app.config import get_settings
from backend.app.engines.enrichment.discovery import ContactDiscoveryEngine
from backend.app.engines.enrichment.verifier import EmailVerifier, VerificationResult
from backend.app.engines.opportunity.resolver import ResolutionResult, WebsiteResolver
from backend.app.models.business import WebsiteStatus
from backend.app.models.contact import EmailVerificationStatus

CSV_A = (
    "name,address,city,country,phone,email,website,category\n"
    "Shah Dental Care,12 Lake Rd,Austin,US,+1 512 555 0101,priya.shah@shahdental-test.com,"
    "https://shahdental-test.com,dentist\n"
    "Lakeview Bakery,40 Hill St,Austin,US,+1 512 555 0102,,,bakery\n"
)
CSV_B = "name,city,country,phone\nRiverside Salon,Austin,US,+1 512 555 0199\n"

HTML = (
    "<html><head><title>Shah Dental Care Austin</title></head>"
    "<body><h1>Shah Dental Care</h1><p>Call us to visit.</p></body></html>"
)


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Real app on a fresh SQLite file, with all outbound network calls stubbed."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{tmp_path / 'pipeline.db'}")
    get_settings.cache_clear()
    # The engine/session factories are module-level singletons; reset them so this test
    # binds to its own database file instead of any engine created earlier in the run.
    monkeypatch.setattr(database, "_async_engine", None)
    monkeypatch.setattr(database, "_async_session_factory", None)

    async def fake_resolve(self, url):
        return ResolutionResult(
            original_url=url,
            final_url=url,
            is_reachable=True,
            http_status=200,
            has_ssl=True,
            load_time_seconds=0.4,
            status=WebsiteStatus.FOUND,
            html_content=HTML,
            headers={},
        )

    async def fake_crawl(self, base_url):
        return []

    def fake_verify(self, email):
        return VerificationResult(
            email=email,
            status=EmailVerificationStatus.VERIFIED,
            is_valid_syntax=True,
            is_disposable=False,
            is_role_based=False,
            has_valid_mx=True,
            verification_score=0.95,
            domain=email.split("@")[-1],
            mx_records=["mx.test"],
            details={},
        )

    monkeypatch.setattr(WebsiteResolver, "resolve", fake_resolve)
    monkeypatch.setattr(ContactDiscoveryEngine, "_crawl_contact_pages", fake_crawl)
    monkeypatch.setattr(EmailVerifier, "verify", fake_verify)

    from backend.app.main import app

    with TestClient(app) as test_client:
        yield test_client
    get_settings.cache_clear()


def _import(client, name, content):
    response = client.post(
        "/api/v1/discovery/import-csv", files={"file": (name, content, "text/csv")}
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_each_csv_file_imports_its_own_rows_and_reimport_is_duplicate(client):
    first = _import(client, "a.csv", CSV_A)
    assert (first["new"], first["duplicate"]) == (2, 0)

    second = _import(client, "b.csv", CSV_B)
    assert (second["new"], second["duplicate"]) == (1, 0)

    again = _import(client, "a.csv", CSV_A)
    assert (again["new"], again["duplicate"]) == (0, 2)

    names = {b["name"] for b in client.get("/api/v1/businesses").json()["items"]}
    assert names == {"Shah Dental Care", "Lakeview Bakery", "Riverside Salon"}


def test_full_pipeline_qualify_enroll_once_and_unsubscribe_by_link(client):
    _import(client, "a.csv", CSV_A)
    items = client.get("/api/v1/businesses", params={"search": "Shah"}).json()["items"]
    business_id = items[0]["id"]

    evaluated = client.post(f"/api/v1/opportunities/evaluate-business/{business_id}")
    assert evaluated.status_code == 200, evaluated.text

    enriched = client.post(f"/api/v1/contacts/enrich-business/{business_id}")
    assert enriched.status_code == 200, enriched.text
    assert enriched.json()["contacts_count"] >= 1

    # Used to fail with HTTP 500 (MissingGreenlet) for any business with a city/category.
    qualified = client.post(f"/api/v1/qualification/qualify-business/{business_id}")
    assert qualified.status_code == 200, qualified.text
    lead = qualified.json()
    assert lead["personalized_pitch"]

    approved = client.patch(
        f"/api/v1/qualification/leads/{lead['lead_id']}/status",
        json={"status": "READY_FOR_OUTREACH"},
    )
    assert approved.status_code == 200, approved.text

    campaign = client.post("/api/v1/campaigns", json={"name": "Austin dentists"}).json()

    # Used to fail with MissingGreenlet; a second call used to duplicate every message.
    first_enroll = client.post(f"/api/v1/campaigns/{campaign['id']}/enroll")
    assert first_enroll.status_code == 200, first_enroll.text
    assert first_enroll.json()["enrolled_count"] == 1

    second_enroll = client.post(f"/api/v1/campaigns/{campaign['id']}/enroll")
    assert second_enroll.status_code == 200, second_enroll.text
    assert second_enroll.json()["enrolled_count"] == 0

    # A clicked unsubscribe link is a GET; it used to return 405 and drop the opt-out.
    unsubscribed = client.get(
        "/api/v1/qualification/unsubscribe", params={"email": lead["contact_email"]}
    )
    assert unsubscribed.status_code == 200, unsubscribed.text
    opt_outs = client.get("/api/v1/qualification/opt-outs").json()["items"]
    assert lead["contact_email"] in {o["email"] for o in opt_outs}


def test_same_name_in_different_cities_is_not_merged(client):
    # Used to merge: same normalized name + same country was enough (confidence 0.60 >= 0.50).
    csv_text = (
        "name,city,country,phone\n"
        "Sharma Sweets,Pune,IN,+91 20 1111 1111\n"
        "Sharma Sweets,Delhi,IN,+91 11 2222 2222\n"
        "Sharma Sweets,Pune,IN,+91 20 3333 3333\n"
    )
    result = _import(client, "sweets.csv", csv_text)
    # Rows 1 and 2 are different shops; row 3 is the Pune shop again with another number.
    assert (result["new"], result["duplicate"]) == (2, 1)


# ─── Input validation & sanitization (every request model / query / upload) ─────────────


def _first_business_id(client):
    _import(client, "a.csv", CSV_A)
    return client.get("/api/v1/businesses").json()["items"][0]["id"]


@pytest.mark.parametrize("payload", [
    {"website_url": "javascript:alert(1)"},
    {"website_url": "data:text/html,<script>x</script>"},
    {"email": "not-an-email"},
    {"phone": "<script>alert(1)</script>"},
    {"country_code": "IND"},
    {"name": ""},
    {"normalized_name": "hijack"},  # unknown / internal field
])
def test_business_update_rejects_bad_input(client, payload):
    business_id = _first_business_id(client)
    response = client.patch(f"/api/v1/businesses/{business_id}", json=payload)
    assert response.status_code == 422, response.text


def test_business_update_sanitizes_text(client):
    business_id = _first_business_id(client)
    response = client.patch(
        f"/api/v1/businesses/{business_id}",
        json={"name": "  Shah\x00 Dental\x07  ", "email": " Info@ShahDental-Test.com ",
              "website_url": "shahdental-test.com", "country_code": "in", "phone": ""},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == "Shah Dental"
    assert body["email"] == "info@shahdental-test.com"
    assert body["website_url"] == "https://shahdental-test.com"
    assert body["country_code"] == "IN"
    assert body["phone"] is None


@pytest.mark.parametrize("payload", [
    {"source_slug": "openstreetmap", "city": "Pune", "query_params": {"sparql": "SELECT *"}},
    {"source_slug": "openstreetmap", "city": "Pune", "query_params": {"csv_content": "a,b"}},
    {"source_slug": "overture", "city": "Pune", "query_params": {"min_confidence": 3}},
    {"source_slug": "csv_import", "query_params": {}},
    {"source_slug": "openstreetmap", "latitude": 18.5},
    {"source_slug": "openstreetmap", "country_code": "india", "city": "Pune"},
    {"source_slug": "../../etc", "city": "Pune"},
    {"source_slug": "openstreetmap", "city": "Pune", "max_results": 0},
    {"source_slug": "openstreetmap", "city": "Pune", "unexpected": 1},
])
def test_discovery_run_rejects_bad_input(client, payload):
    assert client.post("/api/v1/discovery/run", json=payload).status_code == 422


def test_source_create_only_accepts_built_in_adapters(client):
    response = client.post("/api/v1/sources", json={
        "name": "Evil", "slug": "evil", "license_type": "OPEN_LICENSE",
        "adapter_class": "os.system",
    })
    assert response.status_code == 422


def test_csv_upload_guards(client):
    bad_delimiter = client.post("/api/v1/discovery/import-csv", data={"delimiter": "xx"},
                                files={"file": ("a.csv", CSV_A, "text/csv")})
    assert bad_delimiter.status_code == 422
    not_utf8 = client.post("/api/v1/discovery/import-csv",
                           files={"file": ("a.csv", "name\nCaf\xe9".encode("latin-1"), "text/csv")})
    assert not_utf8.status_code == 400
    wrong_type = client.post("/api/v1/discovery/import-csv",
                             files={"file": ("a.exe", b"MZ", "application/octet-stream")})
    assert wrong_type.status_code == 400


def test_csv_import_keeps_more_than_500_rows(client):
    rows = "\n".join(f"Shop {i},Austin,US,+1 512 555 {i:04d}" for i in range(600))
    result = _import(client, "big.csv", "name,city,country,phone\n" + rows + "\n")
    assert result["new"] == 600  # used to stop silently at 500


@pytest.mark.parametrize("method,url,kwargs", [
    ("get", "/api/v1/businesses?country=IND", {}),
    ("get", "/api/v1/opportunities?country=12", {}),
    ("get", "/api/v1/qualification/unsubscribe?email=not-an-email", {}),
    ("get", "/api/v1/discovery/jobs?limit=100000", {}),
    ("patch", "/api/v1/opportunities/1", {"json": {"score": 150}}),
    ("post", "/api/v1/qualification/opt-outs", {"json": {"email": "nope"}}),
    ("post", "/api/v1/campaigns", {"json": {"name": "x" * 300}}),
    ("post", "/api/v1/campaigns", {"json": {"name": "Pune", "target_service_category": "SPAM"}}),
    ("patch", "/api/v1/campaigns/pipeline/crm/1", {"json": {"stage": "WON", "estimated_value": -5}}),
])
def test_other_endpoints_reject_bad_input(client, method, url, kwargs):
    assert getattr(client, method)(url, **kwargs).status_code == 422
