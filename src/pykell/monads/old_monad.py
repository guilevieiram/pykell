"""
__all__ = ["Monad"]
import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

from pykell.monads.helpers import count_leading_space, proc

M = TypeVar("M")


class Monad(ABC, Generic[M]):
    @staticmethod
    @abstractmethod
    def unit(val) -> M:
        ...

    @staticmethod
    @abstractmethod
    def bind(val: M, f):
        ...

    @classmethod
    def do(cls, __f):
        src = inspect.getsource(__f)
        lines = src.split("\n")
        signature = lines[1]
        ident_count = count_leading_space(signature)
        [pre, pos, *_] = signature.split(")")
        [defi, args, *_] = pre.split("(")
        has_args = args.replace(" ", "") != ""
        signature = f"{defi}({args}{',' if has_args else ''} __monad__=__monad__){pos}"
        src = [f"{signature}"]
        lines = lines[2:]
        for i, line in enumerate(lines):
            if "return" in line:
                ident, expr = line.split("return")
                src.append(f"{ident}return __monad__.unit({expr.replace(' ', '')})")
                continue
            if "yield" in line:
                line = line.replace("yield", "")
                [left_with_ident, right, *_] = line.split("=")
                ident = " " * count_leading_space(left_with_ident)
                left = left_with_ident.lstrip(" ").rstrip(" ")
                right = right.lstrip(" ")
                src.append(
                    f"{ident}return __monad__.bind({right}, lambda {left}:__def__{i}({left}))"
                )
                continue
            src.append(line)
        code = "\n".join([l[ident_count:] for l in proc(src)])
        local: Dict[str, Any] = {"__monad__": cls}
        exec(code, __f.__globals__, local)
        new_function = local[__f.__name__]
        new_function.source_code = code
        return new_function

__all__ = ["MaybeMonad"]

from typing import TypeVar, Callable

from pykell.monads.abstract import Monad
from pykell.typing.containers import Maybe, Just, Nothing

T = TypeVar("T")
U = TypeVar("U")


class MaybeMonad(Monad[Maybe[T]]):
    @staticmethod
    def unit(val: T) -> Maybe[T]:
        return Just(val)

    @staticmethod
    def bind(val: Maybe[T], f: Callable[[T], Maybe[U]]) -> Maybe[U]:
        if isinstance(val, Nothing):
            return Nothing()
        assert isinstance(val, Just)
        return f(val.value)


if __name__ == "__main__":

    def f(x: int) -> Maybe[float]:
        if x < 10:
            return Just(x + 10)
        else:
            return Nothing()

    def h(x: int) -> Maybe[float]:
        if x < 10:
            return Just(x / 10)
        else:
            return Nothing()

    # encapsulates the f variable
    @MaybeMonad.do
    def result(x):
        y = yield f(x)
        return y

    print(result(3))

__all__ = ["ListMonad"]
from typing import Generic, TypeVar, Callable, List

from pykell.monads.abstract import Monad

T = TypeVar("T")
U = TypeVar("U")


class ListMonad(Generic[T], Monad):
    @staticmethod
    def unit(val: T) -> List[T]:
        return [val]

    @staticmethod
    def bind(val: List[T], f: Callable[[T], List[U]]) -> List[U]:
        return [u for v in val for u in f(v)]
"""
