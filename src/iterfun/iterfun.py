#!/usr/bin/env python3

from __future__ import annotations

import functools
import itertools
import operator
import random
import statistics
from collections import Counter
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, Union, overload


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

    def all(self, fun: Optional[Callable]=None) -> bool:
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

    def any(self, fun: Optional[Callable]=None) -> bool:
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

    def chunk_by(self, fun: Callable) -> Iter:
        """
        Split `self.image` on every element for which `fun` returns a new value.

        ```python
        >>> Iter([1, 2, 2, 3, 4, 4, 6, 7, 7, 7]).chunk_by(lambda x: x % 2 == 1)
        [[1], [2, 2], [3], [4, 4, 6], [7, 7, 7]]
        ```
        """
        self.image = [list(group) for _, group in itertools.groupby(self.image, fun)]
        return self

    def chunk_every(self, count: int, step: Optional[int]=None, leftover: Optional[List[Any]]=None) -> Iter:
        """
        Return list of lists containing `count` elements each. `step` is optional
        and, if not passed, defaults to `count`, i.e. chunks do not overlap.

        ```python
        >>> Iter(range(1, 7)).chunk_every(2)
        [[1, 2], [3, 4], [5, 6]]
        >>> Iter(range(1, 7)).chunk_every(3, 2, [7])
        [[1, 2, 3], [3, 4, 5], [5, 6, 7]]
        >>> Iter(range(1, 4)).chunk_every(3, 3)
        [[1, 2, 3], [4]]
        ```
        """
        step = step or count
        self.image = [list(self.image)[i:i+count] for i in range(0, len(self.image), count-(count-step))]
        if leftover: self.image[-1].extend(leftover[:len(self.image[-1])])
        return self

    def chunk_while(self, acc: List, chunk_fun: Callable, chunk_after: Callable) -> Iter:
        raise NotImplementedError()

    @overload
    @staticmethod
    def concat(iter: List[Any]) -> Iter: ...

    @overload
    @staticmethod
    def concat(*iter: Tuple[int, int]) -> Iter: ...

    @staticmethod
    def concat(*iter: List[Any] | Tuple[int, int]) -> Iter:
        """
        Given a list of lists, concatenates the list into a single list.

        ```python
        >>> Iter.concat([[1, [2], 3], [4], [5, 6]])
        [1, [2], 3, 4, 5, 6]
        >>> Iter.concat((1, 3), (4, 6))
        [1, 2, 3, 4, 5, 6]
        ```
        """
        return Iter(list(itertools.chain(*(iter[0] if isinstance(iter[0], List) else [range(t[0], t[1]+1) for t in iter]))))

    def count(self, fun: Optional[Callable]=None) -> int:
        """
        Return the size of the `self.image` if `fun` is `None`, else return the
        count of elements in `self.image` for which `fun` returns a truthy value.

        ```python
        >>> Iter(range(1,4)).count()
        3
        >>> Iter(range(1, 6).count(lambda x: x % 2 == 0))
        2
        ```
        """
        return len(self.image) if fun is None else len(list(filter(fun, self.image)))

    def __str__(self) -> str:
        return f"[{', '.join(map(str, self.iter))}]" if isinstance(self.image, Iterable) else self.image
