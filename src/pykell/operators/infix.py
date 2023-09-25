__all__ = ["infix"]

from typing import Callable


class infix():
    def __init__(self, function: Callable):
        self._function: Callable = function

    @property
    def function(self):
        return self._function

    def __str__(self):
        return "Infix"
    
    def __repr__(self):
        return self.__str__()

    def __rlshift__(self, other):
        return infix(lambda x, self=self, other=other: self.function(other, x))

    def __rshift__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self._function(value1, value2)
