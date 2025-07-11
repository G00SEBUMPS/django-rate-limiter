#!/usr/bin/env python3
"""
Django Rate Limiter - Code Quality Check Script

Cross-platform Python script to run all quality checks before committing.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description, cwd=None):
    """Run a command and return True if successful."""
    print(f"\n🔧 {description}...")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {description} passed")
            return True
        else:
            print(f"❌ {description} failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ {description} failed with error: {e}")
        return False


def main():
    """Run all quality checks."""
    print("🚀 Django Rate Limiter - Code Quality Checker")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if we're in the right directory
    if not Path("django_rate_limiter").exists():
        print("❌ Error: django_rate_limiter directory not found!")
        print("Make sure you're running this from the project root.")
        sys.exit(1)
    
    checks = [
        ("black --check django_rate_limiter tests", "Black formatting check"),
        ("isort --check-only --profile black django_rate_limiter tests", "Import sorting check"),
        ("flake8 django_rate_limiter tests --max-line-length=88 --extend-ignore=E203,W503", "Flake8 linting"),
        ("mypy django_rate_limiter --ignore-missing-imports --no-strict-optional", "Type checking"),
        ("python -m pytest tests/ -v", "Running tests"),
    ]
    
    failed_checks = []
    
    for command, description in checks:
        if not run_command(command, description):
            failed_checks.append(description)
    
    print("\n" + "=" * 50)
    
    if failed_checks:
        print(f"❌ {len(failed_checks)} check(s) failed:")
        for check in failed_checks:
            print(f"   • {check}")
        print("\n🔧 To fix formatting issues, run:")
        print("   python -m black django_rate_limiter tests")
        print("   python -m isort --profile black django_rate_limiter tests")
        sys.exit(1)
    else:
        print("🎉 All checks passed! Your code is ready to commit.")
        print("\n📦 To build the package, run:")
        print("   python -m build")
        print("\n📝 To commit your changes, run:")
        print("   git add .")
        print("   git commit -m 'Your commit message'")
        print("   git push origin main")


if __name__ == "__main__":
    main()
