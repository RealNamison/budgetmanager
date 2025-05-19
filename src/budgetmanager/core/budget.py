# src/budgetmanager/core/budget.py

from __future__ import annotations
from decimal import Decimal, InvalidOperation
from typing import Any


class Budget:
    """Represents a budget limit for a single category.

    Args:
        category (str): Name of the category.
        limit (Decimal): Maximum allowed expense for the category.

    Attributes:
        category (str): Category name.
        limit (Decimal): Budget limit.
    """

    def __init__(self, category: str, limit: Decimal) -> None:
        self.category = category
        self.limit = limit

    def to_dict(self) -> dict[str, str]:
        """Serialize Budget to a JSON-friendly dict.

        Returns:
            dict[str, str]: {'category': str, 'limit': str}
        """
        return {"category": self.category, "limit": str(self.limit)}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Budget:
        """Deserialize Budget from a dict.

        Args:
            data (dict[str, Any]): {'category': str, 'limit': str|Decimal}

        Returns:
            Budget: New instance.

        Raises:
            KeyError: Missing 'category' or 'limit'.
            ValueError: Invalid limit value.
        """
        try:
            category = data["category"]
            raw = data["limit"]
        except KeyError as e:
            raise KeyError(f"Missing key in budget data: {e}") from e

        try:
            limit = raw if isinstance(raw, Decimal) else Decimal(str(raw))
        except (InvalidOperation, ValueError) as e:
            raise ValueError(f"Invalid limit for budget: {raw}") from e

        return cls(category=category, limit=limit)
