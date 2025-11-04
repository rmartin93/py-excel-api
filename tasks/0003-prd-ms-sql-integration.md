# Product Requirements Document (PRD)

## MS SQL Database Integration

**Document Version:** 1.0
**Date:** November 4, 2025
**Project:** py-excel-api
**PRD Type:** Database Integration (Phase 3)
**Dependencies:** Core API Infrastructure (Phase 1), Windows Authentication (Phase 2)

---

## 1. Introduction/Overview

This PRD defines the MS SQL Server database integration for the Python Excel API. Building on the authentication and core infrastructure from previous phases, this phase replaces sample data with real database connectivity, enabling dynamic report generation from live enterprise data.

**Problem Statement:** The API currently uses static sample data, but production reports need real-time data from MS SQL Server databases. Integration must be secure, performant, and maintainable.

**Goal:** Implement robust MS SQL Server connectivity that replaces sample data with dynamic database queries, includes connection pooling, error handling, and provides a foundation for complex reporting scenarios.

---

## 2. Goals

1. **Database Connectivity**: Establish secure, reliable connections to MS SQL Server
2. **Replace Sample Data**: Transition from static sample data to dynamic database queries
3. **Connection Management**: Implement connection pooling and resource management
4. **Query Framework**: Create reusable database query utilities and error handling
5. **Performance Optimization**: Ensure efficient data retrieval for report generation
6. **Security**: Implement secure database authentication and query practices
7. **Documentation**: Provide database setup and configuration documentation

---

## 3. User Stories

### Developer Stories

-   **As a developer**, I want to query real database data for reports so that the generated Excel files contain current information
-   **As a developer**, I want reusable database utilities so that I can easily add new data sources for different reports
-   **As a developer**, I want clear error messages when database queries fail so that I can troubleshoot integration issues
-   **As a developer**, I want connection pooling so that the API performs well under concurrent load

### System Administrator Stories

-   **As a system administrator**, I want configurable database connections so that I can manage different environments (dev, test, prod)
-   **As a system administrator**, I want database connection monitoring so that I can track performance and identify issues
-   **As a system administrator**, I want secure database authentication so that credentials are properly managed

### Business User Stories

-   **As a business user**, I want reports to contain the most current data so that my submissions are accurate and up-to-date
-   **As a business user**, I want reliable report generation so that database issues don't prevent me from meeting deadlines
-   **As a business user**, I want fast report generation so that I can generate multiple reports efficiently

---

## 4. Functional Requirements

### 4.1 Database Connection Management

1. **FR-1.1**: The system must use `pyodbc` or `sqlalchemy` for MS SQL Server connectivity
2. **FR-1.2**: The system must implement connection pooling with configurable pool size
3. **FR-1.3**: The system must support both Windows Authentication and SQL Server authentication
4. **FR-1.4**: The system must handle connection timeouts gracefully with automatic retry
5. **FR-1.5**: The system must validate database connectivity on application startup
6. **FR-1.6**: The system must close connections properly to prevent resource leaks

### 4.2 Configuration Management

7. **FR-2.1**: The system must support database configuration via environment variables
8. **FR-2.2**: The system must support multiple database connection strings for different environments
9. **FR-2.3**: The system must validate database configuration on startup
10. **FR-2.4**: The system must support connection string encryption for production deployment
11. **FR-2.5**: The system must provide database configuration templates for easy setup
12. **FR-2.6**: The system must log database configuration (without credentials) for debugging

### 4.3 Query Framework

13. **FR-3.1**: The system must create a reusable database service layer
14. **FR-3.2**: The system must support parameterized queries to prevent SQL injection
15. **FR-3.3**: The system must implement query timeout handling with configurable limits
16. **FR-3.4**: The system must support both simple queries and stored procedure calls
17. **FR-3.5**: The system must handle large result sets with streaming or pagination
18. **FR-3.6**: The system must provide query result caching for frequently accessed data

### 4.4 Data Mapping and Transformation

