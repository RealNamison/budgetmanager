# BudgetManager Documentation

Welcome to the official documentation for **BudgetManager**.

## Quick Start

Install the package:

```bash
pip install .
```

Display the CLI help:

```bash
budgetmgr --help
```

## CLI Commands

### Add Transaction

```bash
budgetmgr add -c groceries -a -25.50 -d "Lunch"
```

Options:

* `-t`, `--timestamp`: ISO timestamp (optional, default: now)
* `-c`, `--category`: Transaction category (e.g. `groceries`, `rent`)
* `-a`, `--amount`: Amount (positive = income, negative = expense)
* `-d`, `--description`: Description (optional)

### List Transactions

```bash
budgetmgr list
```

### Show Balance

```bash
budgetmgr balance
```

### Generate Summary

```bash
budgetmgr summary -y 2025 -m 5
```

Parameters:

* `-y`, `--year`: Year (e.g. `2025`)
* `-m`, `--month`: Month (1–12; omit for yearly summary)
* `-e`, `--export`: optional `csv`

The generated CSV file is saved to `data/processed/summary_<year>-<month>.csv`.
