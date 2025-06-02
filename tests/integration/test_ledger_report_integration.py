#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Integration tests for Ledger → ReportGenerator.

Verifies that monthly and yearly summaries are computed correctly
and that summaries can be exported to CSV.
"""

from decimal import Decimal
from pathlib import Path

from budgetmanager.core.ledger import Ledger
from budgetmanager.core.transaction import Transaction
from budgetmanager.core.report import ReportGenerator
from budgetmanager.utils.timestamp import Timestamp


def test_monthly_and_yearly_summary(tmp_path: Path) -> None:
    """
    Test that ReportGenerator produces correct monthly and yearly
    summaries and exports the monthly summary to CSV.

    Args:
        tmp_path (Path): Temporary directory for CSV export.

    Raises:
        AssertionError: If summary values or CSV export path are invalid.
    """
    # Arrange: create a ledger and add three transactions
    ledger = Ledger()
    # two transactions in January and one in February
    ledger.add_transaction(
        Transaction(
            timestamp=Timestamp.from_components(2025, 1, 10),
            category="inc",
            amount=Decimal("200"),
            description=""
        )
    )
    ledger.add_transaction(
        Transaction(
            timestamp=Timestamp.from_components(2025, 1, 20),
            category="exp",
            amount=Decimal("-50"),
            description=""
        )
    )
    ledger.add_transaction(
        Transaction(
            timestamp=Timestamp.from_components(2025, 2, 1),
            category="inc",
            amount=Decimal("100"),
            description=""
        )
    )

    # Act: generate summaries and export the January summary to CSV
    january_summary = ReportGenerator.monthly_summary(ledger, 2025, 1)
    yearly_summary = ReportGenerator.yearly_summary(ledger, 2025)
    csv_path = tmp_path / "summary_2025-01.csv"
    exported_file = ReportGenerator.export_to_csv(january_summary, csv_path)

    # Assert: verify summary contents and CSV export success
    assert january_summary == {
        "income": Decimal("200"),
        "expenses": Decimal("-50"),
        "balance": Decimal("150"),
    }
    assert "income" in yearly_summary and "balance" in yearly_summary
    assert exported_file.exists()
