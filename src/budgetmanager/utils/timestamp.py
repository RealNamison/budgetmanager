#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for creating and manipulating Timestamp objects.

This module provides the Timestamp class which encapsulates separate date and time
components and offers methods for instantiation from various sources, conversion
to datetime and float timestamp, and comparison operations.
"""

from __future__ import annotations
from datetime import date, time, datetime
from functools import total_ordering


@total_ordering
class Timestamp:
    """
    A class to manage date and time as separate components.

    Provides methods to:
        - Instantiate with explicit date and time.
        - Instantiate from individual components (year, month, day, hour, minute, second, microsecond).
        - Create current timestamp.
        - Instantiate from datetime object.
        - Instantiate from ISO formatted string.
        - Convert to datetime.
        - Convert to POSIX float timestamp.
        - Compare Timestamp instances.
    """

    def __init__(self, date_obj: date, time_obj: time) -> None:
        """
        Initializes a Timestamp with date and time.

        Args:
            date_obj (date): The date component.
            time_obj (time): The time component.

        Raises:
            TypeError: If date_obj is not a datetime.date instance.
            TypeError: If time_obj is not a datetime.time instance.
        """
        if not isinstance(date_obj, date):
            raise TypeError(f"date_obj must be datetime.date, got {type(date_obj).__name__}")
        if not isinstance(time_obj, time):
            raise TypeError(f"time_obj must be datetime.time, got {type(time_obj).__name__}")
        self.date = date_obj
        self.time = time_obj

    @property
    def year(self) -> int:
        """int: The year component of the Timestamp."""
        return self.date.year

    @property
    def month(self) -> int:
        """int: The month component of the Timestamp."""
        return self.date.month

    @property
    def day(self) -> int:
        """int: The day component of the Timestamp."""
        return self.date.day

    @property
    def hour(self) -> int:
        """int: The hour component of the Timestamp."""
        return self.time.hour

    @property
    def minute(self) -> int:
        """int: The minute component of the Timestamp."""
        return self.time.minute

    @property
    def second(self) -> int:
        """int: The second component of the Timestamp."""
        return self.time.second

    @property
    def microsecond(self) -> int:
        """int: The microsecond component of the Timestamp."""
        return self.time.microsecond

    @classmethod
    def from_components(
            cls,
            year: int,
            month: int,
            day: int,
            hour: int = 0,
            minute: int = 0,
            second: int = 0,
            microsecond: int = 0
    ) -> Timestamp:
        """
        Creates a Timestamp from individual date and time components.

        Args:
            year (int): The year component.
            month (int): The month component (1-12).
            day (int): The day component (1-31).
            hour (int): The hour component (0-23). Defaults to 0.
            minute (int): The minute component (0-59). Defaults to 0.
            second (int): The second component (0-59). Defaults to 0.
            microsecond (int): The microsecond component (0-999999). Defaults to 0.

        Returns:
            Timestamp: A Timestamp representing the specified components.

        Raises:
            ValueError: If the provided components do not form a valid date or time.
        """
        date_obj = date(year, month, day)
        time_obj = time(hour, minute, second, microsecond)
        return cls(date_obj, time_obj)

    @classmethod
    def now(cls) -> Timestamp:
        """
        Creates a Timestamp for the current local date and time.

        Returns:
            Timestamp: A new Timestamp object set to the current date and time.
        """
        now_dt = datetime.now()
        return cls(now_dt.date(), now_dt.time())

    @classmethod
    def from_datetime(cls, dt: datetime) -> Timestamp:
        """
        Creates a Timestamp from a datetime object.

        Args:
            dt (datetime): A datetime instance to convert.

        Returns:
            Timestamp: A Timestamp representing the same date and time as dt.

        Raises:
            TypeError: If dt is not a datetime.datetime instance.
        """
        if not isinstance(dt, datetime):
            raise TypeError(f"dt must be datetime.datetime, got {type(dt).__name__}")
        return cls(dt.date(), dt.time())

    @classmethod
    def from_isoformat(cls, iso_str: str) -> Timestamp:
        """
        Creates a Timestamp from an ISO 8601 formatted string.

        Args:
            iso_str (str): A string in ISO format 'YYYY-MM-DD[T]HH:MM:SS[.ffffff]'.

        Returns:
            Timestamp: A Timestamp parsed from the given string.

        Raises:
            ValueError: If iso_str is not a valid ISO format string.
        """
        try:
            dt = datetime.fromisoformat(iso_str)
        except ValueError as e:
            raise ValueError(f"Invalid ISO format string: {iso_str}") from e
        return cls(dt.date(), dt.time())

    def to_datetime(self) -> datetime:
        """
        Converts this Timestamp to a datetime object.

        Returns:
            datetime: A datetime combining the date and time of this Timestamp.
        """
        return datetime.combine(self.date, self.time)

    def to_isoformat(self) -> str:
        """
        Returns the ISO 8601 string representation of this Timestamp.

        Returns:
            str: The timestamp as an ISO formatted string.
        """
        return self.to_datetime().isoformat()

    def __float__(self) -> float:
        """
        Returns the POSIX timestamp (seconds since epoch) of this Timestamp.

        Returns:
            float: POSIX timestamp including fractional seconds.
        """
        return self.to_datetime().timestamp()

    def __str__(self) -> str:
        """
        Returns the ISO 8601 string representation of the Timestamp.

        Returns:
            str: The timestamp as an ISO formatted string.
        """
        return self.to_isoformat()

    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the Timestamp.

        Returns:
            str: The representation of the Timestamp including date and time.
        """
        # Represent using date() and time() without module prefix for readability
        date_part = f"date({self.date.year}, {self.date.month}, {self.date.day})"
        time_part = (
            f"time({self.time.hour}, {self.time.minute}, {self.time.second}, {self.time.microsecond})"
        )
        return f"{self.__class__.__name__}(date={date_part}, time={time_part})"

    def __eq__(self, other: object) -> bool:
        """
        Checks equality with another Timestamp.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if other is a Timestamp with the same date and time, False otherwise.
        """
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self.date == other.date and self.time == other.time

    def __lt__(self, other: object) -> bool:
        """
        Checks if this Timestamp is earlier than another.

        Args:
            other (Timestamp): The other Timestamp to compare.

        Returns:
            bool: True if this Timestamp is earlier than other, False otherwise.
        """
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self.to_datetime() < other.to_datetime()
