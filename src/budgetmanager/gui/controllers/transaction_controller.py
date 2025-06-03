#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Module for the TransactionController, interfacing between the GUI and
core/data layers for transactions, ledger, timestamps, and SQLite storage.
"""

# Standard library imports
from decimal import Decimal

# Local application imports
from ...core.transaction import Transaction
from ...core.ledger import Ledger
from ...utils.timestamp import Timestamp
from ...file.sqlite_handler import SQLiteHandler


class TransactionController:
    """
    Controller class to manage transactions between GUI and core/data.

    This class uses SQLiteHandler to persist transactions, maintains
    an in-memory Ledger for fast access, and provides methods to add,
    remove, and query transactions.

    Attributes:
        handler (SQLiteHandler): Handler to interact with SQLite database.
        ledger (Ledger): In-memory ledger of Transaction instances.
    """

    def __init__(self, db_path: str | None = None) -> None:
        """
        Initialize controller, set up SQLite handler, and load existing data.

        Args:
            db_path (str | None): Optional path to custom SQLite DB file.
                If None, uses default from config.
        """
        self.handler = SQLiteHandler(db_path)
        self.ledger = Ledger()
        self._load_transactions()

    def _load_transactions(self) -> None:
        """
        Load all persisted transactions from database
        into the in-memory ledger.

        Raises:
            sqlite3.OperationalError: On query failure.
        """
        txs = self.handler.get_all_transactions()
        for tx in txs:
            self.ledger.add_transaction(tx)

    def get_all_transactions(self) -> list[Transaction]:
        """
        Retrieve all transactions currently in the ledger.

        Returns:
            list[Transaction]: List of all Transaction instances.
        """
        return list(self.ledger)

    def add_transaction(
        self,
        category: str,
        amount: Decimal,
        description: str,
        timestamp: Timestamp | None = None,
    ) -> Transaction:
        """
        Create and persist a new transaction, then add it to the ledger.

        Args:
            category (str): Category or tag of the transaction.
            amount (Decimal): Positive for income, negative for expense.
            description (str): Short description of the transaction.
            timestamp (Timestamp | None): Optional timestamp. If None,
                current time is used.

        Returns:
            Transaction: The newly created Transaction with assigned ID.

        Raises:
            sqlite3.IntegrityError: On DB constraint violation.
            sqlite3.OperationalError: On other DB errors.
        """
        ts = timestamp or Timestamp.now()
        tx = Transaction(timestamp=ts, category=category, amount=amount,
                         description=description)
        self.handler.add_transaction(tx)
        self.ledger.add_transaction(tx)
        return tx

    def remove_transaction(self, transaction_id: int) -> bool:
        """
        Remove a transaction by its ID from both DB and ledger.

        Args:
            transaction_id (int): ID of the transaction to remove.

        Returns:
            bool: True if a transaction was found and removed, False otherwise.

        Raises:
            sqlite3.OperationalError: On DB query failure.
        """
        deleted_tx = self.handler.remove_transaction(transaction_id)
        if deleted_tx is None:
            return False
        try:
            self.ledger.remove_transaction(deleted_tx)
        except ValueError:
            # If ledger does not contain this transaction, ignore
            pass
        return True

    def get_balance(self) -> Decimal:
        """
        Compute net balance from the in-memory ledger.

        Returns:
            Decimal: Net sum of all transaction amounts.
        """
        return self.ledger.get_balance()

    def get_total_income(self) -> Decimal:
        """
        Compute total income (sum of positive amounts) from the ledger.

        Returns:
            Decimal: Sum of all income transactions.
        """
        return self.ledger.total_income()

    def get_total_expenses(self) -> Decimal:
        """
        Compute total expenses (sum of negative amounts) from the ledger.

        Returns:
            Decimal: Sum of all expense transactions.
        """
        return self.ledger.total_expenses()

    def filter_transactions_by_category(
            self, category: str
    ) -> list[Transaction]:
        """
        Retrieve transactions matching a specific category.

        Args:
            category (str): Category to filter by.

        Returns:
            list[Transaction]: Transactions whose category equals the given.
        """
        return self.ledger.filter_by_category(category)

    def filter_transactions_by_date(
        self, start: Timestamp, end: Timestamp
    ) -> list[Transaction]:
        """
        Retrieve transactions between two timestamps (inclusive).

        Args:
            start (Timestamp): Start of date range.
            end (Timestamp): End of date range.

        Returns:
            list[Transaction]: Transactions with timestamp within range.
        """
        return self.ledger.filter_by_date_range(start, end)

    def refresh_ledger(self) -> None:
        """
        Clear and reload the in-memory ledger from the database.

        Useful if external changes to the DB occurred.

        Raises:
            sqlite3.OperationalError: On DB query failure.
        """
        self.ledger = Ledger()
        self._load_transactions()
