__all__ = ["arr"]


class arr:
    def __init__(self, i):
        self._iter = (_ for _ in i)
        self._value = None

    def __next__(self):
        return next(self._iter)

    def __iter__(self):
        yield from self._iter

    def __str__(self):
        return f"array: {self._iter}"

    def map(self, f):
        return arr((f(_) for _ in self))

    def fold(self, state, g):
        def gen(s):
            for x in self:
                s = g(s, x)

            yield s

        return arr((_ for _ in gen(state)))

    def take(self, n):
        return arr([next(self) for _ in range(n)])

    def filter(self, f):
        return arr((_ for _ in self if f(_)))

    @property
    def _(self):
        if self._value is None:
            self._value = list(self._iter)
        return self._value


if __name__ == "__main__":
    res = (
        arr([1, 2, 3])
        .map(lambda x: x + 1)
        .filter(lambda x: x % 2 != 0)
        .fold(0, lambda acc, cur: cur + acc)
    )
    print(res._)
