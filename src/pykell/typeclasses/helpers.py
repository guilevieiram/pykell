__all__ = ["find_mro_LCA", "FunctionRepo"]

from typing import List, Set, Tuple, Dict, Callable


def find_mro_LCA(
    positions_to_check: List[int], available_types: Set[type], args: Tuple
) -> type:
    arguments = [args[i] for i in positions_to_check]
    mros = [
        filter(lambda x: x in available_types, type(argument).mro())
        for argument in arguments
    ]
    mro0 = list(mros[0])
    mron = [set(mro) for mro in mros[1:]]
    t = mro0[0]
    for t in mro0:  # finding the LCA
        if all(t in mro for mro in mron):
            break
    return t


class FunctionRepo:
    def __init__(self, f):
        self._function_repo: Dict[type, Callable] = {object: f}
        self._allowed_types: Set[type] = {object}
        self._marked_arguments_indexes: List[int] = []

    def __call__(self, *args):
        _type = find_mro_LCA(self.marked_argument_indexes, self.allowed_types, args)
        return self.repository[_type](*args)

    def instance(self, _type):
        def wrap(f):
            self.update_callers(_type, f)
            return f

        return wrap

    def __getitem__(self, __type: type) -> Callable:
        return self.repository[__type]

    def update_callers(self, t: type, f: Callable):
        self._allowed_types.add(t)
        self._function_repo[t] = f

    @property
    def repository(self):
        return self._function_repo

    @property
    def allowed_types(self):
        return self._allowed_types

    @property
    def base_function(self):
        return self._function_repo[object]

    @property
    def marked_argument_indexes(self):
        return self._marked_arguments_indexes

    @marked_argument_indexes.setter
    def marked_argument_indexes(self, args: List[int]):
        self._marked_arguments_indexes = args
