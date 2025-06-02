#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Pytest fixtures for chart module tests, providing a real Ledger
with two sample transactions (income & expense).
"""

from decimal import Decimal

import pytest

from budgetmanager.core.chart import generate_chart, _print_ascii_chart
from budgetmanager.core.transaction import Transaction
from budgetmanager.core.ledger import Ledger
from budgetmanager.file.file_handler import FileHandler
from budgetmanager.utils.timestamp import Timestamp


@pytest.fixture
def sample_ledger() -> Ledger:
    """Return a Ledger pre-populated with one income and one expense."""
    ledger = Ledger()
    # timestamp at 2025-01-01 00:00:00
    ts = Timestamp.from_components(2025, 1, 1)
    # add one income
    ledger.add_transaction(
        Transaction(
            ts,
            "salary",
            Decimal("1000"),
            "monthly salary"
        )
    )
    # add one expense
    ledger.add_transaction(
        Transaction(
            ts,
            "groceries",
            Decimal("-200"),
            "weekly groceries"
        )
    )
    return ledger


def test_print_ascii_chart(capsys) -> None:
    """Ensure ASCII chart prints section header and bars."""
    data = {"catA": Decimal("2"), "catB": Decimal("4")}
    _print_ascii_chart("Section", data)
    out = capsys.readouterr().out

    assert "Section:" in out
    assert "catA" in out
    assert "catB" in out


def test_generate_chart_empty(capsys) -> None:
    """Check message when no transactions are in the given range."""
    empty_ledger = Ledger()
    start = Timestamp.from_components(2025, 5, 1)
    end = Timestamp.from_components(2025, 5, 1, 23, 59, 59, 999_999)

    generate_chart(empty_ledger, start, end)
    out = capsys.readouterr().out

    assert "No data in the specified time range." in out


def test_generate_chart_ascii_only(sample_ledger, capsys) -> None:
    """
    Verify ASCII output for the sample_ledger fixture
    (one income, one expense).
    """
    start = Timestamp.from_components(2025, 1, 1)
    end = Timestamp.from_components(2025, 1, 1, 23, 59, 59, 999_999)

    generate_chart(sample_ledger, start, end)
    out = capsys.readouterr().out

    assert "Income:" in out
    assert "salary" in out
    assert "Expenses:" in out
    assert "groceries" in out


def test_generate_chart_with_export(
    sample_ledger, tmp_path, monkeypatch, capsys
) -> None:
    """Ensure graphical export saves a PNG file and prints its path."""
    # Redirect chart output directory to tmp_path
    monkeypatch.setattr(FileHandler, "create_directory", lambda p: tmp_path)

    # Use the same date as sample_ledger entries to ensure data is found
    start = Timestamp.from_components(2025, 1, 1)
    end = Timestamp.from_components(2025, 1, 1, 23, 59, 59, 999_999)

    generate_chart(sample_ledger, start, end, export_format="png")

    date_str = start.to_isoformat().split("T")[0]
    expected_path = tmp_path / f"chart_{date_str}_to_{date_str}.png"

    assert expected_path.exists()
    out = capsys.readouterr().out
    assert "Graphical chart saved to:" in out
