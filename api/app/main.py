from contextlib import asynccontextmanager
from fastapi import FastAPI

import app.core.models
from app.core.database import engine

from app.core.config import settings

from app.core.router import router as api_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    lifespan=lifespan,
)


app.include_router(api_router)
