# Product Requirements Document (PRD)

## Core API Infrastructure and Basic Excel Report Generation

**Document Version:** 1.0
**Date:** November 4, 2025
**Project:** py-excel-api
**PRD Type:** Core Infrastructure (Phase 1)

---

## 1. Introduction/Overview

This PRD defines the core infrastructure and basic Excel report generation functionality for the Python Excel API. This represents the foundational phase of development, focusing on establishing the API framework, basic template processing, and sample data integration. The goal is to create a working API that can generate Excel reports from templates using sample data, providing the foundation for future enhancements.

**Problem Statement:** Manual Excel report generation is time-consuming and error-prone. The existing TypeScript solution has limitations with Excel manipulation that Python libraries can potentially solve better.

**Goal:** Create a robust Python API foundation that can generate Excel reports from templates with sample data, setting the stage for future MS SQL integration and production deployment.

---

## 2. Goals

1. **Establish API Foundation**: Create a working FastAPI application with proper project structure
2. **Basic Excel Generation**: Successfully generate Excel files from templates using sample data
3. **Template Management**: Implement file-based template storage and retrieval system
4. **Error Handling**: Implement comprehensive error handling and logging framework
5. **Development Environment**: Create a development-ready environment for iterative enhancement
6. **Documentation**: Provide auto-generated API documentation for developer integration

---

## 3. User Stories

### Developer Stories

-   **As a developer**, I want to call a REST API endpoint with sample data so that I can generate an Excel report programmatically
-   **As a developer**, I want to see auto-generated API documentation so that I can understand available endpoints and parameters
-   **As a developer**, I want clear error messages when something goes wrong so that I can debug integration issues quickly
-   **As a developer**, I want to list available templates so that I can understand what reports are available

### System Administrator Stories

-   **As a system administrator**, I want comprehensive logging so that I can troubleshoot issues and monitor API usage
-   **As a system administrator**, I want the API to handle errors gracefully so that one bad request doesn't crash the entire service

### Business User Stories (Future)

-   **As a business user**, I want automated report generation so that I can focus on analysis rather than manual Excel work
-   **As a business user**, I want generated reports to maintain proper formatting so that they meet submission requirements

---

## 4. Functional Requirements

### 4.1 API Infrastructure

1. **FR-1.1**: The system must use FastAPI framework for web service implementation
2. **FR-1.2**: The system must provide auto-generated OpenAPI documentation accessible at `/docs`
3. **FR-1.3**: The system must implement proper HTTP status codes (200, 400, 404, 500, etc.)
4. **FR-1.4**: The system must support JSON request and response formats
5. **FR-1.5**: The system must include CORS middleware configuration for future domain restrictions
6. **FR-1.6**: The system must implement request/response logging middleware

### 4.2 Template Management

7. **FR-2.1**: The system must read Excel templates from a `/templates/` directory in the project root
8. **FR-2.2**: The system must support `.xlsx` file format for templates
9. **FR-2.3**: The system must validate template file existence before processing
10. **FR-2.4**: The system must provide an endpoint to list available templates: `GET /api/templates`
11. **FR-2.5**: The system must return template metadata (filename, last modified, size)
12. **FR-2.6**: The system must handle template file access errors gracefully

### 4.3 Excel Processing

13. **FR-3.1**: The system must use `openpyxl` library for Excel file manipulation
14. **FR-3.2**: The system must preserve original template formatting when inserting data
15. **FR-3.3**: The system must support placeholder replacement in template cells (e.g., `{{field_name}}`)
16. **FR-3.4**: The system must handle multiple worksheets within a single template
17. **FR-3.5**: The system must support dynamic table row insertion for data arrays
18. **FR-3.6**: The system must maintain conditional formatting from original templates

### 4.4 Data Processing

19. **FR-4.1**: The system must accept JSON data payloads for report generation
20. **FR-4.2**: The system must validate required data fields for each template
21. **FR-4.3**: The system must provide meaningful error messages for missing or invalid data
22. **FR-4.4**: The system must support nested JSON objects for complex data structures
23. **FR-4.5**: The system must handle data type conversion (string, number, date) for Excel cells
24. **FR-4.6**: The system must include sample data sets for testing and development

### 4.5 Report Generation API

25. **FR-5.1**: The system must provide POST endpoint: `POST /api/reports/generate`
26. **FR-5.2**: The system must accept parameters: `template_name` and `data` in request body
27. **FR-5.3**: The system must return generated Excel file as downloadable attachment
28. **FR-5.4**: The system must set proper Content-Type header: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
29. **FR-5.5**: The system must set Content-Disposition header with meaningful filename
30. **FR-5.6**: The system must clean up temporary files after response is sent

### 4.6 Error Handling and Logging

31. **FR-6.1**: The system must implement global exception handler for uncaught errors
32. **FR-6.2**: The system must log all errors to both console and rotating log files
33. **FR-6.3**: The system must use structured logging with timestamp, level, and context
34. **FR-6.4**: The system must create log files in `/logs/` directory with date rotation
35. **FR-6.5**: The system must return standardized error response format with error codes
36. **FR-6.6**: The system must log request details (method, path, user agent) for debugging

### 4.7 Health and Monitoring

