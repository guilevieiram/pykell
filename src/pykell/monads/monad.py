__all__ = ["Monad", "do"]
from typing import Generic, TypeVar
from pykell.typeclasses.typeclass import typeclass, where
from pykell.monads.helpers import convert


M = TypeVar("M")


@typeclass
class Monad(Generic[M]):
    @where
    def bind(x: M, f) -> M:
        raise

    @where
    def unit(x) -> M:
        raise


class Do:
    def __getitem__(self, __name):
        return lambda func: convert(func, Monad.bind[__name], Monad.unit[__name])


do = Do()


if __name__ == "__main__":
    from pykell.typing.containers import Maybe, Just, Nothing

    @Monad.bind.instance(Maybe)
    def _(x, f):
        if isinstance(x, Nothing):
            return Nothing()
        return f(x.value)

    @Monad.unit.instance(Maybe)
    def _(x):
        return Just(x)

    f = lambda x: Nothing() if x < 10 else Just(x + 10)
    g = lambda x: Nothing() if x < 10 else Just(x * 10)

    Monad.bind(Just(30), f)

    @do[Maybe]
    def result(x):
        y = yield f(x)
        print(y)
        z = yield g(y)
        return x + z

    print(result(20))


if False:
    """haskell
    zz = do
        x <- Just 30
        y <- f x
        z <- g y
        return z
    """
    """pykell
    @Monad.do
    def zz(x):
        y = yield f(x)
        z = yield g(y)
        return z
    zz(Just(30))
    """
    # one liner lambdas
    M = Maybe
    zz = Monad.bind[M](
        Just(30),
        lambda x: Monad.bind[M](
            f(x), lambda y: Monad.bind[M](g(y), lambda z: Monad.unit[M](z))
        ),
    )

    # functioner
    # return becomes unit
    M = Maybe

    def zz(x):
        y = yield f(x)
        z = yield g(y)
        return Monad.unit[M](z)

    # becomes
    ## recursive change yield for functions definitions
    def zzz(x):
        def __def__1(y):
            z = yield g(y)
            return Monad.unit[M](z)

        return Monad.bind[M](f(x), lambda y: __def__1(y))

    # becomes
    def zzzz(x):
        def __def__1(y):
            def __def__2(z):
                return Monad.unit[M](z)

            return Monad.bind[M](g(y), lambda z: __def__2(z))

        return Monad.bind[M](f(x), lambda y: __def__1(y))

    zzzz(20)  # Just 300

    # another example
    @Monad[Maybe].do
    def k(x):
        y = yield f(x)
        print(y)
        if y < 10:
            return y + 10
        z = yield g(y)
        return z + y

    M = Maybe

    def kk(x):  # returns to units
        y = yield f(x)
        print(y)
        if y < 10:
            return Monad.unit[M](y + 10)
        z = yield g(y)
        return Monad.unit[M](z + y)

    # becomes
    ## recursive change yield for functions definitions
    def kkk(x):
        def __def__1(y):
            print(y)
            if y < 10:
                return Monad.unit[M](y + 10)
            z = yield g(y)
            return Monad.unit[M](z + y)

        return Monad.bind[M](f(x), lambda y: __def__1(y))

    # becomes
    def kkkk(x):
        def __def__1(y):
            def __def__2(z):
                return Monad.unit[M](z + y)

            print(y)
            if y < 10:
                return Monad.unit[M](y + 10)

            return Monad.bind[M](g(y), lambda z: __def__2(z))

        return Monad.bind[M](f(x), lambda y: __def__1(y))

    kkkk(10)  # works, .... but I dont wanna do it by hand
    # we kinda need to give the M value beforehand, as it does not infer weel
    # at least for the units
