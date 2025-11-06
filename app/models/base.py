"""
Base response models for consistent API responses.

These models define the standard response format used across all endpoints
as specified in the PRD.
"""

from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Base response model that all API responses should inherit from.

    This ensures consistent response format across all endpoints
    as specified in the PRD.
    """
    success: bool
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


class SuccessResponse(BaseResponse):
    """Standard success response format."""
    success: bool = True
    data: Dict[str, Any]


class ErrorDetail(BaseModel):
    """Error details structure for consistent error responses."""
    code: str
    message: str
    details: str | None = None


class ErrorResponse(BaseResponse):
    """Standard error response format."""
    success: bool = False
    error: ErrorDetail


class MessageResponse(BaseResponse):
    """Simple response with just a message (no data)."""
    success: bool = True
    data: Dict[str, str] = Field(default_factory=dict)