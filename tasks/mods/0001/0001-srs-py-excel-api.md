# Software Requirements Specification (SRS)

## Python Excel API for Government Report Generation

**Document Version:** 1.0
**Date:** November 4, 2025
**Project:** py-excel-api

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the requirements for a Python-based API that generates Excel reports from templates and data sources. The system will serve as a replacement for an existing TypeScript/Express implementation, with enhanced Excel manipulation capabilities and eventual deployment to Windows IIS with MS SQL database integration.

### 1.2 Scope

The Python Excel API will:

-   Generate Excel reports using predefined templates stored in the project
-   Fill templates with sample data initially, with future MS SQL database connectivity
-   Support complex Excel features including formatting, dynamic tables, and multiple worksheets
-   Provide a RESTful API interface for developers and automated report generation
-   Handle Windows Authentication for enterprise deployment
-   Include comprehensive error handling and logging capabilities

The system will NOT:

-   Provide a user interface for template creation (templates managed as files)
-   Handle real-time collaboration features
-   Support non-Excel output formats in the initial version

### 1.3 Definitions, Acronyms, and Abbreviations

-   **API**: Application Programming Interface
-   **IIS**: Internet Information Services (Microsoft web server)
-   **MS SQL**: Microsoft SQL Server
-   **SRS**: Software Requirements Specification
-   **Template**: Pre-formatted Excel file with placeholders for data insertion
-   **Windows Auth**: Windows Authentication system

### 1.4 References

-   Original TypeScript/Express implementation (reference for feature parity)
-   ExcelJS library (previous solution with known limitations)
-   Python 3.13.3 (target deployment version)

---

## 2. Overall Description

### 2.1 Product Perspective

This is a standalone Python API that will replace an existing TypeScript/Express solution. The system is designed to integrate with:

-   Windows IIS web server environment
-   MS SQL Server databases (future phase)
-   Existing PHP and Node.js applications on the same server
-   Frontend applications using the API for automated report generation

### 2.2 Product Functions

The main functions of the system include:

-   **Template Management**: Store and access Excel templates from project filesystem
-   **Data Processing**: Accept and validate data for report generation
-   **Excel Generation**: Create Excel files with complex formatting, dynamic tables, and multiple worksheets
-   **API Services**: Provide RESTful endpoints for report generation requests
-   **Authentication**: Integrate with Windows Authentication for user identification
-   **Error Handling**: Comprehensive logging and error management
-   **Database Connectivity**: Future integration with MS SQL Server (utility framework)

### 2.3 User Characteristics

**Primary Users:**

-   **Developers**: Technical users who integrate the API into applications for automated report generation
-   **Business Users**: Government report submission personnel who need annual compliance reports

**User Expertise:**

-   Developers: Intermediate to advanced technical skills
-   Business Users: Basic to intermediate Excel knowledge, minimal technical background

**Usage Patterns:**

-   Medium volume: 10-100 reports per day
-   Seasonal peaks during government submission periods
-   Primarily automated generation with some manual triggers

### 2.4 Constraints

**Technical Constraints:**

-   Must deploy on Windows IIS with Python 3.13.3
-   Must coexist with existing PHP and Node.js applications
-   Must handle CORS for specific domains
-   Must integrate with Windows Authentication
-   Limited to Excel format output initially

**Business Constraints:**

-   Government compliance requirements for report formats
-   Annual submission deadlines creating time-sensitive requirements
-   Template formats dictated by external government agencies

### 2.5 Assumptions and Dependencies

**Assumptions:**

-   Windows Authentication infrastructure is available and properly configured
-   Excel templates will be provided in standardized formats
-   Government report requirements will remain relatively stable
-   Python 3.13.3 runtime will be available on deployment server

**Dependencies:**

-   Windows IIS server environment
-   Windows Authentication system
-   MS SQL Server (future phase)
-   Excel template files provided by business users
-   Python Excel manipulation library (to be selected)

---

## 3. System Features

### Feature 1: Excel Template Processing

**Description:** Load and process Excel templates from the filesystem to prepare them for data insertion.

**Functional Requirements:**

