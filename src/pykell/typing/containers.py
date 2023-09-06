__all__ = [
    "Maybe",
    "Result",
    "Unit",
    "Just",
    "Error",
    "Nothing",
    "Either",
    "Left",
    "Right",
]

from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class Maybe(Generic[T]):
    ...


class Result(Generic[T, E]):
    ...


class Unit:
    ...


class Nothing(Maybe):
    def __str__(self):
        return "Nothing"

    def __repr__(self):
        return str(self)


class Just(Maybe, Result, Generic[T]):
    def __init__(self, val: T):
        self._value = val

    @property
    def value(self) -> T:
        return self._value

    def __str__(self):
        return f"Just {self.value}"

    def __repr__(self):
        return str(self)


class Error(Result, Generic[E]):
    def __init__(self, exception: E):
        self._exception = exception

    @property
    def value(self) -> E:
        return self._exception

    def __str__(self):
        return f"error {self.value}"

    def __repr__(self):
        return str(self)


L = TypeVar("L")
R = TypeVar("R")


class Either(Generic[L, R]):
    ...


class Left(Either, Generic[L]):
    def __init__(self, val: L):
        self._ = val

    @property
    def value(self) -> L:
        return self._


class Right(Either, Generic[R]):
    def __init__(self, val: R):
        self._ = val

    @property
    def value(self) -> R:
        return self._
