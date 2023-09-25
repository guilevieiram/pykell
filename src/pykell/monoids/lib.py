from pykell.monoids.monoid import Monoid
from pykell.monoids.containers import Sum, Prod, Min, Max, Any, All


@Monoid.empty.instance(Sum)
def _():
    return Sum(0)


@Monoid.append.instance(Sum)
def _(x, y):
    return Sum(x.value + y.value)


@Monoid.empty.instance(Prod)
def _():
    return Prod(1)


@Monoid.append.instance(Prod)
def _(x, y):
    return Prod(x.value * y.value)


@Monoid.empty.instance(Min)
def _():
    return Min(float("inf"))


@Monoid.append.instance(Min)
def _(x, y):
    return Min(min(x.value, y.value))


@Monoid.empty.instance(Max)
def _():
    return Max(float("-inf"))


@Monoid.append.instance(Max)
def _(x, y):
    return Max(max(x.value, y.value))


@Monoid.empty.instance(All)
def _():
    return All(True)


@Monoid.append.instance(All)
def _(x, y):
    return All(x.value and y.value)


@Monoid.empty.instance(Any)
def _():
    return Any(False)


@Monoid.append.instance(Any)
def _(x, y):
    return Any(x.value or y.value)


@Monoid.empty.instance(list)
def _():
    return []


@Monoid.append.instance(list)
def _(x, y):
    return [*x, *y]
