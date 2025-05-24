#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Command-line interface for BudgetManager.

This module provides the CLI entrypoint for interacting with the
financial ledger, allowing users to add, list, report transactions,
and manage budgets with warning on overspend.
"""

import argparse
import argcomplete
import sys
import calendar
from pathlib import Path
from decimal import Decimal, InvalidOperation

from ..config import DATA_ROOT
from ..file.sqlite_handler import SQLiteHandler
from ..core.ledger import Ledger
from ..core.transaction import Transaction
from ..core.budget import Budget
from ..utils.timestamp import Timestamp
from ..core.report import ReportGenerator
from ..core.chart import generate_chart


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments, with argcomplete enabled.

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

    # Add transaction
    add_p = subparsers.add_parser(
        'add',
        help='Add a new transaction'
    )
    add_p.add_argument(
        '-t', '--timestamp',
        help='ISO timestamp of the transaction'
    )
    add_p.add_argument(
        '-c', '--category',
        required=True,
        help='Category or tag for the transaction'
    )
    add_p.add_argument(
        '-a', '--amount',
        required=True,
        help='Amount (positive for income, negative for expense)'
    )
    add_p.add_argument(
        '-d', '--description',
        default='',
        help='Short description'
    )

    # List and balance
    subparsers.add_parser(
        'list',
        help='List all transactions'
    )
    subparsers.add_parser(
        'balance',
        help='Show total balance, income, and expenses'
    )

    # Summary
    sum_p = subparsers.add_parser(
        'summary',
        help='Show monthly or yearly summary'
    )
    sum_p.add_argument(
        '--year', '-y',
        type=int, required=True,
        help='Four-digit year, z.B. 2025'
    )
    sum_p.add_argument(
        '--month', '-m',
        type=int,
        help='Month (1–12); falls weggelassen, wird Jahres-Summary erstellt'
    )
    sum_p.add_argument(
        '--export', '-e',
        choices=['csv'],
        help='Optional export to CSV'
    )

    # Budget subcommands
    budget_p = subparsers.add_parser(
        'budget',
        help='Manage budgets'
    )
    budget_sub = budget_p.add_subparsers(
        dest='budget_command',
        required=True
    )

    add_b = budget_sub.add_parser(
        'add',
        help='Add a new budget'
    )
    add_b.add_argument(
        '-c', '--category',
        required=True,
        help='Category name'
    )
    add_b.add_argument(
        '-l', '--limit',
        required=True,
        help='Budget limit (positive number)'
    )

    budget_sub.add_parser(
        'list',
        help='List all budgets'
    )

    # Chart
    chart_p = subparsers.add_parser(
        'chart',
        help='Show income/expanses per category as ASCII and optional PNG/SVG'
    )
    chart_p.add_argument(
        '--start', '-s',
        type=str, required=True,
        help='Start date (YYYY-MM-DD)'
    )
    chart_p.add_argument(
        '--end', '-e',
        type=str, required=True,
        help='End date (YYYY-MM-DD)'
    )
    fmt_group = chart_p.add_mutually_exclusive_group()
    fmt_group.add_argument(
        '--png', action='store_true',
        help='Save chart as PNG'
    )
    fmt_group.add_argument(
        '--svg', action='store_true',
        help='Save Chart as SVG'
    )

    argcomplete.autocomplete(parser)

    return parser.parse_args()


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        int: Exit code (0 for success, non-zero for errors).
    """
    args = parse_args()
    handler = SQLiteHandler()
    ledger = Ledger(handler.get_all_transactions())

    # --- Budget management ---
    if args.command == 'budget':
        if args.budget_command == 'add':
            try:
                limit = Decimal(args.limit)
            except InvalidOperation:
                print(f"Invalid limit: {args.limit}", file=sys.stderr)
                return 1

            budget = Budget(category=args.category, limit=limit)
            handler.add_budget(budget)
            print(f"Set budget: {budget.category} -> {budget.limit}")
            return 0

        if args.budget_command == 'list':
            budgets = handler.get_budgets()
            if not budgets:
                print("No budgets defined.")
            else:
                for b in budgets:
                    print(f"{b.category}: {b.limit}")
            return 0

    # --- Add transaction ---
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
            description=args.description
        )
        handler.add_transaction(tx)
        ledger.add_transaction(tx)

        # Budget warning on overspend
        budgets = handler.get_budgets()
        now = Timestamp.now()
        year, month = now.year, now.month
        first_day = 1
        last_day = calendar.monthrange(year, month)[1]
        start = Timestamp.from_components(year, month, first_day)
        end = Timestamp.from_components(year, month, last_day)

        spent = sum(
            -t.amount
            for t in ledger.filter_by_category(tx.category)
            if t.is_expense() and start <= t.timestamp <= end
        )
        for b in budgets:
            if b.category == tx.category and spent > b.limit:
                print(
                    f"\033[91mWarning: budget for '{b.category}' "
                    f"exceeded ({spent} > {b.limit})\033[0m"
                )

        print(f"Added: {tx}")
        return 0

    # --- List transactions ---
    if args.command == 'list':
        if not ledger:
            print("No transactions found.")
        else:
            for t in ledger:
                print(t)
        return 0

    # --- Show balance ---
    if args.command == 'balance':
        bal = ledger.get_balance()
        inc = ledger.total_income()
        exp = ledger.total_expenses()
        print(f"Balance:  {bal}")
        print(f"Income:   {inc}")
        print(f"Expenses: {exp}")
        return 0

    # --- Summary report ---
    if args.command == 'summary':
        if args.month:
            data = ReportGenerator.monthly_summary(
                ledger, args.year, args.month
            )
            label = f"{args.year}-{args.month:02d}"
        else:
            data = ReportGenerator.yearly_summary(ledger, args.year)
            label = str(args.year)

        for key, val in data.items():
            print(f"{label} {key.capitalize()}: {val}")

        if args.export == 'csv':
            out = DATA_ROOT / 'processed' / f"summary_{label}.csv"
            path = ReportGenerator.export_to_csv(data, out)
            print(f"Exported to: {path}")
        return 0

    # --- Show chart ---
    if args.command == 'chart':
        try:
            y1, m1, d1 = map(int, args.start.split('-'))
            y2, m2, d2 = map(int, args.end.split('-'))
        except ValueError:
            print(
                "Invalid date format, please use YYYY-MM-DD.",
                file=sys.stderr
            )
            return 1

        start_ts = Timestamp.from_components(y1, m1, d1)
        end_ts = Timestamp.from_components(
            y2, m2, d2, 23, 59, 59, 999_999
        )

        export_fmt: str | None = None
        if args.png:
            export_fmt = 'png'
        elif args.svg:
            export_fmt = 'svg'

        generate_chart(ledger, start_ts, end_ts, export_fmt)
        return 0

    return 1


if __name__ == '__main__':
    sys.exit(main())
