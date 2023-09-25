"""
    Applicatives in Pykell
    -----------------------------------------------------------

    We provide an interface to use applicatives in pykell
    via infix operators!

    They work really well with Functors and pykell Functions.
"""
from pykell.functions import F
from pykell.functors import fm
from pykell.typing import Just

from pykell.applicative import ap


@F
def summing(x, y):
    return x + y

x = summing <<fm>> Just(5) <<ap>> Just(3)   # Just : 8

y = (
    [lambda x: x * 2, lambda y: y + 1] 
    <<ap>> [1, 2, 3]
)   # [2, 2, 4, 3, 6, 4]

