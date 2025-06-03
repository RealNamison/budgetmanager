#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Transaction module for budget entries.

This module defines the `Transaction` class, which represents a single
financial transaction with an optional transaction_id, timestamp, category,
amount and description.
"""

from __future__ import annotations
from decimal import Decimal, InvalidOperation
from typing import Any

from ..utils.timestamp import Timestamp


class Transaction:
    """Represents a financial transaction.

    Attributes:
        transaction_id (int | None): Optional database ID of the transaction.
        timestamp (Timestamp): Date and time of the transaction.
        category (str): Category or tag of the transaction.
        amount (Decimal): Positive for income, negative for expense.
        description (str): Short human-readable description.
    """

    def __init__(
        self,
        timestamp: Timestamp,
        category: str,
        amount: Decimal,
        description: str,
        transaction_id: int | None = None,
    ) -> None:
        """Initialize a Transaction instance.

        Args:
            timestamp (Timestamp): Date and time of the transaction.
            category (str): Category or tag of the transaction.
            amount (Decimal): Positive for income, negative for expense.
            description (str): Short human-readable description.
            transaction_id (int | None): Optional database ID.
                Defaults to None.
        """
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.category = category
        self.amount = amount
        self.description = description

    def __repr__(self) -> str:
        """Return unambiguous representation of Transaction."""
        return (
            "Transaction("
            f"transaction_id={self.transaction_id!r}, "
            f"timestamp={self.timestamp!r}, "
            f"category={self.category!r}, "
            f"amount={self.amount!r}, "
            f"description={self.description!r}"
            ")"
        )

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        id_part = (
            f"[#{self.transaction_id}] | "
            if self.transaction_id is not None
            else "[# - ] | "
        )
        return (
            f"{id_part}{self.timestamp.to_isoformat()} | "
            f"{self.category}: {self.amount} "
            f"({self.description})"
        )

    def __bool__(self) -> bool:
        """Return True if the amount is non-zero."""
        return self.amount != Decimal("0")

    def __hash__(self) -> int:
        """Compute hash based on all immutable attributes."""
        return hash(
            (
                self.transaction_id,
                self.timestamp.to_isoformat(),
                self.category,
                self.amount,
                self.description,
            )
        )

    def __eq__(self, other: object) -> bool:
        """Check equality of two Transaction instances."""
        if not isinstance(other, Transaction):
            return NotImplemented
        return (
            self.transaction_id == other.transaction_id
            and self.timestamp == other.timestamp
            and self.category == other.category
            and self.amount == other.amount
            and self.description == other.description
        )

    def __lt__(self, other: object) -> bool:
        """Amount-based less-than comparison."""
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.amount < other.amount

    def __le__(self, other: object) -> bool:
        """Amount-based less-or-equal comparison."""
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.amount <= other.amount

    def __gt__(self, other: object) -> bool:
        """Amount-based greater-than comparison."""
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.amount > other.amount

    def __ge__(self, other: object) -> bool:
        """Amount-based greater-or-equal comparison."""
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.amount >= other.amount

    def __add__(self, other: Any) -> Decimal:
        """Add Transaction or scalar to this transaction's amount.

        Args:
            other (Transaction | int | float | Decimal):
                If Transaction: returns sum of both amounts.
                If numeric: returns this transaction's amount plus the number.

        Returns:
            Decimal: Result of the addition.

        Raises:
            TypeError: If `other` is not Transaction, int, float or Decimal.
        """
        # Transaction + Transaction → sum of amounts
        if isinstance(other, Transaction):
            return self.amount + other.amount

        # Transaction + scalar → add to this amount
        if isinstance(other, (int, float, Decimal)):
            try:
                scalar = Decimal(str(other))
            except (InvalidOperation, ValueError) as e:
                raise TypeError(f"Cannot convert {other!r} to Decimal") from e
            return self.amount + scalar

        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other: Any) -> Decimal:
        """Subtract Transaction or scalar from this transaction's amount.

        Args:
            other (Transaction | int | float | Decimal):
                If Transaction: returns this.amount minus other.amount.
                If numeric: returns this.amount minus the given number.

        Returns:
            Decimal: Result of the subtraction.

        Raises:
            TypeError: If `other` is not Transaction, int, float or Decimal,
                or if conversion to Decimal fails.
        """
        # Transaction - Transaction → difference of amounts
        if isinstance(other, Transaction):
            return self.amount - other.amount

        # Transaction - scalar → subtract scalar from this amount
        if isinstance(other, (int, float, Decimal)):
            try:
                scalar = Decimal(str(other))
            except (InvalidOperation, ValueError) as e:
                raise TypeError(f"Cannot convert {other!r} to Decimal") from e
            return self.amount - scalar

        return NotImplemented

    def __rsub__(self, other: Any) -> Decimal:
        """
        Support scalar - Transaction → number minus this transaction's amount.

        Args:
            other (int | float | Decimal): Left-hand scalar operand.

        Returns:
            Decimal: Result of the subtraction.

        Raises:
            TypeError: If `other` is not int, float or Decimal,
                or if conversion to Decimal fails.
        """
        if isinstance(other, (int, float, Decimal)):
            try:
                scalar = Decimal(str(other))
            except (InvalidOperation, ValueError) as e:
                raise TypeError(f"Cannot convert {other!r} to Decimal") from e
            return scalar - self.amount

        return NotImplemented

    def __mul__(self, other: Any) -> Decimal:
        """Multiply this transaction's amount by a Transaction or scalar.

        Args:
            other (Transaction | int | float | Decimal):
                If Transaction: returns product of both amounts.
                If numeric: returns this transaction's amount times the number.

        Returns:
            Decimal: Result of the multiplication.

        Raises:
            TypeError: If `other` is not Transaction, int, float or Decimal,
                or if conversion to Decimal fails.
        """
        # Transaction * Transaction → product of amounts
        if isinstance(other, Transaction):
            return self.amount * other.amount

        # Transaction * scalar → scale this amount
        if isinstance(other, (int, float, Decimal)):
            try:
                factor = Decimal(str(other))
            except (InvalidOperation, ValueError) as e:
                raise TypeError(f"Cannot convert {other!r} to Decimal") from e
            return self.amount * factor

        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> Decimal:
        """Divide this transaction's amount by a Transaction or scalar.

        Args:
            other (Transaction | int | float | Decimal):
                If Transaction: returns this.amount divided by other.amount.
                If numeric: returns this.amount divided by the number.

        Returns:
            Decimal: Result of the division.

        Raises:
            TypeError: If `other` is not Transaction, int, float or Decimal,
                or if conversion to Decimal fails.
            ZeroDivisionError: If division by zero is attempted.
        """
        # Transaction / Transaction → ratio of amounts
        if isinstance(other, Transaction):
            if other.amount == Decimal("0"):
                raise ZeroDivisionError("Division by zero Transaction amount")
            return self.amount / other.amount

        # Transaction / scalar → divide amount by scalar
        if isinstance(other, (int, float, Decimal)):
            try:
                divisor = Decimal(str(other))
            except (InvalidOperation, ValueError) as e:
                raise TypeError(f"Cannot convert {other!r} to Decimal") from e
            if divisor == Decimal("0"):
                raise ZeroDivisionError("Division by zero")
            return self.amount / divisor

        return NotImplemented

    def __rtruediv__(self, other: Any) -> Decimal:
        """
        Support scalar / Transaction
        → number divided by this transaction's amount.

        Args:
            other (int | float | Decimal): Left-hand scalar operand.

        Returns:
            Decimal: Result of the division.

        Raises:
            TypeError: If `other` is not int, float or Decimal,
                or if conversion to Decimal fails.
            ZeroDivisionError: If this transaction's amount is zero.
        """
        if isinstance(other, (int, float, Decimal)):
            try:
                dividend = Decimal(str(other))
            except (InvalidOperation, ValueError) as e:
                raise TypeError(f"Cannot convert {other!r} to Decimal") from e
            if self.amount == Decimal("0"):
                raise ZeroDivisionError("Division by zero Transaction amount")
            return dividend / self.amount

        return NotImplemented

    def to_dict(self) -> dict[str, Any]:
        """Serialize Transaction to a dict with JSON-friendly types.

        Returns:
            dict: {
                "transaction_id": int | None,
                "timestamp": str (ISO format),
                "category": str,
                "amount": str,
                "description": str
            }
        """
        output: dict[str, Any] = {
            "timestamp": self.timestamp.to_isoformat(),
            "category": self.category,
            "amount": str(self.amount),
            "description": self.description,
        }
        if self.transaction_id is not None:
            output["transaction_id"] = self.transaction_id
        return output

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Transaction:
        """Create Transaction from dict produced by `to_dict`.

        Args:
            data (dict): {
                "transaction_id": int | None (optional),
                "timestamp": str (ISO format),
                "category": str,
                "amount": str or Decimal,
                "description": str
            }

        Returns:
            Transaction: New instance.

        Raises:
            KeyError: If a required key is missing.
            ValueError: If timestamp, amount or transaction_id
                cannot be parsed.
        """
        # transaction_id parsing (optional)
        tx_id: int | None
        if "transaction_id" in data:
            try:
                tx_id = int(data["transaction_id"])
            except (TypeError, ValueError) as e:
                raise ValueError(
                    f"Invalid transaction_id: {data.get('transaction_id')}"
                ) from e
        else:
            tx_id = None

        # Timestamp parsing
        try:
            ts = Timestamp.from_isoformat(data["timestamp"])
        except Exception as e:
            raise ValueError(
                f"Invalid timestamp: {data.get('timestamp')}"
            ) from e

        # Amount parsing
        try:
            amt = (
                data["amount"]
                if isinstance(data["amount"], Decimal)
                else Decimal(data["amount"])
            )
        except (InvalidOperation, TypeError) as e:
            raise ValueError(f"Invalid amount: {data.get('amount')}") from e

        return cls(
            timestamp=ts,
            category=data["category"],
            amount=amt,
            description=data["description"],
            transaction_id=tx_id,
        )

    def is_income(self) -> bool:
        """Check whether this transaction is income (amount > 0)."""
        return self.amount > Decimal("0")

    def is_expense(self) -> bool:
        """Check whether this transaction is an expense (amount < 0)."""
        return self.amount < Decimal("0")
