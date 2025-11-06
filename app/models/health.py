"""
Health check related models.
"""

from datetime import datetime
from pydantic import BaseModel

from .base import BaseResponse


class HealthData(BaseModel):
    """Health check response data structure."""
    status: str = "healthy"
    app_name: str
    version: str
    debug: bool
    timestamp: datetime


class HealthResponse(BaseResponse):
    """Health check endpoint response."""
    success: bool = True
    data: HealthData
    message: str = "API is running successfully"