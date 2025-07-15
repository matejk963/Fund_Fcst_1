# Fund Analysis

Main project documentation for the Fund Analysis pipeline. See docs/ for API, user, and developer guides.

## Environment Setup & Validation

To set up and validate your development environment:

1. Ensure you have Conda installed.
2. Create and activate the dedicated environment:
   ```powershell
   conda deactivate; conda env remove -n fund_fcst_1
   conda create -n fund_fcst_1 python=3.11
   conda activate fund_fcst_1
   ```
3. Install dependencies:
   ```powershell
   pip install -r EnergyTrading/Python/Utilities/fund_analysis/requirements.txt
   ```
4. Export the environment for reproducibility:
   ```powershell
   conda env export -n fund_fcst_1 > environment.yml
   ```
5. Validate the environment:
   ```powershell
   python scripts/validate_installation.py
   ```
   This script checks that the correct conda environment is active and all required dependencies are installed. It does not check for any package import.

## Project Structure

See the project plan and docs/ for details on the modular structure and migration strategy.
