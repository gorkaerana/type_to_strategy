import sys
from functools import reduce
from itertools import repeat
from operator import or_
from random import randint
from typing import Dict, FrozenSet, List, Set, Tuple, Union, get_args, get_origin

from hypothesis import given
from hypothesis.strategies import (
    binary,
    booleans,
    characters,
    complex_numbers,
    dictionaries,
    floats,
    frozensets,
    integers,
    lists,
    none,
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
        if type_ is bool:
            return booleans()
        elif type_ is bytes:
            return binary()
        elif type_ is complex:
            return complex_numbers()
        elif type_ is float:
            return floats()
        elif type_ is int:
            return integers()
        elif type_ is str:
            return characters()
        elif type_ is None:
            return none()
    elif (origin == UnionType_) or (origin == Union):
        return reduce(or_, map(translate, args))
    else:
        first_arg, *_ = args
        # TODO: assert `args` has correct length for each case
        if (origin is dict) or (origin is Dict):
            return dictionaries(*map(translate, args))
        elif (origin is frozenset) or (origin is FrozenSet):
            return frozensets(translate(first_arg))
        elif (origin is list) or (origin is List):
            return lists(translate(first_arg))
        elif (origin is set) or (origin is Set):
            return sets(translate(first_arg))
        elif (origin is tuple) or (origin is Tuple):
            # As per https://docs.python.org/3/library/typing.html#annotating-tuples
            # if two arguments are provided, the second one being `Ellipsis`,
            # it is a tuple of varying length
            if (len(args) == 2) and (args[1] is ...):
                return tuples(*map(translate, repeat(first_arg, randint(1, 10))))
            return tuples(*map(translate, args))


def strategize(type_: type):
    return given(translate(type_))
