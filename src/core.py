import sys
from functools import reduce
from operator import or_
from random import randint
from typing import Dict, List, Set, Tuple, Union, get_args, get_origin

from hypothesis import given
from hypothesis.strategies import (
    binary,
    booleans,
    characters,
    complex_numbers,
    dictionaries,
    floats,
    integers,
    lists,
    sets,
    tuples,
)

# Annoyingly, `typing.get_origin(str | int) == types.UnionType` after Python 3.10,
# but `typing.get_origin(str | int) == typing.Union` before
if sys.version_info >= (3, 10):
    from types import UnionType
    from typing import TypeAlias

    UnionType_: TypeAlias = UnionType
else:
    from typing_extensions import TypeAlias

    UnionType_: TypeAlias = Union


def translate(type_: type):
    """ """
    origin, args = get_origin(type_), get_args(type_)
    if origin is None:
        # Translate class to strategy
        if type_ == bool:
            return booleans()
        elif type_ == bytes:
            return binary()
        elif type_ == complex:
            return complex_numbers()
        elif type_ == float:
            return floats()
        elif type_ == int:
            return integers()
        elif type_ == str:
            return characters()
    elif (origin == UnionType_) or (origin == Union):
        return reduce(or_, map(translate, args))
    else:
        # TODO: assert `args` has correct length for each case
        if (origin == dict) or (origin == Dict):
            return dictionaries(*map(translate, args))
        elif (origin == list) or (origin == List):
            return lists(translate(args[0]))
        elif (origin == set) or (origin == Set):
            return sets(translate(args[0]))
        elif (origin == tuple) or (origin == Tuple):
            # As per https://docs.python.org/3/library/typing.html#annotating-tuples
            # if two arguments are provided the second one being `Ellipsis`
            # it is a tuple of varying length
            if (len(args) == 2) and (args[-1] == ...):
                return tuples(*map(translate, (args[0] for _ in range(randint(1, 10)))))
            return tuples(*map(translate, args))


def strategize(type_: type):
    return given(translate(type_))
