#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global configuration for the PyGod project.

Defines the project root and data directory locations.
"""

from pathlib import Path

# Determine the project root (two levels above this file: src/file -> src -> PyGod)
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

# Define the data directory under the project root
DATA_ROOT: Path = PROJECT_ROOT / "data"
