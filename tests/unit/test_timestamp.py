#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pytest module for testing the Timestamp class from timestamp.py.

This test suite covers:
    - Initialization with valid and invalid inputs
    - Creation methods: now, from_components, from_datetime, from_isoformat
    - Conversion methods: to_datetime, __float__, __str__, __repr__
    - Property accessors: year, month, day, hour, minute, second, microsecond
    - Comparison operators: ==, <, <=, >, >=
"""

import pytest
from datetime import date, time, datetime

from budgetmanager.utils.timestamp import Timestamp


def test_init_valid():
    """Test that initializing with valid date and time sets attributes correctly."""
    d = date(2025, 1, 2)
    t = time(3, 4, 5, 6)
    ts = Timestamp(d, t)
    assert ts.date == d
    assert ts.time == t


# noinspection PyTypeChecker
def test_init_invalid_types():
    """Test that initializing with wrong types raises TypeError."""
    with pytest.raises(TypeError):
        Timestamp("2025-01-02", time(0, 0))
    with pytest.raises(TypeError):
        Timestamp(date.today(), "00:00")


def test_from_components_valid():
    """Test creating Timestamp from individual components."""
    ts = Timestamp.from_components(2025, 12, 31, 23, 59, 59, 123456)
    assert isinstance(ts, Timestamp)
    assert ts.year == 2025
    assert ts.month == 12
    assert ts.day == 31
    assert ts.hour == 23
    assert ts.minute == 59
    assert ts.second == 59
    assert ts.microsecond == 123456


def test_from_components_invalid():
    """Test that invalid component values raise ValueError."""
    # Invalid month
    with pytest.raises(ValueError):
        Timestamp.from_components(2025, 13, 1)
    # Invalid day
    with pytest.raises(ValueError):
        Timestamp.from_components(2025, 2, 30)
    # Invalid hour
    with pytest.raises(ValueError):
        Timestamp.from_components(2025, 1, 1, hour=24)


def test_now_type():
    """Test that now() returns a Timestamp close to the current datetime."""
    ts_now = Timestamp.now()
    assert isinstance(ts_now, Timestamp)
    # Check that to_datetime returns a datetime close to now
    dt_now = datetime.now()
    delta = abs(ts_now.to_datetime() - dt_now)
    assert delta.total_seconds() < 1.0


def test_from_datetime():
    """Test creating Timestamp from a datetime object."""
    dt = datetime(2020, 5, 17, 10, 20, 30, 400)
    ts = Timestamp.from_datetime(dt)
    assert ts.date == date(2020, 5, 17)
    assert ts.time == time(10, 20, 30, 400)


# noinspection PyTypeChecker
def test_from_datetime_invalid():
    """Test that non-datetime input raises TypeError for from_datetime."""
    with pytest.raises(TypeError):
        Timestamp.from_datetime("2020-05-17T10:20:30")


def test_from_isoformat_valid():
    """Test creating Timestamp from a valid ISO format string."""
    iso = "2021-06-07T08:09:10.123456"
    ts = Timestamp.from_isoformat(iso)
    assert ts.date == date(2021, 6, 7)
    assert ts.time == time(8, 9, 10, 123456)


def test_from_isoformat_invalid():
    """Test that invalid ISO format string raises ValueError."""
    with pytest.raises(ValueError):
        Timestamp.from_isoformat("invalid-format")


def test_to_datetime_and_str_repr():
    """Test conversion to datetime, __str__, and __repr__ outputs."""
    ts = Timestamp.from_components(2022, 2, 22, 2, 22, 22)
    dt = ts.to_datetime()
    assert isinstance(dt, datetime)
    assert str(ts) == dt.isoformat()
    rep = repr(ts)
    assert "Timestamp(date=date(2022, 2, 22)" in rep


def test_float():
    """Test __float__ returns the POSIX timestamp (seconds since epoch) including fractional seconds."""
    ts = Timestamp.from_components(2000, 1, 2, 3, 4, 5, 600000)
    dt = ts.to_datetime()
    expected = dt.timestamp()
    assert float(ts) == pytest.approx(expected)


def test_comparisons():
    """Test comparison operators utilizing total_ordering."""
    ts1 = Timestamp.from_components(2021, 1, 1, 0, 0, 0)
    ts2 = Timestamp.from_components(2021, 1, 1, 0, 0, 1)
    assert ts1 < ts2
    assert ts1 <= ts2
    assert ts2 > ts1
    assert ts2 >= ts1
    assert ts1 != ts2
    ts1_clone = Timestamp.from_datetime(ts1.to_datetime())
    assert ts1 == ts1_clone
