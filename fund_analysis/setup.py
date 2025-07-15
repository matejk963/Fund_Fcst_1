from setuptools import setup, find_packages

setup(
    name="fund-analysis",
    version="0.1.0",
    description="Fundamental Forecasting Pipeline for Energy Trading",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "xgboost",
        "sqlalchemy",
        "psycopg2",
        "pydantic",
        "click",
        "pyyaml"
    ],
    python_requires=">=3.11",
)
