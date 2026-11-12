"""
Email engine v2, phase E1 - eligibility models (spec: docs/spec/email-engine-v2.md rows 2-4, 8, 19).

Four tables, all new, so an existing database gets them from `create_all` without a migration:

- `email_captures`        append-only evidence: where and when an address was seen (one row per sighting).
- `email_verifications`   verifier cache: the latest result per (address, provider), re-checked after 30 days.
- `social_confirmations`  the founder's own check of a business's Instagram bio (automated reading of
                          Instagram / Facebook is banned in this project, DECISIONS 2026-11-08).
- `email_eligibility`     one row per (business, address): tier, provenance, recipient type, verifier status,
                          observation, suppression, HOLD reasons and the final `eligible` flag. Recomputed by
                          `EligibilityService.evaluate`; never edited by hand.

The rules that fill `email_eligibility` live in `backend/app/engines/eligibility/rules.py` (pure functions).
HOLD reason codes are the `HoldReason` enum below; every HOLD row carries at least one.
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base

JSON_TYPE = JSON().with_variant(JSONB, "postgresql")

EXCERPT_MAX_CHARS = 300   # spec row 3 / E1 brief: the page excerpt around the address
PILOT_COUNTRIES = {"IN"}  # spec row 2: India only for the controlled pilot


class EligibilityTier(str, enum.Enum):
    """Spec row 3 and RESULT row 9."""

    TIER1 = "TIER1"  # on the business's own website (host match) with URL + date + excerpt, or founder-confirmed
    TIER2 = "TIER2"  # listing-only (e.g. Overture alone): always HOLD
    HOLD = "HOLD"    # provenance incomplete or unclear (own-site method without excerpt, other host, ...)


class CaptureMethod(str, enum.Enum):
    """How an address was read. The first three are the only page methods spec row 10 of the outreach spec allows."""

    MAILTO = "mailto"
    VISIBLE_TEXT = "visible_text"            # includes "name [at] domain [dot] com" written on the page
    CLOUDFLARE_DECODE = "cloudflare_decode"
    FOUNDER_CONFIRMED = "founder_confirmed"  # seen by the founder on a profile the business controls
    LISTING = "listing"                      # a directory / Overture field: Tier 2


class RecipientType(str, enum.Enum):
    BUSINESS = "business"            # role inbox or an address that names the business
    EMPLOYEE_LIKE = "employee_like"  # a personal-name local part at a company domain: HOLD
    UNKNOWN = "unknown"              # cannot tell (e.g. a free-mail address that does not name the business)


class VerificationStatus(str, enum.Enum):
    """Verifier ladder result (spec row 3: only VALID may be sent to)."""

    UNVERIFIED = "UNVERIFIED"  # no verifier answer (no key configured, or the call failed): never pretend
    VALID = "VALID"
    RISKY = "RISKY"
    CATCH_ALL = "CATCH_ALL"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"


class ObservationType(str, enum.Enum):
    """Spec row 4: the three observations used in the pilot."""

    SOCIAL_ONLY = "SOCIAL_ONLY"
    SITE_DOWN = "SITE_DOWN"
    NO_VIEWPORT = "NO_VIEWPORT"


class HoldReason(str, enum.Enum):
    """
    Why an address may not be emailed. A HOLD row lists every reason that applies, so fixing one shows the next.

    COUNTRY_NOT_IN_PILOT     business country is not India (or unknown) - spec row 2
    LISTING_ONLY             address found only in a listing such as Overture (Tier 2) - spec row 3
    PROVENANCE_INCOMPLETE    own-page address without source URL, capture date or excerpt - spec row 3
    SOURCE_NOT_OWN_SITE      the page the address was read from is not on the business's own host - spec row 3
    EMPLOYEE_LIKE_ADDRESS    personal-name local part at a company domain - RESULT row 10
    SYSTEM_ADDRESS           no-reply / postmaster / abuse / privacy / legal mailbox, not for a sales message
    CHAIN_OR_DIRECTORY       Overture brand set, or a site / address shared by 3+ businesses - spec row 3
    DUPLICATE_RECIPIENT      the same address belongs to another business that already uses it - spec row 3
    NOT_PRIMARY_RECIPIENT    the business has a better address; one recipient per business - spec row 3
    NOT_A_PROSPECT           website-intelligence rule 9 (school, college, bank, ...)
    SUPPRESSED               opt-out on this address or domain, or a do-not-contact log entry - spec row 13
    NOT_VERIFIED             no verifier result (UNVERIFIED) - spec row 3
    VERIFIER_RISKY           verifier said risky - spec row 3
    VERIFIER_CATCH_ALL       verifier said accept-all / catch-all - spec row 3
    VERIFIER_UNKNOWN         verifier could not tell - spec row 3
    VERIFIER_INVALID         verifier (or the MX check) said the address cannot receive mail
    NO_PILOT_OBSERVATION     no verified SOCIAL_ONLY / SITE_DOWN / NO_VIEWPORT observation - spec row 4
    OBSERVATION_STALE        the observation's check is older than 30 days - outreach spec row 4
    PHONE_CHECK_PENDING      the page source has no viewport tag but the rendered phone check has not run (or failed)
    SITE_DOWN_NEEDS_RECHECK  the homepage failed once (or twice < 6 h apart); a second check >= 6 h later is needed
    SITE_RECOVERED           the homepage was confirmed down earlier but loaded in the latest check
    MAILBOX_DOMAIN_DOWN      SITE_DOWN lead whose address is on the down domain and has not passed an MX check
    NEEDS_FOUNDER_CHECK      social-only business: the founder must check the Instagram bio first - spec row 4
    SOCIAL_ONLY_DOMAIN_ADDRESS  SOCIAL_ONLY lead whose address is on its own (non-free-mail) domain, which may host a
                             website: "no website link" would read as "you have no website" (pre-send review 2026-11-12)
    """

    COUNTRY_NOT_IN_PILOT = "COUNTRY_NOT_IN_PILOT"
    LISTING_ONLY = "LISTING_ONLY"
    PROVENANCE_INCOMPLETE = "PROVENANCE_INCOMPLETE"
    SOURCE_NOT_OWN_SITE = "SOURCE_NOT_OWN_SITE"
    EMPLOYEE_LIKE_ADDRESS = "EMPLOYEE_LIKE_ADDRESS"
    SYSTEM_ADDRESS = "SYSTEM_ADDRESS"
    CHAIN_OR_DIRECTORY = "CHAIN_OR_DIRECTORY"
    DUPLICATE_RECIPIENT = "DUPLICATE_RECIPIENT"
    NOT_PRIMARY_RECIPIENT = "NOT_PRIMARY_RECIPIENT"
    NOT_A_PROSPECT = "NOT_A_PROSPECT"
    SUPPRESSED = "SUPPRESSED"
    NOT_VERIFIED = "NOT_VERIFIED"
    VERIFIER_RISKY = "VERIFIER_RISKY"
    VERIFIER_CATCH_ALL = "VERIFIER_CATCH_ALL"
    VERIFIER_UNKNOWN = "VERIFIER_UNKNOWN"
    VERIFIER_INVALID = "VERIFIER_INVALID"
    NO_PILOT_OBSERVATION = "NO_PILOT_OBSERVATION"
    OBSERVATION_STALE = "OBSERVATION_STALE"
    PHONE_CHECK_PENDING = "PHONE_CHECK_PENDING"
    SITE_DOWN_NEEDS_RECHECK = "SITE_DOWN_NEEDS_RECHECK"
    SITE_RECOVERED = "SITE_RECOVERED"
    MAILBOX_DOMAIN_DOWN = "MAILBOX_DOMAIN_DOWN"
    NEEDS_FOUNDER_CHECK = "NEEDS_FOUNDER_CHECK"
    SOCIAL_ONLY_DOMAIN_ADDRESS = "SOCIAL_ONLY_DOMAIN_ADDRESS"


class EmailCapture(Base):
    """One sighting of an address (append-only). `capture_key` makes imports idempotent."""

    __tablename__ = "email_captures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    method: Mapped[CaptureMethod] = mapped_column(Enum(CaptureMethod), nullable=False)
    raw_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g. visible_text_obfuscated
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # <= EXCERPT_MAX_CHARS
    captured_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # where the sighting came from: "email_finder:2026-11-10", "pool_e1:2026-11-12", "overture", "confirmation:7"
    origin: Mapped[str] = mapped_column(String(100), nullable=False)
    capture_key: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("ix_email_captures_business", "business_id", "email"),)


class EmailVerification(Base):
    """Verifier cache: latest result per (address, provider). Providers: `syntax_mx`, `bouncer`."""

    __tablename__ = "email_verifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), nullable=False)
    # syntax_mx: {"mx_ok": bool, "mx_hosts": [...], "note": ...}; bouncer: {"status", "reason", "accept_all", ...}
    detail: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (UniqueConstraint("email", "provider", name="uq_email_verification_provider"),)


class SocialConfirmation(Base):
    """The founder checked a business's Instagram bio by hand (POST /api/v1/outreach/confirmations)."""

    __tablename__ = "social_confirmations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )
    profile_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    website_link_present: Mapped[bool] = mapped_column(Boolean, nullable=False)
    email_seen: Mapped[Optional[str]] = mapped_column(String(320), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("ix_social_confirmations_business", "business_id"),)


