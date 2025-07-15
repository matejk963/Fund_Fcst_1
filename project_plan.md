# Fund_Fcst_1 Refactoring Project Plan

## Project Goals

### Primary Objective
Transform the fund_analysis pipeline to support both:
1. **Integrated Pipeline Usage**: Full forecasting pipeline via FairValueManager (current functionality)
2. **Modular Component Usage**: Independent access to each module's functionality (e.g., residual demand curves, capacity forecasts, scenario generation)

### Secondary Objectives
- Implement clean architecture principles
- Add comprehensive testing framework
- Improve code maintainability and documentation
- Enhance error handling and monitoring
- Optimize performance and resource usage

## Phased Refactoring Approach

### Phase 1: Foundation & Core Infrastructure (Weeks 1-3)

#### Step 1.1: Environment Setup & Project Structure
**Deliverables**:
- Set up dedicated conda environment for the project
- Create proper project structure with clear separation
- Implement proper package management and dependencies

**Tasks**:
1. Create conda environment: `conda create -n fund_fcst_1 python=3.11`
2. Update `.vscode/settings.json` with environment path
3. Create proper `pyproject.toml` or `requirements.txt`
4. Set up development tools (pytest, black, flake8, mypy)

**Code Changes**:
```
fund_analysis/
├── src/
│   └── fund_analysis/
│       ├── core/           # Core interfaces and abstractions
│       ├── data/           # Data layer (input_data refactored)
│       ├── scenarios/      # Scenario generation
│       ├── models/         # ML models
│       ├── analysis/       # Spread calculations
│       └── utils/          # Utilities
├── tests/
├── config/
├── docs/
└── examples/
```

#### Step 1.2: Core Interfaces & Abstractions
**Deliverables**:
- Base interfaces for all major components
- Dependency injection framework
- Configuration management system

**Tasks**:
1. Create `src/fund_analysis/core/interfaces.py`:
   - `IDataLoader`: Abstract base for data loading
   - `IScenarioGenerator`: Abstract base for scenario generation
   - `IModel`: Abstract base for ML models
   - `ISpreadCalculator`: Abstract base for spread calculations

2. Create `src/fund_analysis/core/config.py`:
   - Configuration management with environment variables
   - Market configuration and mappings
   - Database connection management

3. Create `src/fund_analysis/core/di_container.py`:
   - Simple dependency injection container
   - Service registration and resolution

**Example Interface**:
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd
from datetime import datetime

class IDataLoader(ABC):
    @abstractmethod
    def load_data(self, data_type: str, market: str, 
                  start_date: datetime, end_date: datetime,
                  **kwargs) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_available_markets(self, data_type: str) -> List[str]:
        pass
```

#### Step 1.3: Configuration & Environment Management
**Deliverables**:
- Centralized configuration system
- Environment-specific settings
- Secure credential management

**Tasks**:
1. Create `config/` directory structure:
   - `config/base.yaml`: Base configuration
   - `config/dev.yaml`: Development overrides
   - `config/prod.yaml`: Production overrides
2. Implement configuration loading with validation
3. Move all hardcoded values to configuration files

### Phase 2: Data Layer Refactoring (Weeks 4-6)

#### Step 2.1: Data Loader Modernization
**Deliverables**:
- Refactored DataLoader with clear interface
- Individual data type loaders
- Comprehensive error handling

**Tasks**:
1. Create `src/fund_analysis/data/base_loader.py`:
   - Implement `IDataLoader` interface
   - Add retry mechanisms and error handling
   - Implement caching layer

2. Create specific loaders in `src/fund_analysis/data/loaders/`:
   - `database_loader.py`: Database data loading
   - `eikon_loader.py`: Eikon API data loading
   - `file_loader.py`: Local file data loading

3. Create `src/fund_analysis/data/data_manager.py`:
   - Orchestrates different data loaders
   - Handles data validation and quality checks
   - Manages data source priorities and fallbacks

**Example Implementation**:
```python
class DatabaseLoader(IDataLoader):
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def load_data(self, data_type: str, market: str, 
                  start_date: datetime, end_date: datetime,
                  **kwargs) -> pd.DataFrame:
        try:
            schema, table = self._get_schema_table(data_type, market)
            return self._execute_query(schema, table, start_date, end_date)
        except Exception as e:
            logger.error(f"Failed to load {data_type} for {market}: {e}")
            raise DataLoadingError(f"Failed to load {data_type} for {market}")
