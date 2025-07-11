#!/bin/bash

# Django Rate Limiter - Development Setup Script

echo "🔧 Setting up Django Rate Limiter development environment..."
echo "=" * 60

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install -e .
pip install pytest pytest-django pytest-cov black flake8 mypy isort pre-commit build twine

# Install pre-commit hooks (Option 1 - using pre-commit tool)
echo ""
echo "🪝 Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "✅ Pre-commit hooks installed successfully!"
else
    echo "⚠️  pre-commit not found. Installing..."
    pip install pre-commit
    pre-commit install
    echo "✅ Pre-commit hooks installed successfully!"
fi

# Alternative: Manual git hook installation (Option 2)
echo ""
echo "🔧 Alternative: Manual git hook setup available"
echo "To install manual git hooks, run:"
echo "  cp scripts/pre-commit .git/hooks/pre-commit"

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  ./check-code.sh       - Run all quality checks manually"
echo "  python check_quality.py - Cross-platform quality check"
echo "  make check           - Run checks using Makefile"
echo "  pre-commit run --all-files - Run pre-commit on all files"
echo ""
echo "The pre-commit hooks will now run automatically before each commit."
