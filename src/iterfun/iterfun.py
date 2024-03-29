#!/usr/bin/env python3

"""
The MIT License
Copyright (c) 2023, Stefan Greve
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import annotations

import csv
import functools
import itertools
import json
import math
import operator
import os
import random
import secrets
import statistics
import sys
import textwrap
from collections import ChainMap, Counter
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Final,
    Generator,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    overload
)

if sys.version_info >= (3, 11):
    from typing import Annotated, Self
else:
    from typing_extensions import Annotated, Self

class Functions:
    def invert(x: int | float) -> (int | float):
        """
        Invert the algebraic sign of `x`.
        """
        return -1 * x

    def is_even(n: int) -> bool:
        """
        Test if `n` is an even number.
        """
        return not n & 1

    def is_odd(n: int) -> bool:
        """
        Test if `n` is an odd number.
        """
        return bool(n & 1)

    def is_prime(n: int) -> bool:
        """
        Test whether the number `n` is prime or not.
        """
        if n <= 1: return False

        i = 2
        while i ** 2 <= n:
            if n % i == 0:
                return False
            i += 1

        return True

    def __inner_miller_rabin(n: int, r: int) -> bool:
        m = n - 1 # = (n - 1) / 2^k
        while not m & 1:
            m >>= 1

        if pow(r, m, n) == 1:
            return True

        while m < n - 1:
            if pow(r, m, n) == n - 1:
                return True
            m <<= 1

        return False

    def miller_rabin(n: int, k: int = 40) -> bool:
        """
        Test whether a number `n >= 2` is composite, i.e. not prime. Return `True`
        if `n` passes `k` rounds of the Miller-Rabin primality test and assert that
        a number `n` might possibly be prime, else return `False` if `n` is proved
        to be a composite.
        """
        if n < 2: raise ValueError()
        if n <= 3: return True

        for _ in range(k):
            if not Functions.__inner_miller_rabin(n, r=secrets.choice(range(2, n - 1))):
                return False

        return True

    def sign(x: int | float) -> Literal[-1, 0, 1]:
        """
        Extract the sign of a real number.
        """
        return x and (-1 if x < 0 else 1)


class Iter:
    """
    ## Iter

    Implements an eager set of common algorithms for list and dictionary transformations.
    The image is a public field that is used by this class to temporarily store
    and pass data between method invocations, while the domain registers the input
    that was available during the initial object instantiation.

    ### Example
    ```python
    >>> from iterfun import Iter
    >>> from iterfun import Functions as fun
    >>>
    >>> # map over a collection
    >>> Iter.range(1, 3).map(lambda x: 2*x).sum()
    12
    >>>
    >>> # use helper methods from the Functions class
    >>> Iter.range(10).filter(fun.is_prime).join('-')
    '2-3-5-7'
    ```
    """

    def __init__(self, iter_: Iterable) -> None:
        """
        Initialize a new object of this class.
        """
        self.domain: Final[Iterable] = iter_
        self.image: Iterable = iter_
        self.__value = None
        self.__index = 0

    def all(self: Self, fun: Optional[Callable[[Any], bool]] = None) -> bool:
        """
        Test if all elements in the image are truthy, or if `fun` maps to truthy
        values in all instances.

        ```python
        >>> Iter([1, 2, 3]).all()
        True
        >>> Iter([1, None, 3]).all()
        False
        >>> Iter([]).all()
        True
        >>> Iter([1, 2, 3]).all(lambda x: x % 2 == 0)
        False
        ```
        """
        return all(self.image) if fun is None else all(map(fun, self.image))

    def any(self: Self, fun: Optional[Callable[[Any], bool]] = None) -> bool:
        """
        Test if any elements in the image are truthy, or if `fun` maps to truthy
        values in at least once instance.

        ```python
        >>> Iter([False, False, False]).any()
        False
        >>> Iter([False, True, False]).any()
        True
        >>> Iter([2, 4, 6]).any(lambda x: x % 2 == 1)
        False
        ```
        """
        return any(self.image) if fun is None else any(map(fun, self.image))

    def at(self: Self, index: int) -> Any:
        """
        Find the element at the given zero-based `index`. Raises an `IndexError`
        if `index` is out of bonds. A negative index can be passed, which means
        the image is enumerated once from right to left.

        ```python
        >>> Iter([2, 4, 6]).at(0)
        2
         >>> Iter([2, 4, 6]).at(-1)
        6
         >>> Iter([2, 4, 6]).at(4)
        IndexError: list index out of range
        ```
        """
        return self.image[index]

    def avg(self: Self) -> (int | float):
        """
        Return the sample arithmetic mean of the image.

        ```python
        >>> Iter([0, 10]).avg()
        5
        ```
        """
        return statistics.mean(self.image)

    def cartesian(self: Self, repeat: int = 1) -> Self:
        """
        Return the cartesian product, i.e. `A x B = {(a, b) | a ∈ A ^ b ∈ B}`.

        ```python
        >>> Iter([(1, 2), ('a', 'b')]).cartesian()
        [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
        >>> Iter([True, False]).cartesian(repeat=2)
        [(True, True), (True, False), (False, True), (False, False)]
        ```
        """
        nested = any(isinstance(i, Iterable) for i in self.image)
        self.image = list(itertools.product(*self.image, repeat=repeat) if nested else itertools.product(self.image, repeat=repeat))
        return self

    def chunk_by(self: Self, fun: Callable[[Any], bool], eject: bool = False) -> Self:
        """
        Split the domain on every element for which `fun` returns a new value.
        Remove any group for which `fun` initially returned `True` if `eject` is
        enabled.

        ```python
        >>> Iter([1, 2, 2, 3, 4, 4, 6, 7, 7, 7]).chunk_by(lambda x: x % 2 == 1)
        [[1], [2, 2], [3], [4, 4, 6], [7, 7, 7]]
        >>> sequence = ['a', 'b', '1', 'c', 'd', '2', 'e', 'f']
        >>> Iter(sequence).chunk_by(lambda x: x.isdigit(), eject=True)
        [['a', 'b'], ['c', 'd'], ['e', 'f']]
        ```
        """
        tmp = [list(group) for _, group in itertools.groupby(self.image, fun)]
        self.image = [x for x in tmp if len(x) > 1 and not fun(x[0])] if eject else tmp
        return self

    def chunk_every(self: Self, count: int, step: Optional[int] = None, leftover: Optional[List[Any]] = None) -> Self:
        """
        Return list of lists containing `count` elements each. `step` is optional
        and, if not passed, defaults to `count`, i.e. chunks do not overlap.

        ```python
        >>> Iter.range(1,6).chunk_every(2)
        [[1, 2], [3, 4], [5, 6]]
        >>> Iter.range(1,6).chunk_every(3, 2, [7])
        [[1, 2, 3], [3, 4, 5], [5, 6, 7]]
        >>> Iter.range(1, 4).chunk_every(3, 3)
        [[1, 2, 3], [4]]
        ```
        """
        self.image = [list(self.image)[i:i+count] for i in range(0, len(self.image), step or count)]
        if leftover: self.image[-1].extend(leftover[:len(self.image[-1])])
        return self

    def chunk_while(self: Self, acc: List, chunk_fun: Callable, chunk_after: Callable) -> Self:
        # reference implementation:
        # https://hexdocs.pm/elixir/1.12/Enum.html#chunk_while/4
        raise NotImplementedError("To be released in version 0.0.6")

    def combinations(self: Self, r: int) -> Self:
        """
        Return successive r-length combinations of elements in the iterable.

        ```python
        >>> Iter([1, 2, 3]).combinations(2)
        [(1, 2), (1, 3), (2, 3)]
        >>> Iter.range(1, 3).combinations(r=3)
        [(1, 2, 3)]
        ```
        """
        self.image = list(itertools.combinations(self.image, r=r))
        return self

    def combinations_with_replacement(self: Self, r: int) -> Self:
        """
        Return successive r-length combinations of elements in the iterable
        allowing individual elements to have successive repeats.

        ```python
        >>> Iter([1, 2, 3]).combinations_width_replacement(2)
        [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
        >>> Iter.range(1, 3).combinations_width_replacement(r=3)
        [(1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 2, 2), (1, 2, 3), (1, 3, 3), (2, 2, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3)]
        ```
        """
        self.image = list(itertools.combinations_with_replacement(self.image, r=r))
        return self

    def count(self: Self, fun: Optional[Callable[[Any], bool]] = None) -> int:
        """
        Return the size of the image if `fun` is `None`, else return the cardinality
        of the image for which `fun` returns a truthy value.

        ```python
        >>> Iter([1, 2, 3]).count()
        3
        >>> Iter.range(1, 5).count(lambda x: x % 2 == 0)
        2
        ```
        """
        return len(list(self.image)) if fun is None else len(list(filter(fun, self.image)))

    def count_until(self: Self, limit: int, fun: Optional[Callable[[Any], bool]] = None) -> int:
        """
        Determine the cardinality of the image for which `fun` returns a truthy value,
        stopping at `limit`.

        ```python
        >>> Iter.range(1, 20).count_until(5)
        5
        >>> Iter.range(1, 20).count_until(50)
        20
        ```
        """
        return len(list(self.image)[:limit]) if fun is None else len(list(filter(fun, self.image))[:limit])

    def dedup(self: Self) -> Self:
        """
        Enumerate the image, returning a list where all consecutive duplicated
        elements are collapsed to a single element.

        ```python
        >>> Iter([1, 2, 3, 3, 2, 1]).dedup()
        [1, 2, 3, 2, 1]
        ```
        """
        self.image = list(map(operator.itemgetter(0), itertools.groupby(self.image)))
        return self

    def dedup_by(self: Self, fun: Callable[[Any], bool]) -> Self:
        """
        Enumerates the image, returning a list where all consecutive duplicated
        elements are collapsed to a single element.

        ```python
        >>> Iter([5, 1, 2, 3, 2, 1]).dedup_by(lambda x: x > 2)
        [5, 1, 3, 2]
        >>> Iter([0, 4, 9, 1, 2, 0, 3, 4, 9]).dedup_by(lambda x: x < 2)
        [0, 4, 1, 2, 0, 3]
        >>> Iter([3, 6, 7, 7, 2, 0, 1, 4, 1]).dedup_by(lambda x: x == 2)
        [3, 2, 0]
        ```
        """
        self.image = [self.image[0], *[self.image[i] for i in range(1, len(self.image)) if fun(self.image[i-1]) != fun(self.image[i])]]
        return self

    def difference(self: Self, iter_: Iterable) -> Self:
        """
        Return the difference between the image and `iter_`, sorted in ascending
        order.

        ```python
        >>> Iter.range(1, 10).difference([4, 3, 2, 10])
        [1, 5, 6, 7, 8, 9]
        >>> Iter(list("abc")).difference(range(1, 11))
        ['a', 'b', 'c']
        ```
        """
        self.image = sorted(set(self.image) - set(iter_))
        return self

    def drop(self: Self, amount: int) -> Self:
        """
        Drop the `amount` of elements from the image. If a negative `amount` is
        given, the `amount` of last values will be dropped. The image will be
        enumerated once to retrieve the proper index and the remaining calculation
        is performed from the end.

        ```python
        >>> Iter([1, 2, 3]).drop(2)
        [3]
        >>> Iter([1, 2, 3]).drop(10)
        []
        >>> Iter([1, 2, 3]).drop(-1)
        [1, 2]
        ```
        """
        tmp = list(self.image)
        self.image = tmp[amount:] if amount > 0 else tmp[:len(tmp)+amount]
        return self

    def drop_every(self: Self, nth: int) -> Self:
        """
        Return a list of every `nth` element in the image dropped, starting with
        the first element. The first element is always dropped, unless `nth` is `0`.
        The second argument specifying every nth element must be a non-negative
        integer.

        ```python
        >>> Iter.range(1, 10).drop_every(2)
        [2, 4, 6, 8, 10]
        >>> Iter.range(1, 10).drop_every(0)
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> Iter.range(1, 3).drop_every(1)
        []
        ```
        """
        self.image = [] if nth == 1 else [self.image[i] for i in range(int(nth != 0), len(self.image), nth if nth > 1 else 1)]
        return self

    def drop_while(self: Self, fun: Callable[[Any], bool]) -> Self:
        """
        Drop elements at the beginning of the image while `fun` returns a truthy value.

        ```python
        >>> Iter([1, 2, 3, 2, 1]).drop_while(lambda x: x < 3)
        [3, 2, 1]
        ```
        """
        self.image = list(itertools.dropwhile(fun, self.image))
        return self

    def duplicates(self: Self) -> Self:
        """
        Return all duplicated occurrences from the image.

        ```python
        >>> Iter([1, 1, 1, 2, 2, 3, 4, 4]).duplicates()
        [1, 2, 4]
        ```
        """
        self.image = [item for item, count in Counter(self.image).items() if count > 1]
        return self

    def filter(self: Self, fun: Callable[[Any], bool]) -> Self:
        """
        Filter the image, i.e. return only those elements for which `fun` returns
        a truthy value.

        ```python
        >>> Iter.range(1, 3).filter(lambda x: x % 2 == 0)
        [2]
        ```
        """
        self.image = list(filter(fun, self.image))
        return self

    def find(self: Self, fun: Callable[[Any], bool], default: Optional[Any] = None) -> Optional[Any]:
        """
        Return the first element for which `fun` returns a truthy value. If no
        such element is found, return `default`.

        ```python
        >>> Iter.range(2, 4).find(lambda x: x % 2 == 1)
        3
        >>> Iter([2, 4, 6]).find(lambda x: x % 2 == 1)
        None
        >>> Iter([2, 4, 6]).find(lambda x: x % 2 == 1, default=0)
        0
        ```
        """
        return next(filter(fun, self.image), default)

    def find_index(self: Self, fun: Callable[[Any], bool]) -> Self:
        """
        Return a list of indices for all occurrences in the image whose filter-
        value produced by `fun` is equal to `True`, else an empty list.

        ```python
        >>> from iterfun import Functions as fun
        >>> Iter.range(1, 10).find_index(fun.is_even)
        [1, 3, 5, 7, 9]
        >>> Iter([2, 3, 4]).find_index(lambda x: x < 0)
        []
        ```
        """
        self.image = list(map(operator.itemgetter(0), filter(lambda x: fun(x[1]), enumerate(self.image))))
        return self

    def find_value(self: Self, fun: Callable[[Any], bool], default: Optional[Any] = None) -> Optional[Any]:
        """
        Similar to `self.find`, but return the value of the function invocation instead
        of the element itself.

        ```python
        >>> Iter([2, 4, 6]).find_value(lambda x: x % 2 == 1)
        None
        >>> Iter([2, 3, 4]).find_value(lambda x: x % 2 == 1)
        True
        >>> Iter.range(1, 3).find_value(lambda x: isinstance(x, bool), "no bools!")
        'no bools!'
        ```
        """
        found = next(filter(fun, self.image), default)
        return fun(found) if found is not default else default

    def flat_map(self: Self, fun: Callable[[Any], Any]) -> Self:
        """
        Map the given `fun` over the image and flattens the result.

        ```python
        >>> Iter([(1, 3), (4, 6)]).flat_map(lambda x: list(range(x[0], x[1]+1))).
        [1, 2, 3, 4, 5, 6]
        >>> Iter([1, 2, 3]).flat_map(lambda x: [[x]])
        [[1], [2], [3]]
        ```
        """
        self.image = list(itertools.chain(*map(fun, self.image)))
        return self

    def flat_map_reduce(self: Self, acc: int, fun: Callable[[Any, Any], Any]) -> Self:
        # reference implementation:
        # https://hexdocs.pm/elixir/1.12/Enum.html#flat_map_reduce/3
        raise NotImplementedError("To be released in version 0.0.6")

    def flatten(self: Self) -> Self:
        """
        Flatten the current image.

        ```python
        >>> Iter([[1, 2], [3, 4], [5], [6, None]]).flatten()
        [1, 2, 3, 4, 5, 6, None]
        ```
        """
        self.image = list(itertools.chain(*self.image))
        return self

    def frequencies(self: Self) -> Self:
        """
        Return a map with keys as unique elements of the image and values as
        the count of every element.

        ```python
        >>> Iter([1, 2, 2, 3, 4, 5, 5, 6]).frequencies()
        {1: 1, 2: 2, 3: 1, 4: 1, 5: 2, 6: 1}
        ```
        """
        self.image = Counter(self.image)
        return self

    def frequencies_by(self: Self, key_fun: Callable[[Any], Any]) -> Self:
        """
        Return a map with keys as unique elements given by `key_fun` and values
        as the count of every element.

        ```python
        >>> Iter(["aa", "aA", "bb", "cc"]).frequencies_by(str.lower)
        {"aa": 2, "bb": 1, "cc": 1}
        >>> Iter(["aaa", "aA", "bbb", "cc", "c"]).frequencies_by(len)
        {3: 2, 2: 2, 1: 1}
        ```
        """
        self.image = Counter(map(key_fun, self.image))
        return self

    def group_by(self: Self, key_fun: Callable[[Any], Any], value_fun: Optional[Callable[[Any], Any]] = None) -> Self:
        """
        Split the image into groups based on `key_fun`.

        The result is a map where each key is given by `key_fun` and each value
        is a list of elements given by `value_fun`. The order of elements within
        each list is preserved from the image. However, like all maps, the
        resulting map is unordered.

        ```python
        >>> Iter(["ant", "buffalo", "cat", "dingo"]).group_by(len)
        {3: ["ant", "cat"], 5: ["dingo"], 7: ["buffalo"]}
        >>> Iter(["ant", "buffalo", "cat", "dingo"]).group_by(len, operator.itemgetter(0))
        {3: ["a", "c"], 5: ["d"], 7: ["b"]}
        ```
        """
        def value(g): return list(g) if value_fun is None else list(map(value_fun, g))
        self.image = {k: value(g) for k, g in itertools.groupby(sorted(self.image, key=key_fun), key_fun)}
        return self

    def intersects(self: Self, iter_: Iterable) -> Self:
        """
        Return the intersection between the image and `iter_`, sorted in ascending
        order.

        ```python
        >>> Iter([1, 2, 3, 4]).intersects([5, 6, 1, 2])
        [1, 2]
        >>> Iter.range(1, 10).intersects(list("abc")).count() > 0
        False
        ```
        """
        self.image = sorted(set(self.image) & set(iter_))
        return self

    def intersperse(self: Self, separator: Any) -> Self:
        """
        Intersperses separator between each element of the image.

        ```python
        >>> Iter([1, 3]).intersperse(0)
        [1, 0, 2, 0, 3]
        >>> Iter([1]).intersperse(0)
        [1]
        >>> Iter([]).intersperse(0)
        []
        ```
        """
        self.image = list(itertools.islice(itertools.chain.from_iterable(zip(itertools.repeat(separator), self.image)), 1, None))
        return self

    def into(self: Self, iter_: Iterable) -> Self:
        """
        Insert the given image into `iter_`.

        ```python
        >>> Iter([1, 2]).into([])
        [1, 2]
        >>> Iter({'a': 1, 'b': 2}).into({})
        {'a': 1, 'b': 2}
        >>> Iter({'a': 1}).into({'b': 2})
        {'a': 1, 'b': 2}
        ```
        """
        self.image = {**self.image, **iter_} if isinstance(iter_, Dict) else [*self.image, *iter_]
        return self

    def is_disjoint(self: Self, iter_: Iterable) -> bool:
        """
        Test whether the `iter_` has no elements in common with the image. Sets
        are disjoints if and only if their intersection is the empty set.

        ```python
        >>> Iter.range(1, 10).is_disjoint([11, 12, 13])
        True
        >>> Iter([1, 2, 3]).is_disjoint([1, 2, 3])
        False
        ```
        """
        return set(self.image).isdisjoint(iter_)

    def is_empty(self: Self) -> bool:
        """
        Test if the image is empty.

        ```python
        >>> Iter([]).is_empty()
        True
        >>> Iter([0]).is_empty()
        False
        >>> Iter.range(1, 10).is_empty()
        False
        ```
        """
        return not bool(len(self.image))

    def is_member(self: Self, element: Any) -> bool:
        """
        Test if an element exists in the image.

        ```python
        >>> Iter.range(1, 10).member(5)
        True
        >>> Iter.range(1, 10).member(5.0)
        False
        >>> Iter([1.0, 2.0, 3.0]).member(2)
        True
        >>> Iter([1.0, 2.0, 3.0]).member(2.000)
        True
        >>> Iter(['a', 'b', 'c']).member('d')
        False
        ```
        """
        return element in self.image

    def is_subset(self: Self, iter_: Iterable, proper: bool = False) -> bool:
        """
        Test whether every element in `iter_` is in the image.

        ```python
        >>> Iter.range(1, 10).is_subset([1, 2])
        True
        >>> Iter([1, 2, 3]).is_subset([1, 2, 3])
        True
        >>> Iter([1, 2, 3]).is_subset([1, 2, 3], proper=True)
        False
        ```
        """
        return set(iter_) < set(self.image) if proper else set(iter_).issubset(self.image)

    def is_superset(self: Self, iter_: Iterable, proper: bool = False) -> bool:
        """
        Test whether every element in the image is in `iter_`.

        ```python
        >>> Iter.range(1, 10).is_subset([1, 2])
        True
        >>> Iter([1, 2, 3]).is_subset([1, 2, 3])
        True
        >>> Iter([1, 2, 3]).is_subset([1, 2, 3], proper=True)
        False
        ```
        """
        return set(iter_) > set(self.image) if proper else set(iter_).issuperset(self.image)

    def join(self: Self, joiner: Optional[str] = None) -> str:
        """
        Join the image into a string using `joiner` as a separator. If `joiner`
        is not passed at all, it defaults to an empty string. All elements in
        the image must be convertible to a string, otherwise an error is raised.

        ```python
        >>> Iter([1,5]).join()
        '12345'
        >>> Iter[[1,5]].join(',')
        '1,2,3,4,5'
        ```
        """
        return f"{joiner or ''}".join(map(str, self.image))

    @staticmethod
    def __round(dec: Decimal, prec: int, rounding: str = ROUND_HALF_UP) -> Decimal:
        return dec.quantize(Decimal(10)**-prec, rounding)

    @staticmethod
    def linspace(a: int | float, b: int | float, step: int = 50, prec: int = 28) -> Iter:
        """
        Return evenly spaced numbers over a specified closed interval `[a, b]`.
        Set delta precision by rounding to `prec` decimal places.

        ```python
        >>> Iter.linspace(1.1, 3.3, step=10, prec=2)
        [1.1, 1.32, 1.54, 1.76, 1.98, 2.2, 2.42, 2.64, 2.86, 3.08, 3.3]
        ```
        """
        delta = Iter.__round(Decimal(str(abs(a - b) / step)), prec)
        return Iter([float(Decimal(str(a)) + i * delta) for i in range(step+1)])

    @overload
    def map(self: Self, fun: Callable[[Any], Any]) -> Self:
        """
        Return a list where each element is the result of invoking `fun` on each
        corresponding element of the image.

        ```python
        >>> Iter.range(1,3).map(lambda x: 2 * x)
        [2, 4, 6]
        ```
        """
        ...

    @overload
    def map(self: Self, fun: Callable[[Any, Any], Dict]) -> Self:
        """
        Return a dictionary where each element is the result of invoking `fun` on each
        corresponding key-value pair of the image.

        ```python
        >>> Iter({'a': 1, 'b': 2}).map(lambda k, v: {k: -v})
        {'a': -1, 'b': -2}
        ```
        """
        ...

    def map(self: Self, fun: Callable[[Any], Any]) -> Self:
        self.image = dict(ChainMap(*itertools.starmap(fun, self.image.items()))) if isinstance(self.image, Dict) else list(map(fun, self.image))
        return self

    def map_every(self: Self, nth: int, fun: Callable[[Any], Any]) -> Self:
        """
        Return a list of results of invoking `fun` on every `nth` element of the image,
        starting with the first element. The first element is always passed to the given
        function, unless `nth` is `0`.

        ```python
        >>> Iter.range(1, 10).map_every(2, lambda x: x + 1000)
        [1001, 2, 1003, 4, 1005, 6, 1007, 8, 1009, 10]
        >>> Iter.range(1, 5).map_every(0, lambda x: x + 1000)
        [1, 2, 3, 4, 5]
        >>> Iter.range(1, 3).map_every(1, lambda x: x + 1000)
        [1001, 1002, 1003]
        ```
        """
        if nth != 0:
            for i in range(0, len(self.image), nth):
                self.image[i] = fun(self.image[i])
        return self

    def map_intersperse(self: Self, separator: Any, fun: Callable[[Any], Any]) -> Self:
        """
        Map and intersperses the image in one pass.

        ```python
        >>> Iter.range(1, 3).map_intersperse(None, lambda x: 2 * x)
        [2, None, 4, None, 6]
        ```
        """
        self.image = list(itertools.islice(itertools.chain.from_iterable(zip(itertools.repeat(separator), map(fun, self.image))), 1, None))
        return self

    def map_join(self: Self, fun: Callable[[Any], Any], joiner: Optional[str] = None) -> str:
        """
        Map and join the image in one pass. If joiner is not passed at all, it
        defaults to an empty string. All elements returned from invoking `fun` must
        be convertible to a string, otherwise an error is raised.

        ```python
        >>> Iter.range(1, 3).map_join(lambda x: 2 * x)
        '246'
        >>> Iter.range(1, 3).map_join(lambda x: 2 * x, " = ")
        '2 = 4 = 6'
        ```
        """
        return f"{joiner or ''}".join(map(str, map(fun, self.image)))

    def map_reduce(self: Self, acc: int | float | complex, fun: Callable[[Any], Any], acc_fun: Optional[Callable[[Any, Any], Any]]) -> Self:
        """
        Invoke the given function to each element in the image to reduce it to
        a single element, while keeping an accumulator. Return a tuple where the
        first element is the mapped image and the second one is the final accumulator.

        ```python
        >>> Iter.range(1, 3).map_reduce(0, lambda x: 2 * x, lambda x, acc: x + acc)
        ([2, 4, 6], 6)
        >>> Iter.range(1, 3).map_reduce(6, lambda x: x * x, operator.sub)
        ([1, 4, 9], 0)
        ```
        """
        self.image = (list(map(fun, self.image)), functools.reduce(acc_fun, self.image, acc))
        return self

    def max(self: Self, fun: Optional[Callable[[Any], Any]] = None, empty_fallback: Optional[Any] = None) -> Any:
        """
        Return the maximum of the image as determined by the function `fun`.

        ```python
        >>> Iter.range(1, 3).max()
        3
        >>> Iter("you shall not pass".split()).max()
        'you'
        >>> Iter("you shall not pass".split()).max(len)
        'shall'
        >>> Iter([]).max(empty_fallback='n/a')
        'n/a'
        ```
        """
        return (max(self.image, key=fun) if fun is not None else max(self.image)) if self.image else empty_fallback

    def min(self: Self, fun: Optional[Callable[[Any], Any]] = None, empty_fallback: Optional[Any] = None) -> Any:
        """
        Return the minimum of the image as determined by the function `fun`.

        ```python
        >>> Iter.range(1, 3).min()
        1
        >>> Iter("you shall not pass".split()).min()
        'you'
        >>> Iter("you shall not pass".split()).min(len)
        'not'
        >>> Iter([]).max(empty_fallback='n/a')
        'n/a'
        ```
        """
        return (min(self.image, key=fun) if fun is not None else min(self.image)) if self.image else empty_fallback

    def min_max(self: Self, fun: Optional[Callable[[Any], Any]] = None, empty_fallback: Optional[Any] = None) -> Annotated[Tuple[Any], 2]:
        """
        Return a tuple with the minimal and the maximal elements in the image.

        ```python
        >>> Iter([1, 3]).min_max()
        (1, 3)
        >>> Iter([]).min_max(empty_fallback=None)
        (None, None)
        >>> Iter(["aaa", "a", "bb", "c", "ccc"]).min_max(len)
        ('a', 'aaa')
        ```
        """
        return (self.min(fun, empty_fallback), self.max(fun, empty_fallback))

    @overload
    @staticmethod
    def open(path: str | Path, encoding: str = "utf-8", strip: bool = True) -> Iter:
        """
        Read a plain text file and store its content as a list in the image. This
        methods `file` keyword argument defaults to `File.TEXT`. Set `strip` to
        `False` to disable LF and whitespace trimming (on by default).

        ```python
        >>> Iter.open("people.txt", encoding="cp1252")
        ["Stefan", "Monika", "Anneliese"]
        ```
        """
        ...

    @overload
    @staticmethod
    def open(path: str | Path, encoding: str = "utf-8", delimiter: str = ",", skip_header: bool = False) -> Iter:
        """
        Deserialize a CSV file and store its content as a nested list in the image.
        Pass `File.JSON` to the `file` keyword argument to read a file with the
        `csv` module.

        ```python
        >>> Iter.open("data.csv", skip_header=True)
        [['Stefan', '27'], ['Monika', '28'], ['Anneliese', '33']]
        ```
        """
        ...

    @overload
    @staticmethod
    def open(path: str | Path, encoding: str = "utf-8") -> Iter:
        """
        Deserialize a JSON file and store its content as a dictionary in the image.
        Pass `File.JSON` to the `file` keyword argument to read a file with the
        `json` module.

        ```python
        >>> Iter.open("people.json")
        {'People': [{'Name': 'Stefan', 'Age': 27}, {'Name': 'Monika', 'Age': 28}, {'Name': 'Anneliese', 'Age': 33}]}
        ```
        """
        ...

    @overload
    @staticmethod
    def open(path: str | Path) -> Iter:
        """
        To be released in version 0.0.6
        """
        ...

    @staticmethod
    def open(path: str | Path, encoding: str = "utf-8", strip: bool = True, delimiter: str = ",", skip_header: bool = False) -> Iter:
        extension = Path(path).suffix.lower()

        if extension == ".csv":
            with open(path, mode='r', encoding=encoding) as csv_handler:
                data = csv.reader(csv_handler, delimiter=delimiter, dialect=csv.excel)
                if skip_header: next(data)
                return Iter([row for row in data])
        elif extension == ".json":
            with open(path, mode='r', encoding=encoding) as json_handler:
                data = json.load(json_handler)
                return Iter(data)
        elif extension in [".png", ".jpg", ".jpeg"]:
            raise NotImplementedError("To be released in version 0.0.6")
        else:
            with open(path, mode='r', encoding=encoding) as text_handler:
                data = text_handler.readlines()
                return Iter([line.rstrip('\n').strip() if strip else line for line in data])

    def permutations(self: Self, r: Optional[int] = None) -> Self:
        """
        Return successive r-length permutations of elements in the iterable.

        ```python
        >>> Iter([1, 2, 3]).permutations()
        [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
        >>> Iter.range(1, 3).permutations(r=2)
        [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
        ```
        """
        self.image = list(itertools.permutations(self.image, r=r))
        return self

    def product(self: Self) -> (float | int | complex):
        """
        Return the product of all elements.

        ```python
        >>> Iter([2, 3, 4]).product()
        24
        >>> Iter([2.0, 3.0, 4.0]).product()
        24.0
        ```
        """
        return functools.reduce(operator.mul, self.image, 1)

    @staticmethod
    def __randint(a: int, b: int, size: int, secure: Optional[bool] = False) -> Generator[int]:
        for _ in range(size):
            yield secrets.choice(range(a, b+1)) if secure else random.randint(a, b)

    @staticmethod
    def randint(a: int, b: int, size: int, secure: Optional[bool] = False) -> Iter:
        """
        Generate a collection of random integers. Uses a pseudo-random number
        generator (PRNG) by default, which can be turned off by setting `secure`
        to `True` which falls back to the cryptographically secure `secrets` module
        that runs slower in comparison.

        ```python
        >>> Iter.randint(1, 10, 10)
        [4, 2, 7, 3, 5, 10, 9, 8, 7, 2]
        >>> Iter.randint(1, 10_000, size=10, secure=True)
        [9642, 7179, 1514, 3683, 5117, 9256, 1318, 9880, 5597, 2605]
        ```
        """
        return Iter(Iter.__randint(a, b, size, secure))

    def random(self: Self, secure: Optional[bool] = False) -> Any:
        """
        Return a random element from the image. Uses a pseudo-random number
        generator (PRNG) by default, which can be turned off by setting `secure`
        to `True` which falls back to the cryptographically secure `secrets` module
        that runs slower in comparison.

        ```python
        >>> Iter.range(1, 100).random()
        42
        >>> Iter.range(1, 100).random()
        69
        ```
        """
        return secrets.choice(self.image) if secure else random.choice(self.image)

    @overload
    @staticmethod
    def range(a: int, b: int, step: Optional[int] = 1) -> Iter:
        """
        Return a sequence of integers from `a` (inclusive) to `b` (inclusive) by
        `step`. When `step` is given, it specifies the increment (or decrement).

        ```python
        >>> Iter.range(1, 5)
        [1, 2, 3, 4, 5]
        >>> Iter.range(1, 5, 2)
        [1, 3, 5]
        ```
        """
        ...

    @overload
    @staticmethod
    def range(a: float, b: float, step: Optional[float] = 0.1) -> Iter:
        """
        Return a sequence of floats from `a` (inclusive) to `b` (inclusive) by
        `step`. When `step` is given, it specifies the increment (or decrement).

        ```python
        >>> Iter.range(0.1, 1.0)
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        >>> Iter.range(0.5, 5.0, 0.5)
        [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        >>> Iter.range(5.0, 0.5, -0.5)
        [5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5]
        ```
        """
        ...

    @staticmethod
    def __range(a: float, b: float, step: float) -> Generator[float]:
        a2, n2 = Decimal(str(a)), Decimal(str(step))
        for i in range(int((b - a) / step) + 1):
            yield float(a2 + (i * n2))

    @staticmethod
    def range(a: int | float, b: int | float, step: Optional[int | float] = None) -> Iter:
        if step == 0: raise ValueError("step must not be zero")
        tmp = step or 1
        return Iter(list(range(a, b + Functions.sign(tmp), tmp) if isinstance(a, int) else Iter.__range(a, b, step or 0.1)))

    def reduce(self: Self, fun: Callable[[Any, Any], Any], acc: int = 0) -> Any:
        """
        Invoke `fun` for each element in the image with the accumulator. The
        accumulator defaults to `0` if not otherwise specified. Reduce (sometimes
        also called fold) is a basic building block in functional programming.

        ```python
        >>> Iter.range(1, 4).reduce(operator.add)
        10
        >>> Iter.range(1, 4).reduce(lambda x, acc: x * acc, acc=1)
        24
        ```
        """
        return functools.reduce(fun, self.image, acc)

    def reduce_while(self: Self, fun: Callable[[Any, Any], Tuple[bool, Any]], acc: int = 0) -> Any:
        """
        Reduce the image until `fun` returns `(False, acc)`.

        ```python
        >>> Iter.range(1, 100).reduce_while(lambda x, acc: (True, acc + x) if x < 5 else (False, acc))
        10
        >>> Iter.range(1, 100).reduce_while(lambda x, acc: (True, acc - x) if x % 2 == 0 else (False, acc), acc=2550)
        0
        ```
        """
        return functools.reduce(lambda acc, x: fun(x, acc)[1], filter(lambda x: fun(x, acc)[0], self.image), acc)

    def reject(self: Self, fun: Callable[[Any], bool]) -> Self:
        """
        Return a list of elements in the image excluding those for which the
        function `fun` returns a truthy value.

        ```python
        >>> Iter.range(1, 3).reject(lambda x: x % 2 == 0)
        [1, 3]
        ```
        """
        self.image = list(itertools.filterfalse(fun, self.image))
        return self

    @overload
    def reverse(self: Self) -> Self:
        """
        Return a list of elements in the image in reverse order.

        ```python
        >>> Iter.range(1, 5).reverse()
        [5, 4, 3, 2, 1]
        ```
        """
        ...

    @overload
    def reverse(self: Self, tail: Optional[List] = None) -> Self:
        """
        Reverse the elements in the image, appends the `tail`, and returns it
        as a list.

        ```python
        >>> Iter.range(1, 3).reverse([4, 5, 6])
        [3, 2, 1, 4, 5, 6]
        ```
        """
        ...

    def reverse(self: Self, tail: Optional[List] = None) -> Self:
        self.image = list(reversed(self.image))
        if tail: self.image.extend(tail)
        return self

    def reverse_slice(self: Self, start_index: int, count: int) -> Self:
        """
        Reverse the image in the range from initial `start_index` through `count`
        elements. If `count` is greater than the size of the rest of the image,
        then this function will reverse the rest of the image.

        ```python
        >>> Iter.range(1, 6).reverse_slice(2, 4)
        [1, 2, 6, 5, 4, 3]
        >>> Iter.range(1, 10).reverse_slice(2, 4)
        [1, 2, 6, 5, 4, 3, 7, 8, 9, 10]
        >>> Iter.range(1, 10).reverse_slice(2, 30)
        [1, 2, 10, 9, 8, 7, 6, 5, 4, 3]
        ```
        """
        self.image = [*self.image[:start_index], *reversed(self.image[start_index:count+start_index]), *self.image[count+start_index:]]
        return self

    @overload
    def save(self: Self, path: str | Path, encoding: str = "utf-8", overwrite: bool = False) -> None:
        """
        Store all elements in the image with their string representation as a plain text file to disk.

        ```python
        >>> Iter.range(1, 10).map(lambda x: x**2).save("data.txt")
        ```
        """
        ...

    @overload
    def save(self: Self, path: str | Path, encoding: str = "utf-8", delimiter: str = ",", overwrite: bool = False) -> None:
        """
        Store all elements in the image with their string representation as a CSV file to disk.

        ```python
        >>> Iter.range(1, 10).chunk_every(2).save("data.csv")
        ```
        """
        ...

    @overload
    def save(self: Self, path: str | Path, encoding: str = "utf-8", indent: int = 4, sort_keys: bool = False, overwrite: bool = False) -> None:
        """
        Store all elements in the image as a JSON file to disk.

        ```python
        >>> Iter({'a': 1, 'b':2}).map(lambda k, v: {k: -v * 10}).save("data.json", indent=2)
        ```
        """
        ...

    @overload
    def save(self: Self, path: str | Path, overwrite: bool = False) -> None:
        """
        To be released in version 0.0.6
        """
        ...

    def save(self: Self, path: str | Path, encoding: str = "utf-8", delimiter: str = ",", indent: int = 4, sort_keys: bool = False, overwrite: bool = False) -> None:
        extension = Path(path).suffix.lower()
        if overwrite: os.remove(path)

        with open(path, mode='w', encoding=encoding) as file_handler:
            if extension == ".csv":
                writer = csv.writer(file_handler, delimiter=delimiter)
                writer.writerows(self.image)
            elif extension == ".json":
                data = json.dumps(self.image, indent=indent, sort_keys=sort_keys)
                file_handler.write(data)
            elif extension in [".png", ".jpg", ".jpeg"]:
                raise NotImplementedError("To be released in version 0.0.6")
            else:
                file_handler.writelines('\n'.join(map(str, self.image)))

    def scan(self: Self, fun: Callable[[Any, Any], Any], acc: Optional[int] = None) -> Self:
        """
        Apply the given function `fun` to each element in the image, storing the result
        in a list and passing it as the accumulator for the next computation. Uses
        the first element in the image as the starting value if `acc` is `None`,
        else uses the given `acc` as the starting value.

        ```python
        >>> Iter.range(1, 5).scan(operator.add)
        [1, 3, 6, 10, 15]
        >>> Iter.range(1, 5).scan(lambda x, y: x + y, acc=0)
        [1, 3, 6, 10, 15]
        ```
        """
        acc = acc if acc is not None else 0
        self.image = list(map(lambda x: x + acc, itertools.accumulate(self.image, fun)))
        return self

    def shorten(self: Self, width: int = 20) -> str:
        """
        Shorten an iterable sequence into a short, human-readable string.

        ```python
        >>> Iter.range(1, 6).shorten()
        '[1, 2, 3, 4, 5]'
        >>> Iter.range(1, 100).shorten(width=50)
        '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,...]'
        ```
        """
        return textwrap.shorten(str(self.image), width=width, placeholder=' ...]')

    def shuffle(self: Self) -> Self:
        """
        Return a list with the elements of the image shuffled.

        ```python
        >>> Iter.range(1, 3).shuffle()
        [3, 1, 2]
        ```
        """
        random.shuffle(self.image)
        return self

    @overload
    def slice(self: Self, index: List[int]) -> Self:
        """
        Return a subset list of the image by `index`.

        Given an `Iter`, it drops elements before `index[0]` (zero-base),
        then it takes elements until element `index[1]` (inclusively). Indexes
        are normalized, meaning that negative indexes will be counted from the end.

        If `index[1]` is out of bounds, then it is assigned as the index of
        the last element.

        ```python
        >>> Iter.range(1, 100).slice([5, 10])
        [6, 7, 8, 9, 10, 11]
        >>> Iter.range(1, 10).slice([5, 20])
        [6, 7, 8, 9, 10]
        >>> Iter.range(1, 30).slice([-5, -1])
        [26, 27, 28, 29, 30]
        ```
        """
        ...

    @overload
    def slice(self: Self, index: int, amount: Optional[int] = None) -> Self:
        """
        Return a subset list of the image, from `index` (zero-based) with `amount`
        number of elements if available. Given the image, it drops elements right
        before element `index`; then, it takes `amount` of elements, returning as
        many elements as possible if there are not enough elements.

        A negative `index` can be passed, which means the image is enumerated
        once and the index is counted from the end (for example, `-1` starts slicing
        from the last element). It returns `[]` if `amount` is `0` or if `index` is
        out of bounds.

        ```python
        >>> Iter.range(1, 10).slice(5, 100)
        [6, 7, 8, 9, 10]
        ```
        """
        ...

    def slice(self: Self, index: int | List[int], amount: Optional[int] = None) -> Self:
        if isinstance(index, List):
            self.image = self.image[index[0]:] if index[1] == -1 else self.image[index[0]:index[1]+1]
        else:
            self.image = self.image[index:amount] if abs(index) <= len(self.image) else []
        return self

    @overload
    def slide(self: Self, index: int, insertion_index: int) -> Self:
        """
        Slide a single or multiple elements given by `index` from the image to
        `insertion_index`. The semantics of the range to be moved match the semantics
        of `self.slice()`.

        ```python
        >>> Iter(list("abcdefg")).slide(5, 1)
        ['a', 'f', 'b', 'c', 'd', 'e', 'g']
        >>> Iter(list("abcdefg")).slide([3, 5], 1) # slide backwards
        ['a', 'd', 'e', 'f', 'b', 'c', 'g']
        >>> Iter(list("abcdefg")).slide([1, 3], 5) # slide forwards
        ['a', 'e', 'f', 'b', 'c', 'd', 'g']
        >>> Iter(list("abcdefg")).slide(3, -1)
        ['a', 'b', 'c', 'e', 'f', 'g', 'd']
        ```
        """
        ...

    @overload
    def slide(self: Self, index: List[int], insertion_index: int) -> Self: ...

    def slide(self: Self, index: int | List[int], insertion_index: int) -> Self:
        if isinstance(index, List):
            if (max(index) + len(self.image) if max(index) < 0 else max(index)) > insertion_index:
                p1 = self.image[:insertion_index]
                p3 = self.image[index[0]:index[1]+1]
                p2 = self.image[insertion_index:index[0]]
                p4 = self.image[index[1]+1:]
                self.image = list(itertools.chain(p1, p3, p2, p4))
            else:
                p1 = self.image[:index[0]]
                p2 = self.image[index[0]:index[1]+1]
                p3 = self.image[index[1]+1:insertion_index+1]
                p4 = self.image[insertion_index+1:]
                self.image = list(itertools.chain(p1, p3, p2, p4))
        else:
            element, ii = self.image.pop(index), insertion_index
            self.image.insert((ii, ii+1)[ii < 0], element) if ii != -1 else self.image.append(element)
        return self

    def sort(self: Self, fun: Optional[Callable[[Any], bool]] = None, descending: bool = False) -> Self:
        """
        Return a new sorted image. `fun` specifies a function of one argument that
        is used to extract a comparison key from each element in iterable (for example,
        `key=str.lower`). The `descending` flag can be set to sort the image in
        descending order (ascending by default).

        Use `functools.cmp_to_key()` to convert an old-style cmp function to a key
        function.

        ```python
        >>> Iter([3, 1, 2]).sort()
        [1, 2, 3]
        ```
        """
        self.image = sorted(self.image, key=fun, reverse=descending)
        return self

    def split(self: Self, count: int) -> Self:
        """
        Split the image into two lists, leaving `count` elements in the first
        one. If `count` is a negative number, it starts counting from the back to
        the beginning of the image.

        ```python
        >>> Iter.range(1, 3).split(2)
        [[1,2], [3]]
        >>> Iter.range(1, 3).split(10)
        [[1, 2, 3], []]
        >>> Iter.range(1, 3).split(0)
        [[], [1, 2, 3]]
        >>> Iter.range(1, 3).split(-1)
        [[1, 2], [3]]
        ```
        """
        self.image = [self.image[:count], self.image[count:]]
        return self

    def split_while(self: Self, fun: Callable[[Any], bool]) -> Self:
        """
        Split the image in two at the position of the element for which `fun`
        returns a falsy value for the first time.

        It returns a nested list of length two. The element that triggered the split
        is part of the second list.

        ```python
        >>> Iter.range(1, 4).split_while(lambda x: x < 3)
        [[1, 2], [3, 4]]
        >>> Iter.range(1, 4).split_while(lambda x: x < 0)
        [[], [1, 2, 3, 4]]
        >>> Iter.range(1, 4).split_while(lambda x: x > 0)
        [[1, 2, 3, 4], []]
        ```
        """
        default = len(self.image) + 1
        element = next(itertools.filterfalse(fun, self.image), default)
        count = self.image.index(element) if element in self.image else default
        self.image = [self.image[:count], self.image[count:]]
        return self

    @overload
    def split_with(self: Self, fun: Callable[[Any], bool]) -> Self:
        """
        Split the image in two lists according to the given function `fun`.

        Split the image in two lists by calling `fun` with each element in
        the image as its only argument. Returns a nested list with the first
        list containing all the elements in the image for which applying `fun`
        returned a truthy value, and a second list with all the elements for which
        applying `fun` returned a falsy value. The same logic is also applied when
        a key-value paired lambda expression is passed as an argument, as a consequence
        of which the dictionary will be also split into two parts following the
        same pattern.

        The elements in both the returned lists (or dictionaries) are in the same
        relative order as they were in the original image (if such iterable was
        ordered, like a list).

        ```python
        >>> Iter([1, 5]).reverse().split_with(lambda x: x % 2 == 0)
        [[4, 2, 0], [5, 3, 1]]
        >>> Iter({'a': 1, 'b': -2, 'c': 1, 'd': -3}).split_with(lambda k, v: v < 0)
        [{'b': -2, 'd': -3}, {'a': 1, 'c':1}]
        ```
        """
        ...

    @overload
    def split_with(self: Self, fun: Callable[[Any, Any], bool]) -> Self: ...

    def split_with(self: Self, fun: Callable[[Any], bool] | Callable[[Any, Any], bool]) -> Self:
        if isinstance(self.image, Dict):
            f1 = ChainMap(*[{k: v} for k, v in self.image.items() if fun(k, v)])
            f2 = ChainMap(*[{k: v} for k, v in self.image.items() if not fun(k, v)])
            self.image = [dict(f1), dict(f2)]
        else:
            t1, t2 = itertools.tee(self.image)
            self.image = [list(filter(fun, t1)), list(itertools.filterfalse(fun, t2))]
        return self

    def sum(self: Self) -> Any:
        """
        Return the sum of all elements.

        ```python
        >>> Iter.range(1, 100).sum()
        5050
        ```
        """
        return sum(self.image)

    def symmetric_difference(self: Self, iter_: Iterable) -> Self:
        """
        Return the symmetric difference between the image and `iter_`.

        ```python
        >>> Iter.range(1, 10).symmetric_difference(range(5, 16))
        [1, 2, 3, 4, 11, 12, 13, 14, 15]
        ```
        """
        self.image = list(set(self.image).symmetric_difference(iter_))
        return self

    def take(self: Self, amount: int) -> Self:
        """
        Takes an `amount` of elements from the beginning or the end of the image.
        If a positive `amount` is given, it takes the amount elements from the
        beginning of the image. If a negative `amount` is given, the amount of
        elements will be taken from the end. The image will be enumerated once
        to retrieve the proper index and the remaining calculation is performed from
        the end. If `amount` is `0`, it returns `[]`.

        ```python
        >>> Iter.range(1, 3).take(2)
        [1, 2]
        >>> Iter.range(1, 3).take(10)
        [1, 2, 3]
        >>> Iter([1, 2, 3]).take(0)
        []
        >>> Iter([1, 2, 3]).take(-1)
        [3]
        ```
        """
        self.image = list(itertools.islice(self.image if amount > 0 else reversed(self.image), abs(amount)))
        return self

    def take_every(self: Self, nth: int) -> Self:
        """
        Return a list of every `nth` element in the image, starting with the
        first element. The first element is always included, unless `nth` is `0`.
        The second argument specifying every `nth` element must be a non-negative
        integer.

        ```python
        >>> Iter.range(1, 10).take_every(2)
        [1, 3, 5, 7, 9]
        >>> Iter.range(1, 10).take_every(0)
        []
        >>> Iter.range(1, 3).take_every(1)
        [1, 2, 3]
        ```
        """
        self.image = list(itertools.islice(self.image, 0, len(self.image), nth)) if nth != 0 else []
        return self

    def take_random(self: Self, count: int) -> Self:
        """
        Take `count` random elements from the image.

        ```python
        >>> Iter.range(1, 10).take_random(2)
        [4, 2]
        >>> Iter.range(1, 10).take_random(2)
        [6, 9]
        ```
        """
        self.image = random.choices(self.image, k=count)
        return self

    def take_while(self: Self, fun: Callable[[Any], bool]) -> Self:
        """
        Take the elements from the beginning of the image while `fun` returns
        a truthy value.

        ```python
        >>> Iter.range(1, 3).take_while(lambda x: x < 3)
        [1, 2]
        ```
        """
        self.image = list(itertools.takewhile(fun, self.image))
        return self

    def to_dict(self: Self) -> Dict:
        """
        Return the image as a dictionary object.
        """
        return dict(self.image)

    def to_list(self: Self) -> List[Any]:
        """
        Return the image as a list object.
        """
        return list(self.image)

    def transpose(self: Self, fillvalue: Optional[Any] = None) -> Self:
        """
        Transpose the image. When the shorter iterables are exhausted, the `fillvalue`
        is substituted in their place.

        ```python
        >>> Iter([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]).transpose()
        [('a', 'd', 'g'), ('b', 'e', 'h'), ('c', 'f', 'i')]
        >>> Iter([['a', 'b', 'c'], ['d', 'e'], ['g', 'h']]).transpose(fillvalue=False)
        [('a', 'd', 'g'), ('b', 'e', 'h'), ('c', False, False)]
        ```
        """
        self.image = list(itertools.zip_longest(*self.image, fillvalue=fillvalue))
        return self

    def union(self: Self, iter_: Iterable) -> Self:
        """
        Return the union between the image and `iter_`, sorted in ascending order.

        ```python
        >>> Iter([1, 2, 3, 4]).union([5, 6])
        [1, 2, 3, 4, 5, 6]
        >>> Iter([[1, 2], [3]]).flatten().union([4, 5, 6])
        [1, 2, 3, 4, 5, 6]
        ```
        """
        self.image = sorted(set(self.image) | set(iter_))
        return self

    def unique(self: Self) -> Self:
        """
        Enumerates the image, removing all duplicated elements.

        ```python
        >>> Iter([1, 2, 3, 3, 2, 1]).unique()
        [1, 2, 3]
        ```
        """
        self.image = list(Counter(self.image).keys())
        return self

    def unzip(self: Self) -> Self:
        """
        Opposite of `self.zip`. Extracts two-element tuples from the image and
        groups them together.

        ```python
        >>> Iter({'a': 1, 'b': 2, 'c': 3}).unzip()
        [['a', 'b', 'c'], [1, 2, 3]]
        >>> Iter([('a', 1), ('b', 2), ('c', 3)]).unzip()
        [['a', 'b', 'c'], [1, 2, 3]]
        >>> Iter([['a', 1], ['b', 2], ['c', 3]]).unzip()
        [['a', 'b', 'c'], [1, 2, 3]]
        ```
        """
        if isinstance(self.image, Dict):
            self.image = [list(self.image.keys()), list(self.image.values())]
        else:
            self.image = [list(map(operator.itemgetter(0), self.image)), list(map(operator.itemgetter(1), self.image))]
        return self

    @overload
    def with_index(self: Self, fun_or_offset: Optional[int] = None) -> Self:
        """
        Return the image with each element wrapped in a tuple alongside its index.
        May receive a function or an integer offset. If an offset is given, it will
        index from the given offset instead of from zero. If a function is given,
        it will index by invoking the function for each element and index (zero-based)
        of the image.

        ```python
        >>> Iter(list("abc")).with_index()
        [('a', 0), ('b', 1), ('c', 2)]
        >>> Iter(list("abc")).with_index(2)
        [('a', 2), ('b', 3), ('c', 4)]
        >>> Iter(list("abc")).with_index(lambda k, v: (v, k))
        [(0, 'a'), (1, 'b'), (2, 'c')]
        ```
        """
        ...

    @overload
    def with_index(self: Self, fun_or_offset: Callable[[Any, Any], Any]) -> Self: ...

    def with_index(self: Self, fun_or_offset: Optional[int] | Callable[[Any, Any], Any] = None) -> Self:
        if isinstance(fun_or_offset, int) or fun_or_offset is None:
            offset = 0 if fun_or_offset is None else fun_or_offset
            self.image = list(zip(self.image, range(offset, len(self.image)+offset)))
        else:
            self.image = list(itertools.starmap(fun_or_offset, zip(self.image, range(len(self.image)))))
        return self

    def zip(self: Self, *iter_: Tuple[Iterable, ...]) -> Self:
        """
        Zip corresponding elements from a finite collection of iterables into a
        list of tuples. The zipping finishes as soon as any iterable in the given
        collection completes.

        ```python
        >>> Iter(list("abc")).zip(range(3))
        [('a', 0), ('b', 1), ('c', 2)]
        >>> Iter(list("abc")).zip(range(3), list("def"))
        [('a', 0, 'd'), ('b', 1, 'e'), ('c', 2, 'f')]
        >>> Iter([1, 3]).zip(list("abc"), ["foo", "bar", "baz"])
        [(1, 'a', "foo"), (2, 'b', "bar"), (3, 'c', "baz")]
        ```
        """
        self.image = list(zip(self.image, *iter_))
        return self

    @overload
    def zip_reduce(self: Self, acc: List, reducer: Callable[[Any, Any], Any]) -> Self:
        """
        Reduce over all of the image, halting as soon as any iterable is empty.
        The reducer will receive 2 args: a list of elements (one from each enum) and
        the accumulator.

        ```python
        >>> Iter([[1, 1], [2, 2], [3, 3]]).zip_reduce([], lambda x, acc: tuple(x) + (acc,))
        [(1, 2, 3), (1, 2, 3)]
        ```
        """
        ...

    @overload
    def zip_reduce(self: Self, acc: List, reducer: Callable[[Any, Any], Any], left: Iterable, right: Iterable) -> Self:
        """
        Reduce over two iterables halting as soon as either iterable is empty.

        ```python
        >>> Iter([]).zip_reduce([5, 6], lambda x, acc: tuple(x) + (acc,), [1, 2], {'a': 3, 'b': 4})
        [(1, {'a': 3}, 5), (2, {'b': 4}, 6)]
        ```
        """
        ...

    def zip_reduce(self: Self, acc: List, reducer: Callable[[Any, Any], Any], left: Optional[Iterable] = None, right: Optional[Iterable] = None) -> Self:
        if left is not None and right is not None:
            # reference implementation:
            # https://hexdocs.pm/elixir/1.12/Enum.html#zip_reduce/3
            raise NotImplementedError("To be released in version 0.0.6")
        else:
            self.image = list(functools.reduce(reducer, zip(*self.image), acc))
        return self

    def zip_with(self: Self, fun: Callable[..., Any], *iterable: Tuple[Iterable, ...]) -> Self:
        """
        Zip corresponding elements from a finite collection of iterables into a list,
        transforming them with the `fun` function as it goes. The first element from
        each of the lists in iterables will be put into a list which is then passed
        to the 1-arity `fun` function. Then, the second elements from each of the
        iterables are put into a list and passed to `fun`, and so on until any one
        of the lists in `iterables` runs out of elements. Returns a list with all
        the results of calling `fun`.

        ```python
        >>> Iter([]).zip_with(operator.add, [1, 2, 3], [4, 5, 6])
        [5, 7, 9]
        >>> Iter([1, 1]).zip_with(operator.add, [1, 2], [3, 4, 6, 7]).image
        [5, 7]
        >>> Iter([]).zip_with(lambda x, y, z: x + y + z, [1, 3], [3, 5], [1, 3])
        [5, 11]
        ```
        """
        self.image = [fun(*args) for args in zip(*iterable)]
        return self

    #region magic methods

    def __eq__(self: Self, other: Iter) -> bool:
        return self.image == other.image

    def __ne__(self: Self, other: Iter) -> bool:
        return self.image != other.image

    def __iter__(self: Self) -> Iterator[Iter]:
        return self

    def __next__(self: Self) -> Any:
        if self.__index >= len(self.image): raise StopIteration
        self.__value = self.image[self.__index]
        self.__index += 1
        return self.__value

    def __repr__(self: Self) -> str:
        return f"Iter(image_type={self.image.__class__.__name__},len={len(self.image)})"

    def __str__(self: Self) -> str:
        return repr(self.image) if isinstance(self.image, Dict) else str(self.image)

    #endregion
