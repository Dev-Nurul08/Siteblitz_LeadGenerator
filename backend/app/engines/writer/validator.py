"""
Deterministic checks on every message the AI writer returns (phase 13, docs/spec/outreach-engine.md).

The model's own self-check fields are never trusted. Every rule is recomputed here from the lead, the task and the
company facts, and a message that fails any check is never sent. Pure functions, no network.
"""

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from langdetect import DetectorFactory, LangDetectException, detect_langs

# langdetect samples randomly; a fixed seed makes the same text always get the same answer.
DetectorFactory.seed = 0

CHANNELS = ("email", "whatsapp_reply", "social_dm", "letter")
HOLD_REASONS = (
    "COUNTRY_NOT_LISTED", "COUNTRY_ON_HOLD", "NO_OPTIN", "NO_OBSERVATION",
    "MISSING_COMPANY_FACT", "SUPPRESSED", "LANGUAGE_UNCLEAR",
)
LANGUAGE_BASES = ("business_evidence", "owner_message", "region_rule", "country_default")
REPLY_CLASSES = (
    "INTERESTED", "PRICE_QUESTION", "SEND_DETAILS", "HAS_WEBSITE", "NOT_NOW", "STOP",
    "WRONG_PERSON", "CALL_ME", "OUT_OF_OFFICE", "OTHER",
)
# Reply classes for which the writer sends nothing (the founder or the scheduler acts instead).
SILENT_REPLY_CLASSES = ("OUT_OF_OFFICE", "OTHER")

# Spec row 4: highest priority first.
OBSERVATION_PRIORITY = (
    "SITE_DOWN", "BROKEN_FORM", "NO_VIEWPORT", "SOCIAL_ONLY", "AGGREGATOR_ONLY", "NO_SITE", "NO_HTTPS",
)

# Spec row 5: (min, max) words of the body, without signature and opt-out line. Key = (channel, touch).
WORD_LIMITS = {
    ("email", 1): (60, 85),
    ("email", 2): (40, 70),
    ("email", 3): (30, 50),
    ("social_dm", 1): (30, 60),
    ("letter", 1): (100, 150),
}
WHATSAPP_WORD_LIMITS = (25, 60)
EMAIL_T1_MAX_WITH_SIGNATURE = 100

# Company facts each channel needs before anything can be written (prompt STEP 1).
CHANNEL_FACTS = {
    "email": ("sender_name", "reply_email", "postal_address"),
    "letter": ("sender_name", "reply_email", "postal_address"),
    "social_dm": ("sender_name",),
    "whatsapp_reply": ("sender_name",),
}

# Prompt STYLE list. Matched case-insensitively on word boundaries.
BANNED_PHRASES = (
    "i hope this email finds you well", "i hope you're doing well", "i hope you are doing well", "i came across",
    "i stumbled upon", "i wanted to reach out", "reaching out", "just checking in", "touching base",
    "following up on my previous email", "quick question", "elevate", "seamless", "seamlessly", "unlock",
    "vibrant", "testament", "nestled", "delve", "showcase", "showcasing", "underscore", "leverage",
    "cutting-edge", "game-changer", "game changer", "take your business to the next level", "boost", "skyrocket",
    "in today's digital age", "in today's fast-paced world", "online presence", "digital footprint", "solutions",
    "synergy", "hassle-free", "world-class", "stunning", "transform", "revolutionize", "dear sir/madam",
    "to whom it may concern", "hope to hear from you soon", "looking forward to hearing from you",
    "feel free to", "don't hesitate to", "do not hesitate to",
    # Never mention how the message was made (prompt STYLE, last rule).
    "artificial intelligence", "automated", "automation", "our system", "scraping", "scraped", "database",
)
BANNED_CHARACTERS = {"—": "em dash", "–": "en dash", "!": "exclamation mark", "！": "exclamation mark",
                     ";": "semicolon"}

