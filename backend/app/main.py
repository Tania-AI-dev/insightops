


from fastapi import FastAPI

from backend.app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="AI-powered business intelligence platform for customer feedback analytics.",
    version=settings.app_version,
)


@app.get("/")
def root():
    return {
        "message": "Welcome to InsightOps API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.app_name,
    }
