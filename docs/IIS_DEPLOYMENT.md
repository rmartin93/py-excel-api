# IIS Deployment Guide for Python Excel API

This guide provides step-by-step instructions for deploying the Python Excel API on Windows Server with IIS.

## 📋 Prerequisites

-   Windows Server 2016+ or Windows 10/11 Pro
-   IIS installed with CGI/FastCGI support
-   Python 3.11+ installed
-   Administrator access to the server

## 🔧 Step 1: Install Required IIS Features

### Using Windows Features (GUI)

1. Open **Control Panel** → **Programs** → **Turn Windows features on or off**
2. Enable **Internet Information Services**
3. Under **IIS** → **World Wide Web Services** → **Application Development Features**, enable:
    - CGI
    - ISAPI Extensions
    - ISAPI Filters

### Using PowerShell (Recommended)

Run as Administrator:

```powershell
# Enable IIS and required features
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpLogging
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Security
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestFiltering
Enable-WindowsOptionalFeature -Online -FeatureName IIS-StaticContent
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DefaultDocument
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DirectoryBrowsing
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIExtensions
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIFilter
```

## 🐍 Step 2: Install Python

1. **Download Python 3.11+** from [python.org](https://www.python.org/downloads/)
2. **Install with these options**:
    - ✅ Add Python to PATH
    - ✅ Install for all users
    - ✅ Install pip
3. **Verify installation**:
    ```cmd
    python --version
    pip --version
    ```

## 📦 Step 3: Install FastCGI for Python

1. **Download and install** [Microsoft IIS FastCGI Extension](https://www.iis.net/downloads/microsoft/fastcgi-for-iis)
2. **Or use Web Platform Installer** to install FastCGI support

## 🏗️ Step 4: Deploy Application Files

### 4.1 Create Application Directory

```powershell
# Create application directory
New-Item -Path "C:\inetpub\wwwroot\py-excel-api" -ItemType Directory -Force

# Create subdirectories
New-Item -Path "C:\inetpub\wwwroot\py-excel-api\app" -ItemType Directory -Force
New-Item -Path "C:\inetpub\wwwroot\py-excel-api\templates" -ItemType Directory -Force
New-Item -Path "C:\inetpub\logs\py-excel-api" -ItemType Directory -Force
```

### 4.2 Copy Application Files

Copy your entire project to `C:\inetpub\wwwroot\py-excel-api\`:

-   `app/` directory
-   `templates/` directory
-   `requirements.txt`
-   `.env` file (configured for production)

### 4.3 Install Python Dependencies

```cmd
cd C:\inetpub\wwwroot\py-excel-api
python -m pip install -r requirements.txt
```

## ⚙️ Step 5: Configure IIS Application

### 5.1 Create Application Pool

```powershell
# Import IIS module
Import-Module WebAdministration

# Create new application pool
New-WebAppPool -Name "PyExcelAPI" -Force

# Configure application pool
Set-ItemProperty -Path "IIS:\AppPools\PyExcelAPI" -Name processModel.identityType -Value ApplicationPoolIdentity
Set-ItemProperty -Path "IIS:\AppPools\PyExcelAPI" -Name recycling.periodicRestart.time -Value "00:00:00"
Set-ItemProperty -Path "IIS:\AppPools\PyExcelAPI" -Name processModel.idleTimeout -Value "00:00:00"
```

### 5.2 Create IIS Application

```powershell
# Create IIS application
New-WebApplication -Site "Default Web Site" -Name "py-excel-api" -PhysicalPath "C:\inetpub\wwwroot\py-excel-api" -ApplicationPool "PyExcelAPI"
```

### 5.3 Configure FastCGI

```powershell
# Add FastCGI application
Add-WebConfiguration -Filter "system.webServer/fastCgi" -Value @{
    fullPath = "C:\Python311\python.exe"
    arguments = "C:\inetpub\wwwroot\py-excel-api\iis_handler.py"
    maxInstances = 4
    requestTimeout = "00:10:00"
    activityTimeout = "00:10:00"
    flushNamedPipe = $false
    monitorChangesTo = "C:\inetpub\wwwroot\py-excel-api"
}

# Add handler mapping
Add-WebConfiguration -Filter "system.webServer/handlers" -Value @{
    name = "Python FastCGI"
    path = "*"
    verb = "*"
    modules = "FastCgiModule"
    scriptProcessor = "C:\Python311\python.exe|C:\inetpub\wwwroot\py-excel-api\iis_handler.py"
    resourceType = "Unspecified"
} -PSPath "IIS:\Sites\Default Web Site\py-excel-api"
```

## 📄 Step 6: Create IIS Handler Script

Create `C:\inetpub\wwwroot\py-excel-api\iis_handler.py`:

```python
#!/usr/bin/env python3
"""
IIS FastCGI handler for Python Excel API
This script serves as the entry point for IIS to run our FastAPI application
"""

import sys
import os
from pathlib import Path

# Add the application directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Set environment variables for production
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('LOG_LEVEL', 'WARNING')
os.environ.setdefault('TEMPLATES_DIR', str(app_dir / 'templates'))
os.environ.setdefault('LOGS_DIR', 'C:\\inetpub\\logs\\py-excel-api')

try:
    from app.main import app

    # For FastCGI, we need to use a WSGI server
    from fastapi.middleware.wsgi import WSGIMiddleware
    import uvicorn

    # Create WSGI application
    if __name__ == "__main__":
        # This won't be called in FastCGI mode, but kept for testing
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # FastCGI mode - create WSGI callable
        application = app

except Exception as e:
    # Log startup errors
    with open("C:\\inetpub\\logs\\py-excel-api\\startup_error.log", "a") as f:
        f.write(f"Startup error: {e}\\n")
    raise
```

## 🔐 Step 7: Configure Security & Permissions

### 7.1 Set Directory Permissions

```powershell
# Grant IIS application pool read/execute permissions
$acl = Get-Acl "C:\inetpub\wwwroot\py-excel-api"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS AppPool\PyExcelAPI", "ReadAndExecute", "ContainerInherit,ObjectInherit", "None", "Allow")
$acl.SetAccessRule($accessRule)
Set-Acl "C:\inetpub\wwwroot\py-excel-api" $acl

# Grant write permissions to logs directory
$acl = Get-Acl "C:\inetpub\logs\py-excel-api"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS AppPool\PyExcelAPI", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
$acl.SetAccessRule($accessRule)
Set-Acl "C:\inetpub\logs\py-excel-api" $acl
```

### 7.2 Configure Authentication (Optional)

For Windows Authentication integration:

```powershell
# Enable Windows Authentication
Set-WebConfiguration -Filter "system.webServer/security/authentication/windowsAuthentication" -Value @{enabled="true"} -PSPath "IIS:\Sites\Default Web Site\py-excel-api"

# Disable Anonymous Authentication for API endpoints
Set-WebConfiguration -Filter "system.webServer/security/authentication/anonymousAuthentication" -Value @{enabled="false"} -PSPath "IIS:\Sites\Default Web Site\py-excel-api"
```

## 🌐 Step 8: Configure Production Environment

### 8.1 Create Production .env File

Create `C:\inetpub\wwwroot\py-excel-api\.env`:

```env
# Production Configuration
DEBUG=False
LOG_LEVEL=WARNING

# Paths (Windows format)
TEMPLATES_DIR=C:\inetpub\wwwroot\py-excel-api\templates
LOGS_DIR=C:\inetpub\logs\py-excel-api

# Database (when implemented)
# DATABASE_URL=mssql+pyodbc://server/database?driver=ODBC+Driver+17+for+SQL+Server

# Security
# SECRET_KEY=your-production-secret-key-here
```

### 8.2 Configure CORS (if needed)

Add to `web.config` in application root:

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <httpProtocol>
      <customHeaders>
        <add name="Access-Control-Allow-Origin" value="*" />
        <add name="Access-Control-Allow-Methods" value="GET, POST, PUT, DELETE, OPTIONS" />
        <add name="Access-Control-Allow-Headers" value="Content-Type, Authorization" />
      </customHeaders>
    </httpProtocol>
  </system.webServer>
</configuration>
```

## 🧪 Step 9: Test Deployment

### 9.1 Test Application Pool

```powershell
# Start application pool
Start-WebAppPool -Name "PyExcelAPI"

# Check status
Get-WebAppPool -Name "PyExcelAPI"
```

### 9.2 Test API Endpoints

```powershell
# Test health endpoint
Invoke-RestMethod -Uri "http://localhost/py-excel-api/health" -Method GET

# Test templates endpoint
Invoke-RestMethod -Uri "http://localhost/py-excel-api/templates" -Method GET
```

## 🔍 Step 10: Monitoring & Troubleshooting

### 10.1 Log Locations

-   **Application Logs**: `C:\inetpub\logs\py-excel-api\`
-   **IIS Logs**: `C:\inetpub\logs\LogFiles\W3SVC1\`
-   **Windows Event Logs**: Event Viewer → Windows Logs → Application

### 10.2 Common Issues

#### Python Module Not Found

-   Verify Python path in FastCGI configuration
-   Check application pool identity permissions
-   Ensure all dependencies are installed

#### 500 Internal Server Error

-   Check `startup_error.log` for Python errors
-   Verify file permissions on application directory
-   Review IIS error logs

#### Performance Issues

-   Increase FastCGI `maxInstances` if needed
-   Monitor memory usage of Python processes
-   Consider using a proper ASGI server like Hypercorn

### 10.3 Health Monitoring Script

Create `C:\inetpub\wwwroot\py-excel-api\health_monitor.ps1`:

```powershell
# Health monitoring script for Python Excel API
$apiUrl = "http://localhost/py-excel-api/health"
$logPath = "C:\inetpub\logs\py-excel-api\health_monitor.log"

try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method GET -TimeoutSec 30
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    if ($response.status -eq "healthy") {
        Add-Content -Path $logPath -Value "$timestamp - API Health: OK"
    } else {
        Add-Content -Path $logPath -Value "$timestamp - API Health: DEGRADED - $($response | ConvertTo-Json)"
    }
} catch {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logPath -Value "$timestamp - API Health: FAILED - $($_.Exception.Message)"
}
```

## 📋 Deployment Checklist

-   [ ] IIS installed with FastCGI support
-   [ ] Python 3.11+ installed and accessible
-   [ ] Application files deployed to IIS directory
-   [ ] Python dependencies installed
-   [ ] Application pool created and configured
-   [ ] FastCGI application and handler configured
-   [ ] File permissions set correctly
-   [ ] Production environment variables configured
-   [ ] Health endpoint responding
-   [ ] Templates endpoint returning data
-   [ ] Excel generation working
-   [ ] Logging directory writable
-   [ ] Monitoring script scheduled (optional)

## 🔗 Additional Resources

-   [IIS FastCGI Documentation](https://learn.microsoft.com/en-us/iis/configuration/system.webserver/fastcgi/)
-   [Python on Windows Documentation](https://docs.python.org/3/using/windows.html)
-   [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)

---

> **💡 Pro Tip**: For production environments, consider using a proper ASGI server like Hypercorn or Uvicorn behind IIS as a reverse proxy for better performance and features.