class EmailEligibility(Base):
    """Eligibility of one address for one business (spec rows 2-4). Recomputed, never hand-edited."""

    __tablename__ = "email_eligibility"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    email_hash: Mapped[str] = mapped_column(String(64), nullable=False)  # sha256_hex(email.strip().lower())
    tier: Mapped[EligibilityTier] = mapped_column(Enum(EligibilityTier), nullable=False)

    # provenance of the best sighting
    capture_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("email_captures.id", ondelete="SET NULL"), nullable=True
    )
    method: Mapped[Optional[CaptureMethod]] = mapped_column(Enum(CaptureMethod), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    captured_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    recipient_type: Mapped[RecipientType] = mapped_column(Enum(RecipientType), nullable=False)
    verification_status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), nullable=False)
    verification_provider: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    country: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    vertical: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    observation_type: Mapped[Optional[ObservationType]] = mapped_column(Enum(ObservationType), nullable=True)
    observation_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    observation_checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    observation_evidence_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    suppressed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    hold_reasons: Mapped[list] = mapped_column(JSON_TYPE, nullable=False, default=list)
    eligible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # True when the only thing missing is a verifier result (hold_reasons == ["NOT_VERIFIED"]) or nothing
    eligible_if_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("business_id", "email", name="uq_email_eligibility_business_email"),
        Index("ix_email_eligibility_eligible", "eligible"),
        Index("ix_email_eligibility_hash", "email_hash"),
    )
