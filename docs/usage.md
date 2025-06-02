# Usage Guide

This **Usage Guide** provides detailed instructions on how to interact with BudgetManager via the command-line interface (CLI). It covers installation steps, configuration options, command syntax, and practical examples to help you get started quickly.

---

## Installation Recap

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/RealNamison/budgetmanager.git
   cd budgetmanager
   ```

2. **Create Virtual Environment (Optional but Recommended)**  
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. **Install Package and Dependencies**  
   ```bash
   pip install --upgrade pip
   pip install .
   ```

4. **Verify Installation**  
   ```bash
   budgetmgr --help
   ```

---

## Configuration

By default, BudgetManager stores data in:

```
<data_root>/processed/budget.db
```

where `<data_root>` is:

- The `data/` folder in the project root, or
- A custom directory set via the environment variable:

  ```bash
  export BUDGETMANAGER_DATA_ROOT="/custom/path/to/data"
  ```

---

## CLI Command Syntax

All commands are invoked using the main executable `budgetmgr`. Use `--help` after any command or subcommand to view available options.

```bash
budgetmgr [GLOBAL_OPTIONS] <COMMAND> [OPTIONS]
```

- **Global Options**  
  - `-h, --help`: Show help message and exit.
  - `--version`: Display the current version of BudgetManager.

### Primary Commands

1. **add**: Add a new transaction.  
2. **list**: List existing transactions.  
3. **balance**: Show overall balance, income, and expenses.  
4. **remove**: Remove a transaction by ID.  
5. **summary**: Generate a report summary of transactions.  
6. **budget**: Manage budgets (add, list, remove).  
7. **chart**: Generate ASCII or graphical charts for specified date range.

---

## Detailed Command Examples

### 1. Add Transaction

Add income or expense to the ledger.

```bash
budgetmgr add -c CATEGORY -a AMOUNT [-t TIMESTAMP] [-d DESCRIPTION]
```

- `-c, --category` (string, required): Category name (e.g., `salary`, `groceries`).
- `-a, --amount` (decimal, required): Positive for income, negative for expense (e.g., `500.00` or `-150.25`).
- `-t, --timestamp` (ISO 8601 string, optional): Timestamp of transaction (defaults to current time). Example: `2025-06-02T09:30:00`.
- `-d, --description` (string, optional): Short description or note.

**Example**:  
```bash
# Add a salary payment of $4000 with description
budgetmgr add -c salary -a 4000.00 -d "June salary"

# Add a grocery expense with explicit timestamp
budgetmgr add -c groceries -a -75.50 -t 2025-06-01T18:45:00 -d "Weekly shopping"
```

### 2. List Transactions

List transactions in the database, optionally limiting or reversing order.

```bash
budgetmgr list [-n LIMIT] [-r]
```

- `-n, --limit` (integer, optional): Show only the last N transactions (default: all).
- `-r, --reverse` (flag, optional): Reverse the order (oldest first instead of newest).

**Example**:  
```bash
# List all transactions (newest first)
budgetmgr list

# List 10 most recent transactions
budgetmgr list -n 10

# List all transactions (oldest first)
budgetmgr list -r
```

### 3. Show Balance

Display aggregate totals: total income, total expenses, and net balance.

```bash
budgetmgr balance
```

**Example**:  
```bash
budgetmgr balance
# Output:
# Total Income   : 5000.00
# Total Expenses : 1500.25
# Net Balance    : 3499.75
```

### 4. Remove Transaction

Delete a transaction by specifying its unique ID.

```bash
budgetmgr remove -i TRANSACTION_ID
```

- `-i, --id` (integer, required): The ID of the transaction to remove.

**Example**:  
```bash
# Remove transaction with ID 7
budgetmgr remove -i 7
```

### 5. Generate Summary (Reports)

Create a summary report of transactions for a specific period.

```bash
budgetmgr summary [--year YEAR] [--month MONTH] [--range START END] [--export csv]
```

- `--year YEAR` (integer): Four-digit year (e.g., `2025`).
- `--month MONTH` (integer): Month number (1–12), requires `--year`.
- `--range START END`: Two ISO 8601 timestamps (inclusive). Example: `2025-06-01T00:00:00 2025-06-30T23:59:59`.
- `--export csv`: Flag to export CSV file. Saved as `data/processed/summary_<label>.csv`.

**Examples**:  
```bash
# Yearly summary for 2025
budgetmgr summary --year 2025

# Monthly summary for June 2025
budgetmgr summary --year 2025 --month 6

# Custom range summary (first half of June 2025)
budgetmgr summary --range 2025-06-01T00:00:00 2025-06-15T23:59:59

# Export monthly summary to CSV
budgetmgr summary --year 2025 --month 6 --export csv
# Output file: data/processed/summary_2025-06.csv
```

### 6. Manage Budgets

Define or remove spending limits by category.

```bash
# Add a budget
budgetmgr budget add -c CATEGORY -l LIMIT

# List all budgets
budgetmgr budget list

# Remove a budget by category
budgetmgr budget remove -c CATEGORY
```

- `-c, --category` (string, required for add/remove): Category name.
- `-l, --limit` (decimal, required for add): Monthly spending limit.

**Examples**:  
```bash
# Add budget of $500 for groceries
budgetmgr budget add -c groceries -l 500.00

