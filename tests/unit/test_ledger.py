#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Unit tests for the Ledger class in budgetmanager.ledger.

This module uses pytest to verify all functionality of the Ledger class,
including initialization, transaction management, sequence protocol,
equality, copying, and string representation.
"""

import pytest
from decimal import Decimal
from copy import copy, deepcopy

from budgetmanager.core.ledger import Ledger
from budgetmanager.core.transaction import Transaction
from budgetmanager.utils.timestamp import Timestamp


def make_tx(year: int,
            month: int,
            day: int,
            hour: int,
            minute: int,
            second: int,
            category: str,
            amount: str,
            description: str) -> Transaction:
    """
    Helper to create a Transaction with ISO timestamp and Decimal amount.

    Args:
        year (int): Year component of timestamp.
        month (int): Month component of timestamp.
        day (int): Day component of timestamp.
        hour (int): Hour component of timestamp.
        minute (int): Minute component of timestamp.
        second (int): Second component of timestamp.
        category (str): Transaction category.
        amount (str): Decimal amount as string.
        description (str): Description of the transaction.

    Returns:
        Transaction: A new Transaction instance.

    Examples:
        >>> tx = make_tx(2025, 1, 1, 0, 0, 0, "income", "100.00", "Salary")
    """
    ts = Timestamp.from_components(year, month, day, hour, minute, second)
    return Transaction(ts, category, Decimal(amount), description)


@pytest.fixture
def sample_transactions():
    """
    Provide a list of sample Transaction objects for testing.

    Returns:
        list[Transaction]: A list of three sample transactions.
    """
    return [
        make_tx(2025, 1, 1, 0, 0, 0, "income",  "100.00", "Salary"),
        make_tx(2025, 1, 2, 0, 0, 0, "expense", "-50.00", "Groceries"),
        make_tx(2025, 1, 3, 0, 0, 0, "income",  "25.00",  "Gift"),
    ]


def test_init_empty():
    """
    Test that a newly initialized Ledger is empty and evaluates to False.
    """
    ledger = Ledger()
    assert len(ledger) == 0
    assert not ledger


def test_init_copy_of_list(sample_transactions):
    """
    Test that Ledger makes a copy of the initial list and is immune to
    external modifications.
    """
    orig = sample_transactions
    ledger = Ledger(orig)
    assert ledger.transactions == orig
    assert ledger.transactions is not orig
    orig.append(make_tx(2025, 1, 4, 0, 0, 0, "misc", "0", ""))
    assert len(ledger) == 3


def test_add_and_contains_and_len():
    """
    Test adding a transaction, membership __contains__, and __len__.
    """
    ledger = Ledger()
    tx = make_tx(2025, 1, 1, 0, 0, 0, "foo", "10", "desc")
    ledger.add_transaction(tx)
    assert tx in ledger
    assert len(ledger) == 1


def test_add_transaction_type_error():
    """
    Test that adding a non-Transaction raises TypeError.
    """
    ledger = Ledger()
    with pytest.raises(TypeError) as excinfo:
        ledger.add_transaction("not a tx")  # type: ignore
    assert "Expected Transaction" in str(excinfo.value)


def test_remove_transaction_and_value_error(sample_transactions):
    """
    Test removing a transaction and that removing again raises ValueError.
    """
    ledger = Ledger(sample_transactions.copy())
    tx = sample_transactions[1]
    ledger.remove_transaction(tx)
    assert tx not in ledger
    with pytest.raises(ValueError) as excinfo:
        ledger.remove_transaction(tx)
    assert "not found in ledger" in str(excinfo.value)


def test_get_balance_and_totals(sample_transactions):
    """
    Test get_balance, total_income, and total_expenses calculations.
    """
    ledger = Ledger(sample_transactions)
    assert ledger.get_balance() == Decimal("75.00")
    assert ledger.total_income() == Decimal("125.00")
    assert ledger.total_expenses() == Decimal("-50.00")


def test_filter_by_category_and_date_range(sample_transactions):
    """
    Test filtering transactions by category and by date range.
    """
    ledger = Ledger(sample_transactions)
    income_txs = ledger.filter_by_category("income")
    assert all(t.is_income() for t in income_txs)
    start = Timestamp.from_components(2025, 1, 2, 0, 0, 0)
    end = Timestamp.from_components(2025, 1, 3, 23, 59, 59)
    ranged = ledger.filter_by_date_range(start, end)
    assert len(ranged) == 2
    assert all(start <= t.timestamp <= end for t in ranged)


def test_to_dict_and_from_dict_roundtrip(sample_transactions):
    """
    Test that to_dict() produces the expected dict structure and that
    from_dict() reconstructs an equivalent Ledger.
    """
    ledger = Ledger(sample_transactions)
    data = ledger.to_dict()

    # verify structure
    assert isinstance(data, dict)
    assert "transactions" in data
    assert isinstance(data["transactions"], list)
    expected = [tx.to_dict() for tx in sample_transactions]
    assert data["transactions"] == expected

    # round-trip
    new_ledger = Ledger.from_dict(data)
    assert isinstance(new_ledger, Ledger)
    assert new_ledger == ledger
    assert new_ledger is not ledger
    for orig, fresh in zip(ledger.transactions, new_ledger.transactions):
        assert fresh == orig
        assert fresh is not orig


def test_from_dict_missing_key_raises_key_error():
    """
    Test that from_dict() raises KeyError when the 'transactions' key is missing.
    """
    with pytest.raises(KeyError):
        Ledger.from_dict({})


# noinspection PyTypeChecker
def test_from_dict_transactions_not_list_raises_type_error():
    """
    Test that from_dict() raises TypeError when 'transactions' is not a list.
    """
    with pytest.raises(TypeError):
        Ledger.from_dict({"transactions": "not a list"})


def test_from_dict_invalid_transaction_data_raises_value_error():
    """
    Test that from_dict() raises ValueError when a transaction dict is invalid.
    """
    bad_payload = {"transactions": [{"foo": "bar"}]}
    with pytest.raises(ValueError):
        Ledger.from_dict(bad_payload)


def test_iter_and_indexing_and_slice(sample_transactions):
    """
    Test __iter__, __getitem__ for index, and __getitem__ for slice.
    """
    ledger = Ledger(sample_transactions)
    assert list(iter(ledger)) == sample_transactions
    assert ledger[0] == sample_transactions[0]
    sub = ledger[1:3]
    assert isinstance(sub, Ledger)
    assert list(sub) == sample_transactions[1:3]


def test_delitem_index_and_slice(sample_transactions):
    """
    Test __delitem__ for index deletion and slice deletion.
    """
    ledger = Ledger(sample_transactions.copy())
    del ledger[0]
    assert len(ledger) == 2
    del ledger[0:1]
    assert len(ledger) == 1


def test_contains_and_bool(sample_transactions):
    """
    Test __contains__ membership and __bool__ truthiness.
    """
    ledger = Ledger(sample_transactions)
    assert sample_transactions[0] in ledger
    assert bool(ledger)
    empty = Ledger()
    assert not empty


def test_equality_and_add_iadd(sample_transactions):
    """
    Test __eq__, __add__, and __iadd__ operations.
    """
    l1 = Ledger(sample_transactions)
    l2 = Ledger(sample_transactions.copy())
    assert l1 == l2
    l2.transactions.reverse()
    assert not (l1 == l2)
    combined = Ledger([sample_transactions[0]]) + Ledger([sample_transactions[1]])
    assert isinstance(combined, Ledger)
    assert len(combined) == 2
    l3 = Ledger([sample_transactions[0]])
    l3 += Ledger([sample_transactions[1]])
    assert len(l3) == 2


def test_copy_and_deepcopy(sample_transactions):
    """
    Test shallow copy via copy.copy and deep copy via copy.deepcopy.
    """
    ledger = Ledger(sample_transactions)
    sc = copy(ledger)
    assert sc == ledger
    assert sc is not ledger
    assert sc.transactions is not ledger.transactions
    assert sc.transactions[0] is ledger.transactions[0]

    dc = deepcopy(ledger)
    assert dc == ledger
    assert dc is not ledger
    assert dc.transactions is not ledger.transactions
    assert dc.transactions[0] == ledger.transactions[0]
    assert dc.transactions[0] is not ledger.transactions[0]


def test_repr_and_str(sample_transactions):
    """
    Test __repr__ contains class name and transactions repr, and __str__
    produces one line per transaction with description.
    """
    ledger = Ledger(sample_transactions)
    r = repr(ledger)
    assert r.startswith("Ledger(")
    assert "Transaction(" in r

    s = str(ledger)
    lines = s.splitlines()
    assert len(lines) == len(sample_transactions)
    assert sample_transactions[0].description in lines[0]
