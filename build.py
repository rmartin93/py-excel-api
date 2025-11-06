#!/usr/bin/env python3
"""
Build validation script for the Python Excel API.
This is like 'npm run build' for TypeScript projects.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=Path.cwd())
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Run all validation checks."""
    print("🏗️  Building Python Excel API...")
    print("=" * 50)

    checks = [
        # Import validation (like TypeScript compilation)
        ("python -c \"import app.main; print('All imports successful')\"", "Import validation"),

        # Syntax checking
        ("python -m py_compile app/main.py app/models/reports.py app/api/reports.py", "Syntax validation"),

        # Type checking (like TypeScript compiler)
        ("mypy app --ignore-missing-imports --no-error-summary", "Type checking"),

        # FastAPI schema validation
        ("python -c \"from app.main import app; print('FastAPI app created successfully')\"", "FastAPI validation"),
    ]

    passed = 0
    failed = 0

    for cmd, description in checks:
        if run_command(cmd, description):
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 50)
    print(f"📊 Build Summary: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 BUILD SUCCESSFUL - All checks passed!")
        return 0
    else:
        print("💥 BUILD FAILED - Fix the errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())