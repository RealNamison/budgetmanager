#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Module for handling file system operations: creating directories, files,
and managing paths for directories and files.

This module uses Python's built-in pathlib module to work with paths,
anchored in a configurable data root directory.
"""

from pathlib import Path
import re

from .. import config


class FileHandler:
    """
    A handler class to manage file and directory operations under DATA_ROOT.

    Provides methods to:
        - Create directories
        - Create empty files
        - Construct directory and file paths
    """

    @staticmethod
    def create_directory(path: str) -> Path:
        """
        Creates a directory at config.DATA_ROOT/path (if `path` is relative) or at an
        absolute path.

        Args:
            path (str): Relative (to DATA_ROOT) or absolute directory path.

        Returns:
            Path: A pathlib.Path object of the created directory.

        Raises:
            OSError: If the directory cannot be created, with contextual info.
        """
        candidate = Path(path)
        dir_path = candidate if candidate.is_absolute() else config.DATA_ROOT / candidate

        try:
            dir_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create directory '{dir_path}': {e.strerror}") from e

        return dir_path

    @staticmethod
    def create_file(directory_path: str, file_name: str, file_type: str) -> Path:
        """
        Creates an empty file with the specified name and type in the given directory.
        Relies on create_directory to ensure the directory exists.

        Args:
            directory_path (str): Relative (to DATA_ROOT) or absolute directory path.
            file_name (str): Name of the file without extension. Allowed characters: letters, numbers, hyphens, underscores.
            file_type (str): File extension (e.g., 'txt', 'csv'). Allowed characters: letters and numbers.

        Returns:
            Path: A pathlib.Path object of the created file.

        Raises:
            ValueError: If file_name or file_type is invalid.
            OSError: If the file or its parent directory cannot be created, with contextual info.
        """
        # Validate file_name using regex
        if not re.match(r'^[A-Za-z0-9_-]+$', file_name):
            raise ValueError(
                f"Invalid file_name '{file_name}': must contain only letters, numbers, hyphens, or underscores")
        # Validate file_type using regex
        if not file_type or not re.match(r'^[A-Za-z0-9]+$', file_type):
            raise ValueError(f"Invalid file_type '{file_type}': must contain only letters and numbers and be non-empty")

        try:
            dir_path = FileHandler.create_directory(directory_path)
        except OSError as e:
            raise OSError(f"Cannot ensure directory exists for file '{directory_path}': {e}") from e

        file_path = dir_path / f"{file_name}.{file_type.lower()}"
        try:
            file_path.touch(exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create file '{file_path}': {e.strerror}") from e

        return file_path

    @staticmethod
    def get_directory_path(*paths: str) -> Path:
        """
        Constructs a directory path by returning the first argument if it's absolute,
        otherwise joins components under DATA_ROOT.

        Args:
            *paths (str): Path components to join.

        Returns:
            Path: A pathlib.Path object representing the directory path.
        """
        first = Path(paths[0])
        if first.is_absolute():
            return first
        return config.DATA_ROOT.joinpath(*paths)

    @staticmethod
    def get_file_path(*paths: str) -> Path:
        """
        Constructs a file path by returning the first argument if it's absolute,
        otherwise joins components under DATA_ROOT.

        Args:
            *paths (str): Path components to join, including filename.

        Returns:
            Path: A pathlib.Path object representing the file path.
        """
        first = Path(paths[0])
        if first.is_absolute():
            return first
        return config.DATA_ROOT.joinpath(*paths)
