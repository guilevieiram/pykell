"""
    Containers in Pykell
    -----------------------------------------------------------
    
    Container types provide a very intuitive api in Haskell
    for options, lists, eithers, results, ...

    We implemented an implentation of those types here in 
    pykell.
"""

# Maybe
from pykell.typing import Maybe, Just, Nothing


def f(x: int) -> Maybe[int]:
    if x < 10:
        return Nothing()
    return Just(x + 2)


# result
from pykell.typing import Result, Just, Error


def g(x: int) -> Result[int, ValueError]:
    if x > 0:
        return Just(x + 10)
    return Error(ValueError("Only negative values allowed"))


# Either
from pykell.typing import Either, Left, Right


def h(x: str) -> Either[int, str]:
    if x:
        return Left(len(x))
    return Right("There was no string!")
