# Vulnerable Django Application

⚠️ **WARNING: This application contains intentional security vulnerabilities for educational and testing purposes only. DO NOT USE IN PRODUCTION!**

## Overview

This is a deliberately vulnerable Django application built to demonstrate common web security vulnerabilities. It uses Django 3.2.0, which contains multiple known critical CVEs.

## Requirements

- Python 3.8+
- uv (package manager)

## Setup

1. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

2. **Run database migrations:**
   ```bash
   uv run python manage.py migrate
   ```

3. **Create a test user (optional):**
   ```bash
   uv run python manage.py shell
   ```
   Then in the Python shell:
   ```python
   from vulnapp.models import User
   User.objects.create(username='admin', password='admin123', email='admin@example.com', is_admin=True)
   User.objects.create(username='user', password='password', email='user@example.com', is_admin=False)
   exit()
   ```

4. **Run the development server:**
   ```bash
   uv run python manage.py runserver
   ```

5. **Access the application:**
   Open http://127.0.0.1:8000/ in your browser

## Known Vulnerabilities

### 1. **Vulnerable Django Version (3.2.0)**
   - Contains multiple critical CVEs including:
     - CVE-2021-28658: Directory traversal via archive extraction
     - CVE-2021-31542: File upload validation bypass
     - CVE-2021-33203: Potential path traversal via uploaded files
     - CVE-2021-33571: URLValidator regular expression denial-of-service
     - And many more...

### 2. **SQL Injection**
   - **Location:** `/search/` endpoint
   - **Vulnerability:** Raw SQL queries with unsanitized user input
   - **Test:** Try `admin' OR '1'='1` in the username field

### 3. **Cross-Site Scripting (XSS)**
   - **Location:** `/comments/` endpoint
   - **Vulnerability:** User input rendered without sanitization
   - **Test:** Post `<script>alert('XSS')</script>` as a comment

### 4. **CSRF Protection Disabled**
   - **Location:** Global setting in `settings.py`
   - **Vulnerability:** CsrfViewMiddleware is commented out
   - **Impact:** All POST requests are vulnerable to CSRF attacks

### 5. **Path Traversal**
   - **Location:** `/profile/` endpoint
   - **Vulnerability:** Unsanitized file path input
   - **Test:** Try `?file=../../../etc/passwd`

### 6. **Hardcoded Secret Key**
   - **Location:** `settings.py`
   - **Vulnerability:** Secret key is hardcoded in source code
   - **Impact:** Can be used to forge session cookies

### 7. **Plain Text Password Storage**
   - **Location:** User model in `models.py`
   - **Vulnerability:** Passwords stored without hashing
   - **Impact:** Complete password exposure if database is compromised

### 8. **Weak Authentication**
   - **Location:** `/login/` endpoint
   - **Vulnerability:** No rate limiting, timing attacks possible
   - **Impact:** Vulnerable to brute force and timing attacks

### 9. **Insecure Security Headers**
   - **Location:** `settings.py`
   - **Vulnerabilities:**
     - XSS filter disabled
     - Content type sniffing allowed
     - Insecure cookies
     - Clickjacking allowed

### 10. **No Password Validation**
   - **Location:** `settings.py`
   - **Vulnerability:** `AUTH_PASSWORD_VALIDATORS` is empty
   - **Impact:** Users can set weak passwords

## File Structure

```
vulndjangoapp/
├── manage.py
├── pyproject.toml          # uv configuration with vulnerable Django 3.2.0
├── uv.lock                 # Locked dependencies
├── vulndjangoapp/
│   ├── __init__.py
│   ├── settings.py         # Insecure Django settings
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── vulnapp/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py           # Vulnerable data models
    ├── urls.py
    ├── views.py            # Vulnerable view functions
    └── templates/
        └── vulnapp/
            ├── index.html
            ├── search.html
            ├── comments.html
            └── login.html
```

## Educational Use

This application is designed for:
- Security training and education
- Penetration testing practice
- Vulnerability scanning tool testing
- Security awareness demonstrations

## Security Tools to Test With

- **OWASP ZAP** - Web application security scanner
- **Burp Suite** - Web vulnerability scanner
- **SQLMap** - Automated SQL injection testing
- **Bandit** - Python security linter
- **Safety** - Dependency vulnerability scanner

Run dependency scan:
```bash
uv run pip install safety
uv run safety check
```

## License

This is for educational purposes only. Use at your own risk.

## Disclaimer

This application is intentionally insecure. Never deploy this to production or any publicly accessible server. The maintainers are not responsible for any misuse of this code.
