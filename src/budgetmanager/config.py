#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global configuration for the BudgetManager project.

Attributes:
    PROJECT_ROOT (Path): The root directory of the BudgetManager project.
    DATA_ROOT (Path):    The data directory under the project root.
"""

from pathlib import Path

# Determine the project root (two levels above this file: budgetmanager/ → src/ → project root)
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

# Define the data directory under the project root
DATA_ROOT: Path = PROJECT_ROOT / "data"
