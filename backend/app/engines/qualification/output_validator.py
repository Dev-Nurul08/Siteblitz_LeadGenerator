"""
Output Safety & Compliance Validator (Phase 4).

Inspects generated outreach messages for deceptive claims, spam triggers,
unresolved template variables, and mandatory regulatory footer components.
"""

from dataclasses import dataclass, field
import re
from typing import List

# Prohibited predatory, deceptive, or high-risk spam phrases
SPAM_TRIGGER_PATTERNS = [
    r"\bguaranteed (?:100%|\d+%|million|wealth|rich|roi|results)",
    r"\bmake money fast\b",
    r"\brisk free guaranteed\b",
    r"\bcongratulations you won\b",
    r"\bact immediately or lose\b",
    r"\bcrypto returns\b",
    r"\bviagra\b",
    r"\b100% free money\b",
]

# Unresolved template placeholders that indicate generation bugs
UNRESOLVED_TOKEN_PATTERN = r"\{\{(?!(?:UNSUBSCRIBE_LINK|PHYSICAL_ADDRESS|COMPANY_REGISTRATION))\w+\}\}"


@dataclass
class ValidationResult:
    """Outcome of safety and compliance inspection."""

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    checked_tokens: List[str] = field(default_factory=list)


class OutputValidator:
    """
    Validates marketing pitches against FTC truth-in-advertising standards,
    CAN-SPAM mandatory opt-out tokens, and spam filter heuristics.
    """

    def validate(
        self,
        subject: str,
        body: str,
        require_unsubscribe: bool = True,
        require_physical_address: bool = True,
    ) -> ValidationResult:
        """
        Validate generated subject line and body text.
        """
        errors = []
        warnings = []
        checked_tokens = []

        # 1. Subject line checks
        if not subject or not subject.strip():
            errors.append("Subject line cannot be empty.")
        elif len(subject) > 120:
            warnings.append(f"Subject line is {len(subject)} chars (recommended under 80 for mobile email clients).")

        # 2. Body length checks
        words = body.split()
        if len(words) < 20:
            errors.append(f"Body text is too short ({len(words)} words; minimum 20 words required for context).")
        elif len(words) > 400:
            warnings.append(f"Body text is {len(words)} words (recommended under 200 words for B2B executive conversion).")

        # 3. Mandatory regulatory footer elements
        if require_unsubscribe:
            checked_tokens.append("UNSUBSCRIBE_LINK")
            if "{{UNSUBSCRIBE_LINK}}" not in body and "opt out" not in body.lower():
                errors.append("Mandatory unsubscribe mechanism ({{UNSUBSCRIBE_LINK}}) missing from message body.")

        if require_physical_address:
            checked_tokens.append("PHYSICAL_ADDRESS")
            # Checks for postal indicator or address token
            has_address = any(
                term in body.lower()
                for term in ["suite", "way", "st", "street", "ave", "avenue", "new york", "zip", "po box", "{{physical_address}}"]
            )
            if not has_address:
                errors.append("Valid physical postal address or {{PHYSICAL_ADDRESS}} token missing from message body.")

        # 4. Unresolved template placeholders check
        unresolved_subject = re.findall(UNRESOLVED_TOKEN_PATTERN, subject, flags=re.IGNORECASE)
        unresolved_body = re.findall(UNRESOLVED_TOKEN_PATTERN, body, flags=re.IGNORECASE)
        if unresolved_subject or unresolved_body:
            tokens = set(unresolved_subject + unresolved_body)
            errors.append(f"Found unreplaced placeholder variables: {', '.join(tokens)}")

        # Check for literal None or undefined leaking into text
        leak_matches = re.findall(r"\b(?:None|undefined|NaN)\b", f"{subject} {body}")
        if leak_matches:
            warnings.append("Text contains suspicious placeholder literals ('None', 'undefined', or 'NaN').")

        # 5. Spam trigger & deceptive claims inspection
        combined_text = f"{subject} {body}".lower()
        for pat in SPAM_TRIGGER_PATTERNS:
            if re.search(pat, combined_text, flags=re.IGNORECASE):
                errors.append(f"Spam trigger or deceptive claim detected matching pattern: {pat}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            checked_tokens=checked_tokens,
        )
