from __future__ import annotations

from typing import get_args, get_origin

# from hypothesis.strategies._internal.lazy import LazyStrategy
from type_to_strategy.const import (
    BUILTIN_TYPE_TO_N_TYPING_ARGS,
    BUILTIN_TYPE_TO_STRATEGIES,
    BUILTIN_TYPE_TO_TYPING_EQUIVALENT,
    SIMPLE_TYPES_TO_STRATEGIES,
)
from type_to_strategy.errors import WrongAmountTypeArguments


# TODO: support `bytearray`
# TODO: support `Any`?
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
    origin_type, type_args = get_origin(type_), get_args(type_)
    if (origin_type is None) and (type_ in SIMPLE_TYPES_TO_STRATEGIES):
        return SIMPLE_TYPES_TO_STRATEGIES[type_]()
    if (origin_type is not None) and (origin_type in SIMPLE_TYPES_TO_STRATEGIES):
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
                args = []
                for arg in type_args:
                    strategy = SIMPLE_TYPES_TO_STRATEGIES.get(arg)
                    if strategy is None:
                        raise ValueError(
                            f"Type {type_} not supported. Check `SUPPORTED_TYPES` "
                            "for all supported types."
                        )
                    else:
                        args.append(strategy)
                return BUILTIN_TYPE_TO_STRATEGIES[t](*(a() for a in args))
    raise ValueError(
        f"Type {type_} not supported. Check `SUPPORTED_TYPES` for all supported types."
    )
