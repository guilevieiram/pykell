"""
    Typeclasses in Pykell
    -----------------------------------------------------------

    Typeclasses allow us to generalize behaviour associated
    with certain types.

    In pykell we provide an API for these constructs.
"""

from pykell.typeclasses import typeclass, where
from typing import TypeVar, Generic

# Define a new typeclass
# Examples of typeclasses include Functor and Monad

T = TypeVar("T")

@typeclass
class Equals(Generic[T]):
    @where
    def eq(x: T, y: T):
        return not Equals.neq(x, y)

    @where
    def neq(x: T, y: T):
        return not Equals.eq(x, y)


# Provide an instance for your typeclass
class MyInteger:
    val: int
    def __init__(self, val): 
        self.val = val

@Equals.eq.instance(MyInteger)
def _(x, y): return x.val == y.val


# Use the typeclass (types are infered on call time)
i1 = MyInteger(5)
i2 = MyInteger(1)

Equals.eq(i1, i2)   # False
Equals.neq(i1, i2)  # True
