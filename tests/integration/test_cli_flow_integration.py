#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
End-to-end integration tests for the CLI.

Verifies that the `add`, `list`, `balance`, `summary`, and `chart` commands
operate correctly against a temporary DATA_ROOT.
"""

import subprocess
import os
import sys
from pathlib import Path

import pytest

from budgetmanager import config


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> None:
    """
    Override DATA_ROOT for all CLI tests to use a temporary directory.
    """
    monkeypatch.setenv("BUDGETMANAGER_DATA_ROOT", str(tmp_path))
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    """
    Helper function to invoke the CLI.

    Args:
        args (list[str]): Command-line arguments for the CLI.

    Returns:
        subprocess.CompletedProcess[str]: Completed process containing stdout and stderr.
    """
    cmd = [sys.executable, "-m", "budgetmanager.cli.cli"] + args
    env = os.environ.copy()
    env["BUDGETMANAGER_DATA_ROOT"] = str(config.DATA_ROOT)
    return subprocess.run(cmd, env=env, capture_output=True, text=True)


def test_cli_add_and_list(tmp_path: Path) -> None:
    """
    Test that the 'add' command creates an entry and 'list' displays it.
    """
    result_add = run_cmd(["add", "-c", "test", "-a", "10.00"])
    result_list = run_cmd(["list"])

    assert result_add.returncode == 0
    assert "test" in result_list.stdout


def test_cli_balance_and_summary(tmp_path: Path) -> None:
    """
    Test that the 'balance' and 'summary' commands return expected output.
    """
    run_cmd(["add", "-c", "foo", "-a", "20.00"])
    balance_result = run_cmd(["balance"])
    summary_result = run_cmd(["summary", "-y", "2025", "-m", "1"])

    assert "Balance:" in balance_result.stdout
    assert "2025-01 Income" in summary_result.stdout


def test_cli_budget_add_and_list(tmp_path: Path) -> None:
    """
    Test the 'budget add' and 'budget list' commands work end-to-end.
    """
    result_add = run_cmd(["budget", "add", "-c", "rent", "-l", "1000"])
    assert result_add.returncode == 0
    assert "Set budget: rent -> 1000" in result_add.stdout

    result_list = run_cmd(["budget", "list"])
    assert result_list.returncode == 0
    assert "rent: 1000" in result_list.stdout


def test_cli_budget_warning_on_overspend(tmp_path: Path) -> None:
    """
    Test that adding a transaction beyond the budget limit emits a warning.
    """
    run_cmd(["budget", "add", "-c", "groceries", "-l", "50"])
    run_cmd(["add", "-c", "groceries", "-a", "-30"])
    result_warn = run_cmd(["add", "-c", "groceries", "-a", "-25"])

    assert result_warn.returncode == 0
    assert "Warning: budget for 'groceries' exceeded" in result_warn.stdout


def test_cli_chart_ascii_only(tmp_path: Path) -> None:
    """
    Test that the 'chart' command prints ASCII bars for Income and Expenses.
    """
    run_cmd(["add", "-t", "2025-05-20", "-c", "salary", "-a", "1000"])
    run_cmd(["add", "-t", "2025-05-20", "-c", "rent", "-a", "-500"])

    result = run_cmd([
        "chart",
        "--start", "2025-01-01",
        "--end",   "2026-01-01"
    ])

    assert result.returncode == 0
    assert "Income:" in result.stdout
    assert "salary" in result.stdout
    assert "Expenses:" in result.stdout
    assert "rent" in result.stdout


def test_cli_chart_with_png_export(tmp_path: Path) -> None:
    """
    Test that the 'chart --png' command saves a PNG file and reports its path.
    """
    run_cmd(["add", "-t", "2025-05-20", "-c", "bonus", "-a", "200"])
    run_cmd(["add", "-t", "2025-05-20", "-c", "groceries", "-a", "-100"])

    result = run_cmd([
        "chart",
        "--start", "2025-01-01",
        "--end",   "2026-01-01",
        "--png"
    ])

    assert result.returncode == 0
    assert "Graphical chart saved to:" in result.stdout

    chart_file = (
        config.DATA_ROOT
        / "processed"
        / "charts"
        / "chart_2025-01-01_to_2026-01-01.png"
    )
    assert chart_file.exists()
