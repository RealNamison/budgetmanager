#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add project src directory to Python’s import path so that pytest
can find the budgetmanager package.
"""

import os
import sys


# Project-Root = one layer above tests/
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
