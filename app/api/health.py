"""
Health check routes for the Excel API.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.health import HealthResponse, HealthData

logger = get_logger(__name__)
settings = get_settings()

# Create health router
router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Health Check")
async def health_check() -> HealthResponse:
    """
    Health check endpoint returning API status and version.

    Returns:
        HealthResponse: API health status with version and debug info
    """
    try:
        logger.info("Health check requested")

        health_data = HealthData(
            status="healthy",
            app_name=settings.app_name,
            version=settings.app_version,
            debug=settings.debug,
            timestamp=datetime.now()
        )

        return HealthResponse(
            success=True,
            data=health_data,
            message="API is running successfully"
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed"
        )