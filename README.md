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
- [X] `bool`
- [X] `bytes`
- [X] `complex`
- [X] `dict` (and `typing.Dict`)
- [X] `float`
- [ ] `frozenset`
- [X] `int`
- [X] `list` (and `typing.List`)
- [X] `set` (and `typing.Set`)
- [X] `str`
- [X] `tuple` (and `typing.Tuple`)
- [X] `types.UnionType`
- [ ] `typing.Any`
