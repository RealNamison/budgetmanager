# Reports

The **Reports** module in BudgetManager is responsible for generating summarized financial data, including income, expenses, and balances. These summaries can be used for budgeting analysis, tax preparation, or general financial tracking. Reports can be generated for a specific year, month, or a custom date range, and can be exported to CSV for further processing.

---

## Overview of the Report Module

- **Location**: `src/budgetmanager/core/report.py`  
- **Primary Class/Functions**:
  - `ReportGenerator`: A static class that provides methods to compute financial summaries.
    - `generate_summary_by_year(year: int, ledger: Ledger) -> dict[str, float]`
    - `generate_summary_by_month(year: int, month: int, ledger: Ledger) -> dict[str, float]`
    - `generate_summary_by_range(start: Timestamp, end: Timestamp, ledger: Ledger) -> dict[str, float]`
    - `export_to_csv(summary_data: dict[str, float], output_path: Path) -> Path`

### Summary Data Structure

The summary methods return a dictionary containing:
- `"total_income"`: Total income within the specified period.
- `"total_expenses"`: Total expenses within the specified period.
- `"net_balance"`: Net balance (income minus expenses) within the specified period.
- `"by_category"`: A nested dictionary mapping each category to its total amount (positive for income, negative for expense).

Example:
```python
{
    "total_income": 5000.00,
    "total_expenses": 1200.50,
    "net_balance": 3799.50,
    "by_category": {
        "salary": 5000.00,
        "groceries": -400.25,
        "rent": -800.25
    }
}
```

---

## How to Generate Reports via CLI

BudgetManager provides a `summary` command to generate and view reports from the command line. The data is pulled from the SQLite database defined in your configuration.

### Command Syntax

```bash
budgetmgr summary [--year YEAR] [--month MONTH] [--range START END] [--export csv]
```

- `--year YEAR`: Four-digit year (e.g., `2025`). This option can be used alone or together with `--month`.
- `--month MONTH`: Month number (1–12). Requires `--year` to be specified.
- `--range START END`: Two ISO 8601 timestamps defining the start and end of the report period (inclusive).  
  - Example: `2025-05-01T00:00:00 2025-05-31T23:59:59`.
- `--export csv`: Optional flag to export the report to a CSV file. The file will be saved under the configured data directory as `summary_<label>.csv`, where `<label>` is either `<year>` or `<start>_to_<end>`.

### Valid Scenarios

1. **Yearly Summary**  
   ```bash
   budgetmgr summary --year 2025
   ```
   Generates a summary for all transactions in the year 2025.

2. **Monthly Summary**  
   ```bash
   budgetmgr summary --year 2025 --month 6
   ```
   Generates a summary for June 2025.

3. **Custom Range Summary**  
   ```bash
   budgetmgr summary --range 2025-05-01T00:00:00 2025-05-15T23:59:59
   ```
   Generates a summary for transactions between May 1, 2025, and May 15, 2025.

4. **Exporting to CSV**  
   - Yearly CSV:
     ```bash
     budgetmgr summary --year 2025 --export csv
     ```
     Saves the file as `data/processed/summary_2025.csv`.
   - Range CSV:
     ```bash
     budgetmgr summary --range 2025-05-01T00:00:00 2025-05-15T23:59:59 --export csv
     ```
     Saves the file as `data/processed/summary_2025-05-01_to_2025-05-15.csv`.

In each case, the summary is printed to the console with a simple layout:
```
Summary for [Period]
--------------------
Total Income   : 5000.00
Total Expenses : 1200.50
Net Balance    : 3799.50

By Category:
  salary : 5000.00
  groceries : -400.25
  rent : -800.25
```

---

## Detailed API Usage

For advanced users or integration in Python scripts, the `ReportGenerator` can be used directly:

