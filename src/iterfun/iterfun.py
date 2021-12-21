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
    Define a set of algorithms to work with iterable collections. In Python,
    an iterable is any data type that implements the `__iter__` method which
    returns an iterator, or alternatively, a `__getitem__` method suitable for
    indexed lookup such as `list`, `tuple`, `dict`, or `set`.

    ```python
    >>> Iter(1, 3).map(lambda x: 2*x)
    [2, 4, 6]
    >>> Iter([1, 2, 3]).sum()
    6
    >>> Iter({'a': 1, 'b': 2}).map(lambda k,v: {k, 2 * v}
    {'a': 2, 'b': 4}
    ```
    """

    @overload
    def __init__(self, iter: Iterable) -> Iter: ...

    @overload
    def __init__(self, *iter: int) -> Iter: ...

    def __init__(self, *iter: Iterable | int) -> Iter:
        self.domain = iter[0]
        self.image = Iter.__ctor(iter)

    @staticmethod
    def __ctor(iter: Iterable | int) -> List:
        if isinstance(iter, Tuple) and len(iter) == 2:
            return list(range(iter[0], iter[1]+1)) if iter[1] != 0 else []
        return iter[0]

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
        >>> Iter(range(1, 6)).count(lambda x: x % 2 == 0)
        2
        ```
        """
        return len(list(self.image)) if fun is None else len(list(filter(fun, self.image)))

    def count_until(self, limit: int, fun: Optional[Callable]=None) -> int:
        """
        Count the elements in `self.image` for which `fun` returns a truthy value,
        stopping at `limit`.

        ```python
        >>> Iter(range(1, 21)).count_until(5)
        5
        >>> Iter(range(1, 21)).count_until(50)
        20
        ```
        """
        return len(list(self.image)[:limit]) if fun is None else len(list(filter(fun, self.image))[:limit])


    def dedup(self) -> Iter:
        """
        Enumerates `self.image`, returning a list where all consecutive duplicated
        elements are collapsed to a single element.

        ```python
        >>> Iter([1, 2, 3, 3, 2, 1]).dedup()
        [1, 2, 3, 2, 1]
        ```
        """
        self.image = [group[0] for group in itertools.groupby(self.image)]
        return self

    def dedup_by(self, fun: Callable):
        raise NotImplementedError()

    def drop(self, amount: int) -> Iter:
        """
        ```python
        >>> Iter([1, 2, 3]).drop(2)
        [3]
        >>> Iter([1, 2, 3]).drop(10)
        []
        >>> Iter([1, 2, 3]).drop(-1)
        [1, 2]
        ```
        """
        self.image = list(self.image)
        self.image = self.image[amount:] if amount > 0 else self.image[:len(self.image)+amount]
        return self

    def drop_every(self, nth: int) -> Iter:
        """
        Return a list of every `nth` element in the `self.image` dropped, starting
        with the first element. The first element is always dropped, unless `nth` is `0`.
        The second argument specifying every nth element must be a non-negative integer.

        ```python
        >>> Iter(1, 10).drop_every(2)
        [2, 4, 6, 8, 10]
        >>> Iter(1, 10).drop_every(0)
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> Iter(1, 3).drop_every(1)
        []
        ```
        """
        self.image = [] if nth == 1 else [self.image[i] for i in range(int(nth != 0), len(self.image), nth if nth > 1 else 1)]
        return self

    def drop_while(self, fun: Callable) -> Iter:
        """
        Drop elements at the beginning of the enumerable while `fun` returns a
        truthy value.

        ```python
        >>> Iter([1, 2, 3, 2, 1]).drop_while(lambda x: x < 3)
        [3, 2, 1]
        ```
        """
        self.image = self.image[self.image.index(list(itertools.filterfalse(fun, self.image))[0]):]
        return self

    def each(self, fun: Callable) -> bool:
        """
        Invoke the given `fun` for each element in `self.image`, then return
        `True`.
        >>> Iter(1, 3).each(print)
        1
        2
        3
        """
        list(map(fun, self.image))
        return True

    def empty(self) -> bool:
        """
        Return `True` if `self.image` is empty, otherwise `False`.

        ```python
        >>> Iter([]).empty()
        True
        >>> Iter(0, 0).empty()
        True
        >>> Iter(1, 10).empty()
        False
        ```
        """
        return not bool(len(self.image))

    def fetch(self, index: int) -> bool:
        raise NotImplementedError()

    def filter(self, fun: Callable) -> Iter:
        """
        Filter `self.image`, i.e. return only those elements for which `fun` returns
        a truthy value.

        ```python
        >>> Iter(1, 3).filter(lambda x: x % 2 == 0)
        [2]
        ```
        """
        self.image = list(filter(fun, self.image))
        return self

    def find(self, fun: Callable, default: Optional[Any]=None) -> Optional[Any]:
        """
        Return the first element for which `fun` returns a truthy value. If no
        such element is found, return `default`.

        ```python
        >>> Iter(2, 4).find(lambda x: x % 2 == 1)
        3
        >>> Iter([2, 4, 6]).find(lambda x: x % 2 == 1)
        None
        >>> Iter([2, 4, 6]).find(lambda x: x % 2 == 1, default=0)
        0
        ```
        """
        return next(filter(fun, self.image), default)

    def find_index(self, fun: Callable, default: Optional[Any]=None) -> Optional[Any]:
        """
        Similar to `self.find`, but return the index (zero-based) of the element
        instead of the element itself.

        ```python
        >>> Iter([2, 4, 6]).find_index(lambda x: x % 2 == 1)
        None
        >>> Iter([2, 3, 4]).find_index(lambda x: x % 2 == 1)
        1
        ```
        """
        found = next(filter(fun, self.image), default)
        return self.image.index(found) if found in self.image else default

    def find_value(self, fun: Callable, default: Optional[Any]=None) -> Optional[Any]:
        """
        Similar to `self.find`, but return the value of the function invocation instead
        of the element itself.

        ```python
        >>> Iter([2, 4, 6]).find_value(lambda x: x % 2 == 1)
        None
        >>> Iter([2, 3, 4]).filter(lambda x: x > 2).find_value(lambda x: x * x)
        9
        >>> Iter(1, 3).find_value(lambda x: isinstance(x, bool), "no bools!")
        'no bools!'
        ```
        """
        found = next(filter(fun, self.image), default)
        return fun(found) if found is not default else default

    def flat_map(self, fun: Callable) -> Iter:
        """
        Map the given `fun` over `self.image` and flattens the result.

        ```python
        >>> Iter([(1, 3), (4, 6)]).flat_map(lambda x: list(range(x[0], x[1]+1)))
        [1, 2, 3, 4, 5, 6]
        >>> Iter([1, 2, 3]).flat_map(lambda x: [[x]])
        [[1], [2], [3]]
        ```
        """
        self.image = list(itertools.chain(*map(fun, self.image)))
        return self

    def flat_map_reduce(self, fun: Callable[[Any, Any], Any], acc: Any) -> Iter:
        """
        Map and reduce an `self.image`, flattening the given results (only one
        level deep). It expects an accumulator and a function that receives each
        enumerable element, and must return a...

        ```python
        >>> #example
        ```
        """
        raise NotImplementedError()

    @overload
    @staticmethod
    def range(lim: List[int, int]) -> List[int]: ...

    @overload
    @staticmethod
    def range(lim: Tuple[int, int]) -> List[int]: ...

    @staticmethod
    def range(lim: List[int, int] | Tuple[int, int]) -> List[int]:
        """
        Return a sequence of integers from start to end.

        ```python
        >>> Iter.range([1, 5])
        [1, 2, 3, 4, 5]
        >>> Iter.range((1, 5))
        [2, 3, 4]
        ```
        """
        return list(range(lim[0], lim[1]+1) if isinstance(lim, List) else range(lim[0]+1, lim[1]))

    def __str__(self) -> str:
        return f"[{', '.join(map(str, self.iter))}]" if isinstance(self.image, Iterable) else self.image
