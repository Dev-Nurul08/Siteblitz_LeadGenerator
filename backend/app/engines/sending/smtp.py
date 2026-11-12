"""
SMTP submission adapter (spec row 8: the app submits over SMTP to the Mailforge mailbox; smtplib, 30 s timeout).

submit() tells three outcomes apart, because they need different handling:
    ACCEPTED   the server answered 2xx to the end of DATA
    FAILED     a definite 5xx refusal (MAIL, RCPT, DATA command or end of DATA)
    NOT_SENT   nothing was accepted and it is safe to try again later: a 4xx answer, or a connection / TLS / login
               problem before the message text was sent (mailbox_problem = True for the latter)
    UNCERTAIN  the connection timed out or dropped AFTER the message text was sent and before the server's
               answer arrived. The message may have been accepted: it is NEVER retried automatically.

The mailbox password is read only here, from the environment or `.env`, as MAILBOX_<SLUG>_PASSWORD. It is never
stored in the database, never logged and never returned by the API.
"""

import os
import re
import smtplib
import ssl
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import dotenv_values

SMTP_TIMEOUT_SECONDS = 30
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}
_STATUS = re.compile(r"(?<![\d.])([245]\.\d{1,3}\.\d{1,3})(?![\d.])")

ACCEPTED, FAILED, NOT_SENT, UNCERTAIN = "ACCEPTED", "FAILED", "NOT_SENT", "UNCERTAIN"


def password_variable(slug: str) -> str:
    return f"MAILBOX_{slug.upper()}_PASSWORD"


def mailbox_password(slug: str, env_file: Optional[Path] = Path(".env")) -> Optional[str]:
    name = password_variable(slug)
    value = os.environ.get(name)
    if value is None and env_file is not None and env_file.is_file():
        value = dotenv_values(env_file).get(name)
    value = (value or "").strip()
    return value or None


@dataclass
class SmtpConfig:
    host: str
    port: int
    tls: str               # "starttls" | "ssl" | "none" (loopback test server only)
    username: str
    password: Optional[str]
    timeout: float = SMTP_TIMEOUT_SECONDS


@dataclass
class SubmitResult:
    outcome: str
    phase: str                       # where the conversation ended: connect, ehlo, starttls, auth, mail, rcpt, data,
    code: Optional[int] = None       # after_data, done
    response: Optional[str] = None
    status: Optional[str] = None     # enhanced status code from the response text, e.g. "5.1.1"
    mailbox_problem: bool = False    # connect / TLS / login trouble: pause this mailbox

    @property
    def accepted(self) -> bool:
        return self.outcome == ACCEPTED


def _text(response) -> str:
    if isinstance(response, bytes):
        return response.decode("utf-8", errors="replace")
    return str(response or "")


def _answer(code: int, response, phase: str) -> SubmitResult:
    text = _text(response)
    found = _STATUS.search(text)
    status = found.group(1) if found else None
    if 200 <= code < 300:
        return SubmitResult(ACCEPTED, phase, code, text, status)
    if 500 <= code < 600:
        return SubmitResult(FAILED, phase, code, text, status)
    if 400 <= code < 500:
        return SubmitResult(NOT_SENT, phase, code, text, status)
    # Anything else at the end of DATA is not an acceptance we can prove.
    return SubmitResult(UNCERTAIN if phase == "after_data" else NOT_SENT, phase, code, text, status)


def dot_stuff(data: bytes) -> bytes:
    """CRLF line ends, a leading '.' doubled (RFC 5321 4.5.2), then the end-of-data line."""
    data = re.sub(rb"\r\n|\r|\n", b"\r\n", data)
    data = re.sub(rb"(?m)^\.", b"..", data)
    if not data.endswith(b"\r\n"):
        data += b"\r\n"
    return data + b".\r\n"


def _drop(smtp: Optional[smtplib.SMTP]) -> None:
    """Close without QUIT: after a lost answer the server may never reply, and QUIT would wait another timeout."""
    if smtp is not None:
        try:
            smtp.close()
        except Exception:
            pass
    return None


def submit(config: SmtpConfig, envelope_from: str, recipient: str, data: bytes) -> SubmitResult:
    phase = "connect"
    smtp: Optional[smtplib.SMTP] = None
    try:
        if config.tls == "none" and config.host not in LOOPBACK_HOSTS:
            raise ValueError("TLS mode 'none' is only allowed for a loopback test server")
        if config.tls == "ssl":
            smtp = smtplib.SMTP_SSL(config.host, config.port, timeout=config.timeout,
                                    context=ssl.create_default_context())
        else:
            smtp = smtplib.SMTP(config.host, config.port, timeout=config.timeout)
        phase = "ehlo"
        smtp.ehlo()
        if config.tls == "starttls":
            phase = "starttls"
            smtp.starttls(context=ssl.create_default_context())
            smtp.ehlo()
        if config.password is not None:
            phase = "auth"
            smtp.login(config.username, config.password)
        phase = "mail"
        code, response = smtp.mail(envelope_from)
        if code != 250:
            return _answer(code, response, phase)
        phase = "rcpt"
        code, response = smtp.rcpt(recipient)
        if code not in (250, 251):
            return _answer(code, response, phase)
        phase = "data"
        code, response = smtp.docmd("DATA")
        if code != 354:
            return _answer(code, response, phase)
        # From here on the server may have the whole message: a lost answer means "unknown", never "not sent".
        phase = "after_data"
        smtp.send(dot_stuff(data))
        code, response = smtp.getreply()
        result = _answer(code, response, phase)
        result.phase = "done" if result.outcome in (ACCEPTED, FAILED) else phase
        return result
    except smtplib.SMTPResponseException as exc:
        if phase == "after_data":
            smtp = _drop(smtp)
            return SubmitResult(UNCERTAIN, phase, exc.smtp_code, _text(exc.smtp_error))
        result = _answer(exc.smtp_code, exc.smtp_error, phase)
        result.mailbox_problem = phase in ("connect", "ehlo", "starttls", "auth")
        if result.mailbox_problem and result.outcome == FAILED:
            result.outcome = NOT_SENT   # a refused login is our configuration, not the recipient's address
        return result
    except Exception as exc:   # timeouts, resets, TLS errors, DNS, refused connections
        if phase == "after_data":
            smtp = _drop(smtp)
            return SubmitResult(UNCERTAIN, phase, None, f"{type(exc).__name__}: {exc}"[:500])
        return SubmitResult(NOT_SENT, phase, None, f"{type(exc).__name__}: {exc}"[:500],
                            mailbox_problem=phase in ("connect", "ehlo", "starttls", "auth"))
    finally:
        if smtp is not None:
            try:
                smtp.quit()
            except Exception:
                try:
                    smtp.close()
                except Exception:
                    pass
