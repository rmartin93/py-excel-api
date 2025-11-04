# Product Requirements Document (PRD)

## Windows Authentication Integration

**Document Version:** 1.0
**Date:** November 4, 2025
**Project:** py-excel-api
**PRD Type:** Authentication (Phase 2)
**Dependencies:** Core API Infrastructure (Phase 1)

---

## 1. Introduction/Overview

This PRD defines the Windows Authentication integration for the Python Excel API. Building on the core infrastructure from Phase 1, this phase adds enterprise-grade authentication using Windows Integrated Authentication, enabling the API to identify users and prepare for role-based authorization in future phases.

**Problem Statement:** The API needs to integrate with existing Windows infrastructure to identify users for audit trails and future authorization requirements. This is critical for enterprise deployment on Windows IIS.

**Goal:** Implement Windows Authentication integration that extracts user information from HTTP headers, provides audit logging, and creates a foundation for future role-based permissions.

---

## 2. Goals

1. **Windows Auth Integration**: Successfully extract Windows username from HTTP headers
2. **User Context**: Maintain user context throughout request processing
3. **Audit Logging**: Log user actions for compliance and troubleshooting
4. **CORS Configuration**: Implement domain-specific CORS for enterprise environment
5. **Security Foundation**: Prepare framework for future role-based authorization
6. **IIS Compatibility**: Ensure authentication works with Windows IIS deployment

---

## 3. User Stories

### Developer Stories

-   **As a developer**, I want the API to automatically identify the current Windows user so that I don't need to pass authentication tokens
-   **As a developer**, I want to see which user made each API request in the logs so that I can track usage and troubleshoot issues
-   **As a developer**, I want the API to reject requests from unauthenticated users so that the system remains secure

### System Administrator Stories

-   **As a system administrator**, I want user activity logged with usernames so that I can audit API usage
-   **As a system administrator**, I want the API to work with our existing Windows infrastructure so that users don't need separate login credentials
-   **As a system administrator**, I want CORS properly configured so that only authorized domains can access the API

### Business User Stories

-   **As a business user**, I want seamless authentication using my Windows login so that I don't need to remember additional passwords
-   **As a business user**, I want my generated reports to be associated with my username for compliance tracking

---

## 4. Functional Requirements

### 4.1 Authentication Middleware

1. **FR-1.1**: The system must implement FastAPI middleware to extract Windows authentication headers
2. **FR-1.2**: The system must check for `REMOTE_USER` header first, then fall back to `AUTH_USER`
3. **FR-1.3**: The system must parse username from `DOMAIN\username` format to extract just the username
4. **FR-1.4**: The system must reject requests with HTTP 401 when no valid Windows authentication is found
5. **FR-1.5**: The system must support both domain\username and username-only formats
6. **FR-1.6**: The system must validate that extracted username is not empty or whitespace

### 4.2 User Context Management

7. **FR-2.1**: The system must create a user context object for each authenticated request
8. **FR-2.2**: The system must make user context available to all route handlers
9. **FR-2.3**: The system must include username in all log entries for that request
10. **FR-2.4**: The system must pass user context to Excel generation for metadata inclusion
11. **FR-2.5**: The system must include user information in API response headers (optional debug mode)
12. **FR-2.6**: The system must handle user context cleanup after request completion

### 4.3 Enhanced Logging

13. **FR-3.1**: The system must include username in all application log entries
14. **FR-3.2**: The system must log authentication attempts (success/failure)
15. **FR-3.3**: The system must log user actions (template access, report generation)
16. **FR-3.4**: The system must create audit trail for compliance reporting
17. **FR-3.5**: The system must separate security logs from application logs
18. **FR-3.6**: The system must include request correlation ID linking user actions

### 4.4 CORS Configuration

19. **FR-4.1**: The system must implement CORS middleware with domain restrictions
20. **FR-4.2**: The system must support configuration of allowed origins via environment variables
21. **FR-4.3**: The system must allow credentials in CORS for Windows authentication
22. **FR-4.4**: The system must support preflight OPTIONS requests
23. **FR-4.5**: The system must restrict allowed methods to necessary HTTP verbs only
24. **FR-4.6**: The system must log CORS violations for security monitoring

### 4.5 Security Headers

25. **FR-5.1**: The system must implement security headers middleware
26. **FR-5.2**: The system must set X-Content-Type-Options: nosniff
27. **FR-5.3**: The system must set X-Frame-Options: DENY
28. **FR-5.4**: The system must set X-XSS-Protection: 1; mode=block
29. **FR-5.5**: The system must set Referrer-Policy: strict-origin-when-cross-origin
30. **FR-5.6**: The system must include security headers in all responses

### 4.6 Authentication Testing

31. **FR-6.1**: The system must provide development mode with mock authentication
32. **FR-6.2**: The system must support authentication bypass for health check endpoint
33. **FR-6.3**: The system must include authentication test endpoint for IIS configuration validation
34. **FR-6.4**: The system must provide detailed authentication debugging in development mode
35. **FR-6.5**: The system must support multiple authentication testing scenarios

### 4.7 Enhanced API Endpoints

