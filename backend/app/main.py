
import logging

from fastapi import FastAPI

from backend.app.core.config import settings
from backend.app.core.logging_config import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="AI-powered business intelligence platform for customer feedback analytics.",
    version=settings.app_version,
)

logger.info("InsightOps application initialised")

@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "message": "Welcome to InsightOps API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    logger.info("Health check requested")

    return {
        "status": "healthy",
        "application": settings.app_name,
    }