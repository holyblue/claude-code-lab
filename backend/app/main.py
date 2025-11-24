"""
FastAPI application entry point.

This is the main application file that creates and configures the FastAPI app.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A time tracking system for recording daily work hours and syncing to TCS",
    debug=settings.DEBUG,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.

    Initializes the database and performs any necessary setup.
    """
    init_db()


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include API routers
from app.api.endpoints import (
    account_groups,
    work_categories,
    projects,
    time_entries,
    stats,
    tcs,
    milestones,
)

app.include_router(
    account_groups.router,
    prefix="/api/account-groups",
    tags=["account-groups"],
)
app.include_router(
    work_categories.router,
    prefix="/api/work-categories",
    tags=["work-categories"],
)
app.include_router(
    projects.router,
    prefix="/api/projects",
    tags=["projects"],
)
app.include_router(
    time_entries.router,
    prefix="/api/time-entries",
    tags=["time-entries"],
)
app.include_router(
    stats.router,
    prefix="/api/stats",
    tags=["statistics"],
)
app.include_router(
    tcs.router,
    prefix="/api/tcs",
    tags=["tcs-format"],
)
app.include_router(
    milestones.router,
    prefix="/api",
    tags=["milestones"],
)
