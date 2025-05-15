# BudgetManager

BudgetManager is a simple CLI application for managing your finances.

## Installation

Make sure you have Python ≥ 3.10 installed:

```bash
git clone https://github.com/RealNamison/budgetmanager
cd budgetmanager
pip install .
```

## Usage

Available commands:

### Add Transaction

Adds a new transaction. If no timestamp is provided, the current time will be used.

```bash
budgetmgr add -c groceries -a -25.50 -d "Lunch"
budgetmgr add -t 2025-05-15T12:30:00 -c salary -a 2500.00 -d "Monthly salary"
```

### List Transactions

Lists all stored transactions.

```bash
budgetmgr list
```

### Show Balance

Displays the total balance, income, and expenses.

```bash
budgetmgr balance
```

### Monthly and Yearly Summary

Generates a summary for a specific month or year.

```bash
# May 2025 summary
budgetmgr summary -y 2025 -m 5

# 2025 yearly summary
budgetmgr summary -y 2025

# Export May summary as CSV
budgetmgr summary -y 2025 -m 5 -e csv
```

## Data Directory

By default, data is stored in `data/processed/ledger.json`.

## License

This project is licensed under the MIT License.
