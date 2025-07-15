#!/usr/bin/env python3
"""Setup script for Fund Analysis development environment."""
import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout

def main():
    """Main setup function."""
    project_root = Path(__file__).parent.parent
    # Create conda environment
    print("Setting up conda environment...")
    run_command("conda env create -f environment.yml", cwd=project_root)
    # Activate environment and install package in development mode
    print("Installing package in development mode...")
    run_command("conda run -n fund_fcst_1 pip install -e .", cwd=project_root)
    # Run validation
    print("Validating installation...")
    run_command("python scripts/validate_installation.py", cwd=project_root)
    print("Setup complete!")

if __name__ == "__main__":
    main()
