#!/bin/bash

# Django Rate Limiter - Code Quality Check Script
# Run this script before committing to ensure code quality

set -e  # Exit on any error

echo "🔍 Running code quality checks for Django Rate Limiter..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository!"
    exit 1
fi

# Check if there are unstaged changes
if ! git diff-index --quiet HEAD --; then
    print_warning "You have unstaged changes. Consider staging them first."
fi

echo ""
echo "1️⃣  Running Black (code formatting)..."
if black --check django_rate_limiter tests; then
    print_status "Black formatting check passed"
else
    print_error "Black formatting failed. Run: black django_rate_limiter tests"
    exit 1
fi

echo ""
echo "2️⃣  Running isort (import sorting)..."
if isort --check-only --profile black django_rate_limiter tests; then
    print_status "Import sorting check passed"
else
    print_error "Import sorting failed. Run: isort --profile black django_rate_limiter tests"
    exit 1
fi

echo ""
echo "3️⃣  Running flake8 (linting)..."
if flake8 django_rate_limiter tests --max-line-length=88 --extend-ignore=E203,W503; then
    print_status "Flake8 linting passed"
else
    print_error "Flake8 linting failed. Fix the issues above."
    exit 1
fi

echo ""
echo "4️⃣  Running mypy (type checking)..."
if mypy django_rate_limiter --ignore-missing-imports --no-strict-optional; then
    print_status "Type checking passed"
else
    print_error "Type checking failed. Fix the type annotations above."
    exit 1
fi

echo ""
echo "5️⃣  Running pytest (tests)..."
if python -m pytest tests/ -v --tb=short; then
    print_status "All tests passed"
else
    print_error "Tests failed. Fix the failing tests above."
    exit 1
fi

echo ""
echo "6️⃣  Checking package build..."
if python -m build --wheel --sdist > /dev/null 2>&1; then
    print_status "Package builds successfully"
    # Clean up build artifacts
    rm -rf dist/ build/ *.egg-info/
else
    print_error "Package build failed"
    exit 1
fi

echo ""
echo "=================================================="
print_status "🎉 All checks passed! Your code is ready to commit."
echo ""
echo "To commit your changes, run:"
echo "  git add ."
echo "  git commit -m 'Your commit message'"
echo "  git push origin main"
