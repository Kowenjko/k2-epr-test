from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.database import engine


from app.core.router import router as api_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(api_router)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": "order-service"}
