__all__ = [
    "Functor",
    "fmap",
    "fm"
]

from typing import TypeVar, Generic
from pykell.typeclasses.typeclasses import typeclass, where
from pykell.functions.function import F
from pykell.operators.infix import infix

t = TypeVar("t")


@typeclass
class Functor(Generic[t]):
    @where
    def fmap(func, x: t) -> t:
        raise


def __fmap(f, x):
    return Functor.fmap(f, x)

fmap = F(__fmap)
fm = infix(__fmap)