```

#### Step 2.2: Input Data Modules Refactoring
**Deliverables**:
- Standalone data type handlers
- Independent CLI tools for each data type
- Comprehensive unit tests

**Tasks**:
1. Refactor each input_data module into standalone components:
   - `src/fund_analysis/data/handlers/consumption.py`
   - `src/fund_analysis/data/handlers/capacity.py`
   - `src/fund_analysis/data/handlers/renewables.py`
   - etc.

2. Create CLI tools for each data type:
   - `fund_analysis consumption --market de --start 2024-01-01 --end 2024-12-31`
   - `fund_analysis capacity --market fr --forecast-type normal`

3. Implement comprehensive unit tests for each handler

**Example Handler**:
```python
class ConsumptionHandler:
    def __init__(self, data_loader: IDataLoader):
        self.data_loader = data_loader
    
    def get_consumption_forecast(self, market: str, start_date: datetime, 
                                end_date: datetime, forecast_type: str = 'normal') -> pd.DataFrame:
        """Get consumption forecast for specified market and period"""
        return self.data_loader.load_data('consumption', market, start_date, end_date, 
                                        forecast_type=forecast_type)
    
    def get_historical_consumption(self, market: str, start_date: datetime, 
                                  end_date: datetime) -> pd.DataFrame:
        """Get historical consumption data"""
        return self.data_loader.load_data('consumption_historical', market, start_date, end_date)
```

#### Step 2.3: Data Validation & Quality Framework
**Deliverables**:
- Data validation framework
- Quality checks and monitoring
- Data lineage tracking

**Tasks**:
1. Create `src/fund_analysis/data/validation.py`:
   - Data quality checks (completeness, consistency, accuracy)
   - Outlier detection and handling
   - Data freshness validation

2. Create `src/fund_analysis/data/quality_monitor.py`:
   - Quality metrics tracking
   - Alerting for data issues
   - Quality reports generation

### Phase 3: Scenario Generation Refactoring (Weeks 7-8)

#### Step 3.1: Scenario Framework Modernization
**Deliverables**:
- Modular scenario generation system
- Standalone scenario tools
- Flexible scenario configuration

**Tasks**:
1. Create `src/fund_analysis/scenarios/base.py`:
   - Implement `IScenarioGenerator` interface
   - Common scenario utilities and helpers

2. Refactor existing scenario classes:
   - `HistoricalScenarioGenerator`
   - `CapacityScenarioGenerator`
   - `FuelPriceScenarioGenerator`

3. Create scenario CLI tools:
   - `fund_analysis scenarios historical --data-type consumption --market de --percentiles 10,50,90`
   - `fund_analysis scenarios capacity --market fr --scenario-type outage`

**Example Scenario Generator**:
```python
class HistoricalScenarioGenerator(IScenarioGenerator):
    def __init__(self, data_loader: IDataLoader):
        self.data_loader = data_loader
    
    def generate_scenarios(self, data_type: str, market: str, 
                          start_date: datetime, end_date: datetime,
                          percentiles: List[float] = [0.1, 0.5, 0.9]) -> Dict[str, pd.DataFrame]:
        """Generate historical percentile scenarios"""
        historical_data = self.data_loader.load_data(
            f"{data_type}_historical", market, start_date, end_date
        )
        
        scenarios = {}
        for percentile in percentiles:
            scenarios[f"p{int(percentile*100)}"] = self._calculate_percentile_scenario(
                historical_data, percentile
            )
        
        return scenarios
```

#### Step 3.2: Scenario Combination Framework
**Deliverables**:
- Flexible scenario combination system
- Scenario dependency management
- Scenario validation

**Tasks**:
1. Create `src/fund_analysis/scenarios/combiner.py`:
   - Scenario combination logic
   - Dependency resolution
   - Conflict detection and resolution

2. Create scenario configuration system:
   - YAML-based scenario definitions
   - Scenario templates and presets
   - Validation rules

### Phase 4: Model Layer Refactoring (Weeks 9-10)

#### Step 4.1: Model Framework Modernization
**Deliverables**:
- Standalone model training and prediction
- Model versioning and management
- Performance monitoring

**Tasks**:
1. Create `src/fund_analysis/models/base.py`:
   - Implement `IModel` interface
   - Common model utilities (saving, loading, validation)

2. Refactor XGBoost model:
   - `src/fund_analysis/models/xgboost_model.py`
   - Separate training and prediction logic
   - Add model validation and testing

3. Create model CLI tools:
   - `fund_analysis model train --market de --start 2020-01-01 --end 2024-12-31`
   - `fund_analysis model predict --market de --model-version v1.0 --scenarios scenario_set.json`

**Example Model Implementation**:
```python
class XGBoostModel(IModel):
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = None
        self.is_fitted = False
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series, 
              X_val: pd.DataFrame = None, y_val: pd.Series = None) -> ModelMetrics:
        """Train the model with given data"""
        self.model = XGBRegressor(**self.config.params)
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        
        # Calculate and return metrics
        metrics = self._calculate_metrics(X_val, y_val) if X_val is not None else None
        return metrics
    
    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """Make predictions"""
        if not self.is_fitted:
            raise ModelError("Model must be trained before prediction")
        
        predictions = self.model.predict(X)
        return pd.DataFrame(predictions, index=X.index, columns=['prediction'])
