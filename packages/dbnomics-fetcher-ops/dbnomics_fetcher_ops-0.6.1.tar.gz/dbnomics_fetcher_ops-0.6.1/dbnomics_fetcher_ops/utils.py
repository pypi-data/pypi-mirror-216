"""Utility functions."""

from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def find_index(predicate: Callable[[T], bool], items: Iterable[T], default=None) -> int:
    """Find the index of the first item satisfying the predicate."""
    return next((i for i, item in enumerate(items) if predicate(item)), default)


def without_none_values(d: dict) -> dict:
    """Return a copy of d without None values."""
    return {k: v for k, v in d.items() if v is not None}
