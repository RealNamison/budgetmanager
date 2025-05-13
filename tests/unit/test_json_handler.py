#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Test module for JSONHandler: covers saving and loading JSON files
under DATA_ROOT and via absolute paths, plus alle relevanten Fehlerfälle.
"""

import json
import pytest
from pathlib import Path

from budgetmanager import config
from budgetmanager.file.json_handler import JSONHandler
from budgetmanager.file.file_handler import FileHandler


def test_save_json_relative(tmp_path, monkeypatch):
    """Save JSON under DATA_ROOT and verify content."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)

    payload = {"alpha": 1, "beta": [2, 3]}
    result = JSONHandler.save_json(payload, "example.json")
    expected = tmp_path / "example.json"

    assert result == expected
    assert expected.exists() and expected.is_file()
    assert json.loads(expected.read_text(encoding="utf-8")) == payload


def test_save_json_nested_relative(tmp_path, monkeypatch):
    """Save JSON into nested directories under DATA_ROOT."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)

    payload = {"nested": True}
    result = JSONHandler.save_json(payload, "a", "b", "c.json")
    expected = tmp_path / "a" / "b" / "c.json"

    assert result == expected
    assert expected.exists()
    # Verify that load_json returns the same payload
    assert JSONHandler.load_json("a", "b", "c.json") == payload


def test_save_json_absolute(tmp_path):
    """Saving JSON with absolute path should work."""
    payload = {"abs": "ok"}
    abs_file = tmp_path / "out.json"

    result = JSONHandler.save_json(payload, str(abs_file))
    assert result == abs_file
    assert abs_file.exists()
    assert json.loads(abs_file.read_text(encoding="utf-8")) == payload


def test_load_json_relative(tmp_path, monkeypatch):
    """Load an existing JSON file under DATA_ROOT."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)

    file = tmp_path / "cfg.json"
    data = {"x": 10, "y": 20}
    file.write_text(json.dumps(data), encoding="utf-8")

    loaded = JSONHandler.load_json("cfg.json")
    assert loaded == data


def test_load_json_absolute(tmp_path):
    """Load JSON via an absolute path."""
    data = {"hello": "world"}
    file = tmp_path / "hello.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    loaded = JSONHandler.load_json(str(file))
    assert loaded == data


def test_load_json_not_found(tmp_path, monkeypatch):
    """Loading a non-existent file should raise FileNotFoundError."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)
    with pytest.raises(FileNotFoundError) as exc:
        JSONHandler.load_json("nope.json")
    assert "JSON file not found" in str(exc.value)


def test_load_json_wrong_extension(tmp_path, monkeypatch):
    """Loading a file with non-.json extension should raise ValueError."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)

    file = tmp_path / "data.txt"
    file.write_text('{"ok": true}', encoding="utf-8")

    with pytest.raises(ValueError) as exc:
        JSONHandler.load_json("data.txt")
    assert "Expected a .json file" in str(exc.value)


def test_load_json_invalid_content(tmp_path, monkeypatch):
    """Invalid JSON content should raise JSONDecodeError."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)

    bad = tmp_path / "bad.json"
    bad.write_text("{ not valid json }", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError) as exc:
        JSONHandler.load_json("bad.json")
    assert "Failed to parse JSON file" in str(exc.value)


def test_save_json_directory_creation_error(tmp_path, monkeypatch):
    """Simulate create_file failure and verify OSError from save_json."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)

    # noinspection PyUnusedLocal
    def fake_create(dir_path, name, ext):
        raise OSError("cannot create dir")
    monkeypatch.setattr(FileHandler, "create_file", fake_create)

    with pytest.raises(OSError) as exc:
        JSONHandler.save_json({"a": 1}, "won't.json")
    assert "Cannot ensure file exists at" in str(exc.value)


def test_save_json_write_error(tmp_path, monkeypatch):
    """Simulate write_text failure and verify OSError from save_json."""
    monkeypatch.setattr(config, "DATA_ROOT", tmp_path)

    # noinspection PyUnusedLocal
    def fake_write(self, txt, encoding):
        raise OSError("disk full")
    monkeypatch.setattr(Path, "write_text", fake_write)

    with pytest.raises(OSError) as exc:
        JSONHandler.save_json({"k": "v"}, "x.json")
    assert "Failed to write JSON file" in str(exc.value)
