from pykell.typing.containers import Container
from typing import TypeVar, Union

Num = TypeVar("Num", bound=Union[int, float])


class Sum(Container[Num]):
    __name__ = "Sum"


class Prod(Container[Num]):
    __name__ = "Prod"


class Min(Container[Num]):
    __name__ = "Min"


class Max(Container[Num]):
    __name__ = "Max"


class All(Container[bool]):
    __name__ = "All"


class Any(Container[bool]):
    __name__ = "Any"
