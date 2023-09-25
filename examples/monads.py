"""
    Monads in Pykell
    -----------------------------------------------------------
    
    Hot topic in the FP world and available for you in pykell.


    We provide an adaptation of functors via Typeclasses and
    include a do-notation equivalent for monadic expressions.
"""

# Using monads

from pykell.monads import do
from pykell.typing import Maybe, Just, Nothing


@do[Maybe]  # Provide which monad to use
def compute(x):
    y = yield Just(5)  # Assign via binding (y <- Just 5)

    if x < 50:  # rest works fine!
        print("x is too small")
        return Nothing()  # usual Python return

    z = x + y

    return ~(z + 10)  # monadic return (wraps the value)


z = compute(500)  # Just : 515
z = compute(50)  # Just : 65
z = compute(30)  # Output "x is to small"
# Nothing


# Defining your own monads via typeclasses
from pykell.monads import Monad


@Monad.bind.instance(dict)
def _(x, f):
    return {key: f(val) for key, val in x.items()}


@Monad.unit.instance(dict)
def _(x):
    return {"val": x}


@do[dict]
def dict_compute():
    x = yield {"a": 5, "b": 6}
    y = x + 6
    return y * 10


dict_compute()  # {'a': 110, 'b': 120}
