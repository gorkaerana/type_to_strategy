from itertools import product, starmap
from operator import or_
from typing import Dict, List, Set, Tuple

import pytest
from type_to_strategy.core import strategize

SIMPLE_TYPES = [bool, bytes, complex, float, int, str]


@pytest.mark.parametrize("type_", SIMPLE_TYPES)
def test_strategize_with_simple_types(type_):
    assert isinstance(strategize(type_).example(), type_)


@pytest.mark.parametrize(
    "dict_,key_type,value_type", list(product([dict, Dict], SIMPLE_TYPES, SIMPLE_TYPES))
)
def test_strategize_with_dict(dict_, key_type, value_type):
    strategy = strategize(dict_[key_type, value_type])
    example = strategy.example()
    assert all(isinstance(k, key_type) for k in example.keys())
    assert all(isinstance(v, value_type) for v in example.values())
    assert isinstance(example, dict)


@pytest.mark.parametrize("list_,value_type", product([list, List], SIMPLE_TYPES))
def test_strategize_with_list(list_, value_type):
    strategy = strategize(list_[value_type])
    example = strategy.example()
    assert all(isinstance(v, value_type) for v in example)
    assert isinstance(example, list)


@pytest.mark.parametrize("set_,value_type", product([set, Set], SIMPLE_TYPES))
def test_strategize_with_set(set_, value_type):
    strategy = strategize(set_[value_type])
    example = strategy.example()
    assert all(isinstance(v, value_type) for v in example)
    assert isinstance(example, set)


@pytest.mark.parametrize("tuple_,value_type", product([tuple, Tuple], SIMPLE_TYPES))
def test_strategize_with_set_and_one_argument(tuple_, value_type):
    strategy = strategize(tuple_[value_type])
    example = strategy.example()
    assert isinstance(example[0], value_type)
    assert len(example) == 1
    assert isinstance(example, tuple)


@pytest.mark.parametrize(
    "tuple_,value_type1,value_type2",
    product([tuple, Tuple], SIMPLE_TYPES, SIMPLE_TYPES),
)
def test_strategize_with_set_and_several_arguments(tuple_, value_type1, value_type2):
    strategy = strategize(tuple_[value_type1, value_type2])
    example = strategy.example()
    assert isinstance(example[0], value_type1) and isinstance(example[1], value_type2)
    assert len(example) == 2
    assert isinstance(example, tuple)


@pytest.mark.parametrize(
    "tuple_,value_type",
    product([tuple, Tuple], SIMPLE_TYPES),
)
def test_strategize_with_set_and_ellipsis(tuple_, value_type):
    strategy = strategize(tuple_[value_type, ...])
    example = strategy.example()
    assert all(isinstance(v, value_type) for v in example)
    assert len(example) > 0
    assert isinstance(example, tuple)


# TODO: test with dicts, lists, etc.
@pytest.mark.parametrize(
    "type_", list(starmap(or_, product(SIMPLE_TYPES, SIMPLE_TYPES)))
)
def test_strategize_with_union_type(type_):
    type_ = or_(str, int)
    strategy = strategize(type_)
    example = strategy.example()
    assert isinstance(example, type_)
