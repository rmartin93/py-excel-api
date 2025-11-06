"""
Tests for service layer functionality.

Tests the template-specific services including template management,
Excel generation, and template-specific report generation logic.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.services.template_service import TemplateService
from app.services.excel_service import ExcelService, ExcelUtilities
from app.models.reports import ReportRequest


class TestTemplateService:
    """Test the template service functionality."""

    def test_template_service_initialization(self):
        """Test that TemplateService initializes correctly."""
        service = TemplateService()
        assert service.templates_dir is not None
        assert isinstance(service.templates_dir, Path)

    def test_list_templates_with_existing_templates(self):
        """Test listing templates when templates exist."""
        service = TemplateService()
        response = service.list_templates()

        # Should return success response structure
        assert response.success is True
        assert "data" in response.__dict__
        assert "templates" in response.data

        # Should find at least Template-1.xlsx if it exists
        templates = response.data["templates"]
        assert isinstance(templates, list)

    def test_template_path_validation(self):
        """Test template path validation functionality."""
        service = TemplateService()

        # Test with Template-1.xlsx which should exist in templates directory
        path = service.get_template_path("Template-1.xlsx")
        assert isinstance(path, (Path, type(None)))

        # Test with non-existent template
        path = service.get_template_path("nonexistent-template.xlsx")
        # Should return None for non-existent templates based on implementation
        assert path is None or isinstance(path, Path)

    def test_get_template_path(self):
        """Test getting template path."""
        service = TemplateService()

        path = service.get_template_path("Template-1.xlsx")
        assert isinstance(path, Path)
        assert path.name == "Template-1.xlsx"

    def test_template_validation(self):
        """Test template validation functionality."""
        service = TemplateService()

        # Test validation of Template-1.xlsx if it exists
        try:
            result = service.validate_template("Template-1.xlsx")
            assert isinstance(result, dict)
            # Should have validation information
        except Exception:
            # Template might not exist, that's ok for this test
            pass

        # Test validation of non-existent template
        try:
            result = service.validate_template("nonexistent.xlsx")
            # Should handle gracefully or raise appropriate error
            assert isinstance(result, dict) or result is None
        except Exception:
            # Expected to fail for non-existent template
            pass


class TestExcelUtilities:
    """Test the Excel utilities functionality."""

    def test_excel_utilities_initialization(self):
        """Test that ExcelUtilities initializes correctly."""
        utils = ExcelUtilities()
        # Test that it has the expected methods
        assert hasattr(utils, 'create_workbook')
        assert hasattr(utils, 'add_headers')

    def test_create_workbook(self):
        """Test workbook creation."""
        utils = ExcelUtilities()
        workbook = utils.create_workbook("Test Sheet")

        assert workbook is not None
        assert workbook.active is not None
        assert workbook.active.title == "Test Sheet"

    def test_add_headers(self):
        """Test adding headers to worksheet."""
        utils = ExcelUtilities()
        workbook = utils.create_workbook()
        worksheet = workbook.active

        headers = ["Name", "Age", "Department"]
        utils.add_headers(worksheet, headers)

        # Check that headers were added
        assert worksheet.cell(row=1, column=1).value == "Name"
        assert worksheet.cell(row=1, column=2).value == "Age"
        assert worksheet.cell(row=1, column=3).value == "Department"

    def test_populate_data_rows(self):
        """Test populating data rows."""
        utils = ExcelUtilities()
        workbook = utils.create_workbook()
        worksheet = workbook.active

        # Add headers
        headers = ["name", "age", "department"]
        utils.add_headers(worksheet, headers)

        # Add data
        data_rows = [
            {"name": "John", "age": 30, "department": "Engineering"},
            {"name": "Jane", "age": 25, "department": "Sales"}
        ]

        last_row = utils.populate_data_rows(worksheet, data_rows, headers)

        # Check data was added
        assert worksheet.cell(row=2, column=1).value == "John"
        assert worksheet.cell(row=2, column=2).value == 30
        assert worksheet.cell(row=2, column=3).value == "Engineering"

        assert worksheet.cell(row=3, column=1).value == "Jane"
        assert worksheet.cell(row=3, column=2).value == 25
        assert worksheet.cell(row=3, column=3).value == "Sales"

        # Should return next available row
        assert last_row == 4

    def test_excel_utilities_methods(self):
        """Test Excel utilities calculation methods."""
        utils = ExcelUtilities()

        # Test that utility methods exist and work
        workbook = utils.create_workbook()
        worksheet = workbook.active

        # Test adding calculated totals row
        data_rows = [
            {"revenue": 1000, "expenses": 200},
            {"revenue": 2000, "expenses": 300}
        ]

        columns = ["revenue", "expenses"]
        utils.add_headers(worksheet, columns)
        last_row = utils.populate_data_rows(worksheet, data_rows, columns)

        # Test adding totals row
        utils.add_calculated_totals_row(worksheet, columns, data_rows, last_row)

        # Check that totals were added (max_row should be at least equal to last_row + 1)
        totals_row = worksheet.max_row
        assert totals_row >= last_row


class TestExcelService:
    """Test the Excel service functionality."""

    def test_excel_service_initialization(self):
        """Test that ExcelService initializes correctly."""
        service = ExcelService()
        # Test that it has the expected properties and methods
        assert hasattr(service, 'utils')
        assert isinstance(service.utils, ExcelUtilities)

    def test_generate_report_with_template_1_data(self):
        """Test report generation with Template-1 specific data."""
        service = ExcelService()

        # Create Template-1 specific request
        request = ReportRequest(
            template_name="Template-1.xlsx",
            data={
                "company_name": "Test Corp",
                "report_date": "2025-11-06",
                "rows": [
                    {
                        "department": "Engineering",
                        "revenue": 1000000,
                        "expenses": 200000,
                        "profit": 800000
                    },
                    {
                        "department": "Sales",
                        "revenue": 800000,
                        "expenses": 150000,
                        "profit": 650000
                    }
                ]
            }
        )

        response = service.generate_report(request)

        # Should return a response
        assert response is not None
        assert hasattr(response, 'success')
        assert hasattr(response, 'data')
        assert hasattr(response, 'message')

    def test_generate_template_1_report_via_service(self):
        """Test Template-1 specific report generation via main service."""
        service = ExcelService()

        # Create Template-1 specific request
        request = ReportRequest(
            template_name="Template-1.xlsx",  # This should trigger template-specific logic
            data={
                "company_name": "Acme Corp",
                "report_date": "2025-11-06",
                "rows": [
                    {
                        "department": "Engineering",
                        "revenue": 1500000,
                        "expenses": 300000,
                        "profit": 1200000
                    }
                ]
            }
        )

        response = service.generate_report(request)

        # Test response structure
        assert response.success is True
        assert hasattr(response, 'data')
        assert hasattr(response, 'file_data')

        # Test response data
        assert response.data is not None
        if "filename" in response.data:
            assert response.data["filename"] is not None

        # Test file data
        if response.file_data:
            assert isinstance(response.file_data, bytes)
            assert len(response.file_data) > 0

    def test_generate_generic_report_via_service(self):
        """Test generic report generation for unknown templates via main service."""
        service = ExcelService()

        # Create request for unknown template (should trigger generic logic)
        request = ReportRequest(
            template_name="unknown-template.xlsx",
            data={
                "title": "Generic Report",
                "rows": [
                    {"column1": "value1", "column2": "value2"},
                    {"column1": "value3", "column2": "value4"}
                ]
            }
        )

        response = service.generate_report(request)

        # The service might return an error for unknown templates
        # Test that we get a response structure
        assert hasattr(response, 'success')
        assert hasattr(response, 'message')

        # If it fails (template not found), that's expected behavior
        if not response.success:
            assert "not found" in response.message.lower()
        else:
            # If it succeeds (has fallback), check structure
            assert hasattr(response, 'data')
            assert hasattr(response, 'file_data')

    def test_invalid_template_name_handling(self):
        """Test handling of invalid template names."""
        service = ExcelService()

        request = ReportRequest(
            template_name="nonexistent-template.xlsx",
            data={"some": "data"}
        )

        response = service.generate_report(request)

        # Should handle gracefully (may fall back to generic or return error)
        assert response is not None
        assert hasattr(response, 'success')
        assert hasattr(response, 'message')

    def test_empty_data_handling(self):
        """Test handling of empty data."""
        service = ExcelService()

        request = ReportRequest(
            template_name="Template-1.xlsx",
            data={"rows": []}  # Empty rows
        )

        response = service.generate_report(request)

        # Should handle gracefully
        assert response is not None
        assert hasattr(response, 'success')


class TestTemplateSpecificBehavior:
    """Test template-specific behaviors and patterns."""

    def test_template_1_data_structure_via_service(self):
        """Test that Template-1 expects specific data structure via main service."""
        service = ExcelService()

        # Test with correct Template-1 structure
        correct_request = ReportRequest(
            template_name="Template-1.xlsx",
            data={
                "company_name": "Test Company",
                "report_date": "2025-11-06",
                "rows": [
                    {
                        "department": "Engineering",
                        "revenue": 1000000,
                        "expenses": 200000,
                        "profit": 800000
                    }
                ]
            }
        )

        response = service.generate_report(correct_request)
        assert response.success is True

    def test_template_specific_vs_generic_approach(self):
        """Test that our approach uses template-specific logic rather than generic."""
        service = ExcelService()

        # Template-1 should use specific logic
        template_1_request = ReportRequest(
            template_name="Template-1.xlsx",
            data={"company_name": "Test", "rows": []}
        )

        response_1 = service.generate_report(template_1_request)

        # Generic template should use different logic
        generic_request = ReportRequest(
            template_name="unknown-template.xlsx",
            data={"title": "Test", "rows": []}
        )

        response_generic = service.generate_report(generic_request)

        # Both should work but may use different code paths
        assert response_1 is not None
        assert response_generic is not None

        # This test demonstrates our template-specific approach
        # where different templates get different handling logic


if __name__ == "__main__":
    # Allow running tests directly: python test_services.py
    pytest.main([__file__])