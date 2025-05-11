#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combined tests for file_handler.py focusing on directory and file creation,
path construction, and error handling.
"""

from pathlib import Path
import pytest

from budgetmanager import config
from budgetmanager.file.file_handler import FileHandler


def test_create_directory_absolute(tmp_path: Path):
    """Test that create_directory creates an absolute directory when given an absolute path."""
    abs_dir = tmp_path / "abs_test"
    result = FileHandler.create_directory(str(abs_dir))
    assert result.exists() and result.is_dir()
    assert result == abs_dir


def test_create_directory_relative(tmp_path: Path, monkeypatch):
    """Test that create_directory creates a directory under DATA_ROOT for relative paths."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)
    rel_dir = "rel_test"
    result = FileHandler.create_directory(rel_dir)
    expected = tmp_path / rel_dir
    assert result.exists() and result.is_dir()
    assert result == expected


def test_create_file_absolute(tmp_path: Path):
    """Test that create_file creates an empty file at an absolute path."""
    abs_dir = tmp_path / "file_dir"
    file_name = "testfile"
    file_type = "txt"
    result = FileHandler.create_file(str(abs_dir), file_name, file_type)
    expected = abs_dir / f"{file_name}.{file_type}"
    assert result.exists() and result.is_file()
    assert result == expected


def test_create_file_relative(tmp_path: Path, monkeypatch):
    """Test that create_file creates a file under DATA_ROOT when using a relative directory."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)
    rel_dir = "file_rel"
    file_name = "test"
    file_type = "md"
    result = FileHandler.create_file(rel_dir, file_name, file_type)
    expected = tmp_path / rel_dir / f"{file_name}.{file_type}"
    assert result.exists() and result.is_file()
    assert result == expected


def test_get_directory_path(tmp_path: Path, monkeypatch):
    """Test get_directory_path returns a path under DATA_ROOT for components."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)
    result = FileHandler.get_directory_path("a", "b", "c")
    expected = tmp_path / "a" / "b" / "c"
    assert result == expected


def test_get_file_path(tmp_path: Path, monkeypatch):
    """Test get_file_path returns a file path under DATA_ROOT for components."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)
    result = FileHandler.get_file_path("dir", "file.txt")
    expected = tmp_path / "dir" / "file.txt"
    assert result == expected


def test_create_directory_error_when_file_exists(tmp_path: Path, monkeypatch):
    """Test that create_directory raises OSError when a file exists at the target path."""
    monkeypatch.setattr(config, 'DATA_ROOT', tmp_path)
    conflict_path = tmp_path / 'conflict'
    conflict_path.write_text('I am a file, not a directory')
    with pytest.raises(OSError) as exc_info:
        FileHandler.create_directory('conflict')
    msg = str(exc_info.value)
    assert 'Failed to create directory' in msg
    assert str(conflict_path) in msg


def test_create_file_error_when_parent_is_file(tmp_path: Path, monkeypatch):
    """Test that create_file raises OSError when the parent path is a file."""
    monkeypatch.setattr(config, 'DATA_ROOT', tmp_path)
    parent_file = tmp_path / 'parent.txt'
    parent_file.write_text('I am a file, not a directory')
    with pytest.raises(OSError) as exc_info:
        FileHandler.create_file('parent.txt', 'child', 'txt')
    msg = str(exc_info.value)
    assert 'Cannot ensure directory exists for file' in msg
    assert 'parent.txt' in msg


def test_get_directory_path_absolute_ignores_data_root(tmp_path: Path, monkeypatch):
    """Test get_directory_path returns the absolute path ignoring DATA_ROOT."""
    monkeypatch.setattr(config, 'DATA_ROOT', tmp_path / 'will_not_be_used')
    abs_path = tmp_path / 'abs' / 'dir'
    result = FileHandler.get_directory_path(str(abs_path), 'ignored')
    assert result == abs_path


def test_get_file_path_absolute_ignores_data_root(tmp_path: Path, monkeypatch):
    """Test get_file_path returns the absolute path ignoring DATA_ROOT."""
    monkeypatch.setattr(config, 'DATA_ROOT', tmp_path / 'unused')
    abs_path = tmp_path / 'some' / 'file.txt'
    result = FileHandler.get_file_path(str(abs_path), 'ignored')
    assert result == abs_path


def test_create_directory_idempotent(tmp_path):
    dir1 = FileHandler.create_directory(str(tmp_path / "a"))
    dir2 = FileHandler.create_directory(str(tmp_path / "a"))
    assert dir1 == dir2
    assert dir2.exists() and dir2.is_dir()


def test_create_directory_nested(tmp_path: Path, monkeypatch):
    """Test nested directory creation under DATA_ROOT for relative paths."""
    # Override DATA_ROOT to the temporary path
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)

    nested = "a/b/c/d"
    result = FileHandler.create_directory(nested)
    expected = tmp_path / "a" / "b" / "c" / "d"

    assert result == expected
    assert expected.is_dir()


# noinspection PyUnusedLocal
def test_create_file_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)
    path1 = FileHandler.create_file("dir", "file", "txt")
    ts1 = path1.stat().st_mtime
    path2 = FileHandler.create_file("dir", "file", "txt")
    ts2 = path2.stat().st_mtime
    assert path1 == path2
    assert path1.exists()
    # Optional: ts2 >= ts1


def test_get_directory_path_multi_segments(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)
    result = FileHandler.get_directory_path("x", "y", "z")
    assert result == tmp_path / "x" / "y" / "z"


def test_get_directory_path_no_args():
    with pytest.raises(IndexError):
        FileHandler.get_directory_path()
