from __future__ import annotations

import typing
from collections.abc import Callable


T = typing.TypeVar('T')


def trap(fn: Callable[[], T]) -> tuple[T, None] | tuple[None, Exception]:
    try:
        return fn(), None
    except Exception as e:
        return None, e
