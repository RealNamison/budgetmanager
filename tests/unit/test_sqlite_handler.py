#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Unit tests for sqlite_handler.py using a temporary file-based SQLite database.
"""

import pytest
from pathlib import Path
from decimal import Decimal

from budgetmanager.file.sqlite_handler import SQLiteHandler
from budgetmanager.core.transaction import Transaction
from budgetmanager.core.budget import Budget
from budgetmanager.utils.timestamp import Timestamp


@pytest.fixture(autouse=True)
def patch_create_directory(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Disable actual directory creation in FileHandler to avoid FS side effects.
    """
    monkeypatch.setattr(
        'budgetmanager.file.file_handler.FileHandler.create_directory',
        lambda path: Path(path),
        raising=True
    )


@pytest.fixture
def handler(tmp_path: Path) -> SQLiteHandler:
    """
    Provides a SQLiteHandler using a temporary file database.
    The _ensure_directory step is patched to do nothing.
    """
    db_file = tmp_path / "test.db"
    return SQLiteHandler(db_path=db_file)


def test_empty_db_returns_no_transactions(handler: SQLiteHandler) -> None:
    """get_all_transactions() should be empty on a fresh DB file."""
    assert handler.get_all_transactions() == []


def test_add_and_get_transaction(handler: SQLiteHandler) -> None:
    """
    add_transaction() followed by get_all_transactions()
    returns the inserted tx.
    """
    ts = Timestamp.from_components(2025, 5, 22, 12, 0, 0)
    tx = Transaction(
        timestamp=ts,
        category="test",
        amount=Decimal("9.99"),
        description="Lunch"
    )
    handler.add_transaction(tx)
    txs = handler.get_all_transactions()
    assert txs == [tx]


def test_remove_transaction(handler: SQLiteHandler) -> None:
    """
    remove_transaction() deletes by ID.
    First insert two transactions, remove the first (ID=1),
    only second remains.
    """
    ts = Timestamp.from_components(2025, 5, 22)
    t1 = Transaction(ts, "a", Decimal("1.00"), "one")
    t2 = Transaction(ts, "b", Decimal("2.00"), "two")
    handler.add_transaction(t1)
    handler.add_transaction(t2)
    handler.remove_transaction(1)
    remaining = handler.get_all_transactions()
    assert remaining == [t2]


def test_budget_crud_operations(handler: SQLiteHandler) -> None:
    """
    Test add_budget, get_budgets, update_budget and remove_budget flow.
    """
    b1 = Budget(category="food", limit=Decimal("100"))
    # initially no budgets
    assert handler.get_budgets() == []

    # insert new budget
    handler.add_budget(b1)
    budgets = handler.get_budgets()
    assert budgets == [b1]

    # add_budget on existing category should update
    b1_updated = Budget(category="food", limit=Decimal("150"))
    handler.add_budget(b1_updated)
    assert handler.get_budgets() == [b1_updated]

    # remove_budget()
    handler.remove_budget("food")
    assert handler.get_budgets() == []
