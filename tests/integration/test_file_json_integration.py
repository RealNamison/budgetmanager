#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Integration tests for FileHandler and JSONHandler.

Verifies that FileHandler.create_file and JSONHandler.save_json/load_json
can create, write, and read a JSON file correctly.
"""

import json
from pathlib import Path

import pytest

from budgetmanager.file.file_handler import FileHandler
from budgetmanager.file.json_handler import JSONHandler


def test_create_and_load_json(tmp_path: Path) -> None:
    test_dir = tmp_path / "processed"
    file_path = FileHandler.create_file(str(test_dir), "data", "json")

    data = {"foo": 42, "bar": ["a", "b", "c"]}

    saved = JSONHandler.save_json(data, str(file_path))
    loaded = JSONHandler.load_json(str(file_path))

    assert saved == file_path
    assert loaded == data
