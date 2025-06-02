#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
SQLite handler for persisting transactions and budgets.

This module provides the SQLiteHandler class to manage database
interactions for transactions and budgets using a SQLite database
file under DATA_ROOT/processed/budget.db.
"""

import sqlite3
from pathlib import Path
from decimal import Decimal

from ..config import DB_FILE
from .file_handler import FileHandler
from ..core.transaction import Transaction
from ..core.budget import Budget
from ..utils.timestamp import Timestamp


class SQLiteHandler:
    """Manage SQLite database for transactions and budgets."""

    def __init__(self, db_path: Path | None = None) -> None:
        """Initialize handler and ensure schema exists.

        Args:
            db_path (Path | None): Custom path to DB file. Defaults to
                DATA_ROOT/processed/budget.db.

        Raises:
            sqlite3.Error: If database initialization fails.
        """
        self.db_path = db_path or DB_FILE
        self._ensure_directory()
        with self._connect() as conn:
            self._create_tables(conn)

    def _ensure_directory(self) -> None:
        """Ensure that the directory for the DB file exists."""
        FileHandler.create_directory(str(self.db_path.parent))

    def _connect(self) -> sqlite3.Connection:
        """Open a SQLite connection with dict-like rows.

        Returns:
            sqlite3.Connection: Connection object.

        Raises:
            sqlite3.Error: If connection cannot be opened.
        """
        conn = sqlite3.connect(
            self.db_path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _create_tables(conn: sqlite3.Connection) -> None:
        """Create tables if they do not already exist.

        Args:
            conn (sqlite3.Connection): Active DB connection.

        Raises:
            sqlite3.Error: On SQL errors.
        """
        # Transactions table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                category TEXT NOT NULL,
                amount TEXT NOT NULL,
                description TEXT
            )
        """
        )
        # Budgets table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE NOT NULL,
                limit_amount TEXT NOT NULL
            )
        """
        )
        # Use PRAGMA for simple schema versioning if needed
        conn.execute("PRAGMA user_version = 1")

    def add_transaction(self, tx: Transaction) -> None:
        """Insert a Transaction into the database.

        Args:
            tx (Transaction): Transaction to persist.

        Raises:
            sqlite3.IntegrityError: On constraint violation.
            sqlite3.OperationalError: On other DB errors.

        Examples:
            >>> handler = SQLiteHandler()
            >>> handler.add_transaction(tx)
        """
        sql = (
            "INSERT INTO transactions "
            "(timestamp, category, amount, description) "
            "VALUES (?, ?, ?, ?)"
        )
        with self._connect() as conn:
            conn.execute(
                sql,
                (
                    tx.timestamp.to_isoformat(),
                    tx.category,
                    str(tx.amount),
                    tx.description,
                ),
            )

    def get_all_transactions(self) -> list[Transaction]:
        """Load all transactions from the database.

        Returns:
            list[Transaction]: All stored transactions.

        Raises:
            sqlite3.OperationalError: On query failure.

        Examples:
            >>> txs = handler.get_all_transactions()
        """
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM transactions").fetchall()

        result: list[Transaction] = []
        for r in rows:
            ts = Timestamp.from_isoformat(r["timestamp"])
            amt = Decimal(r["amount"])
            result.append(
                Transaction(ts, r["category"], amt, r["description"])
            )
        return result

    def remove_transaction(self, tx_id: int) -> Transaction | None:
        """Delete a transaction by its ID and return the deleted Transaction.

        Args:
            tx_id (int): ID of the transaction to remove.

        Returns:
            Transaction | None: The deleted transaction if found,
            otherwise None.

        Raises:
            sqlite3.IntegrityError: If deletion violates constraints.
            sqlite3.OperationalError: On query failure.
        """
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, timestamp, category, amount, description "
                "FROM transactions WHERE id = ?",
                (tx_id,),
            ).fetchone()
            if row is None:
                return None

            tx = Transaction(
                Timestamp.from_isoformat(row["timestamp"]),
                row["category"],
                Decimal(row["amount"]),
                row["description"] or "",
            )

            conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))

            return tx

    def add_budget(self, budget: Budget) -> None:
        """Insert or update a Budget in the database.

        Checks if a budget for the given category exists.
        Updates the limit if present, otherwise inserts a new record.

        Args:
            budget (Budget): Budget to insert or update.

        Raises:
            sqlite3.OperationalError: On SQL errors.
            sqlite3.IntegrityError: On constraint violations.

        Examples:
            >>> handler.add_budget(Budget('food', Decimal('100')))
        """
        insert_sql = (
            "INSERT INTO budgets (category, limit_amount) VALUES (?, ?)"
        )
        update_sql = "UPDATE budgets SET limit_amount = ? WHERE category = ?"
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM budgets WHERE category = ?", (budget.category,)
            )
            if cursor.fetchone():
                conn.execute(update_sql, (str(budget.limit), budget.category))
            else:
                conn.execute(insert_sql, (budget.category, str(budget.limit)))

    def get_budgets(self) -> list[Budget]:
        """Load all budgets from the database.

        Returns:
            list[Budget]: All stored budgets.

        Raises:
            sqlite3.OperationalError: On query failure.
        """
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM budgets").fetchall()

        result: list[Budget] = []
        for r in rows:
            result.append(Budget(r["category"], Decimal(r["limit_amount"])))
        return result

    def remove_budget(self, category: str) -> None:
        """Delete a budget by its category.

        Args:
            category (str): Category of the budget to remove.

        Raises:
            sqlite3.IntegrityError: If deletion violates constraints.
        """
        with self._connect() as conn:
            conn.execute("DELETE FROM budgets WHERE category = ?", (category,))
