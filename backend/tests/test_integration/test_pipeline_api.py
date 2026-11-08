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


# ─── Export CSV / PDF ───────────────────────────────────────────────────────────────────


def test_export_csv_has_all_rows_and_neutralises_formulas(client):
    _import(client, "a.csv", CSV_A + '"=HYPERLINK(""http://evil"")",Austin,US,,,,bakery\n')
    response = client.get("/api/v1/businesses/export", params={"format": "csv"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "attachment;" in response.headers["content-disposition"]
    text = response.content.decode("utf-8-sig")
    lines = text.strip().splitlines()
    assert lines[0].startswith("id,name,category")
    assert len(lines) == 1 + 3
    assert "'=HYPERLINK" in text           # formula neutralised
    assert "'+15125550101" in text         # phone kept as text, not a number/formula


def test_export_pdf_and_job_filter(client):
    first = _import(client, "a.csv", CSV_A)
    _import(client, "b.csv", CSV_B)
    by_job = client.get("/api/v1/businesses", params={"job_id": first["job_id"]}).json()
    assert {b["name"] for b in by_job["items"]} == {"Shah Dental Care", "Lakeview Bakery"}

    pdf = client.get("/api/v1/businesses/export", params={"format": "pdf", "job_id": first["job_id"]})
    assert pdf.status_code == 200
    assert pdf.headers["content-type"] == "application/pdf"
    assert pdf.content.startswith(b"%PDF")
    assert f"-job{first['job_id']}-" in pdf.headers["content-disposition"]

    assert client.get("/api/v1/businesses/export", params={"format": "xlsx"}).status_code == 422


# ─── Website Intelligence (phase 2) through the real API ─────────────────────────────────


@pytest.fixture
def no_guessed_domains(monkeypatch):
    """Every guessed domain is unregistered (no DNS) — deterministic, no network."""
    from backend.app.engines.intelligence import checks as net

    async def never(host):
        return False

    monkeypatch.setattr(net, "_resolves", never)


def _id(client, name):
    return client.get("/api/v1/businesses", params={"search": name}).json()["items"][0]["id"]


def test_intelligence_flow_to_hot_and_label(client, no_guessed_domains):
    _import(client, "a.csv", CSV_A)
    _import(client, "c.csv", "name,city,country,phone,category\n"
                             "Glow Salon,Austin,US,+1 512 555 0177,hairdresser\n")
    salon = _id(client, "Glow")
    clinic = _id(client, "Shah Dental")

    batch = client.post("/api/v1/intelligence/assess-batch").json()
    assert batch["assessed"] == 3 and batch["remaining_unassessed"] == 0

    own = client.get(f"/api/v1/intelligence/business/{clinic}").json()["assessment"]
    assert own["website_verdict"] == "OWN_SITE_VERIFIED"

    first = client.get(f"/api/v1/intelligence/business/{salon}").json()
    assert first["assessment"]["website_verdict"] == "NO_SITE_VERIFIED"
    assert first["assessment"]["evidence_confidence"] == "MEDIUM"
    assert first["assessment"]["tier"] != "HOT"  # no search recorded yet
    assert "Record a search for its name + city" in first["assessment"]["next_actions"]
    assert any(c["type"] == "DOMAIN_GUESS" for c in first["checks"])

    client.post(f"/api/v1/intelligence/business/{salon}/manual-search", json={"note": "Google: nothing"})
    hot = client.post(f"/api/v1/intelligence/business/{salon}/activity",
                      json={"active": True, "method": "call"}).json()["assessment"]
    assert hot["tier"] == "HOT" and hot["need_score"] == 80
    assert all(r["points"] > 0 for r in hot["reasons"])

    leads = client.get("/api/v1/intelligence/leads", params={"tier": "HOT"}).json()
    assert [i["name"] for i in leads["items"]] == ["Glow Salon"]
    assert leads["tier_counts"]["HOT"] == 1

    assert client.post(f"/api/v1/intelligence/business/{salon}/label",
                       json={"label": "WRONG"}).status_code == 422
    labeled = client.post(f"/api/v1/intelligence/business/{salon}/label",
                          json={"label": "CORRECT"}).json()["assessment"]
    assert labeled["label"] == "CORRECT"
    assert client.get("/api/v1/intelligence/stats").json()["labeled"] == 1


def test_found_website_disqualifies_new_website_opportunity(client, no_guessed_domains):
    _import(client, "a.csv", CSV_A)
    bakery = _id(client, "Lakeview")
    opps = client.post(f"/api/v1/opportunities/evaluate-business/{bakery}").json()["opportunities"]
    assert any(o["service_category"] == "NEW_WEBSITE" for o in opps)

    result = client.post(f"/api/v1/intelligence/business/{bakery}/manual-search",
                         json={"found_url": "lakeviewbakery-test.com"})
    assert result.json()["assessment"]["website_verdict"] == "OWN_SITE_VERIFIED"
    statuses = {o["service_category"]: o["status"] for o in
                client.get("/api/v1/opportunities").json()["items"] if o["business_id"] == bakery}
    assert statuses["NEW_WEBSITE"] == "DISQUALIFIED"


def test_points_endpoint_and_job_fields(client):
    first = _import(client, "a.csv", CSV_A)
    jobs = client.get("/api/v1/discovery/jobs").json()
    assert jobs[0]["job_id"] == first["job_id"] and "city" in jobs[0] and "category" in jobs[0]
    points = client.get("/api/v1/businesses/points", params={"job_id": first["job_id"]}).json()
    assert points["total"] == 2  # CSV rows have no coordinates, so no map points
    assert points["points"] == []


def test_contact_log_do_not_contact_blocks_readiness(client, no_guessed_domains):
    _import(client, "b.csv", CSV_B)
    salon = _id(client, "Riverside")
    client.post(f"/api/v1/intelligence/assess/{salon}")
    logged = client.post(f"/api/v1/intelligence/business/{salon}/contact-log",
                         json={"channel": "phone", "outcome": "do_not_contact", "note": "asked us not to call"})
    assert logged.status_code == 200
    body = logged.json()
    assert body["contact_log"][0]["outcome"] == "do_not_contact"
    assert body["assessment"]["outreach_readiness"] == "BLOCKED"
    assert client.post(f"/api/v1/intelligence/business/{salon}/contact-log",
                       json={"channel": "fax", "outcome": "other"}).status_code == 422


def test_same_phone_same_city_is_one_business_even_with_another_name(client):
    csv_text = (
        "name,city,country,phone\n"
        "Cafe Nirvana,Udaipur,IN,+91 76652 95252\n"
        "Nirvana Cafe & Lounge,Udaipur,IN,076652 95252\n"   # same number, other spelling
        "Cafe Nirvana,Jaipur,IN,+91 76652 95252\n"          # same number, other city: kept
    )
    result = _import(client, "phones.csv", csv_text)
    assert (result["new"], result["duplicate"]) == (2, 1)


def test_one_bad_record_does_not_fail_the_job(client, monkeypatch):
    from backend.app.services.discovery_service import DiscoveryService

    original = DiscoveryService._create_business

    async def flaky(self, discovered, source_record):
        if discovered.name == "Broken Row":
            raise RuntimeError("simulated bad record")
        return await original(self, discovered, source_record)

    monkeypatch.setattr(DiscoveryService, "_create_business", flaky)
    csv_text = "name,city,country\nGood One,Pune,IN\nBroken Row,Pune,IN\nGood Two,Pune,IN\n"
    result = _import(client, "flaky.csv", csv_text)
    assert result["status"] in ("COMPLETED", "PARTIAL")
    assert (result["new"], result["errors"]) == (2, 1)
    names = {b["name"] for b in client.get("/api/v1/businesses").json()["items"]}
    assert names == {"Good One", "Good Two"}


def test_duplicate_categories_on_one_record_are_merged(client, monkeypatch):
    from backend.app.engines.discovery.csv_import import CSVImportAdapter
    from backend.app.engines.discovery.base import AdapterResult, DiscoveredBusiness

    async def two_clinic_tags(self, **kw):
        return AdapterResult(businesses=[DiscoveredBusiness(
            source_external_id="csv:row:x1", name="Care Clinic", city="Pune", country_code="IN",
            categories=["clinic", "clinic"], source_categories=["amenity:clinic", "healthcare:clinic"])])

    monkeypatch.setattr(CSVImportAdapter, "discover", two_clinic_tags)
    result = _import(client, "x.csv", "name\nignored\n")
    assert (result["new"], result["errors"]) == (1, 0)


def test_dead_listed_domain_is_explained_and_can_be_rechecked(client, monkeypatch, no_guessed_domains):
    async def dead(self, url):
        return ResolutionResult(original_url=url, is_reachable=False, status=WebsiteStatus.BROKEN,
                                error_message="Could not establish connection to host")

    monkeypatch.setattr(WebsiteResolver, "resolve", dead)
    _import(client, "a.csv", CSV_A)  # Shah Dental lists https://shahdental-test.com
    clinic = _id(client, "Shah Dental")
    first = client.post(f"/api/v1/intelligence/assess/{clinic}").json()
    assert first["assessment"]["website_verdict"] == "UNKNOWN"  # one failure: wait for a 2nd ≥ 6 h later
    fetch = [c for c in first["checks"] if c["type"] == "SITE_FETCH"][0]
    assert "no DNS record" in fetch["detail"]["note"]

    again = client.post("/api/v1/intelligence/assess-batch", params={"recheck": "UNKNOWN"}).json()
    assert again["assessed"] == 1
    detail = client.get(f"/api/v1/intelligence/business/{clinic}").json()
    assert len([c for c in detail["checks"] if c["type"] == "SITE_FETCH"]) == 2


def test_same_email_same_city_is_one_business(client):
    csv_text = (
        "name,city,country,email\n"
        "Cosmo Dentist,Delhi,IN,Cosmodontist@gmail.com\n"
        "Dr Gupta Cosmo Dental Clinic,Delhi,IN,cosmodontist@gmail.com\n"
    )
    result = _import(client, "emails.csv", csv_text)
    assert (result["new"], result["duplicate"]) == (1, 1)


def test_shared_head_office_email_does_not_merge_two_branches(client):
    csv_text = (
        "name,city,country,email\n"
        "Clove Dental Andheri,Mumbai,IN,care@chain-test.in\n"
        "Clove Dental Bandra,Mumbai,IN,care@chain-test.in\n"   # same chain e-mail, different branch
        "Sunrise Orthodontics,Mumbai,IN,care@chain-test.in\n"  # no shared distinctive word -> separate
    )
    result = _import(client, "branches.csv", csv_text)
    # Andheri / Bandra branches differ by a distinctive word each -> kept apart; the third shares none.
    assert (result["new"], result["duplicate"]) == (3, 0)
