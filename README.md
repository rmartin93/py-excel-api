# Python Excel API

A **template-specific** Python API for Excel report generation, built with FastAPI. This project demonstrates a practical approach to Excel automation where each template has dedicated, hardcoded logic rather than attempting to create a generic solution.

## 🎯 Project Philosophy

Unlike generic Excel generation libraries, this API uses **template-specific approaches**:

-   Each Excel template (e.g., `Template-1.xlsx`) has its own dedicated generation logic
-   Predictable, reliable outputs tailored to specific business requirements
-   Clear mapping between API endpoints and Excel templates (`/api/reports/1` → `Template-1.xlsx`)
-   Easier to maintain and debug than complex generic systems

## 🚀 Quick Start

### Prerequisites

-   Python 3.8+
-   Virtual environment (recommended)

### Installation

1. **Clone and setup**:

    ```bash
    cd py-excel-api
    python -m venv venv

    # Windows
    venv\Scripts\activate

    # macOS/Linux
    source venv/bin/activate
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the API**:

    ```bash
    uvicorn app.main:app --reload
    ```

4. **Open your browser**: http://localhost:8000/docs

## 📁 Project Structure

```
py-excel-api/
├── app/
│   ├── api/                    # Domain-organized API routes
│   │   ├── health.py          # Health check endpoints
│   │   ├── templates.py       # Template management
│   │   └── reports.py         # Report generation endpoints
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   └── logging.py         # Logging setup
│   ├── models/                # Pydantic data models
│   │   ├── base.py           # Base response models
│   │   ├── reports.py        # Report request/response models
│   │   └── templates.py      # Template models
│   ├── services/              # Business logic
│   │   ├── excel_service.py  # Template-specific Excel generation
│   │   └── template_service.py # Template management
│   └── main.py               # FastAPI application entry point
├── templates/                 # Excel template files
│   └── Template-1.xlsx       # Sample template
├── tests/                    # Comprehensive test suite
│   ├── test_main.py         # Application tests
│   ├── test_services.py     # Service layer tests
│   └── test_api.py          # API endpoint tests
├── logs/                     # Application logs
├── build.py                  # Build validation script
└── requirements.txt          # Python dependencies
```

## 🔗 API Endpoints

### Health & Status

```http
GET /api/health                # Health check
GET /                          # API information
```

### Templates

```http
GET /api/templates             # List available templates
```

### Report Generation

```http
POST /api/reports/1            # Generate Template-1.xlsx report
```

## 📊 Template-Specific Usage

### Template-1 Report Generation

**Endpoint**: `POST /api/reports/1`

**Request Body**:

```json
{
	"company_name": "Acme Corporation",
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
```

**Response**: Excel file download with proper headers

**cURL Example**:

```bash
curl -X POST "http://localhost:8000/api/reports/1" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Corp",
    "report_date": "2025-11-06",
    "rows": [
      {
        "department": "Engineering",
        "revenue": 500000,
        "expenses": 100000,
        "profit": 400000
      }
    ]
  }' \
  --output report.xlsx
```

## 🧪 Testing

### Run All Tests

```bash
# Run complete test suite
pytest tests/ -v

# Run specific test files
pytest tests/test_api.py -v
pytest tests/test_services.py -v
pytest tests/test_main.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Test Categories

-   **`test_main.py`**: FastAPI application, health endpoints, error handling
-   **`test_services.py`**: Template-specific business logic, Excel utilities
-   **`test_api.py`**: Template-specific API routes, request/response validation

### Build Validation

```bash
# Comprehensive build check (equivalent to "npm run build")
python build.py
```

The build script validates:

-   ✅ Import validation
-   ✅ Syntax validation
-   ✅ Type checking (mypy)
-   ✅ FastAPI validation

## 🏗️ Development

### Adding a New Template

1. **Add template file**:

    ```bash
    # Place Excel template in templates/ directory
    templates/Template-2.xlsx
    ```

2. **Create template-specific logic** in `app/services/excel_service.py`:

    ```python
    def _generate_template_2_report(self, request: ReportRequest) -> ReportResponse:
        """Generate Template-2 specific report with hardcoded logic."""
        # Template-2 specific implementation
        pass
    ```

