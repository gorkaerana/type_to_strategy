from typing import Dict, List, Set, Tuple, get_args, get_origin

import pytest
from type_to_strategy import translate


# TODO: how to test the first four only for Python > 3.8?
composite_types = [
    # dict[str, str],
    # list[str],
    # set[str],
    # tuple[str],
    Dict[str, str],
    List[str],
    Set[str],
    Tuple[str],
]


@pytest.mark.parametrize("type_", [bool, bytes, complex, float, int, str])
def test_translate_with_simple_types(type_):
    assert type(translate(type_).example()) == type_


@pytest.mark.parametrize("type_", composite_types)
def test_translate_with_composite_types_correct_example_type(type_):
    assert type(translate(type_).example()) == get_origin(type_)


@pytest.mark.parametrize("type_", composite_types)
def test_translate_with_composite_types_correct_example_component_type(type_):
    assert all(type(c) == get_args(type_)[0] for c in translate(type_).example())
