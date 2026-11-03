"""
CSV/XLSX import source adapter.

Handles bulk import of business records from user-provided files.
Supports field mapping, validation, and error reporting.

License: MANUAL_OR_OPT_IN — data provenance is user's responsibility.
"""

import csv
import io
from typing import Optional

import structlog

from backend.app.engines.discovery.base import (
    AdapterResult,
    BaseSourceAdapter,
    DiscoveredBusiness,
)

logger = structlog.get_logger(__name__)

# Default field mappings
DEFAULT_FIELD_MAP = {
    "name": ["name", "business_name", "company_name", "company", "business"],
    "address": ["address", "address_line_1", "street_address", "street"],
    "city": ["city", "town", "locality"],
    "state": ["state", "state_province", "province", "region", "county"],
    "postal_code": ["postal_code", "zip", "zip_code", "postcode"],
    "country": ["country", "country_code", "country_name"],
    "phone": ["phone", "telephone", "tel", "phone_number"],
    "email": ["email", "email_address", "contact_email"],
    "website": ["website", "url", "web", "website_url", "homepage"],
    "category": ["category", "industry", "type", "business_type", "sector"],
}


class CSVImportAdapter(BaseSourceAdapter):
    """
    CSV/XLSX import adapter for bulk business data ingestion.

    This is not a discovery adapter — it processes user-provided data.
    The user is responsible for ensuring they have the right to use the data.
    """

    def __init__(self, rate_limit_rpm: int = 1000):
        """CSV import has no external rate limit."""
        super().__init__(rate_limit_rpm=rate_limit_rpm)

    def get_source_metadata(self) -> dict:
        return {
            "name": "CSV/XLSX Import",
            "slug": "csv_import",
            "description": (
                "Bulk import of business records from CSV or XLSX files. "
                "Data provenance and usage rights are the user's responsibility."
            ),
            "license_type": "MANUAL_OR_OPT_IN",
            "license_url": None,
            "attribution_required": False,
            "allows_commercial_storage": True,
            "allows_contact_enrichment": True,
            "allows_marketing_use": True,  # User-determined
            "adapter_class": "backend.app.engines.discovery.csv_import.CSVImportAdapter",
        }

    async def discover(
        self,
        *,
        country_code: Optional[str] = None,
        region: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius_km: Optional[float] = None,
        max_results: int = 500,
        cursor: Optional[str] = None,
        query_params: Optional[dict] = None,
    ) -> AdapterResult:
        """
        Import businesses from CSV data.

        query_params must contain:
        - csv_content: str — Raw CSV text content
        - field_map: dict (optional) — Custom field mapping
        - delimiter: str (optional) — CSV delimiter (default: ',')
        """
        result = AdapterResult()

        if not query_params:
            result.errors.append(
                self._create_error(
                    "missing_data",
                    "query_params must contain 'csv_content'",
                )
            )
            return result

        csv_content = query_params.get("csv_content", "")
        if not csv_content:
            result.errors.append(
                self._create_error(
                    "missing_data",
                    "csv_content is empty",
                )
            )
            return result

        custom_field_map = query_params.get("field_map", {})
        delimiter = query_params.get("delimiter", ",")

        try:
            # Merge custom field map with defaults
            field_map = {**DEFAULT_FIELD_MAP}
            for key, aliases in custom_field_map.items():
                if key in field_map:
                    field_map[key] = aliases + field_map[key]
                else:
                    field_map[key] = aliases

            # Parse CSV
            reader = csv.DictReader(
                io.StringIO(csv_content),
                delimiter=delimiter,
            )

            # Resolve field names from headers
            if not reader.fieldnames:
                result.errors.append(
                    self._create_error(
                        "parse_error",
                        "CSV has no headers",
                    )
                )
                return result

            header_lower = {h.lower().strip(): h for h in reader.fieldnames}
            resolved_fields = self._resolve_fields(field_map, header_lower)

            logger.info(
                "csv_import_start",
                headers=list(reader.fieldnames),
                resolved=resolved_fields,
            )

            row_number = 0
            for row in reader:
                row_number += 1
                if row_number > max_results:
                    result.has_more = True
                    break

                try:
                    business = self._parse_row(
                        row, row_number, resolved_fields, country_code
                    )
                    if business:
                        result.businesses.append(business)
                except Exception as e:
                    result.errors.append(
                        self._create_error(
                            "parse_error",
                            f"Row {row_number}: {str(e)}",
                            details={"row": row_number},
                            is_retryable=False,
                        )
                    )

            result.total_available = row_number

        except csv.Error as e:
            result.errors.append(
                self._create_error(
                    "parse_error",
                    f"CSV parsing error: {str(e)}",
                    is_retryable=False,
                )
            )
        except Exception as e:
            result.errors.append(
                self._create_error(
                    "unknown",
                    f"Import error: {str(e)}",
                    is_retryable=False,
                )
            )

        logger.info(
            "csv_import_complete",
            businesses=len(result.businesses),
            errors=len(result.errors),
        )

        return result

    def _resolve_fields(
        self,
        field_map: dict[str, list[str]],
        header_map: dict[str, str],
    ) -> dict[str, Optional[str]]:
        """Resolve normalized field names to actual CSV header names."""
        resolved = {}
        for field_key, aliases in field_map.items():
            resolved[field_key] = None
            for alias in aliases:
                if alias.lower() in header_map:
                    resolved[field_key] = header_map[alias.lower()]
                    break
        return resolved

    def _parse_row(
        self,
        row: dict,
        row_number: int,
        fields: dict[str, Optional[str]],
        default_country: Optional[str],
    ) -> Optional[DiscoveredBusiness]:
        """Parse a single CSV row into a DiscoveredBusiness."""

        def get_field(key: str) -> Optional[str]:
            header = fields.get(key)
            if not header:
                return None
            value = row.get(header, "").strip()
            return value if value else None

        name = get_field("name")
        if not name:
            return None  # Name is required

        country = get_field("country") or default_country

        return DiscoveredBusiness(
            source_external_id=f"csv:row:{row_number}",
            raw_data=dict(row),
            name=name,
            address_line_1=get_field("address"),
            city=get_field("city"),
            state_province=get_field("state"),
            postal_code=get_field("postal_code"),
            country_code=country,
            website_url=get_field("website"),
            phone=get_field("phone"),
            email=get_field("email"),
            categories=[get_field("category")] if get_field("category") else [],
        )