```

#### Step 4.2: Model Performance & Monitoring
**Deliverables**:
- Model performance tracking
- A/B testing framework
- Model drift detection

**Tasks**:
1. Create `src/fund_analysis/models/performance.py`:
   - Performance metrics calculation
   - Model comparison utilities
   - Drift detection algorithms

2. Create `src/fund_analysis/models/monitor.py`:
   - Real-time model monitoring
   - Performance alerting
   - Model health checks

### Phase 5: Analysis Layer Refactoring (Weeks 11-12)

#### Step 5.1: Spread Calculation Modernization
**Deliverables**:
- Standalone spread calculation tools
- Flexible spread configuration
- Comprehensive spread analysis

**Tasks**:
1. Create `src/fund_analysis/analysis/base.py`:
   - Implement `ISpreadCalculator` interface
   - Common spread calculation utilities

2. Refactor spread calculators:
   - `CountrySpreadCalculator`
   - `PeriodSpreadCalculator`
   - `BasepeakSpreadCalculator`
   - `CleanSparkSpreadCalculator`
   - `CapacitySpreadCalculator`

3. Create spread CLI tools:
   - `fund_analysis spreads country --markets de,fr --products M_1,M_2,M_3`
   - `fund_analysis spreads spark --market de --fuel-type gas`

**Example Spread Calculator**:
```python
class CountrySpreadCalculator(ISpreadCalculator):
    def __init__(self, config: SpreadConfig):
        self.config = config
    
    def calculate_spreads(self, data: Dict[str, pd.DataFrame], 
                         markets: List[str], 
                         products: List[str]) -> Dict[str, pd.DataFrame]:
        """Calculate country spreads between markets"""
        spreads = {}
        
        for market_pair in itertools.combinations(markets, 2):
            market1, market2 = market_pair
            spread_key = f"{market1}_{market2}"
            
            spreads[spread_key] = self._calculate_market_spread(
                data[market1], data[market2], products
            )
        
        return spreads
```

#### Step 5.2: Analysis Pipeline Framework
**Deliverables**:
- Flexible analysis pipeline
- Result aggregation and reporting
- Analysis configuration system

**Tasks**:
1. Create `src/fund_analysis/analysis/pipeline.py`:
   - Analysis pipeline orchestration
   - Result aggregation
   - Report generation

2. Create analysis configuration system:
   - YAML-based analysis definitions
   - Analysis templates and presets
   - Custom analysis workflows

### Phase 6: Integration & CLI Development (Weeks 13-14)

#### Step 6.1: Command Line Interface
**Deliverables**:
- Comprehensive CLI for all modules
- Interactive configuration
- Help and documentation system

**Tasks**:
1. Create `src/fund_analysis/cli/main.py`:
   - Main CLI entry point
   - Command routing and parsing
   - Global configuration handling

2. Create module-specific CLI commands:
   - `cli/data_commands.py`: Data loading and management
   - `cli/scenario_commands.py`: Scenario generation
   - `cli/model_commands.py`: Model training and prediction
   - `cli/analysis_commands.py`: Analysis and spread calculations

3. Create interactive configuration tools:
   - `fund_analysis config init`: Initialize configuration
   - `fund_analysis config validate`: Validate configuration
   - `fund_analysis config show`: Display current configuration

**Example CLI Structure**:
```bash
# Data commands
fund_analysis data consumption --market de --start 2024-01-01 --end 2024-12-31 --output consumption_de.csv
fund_analysis data capacity --market fr --forecast-type normal --output capacity_fr.csv

# Scenario commands
fund_analysis scenarios generate --config scenarios.yaml --output scenarios/
fund_analysis scenarios validate --scenario-file scenarios.json

# Model commands
fund_analysis model train --config model_config.yaml --output models/
fund_analysis model predict --model models/xgb_de_v1.0 --data test_data.csv --output predictions.csv

# Analysis commands
fund_analysis analysis spreads --config analysis_config.yaml --data predictions.csv --output spreads/
fund_analysis analysis report --input spreads/ --template report_template.html --output report.html

