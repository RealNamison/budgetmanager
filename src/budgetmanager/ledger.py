#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for managing a collection of financial transactions via a ledger.

This module defines the Ledger class, which holds multiple Transaction
instances and provides methods to add, remove, filter, and compute balances,
as well as sequence protocol methods.
"""

from __future__ import annotations
from decimal import Decimal
from typing import Iterator
from copy import deepcopy

from .transaction import Transaction
from .utils.timestamp import Timestamp


class Ledger:
    """
    Represents a financial ledger containing multiple transactions.

    Attributes:
        transactions (list[Transaction]): List of transactions in the ledger.
    """

    def __init__(self, transactions: list[Transaction] | None = None) -> None:
        """
        Initialize a Ledger instance.

        Creates a new Ledger, optionally pre-populated with a list of
        Transaction objects. The provided list is copied to avoid
        side effects from external modifications.

        Args:
            transactions (list[Transaction] | None): Optional initial list
                of Transaction instances. If None, starts with an empty list.

        Examples:
            >>> ledger = Ledger()
            >>> initial_txs = [tx1, tx2]
            >>> ledger_with_txs = Ledger(initial_txs)
        """
        self.transactions: list[Transaction] = (
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
            >>> ledger.add_transaction(Transaction(...))
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
            >>> ledger.remove_transaction(some_tx)
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

    def filter_by_category(self, category: str) -> list[Transaction]:
        """
        Filter transactions by category.

        Args:
            category (str): Category to filter by.

        Returns:
            list[Transaction]: Transactions matching the category.
        """
        return [t for t in self.transactions if t.category == category]

    def filter_by_date_range(
        self, start: Timestamp, end: Timestamp
    ) -> list[Transaction]:
        """
        Filter transactions between start and end timestamps (inclusive).

        Args:
            start (Timestamp): Start timestamp.
            end (Timestamp): End timestamp.

        Returns:
            list[Transaction]: Transactions in the specified range.
        """
        return [
            t for t in self.transactions
            if start <= t.timestamp <= end
        ]

    def __len__(self) -> int:
        """
        Return the number of transactions in the ledger.

        Returns:
            int: Number of transactions.

        Examples:
            >>> len(ledger)
        """
        return len(self.transactions)

    def __iter__(self) -> Iterator[Transaction]:
        """
        Return an iterator over the transactions.

        Returns:
            Iterator[Transaction]: Iterator of transactions.

        Examples:
            >>> for tx in ledger:
        """
        return iter(self.transactions)

    def __getitem__(self, key: int | slice) -> Transaction | Ledger:
        """
        Retrieve transaction(s) by index or slice.

        If an integer index is provided, returns the single Transaction
        at that position. If a slice is provided, returns a new Ledger
        containing the sliced subset of transactions.

        Args:
            key (int | slice): Position index or slice object.

        Returns:
            Transaction | Ledger: Single Transaction for int key,
                or a new Ledger for slice key.

        Raises:
            IndexError: If the integer index is out of range.

        Examples:
            >>> tx = ledger[0]
            >>> sub_ledger = ledger[1:4]
        """
        if isinstance(key, slice):
            return Ledger(self.transactions[key])
        else:
            return self.transactions[key]

    def __delitem__(self, key: int | slice) -> None:
        """
        Delete transaction(s) by index or slice.

        Removes the transaction at the given index, or all transactions
        in the given slice, from this Ledger.

        Args:
            key (int | slice): Position index or slice object to delete.

        Raises:
            IndexError: If the integer index is out of range.

        Examples:
            >>> del ledger[2]
            >>> del ledger[0:2]
        """
        del self.transactions[key]

    def __contains__(self, item: Transaction) -> bool:
        """
        Check if a transaction is in the ledger.

        Args:
            item (Transaction): Transaction to check.

        Returns:
            bool: True if present, False otherwise.

        Examples:
            >>> tx in ledger
        """
        return item in self.transactions

    def __bool__(self) -> bool:
        """
        Determine the truth value of the ledger.

        A ledger is considered True if it contains any transactions.

        Returns:
            bool: True if the ledger has at least one transaction,
                False otherwise.

        Examples:
            >>> if ledger:
            ...     print("There are transactions")
        """
        return bool(self.transactions)

    def __eq__(self, other: object) -> bool:
        """
        Compare this ledger with another for equality.

        Two ledgers are equal if they are both Ledger instances
        and their transactions lists are identical in order and content.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if `other` is a Ledger with the same transactions,
                NotImplemented if `other` is not a Ledger.

        Examples:
            >>> ledger1 == ledger2
        """
        if not isinstance(other, Ledger):
            return NotImplemented
        return self.transactions == other.transactions

    def __add__(self, other: Ledger) -> Ledger:
        """
        Return a new ledger by concatenating two ledgers.

        The new ledger contains all transactions from this ledger
        followed by all transactions from `other`.

        Args:
            other (Ledger): The ledger to add.

        Returns:
            Ledger: A new Ledger instance with combined transactions,
                or NotImplemented if `other` is not a Ledger.

        Examples:
            >>> combined = ledger1 + ledger2
        """
        if not isinstance(other, Ledger):
            return NotImplemented
        return Ledger(self.transactions + other.transactions)

    def __iadd__(self, other: Ledger) -> Ledger:
        """
        In-place addition of another ledger's transactions.

        Extends this ledger's transactions list by those in `other`.

        Args:
            other (Ledger): The ledger whose transactions to append.

        Returns:
            Ledger: This ledger after appending, or NotImplemented
                if `other` is not a Ledger.

        Examples:
            >>> ledger1 += ledger2
        """
        if not isinstance(other, Ledger):
            return NotImplemented
        self.transactions.extend(other.transactions)
        return self

    def __copy__(self) -> Ledger:
        """
        Create a shallow copy of the ledger.

        Returns:
            Ledger: A new Ledger instance with a shallow copy of the transactions list.

        Examples:
            >>> from copy import copy
            >>> new_ledger = copy(ledger)
        """
        return Ledger(self.transactions.copy())

    def __deepcopy__(self, memo: dict) -> Ledger:
        """
        Create a deep copy of the ledger.

        Args:
            memo (dict): Memoization dict for objects already copied.

        Returns:
            Ledger: A new Ledger instance with a deep copy of the transactions list.

        Examples:
            >>> from copy import deepcopy
            >>> new_ledger = deepcopy(ledger)
        """
        copied_transactions = deepcopy(self.transactions, memo)
        return Ledger(copied_transactions)

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
