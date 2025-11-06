# PowerShell script to automate IIS deployment of Python Excel API
# Run as Administrator

param(
    [Parameter(Mandatory=$false)]
    [string]$PythonPath = "C:\Python311\python.exe",

    [Parameter(Mandatory=$false)]
    [string]$AppPath = "C:\inetpub\wwwroot\py-excel-api",

    [Parameter(Mandatory=$false)]
    [string]$SiteName = "Default Web Site",

    [Parameter(Mandatory=$false)]
    [string]$AppName = "py-excel-api",

    [Parameter(Mandatory=$false)]
    [string]$AppPoolName = "PyExcelAPI"
)

Write-Host "🚀 Starting IIS deployment for Python Excel API..." -ForegroundColor Green

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "This script must be run as Administrator!"
    exit 1
}

try {
    # Step 1: Enable IIS Features
    Write-Host "📦 Enabling IIS features..." -ForegroundColor Yellow

    $features = @(
        "IIS-WebServerRole",
        "IIS-WebServer",
        "IIS-CommonHttpFeatures",
        "IIS-HttpErrors",
        "IIS-HttpLogging",
        "IIS-Security",
        "IIS-RequestFiltering",
        "IIS-StaticContent",
        "IIS-DefaultDocument",
        "IIS-DirectoryBrowsing",
        "IIS-CGI",
        "IIS-ISAPIExtensions",
        "IIS-ISAPIFilter"
    )

    foreach ($feature in $features) {
        Write-Host "  Enabling $feature..."
        Enable-WindowsOptionalFeature -Online -FeatureName $feature -All -NoRestart
    }

    # Step 2: Import IIS module
    Write-Host "🔧 Importing IIS module..." -ForegroundColor Yellow
    Import-Module WebAdministration

    # Step 3: Create directories
    Write-Host "📁 Creating application directories..." -ForegroundColor Yellow

    $directories = @(
        $AppPath,
        "$AppPath\app",
        "$AppPath\templates",
        "C:\inetpub\logs\py-excel-api"
    )

    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -Path $dir -ItemType Directory -Force
            Write-Host "  Created: $dir"
        } else {
            Write-Host "  Exists: $dir"
        }
    }

    # Step 4: Create Application Pool
    Write-Host "🏊 Creating application pool..." -ForegroundColor Yellow

    if (Get-WebAppPool -Name $AppPoolName -ErrorAction SilentlyContinue) {
        Write-Host "  Application pool '$AppPoolName' already exists, removing..."
        Remove-WebAppPool -Name $AppPoolName
    }

    New-WebAppPool -Name $AppPoolName -Force
    Set-ItemProperty -Path "IIS:\AppPools\$AppPoolName" -Name processModel.identityType -Value ApplicationPoolIdentity
    Set-ItemProperty -Path "IIS:\AppPools\$AppPoolName" -Name recycling.periodicRestart.time -Value "00:00:00"
    Set-ItemProperty -Path "IIS:\AppPools\$AppPoolName" -Name processModel.idleTimeout -Value "00:00:00"

    Write-Host "  Application pool '$AppPoolName' created successfully"

    # Step 5: Create IIS Application
    Write-Host "🌐 Creating IIS application..." -ForegroundColor Yellow

    if (Get-WebApplication -Site $SiteName -Name $AppName -ErrorAction SilentlyContinue) {
        Write-Host "  Application '$AppName' already exists, removing..."
        Remove-WebApplication -Site $SiteName -Name $AppName
    }

    New-WebApplication -Site $SiteName -Name $AppName -PhysicalPath $AppPath -ApplicationPool $AppPoolName
    Write-Host "  IIS application '$AppName' created successfully"

    # Step 6: Configure FastCGI
    Write-Host "⚡ Configuring FastCGI..." -ForegroundColor Yellow

    # Remove existing FastCGI application if it exists
    $existingFastCgi = Get-WebConfiguration -Filter "system.webServer/fastCgi/application[@fullPath='$PythonPath' and @arguments='$AppPath\iis_handler.py']"
    if ($existingFastCgi) {
        Write-Host "  Removing existing FastCGI configuration..."
        Remove-WebConfiguration -Filter "system.webServer/fastCgi/application[@fullPath='$PythonPath' and @arguments='$AppPath\iis_handler.py']"
    }

    # Add FastCGI application
    Add-WebConfiguration -Filter "system.webServer/fastCgi" -Value @{
        fullPath = $PythonPath
        arguments = "$AppPath\iis_handler.py"
        maxInstances = 4
        requestTimeout = "00:10:00"
        activityTimeout = "00:10:00"
        flushNamedPipe = $false
        monitorChangesTo = $AppPath
    }

    # Remove existing handler mapping if it exists
    $existingHandler = Get-WebConfiguration -Filter "system.webServer/handlers/add[@name='Python FastCGI']" -PSPath "IIS:\Sites\$SiteName\$AppName" -ErrorAction SilentlyContinue
    if ($existingHandler) {
        Write-Host "  Removing existing handler mapping..."
        Remove-WebConfiguration -Filter "system.webServer/handlers/add[@name='Python FastCGI']" -PSPath "IIS:\Sites\$SiteName\$AppName"
    }

    # Add handler mapping
    Add-WebConfiguration -Filter "system.webServer/handlers" -Value @{
        name = "Python FastCGI"
        path = "*"
        verb = "*"
        modules = "FastCgiModule"
        scriptProcessor = "$PythonPath|$AppPath\iis_handler.py"
        resourceType = "Unspecified"
    } -PSPath "IIS:\Sites\$SiteName\$AppName"

    Write-Host "  FastCGI configured successfully"

    # Step 7: Set Permissions
    Write-Host "🔐 Setting file permissions..." -ForegroundColor Yellow

    # Application directory permissions
    $acl = Get-Acl $AppPath
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS AppPool\$AppPoolName", "ReadAndExecute", "ContainerInherit,ObjectInherit", "None", "Allow")
    $acl.SetAccessRule($accessRule)
    Set-Acl $AppPath $acl
    Write-Host "  Set ReadAndExecute permissions for application directory"

    # Logs directory permissions
    $acl = Get-Acl "C:\inetpub\logs\py-excel-api"
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS AppPool\$AppPoolName", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
    $acl.SetAccessRule($accessRule)
    Set-Acl "C:\inetpub\logs\py-excel-api" $acl
    Write-Host "  Set FullControl permissions for logs directory"

    # Step 8: Create IIS Handler Script
    Write-Host "📄 Creating IIS handler script..." -ForegroundColor Yellow

    $handlerScript = @"