# Languages langdetect 1.0.9 can recognise (its profile list). Anything else cannot be verified -> fail closed.
DETECTABLE = {
    "af", "ar", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa", "fi", "fr", "gu", "he",
    "hi", "hr", "hu", "id", "it", "ja", "kn", "ko", "lt", "lv", "mk", "ml", "mr", "ne", "nl", "no", "pa", "pl",
    "pt", "ro", "ru", "sk", "sl", "so", "sq", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "vi",
    "zh-cn", "zh-tw",
}
# Languages written without spaces: a word count means nothing there and no character rule exists yet.
NO_WORD_COUNT = {"ja", "zh", "th"}
# Common Roman Hindi words. Roman Hindi cannot be detected by langdetect, so an owner's message counts as
# Roman Hindi when it is plain ASCII and uses at least two of these words.
ROMAN_HINDI_WORDS = {
    "hai", "hain", "ke", "ki", "ka", "kya", "nahi", "nahin", "aap", "mujhe", "hum", "karna", "chahiye", "kaise",
    "kitna", "kitne", "bhai", "ji", "haan", "acha", "accha", "achha", "mein", "yeh", "woh", "kar", "batao",
    "bataiye", "dijiye", "kijiye", "website", "wala", "wali", "sab", "abhi",
}
ROMAN_HINDI_STRONG = ROMAN_HINDI_WORDS - {"website"}
DEVANAGARI = re.compile(r"[ऀ-ॿ]")

NUMBER = re.compile(r"\d[\d,.]*")
URL = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
DOMAIN = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}\b", re.IGNORECASE)
UNRESOLVED = re.compile(r"\[[^\]]*\]|\{\{|\}\}|TO FILL")

# ─── Email engine v2 pilot (docs/outreach/pilot-templates.md; spec v2 rows 5-6, RESULT rows 13 / 16 / C) ──────
# Body words per touch (spec v2 rows 5-6). The phase-13 "100 with signature" cap is not applied to pilot emails:
# the v2 signature adds WhatsApp + unsubscribe lines, so that cap would depend on the postal address (e3-notes.md).
PILOT_WORD_LIMITS = {1: (60, 85), 2: (40, 70), 3: (30, 50)}
PILOT_SUBJECT_FACT_WORDS = (3, 8)
# RESULT C / spec v2 row 5, word for word (India).
PILOT_PRICE_LINE = "Website setup starts at ₹7,999, with domain and hosting charged separately."
PILOT_IDENTITY_LINE = "I'm {sender} from SiteBlitz, a small web studio in Gujarat."
PILOT_QUESTION = "Shall I make a sample page for {business} and send it here?"
# The opt-out line E2's message builder writes (backend/app/engines/sending/message.py UNSUBSCRIBE_LINE). Until a
# send record exists the stored text carries the placeholder; the builder replaces the whole line at send time.
UNSUBSCRIBE_PREFIX = 'Reply "stop" or unsubscribe here:'
UNSUBSCRIBE_PLACEHOLDER = "[unsubscribe link added when sent]"
UNSUBSCRIBE_LINE_RE = re.compile(r'^Reply "stop" or unsubscribe here: (\S+|\[unsubscribe link added when sent\])$')
# Prompt P8 (no deadlines, discounts, "limited slots", "only this week", fear or guilt), checked in every pilot touch.
PRESSURE_PHRASES = ("limited", "last chance", "hurry", "urgent", "only this week", "act now", "offer ends",
                    "deadline", "discount", "don't miss")
# A follow-up must carry new information (RESULT row 13), not a nudge.
FOLLOW_UP_FILLER = ("just following up", "following up", "checking in", "circling back", "bumping",
                    "my last email", "my previous email", "did you get a chance", "did you see my")


@dataclass(frozen=True)
class LanguageRow:
    """One row of docs/outreach/country-language.csv."""

    country: str
    country_name: str
    email_status: str
    default_language: str
    allowed_languages: tuple[str, ...]
    region_rule: str
    greeting_no_name: str
    signoff: str


def load_country_languages(path: Path) -> dict[str, LanguageRow]:
    rows: dict[str, LanguageRow] = {}
    with open(path, encoding="utf-8", newline="") as handle:
        for raw in csv.DictReader(handle):
            rows[raw["country"].strip().upper()] = LanguageRow(
                country=raw["country"].strip().upper(),
                country_name=raw["country_name"].strip(),
                email_status=raw["email_status"].strip().upper(),
                default_language=raw["default_language"].strip(),
                allowed_languages=tuple(x.strip() for x in raw["allowed_languages"].split("|") if x.strip()),
                region_rule=raw["region_rule"].strip(),
                greeting_no_name=raw["greeting_no_name"].strip(),
                signoff=raw["signoff"].strip(),
            )
    return rows


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def word_count(text: str) -> int:
    return len((text or "").split())


