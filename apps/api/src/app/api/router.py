from fastapi import APIRouter

from app.auth.api import router as auth_router
from app.events.api import router as event_router
from app.gallery.api import router as gallery_router
from app.organization.api import router as organization_router

api_router = APIRouter()

api_router.include_router(organization_router)
api_router.include_router(auth_router)
api_router.include_router(event_router)
api_router.include_router(gallery_router)