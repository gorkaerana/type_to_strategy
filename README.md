# `type_to_strategy`

In short, `type_to_strategy` aims to improve the developer experience of using [`hypothesis`](https://github.com/HypothesisWorks/hypothesis), from

```python
from hypothesis import given
from hypothesis.strategies import integers, text

@given(text() | integers())
def test_something(o):
    assert True
```

to

```python
from type_to_strategy import strategize

@strategize(str | int)
def test_something(o):
    assert True
```

## Supported types
### Built-in types
- [X] `bool`
- [X] `bytes`
- [X] `complex`
- [X] `dict`
- [X] `float`
- [X] `frozenset`
- [X] `int`
- [X] `list`
- [X] `set`
- [X] `str`
- [X] `tuple`
- [X] `None`

### `typing` types
- [ ] `Any`
- [ ] `Callable`
- [X] `Dict`
- [X] `FrozenSet`
- [ ] `Generator`
- [ ] `Iterable`
- [ ] `Iterator`
- [X] `List`
- [ ] `Mapping`
- [ ] `MutableMapping`
- [ ] `MutableSequence`
- [ ] `MutableSet`
- [X] `Optional`
- [X] `Set`
- [X] `Tuple`
- [X] `UnionType`
