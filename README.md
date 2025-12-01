# Vulnerable Django Application

⚠️ **WARNING: This application contains intentional security vulnerabilities for educational and testing purposes only. DO NOT USE IN PRODUCTION!**

## Overview

This is a deliberately vulnerable Django application built to demonstrate common web security vulnerabilities. It uses Django 3.2.0, which contains multiple known critical CVEs.

## Requirements

- Python 3.11+
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
   from webapp.models import User
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
   - **Location:** Global setting in `config/settings.py`
   - **Vulnerability:** CsrfViewMiddleware is commented out
   - **Impact:** All POST requests are vulnerable to CSRF attacks

### 5. **Path Traversal**
   - **Location:** `/profile/` endpoint
   - **Vulnerability:** Unsanitized file path input
   - **Test:** Try `?file=../../../etc/passwd`

### 6. **Hardcoded Secret Key**
   - **Location:** `config/settings.py`
   - **Vulnerability:** Secret key is hardcoded in source code
   - **Impact:** Can be used to forge session cookies

### 7. **Plain Text Password Storage**
   - **Location:** User model in `webapp/models.py`
   - **Vulnerability:** Passwords stored without hashing
   - **Impact:** Complete password exposure if database is compromised

### 8. **Weak Authentication**
   - **Location:** `/login/` endpoint
   - **Vulnerability:** No rate limiting, timing attacks possible
   - **Impact:** Vulnerable to brute force and timing attacks

### 9. **Insecure Security Headers**
   - **Location:** `config/settings.py`
   - **Vulnerabilities:**
     - XSS filter disabled
     - Content type sniffing allowed
     - Insecure cookies
     - Clickjacking allowed

### 10. **No Password Validation**
   - **Location:** `config/settings.py`
   - **Vulnerability:** `AUTH_PASSWORD_VALIDATORS` is empty
   - **Impact:** Users can set weak passwords

### 11. **Server-Side Template Injection (SSTI)**
   - **Location:** `/template/` endpoint
   - **Vulnerability:** User-provided Jinja2 templates rendered without sandboxing
   - **Test:** Try `{{ config.items() }}` or `{{ ''.__class__.__mro__[1].__subclasses__() }}`
   - **Impact:** Arbitrary code execution on the server

### 12. **Vulnerable Dependencies**
   - **Pillow 9.3.0**: CVE-2023-50447 (Arbitrary code execution via crafted images)
   - **PyYAML 5.3.1**: CVE-2020-14343 (Arbitrary code execution via unsafe YAML loading)
   - **Requests 2.32.0**: Potential SSRF vulnerabilities
   - **Jinja2 2.11.3**: CVE-2024-22195 (XSS), CVE-2020-28493 (ReDoS)

## File Structure

```
vulndjangoapp/
├── manage.py
├── pyproject.toml          # Project configuration with vulnerable dependencies
├── uv.lock                 # Locked dependencies (managed by uv)
├── db.sqlite3              # SQLite database (created after migrations)
├── .github/
│   ├── dependabot.yml      # Dependabot configuration for automated updates
│   └── workflows/
│       ├── auto-merge-dependabot.yml  # Auto-merge workflow for Dependabot PRs
│       ├── tests.yml       # Automated testing workflow
│       └── code-quality.yml  # Code quality and security checks
├── scripts/
│   └── auto_merge.py       # Dependabot auto-merge decision helper
├── config/
│   ├── __init__.py
│   ├── settings.py         # Insecure Django settings
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── webapp/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py           # Vulnerable data models
    ├── urls.py
    ├── views.py            # Vulnerable view functions
    ├── utils.py            # Utility functions using vulnerable dependencies
    ├── tests.py            # Unit tests
    ├── migrations/
    │   └── 0001_initial.py
    └── templates/
        └── webapp/
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
- Testing automated dependency management and security workflows

## Automated Dependency Management

This project uses **Dependabot** with automated PR processing:

- **Dependabot**: Configured via `.github/dependabot.yml` to automatically check for dependency updates weekly
- **Auto-merge workflow**: Automatically evaluates and merges Dependabot PRs based on:
  - **Patch updates**: Auto-merged automatically
  - **Minor updates**: Auto-merged if compatibility score ≥ 80%
  - **Major updates**: Require manual review
- **Update grouping**: Patch and minor updates are grouped to reduce PR noise
- **Lock file support**: Automatically updates both `pyproject.toml` and `uv.lock`

### Auto-merge Decision Logic

The `scripts/auto_merge.py` script evaluates Dependabot PRs using:
1. Semantic versioning analysis (Major/Minor/Patch)
2. Dependabot compatibility score extraction
3. Configurable threshold (default: 80%)
4. Support for manual override via `no-auto-merge` label

## CI/CD Workflows

### Automated Tests
- Runs on every PR and push to main/develop
- Executes Django migrations and unit tests
- Uses `uv` for dependency management

### Code Quality Checks
- **Ruff**: Linting and formatting
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checking
- **Pre-commit hooks**: Automated code quality enforcement

### Auto-merge Dependabot
- Evaluates Dependabot PRs automatically
- Enables GitHub's native auto-merge for qualifying updates
- Posts detailed decision rationale as PR comments
- Supports manual threshold override via workflow dispatch

## Security Tools to Test With

- **OWASP ZAP** - Web application security scanner
- **Burp Suite** - Web vulnerability scanner
- **SQLMap** - Automated SQL injection testing
- **Bandit** - Python security linter
- **Safety** - Dependency vulnerability scanner
- **Ruff** - Fast Python linter with security rules

Run security scans:
```bash
# Install security tools
uv sync --group lint

# Run Bandit security scan
uv run bandit -r webapp/ config/

# Run Safety dependency check
uv run safety check

# Run Ruff linter
uv run ruff check .
```

## License

This is for educational purposes only. Use at your own risk.

## Disclaimer

This application is intentionally insecure. Never deploy this to production or any publicly accessible server. The maintainers are not responsible for any misuse of this code.
