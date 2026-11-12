"""
API v1 router — aggregates all v1 route modules.
"""

from fastapi import APIRouter

from backend.app.api.v1.sources import router as sources_router
from backend.app.api.v1.businesses import router as businesses_router
from backend.app.api.v1.discovery import router as discovery_router
from backend.app.api.v1.opportunities import router as opportunities_router
from backend.app.api.v1.contacts import router as contacts_router
from backend.app.api.v1.qualification import router as qualification_router
from backend.app.api.v1.campaigns import router as campaigns_router
from backend.app.api.v1.lead_radar import router as lead_radar_router
from backend.app.api.v1.intelligence import router as intelligence_router
from backend.app.api.v1.outreach import router as outreach_router
from backend.app.api.v1.outreach_sending import router as outreach_sending_router
from backend.app.api.v1.outreach_batches import router as outreach_batches_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(sources_router)
api_v1_router.include_router(businesses_router)
api_v1_router.include_router(discovery_router)
api_v1_router.include_router(opportunities_router)
api_v1_router.include_router(contacts_router)
api_v1_router.include_router(qualification_router)
api_v1_router.include_router(campaigns_router)
api_v1_router.include_router(lead_radar_router)
api_v1_router.include_router(intelligence_router)
api_v1_router.include_router(outreach_router)
api_v1_router.include_router(outreach_sending_router)
api_v1_router.include_router(outreach_batches_router)
