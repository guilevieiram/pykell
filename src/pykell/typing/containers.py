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
    "Container",
]

from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class Container(Generic[T]):
    __name__ = "Container"

    def __init__(self, __value: T):
        self.__value = __value

    @property
    def value(self) -> T:
        return self.__value

    def __repr__(self):
        return f"{self.__name__} : {self.value}"

    def __str__(self):
        return self.__repr__()


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


class Just(Maybe, Result, Container[T]):
    __name__ = "Just"


class Error(Result, Container[E]):
    __name__ = "Error"


L = TypeVar("L")
R = TypeVar("R")


class Either(Generic[L, R]):
    ...


class Left(Either, Container[L]):
    __name__ = "Left"


class Right(Either, Container[R]):
    __name__ = "Right"
