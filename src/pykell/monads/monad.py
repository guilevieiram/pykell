__all__ = ["Monad", "do", "bi"]
from typing import Generic, TypeVar
from pykell.typeclasses.typeclasses import typeclass, where
from pykell.monads.helpers import convert
from pykell.operators.infix import infix


M = TypeVar("M")


@typeclass
class Monad(Generic[M]):
    @where
    def bind(x: M, f) -> M:
        raise

    @where
    def unit(x) -> M:
        raise


class Do:
    def __getitem__(self, __name):
        return lambda func: convert(func, Monad.bind[__name], Monad.unit[__name])


do = Do()


bi = infix(lambda x, f: Monad.bind(x, f))