1. FR-1.1: System shall read Excel template files from a designated templates directory
2. FR-1.2: System shall support .xlsx file format templates
3. FR-1.3: System shall identify placeholder markers within template cells
4. FR-1.4: System shall preserve all original formatting, styles, and structure
5. FR-1.5: System shall support templates with multiple worksheets
6. FR-1.6: System shall validate template integrity before processing

### Feature 2: Data Integration and Validation

**Description:** Accept and validate data from various sources for insertion into Excel templates.

**Functional Requirements:** 2. FR-2.1: System shall accept sample/mock data for initial implementation 2. FR-2.2: System shall provide data validation for report generation endpoints 3. FR-2.3: System shall include framework for future MS SQL database connectivity 4. FR-2.4: System shall handle data type validation for Excel cell insertion 5. FR-2.5: System shall support streaming data processing for large datasets 6. FR-2.6: System shall provide clear error messages for data validation failures

### Feature 3: Excel Report Generation

**Description:** Generate Excel files by combining templates with validated data.

**Functional Requirements:**

1. FR-3.1: System shall insert data into template placeholders while preserving formatting
2. FR-3.2: System shall support dynamic table sizing based on data volume
3. FR-3.3: System shall maintain conditional formatting rules from templates
4. FR-3.4: System shall support pivot table generation and updates
5. FR-3.5: System shall handle multiple worksheets within a single output file
6. FR-3.6: System shall return generated Excel files via HTTP response

### Feature 4: RESTful API Interface

**Description:** Provide HTTP endpoints for report generation and system management.

**Functional Requirements:**

1. FR-4.1: System shall provide POST endpoints for report generation requests
2. FR-4.2: System shall accept JSON payloads for data input
3. FR-4.3: System shall return Excel files as downloadable attachments
4. FR-4.4: System shall provide endpoint for listing available templates
5. FR-4.5: System shall include API documentation (auto-generated)
6. FR-4.6: System shall handle CORS for specified domains

### Feature 5: Authentication and Authorization

**Description:** Integrate with Windows Authentication for user identification and access control.

**Functional Requirements:**

1. FR-5.1: System shall extract username from Windows Authentication headers
2. FR-5.2: System shall use Windows username for audit logging
3. FR-5.3: System shall reject requests without valid Windows Authentication
4. FR-5.4: System shall provide framework for future role-based permissions
5. FR-5.5: System shall maintain user context throughout request processing

### Feature 6: Error Handling and Logging

**Description:** Comprehensive error management and logging system for troubleshooting and monitoring.

**Functional Requirements:**

1. FR-6.1: System shall log all errors to console output
2. FR-6.2: System shall log all errors to rotating log files
3. FR-6.3: System shall include global error handler for uncaught exceptions
4. FR-6.4: System shall provide framework for future database error logging
5. FR-6.5: System shall include structured logging with severity levels
6. FR-6.6: System shall capture user context in error logs

---

## 4. External Interface Requirements

### 4.1 User Interfaces

**API Documentation Interface:**

-   Auto-generated API documentation accessible via web browser
-   Interactive endpoint testing capabilities
-   Clear parameter descriptions and example requests/responses

**File Management:**

-   Template files managed through filesystem (no UI required)
-   Generated reports delivered via HTTP download

### 4.2 Hardware Interfaces

Not applicable - software-only solution.

### 4.3 Software Interfaces

**Windows IIS Integration:**

-   Deploy as Python web application under IIS
-   Integrate with IIS request pipeline
-   Support IIS application pools and process management

**Windows Authentication:**

-   Interface: HTTP headers (REMOTE_USER, AUTH_USER)
-   Protocol: Windows Integrated Authentication
-   Data format: Domain\Username or Username format

**Excel File System:**

-   Interface: Local filesystem I/O
-   File formats: .xlsx (input templates), .xlsx (output files)
-   Directory structure: /templates/ for input, temporary directories for output

**Future MS SQL Integration:**

-   Interface: Database connection pooling
-   Protocol: SQL Server Native Client or ODBC
-   Authentication: Windows Authentication or SQL Server authentication

### 4.4 Communications Interfaces

**HTTP/HTTPS Protocol:**

-   RESTful API endpoints
-   JSON request/response format
-   Support for multipart file uploads (future)
-   CORS headers for specified domains

**File Transfer:**

-   Excel file download via HTTP response
-   Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
-   Content-Disposition: attachment with filename

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