def numbers_in(text: str) -> set[str]:
    """Digit groups with thousands separators removed: "₹7,999." -> "7999"."""
    found = set()
    for match in NUMBER.finditer(text or ""):
        value = match.group().replace(",", "").rstrip(".")
        if value:
            found.add(value)
    return found


def domains_in(text: str) -> set[str]:
    found = {m.group().lower() for m in DOMAIN.finditer(text or "")}
    for url in URL.findall(text or ""):
        found.update(m.group().lower() for m in DOMAIN.finditer(url))
    return {d[4:] if d.startswith("www.") else d for d in found}


def is_roman_hindi(message: Optional[str]) -> bool:
    if not message or not message.isascii():
        return False
    words = set(re.findall(r"[a-z]+", message.lower()))
    return len(words & ROMAN_HINDI_STRONG) >= 2


def detector_code(language_tag: str) -> Optional[str]:
    """BCP-47 tag -> langdetect code, or None when langdetect cannot recognise the language."""
    lang, _, region = language_tag.partition("-")
    lang = lang.lower()
    if lang == "zh":
        return "zh-tw" if region.upper() in ("TW", "HK", "HANT") else "zh-cn"
    if lang == "fil":
        return "tl"
    return lang if lang in DETECTABLE else None


def owner_message(lead: dict, task: dict) -> Optional[str]:
    if task.get("inbound_message"):
        return task["inbound_message"]
    optin = lead.get("optin") or {}
    return optin.get("message")


def expected_hold(lead: dict, task: dict, rows: dict[str, LanguageRow], missing_facts: list[str]) -> Optional[str]:
    """Prompt STEP 1, recomputed. Returns the first hold reason that applies, or None."""
    channel = task.get("channel")
    row = rows.get((lead.get("country") or "").strip().upper())
    if row is None:
        return "COUNTRY_NOT_LISTED"
    if channel in ("email", "social_dm", "letter") and row.email_status != "PILOT":
        return "COUNTRY_ON_HOLD"
    if channel == "whatsapp_reply" and not lead.get("optin"):
        return "NO_OPTIN"
    if task.get("touch") == 1 and not task.get("inbound_message") and not lead.get("observations"):
        return "NO_OBSERVATION"
    if missing_facts:
        return "MISSING_COMPANY_FACT"
    if lead.get("suppressed"):
        return "SUPPRESSED"
    return None


def best_observation(lead: dict) -> Optional[dict]:
    observations = lead.get("observations") or []
    ranked = sorted(
        (o for o in observations if o.get("type") in OBSERVATION_PRIORITY),
        key=lambda o: OBSERVATION_PRIORITY.index(o["type"]),
    )
    return ranked[0] if ranked else None


def _has_phrase(text: str, phrase: str) -> bool:
    return re.search(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])", text, flags=re.IGNORECASE) is not None


def _flat(text: Optional[str]) -> str:
    """Whitespace collapsed to single spaces: paragraph breaks do not matter for the word-for-word lines."""
    return " ".join((text or "").split())


