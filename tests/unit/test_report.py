#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Unit tests for the ReportGenerator class in report.py.

This module tests monthly_summary, yearly_summary,
and CSV export functionality.
"""

import csv
from decimal import Decimal
from pathlib import Path
import calendar

import pytest

from budgetmanager.core.report import ReportGenerator
from budgetmanager.core.ledger import Ledger
from budgetmanager.core.transaction import Transaction
from budgetmanager.utils.timestamp import Timestamp


def make_sample_ledger() -> Ledger:
    """
    Helper function to create a Ledger with sample transactions.

    Returns:
        Ledger: A ledger populated with transactions in May and June 2025,
            as well as May 2024.
    """
    ledger = Ledger()
    # May 2025: income and expense
    ledger.add_transaction(Transaction(
        timestamp=Timestamp.from_components(2025, 5, 1),
        category="Salary",
        amount=Decimal("1000.00"),
        description="Monthly salary"
    ))
    ledger.add_transaction(Transaction(
        timestamp=Timestamp.from_components(2025, 5, 15),
        category="Groceries",
        amount=Decimal("-200.50"),
        description="Supermarkt"
    ))
    # June 2025: only income
    ledger.add_transaction(Transaction(
        timestamp=Timestamp.from_components(2025, 6, 10),
        category="Freelance",
        amount=Decimal("500.00"),
        description="Projekt X"
    ))
    # May 2024: different year
    ledger.add_transaction(Transaction(
        timestamp=Timestamp.from_components(2024, 5, 20),
        category="Gift",
        amount=Decimal("150.00"),
        description="Birthday gift"
    ))
    return ledger


def test_monthly_summary_correct_values() -> None:
    """
    Test that monthly_summary returns correct totals and balance.

    Verifies income, expenses, and net balance for May 2025.
    """
    ledger = make_sample_ledger()
    summary = ReportGenerator.monthly_summary(ledger, year=2025, month=5)

    assert summary["income"] == Decimal("1000.00")
    assert summary["expenses"] == Decimal("-200.50")
    assert summary["balance"] == Decimal("799.50")


def test_monthly_summary_no_transactions() -> None:
    """
    Test that monthly_summary returns zeros when no transactions exist.

    Checks a month with no entries (July 2025).
    """
    ledger = make_sample_ledger()
    summary = ReportGenerator.monthly_summary(ledger, year=2025, month=7)

    assert summary["income"] == Decimal("0")
    assert summary["expenses"] == Decimal("0")
    assert summary["balance"] == Decimal("0")


def test_monthly_summary_invalid_month() -> None:
    """
    Test that monthly_summary raises ValueError for invalid month.

    An invalid month (0 or >12) should trigger a ValueError.
    """
    ledger = make_sample_ledger()
    with pytest.raises(ValueError):
        ReportGenerator.monthly_summary(ledger, year=2025, month=0)


def test_yearly_summary_correct_values() -> None:
    """
    Test that yearly_summary returns correct totals and balance.

    Verifies sums for years 2025 and 2024.
    """
    ledger = make_sample_ledger()
    summary_2025 = ReportGenerator.yearly_summary(ledger, year=2025)

    # 2025: income 1000 + 500, expenses -200.50
    assert summary_2025["income"] == Decimal("1500.00")
    assert summary_2025["expenses"] == Decimal("-200.50")
    assert summary_2025["balance"] == Decimal("1299.50")

    summary_2024 = ReportGenerator.yearly_summary(ledger, year=2024)
    assert summary_2024["income"] == Decimal("150.00")
    assert summary_2024["expenses"] == Decimal("0")
    assert summary_2024["balance"] == Decimal("150.00")


def test_export_to_csv(tmp_path: Path) -> None:
    """
    Test that export_to_csv writes a CSV file with expected content.

    Args:
        tmp_path (Path): Temporary directory fixture for output file.
    """
    data = {
        "income": Decimal("123.45"),
        "expenses": Decimal("-67.89"),
        "balance": Decimal("55.56"),
    }
    out_file = tmp_path / "summary.csv"
    result_path = ReportGenerator.export_to_csv(data, out_file)

    # Path is correct and file exists
    assert result_path == out_file
    assert out_file.exists()

    # Verify CSV content
    with out_file.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # First row is header
    assert rows[0] == ["field", "value"]
    # Convert remaining rows to dict for comparison
    content = {row[0]: row[1] for row in rows[1:]}
    assert content["income"] == "123.45"
    assert content["expenses"] == "-67.89"
    assert content["balance"] == "55.56"


def test_monthly_summary_february_leap_year() -> None:
    """
    Test that monthly_summary includes transactions on Feb 29 of a leap
    year (2024).
    """
    ledger = Ledger()
    ledger.add_transaction(Transaction(
        timestamp=Timestamp.from_components(2024, 2, 29),
        category="LeapDay",
        amount=Decimal("100.00"),
        description="Leap day income"
    ))
    summary = ReportGenerator.monthly_summary(ledger, year=2024, month=2)

    assert summary["income"] == Decimal("100.00")
    assert summary["expenses"] == Decimal("0")
    assert summary["balance"] == Decimal("100.00")


def test_monthly_summary_february_non_leap_year() -> None:
    """
    Test that monthly_summary correctly handles February in a non-leap
    year (2025).
    """
    ledger = Ledger()
    # Mitte Februar Ausgabe
    ledger.add_transaction(Transaction(
        timestamp=Timestamp.from_components(2025, 2, 15),
        category="Expense",
        amount=Decimal("-50.00"),
        description="Mid-February expense"
    ))
    # Ende Februar Einnahme
    ledger.add_transaction(Transaction(
        timestamp=Timestamp.from_components(2025, 2, 28),
        category="Income",
        amount=Decimal("200.00"),
        description="End-of-February income"
    ))
    summary = ReportGenerator.monthly_summary(ledger, year=2025, month=2)

    assert summary["income"] == Decimal("200.00")
    assert summary["expenses"] == Decimal("-50.00")
    assert summary["balance"] == Decimal("150.00")


def test_range_summary_full_month() -> None:
    """
    Test that range_summary over full May 2025 matches monthly_summary.

    Uses the full month range and compares with monthly_summary results.
    """
    ledger = make_sample_ledger()
    # full May 2025: from May 1 to May 31
    start = Timestamp.from_components(2025, 5, 1)
    end_day = calendar.monthrange(2025, 5)[1]
    end = Timestamp.from_components(2025, 5, end_day)

    full_range = ReportGenerator.range_summary(ledger, start, end)
    monthly = ReportGenerator.monthly_summary(ledger, year=2025, month=5)

    assert full_range == monthly


def test_range_summary_empty() -> None:
    """
    Test that range_summary returns zeros for a range with no transactions.
    """
    ledger = make_sample_ledger()
    # July 2025 has no sample transactions
    start = Timestamp.from_components(2025, 7, 1)
    end = Timestamp.from_components(2025, 7, 31)

    summary = ReportGenerator.range_summary(ledger, start, end)
    assert summary["income"] == Decimal("0")
    assert summary["expenses"] == Decimal("0")
    assert summary["balance"] == Decimal("0")


def test_range_summary_partial_span() -> None:
    """
    Test that range_summary correctly aggregates
    transactions between two dates.

    Range covers the expense on May 15 and the income on June 10.
    """
    ledger = make_sample_ledger()
    start = Timestamp.from_components(2025, 5, 15)
    end = Timestamp.from_components(2025, 6, 10)

    summary = ReportGenerator.range_summary(ledger, start, end)
    # expected: income 500.00, expenses -200.50, balance 299.50
    assert summary["income"] == Decimal("500.00")
    assert summary["expenses"] == Decimal("-200.50")
    assert summary["balance"] == Decimal("299.50")


def test_range_summary_invalid_dates() -> None:
    """
    Test that range_summary raises ValueError when start is after end.
    """
    ledger = make_sample_ledger()
    start = Timestamp.from_components(2025, 6, 1)
    end = Timestamp.from_components(2025, 5, 1)

    with pytest.raises(ValueError):
        ReportGenerator.range_summary(ledger, start, end)
