#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Global configuration for the BudgetManager project.

Attributes:
    PROJECT_ROOT (Path): The root directory of the project.
    DATA_ROOT (Path): The directory where data files are stored.
"""

import os
from pathlib import Path


def _determine_project_root() -> Path:
    """
    Determine the BudgetManager project root directory.

    Uses the current working directory, which should be the project
    root when the CLI is invoked from the project folder.

    Returns:
        Path: The project root directory.
    """
    return Path.cwd()


PROJECT_ROOT: Path = _determine_project_root()

_env: str | None = os.getenv("BUDGETMANAGER_DATA_ROOT")
DATA_ROOT: Path = Path(_env) if _env else PROJECT_ROOT / "data"

BUDGETS_FILE: Path = DATA_ROOT / "processed" / "budgets.json"
