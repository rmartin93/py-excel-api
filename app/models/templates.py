"""
Template management related models.
"""

from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel, Field, field_validator

from .base import BaseResponse


class TemplateInfo(BaseModel):
    """Information about an Excel template file.

    Similar to a TypeScript interface but with validation:
    interface TemplateInfo {
        name: string;
        filename: string;
        size: number;
        lastModified: string;
        description?: string;
        columns: string[];
        sampleData: Record<string, any>;
    }
    """
    name: str = Field(..., description="Template display name (without .xlsx extension)")
    filename: str = Field(..., description="Full filename including .xlsx extension")
    size: int = Field(..., description="File size in bytes")
    last_modified: datetime = Field(..., description="Last modification timestamp")
    description: str = Field(default="", description="Template description")
    columns: List[str] = Field(default_factory=list, description="Column names found in template")
    sample_data: Dict[str, Any] = Field(default_factory=dict, description="Sample data structure for template")

    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v):
        """Ensure filename has .xlsx extension."""
        if not v.endswith('.xlsx'):
            raise ValueError('Template filename must end with .xlsx')
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Ensure name is not empty."""
        if not v.strip():
            raise ValueError('Template name cannot be empty')
        return v.strip()


class TemplateListResponse(BaseResponse):
    """Response for listing available templates."""
    success: bool = True
    data: Dict[str, List[TemplateInfo]] = Field(..., description="List of available templates")
    message: str = "Templates retrieved successfully"


class SampleDataResponse(BaseResponse):
    """Response containing sample data for testing templates."""
    success: bool = True
    data: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Sample data sets for different templates"
    )
    message: str = "Sample data retrieved successfully"