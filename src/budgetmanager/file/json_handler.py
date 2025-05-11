#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for handling JSON file operations: loading and saving JSON data.

This module leverages FileHandler to ensure that all JSON files
are located exclusively under the configured data directory (DATA_ROOT).
"""

import json
from typing import Any
from pathlib import Path

from budgetmanager.file.file_handler import FileHandler


class JSONHandler:
    """
    A handler class to manage loading and saving JSON files under DATA_ROOT.

    Provides methods to:
        - Load JSON data from a file
        - Save Python objects as JSON files
    """

    @staticmethod
    def load_json(*paths: str) -> Any:
        """
        Loads JSON data from a file located in DATA_ROOT or via absolute path.
        First checks if the file exists and raises FileNotFoundError if not.

        Args:
            *paths (str): Path components to the JSON file.

        Returns:
            Any: The Python object resulting from parsing the JSON file.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
            OSError: For other I/O related errors when opening the file.
        """
        # Resolve file path using FileHandler
        file_path: Path = FileHandler.get_file_path(*paths)

        # Check existence before attempting to open
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")

        if file_path.suffix.lower() != ".json":
            raise ValueError(f"Expected a .json file, but got: {file_path}")

        # Attempt to open and parse JSON, with contextual exception handling
        try:
            with file_path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            # Provide context on JSON parsing error
            raise json.JSONDecodeError(f"Failed to parse JSON file '{file_path}': {e.msg}", e.doc, e.pos) from e
        except OSError as e:
            # Contextualize file opening errors
            raise OSError(f"Failed to open JSON file '{file_path}': {e.strerror}") from e

    @staticmethod
    def save_json(data: Any, *paths: str) -> Path:
        """
        Saves Python data as JSON to a file located in DATA_ROOT or via absolute path.
        Uses FileHandler.create_file to ensure the file exists before writing.

        Args:
            data (Any): The Python object to serialize to JSON.
            *paths (str): Path components for the target JSON file.

        Returns:
            Path: The pathlib.Path object of the saved JSON file.

        Raises:
            OSError: For I/O related errors when creating or writing the file.
        """
        # Resolve the file path
        file_path: Path = FileHandler.get_file_path(*paths)
        # Ensure the file exists
        try:
            FileHandler.create_file(str(file_path.parent), file_path.stem, "json")
        except OSError as e:
            raise OSError(f"Cannot ensure file exists at '{file_path}': {e}") from e

        # Write JSON data as a string
        json_str = json.dumps(data, indent=4)
        try:
            # Use Path.write_text to write the JSON string, avoiding type mismatch
            file_path.write_text(json_str, encoding='utf-8')
        except OSError as e:
            raise OSError(f"Failed to write JSON file '{file_path}': {e.strerror}") from e

        return file_path
