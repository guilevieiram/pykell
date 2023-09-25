__all__ = [
    "Functor",
    "fmap",
]

from typing import TypeVar, Generic
from pykell.typeclasses.typeclasses import typeclass, where
from pykell.functions.function import F

f = TypeVar("f")


@typeclass
class Functor(Generic[f]):
    @where
    def fmap(func, x: f) -> f:
        raise


@F
def fmap(f, x):
    return Functor.fmap(f, x)