# List existing budgets
budgetmgr budget list

# Remove budget for groceries
budgetmgr budget remove -c groceries
```

When a new transaction is added, the CLI checks if the total spending for that category in the current month exceeds the defined budget. A warning is printed if it does.

### 7. Generate Charts

Create ASCII-based charts for quick terminal visualization, or export PNG/SVG bar charts.

```bash
budgetmgr chart --start YYYY-MM-DD --end YYYY-MM-DD [--png | --svg]
```

- `--start YYYY-MM-DD` (string, required): Start date (inclusive).
- `--end YYYY-MM-DD` (string, required): End date (inclusive).
- `--png`: Flag to save a PNG file.
- `--svg`: Flag to save an SVG file.

**Examples**:  
```bash
# Display ASCII chart for May 2025
budgetmgr chart --start 2025-05-01 --end 2025-05-31

# Export PNG chart for June 2025
budgetmgr chart --start 2025-06-01 --end 2025-06-30 --png
# Output file: data/processed/charts/chart_2025-06-01_to_2025-06-30.png
```

---

## Practical Workflows

Below are example workflows demonstrating daily, monthly, and ad-hoc usage of BudgetManager.

### A. Daily Expense Tracking

1. **Add Daily Expenses**  
   ```bash
   budgetmgr add -c coffee -a -3.50 -d "Morning coffee"
   budgetmgr add -c lunch -a -12.00 -d "Lunch at cafe"
   ```
2. **Check Balance**  
   ```bash
   budgetmgr balance
   ```
3. **List Recent Transactions**  
   ```bash
   budgetmgr list -n 5
   ```

### B. Monthly Budgeting

1. **Define Budgets at Month Start**  
   ```bash
   budgetmgr budget add -c groceries -l 400.00
   budgetmgr budget add -c entertainment -l 200.00
   ```
2. **Record Transactions Throughout Month**  
   ```bash
   budgetmgr add -c groceries -a -50.00 -d "Supermarket"
   budgetmgr add -c entertainment -a -30.00 -d "Movie tickets"
   ```
3. **Generate Mid-Month Summary**  
   ```bash
   budgetmgr summary --range 2025-06-01T00:00:00 2025-06-15T23:59:59
   ```
4. **Generate End-of-Month Summary and CSV**  
   ```bash
   budgetmgr summary --year 2025 --month 6 --export csv
   ```
5. **Create Chart for Month**  
   ```bash
   budgetmgr chart --start 2025-06-01 --end 2025-06-30 --svg
   ```

### C. Year-End Review

1. **List All Transactions for Year**  
   ```bash
   budgetmgr summary --year 2025
   ```
2. **Export Yearly Summary to CSV**  
   ```bash
   budgetmgr summary --year 2025 --export csv
   ```
3. **Review Budgets vs. Actual Spending**  
   - Compare summary CSV data with budget definitions.
4. **Generate Yearly Chart**  
   ```bash
   budgetmgr chart --start 2025-01-01 --end 2025-12-31 --png
   ```

---

## Common Errors and Solutions

- **Invalid Command**  
  - **Error**: `Error: invalid choice: 'summry' (choose from 'add', 'list', 'balance', ...)`  
  - **Solution**: Check spelling or run `budgetmgr --help` to view valid commands.

- **Missing Required Arguments**  
  - **Error**: `Error: Missing option '-c/--category' for command 'add'`  
  - **Solution**: Provide all required flags. Example: `budgetmgr add -c salary -a 500.00`.

- **Invalid Date Format**  
  - **Error**: `Error: Invalid timestamp format: '2025/06/01'`  
  - **Solution**: Use ISO 8601 format: `YYYY-MM-DDThh:mm:ss` for timestamps, `YYYY-MM-DD` for chart dates.

- **CSV Export Permission Denied**  
  - **Error**: `PermissionError: [Errno 13] Permission denied: 'data/processed/...'`  
  - **Solution**: Ensure the `data/processed/` directory exists and is writable. Create manually if needed.

---

## Tips and Best Practices

- **Consistent Naming**: Use consistent category names (e.g., `groceries` vs. `grocery`) to avoid fragmented category totals.  
- **Timestamp Precision**: If exact time of expense matters (e.g., multiple entries per day), always specify time. Otherwise, omit and let the system record current time.  
- **Budget Alerts**: Define budgets for categories where you want to limit spending. When you approach or exceed, BudgetManager notifies you.  
- **Regular Backups**: Periodically back up the SQLite database (`budget.db`) by copying from the `data/processed` directory.  
- **Combining Commands**: Use shell scripts or automation tools (cron, Task Scheduler) to regularly export summaries or generate charts.  

---

## Further Resources

- **Full Documentation**: See the `docs/` directory for additional guides, including `reports.md` and `project_structure.txt`.  
- **Source Code**: Explore `src/budgetmanager` for implementation details.  
- **Testing**: If you wish to contribute or verify functionality, refer to the `tests/` directory containing unit and integration tests.

For any questions or issues, please open an issue on the GitHub repository:  
https://github.com/RealNamison/budgetmanager/issues  
