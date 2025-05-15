#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Integration tests for Transaction and Ledger.

Verifies that transactions can be added to a Ledger, filtered by
category, and that the ledger balance is computed correctly.
"""

from decimal import Decimal
import pytest

from budgetmanager.core.transaction import Transaction  # :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}
from budgetmanager.core.ledger import Ledger  # :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}
from budgetmanager.utils.timestamp import Timestamp  # :contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}


def test_add_filter_and_balance() -> None:
    """
    Test that Transaction instances are collected in a Ledger,
    can be filtered by category, and that the balance is calculated.

    Raises:
        AssertionError: If filtering or balance calculation fails.
    """
    # Arrange: create two transactions and an empty ledger
    t1 = Transaction(
        timestamp=Timestamp.from_components(2025, 1, 1),
        category="income",
        amount=Decimal("100.00"),
        description="Salary"
    )
    t2 = Transaction(
        timestamp=Timestamp.from_components(2025, 1, 5),
        category="expense",
        amount=Decimal("-30.00"),
        description="Groceries"
    )
    ledger = Ledger()

    # Act: add transactions, filter by income, compute balance
    ledger.add_transaction(t1)
    ledger.add_transaction(t2)
    income_transactions = ledger.filter_by_category("income")
    balance = ledger.get_balance()

    # Assert: only the income transaction is returned and balance is correct
    assert income_transactions == [t1]
    assert balance == Decimal("70.00")
