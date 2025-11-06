# IIS Deployment Checklist

## 🚀 Quick Deployment (Using PowerShell Script)

### Prerequisites

-   [ ] Windows Server 2016+ or Windows 10/11 Pro
-   [ ] Administrator privileges
-   [ ] Python 3.11+ installed at `C:\Python311\`

### Automated Deployment

1. [ ] **Run PowerShell as Administrator**
2. [ ] **Execute deployment script**:
    ```powershell
    .\docs\deploy-iis.ps1
    ```
3. [ ] **Copy application files** to `C:\inetpub\wwwroot\py-excel-api\`
4. [ ] **Install dependencies**:
    ```cmd
    cd C:\inetpub\wwwroot\py-excel-api
    python -m pip install -r requirements.txt
    ```
5. [ ] **Configure production environment**:
    - Rename `.env.production` to `.env`
    - Update paths and settings as needed
6. [ ] **Test deployment**:
    ```powershell
    Invoke-RestMethod -Uri "http://localhost/py-excel-api/health"
    ```

## 📋 Manual Deployment Checklist

### System Setup

-   [ ] IIS installed with FastCGI support
-   [ ] Python 3.11+ installed and in PATH
-   [ ] Administrator access confirmed

### Application Setup

-   [ ] Application directory created: `C:\inetpub\wwwroot\py-excel-api\`
-   [ ] Logs directory created: `C:\inetpub\logs\py-excel-api\`
-   [ ] Application files copied
-   [ ] Python dependencies installed
-   [ ] Production `.env` file configured

### IIS Configuration

-   [ ] Application pool created: `PyExcelAPI`
-   [ ] Application pool configured (identity, timeouts)
-   [ ] IIS application created and linked to app pool
-   [ ] FastCGI application configured
-   [ ] Handler mapping added
-   [ ] File permissions set correctly

### Security Configuration

-   [ ] Application pool has ReadAndExecute on app directory
-   [ ] Application pool has FullControl on logs directory
-   [ ] Windows Authentication enabled (if required)
-   [ ] Anonymous authentication disabled (if required)
-   [ ] CORS configured (if required)

### Testing & Validation

-   [ ] Application pool starts without errors
-   [ ] Health endpoint responds: `/health`
-   [ ] Templates endpoint responds: `/templates`
-   [ ] Excel generation works: `/reports/template-1`
-   [ ] Logs are being written
-   [ ] Error handling works correctly

### Production Monitoring

-   [ ] Health monitoring script scheduled
-   [ ] Log rotation configured
-   [ ] Performance counters reviewed
-   [ ] Backup strategy in place

## 🔧 Common Issues & Solutions

### Python Module Not Found

-   ✅ Check Python path in FastCGI config
-   ✅ Verify all dependencies installed
-   ✅ Check application pool identity

### 500 Internal Server Error

-   ✅ Check `startup_error.log`
-   ✅ Review IIS error logs
-   ✅ Verify file permissions

### Slow Performance

-   ✅ Increase FastCGI `maxInstances`
-   ✅ Monitor memory usage
-   ✅ Consider ASGI server behind IIS

### Authentication Issues

-   ✅ Verify Windows Authentication enabled
-   ✅ Check application pool identity
-   ✅ Review CORS configuration

## 📞 Support Resources

-   **Detailed Guide**: `docs/IIS_DEPLOYMENT.md`
-   **Deployment Script**: `docs/deploy-iis.ps1`
-   **Application Logs**: `C:\inetpub\logs\py-excel-api\`
-   **IIS Logs**: `C:\inetpub\logs\LogFiles\W3SVC1\`
