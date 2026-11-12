"""E2 message builder details and the suppression client's refusal to guess (httpx MockTransport, no network)."""

from datetime import datetime, timezone

import httpx
import pytest

from backend.app.engines.sending.message import body_with_unsubscribe, build_message, reply_subject
from backend.app.engines.sending.suppression_client import SuppressionClient, SuppressionUnavailable
from backend.app.engines.sending.tokens import email_hash

from .conftest import BASE, CONFIG, SECRET

H1, H2 = email_hash("a@example.org"), email_hash("b@example.org")


def test_body_gets_exactly_one_unsubscribe_line_at_the_end():
    url = f"{BASE}/u/t.s"
    body = body_with_unsubscribe('Hello\r\n\r\nReply "stop" or unsubscribe here: [unsubscribe URL]\n\n', url)
    assert body == f'Hello\n\nReply "stop" or unsubscribe here: {url}\n'
    assert body_with_unsubscribe("Hello", url).count("unsubscribe here") == 1


def test_reply_subject_is_not_doubled():
    assert reply_subject("Glow Hair: a note") == "Re: Glow Hair: a note"
    assert reply_subject("Re: Glow Hair: a note") == "Re: Glow Hair: a note"


def test_non_ascii_subject_and_name_are_encoded_and_nothing_but_text_is_attached():
    out = build_message(mailbox_address="test.founder@send-one.example", display_name="Test Fóunder",
                        recipient="info@example.org", subject="Shree Ganesh Sarees: ₹ prices online?",
                        body="Hello", message_id="<m1@send-one.example>", send_record_id="7", base_url=BASE,
                        signing_secret=SECRET, date=datetime(2026, 11, 17, 3, 30, tzinfo=timezone.utc))
    raw = out.as_bytes()
    raw.decode("ascii")                                    # 7-bit on the wire (encoded words + quoted-printable)
    assert out.message.get_content_type() == "text/plain" and not out.message.is_multipart()
    assert len(list(out.message.iter_attachments())) == 0
    assert out.unsubscribe_url == f"{BASE}/u/{out.token}"


def client_for(handler):
    return SuppressionClient(BASE, CONFIG.api_key, transport=httpx.MockTransport(handler))


async def test_check_returns_only_what_was_asked_and_refuses_anything_odd():
    def ok(request):
        assert request.headers["authorization"] == f"Bearer {CONFIG.api_key}"
        return httpx.Response(200, json={"ok": True, "suppressed": [H1], "checked_at": "x"})
    assert await client_for(ok).check([H1, H2]) == {H1}
    assert await client_for(ok).check([]) == set()

    def extra(request):
        return httpx.Response(200, json={"ok": True, "suppressed": [H1, "f" * 64]})
    with pytest.raises(SuppressionUnavailable):
        await client_for(extra).check([H1])

    def no_list(request):
        return httpx.Response(200, json={"ok": True})
    with pytest.raises(SuppressionUnavailable):
        await client_for(no_list).check([H1])

    def redirect(request):
        return httpx.Response(308, headers={"location": f"{BASE}/elsewhere"})
    with pytest.raises(SuppressionUnavailable):
        await client_for(redirect).check([H1])

    with pytest.raises(SuppressionUnavailable):
        await SuppressionClient(None, CONFIG.api_key).check([H1])      # not configured: never "not suppressed"
    with pytest.raises(ValueError):
        await client_for(ok).check(["not-a-hash"])
    with pytest.raises(ValueError):
        await client_for(ok).check([email_hash(f"{i}@example.org") for i in range(501)])


async def test_add_needs_a_confirmed_write():
    def unconfirmed(request):
        return httpx.Response(200, json={})
    with pytest.raises(SuppressionUnavailable):
        await client_for(unconfirmed).add(H1, "hard_bounce", "smtp")
    with pytest.raises(ValueError):
        await client_for(unconfirmed).add(H1, "unsubscribe_link", "smtp")   # the website sets that reason itself