def pilot_email_errors(output: dict, lead: dict, task: dict) -> list[str]:
    """The pilot template rules for one email touch (docs/outreach/pilot-templates.md). `task["pilot"]` is built by
    the app (observation sentence from E1, identity / price / question lines), never by the model."""
    pilot = task.get("pilot") or {}
    touch = task.get("touch")
    errors: list[str] = []
    subject = (output.get("subject") or "").strip()
    body = (output.get("body") or "").strip()
    model_text = "\n".join(x for x in (subject, body) if x)
    flat = _flat(body)

    if (output.get("signoff") or "").strip():
        errors.append("a pilot email has no sign-off line: the app adds the signature block")
    if (output.get("opt_out_line") or "").strip():
        errors.append("a pilot email has no opt-out line of its own: the app adds the unsubscribe line")
    if URL.search(model_text):
        errors.append("no link is allowed in a pilot email (the app adds only the unsubscribe link)")
    low, high = PILOT_WORD_LIMITS.get(touch, (0, 0))
    words = word_count(body)
    if not low <= words <= high:
        errors.append(f"body has {words} words; pilot touch {touch} needs {low}-{high}")
    for phrase in PRESSURE_PHRASES:
        if _has_phrase(model_text, phrase):
            errors.append(f"pressure wording is not allowed: {phrase!r}")
    questions = body.count("?") + body.count("？")

    if touch == 1:
        observation = _flat(pilot.get("observation_sentence"))
        identity = _flat(pilot.get("identity_line"))
        price = _flat(pilot.get("price_line"))
        question = _flat(pilot.get("question"))
        tail = f"{price} {question}" if price else question
        if not observation or not flat.startswith(observation):
            errors.append("line 1 must be the observation sentence, word for word: " + repr(observation))
        else:
            rest = flat[len(observation):].strip()
            if not rest.startswith(identity):
                errors.append("the identity line must come right after the observation, word for word: "
                              + repr(identity))
            elif flat.endswith(tail) and not rest[len(identity):len(rest) - len(tail)].strip():
                errors.append("say what we build for this vertical between the identity line and the price line")
        if questions != 1:
            errors.append(f"a pilot touch 1 needs exactly one question, found {questions}")
        if not flat.endswith(question):
            errors.append("the last sentence must be the question, word for word: " + repr(question))
        elif price and not flat.endswith(tail):
            errors.append("the price line must come just before the question, word for word: " + repr(price))
        if price and flat.count(price) != 1:
            errors.append("the price line must appear exactly once")
        name = (lead.get("business_name") or "").strip()
        if not subject:
            errors.append("email touch 1 needs a subject")
        elif not subject.startswith(f"{name}:"):
            errors.append(f"the subject must start with the business name and a colon: {name + ':'!r}")
        else:
            fact_words = word_count(subject[len(name) + 1:])
            low_s, high_s = PILOT_SUBJECT_FACT_WORDS
            if not low_s <= fact_words <= high_s:
                errors.append(f"the subject fact after the name has {fact_words} words; {low_s}-{high_s} allowed")
        if re.match(r"\s*(re|fwd?)\s*:", subject, flags=re.IGNORECASE):
            errors.append("the first subject must not start with Re: or Fwd:")
        if "?" in subject or "!" in subject:
            errors.append("the subject must not contain a question or exclamation mark")
    else:
        for phrase in FOLLOW_UP_FILLER:
            if _has_phrase(model_text, phrase):
                errors.append(f"a follow-up must add new information, not {phrase!r}")
        if touch == 2:
            identity = _flat(pilot.get("identity_line"))
            if identity and not _flat(body).startswith(identity):
                # Pre-send review 2026-11-12: T2 is often read without touch 1, so it names the sender first.
                errors.append("touch 2 must start with the identity line, word for word: " + repr(identity))
            if not re.search(r"\bsample\b", body, flags=re.IGNORECASE):
                errors.append("touch 2 must offer the sample page again")
            if questions != 1:
                errors.append(f"touch 2 needs exactly one question, found {questions}")
            elif not body.rstrip().endswith(("?", "？")):
                errors.append("the question must be the last sentence")
    return errors


def assembled_pilot_errors(text: str, signature_lines: list[str]) -> list[str]:
    """Checks on the full text the app stores for sending: the signature block is there, the unsubscribe line is the
    last line (exactly once, with a URL or the placeholder E2 replaces) and it holds the only URL in the message."""
    errors: list[str] = []
    lines = (text or "").replace("\r\n", "\n").rstrip().split("\n")
    last = lines[-1].strip() if lines else ""
    if not UNSUBSCRIBE_LINE_RE.match(last):
        errors.append(f'the last line must be: {UNSUBSCRIBE_PREFIX} <unsubscribe link>')
    if sum(1 for line in lines if line.strip().startswith(UNSUBSCRIBE_PREFIX)) != 1:
        errors.append("the unsubscribe line must appear exactly once")
    rest = "\n".join(lines[:-1]) if UNSUBSCRIBE_LINE_RE.match(last) else "\n".join(lines)
    if URL.search(rest):
        errors.append("the unsubscribe link is the only link allowed in a pilot email")
    for line in signature_lines:
        if line not in lines:
            errors.append(f"signature line missing: {line!r}")
    return errors


