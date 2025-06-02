#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
End-to-end integration tests for the CLI.

Verifies that all commands and options from the cli module operate correctly
against a temporary DATA_ROOT and SQLite database backend.
"""

import subprocess
import os
import sys
from pathlib import Path

import pytest

from budgetmanager import config


@pytest.fixture(autouse=True)
def isolate_data_root_and_db(tmp_path: Path, monkeypatch) -> None:
    """
    Override DATA_ROOT and DB_FILE for all CLI tests to use a temporary
    directory and database.
    """
    # Redirect DATA_ROOT to tmp_path
    monkeypatch.setenv("BUDGETMANAGER_DATA_ROOT", str(tmp_path))
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)

    # Ensure the SQLiteHandler uses a DB under tmp_path/processed/budget.db
    db_file = tmp_path / "processed" / "budget.db"
    monkeypatch.setattr(config, "DB_FILE", db_file)


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    """
    Helper to invoke the CLI.

    Args:
        args: Command-line arguments for budgetmgr.

    Returns:
        CompletedProcess with stdout, stderr, and returncode.
    """
    cmd = [sys.executable, "-m", "budgetmanager.cli.cli"] + args
    env = os.environ.copy()
    env["BUDGETMANAGER_DATA_ROOT"] = str(config.DATA_ROOT)
    return subprocess.run(cmd, env=env, capture_output=True, text=True)


def test_cli_no_command() -> None:
    """Running without arguments should print usage and return non-zero."""
    result = run_cmd([])
    assert result.returncode != 0
    assert "usage: budgetmgr" in result.stderr


def test_cli_list_empty() -> None:
    """
    The 'list' command without any transactions
    returns a notice and exit code 0.
    """
    result = run_cmd(["list"])
    assert result.returncode == 0
    assert "No transactions found." in result.stdout


def test_cli_balance_empty() -> None:
    """The 'balance' command with no transactions shows 0 for all fields."""
    result = run_cmd(["balance"])
    assert result.returncode == 0
    assert "Balance:  0" in result.stdout
    assert "Income:   0" in result.stdout
    assert "Expenses: 0" in result.stdout


def test_cli_add_and_list_default() -> None:
    """Test that 'add' without timestamp/description and 'list' work."""
    res_add = run_cmd(["add", "-c", "test", "-a", "10.00"])
    assert res_add.returncode == 0
    assert "Added:" in res_add.stdout

    res_list = run_cmd(["list"])
    assert res_list.returncode == 0
    assert "test: 10.00" in res_list.stdout


def test_cli_add_with_timestamp_and_description() -> None:
    """
    'add' with -t and -d should use the correct timestamp and description.
    """
    ts = "2025-05-15T12:30:00"
    res = run_cmd(
        ["add", "-t", ts, "-c", "tscat", "-a", "15.00", "-d", "sample desc"]
    )
    assert res.returncode == 0
    assert f"Added: {ts}" in res.stdout
    assert "(sample desc)" in res.stdout


def test_cli_invalid_amount() -> None:
    """Invalid amount results in exit code 1 and an error message."""
    res = run_cmd(["add", "-c", "foo", "-a", "notnum"])
    assert res.returncode == 1
    assert "Invalid amount" in res.stderr


def test_cli_invalid_timestamp() -> None:
    """Invalid timestamp format results in exit code 1."""
    res = run_cmd(["add", "-t", "badtime", "-c", "foo", "-a", "1.00"])
    assert res.returncode == 1
    assert "Invalid timestamp" in res.stderr


def test_cli_remove_transaction() -> None:
    """'remove' removes a transaction by ID."""
    # Add a transaction
    run_cmd(["add", "-c", "remcat", "-a", "5.00"])
    # Directly query DB for ID
    import sqlite3

    conn = sqlite3.connect(str(config.DB_FILE))
    cur = conn.execute(
        "SELECT id FROM transactions WHERE category=?", ("remcat",)
    )
    row = cur.fetchone()
    conn.close()
    assert row is not None
    tx_id = row[0]

    # Remove it
    res = run_cmd(["remove", "-i", str(tx_id)])
    assert res.returncode == 0
    assert f"Removed transaction with ID {tx_id}" in res.stdout

    # Ensure list is empty again
    res_list = run_cmd(["list"])
    assert "No transactions found." in res_list.stdout


def test_cli_summary_monthly_and_yearly() -> None:
    """
    Test 'summary' with a month and without a month, including CSV export.
    """
    # Add income and expense in January 2025
    run_cmd(["add", "-t", "2025-01-10T00:00:00", "-c", "inc", "-a", "100"])
    run_cmd(["add", "-t", "2025-01-20T00:00:00", "-c", "exp", "-a", "-40"])

    # Monthly summary
    res_m = run_cmd(["summary", "-y", "2025", "-m", "1"])
    assert res_m.returncode == 0
    assert "2025-01 Income: 100" in res_m.stdout
    assert "2025-01 Expenses: -40" in res_m.stdout
    assert "2025-01 Balance: 60" in res_m.stdout

    # Yearly summary
    res_y = run_cmd(["summary", "-y", "2025"])
    assert res_y.returncode == 0
    assert "2025 Income: 100" in res_y.stdout
    assert "2025 Expenses: -40" in res_y.stdout
    assert "2025 Balance: 60" in res_y.stdout

    # CSV export
    res_csv = run_cmd(["summary", "-y", "2025", "-e", "csv"])
    assert res_csv.returncode == 0
    assert "Exported to:" in res_csv.stdout
    csv_path = config.DATA_ROOT / "processed" / "summary_2025.csv"
    assert csv_path.exists()
    # Check header
    content = csv_path.read_text().splitlines()
    assert content[0] == "field,value"


def test_cli_chart_ascii_and_graphical_exports(tmp_path: Path) -> None:
    """Test 'chart' ASCII, PNG, and SVG export as well as error case."""
    # Seed some data
    run_cmd(["add", "-t", "2025-05-20T00:00:00", "-c", "salary", "-a", "1000"])
    run_cmd(["add", "-t", "2025-05-20T00:00:00", "-c", "rent", "-a", "-500"])

    # ASCII-only
    res_a = run_cmd(["chart", "--start", "2025-01-01", "--end", "2026-01-01"])
    assert res_a.returncode == 0
    assert "Income:" in res_a.stdout
    assert "salary" in res_a.stdout
    assert "Expenses:" in res_a.stdout
    assert "rent" in res_a.stdout

    # PNG export
    res_png = run_cmd(
        ["chart", "--start", "2025-01-01", "--end", "2026-01-01", "--png"]
    )
    assert res_png.returncode == 0
    assert "Graphical chart saved to:" in res_png.stdout
    png_file = (
        config.DATA_ROOT
        / "processed"
        / "charts"
        / "chart_2025-01-01_to_2026-01-01.png"
    )
    assert png_file.exists()

    # SVG export
    res_svg = run_cmd(
        ["chart", "--start", "2025-01-01", "--end", "2026-01-01", "--svg"]
    )
    assert res_svg.returncode == 0
    assert "Graphical chart saved to:" in res_svg.stdout
    svg_file = (
        config.DATA_ROOT
        / "processed"
        / "charts"
        / "chart_2025-01-01_to_2026-01-01.svg"
    )
    assert svg_file.exists()

    # Invalid date format
    res_err = run_cmd(["chart", "--start", "2025-13-01", "--end", "bad"])
    assert res_err.returncode == 1
    assert "Invalid date format" in res_err.stderr


def test_cli_budget_commands_and_validation() -> None:
    """Test budget add, list empty, list populated and invalid limit."""
    # Empty list
    res_empty = run_cmd(["budget", "list"])
    assert res_empty.returncode == 0
    assert "No budgets defined." in res_empty.stdout

    # Add budget
    res_add = run_cmd(["budget", "add", "-c", "rent", "-l", "1000"])
    assert res_add.returncode == 0
    assert "Set budget: rent -> 1000" in res_add.stdout

    # List shows it
    res_list = run_cmd(["budget", "list"])
    assert res_list.returncode == 0
    assert "rent: 1000" in res_list.stdout

    # Invalid limit
    res_bad = run_cmd(["budget", "add", "-c", "food", "-l", "NaN"])
    assert res_bad.returncode == 1
    assert "Invalid limit" in res_bad.stderr


def test_cli_budget_warning_on_overspend() -> None:
    """Adding beyond the budget limit emits a warning."""
    run_cmd(["budget", "add", "-c", "groceries", "-l", "50"])
    run_cmd(["add", "-c", "groceries", "-a", "-30"])
    res_warn = run_cmd(["add", "-c", "groceries", "-a", "-25"])
    assert res_warn.returncode == 0
    assert "Warning: budget for 'groceries' exceeded" in res_warn.stdout
