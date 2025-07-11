.PHONY: help install dev-install test lint format type-check check clean build all

# Default target
help:
	@echo "Django Rate Limiter - Development Commands"
	@echo "=========================================="
	@echo "Available commands:"
	@echo "  install      - Install package in development mode"
	@echo "  dev-install  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run flake8 linting"
	@echo "  format       - Run black and isort formatting"
	@echo "  type-check   - Run mypy type checking"
	@echo "  check        - Run all quality checks (format, lint, type-check, test)"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  all          - Run check + build"

# Installation targets
install:
	pip install -e .

dev-install: install
	pip install pytest pytest-django pytest-cov black flake8 mypy isort pre-commit build twine

# Testing
test:
	python -m pytest tests/ -v --cov=django_rate_limiter --cov-report=term

test-verbose:
	python -m pytest tests/ -v --cov=django_rate_limiter --cov-report=term --cov-report=html

# Code quality
format:
	@echo "Running Black..."
	black django_rate_limiter tests
	@echo "Running isort..."
	isort --profile black django_rate_limiter tests

lint:
	@echo "Running flake8..."
	flake8 django_rate_limiter tests --max-line-length=88 --extend-ignore=E203,W503

type-check:
	@echo "Running mypy..."
	mypy django_rate_limiter --ignore-missing-imports --no-strict-optional

# Combined checks
check: format lint type-check test
	@echo "✅ All quality checks passed!"

# Build and clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

# Pre-commit setup
setup-pre-commit:
	pre-commit install
	pre-commit install --hook-type commit-msg

# Run everything
all: check build
	@echo "🎉 All checks and build completed successfully!"

# Quick commit workflow
quick-commit: check
	@echo "Ready to commit! Run: git add . && git commit -m 'Your message' && git push"
