import sys
from itertools import product
from typing import Any, Dict, List, Set, Tuple, Union

import pytest
from type_to_strategy.core import translate

SIMPLE_TYPES = [bool, bytes, complex, float, int, str]

DICT_TYPES: List[Any] = [Dict]
LIST_TYPES: List[Any] = [List]
SET_TYPES: List[Any] = [Set]
TUPLE_TYPES: List[Any] = [Tuple]

if sys.version_info >= (3, 10):
    DICT_TYPES.append(dict)
    LIST_TYPES.append(list)
    SET_TYPES.append(set)
    TUPLE_TYPES.append(tuple)


@pytest.mark.parametrize("type_", SIMPLE_TYPES)
def test_translate_with_simple_types(type_):
    assert isinstance(translate(type_).example(), type_)


@pytest.mark.parametrize(
    "dict_,key_type,value_type", list(product(DICT_TYPES, SIMPLE_TYPES, SIMPLE_TYPES))
)
def test_translate_with_dict(dict_, key_type, value_type):
    strategy = translate(dict_[key_type, value_type])
    example = strategy.example()
    assert all(isinstance(k, key_type) for k in example.keys())
    assert all(isinstance(v, value_type) for v in example.values())
    assert isinstance(example, dict)


@pytest.mark.parametrize("list_,value_type", product(LIST_TYPES, SIMPLE_TYPES))
def test_translate_with_list(list_, value_type):
    strategy = translate(list_[value_type])
    example = strategy.example()
    assert all(isinstance(v, value_type) for v in example)
    assert isinstance(example, list)


@pytest.mark.parametrize("set_,value_type", product(SET_TYPES, SIMPLE_TYPES))
def test_translate_with_set(set_, value_type):
    strategy = translate(set_[value_type])
    example = strategy.example()
    assert all(isinstance(v, value_type) for v in example)
    assert isinstance(example, set)


@pytest.mark.parametrize("tuple_,value_type", product(TUPLE_TYPES, SIMPLE_TYPES))
def test_translate_with_set_and_one_argument(tuple_, value_type):
    strategy = translate(tuple_[value_type])
    example = strategy.example()
    assert isinstance(example[0], value_type)
    assert len(example) == 1
    assert isinstance(example, tuple)


@pytest.mark.parametrize(
    "tuple_,value_type1,value_type2",
    product(TUPLE_TYPES, SIMPLE_TYPES, SIMPLE_TYPES),
)
def test_translate_with_set_and_several_arguments(tuple_, value_type1, value_type2):
    strategy = translate(tuple_[value_type1, value_type2])
    example = strategy.example()
    assert isinstance(example[0], value_type1) and isinstance(example[1], value_type2)
    assert len(example) == 2
    assert isinstance(example, tuple)


@pytest.mark.parametrize(
    "tuple_,value_type",
    product(TUPLE_TYPES, SIMPLE_TYPES),
)
def test_translate_with_set_and_ellipsis(tuple_, value_type):
    strategy = translate(tuple_[value_type, ...])
    example = strategy.example()
    assert all(isinstance(v, value_type) for v in example)
    assert len(example) > 0
    assert isinstance(example, tuple)


# TODO: test with dicts, lists, etc.
@pytest.mark.parametrize(
    "value_type1,value_type2", list(product(SIMPLE_TYPES, SIMPLE_TYPES))
)
def test_translate_with_union_type(value_type1, value_type2):
    type_ = Union[value_type1, value_type2]
    strategy = translate(type_)
    example = strategy.example()
    assert any(isinstance(example, v) for v in [value_type1, value_type2])
