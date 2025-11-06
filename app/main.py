"""
Main FastAPI application entry point.

This is the equivalent of app.js in an Express application, but with
FastAPI's built-in features like automatic API documentation, request
validation, and dependency injection.
"""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.core.config import settings
from app.core.logging import get_logger, log_request

# Initialize logger for this module
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events.

    This is like Express middleware that runs on app start/stop.
    FastAPI uses this pattern instead of separate startup/shutdown decorators.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"API prefix: {settings.api_prefix}")

    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Python API for Excel report generation from templates",
    debug=settings.debug,
    lifespan=lifespan,
    # API documentation will be available at /docs
    docs_url="/docs",
    redoc_url="/redoc",
)


# CORS Middleware (like cors package in Express)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Custom Exception Handlers (PRD-compliant error format)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions with standardized error format.

    Returns errors in the format specified in the PRD:
    {
        "success": false,
        "error": {
            "code": "HTTP_404",
            "message": "Not found",
            "details": null
        },
        "timestamp": "2025-11-04T10:30:00Z"
    }
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "details": None
            },
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions with standardized error format.

    Logs the full error details but returns safe error message to client.
    """
    # Log the full error for debugging
    logger.error(f"Unexpected error in {request.method} {request.url.path}: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": str(exc) if settings.debug else None
            },
            "timestamp": datetime.now().isoformat()
        }
    )


# Request logging middleware (like morgan in Express)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing information."""
    start_time = datetime.now()

    # Process the request
    response = await call_next(request)

    # Calculate duration
    duration = (datetime.now() - start_time).total_seconds() * 1000

    # Log the request
    log_request(
        method=request.method,
        path=str(request.url.path),
        status_code=response.status_code,
        duration_ms=duration
    )

    return response


# Basic health check endpoint (we'll add more routes later)
@app.get("/api/health")
async def main_health_check() -> dict[str, Any]:
    """Health check endpoint.

    Returns basic application status and information.
    This follows the PRD success response format.
    """
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "debug": settings.debug,
            "timestamp": datetime.now().isoformat()
        },
        "message": "API is running successfully",
        "timestamp": datetime.now().isoformat()
    }


# Root endpoint
@app.get("/")
async def root() -> dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "success": True,
        "data": {
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs",
            "health": "/api/health"
        },
        "message": "API root endpoint",
        "timestamp": datetime.now().isoformat()
    }


# Include API routers (organized by domain)
from app.api.health import router as health_router
from app.api.templates import router as templates_router
from app.api.reports import router as reports_router

app.include_router(health_router)
app.include_router(templates_router)
app.include_router(reports_router)


if __name__ == "__main__":
    # This allows running the app with: python -m app.main
    # Similar to: node app.js
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,  # Auto-reload on file changes (like nodemon)
        log_level=settings.log_level.lower()
    )