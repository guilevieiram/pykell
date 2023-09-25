__all__ = ["Monoid", "concat", "append"]
from typing import Generic, TypeVar
from pykell.typeclasses.typeclasses import typeclass, where
from pykell.functions.function import F
from pykell.functions.lib import foldr


M = TypeVar("M")


@typeclass
class Monoid(Generic[M]):
    @where
    def empty() -> M:
        raise

    @where
    def append(x: M, y: M) -> M:
        raise


@F
def append(x, y):
    return Monoid.append(x, y)


@F
def concat(xs):
    assert len(xs) > 0 and isinstance(xs, list)
    x = xs[0]
    t = type(x)
    return foldr | F(Monoid.append[t]) | Monoid.empty[t]() | xs
