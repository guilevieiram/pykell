from pykell.monads.monad import Monad
from pykell.typing.containers import Maybe, Just, Nothing


@Monad.bind.instance(Maybe)
def _(x, f):
    if isinstance(x, Nothing):
        return Nothing()
    return f(x.value)


@Monad.unit.instance(Maybe)
def _(x):
    return Just(x)


@Monad.bind.instance(list)
def _(xs, f):
    res = []
    for x in xs:
        res.extend(f(x))
    return res


@Monad.unit.instance(list)
def _(x):
    return [x]