19. **FR-4.1**: The system must map database results to Excel template placeholders
20. **FR-4.2**: The system must handle data type conversion (dates, numbers, strings) for Excel
21. **FR-4.3**: The system must support nested data structures for complex reports
22. **FR-4.4**: The system must handle NULL values appropriately in Excel output
23. **FR-4.5**: The system must support data aggregation and calculated fields
24. **FR-4.6**: The system must validate data consistency before Excel generation

### 4.5 Template Enhancement

25. **FR-5.1**: The system must support database-driven templates with query specifications
26. **FR-5.2**: The system must enable templates to specify required database parameters
27. **FR-5.3**: The system must validate that required data is available before processing
28. **FR-5.4**: The system must support multiple queries per template for complex reports
29. **FR-5.5**: The system must handle template-specific data formatting requirements
30. **FR-5.6**: The system must support conditional data inclusion based on query results

### 4.6 Error Handling and Resilience

31. **FR-6.1**: The system must implement database-specific error handling
32. **FR-6.2**: The system must retry failed database connections with exponential backoff
33. **FR-6.3**: The system must provide meaningful error messages for database failures
34. **FR-6.4**: The system must log database errors with query context for debugging
35. **FR-6.5**: The system must handle database unavailability gracefully
36. **FR-6.6**: The system must implement circuit breaker pattern for database resilience

### 4.7 Enhanced API Endpoints

37. **FR-7.1**: The system must update report generation endpoints to use database data
38. **FR-7.2**: The system must provide endpoint for testing database connectivity: `GET /api/database/health`
39. **FR-7.3**: The system must support dynamic parameters in report generation requests
40. **FR-7.4**: The system must validate database permissions for requested data
41. **FR-7.5**: The system must provide data preview endpoints for report development
42. **FR-7.6**: The system must support batch report generation for multiple parameter sets

---

## 5. Non-Goals (Out of Scope)

-   **Database Administration**: No database schema management or migrations
-   **Data Warehousing**: No ETL processes or data transformation beyond reporting needs
-   **Real-time Data**: No WebSocket or real-time data streaming
-   **Multiple Database Types**: MS SQL Server only, no PostgreSQL/MySQL support
-   **Database Security**: Relies on existing database security policies
-   **Backup/Recovery**: Uses existing database backup strategies
-   **Performance Tuning**: Basic optimization only, no advanced database tuning

---

## 6. Design Considerations

### 6.1 Database Architecture

```
FastAPI Application
    ↓
Database Service Layer
    ↓
Connection Pool Manager
    ↓
MS SQL Server Database
```

### 6.2 Configuration Structure

```python
class DatabaseConfig:
    host: str
    port: int = 1433
    database: str
    username: Optional[str] = None
    password: Optional[str] = None
    use_windows_auth: bool = True
    connection_timeout: int = 30
    query_timeout: int = 300
    pool_size: int = 10
    max_overflow: int = 20
```

### 6.3 Database Service Interface

```python
class DatabaseService:
    async def execute_query(self, query: str, params: dict) -> List[dict]
    async def execute_stored_procedure(self, proc_name: str, params: dict) -> List[dict]
    async def test_connection(self) -> bool
    async def get_connection_info(self) -> dict
```

### 6.4 Enhanced Template Metadata

```json
{
	"template_name": "annual-report",
	"queries": [
		{
			"name": "main_data",
			"sql": "SELECT * FROM reports WHERE year = ? AND department = ?",
			"parameters": ["year", "department"],
			"required": true
		},
		{
			"name": "summary_data",
			"sql": "EXEC GetReportSummary @year, @department",
			"parameters": ["year", "department"],
			"required": false
		}
	]
}
```

---

## 7. Technical Considerations

### 7.1 Additional Dependencies

```python
# Add to requirements.txt
sqlalchemy==2.0.23         # ORM and connection pooling
pyodbc==5.0.1              # MS SQL Server driver
alembic==1.12.1            # Database migrations (future)
asyncpg==0.29.0            # Async database operations
databases[postgresql]==0.8.0  # Async database toolkit
```

