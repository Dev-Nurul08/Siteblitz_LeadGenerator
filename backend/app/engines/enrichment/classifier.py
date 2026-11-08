"""
Contact Classifier module (Phase 3).

Parses human names and job titles into structured first/last names and
seniority/department role levels (EXECUTIVE, MANAGEMENT, TECHNICAL, MARKETING, STAFF, GENERAL_INBOX).
"""

from dataclasses import dataclass
import re
from typing import Optional

from backend.app.models.contact import RoleLevel

# Honorific titles to strip during name normalization
HONORIFICS = [
    r"^(?:mr|mrs|ms|miss|dr|prof|eng|rev|sir|dame|herr|frau|monsieur|mme)\.?\s+",
    r"\b(?:esq|phd|md|mba|cpa|do|jd)\.?$",
]

# Title pattern matching
EXECUTIVE_PATTERNS = [
    r"\b(?:ceo|chief executive|founder|co-founder|owner|proprietor|president|managing director|partner|principal|co-owner)\b",
]

MANAGEMENT_PATTERNS = [
    r"\b(?:director|vice president|vp|general manager|operations manager|store manager|branch manager|head of|supervisor|team lead)\b",
]

TECHNICAL_PATTERNS = [
    r"\b(?:cto|chief technology|lead developer|software engineer|it manager|systems architect|tech lead|developer|webmaster|programmer|systems engineer|devops)\b",
]

MARKETING_PATTERNS = [
    r"\b(?:cmo|chief marketing|chief marketing officer|marketing director|head of marketing|growth lead|brand manager|digital marketing|marketing manager|marketing coordinator|marketing|seo specialist|social media manager)\b",
]


@dataclass
class ClassificationResult:
    """Classified contact identity and role level."""

    full_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    job_title: Optional[str]
    role_level: RoleLevel
    department: str = "GENERAL"  # EXECUTIVE, ENGINEERING, MARKETING, OPERATIONS, GENERAL
    seniority_score: float = 0.5  # 0.0 to 1.0


class ContactClassifier:
    """
    Extracts name parts, cleans honorifics, and classifies hierarchy/role level.
    """

    def classify_contact(
        self,
        full_name: Optional[str] = None,
        job_title: Optional[str] = None,
        email: Optional[str] = None,
    ) -> ClassificationResult:
        """
        Parse and categorize a business contact.
        """
        first_name = None
        last_name = None
        cleaned_name = None

        if full_name and isinstance(full_name, str):
            cleaned = full_name.strip()
            # Remove honorifics
            for h in HONORIFICS:
                cleaned = re.sub(h, "", cleaned, flags=re.IGNORECASE).strip()

            parts = cleaned.split()
            if len(parts) == 1:
                first_name = parts[0].capitalize()
                cleaned_name = first_name
            elif len(parts) >= 2:
                first_name = parts[0].capitalize()
                # Handle compound surnames (e.g. Van Der Beek, De La Cruz, St. John)
                last_name = " ".join(p.capitalize() for p in parts[1:])
                cleaned_name = f"{first_name} {last_name}"

        # Determine RoleLevel and Department
        title_lower = (job_title or "").lower().strip()
        email_local = (email or "").split("@")[0].lower() if email else ""

        department = "GENERAL"
        seniority = 0.5

        if any(re.search(pat, title_lower) for pat in EXECUTIVE_PATTERNS):
            role = RoleLevel.EXECUTIVE
            department = "EXECUTIVE"
            seniority = 1.0
        elif any(re.search(pat, title_lower) for pat in TECHNICAL_PATTERNS):
            role = RoleLevel.TECHNICAL
            department = "ENGINEERING"
            seniority = 0.85
        elif any(re.search(pat, title_lower) for pat in MARKETING_PATTERNS):
            role = RoleLevel.MARKETING
            department = "MARKETING"
            seniority = 0.80
        elif any(re.search(pat, title_lower) for pat in MANAGEMENT_PATTERNS):
            role = RoleLevel.MANAGEMENT
            department = "OPERATIONS"
            seniority = 0.75
        elif email_local in [
            "info", "contact", "hello", "office", "enquiries", "support",
            "sales", "admin", "help", "billing", "inquiries", "reception"
        ]:
            role = RoleLevel.GENERAL_INBOX
            department = "GENERAL"
            seniority = 0.20
        elif job_title:
            role = RoleLevel.STAFF
            seniority = 0.50
        elif cleaned_name:
            role = RoleLevel.STAFF
            seniority = 0.50
        else:
            role = RoleLevel.GENERAL_INBOX
            seniority = 0.20

        return ClassificationResult(
            full_name=cleaned_name,
            first_name=first_name,
            last_name=last_name,
            job_title=job_title.strip() if job_title else None,
            role_level=role,
            department=department,
            seniority_score=seniority,
        )
