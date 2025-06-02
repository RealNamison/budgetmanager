#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Module for generating ASCII and graphical charts of income and
expenses per category over a specified time period.

Uses matplotlib for graphical output and saves optional PNG/SVG
under data/processed/charts/.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Dict, Set

import matplotlib.pyplot as plt

from ..file.file_handler import FileHandler
from .ledger import Ledger
from ..utils.timestamp import Timestamp


def generate_chart(
    ledger: Ledger,
    start: Timestamp,
    end: Timestamp,
    export_format: str | None = None
) -> None:
    """Generate an ASCII chart and optional graphical chart.

    Args:
        ledger (Ledger): Ledger containing transactions.
        start (Timestamp): Start timestamp (inclusive).
        end (Timestamp): End timestamp (inclusive).
        export_format (str | None): 'png' or 'svg' to export file,
            or None to skip graphical export.

    Raises:
        ValueError: If export_format is not 'png', 'svg', or None.
    """
    # Filter transactions in the specified time period
    txs = ledger.filter_by_date_range(start, end)

    # Collect sums per category
    incomes: Dict[str, Decimal] = {}
    expenses: Dict[str, Decimal] = {}
    categories: Set[str] = set()
    for tx in txs:
        cat = tx.category
        categories.add(cat)
        if tx.is_income():
            incomes[cat] = incomes.get(cat, Decimal("0")) + tx.amount
        elif tx.is_expense():
            expenses[cat] = expenses.get(cat, Decimal("0")) + abs(tx.amount)

    if not categories:
        print("No data in the specified time range.")
        return

    # Print ASCII charts
    _print_ascii_chart("Income", incomes)
    _print_ascii_chart("Expenses", expenses)

    # Optional PNG/SVG output
    if export_format:
        if export_format not in ("png", "svg"):
            raise ValueError(f"Invalid format: {export_format}")
        _export_graphical_chart(
            categories, incomes, expenses, start, end, export_format
        )


def _print_ascii_chart(
    title: str,
    data: Dict[str, Decimal]
) -> None:
    """Print a horizontal ASCII bar chart.

    Args:
        title (str): Section title.
        data (Dict[str, Decimal]): Mapping from category to amount.
    """
    print(f"\n{title}:")
    max_label = max((len(cat) for cat in data), default=0)
    max_val = max((val for val in data.values()), default=Decimal("1"))
    scale = 40 / float(max_val)
    for cat, val in sorted(data.items()):
        bar = "#" * int(float(val) * scale)
        print(f"{cat.rjust(max_label)} | {bar} ({val})")


def _export_graphical_chart(
    categories: Set[str],
    incomes: Dict[str, Decimal],
    expenses: Dict[str, Decimal],
    start: Timestamp,
    end: Timestamp,
    export_format: str
) -> None:
    """Export bar chart using matplotlib.

    Args:
        categories (Set[str]): All categories.
        incomes (Dict[str, Decimal]): Income per category.
        expenses (Dict[str, Decimal]): Expenses per category.
        start (Timestamp): Start timestamp.
        end (Timestamp): End timestamp.
        export_format (str): 'png' or 'svg'.

    Raises:
        OSError: If saving the chart fails.
    """
    # Define order
    cats = sorted(categories)
    inc_vals = [float(incomes.get(c, Decimal("0"))) for c in cats]
    exp_vals = [float(expenses.get(c, Decimal("0"))) for c in cats]

    x = list(range(len(cats)))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar([i - width / 2 for i in x], inc_vals, width, label="Income")
    ax.bar([i + width / 2 for i in x], exp_vals, width, label="Expenses")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, rotation=45, ha="right")
    ax.legend()
    fig.tight_layout()

    # Prepare output path
    charts_dir: Path = FileHandler.create_directory("processed/charts")
    start_str = start.to_isoformat().split("T")[0]
    end_str = end.to_isoformat().split("T")[0]
    filename = f"chart_{start_str}_to_{end_str}.{export_format}"
    file_path = charts_dir / filename

    try:
        fig.savefig(file_path)
        print(f"\nGraphical chart saved to: {file_path}")
    except Exception as e:
        raise OSError(f"Could not save chart: {e}") from e
