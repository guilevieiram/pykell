__all__ = [
    "Applicative",
    "ap"
]

from typing import TypeVar, Generic
from pykell.typeclasses.typeclasses import typeclass, where
from pykell.operators.infix import infix

f = TypeVar("f")

@typeclass
class Applicative(Generic[f]):
    @where
    def applicative(func: f, x):
        raise

def __applicative(func, x):
    return Applicative.applicative(func ,x)

ap = infix(__applicative)