-   **Response Time**: API endpoints shall respond within 5 seconds for typical report generation
-   **Throughput**: System shall handle 10-100 concurrent report generation requests per day
-   **Memory Usage**: System shall use streaming processing for datasets to avoid memory issues
-   **File Size**: System shall efficiently handle Excel files up to 50MB in size

### 5.2 Security Requirements

-   **Authentication**: All API endpoints require valid Windows Authentication
-   **Authorization**: Username extraction for audit trails and future role-based access
-   **Data Protection**: Sensitive data in logs shall be masked or excluded
-   **CORS**: Restricted to specific domains only
-   **File Security**: Generated reports shall not persist on server beyond request completion

### 5.3 Usability Requirements

-   **API Design**: RESTful interface with intuitive endpoint naming
-   **Documentation**: Auto-generated API documentation with examples
-   **Error Messages**: Clear, actionable error messages for developers
-   **Logging**: Structured logs for easy troubleshooting

### 5.4 Reliability Requirements

-   **Availability**: 99% uptime during business hours (8 AM - 6 PM)
-   **Error Recovery**: Graceful handling of template errors and data validation failures
-   **Fault Tolerance**: Individual request failures shall not impact other requests
-   **Data Integrity**: Generated reports shall accurately reflect input data

### 5.5 Other Requirements

**Maintainability:**

-   Modular code structure for easy enhancement
-   Comprehensive error handling and logging
-   Clear separation between template processing, data handling, and API layers

**Scalability:**

-   Architecture supports future horizontal scaling
-   Database connection pooling for future SQL integration
-   Stateless design for load balancing compatibility

**Portability:**

-   Compatible with Python 3.13.3
-   Windows IIS deployment support
-   Framework for easy migration from development to production environments

---

## 6. System Architecture

### 6.1 Technology Stack

**Web Framework:** FastAPI (recommended for modern features, automatic documentation, and strong community adoption)
**Excel Processing:** openpyxl or xlsxwriter (to be evaluated based on feature requirements)
**Database:** pyodbc + SQL Server (future integration)
**Authentication:** Custom Windows Authentication middleware
**Logging:** Python logging module with file rotation
**Deployment:** Python web application on Windows IIS with pythonnet or similar

### 6.2 Data Storage

**Templates:** Stored as .xlsx files in `/templates/` directory within project
**Generated Reports:** Temporary files cleaned up after HTTP response
**Logs:** Rotating file logs in `/logs/` directory
**Configuration:** Environment variables and configuration files
**Future Database:** MS SQL Server with connection string configuration

### 6.3 High-level Architecture

```
[Client Applications]
    ↓ HTTP/JSON
[IIS Web Server]
    ↓
[Python FastAPI Application]
    ├── Authentication Middleware (Windows Auth)
    ├── API Routes (/api/reports/*)
    ├── Template Service (File System)
    ├── Data Validation Service
    ├── Excel Generation Service (openpyxl/xlsxwriter)
    ├── Error Handler & Logging
    └── Future: Database Service (MS SQL)
    ↓
[File System: Templates & Logs]
[Future: MS SQL Database]
```

---

## 7. Appendix

### 7.1 Sample API Endpoints

```
POST /api/reports/generate
- Body: { "template": "annual-report", "data": {...} }
- Response: Excel file download

GET /api/templates/list
- Response: { "templates": ["annual-report", "quarterly-summary"] }

GET /api/health
- Response: { "status": "healthy", "version": "1.0.0" }
```

### 7.2 Template Directory Structure

```
/templates/
  ├── annual-report.xlsx
  ├── quarterly-summary.xlsx
  └── compliance-form.xlsx
/logs/
  ├── application.log
  └── error.log
```

### 7.3 Success Criteria

**Phase 1 Success Metrics:**

-   Successfully generates basic Excel reports from sample data
-   Works with at least one Excel template with proper formatting
-   Implements Windows Authentication integration
-   Provides comprehensive error handling and logging
-   Creates foundation for future MS SQL database integration

**Future Phase Considerations:**

-   Deployment to Windows IIS production environment
-   MS SQL database connectivity and data integration
-   Performance optimization for higher volume usage
-   Enhanced security and role-based authorization
