#!/usr/bin/env python3

from __future__ import annotations

import functools
import itertools
import operator
import random
import statistics
from collections import Counter
from typing import Any, Callable, Dict, Iterable, List, Set, Tuple, Union, overload


class Iter:
    """
    Provides a set of algorithms to work with iterable collections. In Python,
    an iterable is any data type that implements the `__iter__` method which
    returns an iterator, or alternatively, a `__getitem__` method suitable for
    indexed lookup such as `list`, `tuple`, `dict`, or `set`.

    ```python
    >>> Iter(range(1,4)).map(lambda x: 2*x)
    [2, 4, 6]
    >>> Iter(range(1, 4)).sum()
    6
    >>> Iter({'a': 1, 'b': 2}).map(lambda k,v: {k, 2 * v})
    {'a': 2, 'b': 4}
    ```
    """
    def __init__(self, iter: Iterable) -> Iter:
        self.domain = list(iter)
        self.image = iter

    def all(self, fun: Callable=None) -> bool:
        """
        Return `True` if all elements in `self.image` are truthy, or `True` if
        `fun` is not None and its map truthy for all elements in `self.image`.

        ```python
        >>> Iter([1, 2, 3]).all()
        True
        >>> Iter([1, None, 3]).all()
        False
        >>> Iter([]).all()
        True
        >>> Iter([1,2,3]).all(lambda x: x % 2 == 0)
        False
        ```
        """
        self.image = all(self.image) if fun is None else all(map(fun, self.image))
        return self.image

    def any(self, fun: Callable=None) -> bool:
        """
        Return `True` if any elements in `self.image` are truthy, or `True` if
        `fun` is not None and its map truthy for at least on element in `self.image`.

        ```python
        >>> Iter([False, False, False]).any()
        False
        >>> Iter([False, True, False]).any()
        True
        >>> Iter([2,4,6]).any(lambda x: x % 2 == 1)
        False
        ```
        """
        self.image = any(self.image) if fun is None else any(map(fun, self.image))
        return self.image

    def at(self, index: int) -> Any:
        """
        Find the element at the given `index` (zero-based). Raise an `IndexError`
        if `index` is out of bonds. A negative index can be passed, which means the
        enumerable is enumerated once and the index is counted from the end.

        ```python
        >>> Iter([2,4,6]).at(0)
        2
        >>> Iter([2,4,6]).at(-1)
        6
        >>> Iter([2,4,6]).at(4)
        IndexError: list index out of range
        ```
        """
        self.image = list(self.image)[index]
        return self.image

    def avg(self) -> Union[int, float]:
        """
        Return the sample arithmetic mean of `self.image`.

        ```python
        >>> Iter(range(11)).avg()
        5
        ```
        """
        self.image = statistics.mean(self.image)
        return self.image

    def chunk_by(self, by: Union[int, Callable]) -> Iter:
        """
        Split `self.image` on every element for which `by` returns a new value
        if `by` is a predicate, else split `self.image` into sublists of size `by`.

        ```python
        >>> Iter([1, 2, 2, 3, 4, 4, 6, 7, 7, 7]).chunk_by(lambda x: x % 2 == 1)
        [[1], [2, 2], [3], [4, 4, 6], [7, 7, 7]]
        >>> Iter([1, 2, 2, 3, 4, 4, 6, 7, 7]).chunk_by(3)
        [[1, 2, 2], [3, 4, 4], [6, 7, 7], [7]]
        """
        if isinstance(by, int):
            self.image = [list(self.image)[i:i+by] for i in range(0, len(self.image), by)]
            return self.image
        else:
            raise NotImplementedError()

    def __str__(self) -> str:
        return f"[{', '.join(map(str, self.iter))}]" if isinstance(self.image, Iterable) else self.image
