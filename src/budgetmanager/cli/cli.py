#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Command-line interface for BudgetManager.

This module provides the CLI entrypoint for interacting with the
financial ledger, allowing users to add, list, and report
transactions.
"""

import argparse
import sys
from pathlib import Path
from decimal import Decimal, InvalidOperation

from ..config import DATA_ROOT
from ..file.json_handler import JSONHandler
from ..core.ledger import Ledger
from ..core.transaction import Transaction
from ..utils.timestamp import Timestamp


def load_ledger(file_path: Path) -> Ledger:
    """Load an existing ledger from JSON or initialize a new one.

    Args:
        file_path (Path): Path to the ledger JSON file.

    Returns:
        Ledger: Loaded ledger or a new empty one.

    Raises:
        OSError: If loading the JSON fails due to I/O errors.
        ValueError: If JSON is invalid or ledger data malformed.
    """
    if file_path.exists():
        try:
            data = JSONHandler.load_json(str(file_path))
            return Ledger.from_dict(data)
        except Exception as e:
            print(f"Error loading ledger: {e}", file=sys.stderr)
            sys.exit(1)
    return Ledger()


def save_ledger(ledger: Ledger, file_path: Path) -> None:
    """Save the ledger to a JSON file.

    Args:
        ledger (Ledger): The ledger to save.
        file_path (Path): Path to the target JSON file.

    Raises:
        OSError: If writing the JSON fails.
    """
    try:
        JSONHandler.save_json(ledger.to_dict(), str(file_path))
    except Exception as e:
        print(f"Error saving ledger: {e}", file=sys.stderr)
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog='budgetmgr',
        description='Manage your financial ledger.'
    )
    subparsers = parser.add_subparsers(
        dest='command',
        required=True
    )

    add_p = subparsers.add_parser(
        'add',
        help='Add a new transaction'
    )
    add_p.add_argument(
        '-t', '--timestamp',
        help='ISO timestamp of the transaction'
    )
    add_p.add_argument(
        '-c', '--category', required=True,
        help='Category or tag for the transaction'
    )
    add_p.add_argument(
        '-a', '--amount', required=True,
        help='Amount (positive for income, negative for expense)'
    )
    add_p.add_argument(
        '-d', '--description', default='',
        help='Short description'
    )

    subparsers.add_parser(
        'list',
        help='List all transactions'
    )
    subparsers.add_parser(
        'balance',
        help='Show total balance, income, and expenses'
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        int: Exit code (0 for success, non-zero for errors).
    """
    args = parse_args()
    ledger_file = DATA_ROOT / 'processed' / 'ledger.json'
    ledger = load_ledger(ledger_file)

    if args.command == 'add':
        if args.timestamp:
            ts = Timestamp.from_isoformat(args.timestamp)
        else:
            ts = Timestamp.now()
        try:
            amt = Decimal(args.amount)
        except InvalidOperation:
            print(f"Invalid amount: {args.amount}", file=sys.stderr)
            return 1

        tx = Transaction(
            timestamp=ts,
            category=args.category,
            amount=amt,
            description=args.description,
        )
        ledger.add_transaction(tx)
        save_ledger(ledger, ledger_file)
        print(f"Added: {tx}")
        return 0

    if args.command == 'list':
        if not ledger:
            print('No transactions found.')
        else:
            for t in ledger:
                print(t)
        return 0

    if args.command == 'balance':
        bal = ledger.get_balance()
        inc = ledger.total_income()
        exp = ledger.total_expenses()
        print(f"Balance:  {bal}")
        print(f"Income:   {inc}")
        print(f"Expenses: {exp}")
        return 0

    return 1


if __name__ == '__main__':
    sys.exit(main())
