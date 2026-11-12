"""
IMAP reading for the reply loop (spec rows 8 and 14: the app reads the Mailforge mailboxes over IMAP).

`connect()` opens imaplib over SSL (port 993) or STARTTLS; plain IMAP only for a loopback test server, like SMTP.
The password is MAILBOX_<SLUG>_PASSWORD from the environment / .env (the same variable the SMTP adapter reads); it is
never stored, logged or returned.

`InboxReader` wraps an imaplib-like connection (tests pass a fake with the same methods and answer shapes):
    folders()            INBOX and the junk / spam folder(s) (a "stop" reply the provider filed as spam still counts)
    open(folder)         SELECT read-only (no \\Seen flag is set) + STATUS -> UIDVALIDITY
    uids_after(n)        UID SEARCH UID n+1:*  (the server may return the last UID even if it is <= n: filtered)
    uids_since(day)      UID SEARCH SINCE dd-Mon-yyyy (first read of a folder, or after UIDVALIDITY changed)
    fetch(uid)           UID FETCH (RFC822.SIZE BODY.PEEK[]<0.MAX>): at most MAX bytes of one message
"""

import imaplib
import re
import ssl
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable

from backend.app.engines.sending.smtp import LOOPBACK_HOSTS

IMAP_TIMEOUT_SECONDS = 30
MAX_FETCH_BYTES = 1_048_576   # a reply is small; a big attachment is cut (the text part comes first)
JUNK_NAMES = {"junk", "spam", "junk e-mail", "junk email", "bulk mail", "[gmail]/spam", "inbox.junk", "inbox.spam",
              "inbox/junk", "inbox/spam"}
_LIST_LINE = re.compile(rb'^\((?P<flags>[^)]*)\)\s+(?P<delim>"(?:[^"\\]|\\.)*"|NIL)\s+(?P<name>.+)$')
_UIDVALIDITY = re.compile(rb"UIDVALIDITY\s+(\d+)", re.IGNORECASE)
_SIZE = re.compile(rb"RFC822\.SIZE\s+(\d+)", re.IGNORECASE)
_UID = re.compile(rb"\bUID\s+(\d+)", re.IGNORECASE)
_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


class ImapError(RuntimeError):
    """The mailbox could not be read completely. The reconcile for that mailbox counts as failed."""


@dataclass
class FetchedMessage:
    folder: str
    uid: int
    uidvalidity: int
    size: int
    raw: bytes


def quote(name: str) -> str:
    return '"' + name.replace("\\", "\\\\").replace('"', '\\"') + '"'


def imap_date(day: date) -> str:
    return f"{day.day:02d}-{_MONTHS[day.month - 1]}-{day.year}"


def connect(host: str, port: int, tls: str, timeout: float = IMAP_TIMEOUT_SECONDS) -> Any:
    if tls == "ssl":
        return imaplib.IMAP4_SSL(host, port, ssl_context=ssl.create_default_context(), timeout=timeout)
    if tls == "starttls":
        conn = imaplib.IMAP4(host, port, timeout=timeout)
        conn.starttls(ssl_context=ssl.create_default_context())
        return conn
    if tls == "none" and host in LOOPBACK_HOSTS:
        return imaplib.IMAP4(host, port, timeout=timeout)
    raise ImapError("plain IMAP is only allowed for a loopback test server")


def _ok(answer, what: str):
    try:
        typ, data = answer
    except (TypeError, ValueError) as exc:
        raise ImapError(f"{what}: unexpected answer") from exc
    if typ != "OK":
        detail = b" ".join(d for d in (data or []) if isinstance(d, bytes))[:200].decode("utf-8", "replace")
        raise ImapError(f"{what} failed: {typ} {detail}")
    return data or []


class InboxReader:
    def __init__(self, conn: Any):
        self.conn = conn

    @classmethod
    def open_session(cls, host: str, port: int, tls: str, username: str, password: str,
                     connector: Callable[..., Any] = connect) -> "InboxReader":
        try:
            conn = connector(host, port, tls)
        except ImapError:
            raise
        except Exception as exc:   # DNS, refused, TLS, timeout
            raise ImapError(f"connect: {type(exc).__name__}") from exc
        reader = cls(conn)
        try:
            _ok(conn.login(username, password), "LOGIN")
        except ImapError:
            reader.close()
            raise
        except Exception as exc:   # imaplib raises IMAP4.error on a refused login
            reader.close()
            raise ImapError(f"LOGIN failed: {type(exc).__name__}") from exc
        return reader

    def folders(self) -> list[str]:
        found = ["INBOX"]
        for line in _ok(self.conn.list(), "LIST"):
            if not isinstance(line, bytes):
                continue
            match = _LIST_LINE.match(line.strip())
            if not match:
                continue
            flags = match.group("flags").decode("ascii", "replace").lower()
            name = match.group("name").decode("utf-8", "replace").strip()
            if name.startswith('"') and name.endswith('"'):
                name = name[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            if "\\noselect" in flags:
                continue
            if ("\\junk" in flags or name.lower() in JUNK_NAMES) and name not in found:
                found.append(name)
        return found

    def open(self, folder: str) -> int:
        _ok(self.conn.select(quote(folder), readonly=True), f"SELECT {folder}")
        data = _ok(self.conn.status(quote(folder), "(UIDVALIDITY UIDNEXT)"), f"STATUS {folder}")
        for line in data:
            match = _UIDVALIDITY.search(line if isinstance(line, bytes) else str(line).encode())
            if match:
                return int(match.group(1))
        raise ImapError(f"STATUS {folder}: no UIDVALIDITY")

    def _search(self, *criteria: str) -> list[int]:
        data = _ok(self.conn.uid("SEARCH", *criteria), "UID SEARCH")
        uids: list[int] = []
        for chunk in data:
            if isinstance(chunk, bytes):
                uids += [int(x) for x in chunk.split() if x.isdigit()]
        return sorted(set(uids))

    def uids_after(self, last_uid: int) -> list[int]:
        return [u for u in self._search("UID", f"{last_uid + 1}:*") if u > last_uid]

    def uids_since(self, day: date) -> list[int]:
        return self._search("SINCE", imap_date(day))

    def fetch(self, folder: str, uidvalidity: int, uid: int, max_bytes: int = MAX_FETCH_BYTES) -> FetchedMessage:
        data = _ok(self.conn.uid("FETCH", str(uid), f"(RFC822.SIZE BODY.PEEK[]<0.{max_bytes}>)"), f"FETCH {uid}")
        raw, size = None, None
        for item in data:
            if isinstance(item, tuple) and len(item) >= 2:
                head, body = item[0], item[1]
                found_uid = _UID.search(head or b"")
                if found_uid and int(found_uid.group(1)) != uid:
                    continue
                raw = body if isinstance(body, bytes) else bytes(body or b"")
                found = _SIZE.search(head or b"")
                size = int(found.group(1)) if found else len(raw)
                break
        if raw is None:
            raise ImapError(f"FETCH {uid}: no message body in the answer")
        return FetchedMessage(folder, uid, uidvalidity, size or len(raw), raw)

    def close(self) -> None:
        for step in ("logout",):
            try:
                getattr(self.conn, step)()
            except Exception:
                pass
