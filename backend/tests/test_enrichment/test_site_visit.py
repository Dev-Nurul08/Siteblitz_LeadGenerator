"""
Phase 14 email finder building blocks (QA-040): robots.txt, fetch limits, own-site emails only.

A local HTTP server stands in for business websites; the SSRF guard is switched off only for
that loopback server. No external host is contacted.
"""

import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from backend.app.engines.enrichment import site_visit
from backend.app.engines.enrichment.discovery import ContactDiscoveryEngine
from backend.app.engines.enrichment.site_visit import MAX_BYTES, RobotsRules, fetch, new_client, visit_site

HTML = {"Content-Type": "text/html; charset=utf-8"}
TEXT = {"Content-Type": "text/plain"}
ROBOTS_OPEN = (200, TEXT, b"User-agent: *\nDisallow:\n")


class _Handler(BaseHTTPRequestHandler):
    routes: dict = {}
    hits: list = []

    def log_message(self, *args):
        pass

    def do_GET(self):
        self.hits.append(self.path)
        status, headers, body = self.routes.get(self.path, (404, HTML, b"<html>not found</html>"))
        if callable(body):
            body = body()
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (ConnectionError, OSError):
            pass   # the client stopped reading (2 MB limit)


@pytest.fixture
def serve(monkeypatch):
    async def no_guard(request):
        return None

    monkeypatch.setattr(site_visit, "ensure_public_destination", no_guard)
    servers = []

    def start(routes: dict):
        handler = type("Site", (_Handler,), {"routes": routes, "hits": []})
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        servers.append(server)
        return f"127.0.0.1:{server.server_address[1]}", handler.hits

    yield start
    for server in servers:
        server.shutdown()
        server.server_close()


def extract():
    return ContactDiscoveryEngine()._extract_from_html


# ---------- robots.txt (RFC 9309) ----------

def test_robots_wildcard_and_longest_match():
    rules = RobotsRules.parse("User-agent: *\nDisallow: /*\nAllow: /contact$\n")
    assert not rules.can_fetch("https://shop.in/")
    assert rules.can_fetch("https://shop.in/contact")
    assert not rules.can_fetch("https://shop.in/contact-us")
    tie = RobotsRules.parse("User-agent: *\nDisallow: /about\nAllow: /about\n")
    assert tie.can_fetch("https://shop.in/about")


def test_robots_own_group_replaces_star_group():
    text = "User-agent: *\nDisallow: /\n\nUser-agent: SiteBlitzEnricher\nDisallow: /private\n"
    rules = RobotsRules.parse(text)
    assert rules.can_fetch("https://shop.in/contact")
    assert not rules.can_fetch("https://shop.in/private/x")
    assert RobotsRules.parse("User-agent: *\nDisallow:\n").can_fetch("https://shop.in/")


async def test_robots_disallow_all_means_no_page_is_requested(serve):
    host, hits = serve({"/robots.txt": (200, TEXT, b"User-agent: *\nDisallow: /\n"),
                        "/contact": (200, HTML, b'<a href="mailto:owner@shop.in">mail</a>')})
    visit = await visit_site(f"http://{host}", extract())
    assert visit.outcome == "robots_blocked"
    assert hits == ["/robots.txt"]
    assert visit.contacts == []


async def test_robots_5xx_is_treated_as_disallow_404_as_allow(serve):
    host, hits = serve({"/robots.txt": (503, TEXT, b"busy")})
    visit = await visit_site(f"http://{host}", extract())
    assert (visit.outcome, visit.robots) == ("robots_blocked", "unavailable")
    host, _ = serve({"/": (200, HTML, b"<html><body>Hi</body></html>")})
    visit = await visit_site(f"http://{host}", extract())
    assert (visit.outcome, visit.robots) == ("ok", "none")


# ---------- fetch limits (website-intelligence spec row 6) ----------

async def test_body_read_stops_at_2_mb(serve):
    host, _ = serve({"/big": (200, HTML, b"<html>" + b"a" * (6 * 1024 * 1024) + b"</html>")})
    async with new_client() as client:
        page = await fetch(client, f"http://{host}/big")
    assert page.truncated and len(page.body.encode()) <= MAX_BYTES


async def test_more_than_5_redirects_is_an_error(serve):
    routes = {f"/r/{n}": (302, {"Location": f"/r/{n - 1}"}, b"") for n in range(1, 13)}
    routes["/r/0"] = (200, HTML, b"<html>end</html>")
    host, _ = serve(routes)
    async with new_client() as client:
        assert (await fetch(client, f"http://{host}/r/5")).status == 200
        assert (await fetch(client, f"http://{host}/r/12")).error == "too_many_redirects"


async def test_slow_page_times_out(serve):
    def slow():
        time.sleep(2)
        return b"<html>late</html>"
    host, _ = serve({"/slow": (200, HTML, slow)})
    async with new_client() as client:
        assert (await fetch(client, f"http://{host}/slow", timeout=0.5)).error == "timeout"


# ---------- emails: own pages, visible only ----------

