# Development Setup Guide

## Prerequisites

- Python 3.8+
- Django 3.2+
- Redis (optional, for Redis backend)

## Quick Setup

1. **Clone and setup the development environment:**
   ```bash
   cd /path/to/your/project
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   pip install -e .[dev]
   ```

2. **Run tests:**
   ```bash
   pytest tests/ -v
   pytest tests/ --cov=django_rate_limiter --cov-report=html
   ```

3. **Try the demo:**
   ```bash
   python demo.py
   ```

## VS Code Development

This project includes VS Code tasks for common development activities:

- **Install Package in Development Mode**: Installs the package in editable mode
- **Run Tests with Coverage**: Runs the full test suite with coverage reporting

Use `Ctrl+Shift+P` → "Tasks: Run Task" to access these.

## Project Structure

```
django_rate_limiter/
├── __init__.py           # Package exports
├── algorithms.py         # Rate limiting algorithms
├── backends.py          # Storage backends
├── decorators.py        # Django decorators
├── exceptions.py        # Custom exceptions
├── middleware.py        # Django middleware
├── models.py           # Django models
├── utils.py            # Utility functions
├── apps.py             # Django app configuration
└── management/         # Django management commands
    └── commands/
        └── cleanup_rate_limits.py

tests/
├── __init__.py
├── settings.py         # Test Django settings
├── urls.py            # Test URL patterns
├── test_algorithms.py  # Algorithm tests
└── test_backends.py   # Backend tests
```

## Adding New Features

1. **New Algorithm**: Add to `algorithms.py`, inherit from `BaseRateLimiter`
2. **New Backend**: Add to `backends.py`, inherit from `BaseBackend`
3. **Tests**: Add corresponding tests in `tests/`
4. **Documentation**: Update README.md with usage examples

## Code Quality

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Ensure thread safety for concurrent operations
- Add tests for new functionality

## Release Process

1. Update version in `setup.py` and `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Build and test package: `python -m build`
5. Upload to PyPI: `twine upload dist/*`