# Pipeline commands (original functionality)
fund_analysis pipeline run --config pipeline_config.yaml --start 2024-01-01 --end 2024-12-31
```

#### Step 6.2: Integration Testing & Validation
**Deliverables**:
- End-to-end integration tests
- Performance benchmarking
- Validation against existing system

**Tasks**:
1. Create integration test suite:
   - Full pipeline integration tests
   - Module interaction tests
   - Performance regression tests

2. Create validation framework:
   - Compare results with existing system
   - Validate data consistency
   - Performance benchmarking

### Phase 7: Documentation & Examples (Weeks 15-16)

#### Step 7.1: Comprehensive Documentation
**Deliverables**:
- API documentation
- User guides and tutorials
- Developer documentation

**Tasks**:
1. Create API documentation:
   - Auto-generated API docs with Sphinx
   - Code examples for each module
   - Configuration reference

2. Create user documentation:
   - Getting started guide
   - Tutorial for each module
   - Best practices and troubleshooting

3. Create developer documentation:
   - Architecture overview
   - Contributing guidelines
   - Testing guidelines

#### Step 7.2: Examples & Use Cases
**Deliverables**:
- Practical examples for each module
- Jupyter notebooks with tutorials
- Use case demonstrations

**Tasks**:
1. Create example scripts:
   - `examples/data_loading/`: Data loading examples
   - `examples/scenarios/`: Scenario generation examples
   - `examples/modeling/`: Model training examples
   - `examples/analysis/`: Analysis examples

2. Create Jupyter notebooks:
   - "Getting Started with Fund Analysis"
   - "Advanced Scenario Generation"
   - "Custom Model Development"
   - "Spread Analysis Deep Dive"

### Phase 8: Testing & Quality Assurance (Weeks 17-18)

#### Step 8.1: Comprehensive Testing Framework
**Deliverables**:
- Unit test suite (>90% coverage)
- Integration test suite
- Performance test suite

**Tasks**:
1. Create unit tests for all modules:
   - `tests/unit/data/`: Data loading tests
   - `tests/unit/scenarios/`: Scenario generation tests
   - `tests/unit/models/`: Model tests
   - `tests/unit/analysis/`: Analysis tests

2. Create integration tests:
   - `tests/integration/`: End-to-end workflow tests
   - `tests/integration/cli/`: CLI integration tests

3. Create performance tests:
   - `tests/performance/`: Benchmark tests
   - Memory usage tests
   - GPU utilization tests

#### Step 8.2: Quality Assurance & Code Review
**Deliverables**:
- Code quality metrics
- Performance benchmarks
- Security review

**Tasks**:
1. Set up automated quality checks:
   - Code formatting (black, isort)
   - Type checking (mypy)
   - Security scanning (bandit)

2. Performance optimization:
   - Memory usage optimization
   - GPU utilization optimization
   - Caching improvements

3. Final code review and cleanup

## Implementation Guidelines

### Development Principles

1. **Backward Compatibility**: Ensure existing FairValueManager workflow continues to work
2. **Modular Design**: Each module should be independently usable
3. **Configuration-Driven**: Use configuration files for all settings
4. **Error Handling**: Comprehensive error handling and logging
5. **Testing**: Test-driven development with high coverage
6. **Documentation**: Document all public APIs and workflows

### Technology Stack

- **Language**: Python 3.11+
- **ML Framework**: XGBoost with GPU support
- **Database**: TimescaleDB, PostgreSQL
- **Configuration**: YAML, Pydantic for validation
- **CLI**: Click or Typer
- **Testing**: pytest, pytest-cov
- **Documentation**: Sphinx, MkDocs
- **Package Management**: conda, pip

### Quality Standards

- **Code Coverage**: Minimum 90% test coverage
- **Type Hints**: Full type annotation coverage
- **Documentation**: All public APIs documented
- **Performance**: No performance regression vs. current system
- **Security**: Security scan passing
- **Code Quality**: Linting and formatting enforced

## Success Metrics

### Technical Metrics
- Module independence: Each module can be used standalone
- API coverage: 100% of current functionality accessible via CLI/API
- Performance: <5% performance regression
- Test coverage: >90% code coverage
- Documentation: All public APIs documented

### User Experience Metrics
- Ease of use: Reduced setup time for new users
- Flexibility: Ability to run partial workflows
- Reliability: Reduced error rates
- Maintainability: Easier to add new features

## Risk Management

### Technical Risks
- **Performance degradation**: Mitigate with benchmarking and optimization
- **Integration complexity**: Mitigate with comprehensive testing
- **GPU compatibility**: Maintain current GPU acceleration features

### Project Risks
- **Timeline delays**: Phased approach allows for adjustments
- **Resource constraints**: Modular approach allows for priority focusing
- **Scope creep**: Clear definition of success criteria

## Conclusion

This phased approach transforms the fund_analysis system into a modern, modular, and maintainable forecasting pipeline while preserving all existing functionality. Each phase builds upon the previous one, ensuring continuous progress and immediate value delivery.

The end result will be a system that supports both integrated pipeline usage (via FairValueManager) and standalone module usage (via CLI and API), making it more flexible and accessible for different use cases and users.
