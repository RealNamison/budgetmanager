#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Advanced Usage Script for BudgetManager

This script demonstrates advanced usage of the BudgetManager Python API,
including programmatic transaction creation, budget management, report
generation, and chart creation. It uses type hints, follows PEP 8 standards,
and includes Google-style docstrings.
"""

from decimal import Decimal
from pathlib import Path

from budgetmanager.file.sqlite_handler import SQLiteHandler
from budgetmanager.core.transaction import Transaction
from budgetmanager.core.ledger import Ledger
from budgetmanager.core.budget import Budget
from budgetmanager.core.report import ReportGenerator
from budgetmanager.core.chart import Chart
from budgetmanager.utils.timestamp import Timestamp


def main() -> None:
    """
    Execute advanced usage examples of BudgetManager's API.
    """
    # Initialize database handler
    db_handler = SQLiteHandler()

    # Add sample transactions
    try:
        txn1 = Transaction(
            timestamp=Timestamp.from_datetime(),
            category="consulting",
            amount=Decimal("1200.00"),
            description="Consulting services"
        )
        db_handler.add_transaction(txn1)

        txn2 = Transaction(
            timestamp=Timestamp.from_datetime(),
            category="office_supplies",
            amount=Decimal("-150.75"),
            description="Printer ink and paper"
        )
        db_handler.add_transaction(txn2)
    except Exception as exc:
        print(f"Error adding transactions: {exc}")

    # Load all transactions into ledger
    transactions = db_handler.get_all_transactions()
    ledger = Ledger(transactions=transactions)

    # Print ledger summary
    total_income = ledger.total_income()
    total_expenses = ledger.total_expense()
    net_balance = ledger.balance()

    print(f"Total Income   : {total_income}")
    print(f"Total Expenses : {total_expenses}")
    print(f"Net Balance    : {net_balance}\n")

    # Define and add budgets
    try:
        budget1 = Budget(category="office_supplies", limit=Decimal("200.00"))
        db_handler.add_budget(budget1)
    except Exception as exc:
        print(f"Error adding budget: {exc}")

    # Generate a custom date range report
    start_ts = Timestamp.from_iso_format("2025-06-01T00:00:00")
    end_ts = Timestamp.from_iso_format("2025-06-30T23:59:59")
    report_data = ReportGenerator.generate_summary_by_range(
        start_ts, end_ts, ledger
    )

    print("Custom Date Range Report (June 2025):")
    print(f"Total Income   : {report_data['total_income']}")
    print(f"Total Expenses : {report_data['total_expenses']}")
    print(f"Net Balance    : {report_data['net_balance']}")
    print("By Category:")
    for category, amount in report_data["by_category"].items():
        print(f"  {category} : {amount}")
    print()

    # Export report to CSV
    output_csv = Path("data/processed/summary_june2025.csv")
    try:
        ReportGenerator.export_to_csv(report_data, output_csv)
        print(f"Report exported to {output_csv}")
    except Exception as exc:
        print(f"Error exporting report: {exc}")

    # Generate and save a chart
    output_chart_path = Path("data/processed/charts/chart_june2025.png")
    try:
        Chart.export_graphical_chart(
            ledger=ledger,
            start=start_ts,
            end=end_ts,
            output_path=output_chart_path
        )
        print(f"Chart saved to {output_chart_path}")
    except Exception as exc:
        print(f"Error generating chart: {exc}")


if __name__ == "__main__":
    main()
