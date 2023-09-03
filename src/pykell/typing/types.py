__all__ = ["Function"]
from typing import TypeVar, Callable

A = TypeVar("A")
B = TypeVar("B")

Function = Callable[[A], B]
