# Django Rate Limiter - Development Tools

This directory contains various tools and scripts to enforce code quality before committing.

## Quick Start

Run the setup script to configure your development environment:

```bash
./setup-dev.sh
```

This will install all dependencies and set up pre-commit hooks.

## Available Tools

### 1. Pre-commit Hooks (Recommended) ⭐

**File:** `.pre-commit-config.yaml`

Automatically runs on every commit:
```bash
# Setup (run once)
pip install pre-commit
pre-commit install

# Manual run on all files
pre-commit run --all-files
```

### 2. Shell Script

**File:** `check-code.sh`

```bash
./check-code.sh
```

### 3. Python Script (Cross-platform)

**File:** `check_quality.py`

```bash
python check_quality.py
```

### 4. Makefile

**File:** `Makefile`

```bash
# Run all checks
make check

# Individual commands
make format     # Black + isort
make lint       # Flake8
make type-check # Mypy
make test       # Pytest
make build      # Build package

# Quick commit workflow
make quick-commit
```

### 5. Manual Git Hook

**File:** `scripts/pre-commit`

```bash
# Install manually
cp scripts/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## What Gets Checked

All tools run the same quality checks:

1. **🎨 Black** - Code formatting
2. **📦 isort** - Import sorting  
3. **🔍 Flake8** - Linting (PEP 8)
4. **🏷️ Mypy** - Type checking
5. **🧪 Pytest** - All tests
6. **📦 Build** - Package build verification

## Usage Examples

### Before Every Commit
```bash
# Option 1: Automatic (with pre-commit hooks)
git commit -m "Your message"  # Hooks run automatically

# Option 2: Manual check first
./check-code.sh && git add . && git commit -m "Your message"

# Option 3: Using Make
make check && git add . && git commit -m "Your message"
```

### Fix Formatting Issues
```bash
# Auto-fix formatting
black django_rate_limiter tests
isort --profile black django_rate_limiter tests

# Or using Make
make format
```

### CI/CD Integration

The same checks run in GitHub Actions (`.github/workflows/ci.yml`):

- ✅ Multiple Python/Django versions
- ✅ Code formatting verification  
- ✅ Linting and type checking
- ✅ Full test suite
- ✅ Package build verification

## Configuration Files

- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `pyproject.toml` - Tool configurations (Black, isort, mypy, pytest)
- `setup.cfg` - Additional pytest configuration
- `pytest.ini` - Pytest settings

## Troubleshooting

### Common Issues

1. **Import sorting fails**
   ```bash
   isort --profile black django_rate_limiter tests
   ```

2. **Formatting fails**
   ```bash
   black django_rate_limiter tests
   ```

3. **Type checking fails**
   - Fix type annotations in the reported files
   - Add `# type: ignore` for unavoidable issues

4. **Tests fail**
   ```bash
   python -m pytest tests/ -v --tb=long
   ```

### Bypass Checks (Not Recommended)

```bash
# Skip pre-commit hooks
git commit --no-verify -m "Your message"

# Skip individual checks in scripts
# (Edit the script to comment out specific checks)
```

## Benefits

- 🚫 **Prevents broken commits** - Catches issues before they reach the repository
- 🎨 **Consistent code style** - Automatic formatting with Black and isort  
- 🐛 **Early bug detection** - Type checking and linting catch errors early
- 🧪 **Reliable tests** - Ensures all tests pass before committing
- 👥 **Team consistency** - Everyone uses the same standards
- ⚡ **Fast feedback** - Issues are caught locally, not in CI

Choose the tool that works best for your workflow! The pre-commit hooks are recommended for automatic enforcement.
