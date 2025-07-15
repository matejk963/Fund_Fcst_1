# Task 1.2: Core Interfaces & Abstractions

## Objective
Implement the foundational interfaces, dependency injection, and configuration management for the modular fund_analysis pipeline, as described in Step 1.2 of the project plan.

## Deliverables
- Base interfaces for all major components
- Dependency injection framework
- Configuration management system

## Implementation Steps

### 1. Create Core Interfaces
- **Location:** `fund_analysis/src/fund_analysis/core/interfaces.py`
- **Interfaces to implement:**
  - `IDataLoader`: Abstract base for data loading
  - `IScenarioGenerator`: Abstract base for scenario generation
  - `IModel`: Abstract base for ML models
  - `ISpreadCalculator`: Abstract base for spread calculations
- **Requirements:**
  - Use Python's `abc` module for abstract base classes
  - Include type hints and docstrings
  - Reference example interface from project plan

### 2. Implement Configuration Management
- **Location:** `fund_analysis/src/fund_analysis/core/config.py`
- **Features:**
  - Centralized configuration loading (YAML-based)
  - Support for environment variables and overrides
  - Market configuration and mappings
  - Database connection management (use the `Database` class from EnergyTrading as the connection interface, as implemented in `EnergyTrading/Python/Utilities/tech_analysis/data_loader.py`)
  - Configuration must support:
    - Market mappings and constants (from `ENUMS.py`)
    - Parameter files for model hyperparameters
    - Config files for database connections and paths
    - Setup files for package installation and dependencies
    - Data source selection (DB, Eikon, local files)
    - Paths for data storage and retrieval
    - Market-specific overrides and flexible data source management
    - Robust error handling and support for multiple European markets
**Requirements:**
  - Use Pydantic for validation (as per tech stack)
  - Move hardcoded values to config files in `fund_analysis/config/`
  - For database access, integrate with the existing `Database` class from EnergyTrading, following the pattern in `data_loader.py` for establishing connections and querying data.
  - Ensure configuration is centralized, YAML-based, and loads all relevant settings, integrating with `ENUMS.py` and supporting environment/market overrides.

### 3. Create Dependency Injection Container
- **Location:** `fund_analysis/src/fund_analysis/core/di_container.py`
- **Features:**
  - Simple DI container for service registration and resolution
  - Support for constructor injection
  - Document usage with examples

## Acceptance Criteria
- All interfaces are defined and documented
- Configuration system loads and validates settings from YAML files
- DI container enables modular service registration and retrieval
- All code follows PEP 8 and project coding standards
- Unit tests for config and DI container (to be added in later tasks)

## Notes
- Reference the example code snippets in the project plan for interface and class structure
- Ensure all new files are placed in the correct subdirectories (do not use root)
- Document all public APIs and usage patterns

## Next Steps
After completion, proceed to Step 1.3: Configuration & Environment Management.
