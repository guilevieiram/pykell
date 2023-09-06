__all__ = [
    "Functor",
    "fmap",
]
from pykell.functions.function import F


class Functor: 
    __functors__ = {}

    def __init__(self, f_type: type):
        self.__functors__[f_type] = self

    def fmap(self, f, x):
        return self._fmap(f, x)

    def __call__(self, fmap):
        self._fmap = fmap

@F
def fmap(f, x):
    for f_type, functor in Functor.__functors__.items():
        if isinstance(x, f_type):
            res = functor.fmap(f, x)
            return res
    raise Exception("Functor not defined for type {type(x)}")

