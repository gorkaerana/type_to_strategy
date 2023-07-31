from typing import List, Set, Dict, Tuple, get_origin, get_args

# from hypothesis.strategies._internal.lazy import LazyStrategy
from hypothesis.strategies import (
    booleans,
    binary,
    complex_numbers,
    dictionaries,
    floats,
    frozensets,
    integers,
    lists,
    sets,
    characters,
    tuples,
)


BUILTIN_TYPE_TO_TYPING_EQUIVALENT = {list: List, set: Set, dict: Dict, tuple: Tuple}

BUILTIN_TYPE_TO_N_TYPING_ARGS = {list: 1, set: 1, dict: 2, tuple: None}

BUILTIN_TYPE_TO_STRATEGIES = {
    bool: booleans,
    # bytearray: ...
    bytes: binary,
    complex: complex_numbers,
    dict: dictionaries,
    float: floats,
    frozenset: frozensets,
    int: integers,
    list: lists,
    set: sets,
    str: characters,
    tuple: tuples,
}

TYPING_TO_STRATEGIES = {List: lists, Set: sets, Dict: dictionaries, Tuple: tuples}

SIMPLE_TYPES_TO_STRATEGIES = BUILTIN_TYPE_TO_STRATEGIES | TYPING_TO_STRATEGIES

supported_types = set(SIMPLE_TYPES_TO_STRATEGIES.keys())


def is_simple_type(type_: type) -> bool:
    """Returns `True` for "simple" types (e.g.: `str`, `dict`, etc.), and `False`
    otherwise. Ideally, `is_simple_type(type_) == (not is_complex_type(type_))`"""
    return bool((get_origin(type_) is None) and (not get_args(type_)))


def is_composite_type(type_: type) -> bool:
    """Returns `True` for "complex" types (e.g.: `list[str]`, `dict[int, bool]`, etc.),
    and `False` otherwise."""
    return bool((get_origin(type_) is not None) or get_args(type_))


class WrongAmountTypeArguments(Exception):
    pass


# TODO: support `bytearray`
# TODO: support `typing.Any`?
# TODO: add sensible defaults to builtin types dict, list, set, tuple
# TODO: support union types
# TODO: support custom types
# TODO: support other standard library types
def translate(type_: type):  # -> LazyStrategy:
    """
    Algorithm:
    1.- Check for "simple" types
    2.- Check for "complex" types
    3.- Check for union types
    """
    if is_simple_type(type_) and (type_ in SIMPLE_TYPES_TO_STRATEGIES):
        return SIMPLE_TYPES_TO_STRATEGIES[type_]()
    if is_composite_type(type_):
        origin_type, type_args = get_origin(type_), get_args(type_)
        if origin_type in SIMPLE_TYPES_TO_STRATEGIES:
            for t in [dict, list, set, tuple]:
                if (
                    True
                    and (origin_type == t)
                    or (origin_type == BUILTIN_TYPE_TO_TYPING_EQUIVALENT[t])
                ):
                    if (
                        True
                        and ((n_args := BUILTIN_TYPE_TO_N_TYPING_ARGS[t]) is not None)
                        and (len_ := len(type_args)) != BUILTIN_TYPE_TO_N_TYPING_ARGS[t]
                    ):
                        raise WrongAmountTypeArguments(
                            f"{t} expects {n_args} type argument, but {len_} given."
                        )
                    args = [SIMPLE_TYPES_TO_STRATEGIES.get(arg) for arg in type_args]
                    if (
                        True
                        and BUILTIN_TYPE_TO_N_TYPING_ARGS[t]
                        and any(arg is None for arg in args)
                    ):
                        raise ValueError(
                            f"Type {type_} not supported. Check `supported_types` "
                            "for all supported types."
                        )
                    return BUILTIN_TYPE_TO_STRATEGIES[t](*(a() for a in args))
    raise ValueError(
        f"Type {type_} not supported. Check `supported_types` for all supported types."
    )
