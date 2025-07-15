# Task 1.1: Environment Setup & Project Structure

## Overview

This task implements the foundational environment setup and project structure for the Fund_Fcst_1 refactoring project. It establishes the base infrastructure required for all subsequent development phases.

## Context from Project Plan

**Phase**: Phase 1 - Foundation & Core Infrastructure  
**Step**: 1.1 - Environment Setup & Project Structure  
**Priority**: Critical - All subsequent tasks depend on this foundation

## Deliverables

1. Set up dedicated conda environment for the project
2. Create proper project structure with clear separation
3. Implement proper package management and dependencies

## Current State Analysis

Based on the existing project structure in `c:\Users\krajcovic\Documents\GitHub\Fund_Fcst_1\`, the current state includes:

### Existing Structure
```
Fund_Fcst_1/
├── environment.yml                 # Existing conda environment file
├── project_plan.md                # Project planning document
├── README.md                      # Project documentation
├── EnergyTrading/                 # Main legacy codebase
│   ├── Python/                    # Python modules
│   │   ├── Enums.py              # Configuration enums
│   │   ├── poetry.lock           # Poetry dependencies
│   │   ├── pyproject.toml        # Poetry configuration
│   │   └── [various modules]     # Legacy modules
├── InstructionsRepo/              # Instructions and documentation
├── mcp/                          # MCP server components
├── tasks/                        # Task management (where this file is)
└── tasks_summary/                # Task summaries
```

### Issues with Current Structure
1. **Mixed Environment Management**: Both conda (`environment.yml`) and Poetry (`pyproject.toml`) present
2. **Unclear Project Structure**: Legacy code mixed with new development
3. **No Dedicated Environment**: Need project-specific conda environment
4. **Missing Development Tools**: No standardized development tools setup
5. **Legacy fund_analysis dependency removed**: The new project does not require the legacy fund_analysis package for installation or import. All references and dependencies have been removed except in untouched legacy code.

## Implementation Plan


### 1. Conda Environment Setup

#### 1.1 Delete and Recreate Dedicated Environment
**Important:** If a conda environment named `fund_fcst_1` already exists, it must be deleted and recreated from scratch to ensure a clean, reproducible setup. This avoids legacy package conflicts and ensures all dependencies are managed consistently.

```powershell
# Delete existing environment if present
conda deactivate; conda env remove -n fund_fcst_1

# Recreate environment with the same name
conda create -n fund_fcst_1 python=3.11

