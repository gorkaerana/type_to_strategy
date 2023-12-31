# `type_to_strategy`

In short, `type_to_strategy` aims to improve the developer experience of using [`hypothesis`](https://github.com/HypothesisWorks/hypothesis), from

```python
from hypothesis import given
from hypothesis.strategies import integers, text

@given(text() | integers())
def test_something(value):
    assert str(value) > 5
```

to

```python
from type_to_strategy import strategize

@strategize(str | int)
def test_something(value):
    assert str(value) > 5
```

This is indeed a different implementation of `hypothesis.strategies.from_type`. Nonetheless, it works better with some Python types (`typing.Mapping`, `typing.Iterable`, `collections.abc.Iterable`, etc.), so the idea is to implement those here and then upstream them to `hypothesis`.

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
- [X] `slice`
- [X] `str`
- [X] `tuple`
- [X] `None`

### `typing` types
- [ ] `Any`
- [ ] `Callable`
- [X] `Dict`
- [X] `FrozenSet`
- [ ] `Generator`
- [X] `Iterable`
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

### `datetime` types
- [X] `date`
- [X] `datetime`
- [ ] `time`
- [ ] `timedelta`

### `decimals` types
- [X] `Decimal`

### `fractions` types
- [X] `Fraction`

### `uuid` types
- [ ] `UUID`

### `zoneinfo` types
- [ ] `ZoneInfo`

### Various dataclasses
- [ ] `attrs`
- [ ] `dataclasses`
