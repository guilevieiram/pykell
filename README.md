
<img src="./assets/pykell_logo.svg" style="margin: auto; max-height: 256px" alt="Pykell logo">

# Pykell

Python functional programming library inspired by Haskell.

This is a personal project to deepen my understanding of functional programming by implementing this DSL in python. 

It is open-source, so feel free to open issues and pull requests!


```haskell 
f = filter (\x -> x / 3 < 10)

g = (\x -> x - 2) . (\x -> x ^ 3)

x = fmap g (Just 5)                 -- Just 123

```

```python
f = filter |(lambda x: x / 3 < 10)  

g = F(lambda x: x - 2) < F(lambda x: x ** 3)

x = fmap |g |Just(5)                # Just 123
```

## Installing

We currently have a stable release under pypi:

```bash
pip install pykell
```

## Features
This DSL makes it easy to write functional programming patters with a clean syntax.

### Functions
This is an abstraction layer on top of Python regular functions and lambdas.

```python
from pykell.functions import F


# Via a decorator 
@F
def f(x: int, y: float) -> float: return x + y


# via a lambda (with type hints support)
g = F[float, str](lambda x: f"This is a float: {x}")



f               # type: Function[int, Function[float, float]]
f2 = f |2       # application via | operator
f2_ = f(2)      # works just as fine!
my_float = f2 |1.5



# Composition
h = f2 < g      # this will return f2 ∘ g
h | 1.2         # This is a float: 3.2


# Chaining calls 
x = f |2 |1.5

```

You have access to many of Haskells Prelude functions:
```python
from pykell.functions import map, filter, foldr, head, tail, all, any

map    |(lambda x: x * 2) |[1, 2, 3]    # [2, 4, 6]

filter |(lambda x: x < 2) |[0, 1, 3]    # [0, 1]


head |[1, 2, 3, 4]                      # 1
tail |[1, 2, 3, 4]                      # [2, 3, 4]


even = F[int, bool](lambda x: x%2==0)
all |even |[2, 3, 4]                    # False
any |even |[2, 3, 4]                    # True


# and many more ...
```


### Containers
These are well known containers that can make your life easyer when programming.
```python
from pykell.typing import Maybe, Just, Nothing 


def f(x: int) -> Maybe[int]:
    return Just(x + 10) if x < 10 else Nothing()
```

### Operators
Infix operators make the life of a Haskell programmer much easier and the 
code much more expressive. 

We provide here an API for that that can be used anywhere.

By convention, since python does not consider `$` or `*` as valid function names,
we keep infix operators with short (2 chars) names.

```python
from pykell.operators import infix

sm = infix(lambda x, y: x + y)

x = 5 <<sm>> 6                  # 11


def call_and_print(f, x):
    print("Calling!")
    return f(x)
cp = infix(call_and_print)

y = (lambda x: x * 3) <<cp>> 5  # 15
# Output: Calling
```


### TypeClasses
This is a very core concept in Haskell that we are able to simulate in this library.
It allows us to use Functors, Applicatives and Monads very easily!

Check out the example on how we define Functors with these typeclasses:

```haskell 
-- haskell
class Functor f where
    fmap :: (a -> b) -> f a - f b

instance Functor List where
    fmap g x = map g x
```

```python
# pykell
@typeclass
class Functor(Generic[f]):
    @where
    def fmap(g, x: f) -> f: ...

@Functor.fmap.instance(list)
def _(g, x): return map |g |x
```
### Functors
This is some syntatic sugar to use functors in python.
(infix notation included!)

```python
from pykell.functors import fmap, fm
from pykell.typing import Maybe, Just

f = lambda x: 2 * x + 3


f <<fm>> Just(5)    # Just 13

fmap |f |[1, 2, 3]  # [5, 7, 9]
```

You can define your own as well, just like in haskell
```python
from pykell.functors import Functor

@Functor.fmap.instance(MyType)
def _(f, x): ...
```

### Applicatives
Applicatives are all over the place in Haskell programming.
We provide an infix api to use them here:

```python
from pykell.functions import F
from pykell.typing import Just
from pykell.functors import fm
from pykell.applicative import ap

mul = F(lambda x, y: x * y)
x = mul <<fm>> Just(2) <<ap>> Just(5)   # Just 10
```

```Haskell
let x = (*) <$> Just 2 <*> Just 5       -- Just 10
```


### Monads
This is a good one. There is support for monadic do notation.

In this notation, `yield` and `return~` indicate you are doing a monadic computation.

The rest is just pure python!

```python
from pykell.typing import Maybe, Just, Nothing
from pykell.monads import do


# define some functions we want to compose ...
f = lambda x: Just(x + 10) if x < 10 else Nothing()
g = lambda x: Just(x / 7 ) if x < 10 else Nothing()



# compose them inside the do block!
@do[Maybe]
def calculate(x):
    y: int = yield f(x)     # yield calls with the bind. 
                            # Like the let! in F# or x <- ... in Haskell. 

    if y < 5:               # besides the yield everything works as normal!
        return Nothing()    # Normal return

    z: float = yield g(z)

    return~ z               # Monadic return with the '~'
                            # Like the return! in F# or return ... in Haskell.


calculate(-10)              # Just(5)
calculate(4)                # Just(2.0)
calculate(11)               # Nothing()
```


There are a couple of implementation for monadic types but feel free to do your own:
```python
from pykell.monads import Monad

@Monad.unit.instance(MyType)    # define a unit. Same as 'return' in Haskell
def _(x): ...

@Monad.bind.instance(MyType)    # define a bind. Same as '>>=' in Haskell
def _(x, f): ...
```


### Arrays
This is inspired by other array language features but use haskells lazyness to do computations.
The syntax is more Scala-like, But it is still a nice feature

```python
from pykell.arrays import arr

result = (
    arr([1, 2, 3])
    .map(lambda x: x + 1)
    .filter(lambda x: x % 2 != 0)
    .fold(0, lambda acc, cur: cur + acc)
)

print(result._)     # evaluates the expression:


# you can do infinite calculations with it!
def naturals(i=0): 
    while True: yield (i := i + 1)


result = (
    arr(naturals())
    .map(lambda x: x + 1)
    .filter(lambda x: x % 2 != 0)
    .take(10)
)

print(result._)     # 3, 5, 7, ...
```

## Contributions
This is just an experiment. If you have any ideas of features you want to see in here please reach out!
