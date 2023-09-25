"""
    Monoids in Pykell
    -----------------------------------------------------------
    
    Monoids are a key concept in Haskell that can generalize 
    binary operations between any objects.

    In pykell we offer an API based on typeclasses and a 
    slice of the standard library.
"""

from pykell.monoids import append, concat


two_lists = append | [1, 2, 3] | [2, 3, 4]  # [1, 2, 3, 2, 3, 4]

many_lists = concat | [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # [1, 2, 3, 4, 5, 6, 7, 8, 9]


# for numeric (real or integer) values, there are many possible
# monoids. So we provide a couple of them in the library
from pykell.monoids import Sum, Prod, Min
from pykell.functions import map

int_list = [*range(1, 11)]  # [1..10]

int_sum = concat << (map | Sum) | int_list  # Sum : 55
int_prod = concat << (map | Prod) | int_list  # Prod : 3628800
int_min = concat << (map | Min) | int_list  # Min : 1


# Of course you can define your own monoids!
from pykell.monoids import Monoid
from dataclasses import dataclass


@dataclass
class Order:
    quantity: int
    total_value: float


@Monoid.empty.instance(Order)
def _():
    return Order(0, 0)


@Monoid.append.instance(Order)
def _(x, y):
    return Order(x.quantity + y.quantity, x.total_value + y.total_value)


orders = [Order(5, 1.5), Order(10, 4.5), Order(4, 9.9)]

resume = concat | orders  # Order(quantity=19, total_value=15.9)