# Activate the environment
conda activate fund_fcst_1
```


#### 1.2 Install Dependencies from requirements.txt
Install all required packages using the provided `requirements.txt` file to ensure exact package versions and compatibility. This file is the single source of truth for all dependencies:

```powershell
# Install dependencies from requirements.txt
pip install -r EnergyTrading/Python/Utilities/fund_analysis/requirements.txt
```

#### 1.3 Export Environment
After installation, export the environment to `environment.yml` for reproducibility. This ensures that the conda environment reflects all installed packages:

```powershell
conda env export -n fund_fcst_1 > environment.yml
```

#### 1.4 Update VS Code Configuration
Update `.vscode/settings.json` to use the new environment:

```json
{
    "python.defaultInterpreterPath": "C:\\Users\\krajcovic\\anaconda3\\envs\\fund_fcst_1\\python.exe",
    "python.terminal.activateEnvironment": true,
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ]
}
```


### 2. Project Structure Reorganization

#### 2.1 Create New Project Structure
Transform the project into a clean, modular structure:

```
fund_analysis/
├── README.md                      # Main project documentation
├── environment.yml                # Conda environment specification
├── pyproject.toml                 # Python project configuration
├── setup.py                       # Package setup (if needed)
├── .gitignore                     # Git ignore file
├── .vscode/                       # VS Code configuration
│   └── settings.json             # Python environment settings
├── src/                          # Source code (new structure)
│   └── fund_analysis/
│       ├── __init__.py
│       ├── core/                 # Core interfaces and abstractions
│       │   ├── __init__.py
│       │   ├── interfaces.py     # Abstract base classes
│       │   ├── config.py         # Configuration management
│       │   └── di_container.py   # Dependency injection
│       ├── data/                 # Data layer (refactored input_data)
│       │   ├── __init__.py
│       │   ├── base_loader.py    # Base data loader
│       │   └── handlers/         # Data type handlers
│       ├── scenarios/            # Scenario generation
│       │   ├── __init__.py
│       │   └── base.py          # Base scenario classes
│       ├── models/               # ML models
│       │   ├── __init__.py
│       │   └── base.py          # Base model classes
│       ├── analysis/             # Spread calculations
│       │   ├── __init__.py
│       │   └── base.py          # Base analysis classes
│       ├── utils/                # Utilities
│       │   ├── __init__.py
│       │   └── helpers.py       # Helper functions
│       └── cli/                  # Command line interface
│           ├── __init__.py
│           └── main.py          # Main CLI entry point
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── unit/                     # Unit tests
│   │   ├── __init__.py
│   │   ├── test_data/
│   │   ├── test_scenarios/
│   │   ├── test_models/
│   │   └── test_analysis/
│   ├── integration/              # Integration tests
│   │   ├── __init__.py
│   │   └── test_cli/
│   └── fixtures/                 # Test fixtures
├── config/                       # Configuration files
│   ├── base.yaml                 # Base configuration
│   ├── dev.yaml                  # Development overrides
│   └── prod.yaml                 # Production overrides
├── docs/                         # Documentation
│   ├── api/                      # API documentation
│   ├── user_guide/               # User guides
│   └── developer/                # Developer documentation
├── examples/                     # Example scripts and notebooks
│   ├── data_loading/
│   ├── scenarios/
│   ├── modeling/
│   └── analysis/
├── scripts/                      # Utility scripts
│   ├── setup_environment.py     # Environment setup script
│   └── validate_installation.py # Installation validation
├── legacy/                       # Legacy code (moved from EnergyTrading)
│   └── EnergyTrading/           # Preserved legacy structure
└── logs/                        # Log files
```

#### 2.2 Migration Strategy
1. **Preserve Legacy Code**: Move existing `EnergyTrading/` to `legacy/EnergyTrading/`
2. **Create New Structure**: Implement new `src/fund_analysis/` structure
3. **Maintain Compatibility**: Ensure existing workflows continue to work
4. **Gradual Migration**: Phase-by-phase migration of components

### 3. Package Management Setup

#### 3.1 Create New pyproject.toml

```toml
build-backend = "setuptools.build_meta"
# pyproject.toml should be generated from requirements.txt for consistency.
# Use a tool like pipreqs, poetry, or manual conversion to ensure all dependencies match.
# Example:
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "fund-analysis"
version = "0.1.0"
description = "Fundamental Forecasting Pipeline for Energy Trading"
readme = "README.md"
requires-python = ">=3.11"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Financial and Insurance Industry",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    # All dependencies from requirements.txt should be listed here
    # The legacy fund_analysis package is NOT required and should NOT be listed here.
]
```

#### 3.2 Update environment.yml

```yaml
# environment.yml should be generated from the active conda environment after installing all dependencies from requirements.txt
# Example:
name: fund_fcst_1
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - pip:
      - -r EnergyTrading/Python/Utilities/fund_analysis/requirements.txt
```

### 4. Development Tools Setup

#### 4.1 Create Development Scripts
Create helper scripts for development workflow:

**scripts/setup_environment.py**:
```python
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
```

**scripts/validate_installation.py**:
```python
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

