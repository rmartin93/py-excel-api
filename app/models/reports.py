"""
Report generation related models.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, field_validator

from .base import BaseResponse


class ReportRequest(BaseModel):
    """Request model for generating Excel reports.

    This is like a TypeScript interface for the POST body:
    interface ReportRequest {
        template_name: string;
        data: Record<string, any>;
    }
    """
    template_name: str = Field(
        description="Name of the template to use (with or without .xlsx extension)",
        examples=["annual-report", "Template-1.xlsx"]
    )
    data: Dict[str, Any] = Field(
        description="Data to fill into the template placeholders",
        examples=[{
            "company_name": "Acme Corp",
            "year": 2025,
            "revenue": 1000000,
            "employees": [
                {"name": "John Doe", "department": "Engineering"},
                {"name": "Jane Smith", "department": "Sales"}
            ]
        }]
    )

    @field_validator('template_name')
    @classmethod
    def validate_template_name(cls, v):
        """Normalize template name and ensure it's valid."""
        v = v.strip()
        if not v:
            raise ValueError('Template name cannot be empty')

        # Add .xlsx extension if not present
        if not v.endswith('.xlsx'):
            v += '.xlsx'

        # Basic filename validation
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(char in v for char in invalid_chars):
            raise ValueError(f'Template name contains invalid characters: {invalid_chars}')

        return v

    @field_validator('data')
    @classmethod
    def validate_data(cls, v):
        """Ensure data is not empty."""
        if not v:
            raise ValueError('Data cannot be empty')
        return v


class ReportResponse(BaseResponse):
    """Response for successful report generation.

    Note: The actual Excel file will be returned as a file download,
    but this response provides metadata about the generated report.
    """
    success: bool = True
    data: Dict[str, Any] = Field(
        description="Report generation metadata",
        examples=[{
            "filename": "annual-report-2025-11-04.xlsx",
            "template_used": "annual-report.xlsx",
            "generation_time_ms": 1250.5,
            "file_size_bytes": 52048
        }]
    )
    message: str = "Report generated successfully"
    file_data: Optional[bytes] = Field(
        None,
        description="Binary Excel file data for download"
    )