"""Which businesses a discovery job found - one definition for lists, map, export and checks."""

from sqlalchemy import select, union

from backend.app.models.business import Business, BusinessSourceLink
from backend.app.models.source import SourceJobSighting, SourceRecord


def found_by_job(job_id: int):
    """`Business.id IN (...)` for every business the job found: records it saved first (new and
    dedup-matched) plus records an earlier job had saved and this job found again."""
    record_ids = union(
        select(SourceRecord.id).where(SourceRecord.job_id == job_id),
        select(SourceJobSighting.source_record_id).where(SourceJobSighting.job_id == job_id),
    )
    return Business.id.in_(
        select(BusinessSourceLink.business_id).where(BusinessSourceLink.source_record_id.in_(record_ids))
    )
