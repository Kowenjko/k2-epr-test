from fastapi import APIRouter
from app.core.config import settings

from app.modules.client.router import router as client_router
from app.modules.system.router import router as system_router

router = APIRouter(prefix=settings.api.prefix)

router.include_router(prefix=settings.api.clients, router=client_router)
router.include_router(system_router)