def check_dependencies():
    """Check if all dependencies are installed."""
    required_packages = [
        "pandas", "numpy", "scikit-learn", "xgboost", 
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
```

## Implementation Steps

### Step 1: Environment Setup (Priority: High)
1. **Create conda environment**: `conda create -n fund_fcst_1 python=3.11`
2. **Install dependencies**: Use the provided environment.yml
3. **Update VS Code settings**: Configure Python interpreter path
4. **Validate environment**: Run validation scripts

### Step 2: Directory Structure Creation (Priority: High)
1. **Create new directory structure**: Follow the defined structure
2. **Move legacy code**: Preserve existing code in `legacy/` directory
3. **Create placeholder files**: Add `__init__.py` files and basic structure
4. **Update imports**: Ensure backward compatibility

### Step 3: Package Configuration (Priority: Medium)
1. **Create pyproject.toml**: Define package metadata and dependencies
2. **Update environment.yml**: Standardize conda environment
3. **Create development scripts**: Setup and validation scripts
4. **Configure development tools**: Black, flake8, mypy, pytest

### Step 4: Validation and Testing (Priority: Medium)
1. **Run validation scripts**: Ensure environment is correctly set up
2. **Test basic imports**: Verify package structure works (excluding any fund_analysis package import)
3. **Create basic tests**: Foundation for testing framework
4. **Document setup process**: Update README with setup instructions

## Success Criteria

### Environment Setup
- [ ] Conda environment `fund_fcst_1` created successfully
- [ ] All required packages installed without conflicts
- [ ] VS Code configured to use the new environment
- [ ] Environment validation script passes

### Project Structure
- [ ] New directory structure created according to plan
- [ ] Legacy code preserved in `legacy/` directory
- [ ] All `__init__.py` files created
- [ ] Basic package imports work (excluding any fund_analysis package import)

### Package Management
- [ ] `pyproject.toml` created with correct dependencies
- [ ] `environment.yml` updated and functional
- [ ] Development tools configured (black, flake8, mypy, pytest)
- [ ] Package installable in development mode

### Documentation
- [ ] README updated with setup instructions
- [ ] Development scripts documented
- [ ] VS Code configuration documented
- [ ] Environment validation documented

## Dependencies

### Prerequisites
- Conda installed on the system
- VS Code with Python extension
- Git repository access
- Windows PowerShell (current environment)

### Blocks
This task blocks all subsequent tasks as it provides the foundation for:
- Step 1.2: Core Interfaces & Abstractions
- Step 1.3: Configuration & Environment Management
- All Phase 2+ tasks

### Risks and Mitigation

#### Risk: Environment Conflicts
**Mitigation**: Use dedicated conda environment, test thoroughly

#### Risk: Legacy Code Compatibility
**Mitigation**: Preserve legacy structure, maintain import paths

#### Risk: Package Dependency Issues
**Mitigation**: Test installation on clean environment, provide fallback options

#### Risk: VS Code Configuration Issues
**Mitigation**: Provide detailed configuration instructions, test on Windows

## Validation Checklist

Before marking this task complete, verify:

1. **Environment Functionality**:
   - [ ] `conda activate fund_fcst_1` works
   - [ ] All required packages import successfully
   - [ ] VS Code uses correct Python interpreter
   - [ ] Terminal automatically activates environment

2. **Project Structure**:
   - [ ] New directory structure exists
   - [ ] Legacy code preserved and accessible
   - [ ] Package imports work from new structure (excluding any fund_analysis package import)
   - [ ] All placeholder files created

3. **Development Tools**:
   - [ ] Black formatting works
   - [ ] Flake8 linting works
   - [ ] MyPy type checking works
   - [ ] Pytest test discovery works

4. **Documentation**:
   - [ ] Setup instructions are clear
   - [ ] All scripts are documented
   - [ ] Configuration files are explained
   - [ ] Next steps are identified

## Next Steps

After completing this task:
1. Proceed to **Task 1.2**: Core Interfaces & Abstractions
2. Begin implementing base interfaces using the established structure
3. Set up continuous integration workflows
4. Create initial documentation templates

This task establishes the foundation for all subsequent development work and ensures a consistent, maintainable development environment.
