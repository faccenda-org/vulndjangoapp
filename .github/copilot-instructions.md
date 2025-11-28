# GitHub Copilot Instructions for vulndjangoapp

## Project Overview
This is a deliberately vulnerable Django application for security testing and educational purposes. It contains intentional security vulnerabilities and uses outdated dependencies.

## Critical Instructions

### Documentation Maintenance
**ALWAYS keep README.md synchronized with code changes:**

1. **When adding/modifying endpoints:**
   - Update the "Available Endpoints" section in README.md
   - Document the vulnerability type and test payload

2. **When changing file structure:**
   - Update the "File Structure" section in README.md
   - Ensure all paths match actual directory structure

3. **When updating dependencies:**
   - Update vulnerability descriptions in README.md
   - Document CVE numbers for vulnerable packages
   - Update the setup instructions if dependency management changes

4. **When adding/modifying security vulnerabilities:**
   - Add to "Known Vulnerabilities" section in README.md
   - Include location, vulnerability type, and test examples

5. **When changing module/app names:**
   - Update all references throughout README.md (e.g., `webapp` vs `vulnapp`)
   - Update import examples in setup instructions

6. **When modifying CI/CD workflows:**
   - Update "CI/CD Workflows" section in README.md
   - Document new automation features

### Code Standards

1. **Intentional Vulnerabilities:**
   - This project INTENTIONALLY contains security flaws
   - Mark vulnerable code with comments: `# VULNERABLE: <reason>`
   - Never "fix" security issues unless explicitly asked

2. **Testing:**
   - All new features must have corresponding tests in `webapp/tests.py`
   - Tests should verify the vulnerability exists (not fix it)

3. **Code Quality:**
   - Follow Ruff linting rules (configured in `pyproject.toml`)
   - Use type hints where appropriate
   - Maintain consistent formatting

4. **Dependencies:**
   - Main dependencies are INTENTIONALLY vulnerable
   - Only suggest updates if explicitly asked
   - Document any CVEs when adding new vulnerable dependencies

### Automation
- Dependabot is configured for automated dependency updates
- Auto-merge workflow handles Dependabot PRs based on semver rules
- Pre-commit hooks enforce code quality (but allow intentional vulnerabilities)

## Remember
This is an EDUCATIONAL project demonstrating vulnerabilities. Never suggest security fixes unless explicitly requested. The goal is to help people learn about security flaws in a controlled environment.
