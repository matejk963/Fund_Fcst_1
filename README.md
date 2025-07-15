# Fund_Fcst_1 - Fundamental Forecasting Pipeline

## Project Overview

The Fund_Fcst_1 project is a comprehensive fundamental forecasting pipeline for energy trading markets, specifically designed for power price prediction using machine learning models. The system integrates various data sources, applies scenario analysis, and generates forecasts for multiple European energy markets.

## Core Purpose

This pipeline serves as a sophisticated forecasting system that:
- Aggregates fundamental energy market data from multiple sources
- Applies machine learning models (primarily XGBoost) for price forecasting
- Generates scenario-based predictions for risk management
- Produces various spread calculations for trading strategies
- Supports multiple European energy markets (DE, FR, BE, NL, AT, HU, CZ, SK, RO)

## High-Level Architecture

The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │────│  Data Loading   │────│  Fair Value     │
│   (DB, Eikon,   │    │   & Assembly    │    │   Manager       │
│   Local Files)  │    │                 │    │  (Orchestrator) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Scenario      │────│    Models       │
                       │   Generation    │    │  (XGBoost GPU)  │
                       └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Spread        │────│   Forecasts     │
                       │  Calculations   │    │   & Results     │
                       └─────────────────┘    └─────────────────┘
```

## Project Structure Map

### 🏗️ **Core Components**

#### 1. **Fair Value Manager** (`fair_value_manager.py`)
- **Role**: Main orchestrator and control center
- **Responsibilities**: 
  - Coordinates data flow between all components
  - Manages scenario generation and combination
  - Controls model training and prediction workflow
  - Handles spread calculations and result aggregation
- **Key Methods**: `get_fcst_curves()`, `call_for_base_data()`, `combine_scenarios()`

#### 2. **Data Loader** (`data_loader.py`)
- **Role**: Data acquisition and preprocessing
- **Responsibilities**:
  - Fetches data from multiple sources (Database, Eikon, local files)
  - Handles different data types and formats
  - Manages date range queries and data alignment
- **Data Sources**: TimescaleDB, Eikon API, local CSV files

#### 3. **Models** (`models/`)
- **Role**: Machine learning prediction engine
- **Technologies**: XGBoost with GPU acceleration
- **Features**:
  - Parallel processing for multiple scenarios
  - GPU temperature monitoring
  - Market-specific parameter optimization
  - Automated model saving and loading

### 📊 **Data Input Modules** (`input_data/`)

The system handles multiple fundamental data types:

| Module | Data Type | Source | Purpose |
|--------|-----------|--------|---------|
| `available_capacity.py` | Power plant capacity | Database | Supply-side fundamentals |
| `consumption.py` | Energy consumption | Database/Local | Demand-side fundamentals |
| `residual_demand.py` | Net demand | Calculated | Core price driver |
| `wind.py`, `solar.py` | Renewable generation | Database | Variable supply |
| `hydro.py` | Hydro generation | Database | Flexible supply |
| `gas.py`, `coal.py`, `eua.py` | Fuel prices | Eikon/Database | Cost fundamentals |
| `temp.py` | Temperature | Database | Seasonal demand driver |
| `power.py` | Power prices | Database | Target variable |

### 🎯 **Scenario Generation** (`scenarios/`)

#### Types of Scenarios:
1. **Historical Scenarios** (`external_fund_scenarios.py`)
   - Based on historical data distributions
   - Percentile-based scenario generation (10th, 20th, ..., 90th)
   - Applied to consumption, renewables, and demand patterns

2. **Capacity Scenarios** (`av_cap_scenarios.py`)
   - Available capacity variations
   - Outage scenarios and maintenance patterns
   - Statistical distributions of plant availability

3. **Fuel Price Scenarios** (`fuel_scenarios.py`)
   - Gas, coal, and carbon price variations
   - Stress testing with defined percentage changes
   - Market correlation scenarios

### 🔧 **Utility Modules** (`utils/`)

- **ENUMS.py**: Configuration constants and mappings
- **model_data_assembly.py**: Data preparation and scaling
- **spreads_creation.py**: Spread calculation utilities
- **dict_to_parquet.py**: Data serialization helpers

### 📈 **Spread Calculations**

The system generates comprehensive spread analysis:

1. **Country Spreads**: Price differences between markets
2. **Period Spreads**: Calendar spread calculations
3. **Base-Peak Spreads**: Load profile arbitrage opportunities
4. **Clean Spark Spreads**: Gas-to-power conversion margins
5. **Capacity Spreads**: Transmission capacity arbitrage

### 🔄 **Data Updates** (`updates/`)

Automated data maintenance:
- `update_coal_prices.py`: Coal price updates
- `update_eua_prices.py`: Carbon price updates
- `update_ttf_prices.py`: Gas price updates
- `fund_model_update.py`: Model retraining workflows

## Technical Features

### 🚀 **Performance Optimizations**
- **GPU Acceleration**: XGBoost with CUDA support
- **Parallel Processing**: Multi-threaded scenario processing
- **Memory Management**: Efficient data structures and caching
- **Temperature Monitoring**: GPU thermal management

### 🛡️ **Robustness Features**
- **Error Handling**: Comprehensive exception management
- **Data Validation**: Input data quality checks
- **Fallback Mechanisms**: Alternative data sources
- **Logging**: Detailed execution tracking

### 📦 **Data Management**
- **Multiple Formats**: Parquet, Pickle, CSV support
- **Database Integration**: TimescaleDB for time series
- **Caching**: Intermediate result storage
- **Versioning**: Model and data versioning

## Supported Markets

The system covers major European power markets:
- **DE** (Germany) - Primary market
- **FR** (France) - Major neighbor
- **BE** (Belgium) - Coupling market
- **NL** (Netherlands) - Gas hub integration
- **AT** (Austria) - Alpine region
- **HU** (Hungary) - Eastern Europe
- **CZ** (Czech Republic) - Central Europe
- **SK** (Slovakia) - Regional integration
- **RO** (Romania) - Emerging market

## Key Workflows

### 1. **Forecast Generation Pipeline**
```
Data Loading → Scenario Generation → Model Training → Prediction → Spread Calculation → Result Storage
```

### 2. **Data Update Cycle**
```
Source Monitoring → Data Extraction → Validation → Database Update → Model Retraining
```

### 3. **Scenario Analysis**
```
Base Data → Historical Analysis → Stress Testing → Combination Generation → Risk Assessment
```

## Configuration Management

The system uses comprehensive configuration through:
- **ENUMS.py**: Market mappings and constants
- **Parameter Files**: Model hyperparameters
- **Config Files**: Database connections and paths
- **Setup Files**: Package installation and dependencies

## Current Status & Opportunities

### ✅ **Strengths**
- Comprehensive data integration
- Advanced ML modeling with GPU acceleration
- Extensive scenario analysis capabilities
- Multi-market support
- Automated spread calculations

### 🔧 **Areas for Enhancement**
- **Code Structure**: Modularization and clean architecture
- **Testing**: Unit tests and integration tests
- **Documentation**: API documentation and user guides
- **Error Handling**: More robust error management
- **Performance**: Further optimization opportunities
- **Monitoring**: Real-time performance tracking

## Next Steps for Refactoring

1. **Architecture Modernization**
   - Implement clean architecture principles
   - Add dependency injection
   - Create clear interfaces and abstractions

2. **Testing Framework**
   - Implement comprehensive unit testing
   - Add integration tests
   - Create test data management

3. **Documentation**
   - API documentation
   - User guides and tutorials
   - Code examples and best practices

4. **Performance Optimization**
   - Profiling and benchmarking
   - Memory usage optimization
   - Caching strategies

5. **Monitoring & Logging**
   - Structured logging
   - Performance metrics
   - Error tracking and alerting

This analysis provides the foundation for systematic refactoring and enhancement of the fund_analysis system into a more maintainable, scalable, and robust forecasting pipeline.
