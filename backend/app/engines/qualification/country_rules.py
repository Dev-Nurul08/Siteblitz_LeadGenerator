"""
Country Rules Engine (Phase 4).

Evaluates international legal frameworks for outbound B2B sales outreach
across jurisdictions (US CAN-SPAM, UK GDPR/PECR, EU GDPR, Canada CASL, Australia Spam Act).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from backend.app.models.compliance import LegalBasis, LegalFramework, OutreachMode

# EU member country codes (ISO 3166-1 alpha-2)
EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
    "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
    "PL", "PT", "RO", "SK", "SI", "ES", "SE",
}

# Countries with strict national opt-in or unfair competition laws even for B2B cold email
STRICT_EU_MANUAL_COUNTRIES = {"DE", "AT", "GR"}


@dataclass
class CountryComplianceProfile:
    """Legal evaluation and compliance requirements for a specific jurisdiction."""

    country_code: str
    country_name: str
    framework: LegalFramework
    is_outreach_permitted: bool
    default_mode: OutreachMode
    legal_basis: LegalBasis
    risk_score: float  # 0.0 (safe) to 1.0 (high regulatory risk)
    requirements_checklist: Dict[str, bool] = field(default_factory=dict)
    mandatory_footer_elements: List[str] = field(default_factory=list)
    compliance_guidance: str = ""


class CountryRulesEngine:
    """
    Evaluates country-specific B2B communication regulations.
    """

    def evaluate_jurisdiction(
        self,
        country_code: Optional[str],
        has_business_email: bool = True,
        is_corporate_entity: bool = True,
    ) -> CountryComplianceProfile:
        """
        Evaluate legal posture and compliance obligations based on the lead's country.
        """
        cc = (country_code or "US").strip().upper()

        if cc in ("US", "USA"):
            return CountryComplianceProfile(
                country_code="US",
                country_name="United States",
                framework=LegalFramework.CAN_SPAM,
                is_outreach_permitted=True,
                default_mode=OutreachMode.AUTOMATED,
                legal_basis=LegalBasis.OPT_OUT_REGIME,
                risk_score=0.15,
                requirements_checklist={
                    "valid_physical_postal_address": True,
                    "clear_opt_out_link": True,
                    "non_deceptive_subject_line": True,
                    "accurate_header_information": True,
                    "honor_opt_out_within_10_days": True,
                },
                mandatory_footer_elements=["UNSUBSCRIBE_LINK", "PHYSICAL_ADDRESS"],
                compliance_guidance=(
                    "FTC CAN-SPAM Act compliance: Outbound B2B allowed without prior consent. "
                    "Mandatory physical postal address, clear opt-out mechanism, and non-deceptive subject."
                ),
            )

        if cc in ("GB", "UK"):
            mode = OutreachMode.AUTOMATED if is_corporate_entity else OutreachMode.MANUAL_REVIEW_ONLY
            return CountryComplianceProfile(
                country_code="GB",
                country_name="United Kingdom",
                framework=LegalFramework.GDPR_UK,
                is_outreach_permitted=True,
                default_mode=mode,
                legal_basis=LegalBasis.LEGITIMATE_INTEREST,
                risk_score=0.25 if is_corporate_entity else 0.50,
                requirements_checklist={
                    "corporate_subscriber_verified": is_corporate_entity,
                    "legitimate_interest_assessment_logged": True,
                    "easy_opt_out_in_every_message": True,
                    "sender_company_identified": True,
                },
                mandatory_footer_elements=["UNSUBSCRIBE_LINK", "PHYSICAL_ADDRESS", "COMPANY_REGISTRATION"],
                compliance_guidance=(
                    "PECR Reg 22 & UK GDPR: Corporate subscribers (companies, LLPs) do not require prior opt-in. "
                    "Legitimate interest applies for digital service pitch directly relevant to business functions."
                ),
            )

        if cc in EU_COUNTRIES:
            is_strict = cc in STRICT_EU_MANUAL_COUNTRIES
            mode = OutreachMode.MANUAL_REVIEW_ONLY if is_strict else OutreachMode.AUTOMATED
            risk = 0.60 if is_strict else 0.35

            return CountryComplianceProfile(
                country_code=cc,
                country_name=f"European Union ({cc})",
                framework=LegalFramework.GDPR_EU,
                is_outreach_permitted=True,
                default_mode=mode,
                legal_basis=LegalBasis.LEGITIMATE_INTEREST,
                risk_score=risk,
                requirements_checklist={
                    "legitimate_interest_basis_recorded": True,
                    "direct_role_relevance_established": True,
                    "clear_gdpr_opt_out_link": True,
                    "data_minimization_respected": True,
                    "privacy_policy_accessible": True,
                },
                mandatory_footer_elements=["UNSUBSCRIBE_LINK", "PHYSICAL_ADDRESS", "PRIVACY_POLICY"],
                compliance_guidance=(
                    f"EU GDPR Art. 6(1)(f) Legitimate Interest. Strict B2B targeting applies. "
                    f"{'Requires manual compliance sign-off due to national UWG law.' if is_strict else 'Automated allowed for verified business roles.'}"
                ),
            )

        if cc in ("CA", "CAN"):
            # CASL Section 10(9) conspicuous publication exemption
            return CountryComplianceProfile(
                country_code="CA",
                country_name="Canada",
                framework=LegalFramework.CASL,
                is_outreach_permitted=True,
                default_mode=OutreachMode.MANUAL_REVIEW_ONLY,
                legal_basis=LegalBasis.CONSPICUOUSLY_PUBLISHED_B2B,
                risk_score=0.55,
                requirements_checklist={
                    "conspicuous_publication_provenance_logged": True,
                    "no_negative_statement_found": True,
                    "direct_relevance_to_role": True,
                    "functional_unsubscribe_mechanism": True,
                    "sender_contact_and_postal_info": True,
                },
                mandatory_footer_elements=["UNSUBSCRIBE_LINK", "PHYSICAL_ADDRESS"],
                compliance_guidance=(
                    "CASL §10(9) conspicuous publication exemption: Recipient email must be publicly published "
                    "without express opt-out and message must directly relate to business role. Requires manual review."
                ),
            )

        if cc in ("AU", "AUS"):
            return CountryComplianceProfile(
                country_code="AU",
                country_name="Australia",
                framework=LegalFramework.AUSTRALIA_SPAM_ACT,
                is_outreach_permitted=True,
                default_mode=OutreachMode.AUTOMATED,
                legal_basis=LegalBasis.CONSPICUOUSLY_PUBLISHED_B2B,
                risk_score=0.30,
                requirements_checklist={
                    "inferred_consent_via_publication": True,
                    "direct_connection_to_business": True,
                    "clear_sender_identity": True,
                    "functional_unsubscribe_mandatory": True,
                },
                mandatory_footer_elements=["UNSUBSCRIBE_LINK", "PHYSICAL_ADDRESS"],
                compliance_guidance=(
                    "Australia Spam Act 2003: Inferred consent applies for conspicuously published business addresses "
                    "relevant to recipient's business function. Mandatory functional unsubscribe."
                ),
            )

        # Fallback / General International
        return CountryComplianceProfile(
            country_code=cc,
            country_name=f"International ({cc})",
            framework=LegalFramework.GENERAL_B2B,
            is_outreach_permitted=True,
            default_mode=OutreachMode.MANUAL_REVIEW_ONLY,
            legal_basis=LegalBasis.LEGITIMATE_INTEREST,
            risk_score=0.40,
            requirements_checklist={
                "clear_opt_out_link": True,
                "sender_identity_verified": True,
                "role_relevance_checked": True,
            },
            mandatory_footer_elements=["UNSUBSCRIBE_LINK", "PHYSICAL_ADDRESS"],
            compliance_guidance="International general standard: Conservative manual review posture.",
        )
