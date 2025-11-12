# IIS + FastAPI Flow (Windows + WFastCGI)

```text
Browser
   │
   ▼
IIS (Windows Web Server)
   │  - Handles HTTP request
   │  - Windows Authentication (Kerberos/NTLM)
   ▼
FastCGI / WFastCGI
   │  - Bridge between IIS and Python
   │  - Passes CGI/WSGI environment variables
   ▼
WSGI Callable (entry point)
   │  - Receives `environ` and `start_response`
   │  - `environ` contains:
   │      - REMOTE_USER
   │      - AUTH_USER
   │      - cs-username
   │      - other headers
   ▼
ASGIMiddleware (from a2wsgi)
   │  - Converts WSGI `environ` → ASGI `scope`
   │  - Converts `start_response` → ASGI send/receive
   ▼
FastAPI Application
   │  - Your async app receives ASGI `scope`
   │  - Headers and user info can be accessed via:
   │      `request.scope["wsgi_environ"]["AUTH_USER"]`
   │      `request.scope["headers"]`
   ▼
Response returned back to Browser
```