36. **FR-7.1**: The system must add user information to existing endpoints' responses
37. **FR-7.2**: The system must provide new endpoint: `GET /api/auth/whoami`
38. **FR-7.3**: The system must include authentication status in health check
39. **FR-7.4**: The system must update report generation to include user metadata in Excel files
40. **FR-7.5**: The system must add user context to error responses for debugging

---

## 5. Non-Goals (Out of Scope)

-   **Role-Based Authorization**: User roles and permissions (Phase 4)
-   **JWT Token Authentication**: Windows Authentication only
-   **User Registration/Management**: Uses existing Windows infrastructure
-   **Multi-Factor Authentication**: Relies on Windows security policies
-   **Session Management**: Stateless authentication per request
-   **Password Management**: Handled by Windows domain controllers
-   **External Identity Providers**: Windows only, no OAuth/SAML

---

## 6. Design Considerations

### 6.1 Authentication Flow

```
Client Request with Windows Auth Headers
    ↓
Windows Authentication Middleware
    ↓
Extract & Validate Username
    ↓
Create User Context
    ↓
Route Handler (with user context)
    ↓
Response with Audit Logging
```

### 6.2 User Context Model

```python
@dataclass
class UserContext:
    username: str
    domain: Optional[str]
    authenticated: bool
    request_id: str
    timestamp: datetime
    ip_address: str
    user_agent: str
```

### 6.3 Enhanced Configuration

```python
class Settings:
    # Authentication
    AUTH_REQUIRED: bool = True
    AUTH_DEVELOPMENT_MODE: bool = False
    AUTH_MOCK_USERNAME: str = "dev_user"

    # CORS
    CORS_ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True

    # Security
    SECURITY_HEADERS_ENABLED: bool = True
    AUDIT_LOGGING_ENABLED: bool = True
```

---

## 7. Technical Considerations

### 7.1 Additional Dependencies

```python
# Add to existing requirements.txt
python-jose[cryptography]==3.3.0  # For future JWT support
passlib[bcrypt]==1.7.4            # For future password handling
python-multipart==0.0.6           # Already included
```

### 7.2 IIS Configuration Requirements

-   Enable Windows Authentication in IIS
-   Disable Anonymous Authentication for API endpoints
-   Configure application pool identity correctly
-   Set up proper CORS headers in IIS if needed

### 7.3 Development Environment Setup

-   Configure development server to simulate Windows headers
-   Create mock authentication for local development
-   Provide test utilities for authentication scenarios

### 7.4 Error Handling Enhancement

-   Authentication-specific error codes
-   User-friendly error messages for authentication failures
-   Detailed logging for authentication debugging

---

## 8. Success Metrics

### 8.1 Authentication Metrics

-   **Authentication Success Rate**: > 95% for valid Windows users
-   **Header Extraction Accuracy**: 100% correct username extraction from headers
-   **CORS Compliance**: 0% blocked legitimate requests from configured domains
-   **Security**: 100% rejection of unauthenticated requests (except health check)

### 8.2 Logging Metrics

-   **Audit Trail Completeness**: 100% of user actions logged with username
-   **Log Correlation**: All request logs include user context and correlation ID
-   **Security Event Logging**: All authentication attempts logged

### 8.3 Performance Metrics

-   **Authentication Overhead**: < 10ms additional latency per request
-   **Memory Usage**: User context adds < 1KB per request
-   **Concurrent Users**: Support 50+ concurrent authenticated users

---

## 9. Open Questions

1. **Domain Handling**: Should we store domain information separately or just username?
2. **Authentication Caching**: Should we cache authentication results for performance?
3. **Development Testing**: How should developers test without Windows domain?
4. **Error Responses**: Should authentication errors include helpful debugging information?
5. **Logging Retention**: How long should security/audit logs be retained?
6. **IIS Integration**: What IIS-specific configuration documentation is needed?

---

## 10. Implementation Notes for Junior Developer

### 10.1 Implementation Order

1. Create user context model and middleware structure
2. Implement Windows header extraction logic
3. Add authentication middleware to FastAPI application
4. Enhance logging to include user context
5. Implement CORS configuration
6. Add security headers middleware
7. Create authentication testing endpoints
8. Update existing endpoints to use user context
9. Add comprehensive error handling
10. Write integration tests with mock authentication

### 10.2 Development Strategy

-   **Mock First**: Create mock authentication for development before implementing real Windows auth
-   **Test Locally**: Use custom headers to simulate Windows authentication in development
-   **Log Everything**: Add extensive logging to understand authentication flow
-   **Gradual Rollout**: Start with optional authentication, then make it required
-   **Error Handling**: Focus on clear error messages for authentication failures

### 10.3 Testing Approach

-   Unit tests with mock user contexts
-   Integration tests with simulated Windows headers
-   Security tests for authentication bypass attempts
-   Performance tests for authentication overhead
-   End-to-end tests in Windows IIS environment

### 10.4 IIS Deployment Considerations

-   Document required IIS authentication configuration
-   Provide PowerShell scripts for IIS setup
-   Create deployment checklist for Windows environment
-   Include troubleshooting guide for authentication issues

---

**Next Steps**: After this PRD is implemented, proceed to Phase 3 (MS SQL Integration) PRD for database connectivity and real data processing.
