from fastapi import APIRouter
from app.core.config import settings

from app.modules.system.router import router as system_router

router = APIRouter(prefix=settings.api.prefix)


router.include_router(system_router)
