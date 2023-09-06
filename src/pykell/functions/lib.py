## providing common haskell functions
__all__ = [
    "map",
    "filter",
    "foldl",
    "foldr",
    "head",
    "tail",
    "init",
    "last",
    "reverse",
    "concat",
    "take",
    "drop",
    "drop_while",
    "take_while",
    "all",
    "any",
    "zip",
    "zip_with",
]

from typing import List, TypeVar
from pykell.functions.function import F
from pykell.typing.types import Function

T = TypeVar("T", covariant=True)
U = TypeVar("U")
A = TypeVar("A")
B = TypeVar("B")


@F
def map(f: Function, xs: List) -> List:
    return [f(x) for x in xs]


@F
def filter(f: Function, xs: List) -> List:
    return [x for x in xs if f(x)]


@F
def foldl(f: Function, zero, xs: List):
    return [zero := f(zero)(x) for x in xs][-1]


@F
def foldr(f: Function, zero, xs: List):
    return [zero := f(x)(zero) for x in xs[::-1]][-1]

@F
def head(xs: List):
    return xs[0]


@F
def tail(xs: List):
    return xs[1:]


@F
def init(xs: List):
    return xs[:-1]


@F
def last(xs: List):
    return xs[-1]


@F
def reverse(xs: List):
    return xs[::-1]


@F
def concat(xxs: List[List]):
    return foldr | (lambda xs: lambda ys: xs + ys) | [] | xxs


@F
def take(n: int, xs: List):
    return xs[:n]


@F
def drop(n: int, xs: List):
    return xs[n:]


@F
def take_while(f: Function, xs: List):
    res = []
    for x in xs:
        if not f(x):
            break
        res.append(x)
    return res


@F
def drop_while(f: Function, xs: List):
    i = 0
    for i, x in enumerate(xs):
        if not f(x):
            break
    return xs[i:]


@F
def all(predicate: Function, xs: List):
    return foldr | (lambda val: lambda acc: predicate(val) and acc) | True | xs


@F
def any(predicate: Function, xs: List):
    return foldr | (lambda val: lambda acc: predicate(val) or acc) | False | xs


@F
def zip(xs: List, ys: List):
    idx = min(len(xs), len(ys))
    return [(xs[i], ys[i]) for i in range(idx)]


@F
def zip_with(f: Function, xs, ys):
    return map | f | (zip | xs | ys)


@F 
def sum(xs):
    return foldr |(lambda x:lambda y: x + y) |0 |xs