### 7.2 Database Driver Configuration

-   Install Microsoft ODBC Driver for SQL Server
-   Configure connection string templates
-   Set up connection pooling parameters
-   Handle different authentication methods

### 7.3 Security Considerations

-   Use parameterized queries only
-   Implement query whitelisting for template safety
-   Encrypt connection strings in production
-   Log database access for audit trails

### 7.4 Performance Optimization

-   Implement connection pooling
-   Use query result caching where appropriate
-   Handle large result sets with streaming
-   Monitor database performance metrics

---

## 8. Success Metrics

### 8.1 Performance Metrics

-   **Database Connection Time**: < 2 seconds for initial connection
-   **Query Response Time**: < 10 seconds for typical report queries
-   **Connection Pool Efficiency**: > 90% connection reuse rate
-   **Memory Usage**: Efficient handling of result sets without memory leaks

### 8.2 Reliability Metrics

-   **Database Availability**: Handle 99%+ database uptime gracefully
-   **Error Recovery**: 100% recovery from temporary database disconnections
-   **Data Accuracy**: 100% accuracy in data-to-Excel mapping
-   **Connection Stability**: No connection leaks or hanging connections

### 8.3 Integration Metrics

-   **Template Compatibility**: 100% of existing templates work with database data
-   **API Compatibility**: No breaking changes to existing API endpoints
-   **Configuration Flexibility**: Support for dev/test/prod environments

---

## 9. Open Questions

1. **Connection Pooling**: Should we use SQLAlchemy's pooling or implement custom pooling?
2. **Query Storage**: Should queries be stored in template files, database, or separate configuration?
3. **Caching Strategy**: What data should be cached and for how long?
4. **Transaction Management**: Do we need transaction support for report generation?
5. **Database Monitoring**: What database metrics should be exposed via API?
6. **Error Recovery**: How should we handle partial data scenarios?

---

## 10. Implementation Notes for Junior Developer

### 10.1 Implementation Phases

**Phase 3A: Basic Connectivity**

1. Install and configure database drivers
2. Create database configuration management
3. Implement basic connection testing
4. Create simple query execution framework

**Phase 3B: Integration**

1. Replace sample data with database queries
2. Update template processing for database data
3. Implement error handling for database operations
4. Add database health checks to existing endpoints

**Phase 3C: Advanced Features**

1. Implement connection pooling
2. Add query result caching
3. Create stored procedure support
4. Add performance monitoring

### 10.2 Development Strategy

-   **Database First**: Set up database connectivity before modifying templates
-   **Incremental**: Replace one template at a time with database data
-   **Test Coverage**: Comprehensive testing with both mock and real databases
-   **Configuration**: Make everything configurable for different environments
-   **Error Handling**: Assume database will be unavailable and handle gracefully

### 10.3 Testing Approach

-   Unit tests with mock database connections
-   Integration tests with test database
-   Performance tests with realistic data volumes
-   Error handling tests with simulated database failures
-   End-to-end tests with full database integration

### 10.4 Setup Requirements

-   MS SQL Server instance (local or remote)
-   Test database with sample data
-   ODBC driver installation
-   Connection string configuration
-   Database permissions for API service account

### 10.5 Sample Database Setup

```sql
-- Create sample tables for testing
CREATE TABLE reports (
    id INT PRIMARY KEY,
    year INT,
    department VARCHAR(50),
    amount DECIMAL(10,2),
    created_date DATETIME
);

-- Create sample stored procedure
CREATE PROCEDURE GetReportSummary
    @year INT,
    @department VARCHAR(50)
AS
BEGIN
    SELECT
        department,
        SUM(amount) as total_amount,
        COUNT(*) as record_count
    FROM reports
    WHERE year = @year AND department = @department
    GROUP BY department;
END
```

---

**Next Steps**: After this PRD is implemented, the core functionality will be complete. Consider additional PRDs for advanced features like caching, monitoring, or advanced Excel features based on business needs.
