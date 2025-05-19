#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
End-to-end integration tests for the CLI.

Verifies that the `add`, `list`, `balance`, and `summary` commands
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
    # Ensure the CLI uses the pytest‐tmp_path as DATA_ROOT
    env = os.environ.copy()
    env["BUDGETMANAGER_DATA_ROOT"] = str(config.DATA_ROOT)
    return subprocess.run(cmd, env=env, capture_output=True, text=True)


def test_cli_add_and_list(tmp_path: Path) -> None:
    """
    Test that the 'add' command creates an entry and 'list' displays it.
    """
    # Act: add a new entry and then list all entries
    result_add = run_cmd(["add", "-c", "test", "-a", "10.00"])
    result_list = run_cmd(["list"])

    # Assert: ensure the add command succeeded and the entry is listed
    assert result_add.returncode == 0
    assert "test" in result_list.stdout


def test_cli_balance_and_summary(tmp_path: Path) -> None:
    """
    Test that the 'balance' and 'summary' commands return expected output.
    """
    # Act: add an entry, then retrieve balance and summary
    run_cmd(["add", "-c", "foo", "-a", "20.00"])
    balance_result = run_cmd(["balance"])
    summary_result = run_cmd(["summary", "-y", "2025", "-m", "1"])

    # Assert: verify balance and summary outputs contain expected markers
    assert "Balance:" in balance_result.stdout
    assert "2025-01 Income" in summary_result.stdout


def test_cli_budget_add_and_list(tmp_path: Path) -> None:
    """
    Test the 'budget add' and 'budget list' commands work end-to-end.
    """
    # Add budget
    result_add = run_cmd(["budget", "add", "-c", "rent", "-l", "1000"])
    assert result_add.returncode == 0
    assert "Added budget: rent -> 1000" in result_add.stdout

    # List all budgets
    result_list = run_cmd(["budget", "list"])
    assert result_list.returncode == 0
    assert "rent: 1000" in result_list.stdout


def test_cli_budget_warning_on_overspend(tmp_path: Path) -> None:
    """
    Test that adding a transaction beyond the budget limit emits a warning.
    """
    # 1) Set budget
    run_cmd(["budget", "add", "-c", "groceries", "-l", "50"])
    # 2) Add 2 expenses, with amount < -50
    run_cmd(["add", "-c", "groceries", "-a", "-30"])
    result_warn = run_cmd(["add", "-c", "groceries", "-a", "-25"])

    # Expect warning and still exit code 0 from CLI
    assert result_warn.returncode == 0
    assert "Warning: budget for 'groceries' exceeded (55 > 50)" in result_warn.stdout