```python
from budgetmanager.core.report import ReportGenerator
from budgetmanager.core.ledger import Ledger
from budgetmanager.utils.timestamp import Timestamp
from budgetmanager.file.sqlite_handler import SQLiteHandler

# Initialize the database handler and load transactions
db_handler = SQLiteHandler()
all_transactions = db_handler.get_all_transactions()
ledger = Ledger(transactions=all_transactions)

# Yearly summary
yearly_summary = ReportGenerator.generate_summary_by_year(2025, ledger)

# Monthly summary
june_summary = ReportGenerator.generate_summary_by_month(2025, 6, ledger)

# Custom range summary
start_ts = Timestamp.from_iso_format("2025-05-01T00:00:00")
end_ts = Timestamp.from_iso_format("2025-05-31T23:59:59")
range_summary = ReportGenerator.generate_summary_by_range(start_ts, end_ts, ledger)

# Export to CSV
from pathlib import Path
output_path = Path("data/processed/summary_2025-05.csv")
ReportGenerator.export_to_csv(range_summary, output_path)
```

### Export Format

The CSV file follows a header and row structure:

```
category,amount
salary,5000.00
groceries,-400.25
rent,-800.25
,
total_income,5000.00
total_expenses,1200.50
net_balance,3799.50
```

- Each line under the `category,amount` section represents the total for a single category.
- Blank line separates category breakdown from the overall totals.
- Totals appear at the bottom of the CSV under `total_income`, `total_expenses`, and `net_balance`.

---

## Combining Reports with Charts

Once you have generated a report, you can further visualize category breakdowns using the **Chart** feature:

```bash
budgetmgr chart --start 2025-05-01 --end 2025-05-31 --png
```

This command will create a bar chart PNG representing the income and expenses per category for the specified period. The report data and the chart together provide comprehensive insight into financial trends.

---

## Automating Report Generation

You can integrate report generation into scripts or scheduled tasks. For example, to create a monthly report on the 1st day of each month at 08:00 AM, you could schedule a cron job:

```
0 8 1 * * budgetmgr summary --year $(date +\%Y) --month $(date +\%m) --export csv
```

Alternatively, if you use task schedulers like `cron` or Windows Task Scheduler, point them to run the above command at the desired time interval.

---

## Best Practices and Tips

- **Consistent Timestamps**: Ensure transactions have accurate timestamps. Use the ISO 8601 format (`YYYY-MM-DDThh:mm:ss`) when specifying `--range` periods.
- **Regular Exports**: Regularly export CSV summaries for external analysis or backup.
- **Backup SQLite Database**: Periodically back up the `budget.db` file located in `data/processed/` to prevent data loss.
- **Combine with Budgets**: After generating a report, compare category totals with defined budgets to identify overspending.
- **Version Control**: Store CSV reports in version control if you track historical financial data outside BudgetManager.

---

## Troubleshooting

- **No Transactions Found**: If your summary returns zeros, verify that the database contains transactions within the specified date range.
- **Incorrect Date Format**: Ensure that your `--range` dates are in ISO 8601 format. The CLI will reject invalid timestamps.
- **CSV Permission Errors**: When exporting to CSV, ensure the `data/processed/` directory exists and is writable. Use `budgetmgr` commands or manually create the directory if needed.

---

## Example Workflow

1. **Add Several Transactions**  
   ```bash
   budgetmgr add -c salary -a 4500.00 -d "Paycheck"
   budgetmgr add -c groceries -a -200.75 -d "Weekly groceries"
   budgetmgr add -c utilities -a -120.00 -d "Electricity bill"
   ```

2. **Generate a Monthly Report (May 2025)**  
   ```bash
   budgetmgr summary --year 2025 --month 5 --export csv
   ```

3. **View the Generated CSV**  
   ```bash
   less data/processed/summary_2025-05.csv
   ```

4. **Generate a Chart for the Same Period**  
   ```bash
   budgetmgr chart --start 2025-05-01 --end 2025-05-31 --png
   ```

5. **Review the Chart**  
   Open the generated `chart_2025-05-01_to_2025-05-31.png` under `data/processed/charts/`.

---

## Contributing to Reports

Contributions to the reporting feature are welcome. When submitting a pull request:

- Include test cases for new summary calculations.
- Update `docs/reports.md` with any added functionality.
- Follow naming conventions: new methods should be added to `ReportGenerator`.
- Ensure CSV export formatting remains consistent.

---

## References

- **ReportGenerator Implementation**:  
  See `src/budgetmanager/core/report.py` for detailed code and docstrings.
- **CLI Summary Command**:  
  See `src/budgetmanager/cli/cli.py` under the `summary` subcommand implementation.
