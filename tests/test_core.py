import sys
from collections.abc import Iterable as AbcIterable
from datetime import date, datetime
from decimal import Decimal
from fractions import Fraction
from itertools import product
from typing import Any, Dict, FrozenSet, Iterable, List, Set, Tuple, Union

import pytest
from hypothesis.strategies._internal.core import PrettyIter
from type_to_strategy.core import translate

# `hash(Decimal("sNaN"))` results in `TypeError: Cannot hash a signaling NaN value`
HASHABLE_TYPES = [bool, bytes, complex, date, datetime, float, int, str, Fraction]
SIMPLE_TYPES = HASHABLE_TYPES + [Decimal, slice]

DICT_TYPES: List[Any] = [Dict]
FROZENSET_TYPES: List[Any] = [FrozenSet]
LIST_TYPES: List[Any] = [List]
SET_TYPES: List[Any] = [Set]
TUPLE_TYPES: List[Any] = [Tuple]
ITERABLE_TYPES: List[Any] = [Iterable, AbcIterable]

if sys.version_info >= (3, 10):
    DICT_TYPES.append(dict)
    FROZENSET_TYPES.append(frozenset)
    LIST_TYPES.append(list)
    SET_TYPES.append(set)
    TUPLE_TYPES.append(tuple)


def thorough_isinstance(obj: Any, type_: type) -> bool:
    """`isinstance`, and it accounts for `type_` being `None`"""
    return isinstance(obj, type(None) if type_ is None else type_)


@pytest.mark.parametrize("type_", SIMPLE_TYPES)
def test_translate_with_simple_types(type_):
    assert thorough_isinstance(translate(type_).example(), type_)


@pytest.mark.parametrize(
    "dict_,key_type,value_type", list(product(DICT_TYPES, HASHABLE_TYPES, SIMPLE_TYPES))
)
def test_translate_with_dict(dict_, key_type, value_type):
    strategy = translate(dict_[key_type, value_type])
    example = strategy.example()
    print(example)
    assert all(thorough_isinstance(k, key_type) for k in example.keys())
    assert all(thorough_isinstance(v, value_type) for v in example.values())
    assert thorough_isinstance(example, dict)


@pytest.mark.parametrize(
    "frozenset_,value_type", product(FROZENSET_TYPES, HASHABLE_TYPES)
)
def test_translate_with_frozenset(frozenset_, value_type):
    strategy = translate(frozenset_[value_type])
    example = strategy.example()
    print(example)
    assert all(thorough_isinstance(v, value_type) for v in example)
    assert thorough_isinstance(example, frozenset)


@pytest.mark.parametrize("list_,value_type", product(LIST_TYPES, SIMPLE_TYPES))
def test_translate_with_list(list_, value_type):
    strategy = translate(list_[value_type])
    example = strategy.example()
    assert all(thorough_isinstance(v, value_type) for v in example)
    assert thorough_isinstance(example, list)


@pytest.mark.parametrize("set_,value_type", product(SET_TYPES, HASHABLE_TYPES))
def test_translate_with_set(set_, value_type):
    strategy = translate(set_[value_type])
    example = strategy.example()
    assert all(thorough_isinstance(v, value_type) for v in example)
    assert thorough_isinstance(example, set)


@pytest.mark.parametrize(
    "tuple_,value_type",
    product(TUPLE_TYPES, SIMPLE_TYPES),
)
def test_translate_with_set_and_ellipsis(tuple_, value_type):
    strategy = translate(tuple_[value_type, ...])
    example = strategy.example()
    assert all(thorough_isinstance(v, value_type) for v in example)
    assert len(example) > 0
    assert thorough_isinstance(example, tuple)


# TODO: test with dicts, lists, etc.
@pytest.mark.parametrize(
    "value_type1,value_type2", list(product(SIMPLE_TYPES, SIMPLE_TYPES))
)
def test_translate_with_union_type(value_type1, value_type2):
    type_ = Union[value_type1, value_type2]
    strategy = translate(type_)
    example = strategy.example()
    assert any(thorough_isinstance(example, v) for v in [value_type1, value_type2])


@pytest.mark.parametrize(
    "iterable_,value_type",
    product(ITERABLE_TYPES, SIMPLE_TYPES),
)
def test_translate_with_iterable(iterable_, value_type):
    strategy = translate(iterable_[value_type])
    example = strategy.example()
    assert all(thorough_isinstance(v, value_type) for v in example)
    assert thorough_isinstance(example, PrettyIter)
