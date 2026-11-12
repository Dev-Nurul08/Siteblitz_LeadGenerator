"""E2: the unsubscribe token equals the contract's algorithm (known-answer vector from the website repo)."""

import pytest

from backend.app.engines.sending import tokens

KAT_EMAIL = "  Owner@Example.com "
KAT_HASH = "c8cd3c6427301eaf6665bccacd65ddb614527acc843a15463e3faba57124c351"
KAT_SECRET = "kat-secret-not-for-production-0123456789"
KAT_PAYLOAD = '{"h":"c8cd3c6427301eaf6665bccacd65ddb614527acc843a15463e3faba57124c351","m":"send-0001","v":1}'
KAT_TOKEN = ("eyJoIjoiYzhjZDNjNjQyNzMwMWVhZjY2NjViY2NhY2Q2NWRkYjYxNDUyN2FjYzg0M2ExNTQ2M2UzZmFiYTU3MTI0YzM1MSIsIm0iOiJ"
             "zZW5kLTAwMDEiLCJ2IjoxfQ.CyQyXv0246O-c9S4tTeSF4c3xo-pCWu4M_Uj6ituq3Y")


def test_known_answer_vector():
    assert tokens.email_hash(KAT_EMAIL) == KAT_HASH
    assert tokens.payload_text(KAT_HASH, "send-0001") == KAT_PAYLOAD
    assert tokens.make_token(KAT_HASH, "send-0001", KAT_SECRET) == KAT_TOKEN
    assert tokens.token_for_email(KAT_EMAIL, "send-0001", KAT_SECRET) == KAT_TOKEN


def test_secret_is_trimmed_and_padding_is_never_used():
    assert tokens.make_token(KAT_HASH, "send-0001", f"  {KAT_SECRET}\n") == KAT_TOKEN
    assert "=" not in KAT_TOKEN
    assert tokens.verify_token(KAT_TOKEN, KAT_SECRET) == {"h": KAT_HASH, "m": "send-0001", "v": 1}
    assert tokens.verify_token(KAT_TOKEN, KAT_SECRET.replace("k", "K", 1)) is None
    assert tokens.verify_token(KAT_TOKEN[:-2] + "AA", KAT_SECRET) is None


@pytest.mark.parametrize("secret", [None, "", "   ", "x" * 31, " " + "y" * 31 + " "])
def test_short_or_missing_secret_counts_as_missing(secret):
    with pytest.raises(tokens.MissingSecret):
        tokens.make_token(KAT_HASH, "1", secret)


def test_unsubscribe_url_has_no_trailing_slash():
    assert tokens.unsubscribe_url("https://siteblitz.example/", "abc.def") == "https://siteblitz.example/u/abc.def"
