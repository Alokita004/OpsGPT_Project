from fastapi import FastAPI
from app.api.routes import health, incidents
from app.config.settings import Settings
from app.utils.logging import configure_logging


settings = Settings()
configure_logging(settings)

app = FastAPI(title="OpsGPT", version="0.1.0")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/ready")
async def readiness_check():
    return {"status": "ready"}


# Include routers
app.include_router(health.router, prefix="/", tags=["health"])
app.include_router(incidents.router, prefix="/api/v1", tags=["incidents"])
