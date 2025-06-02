# BudgetManager

**BudgetManager** is a simple, command-line application written in Python 3.10 that helps you manage your personal finances. It allows you to track income and expenses, define budgets per category, generate summary reports, and produce ASCII or graphical charts of your spending and income.

---

## Table of Contents

1. [Features](#features)  
2. [Project Structure](#project-structure)  
3. [Installation](#installation)  
4. [Configuration](#configuration)  
5. [Usage](#usage)  
   - [Command-Line Interface](#command-line-interface)  
   - [Examples](#examples)  
6. [Core Modules](#core-modules)  
   - [CLI](#cli)  
   - [Transaction](#transaction)  
   - [Ledger](#ledger)  
   - [Budget](#budget)  
   - [ReportGenerator](#reportgenerator)  
   - [Chart Generation](#chart-generation)  
7. [File and Data Handling](#file-and-data-handling)  
   - [SQLiteHandler](#sqlitehandler)  
   - [FileHandler](#filehandler)  
   - [JSONHandler (Deprecated)](#jsonhandler-deprecated)  
8. [Utilities](#utilities)  
   - [Timestamp](#timestamp)  
9. [Data Storage](#data-storage)  
10. [Testing](#testing)  
11. [Development Guidelines](#development-guidelines)  
12. [Contributing](#contributing)  
13. [License](#license)  

---

## Features

- **Add Transactions**: Record income or expense transactions with timestamp, category, amount, and description.  
- **List and Remove Transactions**: View recent transactions, reverse order, limit count, and delete transactions by ID.  
- **Budgets**: Define spending limits per category; receive warnings when overspending.  
- **Summaries**: Generate monthly, yearly, or custom-range summaries of income, expenses, and balance.  
- **Charts**: Display ASCII bar charts for income/expenses by category in a given period; optionally export PNG or SVG charts.  
- **Persistent Storage**: All data is saved in an SQLite database by default.  
- **Configurable Data Root**: Override the default data directory using an environment variable.  
- **Modular Design**: Separate modules for core logic, file handling, CLI, and utilities.

---

## Project Structure

Below is a high-level overview of the repository layout (root directory: `budgetmanager/`):

```
budgetmanager/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── processed/
│   │   ├── charts/
│   │   │   └── chart_<start>_to_<end>.<png|svg>
│   │   ├── budget.db
│   │   ├── budgets.json
│   │   ├── ledger.json
│   │   └── summary_<label>.csv
│   └── raw/
├── docs/
│   ├── index.md
│   ├── project_structure.txt
│   ├── reports.md
│   └── usage.md
├── examples/
│   ├── quickstart.ipynb
│   └── advanced_usage.py
├── src/
│   └── budgetmanager/
│       ├── cli/
│       │   ├── __init__.py
│       │   └── cli.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── budget.py
│       │   ├── chart.py
│       │   ├── ledger.py
│       │   ├── report.py
│       │   └── transaction.py
│       ├── file/
│       │   ├── __init__.py
│       │   ├── file_handler.py
│       │   ├── json_handler.py
│       │   └── sqlite_handler.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── timestamp.py
│       ├── __init__.py
│       └── config.py
├── tests/
│   ├── integration/
│   │   ├── test_cli_integration.py
│   │   ├── test_file_json_integration.py
│   │   ├── test_ledger_report_integration.py
│   │   └── test_transaction_ledger_integration.py
│   ├── unit/
│   │   ├── test_chart.py
│   │   ├── test_file_handler.py
│   │   ├── test_json_handler.py
│   │   ├── test_ledger.py
│   │   ├── test_report.py
│   │   ├── test_sqlite_handler.py
│   │   ├── test_timestamp.py
│   │   └── test_transaction.py
│   └── conftest.py
├── .flake8
├── .gitignore
├── LICENSE
├── mkdocs.yml
├── pyproject.toml
├── README.md
└── tox.ini
```

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/RealNamison/budgetmanager.git
   cd budgetmanager
   ```

2. **Ensure Python 3.10+ is Installed**  
   BudgetManager relies on Python 3.10 or newer due to use of modern type hint syntax.

3. **Create a Virtual Environment (Optional but Recommended)**  
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**  
   ```bash
   pip install --upgrade pip
   pip install .
   ```

   - This will install `budgetmanager` and its dependency `matplotlib`.

5. **Verify Installation**  
   ```bash
   budgetmgr --help
   ```
   You should see usage information for the `budgetmgr` CLI.

---

## Configuration

By default, BudgetManager stores data under the `data/` directory in the project root. You can override this location by setting the environment variable `BUDGETMANAGER_DATA_ROOT` to any absolute path:

```bash
export BUDGETMANAGER_DATA_ROOT="/path/to/custom/data"
```

The environment variable is read in `src/budgetmanager/config.py`, which sets:

```python
PROJECT_ROOT = Path.cwd()
DATA_ROOT = Path(os.getenv("BUDGETMANAGER_DATA_ROOT")) if set else PROJECT_ROOT / "data"
DB_FILE = DATA_ROOT / "processed" / "budget.db"
```

---

## Usage

BudgetManager is invoked through the command `budgetmgr`. The CLI supports the following commands:

### Command-Line Interface

- **Add a Transaction**  
  ```bash
  budgetmgr add -c CATEGORY -a AMOUNT [-t TIMESTAMP] [-d DESCRIPTION]
  ```
  - `-c, --category`: Category or tag for the transaction (e.g., `food`, `salary`).  
  - `-a, --amount`: Amount as a decimal string (positive for income, negative for expense).  
  - `-t, --timestamp`: (Optional) ISO 8601 timestamp, e.g., `2025-06-01T14:30:00`. Defaults to current time.  
  - `-d, --description`: (Optional) Short description.

- **List Transactions**  
  ```bash
  budgetmgr list [-n LIMIT] [-r]
  ```
  - `-n, --limit`: (Optional) Show only the last `N` transactions.  
  - `-r, --reverse`: (Optional) Reverse the order of transactions (oldest first).  

- **Show Balance**  
  ```bash
  budgetmgr balance
  ```
  Displays total balance, total income, and total expenses.

- **Remove a Transaction**  
  ```bash
  budgetmgr remove -i TRANSACTION_ID
  ```
  Deletes the transaction with the given ID from the database and ledger.

- **Summary**  
  Generate income/expense/ balance summaries by year, month, or custom range.
  ```bash
  # Yearly summary
  budgetmgr summary --year 2025 [--month 5] [--export csv]

  # Custom range summary
  budgetmgr summary --range 2025-05-01T00:00:00 2025-05-31T23:59:59 [--export csv]
  ```
  - `--year, -y`: Four-digit year (e.g., `2025`).  
  - `--month, -m`: Month number (1–12), valid only if `--year` is provided.  
  - `--range START END`: ISO timestamps for start and end (inclusive).  
  - `--export csv`: (Optional) Export summary to CSV under `data/processed/summary_<label>.csv`.

- **Manage Budgets**  
  ```bash
  # Add a new budget for a category
  budgetmgr budget add -c CATEGORY -l LIMIT

  # List all budgets
  budgetmgr budget list

  # Remove a budget by category
  budgetmgr budget remove -c CATEGORY
  ```
  If spending in a category exceeds the defined limit in the current month, a warning is printed when adding a new transaction.

- **Generate Charts**  
  ```bash
  budgetmgr chart --start YYYY-MM-DD --end YYYY-MM-DD [--png | --svg]
  ```
  - Displays ASCII bar charts for income and expenses per category between the given dates (inclusive).  
  - If `--png` or `--svg` is specified, saves a graphical bar chart under `data/processed/charts/chart_<start>_to_<end>.<png|svg>`.

---

## Examples

1. **Quickstart Example**  
   ```bash
   # Add salary income
   budgetmgr add -c salary -a 5000.00 -d "June salary"

   # Add an expense
   budgetmgr add -c groceries -a -150.25 -d "Weekly groceries"

   # Show all transactions (most recent first)
   budgetmgr list

   # Show summary for June 2025
   budgetmgr summary --year 2025 --month 6

   # Define a budget for groceries: $600 per month
   budgetmgr budget add -c groceries -l 600.00

   # Add more grocery expenses and trigger a budget warning
   budgetmgr add -c groceries -a -500.00 -d "Furniture"
   budgetmgr add -c groceries -a -200.00 -d "More groceries"  # Warning: budget exceeded

   # Generate ASCII chart for June 2025
   budgetmgr chart --start 2025-06-01 --end 2025-06-30

   # Generate and save a PNG chart for May 2025
   budgetmgr chart --start 2025-05-01 --end 2025-05-31 --png
   ```

2. **Quickstart Notebook**  
   The `examples/quickstart.ipynb` provides a step-by-step guided demonstration. You can open it using Jupyter Notebook:

   ```bash
   jupyter notebook examples/quickstart.ipynb
   ```

---

## Core Modules

### CLI

- **Location**: `src/budgetmanager/cli/cli.py`  
- **Description**: Parses command-line arguments using `argparse`, delegates to core logic, handles input validation, and prints results or errors. Implements subcommands: `add`, `list`, `balance`, `remove`, `summary`, `budget`, `chart`.

### Transaction

- **Location**: `src/budgetmanager/core/transaction.py`  
- **Description**: Defines the `Transaction` class representing a single financial transaction. Includes methods for serialization (`to_dict`/`from_dict`), arithmetic operator overloads (add, subtract, multiply, divide), and categorization (`is_income`, `is_expense`).

### Ledger

- **Location**: `src/budgetmanager/core/ledger.py`  
- **Description**: Defines the `Ledger` class to manage a collection of `Transaction` objects. Supports adding, removing, filtering by category or date range, computing total balance, income, and expenses, and implements sequence protocol methods (`__len__`, `__iter__`, `__getitem__`, etc.). Can serialize/deserialize to/from a dictionary.

### Budget

- **Location**: `src/budgetmanager/core/budget.py`  
- **Description**: Defines the `Budget` class for representing spending limits per category. Includes serialization methods (`to_dict`/`from_dict`) and comparison (`__eq__`).

### ReportGenerator

- **Location**: `src/budgetmanager/core/report.py`  
- **Description**: Implements static methods to compute monthly, yearly, or custom-range summaries of income, expenses, and balance. Also includes `export_to_csv` for writing summary data to CSV.

### Chart Generation

- **Location**: `src/budgetmanager/core/chart.py`  
- **Description**: Implements ASCII bar chart printing (`_print_ascii_chart`) and optional graphical chart export using `matplotlib` (`_export_graphical_chart`). Accepts a `Ledger`, start/end `Timestamp`s, and desired export format (`png` or `svg`).

---

## File and Data Handling

### SQLiteHandler

- **Location**: `src/budgetmanager/file/sqlite_handler.py`  
- **Description**: Manages SQLite database for persisting transactions and budgets.  
- **Key Methods**:  
  - `add_transaction(tx: Transaction)`: Inserts a transaction into `transactions` table.  
  - `get_all_transactions() -> list[Transaction]`: Retrieves all transactions.  
  - `remove_transaction(tx_id: int) -> Transaction | None`: Deletes a transaction by ID and returns the removed record.  
  - `add_budget(budget: Budget)`: Inserts or updates a budget in `budgets` table.  
  - `get_budgets() -> list[Budget]`: Retrieves all stored budgets.  
  - `remove_budget(category: str)`: Deletes a budget by category.

### FileHandler

- **Location**: `src/budgetmanager/file/file_handler.py`  
- **Description**: Provides utilities to create directories and files under `DATA_ROOT`. Ensures paths are correctly joined to the configured data directory.  
- **Key Methods**:  
  - `create_directory(path: str) -> Path`: Creates a directory (absolute or relative to `DATA_ROOT`).  
  - `create_file(directory_path: str, file_name: str, file_type: str) -> Path`: Creates an empty file under a specified folder.  
  - `get_directory_path(*paths: str) -> Path`: Constructs directory paths.  
  - `get_file_path(*paths: str) -> Path`: Constructs file paths.

### JSONHandler (Deprecated)

- **Location**: `src/budgetmanager/file/json_handler.py`  
- **Description**: Handles loading and saving JSON data under `DATA_ROOT`. Marked as deprecated; use SQLite instead.  
- **Key Methods**:  
  - `load_json(*paths: str) -> Any`: Loads JSON data from a file.  
  - `save_json(data: Any, *paths: str) -> Path`: Saves Python objects as JSON.

---

## Utilities

### Timestamp

- **Location**: `src/budgetmanager/utils/timestamp.py`  
- **Description**: Defines the `Timestamp` class that encapsulates date and time components separately. Supports creation from components, current local time, `datetime` objects, and ISO-formatted strings. Implements comparison operators and conversion to `datetime` or ISO format string.

---

## Data Storage

By default, BudgetManager stores data in an SQLite database file located at:

```
<data_root>/processed/budget.db
```

where `<data_root>` is either:

- The `data/` folder inside the project root, or  
- A custom directory specified by the environment variable `BUDGETMANAGER_DATA_ROOT`.

Additionally, generated charts (PNG/SVG) are saved under:

```
<data_root>/processed/charts/
```

Summary CSVs are stored under:

```
<data_root>/processed/summary_<label>.csv
```

---

## Testing

BudgetManager includes both unit and integration tests using **pytest**. The test files are located under the `tests/` directory:

- **Unit Tests**:  
  - `tests/unit/test_timestamp.py`  
  - `tests/unit/test_transaction.py`  
  - `tests/unit/test_ledger.py`  
  - `tests/unit/test_budget.py`  
  - `tests/unit/test_report.py`  
  - `tests/unit/test_chart.py`  
  - `tests/unit/test_file_handler.py`  
  - `tests/unit/test_json_handler.py`  
  - `tests/unit/test_sqlite_handler.py`

- **Integration Tests**:  
  - `tests/integration/test_cli_integration.py`  
  - `tests/integration/test_file_json_integration.py`  
  - `tests/integration/test_ledger_report_integration.py`  
  - `tests/integration/test_transaction_ledger_integration.py`

To run all tests:

```bash
pytest --cov=budgetmanager
```

Ensure that `src/` is in the `PYTHONPATH` (configured by `tests/conftest.py`). The `pyproject.toml` includes pytest configuration.

---

## Development Guidelines

- **Python Version**: Minimum 3.10 required.  
- **Coding Style**:  
  - Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with a maximum line length of 79 characters.  
  - Use type hints according to PEP 484, preferring the pipe (`|`) syntax for `Optional` or `Union`.  
  - Document functions, classes, and methods using Google-style docstrings.  
  - Use specific exceptions; avoid catching `Exception` generically.  
- **Formatting and Linting**:  
  - **Black** is configured with `line-length = 79`.  
  - **Flake8** rules are in `.flake8`.  
  - **Mypy** settings enforce strict typing.  
- **Project Structure**:  
  - All source code resides under `src/budgetmanager/`.  
  - Tests are separated into `tests/unit/` and `tests/integration/`.  
  - CI configuration is defined in `.github/workflows/ci.yml`.  
- **Documentation**:  
  - Additional usage examples and guides are available under the `docs/` folder (e.g., `docs/usage.md`, `docs/reports.md`).  
  - Project structure documentation is in `docs/project_structure.txt`.

---

## Contributing

Contributions are welcome! If you would like to contribute:

1. Fork the repository on GitHub.  
2. Create a new branch (`git checkout -b feature/YourFeature`).  
3. Make your changes and ensure all tests pass.  
4. Follow code style guidelines (run `black`, `flake8`, and `mypy`).  
5. Submit a pull request describing your changes.

Please adhere to the existing coding conventions, write tests for new features, and update documentation as needed.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