#!/usr/bin/env python3
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
    application = app
except Exception as e:
    with open("C:\\inetpub\\logs\\py-excel-api\\startup_error.log", "a") as f:
        f.write(f"Startup error: {e}\n")
    raise
"@

    $handlerScript | Out-File -FilePath "$AppPath\iis_handler.py" -Encoding UTF8
    Write-Host "  IIS handler script created"

    # Step 9: Create sample .env file
    Write-Host "⚙️ Creating production .env template..." -ForegroundColor Yellow

    $envContent = @"
# Production Configuration
DEBUG=False
LOG_LEVEL=WARNING

# Paths (Windows format)
TEMPLATES_DIR=$AppPath\templates
LOGS_DIR=C:\inetpub\logs\py-excel-api

# Database (when implemented)
# DATABASE_URL=mssql+pyodbc://server/database?driver=ODBC+Driver+17+for+SQL+Server

# Security
# SECRET_KEY=your-production-secret-key-here
"@

    if (!(Test-Path "$AppPath\.env")) {
        $envContent | Out-File -FilePath "$AppPath\.env.production" -Encoding UTF8
        Write-Host "  Created .env.production template (rename to .env and configure)"
    } else {
        Write-Host "  .env file already exists, skipping template creation"
    }

    # Step 10: Start Application Pool
    Write-Host "🏊 Starting application pool..." -ForegroundColor Yellow
    Start-WebAppPool -Name $AppPoolName
    Write-Host "  Application pool started"

    Write-Host "`n✅ IIS deployment completed successfully!" -ForegroundColor Green
    Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Copy your application files to: $AppPath"
    Write-Host "2. Install Python dependencies: pip install -r requirements.txt"
    Write-Host "3. Configure .env file for production"
    Write-Host "4. Test the application: http://localhost/$AppName/health"
    Write-Host "`n🔗 Application URL: http://localhost/$AppName"

} catch {
    Write-Error "❌ Deployment failed: $($_.Exception.Message)"
    Write-Host "`n🔍 Check the following:" -ForegroundColor Yellow
    Write-Host "- Running as Administrator"
    Write-Host "- Python path is correct: $PythonPath"
    Write-Host "- IIS is installed and running"
    Write-Host "- No conflicting applications using the same name"
    exit 1
}