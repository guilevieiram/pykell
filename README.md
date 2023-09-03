
<img src="./assets/pykell_logo.svg" style="margin: auto; max-height: 256px" alt="Pykell logo">

# Pykell

Python functional programming library inspired by Haskell.

This is a personal project to deepen my understanding of functional programming by implementing this DSL in python. 

It is open-source, so feel free to open issues and pull requests!

## Installing

We have a stable release under pypi:

```bash
pip install pykell
```

## Features

This DSL makes it easy to write functional programming patters with a clean syntax.

### Functions
This is an abstraction layer on top of Python regular functions and lambdas.

```python
from pykell.typing import Function
from pykell.functions import F

# Via a decorator pattern
@F
def f(x: int, y: float) -> float: return x + y

# via a lambda (with type hints support)
g = F[float, str](lambda x: f"This is a float: {x}")


# automatic curying:
f # Function[int, Function[float, float]]
f2 = f |2 # application via | operator
f2_ = f(2) # works just as fine!
my_float = f2 |1.5


# composition
h = f2 >> g # this will return ⃘⃘⃘⃘f ∘ g
h | 1.2 # This is a float: 3.2

# Chaining
x = f |2 |1.5
```
### Containers
These are well known containers that can make your life easyer when programming.
```python
from pykell.typing import Maybe, Just, Nothing, Error, Result

def f(x: int) -> Maybe[int]:
    return Just(x + 10) if x < 10 else Nothing()

def f(x: int) -> Result[int, Exception]:
    return Just(x + 10) if x < 10 else Error(Exception("This  is too big!!!"))

```

### Functors
This is some syntatic sugar to use functors in python.
```python
from pykell.typing import Function
from pykell.functors import Functor

@Functor
def int_to_str(f: Function[int, float]) -> Function[str, str]:
    return lambda x: str(f(int(x)))


# some functions
f = F[int, float](lambda x: x / 7)
g = F[int, float](lambda x: x * 8)

new_f: Function[str, str] = int_to_str(f) # this works

# But this is cleaner!
with int_to_str:
    # inside here all | calls go through the functor
    x = f |"1" # "0.14285714285714285"
    y = f |"3" # "24"
    z = f(7) # when calling with (), no functor is applied
```
### Containers
These are well known containers that can make your life easyer when programming.
```python
from pykell.typing import Maybe, Just, Nothing, Error, Result

def f(x: int) -> Maybe[int]:
    return Just(x + 10) if x < 10 else Nothing()

def f(x: int) -> Result[int, Exception]:
    return Just(x + 10) if x < 10 else Error(Exception("This  is too big!!!"))

```



### Arrays
This is inspired by other array language features but use haskells lazyness to do computations.

```python
from pykell.arrays import arr

result = (
    arr([1, 2, 3])
    .map(lambda x: x + 1)
    .filter(lambda x: x % 2 != 0)
    .fold(0, lambda acc, cur: cur + acc)
)

print(result._) # evaluates the expression:


# you can do infinite calculations with it!
def naturals(): 
    i = 0
    while True: 
        yield (i := i + 1)


result = (
    arr(naturals())
    .map(lambda x: x + 1)
    .filter(lambda x: x % 2 != 0)
    .take(10)
)

print(result._) # 3, 5, 7, ...
```


### Monads
This is a good one.
```python
from pykell.monads import MaybeMonad
from pykell.functions import F
from pykell.typing import Maybe, Just, Nothing

# define some functions we want to compose ...
f = F[int, Maybe[int]](lambda x: Just(x + 10) if x < 10 else Nothing())
g = F[int, Maybe[float]](lambda x: Just(x / 7) if x < 10 else Nothing())

# Play inside the monadic environment!
@MaybeMonad.do
def calculate(x):
    y: int = yield f(x)  # yield calls with the bind. 
                    # Think of it like the let! in f# or x <- ... in Haskell. 
    if y < 5: # besides the yield everything works as normal!
        return y + 5

    z: float = yield g(z)
    return z - 1.5

calculate(-10) # Just(5)
calculate(4)   # Just(2.0)
calculate(11)  # Nothing()
```

## Contributions
This is just an experiment. If you have any ideas of features you want to see in here please reach out!
