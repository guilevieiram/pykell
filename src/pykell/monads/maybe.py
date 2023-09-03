__all__ = ["MaybeMonad"]

from typing import Generic, TypeVar, Callable

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


