# Usage Guide

This document provides detailed information on how to use the **BudgetManager** 
command-line interface.

## General Command Structure

```bash
budgetmgr [command] [options]
```

Use `budgetmgr [command] --help` to view command-specific options.

## Commands

### add

Add a new transaction (income or expense).

**Usage**

```bash
budgetmgr add -c CATEGORY -a AMOUNT -d DESCRIPTION [-t TIMESTAMP]
```

**Options**

- `-c, --category CATEGORY`  
  Category of the transaction (e.g., groceries, salary).

- `-a, --amount AMOUNT`  
  Amount of the transaction (negative for expenses, positive for income).

- `-d, --description DESCRIPTION`  
  Short description or note.

- `-t, --timestamp TIMESTAMP`  
  Optional ISO 8601 timestamp (e.g., 2025-05-15T12:30:00). Defaults to now.

**Examples**

Add an expense:

```bash
budgetmgr add -c groceries -a -25.50 -d "Lunch at café"
```

Add income with timestamp:

```bash
budgetmgr add -t 2025-05-15T12:30:00 -c salary -a 2500.00 -d "Monthly salary"
```

### list

List recorded transactions.

**Usage**

```bash
budgetmgr list [--limit N] [--reverse]
```

**Options**

- `--limit N`  
  Show only the last N transactions.

- `--reverse`  
  Show oldest transactions first.

### balance

Show current balance summary.

**Usage**

```bash
budgetmgr balance
```

### summary

Generate a summary report.

**Usage**

```bash
budgetmgr summary -y YEAR [-m MONTH] [-e {table,csv}]
```

### chart

Visualize spending by category as ASCII or export image.

**Usage**

```bash
budgetmgr chart -s START_DATE -e END_DATE [--png] [--svg]
```
