from pykell.functions.function import F
from pykell.typing.containers import Maybe, Nothing, Just, Either, Left, Right
from pykell.functors.functor import Functor


@Functor.fmap.instance(list)
def _(f, xs):
    return [f(x) for x in xs]


@Functor.fmap.instance(Maybe)
def _(f, mx):
    return Nothing() if isinstance(mx, Nothing) else Just(f(mx.value))


@Functor.fmap.instance(Either)
def _(f, ex):
    res = f(ex.value)
    return Left(res) if isinstance(ex, Left) else Right(res)


@Functor.fmap.instance(F)
def f_functor(f, g):
    return f >> g
