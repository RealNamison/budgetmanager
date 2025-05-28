#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Generate summarized views (monthly, yearly) and export reports.
"""

from __future__ import annotations
from decimal import Decimal
from typing import Any
from pathlib import Path
import calendar

from .ledger import Ledger
from ..utils.timestamp import Timestamp


class ReportGenerator:
    """Compute summaries and export them in different formats."""

    @staticmethod
    def monthly_summary(ledger: Ledger, year: int, month: int) -> dict[str, Decimal]:
        """Compute total income, expenses and balance for a given month.

        Args:
            ledger (Ledger): The ledger to summarize.
            year (int): Four-digit year.
            month (int): Month (1–12).

        Returns:
            dict[str, Decimal]:
                {
                    "income": total positive amounts,
                    "expenses": total negative amounts,
                    "balance": net balance
                }

        Raises:
            ValueError: If month is not in 1..12.
        """
        if not 1 <= month <= 12:
            raise ValueError(f"Invalid month: {month}")

        # define start/end timestamps
        start = Timestamp.from_components(year, month, 1)
        _, end_day = calendar.monthrange(year, month)
        end = Timestamp.from_components(year, month, end_day)
        # filter transactions
        txs = ledger.filter_by_date_range(start, end)
        income = sum((t.amount for t in txs if t.is_income()), Decimal("0"))
        expenses = sum((t.amount for t in txs if t.is_expense()), Decimal("0"))
        return {"income": income, "expenses": expenses,
                "balance": income + expenses}

    @staticmethod
    def yearly_summary(ledger: Ledger, year: int) -> dict[str, Decimal]:
        """Compute total income, expenses and balance for a given year.

        Args:
            ledger (Ledger): The ledger to summarize.
            year (int): Four-digit year.

        Returns:
            dict[str, Decimal]:
                {"income": …, "expenses": …, "balance": …}
        """
        start = Timestamp.from_components(year, 1, 1)
        end = Timestamp.from_components(year, 12, 31)
        txs = ledger.filter_by_date_range(start, end)
        income = sum((t.amount for t in txs if t.is_income()), Decimal("0"))
        expenses = sum((t.amount for t in txs if t.is_expense()), Decimal("0"))
        return {"income": income, "expenses": expenses,
                "balance": income + expenses}

    @staticmethod
    def range_summary(
            ledger: Ledger,
            start: Timestamp,
            end: Timestamp
    ) -> dict[str, Decimal]:
        """Compute total income, expenses and balance between two timestamps.

        Args:
            ledger (Ledger): The ledger to summarize.
            start (Timestamp): Start of interval (inclusive).
            end (Timestamp): End of interval (inclusive).

        Returns:
            dict[str, Decimal]: {
                "income": total positive amounts,
                "expenses": total negative amounts,
                "balance": income + expenses
            }

        Raises:
            ValueError: If start is after end.

        Examples:
            >>> from utils.timestamp import Timestamp
            >>> from .ledger import Ledger
            >>> start = Timestamp.from_isoformat("2025-01-01T00:00:00")
            >>> end = Timestamp.from_isoformat("2025-01-31T23:59:59")
            >>> ReportGenerator.range_summary(ledger, start, end)
            {"income": Decimal("..."), "expenses": Decimal("..."), "balance": Decimal("...")}
        """
        if start > end:
            raise ValueError(f"Start {start} is after end {end}")

        txs = ledger.filter_by_date_range(start, end)
        income = sum((t.amount for t in txs if t.is_income()), Decimal("0"))
        expenses = sum((t.amount for t in txs if t.is_expense()), Decimal("0"))
        return {
            "income": income,
            "expenses": expenses,
            "balance": income + expenses
        }

    @staticmethod
    def export_to_csv(data: dict[str, Any], path: Path) -> Path:
        """Export summary dict to a CSV file with two columns.

        Args:
            data (dict[str, Any]): Mapping of field→value.
            path (Path): Ziel-CSV-Pfad.

        Returns:
            Path: Path zur geschriebenen Datei.

        Raises:
            OSError: Bei Schreibfehlern.
        """
        import csv

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(("field", "value"))
            for key, val in data.items():
                writer.writerow((key, val))
        return path
