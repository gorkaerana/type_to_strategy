from typing import Protocol


class SpecialGenericAlias(Protocol):
    """The types of `typing.Dict`, `typing.List`, `typing.Set`, and `typing.Tuple`
    are `_SpecialGenericAlias` (for the first three) and `_TypeTuple` for the last
    one, where the latter is a subclass of the former. The internal representations
    of these types in typing are not part of any public API, and so we create this
    protocol to avoid for type checking.
    """

    def __getitem__(self, params):
        ...

    def copy_with(self, params):
        ...

    def __repr__(self):
        ...

    def __subclasscheck__(self, cls):
        ...

    def __reduce__(self):
        ...

    def __or__(self):
        ...

    def __ror__(self, left):
        ...
