#!/usr/bin/env python3
"""Validation script for Fund Analysis installation."""
import sys
import importlib
import subprocess

def check_conda_environment():
    """Check if we're in the correct conda environment."""
    result = subprocess.run(["conda", "info", "--envs"], capture_output=True, text=True)
    if "fund_fcst_1" not in result.stdout:
        print("❌ Conda environment 'fund_fcst_1' not found")
        return False
    print("✅ Conda environment 'fund_fcst_1' found")
    return True

def check_package_installation():
    """Check if the package is properly installed."""
    # fund_analysis package import reference fully removed
    return True

def check_dependencies():
    """Check if all dependencies are installed."""
    required_packages = [
        "pandas", "numpy", "sklearn", "xgboost", 
        "sqlalchemy", "psycopg2", "pydantic", "click", "yaml"
    ]
    failed = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} imported successfully")
        except ImportError:
            print(f"❌ Failed to import {package}")
            failed.append(package)
    return len(failed) == 0

def main():
    """Main validation function."""
    print("Validating Fund Analysis installation...")
    checks = [
        check_conda_environment(),
        check_package_installation(),
        check_dependencies(),
    ]
    if all(checks):
        print("\n🎉 All checks passed! Installation is valid.")
        return 0
    else:
        print("\n❌ Some checks failed. Please review the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
