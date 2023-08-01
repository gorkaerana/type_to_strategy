from typing import Callable, Dict, List, Set, Tuple

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
    sets,
    tuples,
)
from type_to_strategy.types import SpecialGenericAlias

BUILTIN_TYPE_TO_TYPING_EQUIVALENT: dict[type, SpecialGenericAlias] = {
    list: List,
    set: Set,
    dict: Dict,
    tuple: Tuple,
}

BUILTIN_TYPE_TO_N_TYPING_ARGS: dict[type, int | None] = {
    list: 1,
    set: 1,
    dict: 2,
    tuple: None,
}

BUILTIN_TYPE_TO_STRATEGIES: dict[type, Callable] = {
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

TYPING_TO_STRATEGIES: dict[SpecialGenericAlias, Callable] = {
    List: lists,
    Set: sets,
    Dict: dictionaries,
    Tuple: tuples,
}

SIMPLE_TYPES_TO_STRATEGIES = BUILTIN_TYPE_TO_STRATEGIES | TYPING_TO_STRATEGIES

SUPPORTED_TYPES = set(SIMPLE_TYPES_TO_STRATEGIES.keys())
