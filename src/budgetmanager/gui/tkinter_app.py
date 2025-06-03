#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Entry-point module for the Tkinter GUI application.

This module creates the main application window, registers all
required tabs, and starts the Tkinter event loop.
"""

# Standard library imports
import sys

# Local application imports
from .views.main_window import MainWindow
from .views.transaction_view import TransactionsTab


def main() -> None:
    """
    Initialize and launch the BudgetManager GUI application.

    Creates a MainWindow instance, registers the TransactionsTab,
    and enters the Tkinter main event loop.

    Raises:
        RuntimeError: If the GUI fails to start.
    """
    try:
        window = MainWindow(title="BudgetManager")
        window.register_tab("Transactions", TransactionsTab)
        window.run()
    except Exception as err:
        print(f"Failed to start GUI: {err}", file=sys.stderr)
        raise RuntimeError("Could not launch Tkinter application") from err


if __name__ == "__main__":
    main()
