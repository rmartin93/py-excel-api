"""
Report generation routes for the Excel API.
"""

from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import StreamingResponse
import io

from app.core.logging import get_logger
from app.services.excel_service import excel_service
from app.models.reports import ReportRequest

logger = get_logger(__name__)

# Create reports router
router = APIRouter(prefix="/api", tags=["reports"])


@router.post("/reports/1", summary="Generate Template-1 Report")
async def generate_template_1_report(data: Dict[str, Any]) -> Response:
    """
    Generate a report using Template-1.xlsx (Financial Cost Center Report).

    This endpoint is specific to Template-1.xlsx and expects data in the format:
    {
        "rows": [
            {
                "Rule ID": "RULE001",
                "Cost Center Group": "IT Department",
                "Pool Amount": 50000.00,
                "AB/CR Amount": 12500.00,
                "Base Amount": 45000.00,
                "Actual Rate": 0.25,
                "FP Rate": 0.22,
                "AB/CR Rate Diff": 0.03
            }
        ]
    }

    Args:
        data: Report data with rows array containing financial data

    Returns:
        StreamingResponse: Excel file download
    """
    try:
        logger.info("Template-1 report generation requested")
        logger.debug(f"Data rows: {len(data.get('rows', []))}")

        # Create ReportRequest for Template-1
        request = ReportRequest(
            template_name="Template-1.xlsx",
            data=data
        )

        # Generate the report using excel service
        report_response = excel_service.generate_report(request)

        if not report_response.success:
            logger.error(f"Template-1 report generation failed: {report_response.message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=report_response.message
            )

        if not report_response.file_data:
            logger.error("Template-1 report generated but no file data returned")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Report generation completed but no file data available"
            )

        # Create filename for download
        filename = report_response.data.get("filename", "template_1_report.xlsx")

        logger.info(f"Template-1 report generated successfully: {filename} ({report_response.data.get('size')} bytes)")

        # Return Excel file as download
        return StreamingResponse(
            io.BytesIO(report_response.file_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(report_response.file_data))
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating Template-1 report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating the Template-1 report"
        )


