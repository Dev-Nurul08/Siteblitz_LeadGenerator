"""
Export discovered businesses as CSV or PDF.

Columns are the stored business fields (no derived or invented values). CSV keeps every
character (UTF-8 with BOM so Excel opens it correctly); PDF is a printable summary table.
"""

import csv
import io
import os
from datetime import datetime, timezone
from typing import Iterable, Optional

from backend.app.models.business import Business

SOCIAL_COLUMNS = ["facebook", "instagram", "linkedin", "tiktok", "youtube", "twitter", "whatsapp", "linktree"]

CSV_COLUMNS = [
    "id", "name", "category", "industry", "address", "city", "state", "postal_code", "country",
    "phone", "email", "website_url", "website_status", *SOCIAL_COLUMNS, "latitude", "longitude",
    "status", "discovered_at",
]

# Spreadsheet apps execute cells that start with these characters as formulas (CSV injection,
# OWASP). Business names, phones ("+91…") and URLs come from outside data, so such cells get a
# leading apostrophe, which Excel/Sheets display as plain text.
_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def _safe_cell(value) -> str:
    if value is None:
        return ""
    text = str(value)
    return "'" + text if text.startswith(_FORMULA_PREFIXES) else text


def business_row(b: Business) -> dict:
    """One flat export row from a Business with locations + categories loaded."""
    location = b.locations[0] if b.locations else None
    category = b.categories[0] if b.categories else None
    socials = b.social_urls or {}
    row = {
        "id": b.id,
        "name": b.name,
        "category": category.category_name if category else None,
        "industry": category.industry_group if category else None,
        "address": location.address_line_1 if location else None,
        "city": location.city if location else None,
        "state": location.state_province if location else None,
        "postal_code": location.postal_code if location else None,
        "country": b.country_code,
        "phone": b.phone,
        "email": b.email,
        "website_url": b.website_url,
        "website_status": b.website_status.value if b.website_status else None,
        "latitude": location.latitude if location else None,
        "longitude": location.longitude if location else None,
        "status": b.status.value if b.status else None,
        "discovered_at": b.discovered_at.isoformat() if b.discovered_at else None,
    }
    for platform in SOCIAL_COLUMNS:
        row[platform] = socials.get(platform)
    return row


def to_csv(rows: Iterable[dict]) -> bytes:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: _safe_cell(row.get(key)) for key in CSV_COLUMNS})
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")


def _pdf_font(pdf) -> tuple[str, bool]:
    """A Unicode TTF when the OS has one (Windows: Arial), else the built-in Latin-1 Helvetica."""
    for path in (r"C:\Windows\Fonts\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(path):
            pdf.add_font("Body", fname=path)
            return "Body", True
    return "Helvetica", False


def to_pdf(rows: list[dict], filters_text: str, generated_at: Optional[datetime] = None) -> bytes:
    """Landscape A4 table: name, category, city, phone, email, website/social, website status."""
    from fpdf import FPDF  # imported lazily: only the PDF export needs it

    generated_at = generated_at or datetime.now(timezone.utc)
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=12)
    font, unicode_ok = _pdf_font(pdf)

    def text(value) -> str:
        value = "" if value is None else str(value)
        # Without a Unicode font, characters outside Latin-1 cannot be drawn; the CSV keeps them.
        return value if unicode_ok else value.encode("latin-1", "replace").decode("latin-1")

    pdf.add_page()
    pdf.set_text_color(23, 24, 26)  # ink #17181a (docs/spec/ui-redesign.md row 3)
    pdf.set_font(font, size=14)
    pdf.cell(0, 8, text("SiteBlitz Lead Generator — businesses export"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(font, size=9)
    pdf.set_text_color(69, 71, 75)  # ink-2 #45474b
    pdf.cell(0, 5, text(f"{len(rows)} businesses · filters: {filters_text or 'none'} · "
                        f"generated {generated_at:%d %b %Y %H:%M} UTC"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    headings = ["Name", "Category", "City", "Phone", "Email", "Website / social", "Website status"]
    widths = [58, 34, 28, 32, 46, 52, 27]  # sums to 277 mm = A4 landscape minus 10 mm margins
    with pdf.table(col_widths=widths, text_align="LEFT", line_height=4.5,
                   first_row_as_headings=False,
                   cell_fill_color=(239, 239, 235), cell_fill_mode="ROWS") as table:
        pdf.set_text_color(23, 24, 26)
        header = table.row()
        for heading in headings:
            header.cell(text(heading))
        for row in rows:
            link = row.get("website_url") or next(
                (row.get(p) for p in SOCIAL_COLUMNS if row.get(p)), None)
            cells = [row.get("name"), row.get("category"), row.get("city"), row.get("phone"),
                     row.get("email"), link,
                     (row.get("website_status") or "").replace("_", " ").capitalize()]
            r = table.row()
            for value in cells:
                r.cell(text(value))
    return bytes(pdf.output())
