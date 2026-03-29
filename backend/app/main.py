from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.research import router as research_router
from app.api.routes.trades import router as trades_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="OTO Research & Trading API",
    version=settings.app_version,
    description="Starter API for 5Y company research and paper trading.",
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(research_router, prefix=settings.api_prefix)
app.include_router(trades_router, prefix=settings.api_prefix)
