"""
    Functors in Pykell
    -----------------------------------------------------------
    
    Functors are a very key concept in Haskell programming and
    lead to very clean and expressive code.

    Here we provide an adaptation of functors via Typeclasses.
"""

from pykell.functors import fmap

# You can use the default implementation for a couple of types
from pykell.typing import Just

new_list = fmap | (lambda x: x * 2) | [1, 2, 3]  # [2, 4, 6]
new_just = fmap | (lambda x: x + 5) | Just(2)  # Just 7


# For newly defined types you can provide an implementation
from pykell.functors import Functor


@Functor.fmap.instance(dict)
def _(f, x):
    return {key: f(val) for key, val in x.items()}


new_dict = fmap | (lambda x: x * 10) | {"a": 5, "b": 1}  # {'a': 50, 'b': 10}


# You can access direcly the fmap instance
# without it being implicited by the interpreter
Functor.fmap[list](lambda x: x + 8, [1, 2, 3])
