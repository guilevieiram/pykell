from pykell.applicative.applicative import Applicative
from pykell.typing.containers import Maybe, Just, Nothing, Result, Error

@Applicative.applicative.instance(Maybe)
def _(f, x):
    if isinstance(f, Nothing) or isinstance(x, Nothing):
        return Nothing()
    return Just(f.value(x.value))

@Applicative.applicative.instance(Result)
def _(f, x):
    if isinstance(f, Error):
        return f
    if isinstance(x, Error):
        return x
    assert isinstance(f, Just) and isinstance(x, Just)
    return Just(f.value(x.value))

@Applicative.applicative.instance(list)
def _(fs, xs):
    return [
        f(x)
        for x in xs
        for f in fs
    ]
