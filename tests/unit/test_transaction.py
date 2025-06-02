#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Unit tests for the Transaction class in budgetmanager.transaction.
"""

import pytest
from decimal import Decimal

from budgetmanager.core.transaction import Transaction
from budgetmanager.utils.timestamp import Timestamp


@pytest.fixture
def sample_ts() -> Timestamp:
    """Return a Timestamp for 2021-05-12 14:30:00."""
    return Timestamp.from_components(2021, 5, 12, 14, 30, 0)


@pytest.fixture
def txn(sample_ts) -> Transaction:
    """Return a sample income transaction."""
    return Transaction(
        timestamp=sample_ts,
        category="salary",
        amount=Decimal("1000.00"),
        description="Monthly salary",
    )


def test_repr_contains_class_and_fields(txn):
    """__repr__ should include class name and all field values."""
    repr_str = repr(txn)
    assert repr_str.startswith("Transaction(")
    assert "category='salary'" in repr_str
    assert "amount=Decimal('1000.00')" in repr_str
    assert "description='Monthly salary'" in repr_str


def test_str_format(txn, sample_ts):
    """__str__ must match '<ISO> | category: amount (description)'."""
    expected = (
        f"{sample_ts.to_isoformat()} | salary: 1000.00 " f"(Monthly salary)"
    )
    assert str(txn) == expected


def test_to_dict_from_dict_roundtrip(txn):
    """Converting to dict and back yields an equal Transaction."""
    d = txn.to_dict()
    txn2 = Transaction.from_dict(d)
    assert txn2 == txn


def test_from_dict_with_decimal_amount(sample_ts):
    """from_dict must accept Decimal for 'amount' without error."""
    data = {
        "timestamp": sample_ts.to_isoformat(),
        "category": "gift",
        "amount": Decimal("50.50"),
        "description": "Birthday gift",
    }
    txn2 = Transaction.from_dict(data)
    assert txn2.category == "gift"
    assert txn2.amount == Decimal("50.50")


def test_is_income_and_is_expense():
    """is_income/is_expense are based on sign of amount."""
    t_pos = Transaction(
        timestamp=Timestamp.from_components(2020, 1, 1),
        category="test",
        amount=Decimal("10"),
        description="",
    )
    t_neg = Transaction(
        timestamp=Timestamp.from_components(2020, 1, 1),
        category="test",
        amount=Decimal("-5"),
        description="",
    )
    assert t_pos.is_income() and not t_pos.is_expense()
    assert t_neg.is_expense() and not t_neg.is_income()


def test_bool():
    """__bool__ is False only for amount == 0."""
    zero = Transaction(
        timestamp=Timestamp.from_components(2020, 1, 1),
        category="foo",
        amount=Decimal("0"),
        description="",
    )
    assert not zero
    non_zero = Transaction(
        timestamp=Timestamp.from_components(2020, 1, 1),
        category="foo",
        amount=Decimal("1"),
        description="",
    )
    assert non_zero


def test_hash_and_set_behavior(txn, sample_ts):
    """Transactions must be hashable and compare equal in sets."""
    txn_clone = Transaction(
        timestamp=sample_ts,
        category="salary",
        amount=Decimal("1000.00"),
        description="Monthly salary",
    )
    s = {txn}
    assert txn_clone in s


def test_equality_and_inequality(txn, sample_ts):
    """__eq__ must only be True for identical field values."""
    txn_same = Transaction(
        timestamp=sample_ts,
        category="salary",
        amount=Decimal("1000.00"),
        description="Monthly salary",
    )
    txn_diff = Transaction(
        timestamp=sample_ts,
        category="rent",
        amount=Decimal("500"),
        description="Rent",
    )
    assert txn == txn_same
    assert txn != txn_diff
    assert not (txn != txn_same)


def test_ordering(sample_ts):
    """total_ordering uses amount for <, <=, >, >=."""
    low = Transaction(sample_ts, "a", Decimal("100"), "")
    high = Transaction(sample_ts, "b", Decimal("200"), "")
    assert low < high
    assert low <= high
    assert high > low
    assert high >= low
    # equal amounts
    low2 = Transaction(sample_ts, "c", Decimal("100"), "")
    assert not (low < low2)
    assert low <= low2


def test_add_transaction_and_scalar(txn, sample_ts):
    """__add__/__radd__ with Transaction and numeric types."""
    bonus = Transaction(sample_ts, "bonus", Decimal("200"), "")
    assert txn + bonus == Decimal("1200.00")
    assert txn + Decimal("50") == Decimal("1050.00")
    assert txn + 50 == Decimal("1050.00")
    assert pytest.approx(txn + 50.5) == Decimal("1050.50")
    assert Decimal("20") + txn == Decimal("1020.00")


def test_add_invalid_type(txn):
    """Adding unsupported type must raise TypeError."""
    with pytest.raises(TypeError):
        _ = txn + "invalid"


def test_sub_transaction_and_scalar(txn, sample_ts):
    """__sub__/__rsub__ with Transaction and numeric types."""
    fee = Transaction(sample_ts, "fee", Decimal("100"), "")
    assert txn - fee == Decimal("900.00")
    assert txn - Decimal("100") == Decimal("900.00")
    assert txn - 100 == Decimal("900.00")
    assert pytest.approx(txn - 50.5) == Decimal("949.50")
    assert 1200 - txn == Decimal("200.00")


def test_sub_invalid_type(txn):
    """Subtracting unsupported type must raise TypeError."""
    with pytest.raises(TypeError):
        _ = txn - [1, 2, 3]


def test_mul_transaction_and_scalar(txn, sample_ts):
    """__mul__/__rmul__ with Transaction and numeric types."""
    two = Transaction(sample_ts, "x", Decimal("2"), "")
    assert txn * two == Decimal("2000.00")
    assert txn * Decimal("2") == Decimal("2000.00")
    assert txn * 2 == Decimal("2000.00")
    assert pytest.approx(txn * 2.5) == Decimal("2500.00")
    assert 3 * txn == Decimal("3000.00")


def test_mul_invalid_type(txn):
    """Multiplying unsupported type must raise TypeError."""
    with pytest.raises(TypeError):
        _ = txn * None


def test_truediv_transaction_and_scalar(txn, sample_ts):
    """__truediv__/__rtruediv__ with Transaction and numeric types."""
    half = Transaction(sample_ts, "half", Decimal("2"), "")
    assert txn / half == Decimal("500.00")
    assert txn / Decimal("2") == Decimal("500.00")
    assert txn / 2 == Decimal("500.00")
    assert pytest.approx(txn / 4.0) == Decimal("250.00")
    assert 2000 / txn == Decimal("2.00")


def test_division_by_zero(sample_ts):
    """
    Division by zero (transaction or scalar) must raise ZeroDivisionError.
    """
    zero_txn = Transaction(sample_ts, "z", Decimal("0"), "")
    t = Transaction(sample_ts, "t", Decimal("100"), "")
    with pytest.raises(ZeroDivisionError):
        _ = t / zero_txn
    with pytest.raises(ZeroDivisionError):
        _ = t / 0
    with pytest.raises(ZeroDivisionError):
        _ = t / Decimal("0")
    with pytest.raises(ZeroDivisionError):
        _ = 100 / zero_txn


def test_truediv_invalid_type(txn):
    """Dividing unsupported type must raise TypeError."""
    with pytest.raises(TypeError):
        _ = txn / "invalid"
    with pytest.raises(TypeError):
        _ = "invalid" / txn


def test_from_dict_missing_keys(sample_ts):
    """
    from_dict without 'description' or 'amount' or 'category' raises KeyError.
    """
    incomplete = {
        "timestamp": sample_ts.to_isoformat(),
        "category": "x",
        "amount": "1",
    }
    with pytest.raises(KeyError):
        Transaction.from_dict(incomplete)


def test_from_dict_invalid_timestamp(sample_ts):
    """Invalid timestamp string must raise ValueError."""
    bad_ts = {
        "timestamp": "not-a-timestamp",
        "category": "x",
        "amount": "1",
        "description": "d",
    }
    with pytest.raises(ValueError):
        Transaction.from_dict(bad_ts)


def test_from_dict_invalid_amount(sample_ts):
    """Non-numeric amount must raise ValueError."""
    bad_amt = {
        "timestamp": sample_ts.to_isoformat(),
        "category": "x",
        "amount": "abc",
        "description": "d",
    }
    with pytest.raises(ValueError):
        Transaction.from_dict(bad_amt)
