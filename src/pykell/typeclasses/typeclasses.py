__all__ = ["typeclass", "where"]

from typing import Generic, TypeVar
import inspect

from pykell.typeclasses.helpers import FunctionRepo

where = FunctionRepo

T = TypeVar("T")


class TypeClass(type):
    def __new__(cls, name, bases, dct):
        function_repos = {
            key: value for key, value in dct.items() if isinstance(value, FunctionRepo)
        }
        dct = {
            key: value for key, value in dct.items() if key not in function_repos.keys()
        }
        new = super().__new__(cls, name, bases, dct)

        # getting the parameters of the class
        assert (
            len(parameters := new.__parameters__) == 1  # type: ignore
        ), "Only single parameter typeclasses are allowed"

        parameter = parameters[0]
        for name, func in function_repos.items():
            # collecting the position of the arguments marked as the required type
            args = [
                i
                for i, (_, v) in enumerate(
                    inspect.signature(func.base_function).parameters.items()
                )
                if v.annotation == parameter
            ]
            func.marked_argument_indexes = args
            setattr(new, name, func)

        return new


C = TypeVar("C")


def typeclass(cls: C) -> C:
    """Applying the TypeClass metaclass as a decorator"""
    return TypeClass(cls.__name__, cls.__bases__, dict(cls.__dict__))  # type: ignore