@router.get("/reports/1b", summary="Generate Template-1 Report from Database (Production Pattern)")
async def generate_template_1_report_from_db() -> Response:
    """
    PRODUCTION PATTERN: GET endpoint that fetches data from database and generates Template-1 report

    This shows how you'd structure a production endpoint that:
    1. Accepts query parameters for filtering/options
    2. Queries your database for the data
    3. Transforms the data for the template
    4. Generates and returns the Excel file

    This is the typical production pattern where the API fetches data rather than
    receiving it in a POST body.

    TODO: Replace the mock implementation with actual database integration
    """
    try:
        logger.info("Template-1 database report generation requested (PRODUCTION PATTERN)")

        # STEP 1: Parse query parameters (add as function parameters as needed)
        # In production, you'd add query parameters like:
        #
        # async def generate_template_1_report_from_db(
        #     date_range: str = Query(None, description="Date range filter YYYY-MM-DD to YYYY-MM-DD"),
        #     cost_center: str = Query(None, description="Filter by cost center"),
        #     rule_ids: List[str] = Query(None, description="Filter by specific rule IDs"),
        #     format_numbers: bool = Query(True, description="Apply number formatting"),
        #     db: DatabaseService = Depends(get_database)
        # ):

        # STEP 2: Database Query Setup & Execution
        # Example of what your database query might look like:
        #
        # query = """
        #     SELECT
        #         rule_id as "Rule ID",
        #         cost_center_group as "Cost Center Group",
        #         pool_amount as "Pool Amount",
        #         abcr_amount as "AB/CR Amount",
        #         base_amount as "Base Amount",
        #         actual_rate as "Actual Rate",
        #         fp_rate as "FP Rate",
        #         (actual_rate - fp_rate) as "AB/CR Rate Diff"
        #     FROM financial_reports
        #     WHERE 1=1
        #       AND (:date_range IS NULL OR report_date BETWEEN :start_date AND :end_date)
        #       AND (:cost_center IS NULL OR cost_center_group = :cost_center)
        #       AND (:rule_ids IS NULL OR rule_id = ANY(:rule_ids))
        #     ORDER BY rule_id
        # """
        #
        # db_results = await db.fetch_all(query, {
        #     "date_range": date_range,
        #     "start_date": parse_date_range(date_range)[0] if date_range else None,
        #     "end_date": parse_date_range(date_range)[1] if date_range else None,
        #     "cost_center": cost_center,
        #     "rule_ids": rule_ids
        # })

        # STEP 3: Transform Database Results to Template Format
        # Convert your database results to the exact format Template-1 expects:
        #
        # report_rows = []
        # for row in db_results:
        #     report_rows.append({
        #         "Rule ID": row["Rule ID"],
        #         "Cost Center Group": row["Cost Center Group"],
        #         "Pool Amount": float(row["Pool Amount"]) if row["Pool Amount"] else 0.0,
        #         "AB/CR Amount": float(row["AB/CR Amount"]) if row["AB/CR Amount"] else 0.0,
        #         "Base Amount": float(row["Base Amount"]) if row["Base Amount"] else 0.0,
        #         "Actual Rate": float(row["Actual Rate"]) if row["Actual Rate"] else 0.0,
        #         "FP Rate": float(row["FP Rate"]) if row["FP Rate"] else 0.0,
        #         "AB/CR Rate Diff": float(row["AB/CR Rate Diff"]) if row["AB/CR Rate Diff"] else 0.0
        #     })

        # MOCK DATA for demonstration (replace with actual database query above)
        logger.info("Fetching Template-1 data from database (MOCK - replace with real DB query)")

        mock_db_results = [
            {
                "Rule ID": "DB_RULE_001",
                "Cost Center Group": "Finance Department",
                "Pool Amount": 125000.00,
                "AB/CR Amount": 31250.00,
                "Base Amount": 112500.00,
                "Actual Rate": 0.28,
                "FP Rate": 0.25,
                "AB/CR Rate Diff": 0.03
            },
            {
                "Rule ID": "DB_RULE_002",
                "Cost Center Group": "Operations",
                "Pool Amount": 200000.00,
                "AB/CR Amount": 50000.00,
                "Base Amount": 180000.00,
                "Actual Rate": 0.32,
                "FP Rate": 0.30,
                "AB/CR Rate Diff": 0.02
            },
            {
                "Rule ID": "DB_RULE_003",
                "Cost Center Group": "Human Resources",
                "Pool Amount": 85000.00,
                "AB/CR Amount": 21250.00,
                "Base Amount": 76500.00,
                "Actual Rate": 0.26,
                "FP Rate": 0.24,
                "AB/CR Rate Diff": 0.02
            }
        ]

        # STEP 4: Create ReportRequest with database data
        request = ReportRequest(
            template_name="Template-1.xlsx",
            data={"rows": mock_db_results}
        )

        # STEP 5: Generate Excel report using existing service
        report_response = excel_service.generate_report(request)

        if not report_response.success:
            logger.error(f"Template-1 database report generation failed: {report_response.message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=report_response.message
            )

        if not report_response.file_data:
            logger.error("Template-1 database report generated but no file data returned")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Report generation completed but no file data available"
            )

        # STEP 6: Return file download with descriptive filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"template_1_db_report_{timestamp}.xlsx"

        logger.info(f"Template-1 database report generated: {filename} ({report_response.data.get('size')} bytes)")

        return StreamingResponse(
            io.BytesIO(report_response.file_data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(report_response.file_data))
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating Template-1 database report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating the database report"
        )


# PRODUCTION DATABASE INTEGRATION EXAMPLES:
# ==========================================
#
# 1. Add these imports to the top of this file:
#    from fastapi import Query, Depends
#    from typing import List, Optional
#    from app.database import get_database
#    from app.services.database_service import DatabaseService
#
# 2. Create a database service (app/services/database_service.py):
#    ```python
#    class DatabaseService:
#        def __init__(self, connection):
#            self.connection = connection
#
#        async def fetch_template_1_data(self, filters: dict) -> List[dict]:
#            # Execute your SQL query here
#            # Return list of dictionaries matching Template-1 column structure
#            pass
#    ```
#
# 3. Add query parameter models (app/models/queries.py):
#    ```python
#    class Template1QueryParams(BaseModel):
#        date_range: Optional[str] = Field(None, description="YYYY-MM-DD to YYYY-MM-DD")
#        cost_center: Optional[str] = Field(None, description="Filter by cost center")
#        rule_ids: Optional[List[str]] = Field(None, description="Filter by rule IDs")
#        include_totals: bool = Field(True, description="Include totals row")
#    ```
#
# 4. Example with dependency injection:
#    ```python
#    async def generate_template_1_report_from_db(
#        date_range: str = Query(None, description="Date range YYYY-MM-DD to YYYY-MM-DD"),
#        cost_center: str = Query(None, description="Filter by cost center"),
#        rule_ids: List[str] = Query(None, description="Filter by rule IDs"),
#        format_numbers: bool = Query(True, description="Apply formatting"),
#        db: DatabaseService = Depends(get_database)
#    ):
#        # Build filters dict
#        filters = {
#            "date_range": date_range,
#            "cost_center": cost_center,
#            "rule_ids": rule_ids
#        }
#
#        # Fetch data from database
#        db_data = await db.fetch_template_1_data(filters)
#
#        # Generate report with fetched data
#        # ... rest of report generation logic
#    ```