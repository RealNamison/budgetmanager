# BudgetManager

**BudgetManager** is a simple command-line application for managing your finances.

## Features

- Add, edit, and delete transactions (income and expenses).
- View current balance, total income, and total expenses.
- Generate monthly and yearly summaries, with optional CSV export.
- Create ASCII charts or export PNG/SVG visualizations of spending per category.
- Flexible storage backend: JSON or SQLite (configurable).

## Prerequisites

- Python 3.10 or higher.
- pip for installation.

## Installation

```bash
git clone https://github.com/RealNamison/budgetmanager.git
cd budgetmanager
pip install .
```

## Usage

After installation, the CLI is available as `budgetmgr`.

### Add a transaction

```bash
budgetmgr add -c groceries -a -25.50 -d "Lunch"
```
Or specify a timestamp:
```bash
budgetmgr add -t 2025-05-15T12:30:00 -c salary -a 2500.00 -d "Monthly salary"
```

### List transactions

```bash
budgetmgr list
```

### Show balance

```bash
budgetmgr balance
```

### Generate summary

Monthly:
```bash
budgetmgr summary -y 2025 -m 5
```
Yearly:
```bash
budgetmgr summary -y 2025
```
Export CSV:
```bash
budgetmgr summary -y 2025 -m 5 -e csv
```

### Charts

Display ASCII chart:
```bash
budgetmgr chart -s 2025-05-01 -e 2025-05-31
```
Export PNG:
```bash
budgetmgr chart -s 2025-05-01 -e 2025-05-31 --png
```

## Configuration

By default, data is stored in `data/processed/ledger.json`.  
To change storage format or location, edit `config.toml`:

```toml
[data]
path   = "data/processed/ledger.json"
format = "json" # or "sqlite"
```

## Tests

Run automated tests with pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License. See `LICENSE` for more information.