37. **FR-7.1**: The system must provide health check endpoint: `GET /api/health`
38. **FR-7.2**: The system must return API version and status in health check response
39. **FR-7.3**: The system must validate template directory accessibility in health check
40. **FR-7.4**: The system must validate Excel library functionality in health check

---

## 5. Non-Goals (Out of Scope)

-   **Windows Authentication**: Will be implemented in Phase 2
-   **MS SQL Database Integration**: Will be implemented in Phase 3
-   **Windows IIS Deployment**: Development environment only for Phase 1
-   **Advanced Excel Features**: Charts, pivot tables, and complex formatting in later phases
-   **User Interface**: API-only, no web interface
-   **Real-time Features**: No WebSocket or real-time updates
-   **Multi-tenancy**: Single instance, no tenant isolation
-   **Advanced Security**: Basic error handling only, no advanced security features

---

## 6. Design Considerations

### 6.1 Project Structure

```
py-excel-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models for request/response
│   ├── services/
│   │   ├── __init__.py
│   │   ├── template_service.py    # Template management logic
│   │   └── excel_service.py       # Excel generation logic
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API endpoint definitions
│   └── core/
│       ├── __init__.py
│       ├── config.py        # Configuration management
│       └── logging.py       # Logging configuration
├── templates/               # Excel template files
├── logs/                   # Log file directory
├── tests/                  # Unit and integration tests
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

### 6.2 API Response Format

```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully",
  "timestamp": "2025-11-04T10:30:00Z"
}
```

### 6.3 Error Response Format

```json
{
	"success": false,
	"error": {
		"code": "TEMPLATE_NOT_FOUND",
		"message": "Template 'annual-report.xlsx' not found",
		"details": "Check available templates at /api/templates"
	},
	"timestamp": "2025-11-04T10:30:00Z"
}
```

---

## 7. Technical Considerations

### 7.1 Required Dependencies

```python
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Excel Processing
openpyxl==3.1.2

# Data Validation
pydantic==2.5.0

# Logging and Utilities
python-multipart==0.0.6
```

### 7.2 Excel Library Choice

-   **Primary**: `openpyxl` for full Excel feature support and active maintenance
-   **Rationale**: Better formatting preservation, multiple worksheet support, and extensive documentation
-   **Alternative**: `xlsxwriter` if write-only performance becomes critical

### 7.3 Template Placeholder Format

-   **Standard Format**: `{{field_name}}` for simple field replacement
-   **Array Format**: `{{#items}}...{{/items}}` for repeating data (future enhancement)
-   **Conditional Format**: `{{?condition}}...{{/condition}}` for conditional content (future enhancement)

### 7.4 Configuration Management

-   Use environment variables for configuration (development vs production)
-   Support for `.env` files in development
-   Configuration validation using Pydantic settings

---

## 8. Success Metrics

### 8.1 Technical Metrics

-   **API Response Time**: < 5 seconds for basic report generation
-   **Template Processing**: Successfully process at least 3 different template formats
-   **Error Rate**: < 5% of requests result in 500 errors
-   **Documentation Coverage**: 100% of endpoints documented in OpenAPI

### 8.2 Development Metrics

-   **Code Coverage**: > 80% test coverage for core functionality
-   **Development Setup**: New developer can set up and run locally in < 30 minutes
-   **Template Creation**: Business user can create a new template and test it in < 1 hour

### 8.3 Functionality Metrics

-   **Sample Data Integration**: Successfully generate reports with 5 different sample datasets
-   **Excel Output Quality**: Generated files open correctly in Excel and maintain formatting
-   **Error Handling**: Clear error messages for all common failure scenarios

---

## 9. Open Questions

1. **Template Validation**: Should we validate template structure on startup or per-request?
2. **File Cleanup**: How long should generated files be kept before cleanup?
3. **Sample Data Format**: Should sample data be JSON files, Python dictionaries, or database fixtures?
4. **Testing Strategy**: Should we include actual Excel files in tests or mock the Excel generation?
5. **Performance Baseline**: What's the acceptable file size limit for generated Excel files?
6. **Development Database**: Should we include SQLite for development even though production uses MS SQL?

---

## 10. Implementation Notes for Junior Developer

### 10.1 Getting Started Checklist

1. Set up Python 3.13+ virtual environment
2. Install dependencies from requirements.txt
3. Create basic FastAPI application structure
4. Implement health check endpoint first
5. Add template listing functionality
6. Create basic Excel generation with sample data
7. Implement comprehensive error handling
8. Add logging and monitoring
9. Write unit tests for core functionality
10. Document API endpoints

### 10.2 Development Tips

-   **Start Simple**: Begin with a single template and hardcoded sample data
-   **Test Early**: Create test endpoints to verify Excel generation before building full API
-   **Log Everything**: Add extensive logging to understand data flow during development
-   **Validate Input**: Use Pydantic models to validate all request data
-   **Handle Errors**: Assume everything will fail and handle gracefully

### 10.3 Testing Approach

-   Create sample Excel templates with various formatting
-   Use pytest for unit testing
-   Test Excel generation with real files, not mocks
-   Include integration tests for full request/response cycle
-   Test error conditions (missing templates, invalid data, etc.)

---

**Next Steps**: After this PRD is implemented, proceed to Phase 2 (Windows Authentication) and Phase 3 (MS SQL Integration) PRDs.
