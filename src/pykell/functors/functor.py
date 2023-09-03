from typing import Generic, TypeVar
from pykell.typing.types import Function

__functors__ = []

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")


class Functor(Generic[A, B, C, D]):
    def __init__(self, fmap: Function[Function[A, B], Function[C, D]]):
        self.fmap = fmap

    def __call__(self, f: Function[A, B]) -> Function[C, D]:
        return self.fmap(f)

    def __enter__(self):
        global __functors__

        __functors__.append(self)

    def __exit__(self, *_):
        global __functors__

        __functors__.pop()
