"""
Template management routes for the Excel API.
"""

from fastapi import APIRouter, HTTPException, status

from app.core.logging import get_logger
from app.services.template_service import template_service
from app.models.templates import TemplateListResponse

logger = get_logger(__name__)

# Create templates router
router = APIRouter(prefix="/api", tags=["templates"])


@router.get("/templates", response_model=TemplateListResponse, summary="List Templates")
async def list_templates() -> TemplateListResponse:
    """
    List all available Excel templates.

    This endpoint scans the templates directory and returns information
    about available templates including their structure and sample data.

    Returns:
        TemplateListResponse: List of available templates with metadata
    """
    try:
        logger.info("Templates listing requested")

        # Get templates from service
        templates_response = template_service.list_templates()

        if templates_response.success:
            logger.info(f"Found {len(templates_response.data['templates'])} templates")
        else:
            logger.warning(f"Template listing failed: {templates_response.message}")

        return templates_response

    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list templates"
        )