async def test_contact_page_keeps_only_the_published_address(serve):
    contact = (b'<html><body><form><input type="email" placeholder="you@example.com"></form>'
               b'<script>Sentry.init({dsn:"https://0a1b2c3d@o4501234.ingest.sentry.io/4505678"});'
               b'var x="dev@agency.in";</script><!-- old: rahul.dev@oldagency.in -->'
               b'<p>Write to <a href="mailto:owner@glowstudio.in?subject=Hi">us</a></p></body></html>')
    host, hits = serve({"/robots.txt": ROBOTS_OPEN,
                        "/": (200, HTML, b'<html><head><meta name="viewport" content="width=device-width">'
                                         b'</head><body>Glow Studio</body></html>'),
                        "/contact": (200, HTML, contact)})
    visit = await visit_site(f"http://{host}", extract())
    assert [(c.email, c.source_method) for c in visit.contacts] == [("owner@glowstudio.in", "mailto")]
    assert visit.contacts[0].source_url == f"http://{host}/contact"
    assert (visit.outcome, visit.has_viewport, visit.has_https) == ("ok", True, False)
    assert hits == ["/robots.txt", "/", "/contact"]   # stops at the first page with an email


async def test_homepage_email_stops_the_visit_and_counts_requests(serve):
    host, hits = serve({"/robots.txt": ROBOTS_OPEN,
                        "/": (200, HTML, b"<html><body>Call or mail info@sharmaclasses.in</body></html>")})
    visit = await visit_site(host, extract())   # no scheme: https first, then plain HTTP
    assert [c.email for c in visit.contacts] == ["info@sharmaclasses.in"]
    assert visit.has_https is False and visit.has_viewport is False
    assert hits == ["/robots.txt", "/"]


async def test_down_site_and_robots_disallowed_contact_path(serve):
    host, _ = serve({"/robots.txt": ROBOTS_OPEN, "/": (500, HTML, b"error")})
    visit = await visit_site(f"http://{host}", extract())
    assert (visit.outcome, visit.note) == ("failed", "HTTP 500")
    host, hits = serve({"/robots.txt": (200, TEXT, b"User-agent: *\nDisallow: /contact\n"),
                        "/": (200, HTML, b"<html><body>No email here</body></html>")})
    visit = await visit_site(f"http://{host}", extract())
    # "Disallow: /contact" is a prefix rule, so /contact-us and /contactus are disallowed too
    assert hits == ["/robots.txt", "/", "/about"]
    assert visit.requests == 3


def test_cloudflare_link_and_obfuscated_text_are_read_scripts_are_not():
    # 'hello@acme.com' XOR 0x12 (same vector as test_phase3_deep)
    html = ('<html><body><a href="/cdn-cgi/l/email-protection#127a777e7e7d5273717f773c717d7f">mail</a>'
            '<p>sales [at] acme [dot] in</p><textarea>name@company.com</textarea></body></html>')
    found = [(c.email, c.source_method) for c in extract()(html, "https://acme.com/contact")]
    assert found == [("hello@acme.com", "cloudflare_decode"), ("sales@acme.in", "visible_text_obfuscated")]


async def test_listing_social_and_empty_addresses_are_not_fetched():
    assert (await visit_site("https://sites.google.com/view/shop", extract())).outcome == "listing"
    assert (await visit_site("https://instagram.com/shop", extract())).outcome == "social"
    for empty in ("", "https://", "   "):
        visit = await visit_site(empty, extract())
        assert (visit.outcome, visit.requests) == ("no_address", 0)


# ---------- email engine v2 E1: a block / challenge page is never "down"; homepage-only recheck ----------

async def test_challenge_page_is_protected_not_down(serve):
    challenge = b"<html><head><title>Just a moment...</title></head><body>cf-browser-verification</body></html>"
    for status in (503, 200):
        host, _ = serve({"/robots.txt": ROBOTS_OPEN, "/": (status, HTML, challenge)})
        visit = await visit_site(f"http://{host}", extract())
        assert visit.outcome == "protected", status
        assert "challenge" in visit.note.lower()
    # a plain server error is still a failed check
    host, _ = serve({"/robots.txt": ROBOTS_OPEN, "/": (503, HTML, b"<html>Service unavailable</html>")})
    assert (await visit_site(f"http://{host}", extract())).outcome == "failed"
    # a normal page with a reCAPTCHA form is a normal page
    host, _ = serve({"/robots.txt": ROBOTS_OPEN,
                     "/": (200, HTML, b'<html><body><form><div class="g-recaptcha">captcha</div></form></body></html>')})
    assert (await visit_site(f"http://{host}", extract())).outcome == "ok"


async def test_homepage_only_check_reads_no_contact_pages(serve):
    host, hits = serve({"/robots.txt": ROBOTS_OPEN, "/": (200, HTML, b"<html><body>Hi</body></html>"),
                        "/contact": (200, HTML, b'<a href="mailto:owner@shop.in">mail</a>')})
    visit = await visit_site(f"http://{host}", extract(), contact_pages=False)
    assert visit.outcome == "ok" and visit.has_viewport is False
    assert hits == ["/robots.txt", "/"]
    assert visit.contacts == []
