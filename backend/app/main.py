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


# API routers will be included here after they are created
# Example:
# from app.api.endpoints import projects, time_entries
# app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
# app.include_router(time_entries.router, prefix="/api/time-entries", tags=["time-entries"])
