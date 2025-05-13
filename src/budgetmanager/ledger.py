#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for managing a collection of financial transactions via a ledger.

This module defines the Ledger class, which holds multiple Transaction
instances and provides methods to add, remove, filter, and compute balances.
"""
# Standard library imports
from decimal import Decimal
from typing import List, Optional

# Local module imports
from .transaction import Transaction
from .utils.timestamp import Timestamp


class Ledger:
    """
    Represents a financial ledger containing multiple transactions.

    Attributes:
        transactions (List[Transaction]): List of transactions in the ledger.
    """

    def __init__(self, transactions: Optional[List[Transaction]] = None) -> None:
        """
        Initialize a Ledger instance with optional transactions.

        Args:
            transactions (Optional[List[Transaction]]): Initial transactions.
                Defaults to an empty list.
        """
        # Copy initial list to avoid Seiteneffekte
        self.transactions: List[Transaction] = (
            transactions.copy() if transactions else []
        )

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add a transaction to the ledger.

        Args:
            transaction (Transaction): The transaction to add.

        Raises:
            TypeError: If transaction is not a Transaction instance.

        Examples:
            >>> ledger = Ledger()
            >>> t = Transaction(...)  # Beispiel-Instanz
            >>> ledger.add_transaction(t)
        """
        if not isinstance(transaction, Transaction):
            raise TypeError(
                f"Expected Transaction, got {type(transaction).__name__}"
            )
        self.transactions.append(transaction)

    def remove_transaction(self, transaction: Transaction) -> None:
        """
        Remove a transaction from the ledger.

        Args:
            transaction (Transaction): The transaction to remove.

        Raises:
            ValueError: If the transaction is not found.

        Examples:
            >>> ledger.remove_transaction(t)
        """
        try:
            self.transactions.remove(transaction)
        except ValueError as e:
            raise ValueError("Transaction not found in ledger") from e

    def get_balance(self) -> Decimal:
        """
        Calculate the net balance of all transactions.

        Returns:
            Decimal: Sum of all transaction amounts.

        Examples:
            >>> ledger.get_balance()
        """
        return sum((t.amount for t in self.transactions), Decimal("0"))

    def total_income(self) -> Decimal:
        """
        Compute the total income (positive amounts).

        Returns:
            Decimal: Sum of positive transaction amounts.
        """
        return sum(
            (t.amount for t in self.transactions if t.is_income()),
            Decimal("0")
        )

    def total_expenses(self) -> Decimal:
        """
        Compute the total expenses (negative amounts).

        Returns:
            Decimal: Sum of negative transaction amounts.
        """
        return sum(
            (t.amount for t in self.transactions if t.is_expense()),
            Decimal("0")
        )

    def filter_by_category(self, category: str) -> List[Transaction]:
        """
        Filter transactions by category.

        Args:
            category (str): Category to filter by.

        Returns:
            List[Transaction]: Transactions matching the category.
        """
        return [t for t in self.transactions if t.category == category]

    def filter_by_date_range(
        self, start: Timestamp, end: Timestamp
    ) -> List[Transaction]:
        """
        Filter transactions between start and end timestamps (inclusive).

        Args:
            start (Timestamp): Start timestamp.
            end (Timestamp): End timestamp.

        Returns:
            List[Transaction]: Transactions in the specified range.
        """
        return [
            t for t in self.transactions
            if start <= t.timestamp <= end
        ]

    def __repr__(self) -> str:
        """
        Return an unambiguous representation of the Ledger.

        Returns:
            str: Representation including all transactions.
        """
        return f"{self.__class__.__name__}(transactions={self.transactions!r})"

    def __str__(self) -> str:
        """
        Return a user-friendly string of the ledger contents.

        Returns:
            str: Each transaction on a new line.
        """
        return "\n".join(str(t) for t in self.transactions)