3. **Add route** in `app/api/reports.py`:

    ```python
    @router.post("/2")
    async def generate_template_2_report(data: dict):
        """Generate Template-2 report."""
        # Template-2 specific endpoint
        pass
    ```

4. **Add tests** in `tests/test_api.py`:
    ```python
    def test_template_2_report_generation(self):
        """Test Template-2 specific functionality."""
        pass
    ```

### Code Quality

**Type Checking**:

```bash
mypy app/
```

**Linting** (if using):

```bash
flake8 app/
black app/
```

**Pre-commit Validation**:

```bash
python build.py  # Runs all checks
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```env
# Application
APP_NAME=Python Excel API
APP_VERSION=1.0.0
DEBUG=True

# Server
HOST=127.0.0.1
PORT=8000

# Logging
LOG_LEVEL=INFO

# Templates
TEMPLATES_DIR=./templates

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### Logging Configuration

Logs are written to `logs/` directory:

-   **`application.log`**: General application logs
-   **`error.log`**: Error-specific logs (auto-rotated)

Log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## 🏭 Production Deployment

### Windows IIS Deployment

> **📋 For detailed IIS setup instructions, see [docs/IIS_DEPLOYMENT.md](docs/IIS_DEPLOYMENT.md)**

**Quick Setup:**

1. **Install Python 3.11+ on Windows Server**
2. **Install IIS with CGI/FastCGI support**
3. **Configure application pool and site**
4. **Set production environment variables**

**Production Environment:**

```env
DEBUG=False
LOG_LEVEL=WARNING
TEMPLATES_DIR=C:\inetpub\wwwroot\py-excel-api\templates
LOGS_DIR=C:\inetpub\logs\py-excel-api
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📋 API Documentation

### Interactive Documentation

-   **Swagger UI**: http://localhost:8000/docs
-   **ReDoc**: http://localhost:8000/redoc
-   **OpenAPI Schema**: http://localhost:8000/openapi.json

### Response Format

All JSON responses follow this structure:

**Success Response**:

```json
{
	"success": true,
	"data": {
		/* response data */
	},
	"message": "Operation completed successfully",
	"timestamp": "2025-11-06T10:30:00Z"
}
```

**Error Response**:

```json
{
	"success": false,
	"error": {
		"code": "HTTP_400",
		"message": "Validation error",
		"details": null
	},
	"timestamp": "2025-11-06T10:30:00Z"
}
```

## 🔍 Troubleshooting

### Common Issues

**Import Errors**:

```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

**Template Not Found**:

```bash
# Check templates directory structure
ls templates/
# Ensure Template-1.xlsx exists
```

**Port Already in Use**:

```bash
# Use different port
uvicorn app.main:app --port 8001

# Or kill existing process (Windows)
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

**Type Errors**:

```bash
# Run type checking
mypy app/

# Run build validation
python build.py
```

### Debug Mode

Enable detailed logging:

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

Check logs:

```bash
tail -f logs/application.log
```

## 🎓 Learning Resources

### For TypeScript Developers

This project mirrors Express.js patterns:

| Express.js      | FastAPI            |
| --------------- | ------------------ |
| `app.js`        | `app/main.py`      |
| `routes/`       | `app/api/`         |
| `middleware/`   | `app/middleware/`  |
| `npm run build` | `python build.py`  |
| `npm test`      | `pytest tests/`    |
| `package.json`  | `requirements.txt` |

### Key Differences

-   **Imports**: `from module import function` vs `import { function } from 'module'`
-   **Types**: Optional but recommended vs required in TypeScript
-   **Async**: `async def` vs `async function`
-   **Validation**: Pydantic models vs manual validation

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-template`
3. **Follow template-specific approach**: Each template gets dedicated logic
4. **Add tests**: Include comprehensive test coverage
5. **Run validation**: `python build.py`
6. **Submit pull request**

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

-   **Issues**: Create GitHub issue with error logs
-   **Documentation**: Check `/docs` endpoint for API reference
-   **Examples**: See `tests/` directory for usage examples

---

**Built with ❤️ using FastAPI and the template-specific approach to Excel automation.**
