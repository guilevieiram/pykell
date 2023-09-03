from typing import Generic, TypeVar, overload, Callable, Optional
import inspect
from typing_extensions import TypeVarTuple
from pykell.typing.types import Function
from pykell.functors.functor import __functors__

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

Ts = TypeVarTuple("Ts")
T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")


class F(Generic[A, B]):
    @property
    def f(self) -> Function[A, B]:
        return self._f  # type: ignore

    @overload
    def __init__(self: "F[None, B]", f: Callable[[], B], argc: Optional[int] = None):
        ...

    @overload
    def __init__(self: "F[A, B]", f: Callable[[A], B], argc: Optional[int] = None):
        ...

    @overload
    def __init__(
        self: "F[A, F[T1, T]]", f: Callable[[A, T1], T], argc: Optional[int] = None
    ):
        ...

    @overload
    def __init__(
        self: "F[A, F[T1, F[T2, T]]]",
        f: Callable[[A, T1, T2], T],
        argc: Optional[int] = None,
    ):
        ...

    def __init__(self, f: Callable, argc: Optional[int] = None):
        if argc is None:
            argc = len(inspect.signature(f).parameters)

        if argc == 1:
            self._f = f

            return

        self._f = lambda x: F(lambda *xs: f(x, *xs), argc - 1)

    def __call__(self, arg: A) -> B:
        f = self.f
        return f(arg)

    def __or__(self, arg: A) -> B:
        f = self.f
        global __functors__
        for functor in __functors__:
            f = functor(f)
        return f(arg)

    def __str__(self):
        return f"Function {self.f.__name__}"

    def __repr__(self):
        return str(self)

    def __rshift__(self, g: "F[B, C]") -> "F[A, C]":
        return F(lambda _: g.f(self.f(_)))

    def __lshift__(self, g: "F[C, A]") -> "F[C, B]":
        return F(lambda _: self.f(g.f(_)))


if __name__ == "__main__":

    @F
    def f(x: int, y: float) -> str:
        return str(x + y)

    @F
    def g(s: str) -> list[str]:
        return [*s]

    h = F[int, int](lambda x: x + 2)

    from pykell.functors.functor import Functor

    h = (f | 3) >> g
    i = h | 2.3

    @Functor
    def int_str(phi: Function[int, float]) -> Function[str, str]:
        return lambda x: str(phi(int(x)))

    a = F[int, float](lambda x: x / 7)
    b = F[int, float](lambda x: x * 8)

    # is this good notation? how does haskell does it?
    with int_str:
        y = a | "9"
        z = b | "8"
        print(y, z)
