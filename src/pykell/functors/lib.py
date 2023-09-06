from pykell.functions.function import F
from pykell.typing.containers import (
    Maybe,
    Nothing,
    Just,
    Either,
    Left,
    Right
)
from pykell.functors.functor import Functor


@Functor(list)
def list_functor(f, xs): 
    return [f(x) for x in xs]

@Functor(Maybe)
def maybe_functor(f, mx):
    if isinstance(mx, Nothing): return Nothing()
    return Just(f(mx.value))


@Functor(Either)
def either_functor(f, ex):
    if isinstance(ex, Left): return Left(f(ex.value))
    return Right(f(ex.value))

@Functor(F)
def f_functor(f, g):
    return f >> g

