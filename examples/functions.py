"""
    Functions in Pykell
    -----------------------------------------------------------

    Pykell provides a module for wrapping functions and 
    give them extra functionality and Haskelly syntax.

    There is also some standard library functions that we've
    reimplemented in the pykell way.


    Here we are going to cover a couple of those examples!
"""


# Lets create a function!
from pykell.functions import F


# Decorate it to convert to pykell functions
@F
def f(x: int, y: int) -> int:
    return x + y


# Or create one via lambdas
g = F[int, int](lambda x: x * 2)


# Calling a function via the | (pipe) operator or () operator
x = g | 3  # 6
x = g(3)  # 6

y = f | 4 | 6  # 10


# Automatic currying!
sum_four = f | 4  # y -> y + 4
z = sum_four | 1  # 5


# Composition of functions
h = f < g  # equivalent of f∘g = h : x -> y -> 2 * x + y
# or the regular "." composition in haskell
w = h | 2 | 4  # 8


# Alternative notation
sum_four_then_double = sum_four > g
fourteen = sum_four_then_double | 3


# Standard library
from pykell.functions import (
    map,
    filter,
    foldr,
    zip,
    zip_with,
    head,
    init,
    tail,
    last,
    reverse,
    concat,
    take,
)


# An example list
my_list = [*range(10)]  # 0..9


# map
double_of_list = map | (lambda x: x * 2) | my_list
double = map | (lambda x: x * 2)  # via partial application
double_of_list = double | my_list


# filter
list_evens = filter | (lambda x: x % 2 == 0) | my_list


# folding
@F
def sum_both(x, y):
    return x + y


summed_list = foldr | sum_both | my_list


# zip and zip_with
other_list = [*range(10, 20)]  # 10..19

zipped = zip | my_list | other_list

zipped_with_product = (
    zip_with | (lambda x: lambda y: x * y) | my_list | other_list  # curried function
)

# head, init, tail, last
x = head | my_list  # 0
xs = tail | my_list  # 1..9
xs = init | my_list  # 0..8
x = last | my_list  # 9


# reverse
tsil_ym = reverse | my_list

# concat
palidromic = concat | [my_list, tsil_ym]

# take
first_five = take | 5 | my_list
