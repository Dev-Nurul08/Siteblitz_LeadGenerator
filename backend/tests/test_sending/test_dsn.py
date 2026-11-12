"""
E2 bounce / DSN parser on 13 bounce samples written for this test (Gmail-, Outlook-, Yahoo-, Postfix- and Exim-style
layouts; example domains only, no real people's data) plus one ordinary reply that is not a bounce.
"""

from pathlib import Path

import pytest

from backend.app.engines.sending import dsn

FIXTURES = Path(__file__).parent / "fixtures" / "dsn"

CASES = [
    # file, kind, status, smtp code, recipient, original Message-ID
    ("01_gmail_style_user_unknown.eml", dsn.HARD, "5.1.1", 550, "owner.one@example.com", "<aaaaaaaa-0001@send-one.example>"),
    ("02_gmail_style_dmarc_policy.eml", dsn.POLICY, "5.7.26", 550, "owner.two@example.com",
     "<aaaaaaaa-0002@send-one.example>"),
    ("03_gmail_style_mailbox_full_delayed.eml", dsn.SOFT, "4.2.2", 452, "owner.three@example.com",
     "<aaaaaaaa-0003@send-one.example>"),
    ("04_outlook_style_recipient_not_found.eml", dsn.HARD, "5.1.10", 550, "owner.four@example.org",
     "<aaaaaaaa-0004@send-one.example>"),
    ("05_outlook_style_spam_block.eml", dsn.POLICY, "5.7.1", 550, "owner.five@example.org",
     "<aaaaaaaa-0005@send-one.example>"),
    ("06_yahoo_style_user_unknown.txt", dsn.HARD, None, 554, "owner.six@example.com",
     "<aaaaaaaa-0006@send-one.example>"),
    ("07_yahoo_style_deferred.txt", dsn.SOFT, "4.7.0", 421, "owner.seven@example.com",
     "<aaaaaaaa-0007@send-one.example>"),
    ("08_postfix_user_unknown.eml", dsn.HARD, "5.1.1", 550, "owner.eight@example.org",
     "<aaaaaaaa-0008@send-one.example>"),
    ("09_postfix_null_mx.eml", dsn.HARD, "5.1.10", None, "owner.nine@example.net", "<aaaaaaaa-0009@send-one.example>"),
    ("10_postfix_delayed.eml", dsn.SOFT, "4.4.1", None, "owner.ten@example.org", "<aaaaaaaa-0010@send-one.example>"),
    ("11_exim_user_unknown.txt", dsn.HARD, "5.1.1", 550, "owner.eleven@example.com",
     "<aaaaaaaa-0011@send-one.example>"),
    ("12_exim_content_policy.txt", dsn.POLICY, "5.7.1", 550, "owner.twelve@example.com",
     "<aaaaaaaa-0012@send-one.example>"),
    ("13_generic_unknown.txt", dsn.UNKNOWN, "5.0.0", None, "owner.thirteen@example.com",
     "<aaaaaaaa-0013@send-one.example>"),
]


@pytest.mark.parametrize("name,kind,status,code,recipient,message_id", CASES, ids=[c[0] for c in CASES])
def test_bounce_samples(name, kind, status, code, recipient, message_id):
    result = dsn.parse_bounce((FIXTURES / name).read_bytes())
    assert result.is_bounce
    assert (result.kind, result.status, result.smtp_code) == (kind, status, code)
    assert result.recipient == recipient
    assert result.original_message_id == message_id


def test_there_are_at_least_twelve_samples_in_five_styles():
    names = [p.name for p in FIXTURES.iterdir()]
    assert len([n for n in names if "not_a_bounce" not in n]) >= 12
    for style in ("gmail", "outlook", "yahoo", "postfix", "exim"):
        assert any(style in n for n in names), style


def test_an_ordinary_reply_is_not_a_bounce():
    result = dsn.parse_bounce((FIXTURES / "14_not_a_bounce_reply.eml").read_bytes())
    assert result.is_bounce is False


@pytest.mark.parametrize("status,kind", [("5.1.1", dsn.HARD), ("5.1.10", dsn.HARD), ("5.1.2", dsn.HARD),
                                         ("5.7.1", dsn.POLICY), ("5.7.26", dsn.POLICY), ("4.2.2", dsn.SOFT),
                                         ("4.7.0", dsn.SOFT), ("5.2.2", dsn.UNKNOWN), ("5.4.1", dsn.UNKNOWN)])
def test_status_classes(status, kind):
    assert dsn.classify_status(status) == kind


def test_our_own_words_in_the_returned_copy_never_decide():
    raw = ("From: MAILER-DAEMON@mx.example.net\nSubject: Undelivered Mail Returned to Sender\n\n"
           "Your message could not be delivered.\n\n"
           "--- Below this line is a copy of the message.\n\nSubject: no spam, blocked words, user unknown\n")
    assert dsn.parse_bounce(raw).kind == dsn.UNKNOWN
