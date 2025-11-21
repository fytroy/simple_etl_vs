# Simple ETL Pipeline

A lightweight, Python-based ETL (Extract, Transform, Load) pipeline designed to read data from CSV files, perform basic transformations (cleaning and type coercion), and load the data into a SQL Server database.

## Project Structure

- `extract.py`: Utilities for reading CSV files into lists of dictionaries.
- `transform.py`: Performs data cleaning (stripping whitespace) and type coercion (inferring integers and floats).
- `load.py`: Handles SQL Server table creation and bulk insertion using `pyodbc`.
- `config.py`: Helper functions for building database connection strings, with support for environment variables.
- `simple_etl`: The package name (if installed as a package).

## Prerequisites

- Python 3.x
- `pyodbc` driver and SQL Server ODBC driver
- `pytest` (for running tests)

## Setup

1. **Install Dependencies:**
   Ensure you have the necessary Python packages installed. You may need to install `pyodbc`.
   ```bash
   pip install pyodbc
   ```
   *(Note: You will also need the system-level ODBC Driver for SQL Server installed on your machine).*

2. **Environment Variables:**
   The pipeline uses environment variables to configure the database connection. You can set the following variables:
   - `SQLSERVER_HOST` (default: `localhost`)
   - `SQLSERVER_DB` (default: `master`)
   - `SQLSERVER_UID`
   - `SQLSERVER_PWD`
   - `SQLSERVER_DRIVER` (default: `ODBC Driver 18 for SQL Server`)

## Usage

You can use the individual modules to build your ETL workflow. Example usage:

```python
import extract
import transform
import load
import config

# 1. Extract
rows = extract.extract_csv("data.csv")

# 2. Transform
cleaned_rows = transform.transform_rows(rows)

# 3. Load
conn_str = config.build_conn_str(database="TargetDB")
load.load_to_sqlserver(cleaned_rows, "TargetTable", conn_str)
```

## Testing

The project includes a comprehensive test suite using `pytest`.

To run the tests, run the following command from the project root:

```bash
PYTHONPATH=. pytest
```

This will run all unit and integration tests, ensuring that extraction, transformation, loading logic (mocked), and configuration work as expected.
