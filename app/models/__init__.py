"""
Models package for request/response validation.

This module provides clean imports for all Pydantic models used throughout
the application. Similar to TypeScript index files that re-export types.
"""

# Base response models
from .base import (
    BaseResponse,
    SuccessResponse,
    ErrorDetail,
    ErrorResponse,
    MessageResponse,
)

# Health check models
from .health import (
    HealthData,
    HealthResponse,
)

# Template management models
from .templates import (
    TemplateInfo,
    TemplateListResponse,
    SampleDataResponse,
)

# Report generation models
from .reports import (
    ReportRequest,
    ReportResponse,
)

# Export all models for easy importing
__all__ = [
    # Base models
    "BaseResponse",
    "SuccessResponse",
    "ErrorDetail",
    "ErrorResponse",
    "MessageResponse",

    # Health models
    "HealthData",
    "HealthResponse",

    # Template models
    "TemplateInfo",
    "TemplateListResponse",
    "SampleDataResponse",

    # Report models
    "ReportRequest",
    "ReportResponse",
]