def validate(
    output: dict,
    lead: dict,
    task: dict,
    rows: dict[str, LanguageRow],
    facts_text: str,
    signature: str,
    missing_facts: list[str],
) -> ValidationResult:
    """Check one writer answer. `facts_text` is the COMPANY_FACTS text the model saw; `signature` is the block the
    app appends (sender, SiteBlitz, reply address, postal address)."""
    errors: list[str] = []
    warnings: list[str] = []
    channel = task.get("channel")
    touch = task.get("touch")
    inbound = task.get("inbound_message")

    decision = output.get("decision")
    if decision not in ("WRITE", "HOLD"):
        return ValidationResult(False, [f"decision must be WRITE or HOLD, got {decision!r}"])

    must_hold = expected_hold(lead, task, rows, missing_facts)
    if decision == "HOLD":
        reason = output.get("hold_reason")
        if reason not in HOLD_REASONS:
            errors.append(f"unknown hold_reason {reason!r}")
        elif must_hold is None and reason != "LANGUAGE_UNCLEAR":
            errors.append(f"held with {reason} although nothing requires a hold")
        elif must_hold and reason != must_hold:
            warnings.append(f"held with {reason}; the rules say {must_hold}")
        if (output.get("body") or "").strip():
            errors.append("a HOLD answer must not contain a message")
        return ValidationResult(not errors, errors, warnings)

    if must_hold:
        return ValidationResult(False, [f"wrote a message although the lead must be held ({must_hold})"])
    if output.get("channel") != channel:
        errors.append(f"channel {output.get('channel')!r} does not match the task ({channel})")

    # --- Country and language (spec row 3) ---
    country = (lead.get("country") or "").strip().upper()
    row = rows[country]
    declared_country = (output.get("declared_country") or "").strip().upper()
    language = (output.get("declared_language") or "").strip()
    if declared_country != country:
        errors.append(f"declared_country {declared_country!r} is not the lead's country {country}")
    if language not in row.allowed_languages:
        errors.append(f"declared_language {language!r} is not allowed for {country} ({', '.join(row.allowed_languages)})")
    if output.get("language_basis") not in LANGUAGE_BASES:
        errors.append(f"unknown language_basis {output.get('language_basis')!r}")
    if (output.get("language_self_check") or "").strip() != language:
        errors.append(f"language_self_check {output.get('language_self_check')!r} differs from declared {language!r}")

    reply_class = output.get("reply_class")
    if inbound:
        if reply_class not in REPLY_CLASSES:
            errors.append(f"an inbound message needs a reply_class, got {reply_class!r}")
        if reply_class == "STOP" and output.get("suppress") is not True:
            errors.append("a STOP reply must set suppress = true")
    body = (output.get("body") or "").strip()
    if inbound and reply_class in SILENT_REPLY_CLASSES:
        if body:
            errors.append(f"{reply_class} replies must not contain a message")
        return ValidationResult(not errors, errors, warnings)
    if not body:
        return ValidationResult(False, errors + ["the message body is empty"], warnings)

    subject = (output.get("subject") or "").strip()
    signoff = (output.get("signoff") or "").strip()
    opt_out = (output.get("opt_out_line") or "").strip()
    model_text = "\n".join(x for x in (subject, body, signoff, opt_out) if x)

    if language == "hi-Latn":
        if not is_roman_hindi(owner_message(lead, task)):
            errors.append("Roman Hindi is allowed only as a reply to an owner who wrote in Roman Hindi")
        if DEVANAGARI.search(model_text):
            errors.append("Roman Hindi must be written in Latin letters, not Devanagari")
    elif language:
        code = detector_code(language)
        if code is None:
            errors.append(f"{language} cannot be verified by the language detector")
        else:
            try:
                ranked = detect_langs("\n".join(x for x in (body, opt_out) if x))
                top = ranked[0].lang if ranked else None
            except LangDetectException:
                top = None
            if top != code:
                errors.append(f"language check: the text reads as {top!r}, declared {language!r}")

    # --- Length and shape (spec row 5) ---
    base_language = language.split("-")[0].lower()
    # Email engine v2 pilot: its own template rules replace the phase-13 email shape rules (pilot-templates.md).
    pilot = channel == "email" and not inbound and bool(task.get("pilot"))
    first_touch = ((channel == "email" and touch == 1) or channel == "social_dm") and not pilot
    limits = WHATSAPP_WORD_LIMITS if channel == "whatsapp_reply" else WORD_LIMITS.get((channel, touch))
    if inbound and channel != "whatsapp_reply":
        limits = None  # email replies have no locked length
    if reply_class == "STOP" or pilot:
        limits = None
    if pilot:
        if base_language in NO_WORD_COUNT:
            errors.append(f"no length rule exists yet for {language}")
        errors.extend(pilot_email_errors(output, lead, task))
    if limits and base_language in NO_WORD_COUNT:
        errors.append(f"no length rule exists yet for {language}")
    elif limits:
        words = word_count(body)
        low, high = limits
        if not low <= words <= high:
            errors.append(f"body has {words} words; {channel} touch {touch} needs {low}-{high}")
        if channel == "email" and touch == 1:
            total = words + word_count(signoff) + word_count(signature)
            if total > EMAIL_T1_MAX_WITH_SIGNATURE:
                errors.append(f"{total} words with the signature; the maximum is {EMAIL_T1_MAX_WITH_SIGNATURE}")

    if first_touch and not inbound:
        questions = body.count("?") + body.count("？")
        if questions != 1:
            errors.append(f"a first message needs exactly one question, found {questions}")
        elif not body.rstrip().endswith(("?", "？")):
            errors.append("the question must be the last sentence")
        if URL.search(body):
            errors.append("no link is allowed in a first message")

    if channel == "email" and not inbound and not pilot:
        if touch == 1:
            if not subject:
                errors.append("email touch 1 needs a subject")
            if re.match(r"\s*(re|fwd?)\s*:", subject, flags=re.IGNORECASE):
                errors.append("the first subject must not start with Re: or Fwd:")
            name =(lead.get("business_name") or "").strip()
            if name and name.lower() not in subject.lower():
                errors.append("the subject must contain the business name")
            else:
                # A long business name counts as one word, so "A website idea for <name>" always fits.
                subject_words = word_count(re.sub(re.escape(name), "NAME", subject, flags=re.IGNORECASE)
                                           if name else subject)
                if not 3 <= subject_words <= 7:
                    errors.append(f"subject has {subject_words} words (business name counted once); 3-7 allowed")
            if "?" in subject:
                errors.append("the subject must not contain a question mark")
        if not signoff:
            errors.append("email needs a sign-off")
    if channel in ("email", "social_dm", "letter") and not inbound and not opt_out and not pilot:
        errors.append(f"{channel} needs an opt-out line")

    # --- Observation (spec row 4) ---
    if not inbound and channel != "whatsapp_reply":
        types = [o.get("type") for o in lead.get("observations") or []]
        used = output.get("observation_type")
        if touch == 1:
            best = best_observation(lead)
            if best and used != best["type"]:
                errors.append(f"observation {used!r} used; the highest-priority one is {best['type']}")
            evidence = (best or {}).get("evidence_value")
            if evidence and evidence.lower() not in body.lower():
                errors.append(f"the observation evidence {evidence!r} is not in the message")
        elif used and used not in types:
            errors.append(f"observation {used!r} is not one of the lead's checked observations")

    # --- Facts guard: nothing the inputs do not contain ---
    source_text = "\n".join([facts_text, repr(lead), repr(task)])
    allowed_numbers = numbers_in(source_text)
    for number in sorted(numbers_in(model_text) - allowed_numbers):
        errors.append(f"number {number} is not in the company facts or the lead")
    allowed_domains = source_text.lower()
    for domain in sorted(domains_in(model_text)):
        if domain not in allowed_domains:
            errors.append(f"domain {domain} is not in the company facts, the lead or the allowed links")

    # --- Style ---
    for phrase in BANNED_PHRASES:
        if _has_phrase(model_text, phrase):
            errors.append(f"banned phrase: {phrase!r}")
    if re.search(r"\bAI\b", model_text):
        errors.append("the message must not mention AI")
    for char, name in BANNED_CHARACTERS.items():
        if char in model_text:
            errors.append(f"banned character: {name}")
    unresolved = UNRESOLVED.findall(model_text)
    if unresolved:
        errors.append(f"unresolved placeholder: {unresolved[0]!r}")

    return ValidationResult(not errors, errors, warnings)
