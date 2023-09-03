__all__ = ["ListMonad"]
from typing import Generic, TypeVar, Callable, List

from pykell.monads.abstract import Monad

T = TypeVar("T")
U = TypeVar("U")


class ListMonad(Generic[T], Monad):
    @staticmethod
    def unit(val: T) -> List[T]:
        return [val]

    @staticmethod
    def bind(val: List[T], f: Callable[[T], List[U]]) -> List[U]:
        return [u for v in val for u in f(v)]
