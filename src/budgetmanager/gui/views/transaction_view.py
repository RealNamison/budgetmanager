#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Module for the TransactionsTab class, displaying all transactions
in a tabular view using Tkinter's Treeview.
"""

# Standard library imports
import tkinter as tk
from tkinter import ttk
from decimal import Decimal

# Local application imports
from ..base import BaseTab
from ..controllers.transaction_controller import TransactionController


class TransactionsTab(BaseTab):
    """
    Tab frame showing all transactions in a table.

    Retrieves data from the TransactionController and displays
    it in a Treeview with columns for ID, timestamp, category,
    amount, and description.

    Attributes:
        controller (TransactionController): Controller for transaction data.
        tree (ttk.Treeview): Treeview widget displaying the transactions.
        scrollbar (tk.Scrollbar): Vertical scrollbar for the Treeview.
    """

    def __init__(self, parent: tk.Widget) -> None:
        """
        Initialize the TransactionsTab and configure its widgets.

        Args:
            parent (tk.Widget): Parent container for the tab.
        """
        super().__init__(parent)
        self.controller = TransactionController()
        self._setup_widgets()
        self.refresh_table()

    def _configure_tab(self) -> None:
        """
        Configure default tab settings such as padding and layout.
        """
        self.pack(fill="both", expand=True)

    def _setup_widgets(self) -> None:
        """
        Create and grid the Treeview and scrollbar widgets.
        """
        # Create Treeview with columns
        columns = ("id", "timestamp", "category", "amount", "description")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("description", text="Description")

        # Define column widths
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("timestamp", width=150, anchor="w")
        self.tree.column("category", width=100, anchor="w")
        self.tree.column("amount", width=80, anchor="e")
        self.tree.column("description", width=200, anchor="w")

        # Grid the Treeview
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add vertical scrollbar
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def refresh_table(self) -> None:
        """
        Clear the current Treeview entries and repopulate with all
        transactions from the controller.
        """
        # Remove existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch transactions and insert into the Treeview
        transactions = self.controller.get_all_transactions()
        for tx in transactions:
            # Format amount with two decimal places
            if isinstance(tx.amount, Decimal):
                amount_str = f"{tx.amount:.2f}"
            else:
                amount_str = str(tx.amount)

            # Assume tx.timestamp has a __str__ method
            timestamp_str = str(tx.timestamp)

            self.tree.insert(
                "",
                "end",
                values=(
                    tx.transaction_id,
                    timestamp_str,
                    tx.category,
                    amount_str,
                    tx.description,
                ),
            )

    def on_show(self) -> None:
        """
        Called when the tab is shown. Refresh the table to show latest data.
        """
        self.refresh_table()
