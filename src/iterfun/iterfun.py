#!/usr/bin/env python3

from __future__ import annotations

import functools
import itertools
import operator
import random
import statistics
import textwrap
from collections import ChainMap, Counter
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, Union, overload


class Iter:
    """
    Define a set of algorithms to work with iterable collections. In Python,
    an iterable is any data type that implements the `__iter__` method which
    returns an iterator, or alternatively, a `__getitem__` method suitable for
    indexed lookup such as `list`, `tuple`, `dict`, or `set`.

    ```python
    >>> Iter([1, 3]).map(lambda x: 2*x)
    [2, 4, 6]
    >>> Iter([1, 2, 3]).sum()
    6
    >>> Iter({'a': 1, 'b': 2}).map(lambda k, v: {k: 2 * v}
    {'a': 2, 'b': 4}
    ```
    """

    @overload
    def __init__(self, iter: Iterable, interval: bool=False) -> Iter: ...

    @overload
    def __init__(self, iter: List[int, int], interval: bool=True) -> Iter: ...

    @overload
    def __init__(self, iter: Tuple[int, int], interval: bool=True) -> Iter: ...

    def __init__(self, iter: Iterable | List[int, int] | Tuple[int, int], interval: bool=True) -> Iter:
        self.image = Iter.__ctor(iter) if interval and len(iter) == 2 else iter
        self.domain = self.image

    @staticmethod
    def __ctor(iter: Iterable | List[int, int] | Tuple[int, int]) -> List:
        if (isinstance(iter, Tuple) or isinstance(iter, List)) and (isinstance(iter[0], int) and isinstance(iter[1], int)):
            return Iter.range(iter) if iter[1] != 0 else []
        return iter

    def all(self, fun: Optional[Callable[[Any], bool]]=None) -> bool:
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
        >>> Iter([1, 2, 3]).all(lambda x: x % 2 == 0)
        False
        ```
        """
        self.image = all(self.image) if fun is None else all(map(fun, self.image))
        return self.image

    def any(self, fun: Optional[Callable[[Any], bool]]=None) -> bool:
        """
        Return `True` if any elements in `self.image` are truthy, or `True` if
        `fun` is not None and its map truthy for at least on element in `self.image`.

        ```python
        >>> Iter([False, False, False]).any()
        False
        >>> Iter([False, True, False]).any()
        True
        >>> Iter([2, 4, 6]).any(lambda x: x % 2 == 1)
        False
        ```
        """
        self.image = any(self.image) if fun is None else any(map(fun, self.image))
        return self.image

    def at(self, index: int) -> Any:
        """
        Find the element at the given `index` (zero-based). Raise an `IndexError`
        if `index` is out of bonds. A negative index can be passed, which means
        `self.image` is enumerated once and the index is counted from the end.

        ```python
        >>> Iter([2, 4, 6]).at(0)
        2
         >>> Iter([2, 4, 6]).at(-1)
        6
         >>> Iter([2, 4, 6]).at(4)
        IndexError: list index out of range
        ```
        """
        self.image = list(self.image)[index]
        return self.image

    def avg(self) -> Union[int, float]:
        """
        Return the sample arithmetic mean of `self.image`.

        ```python
        >>> Iter([0, 10]).avg()
        5
        ```
        """
        self.image = statistics.mean(self.image)
        return self.image

    def chunk_by(self, fun: Callable[[Any], bool]) -> Iter:
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
        >>> Iter([1, 6]).chunk_every(2)
        [[1, 2], [3, 4], [5, 6]]
        >>> Iter([1, 6]).chunk_every(3, 2, [7])
        [[1, 2, 3], [3, 4, 5], [5, 6, 7]]
        >>> Iter([1, 4]).chunk_every(3, 3)
        [[1, 2, 3], [4]]
        ```
        """
        step = step or count
        self.image = [list(self.image)[i:i+count] for i in range(0, len(self.image), count-(count-step))]
        if leftover: self.image[-1].extend(leftover[:len(self.image[-1])])
        return self

    def chunk_while(self, acc: List, chunk_fun: Callable, chunk_after: Callable) -> Iter:
        raise NotImplementedError()

    def concat(self) -> Iter:
        """
        Given a list of lists, concatenates the list into a single list.

        ```python
        >>> Iter([[1, 2, 3], [4, 5, 6]]).concat()
        [1, 2, 4, 5, 6]
        >>> Iter([[1, [2], 3], [4], [5, 6]]).concat()
        [1, [2], 3, 4, 5, 6]
        ```

        mode with ranges:

        ```python
        >>> Iter([[1, 4], [5, 6], [7, 9]]).concat()
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> Iter([(0, 4), (5, 6), (7, 9)]).concat()
        [1, 2, 3, 8]
        >>> Iter([(0, 4), (3, 7), (6, 10)]).concat()
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ```
        """
        if all(map(lambda x: len(x) == 2, self.image)):
            self.image = list(itertools.chain(*map(Iter.range, self.image)))
        else:
            self.image = list(itertools.chain(*self.image))
        return self

    def count(self, fun: Optional[Callable[[Any], bool]]=None) -> int:
        """
        Return the size of the `self.image` if `fun` is `None`, else return the
        count of elements in `self.image` for which `fun` returns a truthy value.

        ```python
        >>> Iter([1, 3]).count()
        3
        >>> Iter([1, 5]).count(lambda x: x % 2 == 0)
        2
        ```
        """
        return len(list(self.image)) if fun is None else len(list(filter(fun, self.image)))

    def count_until(self, limit: int, fun: Optional[Callable[[Any], bool]]=None) -> int:
        """
        Count the elements in `self.image` for which `fun` returns a truthy value,
        stopping at `limit`.

        ```python
        >>> Iter([1, 20]).count_until(5)
        5
        >>> Iter([1, 20]).count_until(50)
        20
        ```
        """
        return len(list(self.image)[:limit]) if fun is None else len(list(filter(fun, self.image))[:limit])

    def dedup(self) -> Iter:
        """
        Enumerate `self.image`, returning a list where all consecutive duplicated
        elements are collapsed to a single element.

        ```python
        >>> Iter([1, 2, 3, 3, 2, 1]).dedup()
        [1, 2, 3, 2, 1]
        ```
        """
        self.image = list(map(operator.itemgetter(0), itertools.groupby(self.image)))
        return self

    def dedup_by(self, fun: Callable[[Any], bool]):
        raise NotImplementedError()

    def drop(self, amount: int) -> Iter:
        """
        Drop the `amount` of elements from `self.image`. If a negative `amount` is
        given, the `amount` of last values will be dropped. `self.image` will be
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
        self.image = list(self.image)
        self.image = self.image[amount:] if amount > 0 else self.image[:len(self.image)+amount]
        return self

    def drop_every(self, nth: int) -> Iter:
        """
        Return a list of every `nth` element in the `self.image` dropped, starting
        with the first element. The first element is always dropped, unless `nth`
        is `0`. The second argument specifying every nth element must be a non-negative
        integer.

        ```python
        >>> Iter([1, 10]).drop_every(2)
        [2, 4, 6, 8, 10]
        >>> Iter([1, 10]).drop_every(0)
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> Iter([1, 3]).drop_every(1)
        []
        ```
        """
        self.image = [] if nth == 1 else [self.image[i] for i in range(int(nth != 0), len(self.image), nth if nth > 1 else 1)]
        return self

    def drop_while(self, fun: Callable[[Any], bool]) -> Iter:
        """
        Drop elements at the beginning of `self.image` while `fun` returns a
        truthy value.

        ```python
        >>> Iter([1, 2, 3, 2, 1]).drop_while(lambda x: x < 3)
        [3, 2, 1]
        ```
        """
        self.image = list(itertools.dropwhile(fun, self.image))
        return self

    def each(self, fun: Callable[[Any], Any]) -> bool:
        """
        Invoke the given `fun` for each element in `self.image`, then return
        `True`.
        >>> Iter([1, 3]).each(print)
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
        >>> Iter([0, 0]).empty()
        True
        >>> Iter([1, 10]).empty()
        False
        ```
        """
        return not bool(len(self.image))

    def fetch(self, index: int) -> bool:
        raise NotImplementedError()

    def filter(self, fun: Callable[[Any], bool]) -> Iter:
        """
        Filter `self.image`, i.e. return only those elements for which `fun` returns
        a truthy value.

        ```python
        >>> Iter([1, 3]).filter(lambda x: x % 2 == 0)
        [2]
        ```
        """
        self.image = list(filter(fun, self.image))
        return self

    def find(self, fun: Callable[[Any], bool], default: Optional[Any]=None) -> Optional[Any]:
        """
        Return the first element for which `fun` returns a truthy value. If no
        such element is found, return `default`.

        ```python
        >>> Iter([2, 4]).find(lambda x: x % 2 == 1)
        3
        >>> Iter([2, 4, 6]).find(lambda x: x % 2 == 1)
        None
        >>> Iter([2, 4, 6]).find(lambda x: x % 2 == 1, default=0)
        0
        ```
        """
        return next(filter(fun, self.image), default)

    def find_index(self, fun: Callable[[Any], bool], default: Optional[Any]=None) -> Optional[Any]:
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

    def find_value(self, fun: Callable[[Any], bool], default: Optional[Any]=None) -> Optional[Any]:
        """
        Similar to `self.find`, but return the value of the function invocation instead
        of the element itself.

        ```python
        >>> Iter([2, 4, 6]).find_value(lambda x: x % 2 == 1)
        None
        >>> Iter([2, 3, 4]).find_value(lambda x: x % 2 == 1)
        True
        >>> Iter([1, 3]).find_value(lambda x: isinstance(x, bool), "no bools!")
        'no bools!'
        ```
        """
        found = next(filter(fun, self.image), default)
        return fun(found) if found is not default else default

    def flat_map(self, fun: Callable[[Any], Any]) -> Iter:
        """
        Map the given `fun` over `self.image` and flattens the result.

        ```python
        >>> Iter([(1, 3), (4, 6)]).flat_map(lambda x: list(range(x[0], x[1] + 1)))
        [1, 2, 3, 4, 5, 6]
        >>> Iter([1, 2, 3]).flat_map(lambda x: [[x]])
        [[1], [2], [3]]
        ```
        """
        self.image = list(itertools.chain(*map(fun, self.image)))
        return self

    def flat_map_reduce(self, fun: Callable[[Any, Any], Any], acc: int=1) -> Iter:
        """
        Map and reduce an `self.image`, flattening the given results (only one
        level deep). It expects an accumulator and a function that receives each
        iterable element, and must return a...

        ```python
        >>> #example
        ```
        """
        raise NotImplementedError()

    def frequencies(self) -> Iter:
        """
        Return a map with keys as unique elements of `self.image` and values as
        the count of every element.

        ```python
        >>> Iter([1, 2, 2, 3, 4, 5, 5, 6]).frequencies()
        {1: 1, 2: 2, 3: 1, 4: 1, 5: 2, 6: 1}
        ```
        """
        self.image = Counter(self.image)
        return self

    def frequencies_by(self, key_fun: Callable[[Any], Any]) -> Iter:
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

    def group_by(self, key_fun: Callable[[Any], Any], value_fun: Optional[Callable[[Any], Any]]=None) -> Iter:
        """
        Split `self.image` into groups based on `key_fun`.

        The result is a map where each key is given by `key_fun` and each value
        is a list of elements given by `value_fun`. The order of elements within
        each list is preserved from `self.image`. However, like all maps, the
        resulting map is unordered.

        ```python
        >>> Iter(["ant", "buffalo", "cat", "dingo"]).group_by(len)
        {3: ["ant", "cat"], 5: ["dingo"], 7: ["buffalo"]}
        >>> Iter(["ant", "buffalo", "cat", "dingo"]).group_by(len, operator.itemgetter(0))
        {3: ["a", "c"], 5: ["d"], 7: ["b"]}
        ```
        """
        value = lambda g: list(g) if value_fun is None else list(map(value_fun, g))
        self.image = {k: value(g) for k, g in itertools.groupby(sorted(self.image, key=key_fun), key_fun)}
        return self

    def intersperse(self, separator: Any) -> Iter:
        """
        Intersperses separator between each element of `self.image`.

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

    def into(self, iter: Iterable) -> Iter:
        """
        Insert the given `self.image` into `iter`.

        ```python
        >>> Iter([1, 2]).into([])
        [1, 2]
        >>> Iter({'a': 1, 'b': 2}).into({})
        {'a': 1, 'b': 2}
        >>> Iter({'a': 1}).into({'b': 2})
        {'a': 1, 'b': 2}
        ```
        """
        self.image = {**self.image, **iter} if isinstance(iter, Dict) else [*self.image, *iter]
        return self

    def join(self, joiner: Optional[str]=None) -> str:
        """
        Join `self.image` into a string using `joiner` as a separator. If `joiner`
        is not passed at all, it defaults to an empty string. All elements in
        `self.image` must be convertible to a string, otherwise an error is raised.

        ```python
        >>> Iter([1,5]).join()
        '12345'
        >>> Iter[[1,5]].join(',')
        '1,2,3,4,5'
        ```
        """
        return f"{joiner or ''}".join(map(str, self.image))

    @overload
    def map(self, fun: Callable[[Any], Any]) -> Iter:
        """
        Return a list where each element is the result of invoking `fun` on each
        corresponding element of `self.image`. For dictionaries, the function expects
        a key-value pair as arguments.

        ```python
        >>> Iter([1,3]).map(lambda x: 2 * x)
        [2, 4, 6]
        >>> Iter({'a': 1, 'b': 2}).map(lambda k, v: {k: -v})
        {'a': -1, 'b': -2}
        ```
        """
        ...

    @overload
    def map(self, fun: Callable[[Any, Any], Dict]) -> Iter: ...

    def map(self, fun: Callable[[Any], Any]) -> Iter:
        self.image = dict(ChainMap(*itertools.starmap(fun, self.image.items()))) if isinstance(self.image, Dict) else list(map(fun, self.image))
        return self

    def map_every(self, nth: int, fun: Callable[[Any], Any]) -> Iter:
        """
        Return a list of results of invoking `fun` on every `nth` element of `self.image`,
        starting with the first element. The first element is always passed to the given
        function, unless `nth` is `0`.

        ```python
        >>> Iter([1, 10]).map_every(2, lambda x: x + 1000)
        [1001, 2, 1003, 4, 1005, 6, 1007, 8, 1009, 10]
        >>> Iter([1, 5]).map_every(0, lambda x: x + 1000)
        [1, 2, 3, 4, 5]
        >>> Iter([1, 3]).map_every(1, lambda x: x + 1000)
        [1001, 1002, 1003]
        ```
        """
        if nth != 0:
            for i in range(0, len(self.image), nth):
                self.image[i] = fun(self.image[i])
        return self

    def map_intersperse(self, separator: Any, fun: Callable[[Any], Any]) -> Iter:
        """
        Map and intersperses `self.image` in one pass.

        ```python
        >>> Iter([1, 3]).map_intersperse(None, lambda x: 2 * x)
        [2, None, 4, None, 6]
        ```
        """
        self.image =  list(itertools.islice(itertools.chain.from_iterable(zip(itertools.repeat(separator), map(fun, self.image))), 1, None))
        return self

    def map_join(self, fun: Callable[[Any], Any], joiner: Optional[str]=None) -> str:
        """
        Map and join `self.image` in one pass. If joiner is not passed at all, it
        defaults to an empty string. All elements returned from invoking `fun` must
        be convertible to a string, otherwise an error is raised.

        ```python
        >>> Iter([1, 3]).map_join(lambda x: 2 * x)
        '246'
        >>> Iter([1, 3]).map_join(lambda x: 2 * x, " = ")
        '2 = 4 = 6'
        ```
        """
        return f"{joiner or ''}".join(map(str, map(fun, self.image)))

    def map_reduce(self, acc: Union[int, float, complex], fun: Callable[[Any], Any], acc_fun: Optional[Callable[[Any, Any], Any]]) -> Iter:
        """
        Invoke the given function to each element in `self.image` to reduce it to
        a single element, while keeping an accumulator. Return a tuple where the
        first element is the mapped `self.image` and the second one is the final
        accumulator.

        ```python
        >>> Iter([1, 3]).map_reduce(0, lambda x: 2 * x, lambda x, acc: x + acc)
        ([2, 4, 6], 6)
        >>> Iter([1, 3]).map_reduce(6, lambda x: x * x, operator.sub)
        ([1, 4, 9], 0)
        ```
        """
        self.image = (list(map(fun, self.image)), functools.reduce(acc_fun, self.image, acc))
        return self

    def max(self, fun: Optional[Callable[[Any], Any]]=None, empty_fallback: Optional[Any]=None) -> Any:
        """
        Return the maximal element in `self.image` as calculated by the given `fun`.

        ```python
        >>> Iter([1, 3]).max()
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

    def member(self, element: Any) -> bool:
        """
        Checks if element exists within `self.image`.

        ```python
        >>> Iter([1, 10]).member(5)
        True
        >>> Iter([1, 10]).member(5.0)
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

    def min(self, fun: Optional[Callable[[Any], Any]]=None, empty_fallback: Optional[Any]=None) -> Any:
        """
        Return the minimum element in `self.image` as calculated by the given `fun`.

        ```python
        >>> Iter([1, 3]).max()
        1
        >>> Iter("you shall not pass".split()).max()
        'you'
        >>> Iter("you shall not pass".split()).max(len)
        'not'
        >>> Iter([]).max(empty_fallback='n/a')
        'n/a'
        ```
        """
        return (min(self.image, key=fun) if fun is not None else min(self.image)) if self.image else empty_fallback

    def min_max(self, fun: Optional[Callable[[Any], Any]]=None, empty_fallback: Optional[Any]=None) -> Tuple:
        """
        Return a tuple with the minimal and the maximal elements in `self.image`.

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

    def product(self) -> Union[float, int, complex]:
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

    def random(self) -> Any:
        """
        Return a random element from `self.image`.

        ```python
        >>> Iter([1, 100]).random()
        42
        >>> Iter([1, 100]).random()
        69
        ```
        """
        return random.choice(self.image)

    @overload
    @staticmethod
    def range(bounds: List[int, int]) -> List[int]:
        """
        Return a sequence of integers from start to end.

        ```python
        >>> Iter.range([1, 5])
        [1, 2, 3, 4, 5]
        >>> Iter.range((1, 5))
        [2, 3, 4]
        ```
        """
        ...

    @overload
    @staticmethod
    def range(bounds: Tuple[int, int]) -> List[int]: ...

    @staticmethod
    def range(bounds: List[int, int] | Tuple[int, int]) -> List[int]:
        return list(range(bounds[0], bounds[1]+1) if isinstance(bounds, List) else range(bounds[0]+1, bounds[1]))

    def reduce(self, fun: Callable[[Any, Any], Any], acc: int=0) -> Any:
        """
        Invoke `fun` for each element in `self.image` with the accumulator. The
        accumulator defaults to `0` if not otherwise specified. Reduce (sometimes
        also called fold) is a basic building block in functional programming.

        ```python
        >>> Iter([1, 4]).reduce(operator.add)
        10
        >>> Iter([1, 4]).reduce(lambda x, acc: x * acc, acc=1)
        24
        ```
        """
        return functools.reduce(fun, self.image, acc)

    def reduce_while(self, fun: Callable[[Any, Any], Tuple[bool, Any]], acc: int=0) -> Any:
        """
        Reduce `self.image` until `fun` returns `(False, acc)`.

        ```python
        >>> Iter([1, 100]).reduce_while(lambda x, acc: (True, acc + x) if x < 5 else (False, acc))
        10
        >>> Iter([1, 100]).reduce_while(lambda x, acc: (True, acc - x) if x % 2 == 0 else (False, acc), acc=2550)
        0
        ```
        """
        return functools.reduce(lambda acc, x: fun(x, acc)[1], filter(lambda x: fun(x, acc)[0], self.image), acc)

    def reject(self, fun: Callable[[Any], bool]) -> Iter:
        """
        Return a list of elements in `self.image` excluding those for which the
        function `fun` returns a truthy value.

        ```python
        >>> Iter([1, 3]).reject(lambda x: x % 2 == 0)
        [1, 3]
        ```
        """
        self.image = list(itertools.filterfalse(fun, self.image))
        return self

    @overload
    def reverse(self) -> Iter:
        """
        Return a list of elements in `self.image` in reverse order.

        ```python
        >>> Iter([1, 5]).reverse()
        [5, 4, 3, 2, 1]
        ```

        Reverse the elements in `self.image`, appends the `tail`, and returns it
        as a list.

        ```python
        >>> Iter([1, 3]).reverse([4, 5, 6])
        [3, 2, 1, 4, 5, 6]
        ```
        """
        ...

    @overload
    def reverse(self, tail: Optional[List]=None) -> Iter: ...

    def reverse(self, tail: Optional[List]=None) -> Iter:
        self.image = list(reversed(self.image))
        if tail: self.image.extend(tail)
        return self

    def reverse_slice(self, start_index: int, count: int) -> Iter:
        """
        Reverse `self.image` in the range from initial `start_index` through `count`
        elements. If `count` is greater than the size of the rest of `self.image`,
        then this function will reverse the rest of `self.image`.

        ```python
        >>> Iter([1, 6]).reverse_slice(2, 4)
        [1, 2, 6, 5, 4, 3]
        >>> Iter([1, 10]).reverse_slice(2, 4)
        [1, 2, 6, 5, 4, 3, 7, 8, 9, 10]
        >>> Iter([1, 10]).reverse_slice(2, 30)
        [1, 2, 10, 9, 8, 7, 6, 5, 4, 3]
        ```
        """
        self.image = [*self.image[:start_index], *reversed(self.image[start_index:count+start_index]), *self.image[count+start_index:]]
        return self

    def scan(self, fun: Callable[[Any, Any], Any], acc: Optional[int]=None) -> Iter:
        """
        Apply the given function to each element in `self.image`, storing the result
        in a list and passing it as the accumulator for the next computation. Uses
        the first element in `self.image` as the starting value if `acc` is `None`,
        else uses the given `acc` as the starting value.

        ```python
        >>> Iter([1, 5]).scan(operator.add)
        [1, 3, 6, 10, 15]
        >>> Iter([1, 5]).scan(lambda x, y: x + y, acc=0)
        [1, 3, 6, 10, 15]
        ```
        """
        acc = acc if acc is not None else 0
        self.image = list(map(lambda x: x + acc, itertools.accumulate(self.image, fun)))
        return self

    @staticmethod
    def shorten(sequence: List, width: int=20) -> str:
        """
        Shorten an iterable sequence into an short, human-readable string.

        ```python
        >>> Iter.shorten(range(1, 6))
        '[1, 2, 3, 4, 5]'
        >>> Iter.shorten(range(1, 101), width=50)
        '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,...]'
        ```
        """
        return textwrap.shorten(str(list(sequence)), width=width, placeholder=' ...]')

    def shuffle(self) -> Iter:
        """
        Return a list with the elements of `self.image` shuffled.

        ```python
        >>> Iter([1, 3]).shuffle()
        [3, 2, 1]
        >>> Iter([1, 3]).shuffle()
        >>> [2, 1, 3]
        ```
        """
        random.shuffle(self.image)
        return self

    @overload
    def slice(self, index: List[int]) -> Iter:
        """
        Return a subset list of `self.image` by `index`.

        Given an `Iter`, it drops elements before `index[0]` (zero-base),
        then it takes elements until element `index[1]` (inclusively). Indexes
        are normalized, meaning that negative indexes will be counted from the end.\

        If `index[1]` is out of bounds, then it is assigned as the index of
        the last element.

        ```python
        >>> Iter([1, 100]).slice([5, 10])
        [6, 7, 8, 9, 10, 11]
        >>> Iter([1, 10]).slice([5, 20])
        [6, 7, 8, 9, 10]
        >>> Iter([1, 30]).slice([-5, -1])
        [26, 27, 28, 29, 30]
        ```

        Alternatively, return a subset list of `self.image`, from `index` (zero-based)
        with `amount` number of elements if available. Given `self.image`, it drops
        elements right before element `index`; then, it takes `amount` of elements,
        returning as many elements as possible if there are not enough elements.

        A negative `index` can be passed, which means `self.image` is enumerated
        once and the index is counted from the end (for example, `-1` starts slicing
        from the last element). It returns `[]` if `amount` is `0` or if `index` is
        out of bounds.

        ```python
        >>> Iter([1, 10]).slice(5, 100)
        [6, 7, 8, 9, 10]
        ```
        """
        ...

    @overload
    def slice(self, index: int, amount: Optional[int]=None) -> Iter: ...

    def slice(self, index: int | List[int], amount: Optional[int]=None) -> Iter:
        if isinstance(index, List):
            self.image = self.image[index[0]:] if index[1] == -1 else self.image[index[0]:index[1]+1]
        else:
            self.image = self.image[index:amount] if abs(index) <= len(self.image) else []
        return self

    @overload
    def slide(self, index: int, insertion_index: int) -> Iter:
        """
        Slide a single or multiple elements given by `index` from `self.image` to
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
    def slide(self, index: List[int], insertion_index: int) -> Iter: ...

    def slide(self, index: int | List[int], insertion_index: int) -> Iter:
        if isinstance(index, List):
            if (max(index) + len(self.image) if max(index) < 0 else max(index)) > insertion_index:
                # slide backwards
                p1 = self.image[:insertion_index]
                p3 = self.image[index[0]:index[1]+1]
                p2 = self.image[insertion_index:index[0]]
                p4 = self.image[index[1]+1:]
                self.image = list(itertools.chain(p1, p3, p2, p4))
            else:
                # slide forwards
                p1 = self.image[:index[0]]
                p2 = self.image[index[0]:index[1]+1]
                p3 = self.image[index[1]+1:insertion_index+1]
                p4 = self.image[insertion_index+1:]
                self.image = list(itertools.chain(p1, p3, p2, p4))
        else:
            element, ii = self.image.pop(index), insertion_index
            self.image.insert((ii, ii+1)[ii<0], element) if ii!=-1 else self.image.append(element)
        return self

    def sort(self, fun: Optional[Callable[[Any], bool]]=None, descending: bool=False) -> Iter:
        """
        Return a new sorted `self.image`. `fun` specifies a function of one argument
        that is used to extract a comparison key from each element in iterable (for
        example, `key=str.lower`). The `descending` flag can be set to sort `self.image`
        in descending order (ascending by default).

        Use `functools.cmp_to_key()` to convert an old-style cmp function to a key
        function.

        ```python
        >>> Iter([3, 1, 2]).sort()
        [1, 2, 3]
        ```
        """
        self.image = sorted(self.image, key=fun, reverse=descending)
        return self

    def split(self, count: int) -> Iter:
        """
        Split `self.image` into two lists, leaving `count` elements in the first
        one. If `count` is a negative number, it starts counting from the back to
        the beginning of `self.image`.

        ```python
        >>> Iter([1, 3]).split(2)
        [[1,2], [3]]
        >>> Iter([1, 3]).split(10)
        [[1, 2, 3], []]
        >>> Iter([1, 3]).split(0)
        [[], [1, 2, 3]]
        >>> Iter([1, 3]).split(-1)
        [[1, 2], [3]]
        ```
        """
        self.image = [self.image[:count], self.image[count:]]
        return self

    def split_while(self, fun: Callable[[Any], bool]) -> Iter:
        """
        Split `self.image` in two at the position of the element for which `fun`
        returns a falsy value for the first time.

        It returns a nested list of length two. The element that triggered the split
        is part of the second list.

        ```python
        >>> Iter([1, 4]).split_while(lambda x: x < 3)
        [[1, 2], [3, 4]]
        >>> Iter([1, 4]).split_while(lambda x: x < 0)
        [[], [1, 2, 3, 4]]
        >>> Iter([1, 4]).split_while(lambda x: x > 0)
        [[1, 2, 3, 4], []]
        ```
        """
        default = len(self.image) + 1
        element = next(itertools.filterfalse(fun, self.image), default)
        count = self.image.index(element) if element in self.image else default
        self.image = [self.image[:count], self.image[count:]]
        return self

    @overload
    def split_with(self, fun: Callable[[Any], bool]) -> Iter:
        """
        Split `self.image` in two lists according to the given function `fun`.

        Split `self.image` in two lists by calling `fun` with each element in
        `self.image` as its only argument. Returns a nested list with the first
        list containing all the elements in `self.image` for which applying `fun`
        returned a truthy value, and a second list with all the elements for which
        applying fun returned a falsy value. The same logic is also applied when
        a key-value paired lambda expression is passed as an argument, as a consequence
        of which the dictionary will be also split into two parts following the
        same pattern.

        The elements in both the returned lists (or dictionaries) are in the same
        relative order as they were in the original `self.image` (if such iterable
        was ordered, like a list). See the examples below.

        ```python
        >>> Iter([1, 5]).reverse().split_with(lambda x: x % 2 == 0)
        [[4, 2, 0], [5, 3, 1]]
        >>> Iter({'a': 1, 'b': -2, 'c': 1, 'd': -3}).split_with(lambda k, v: v < 0)
        [{'b': -2, 'd': -3}, {'a': 1, 'c':1}]
        ```
        """
        ...

    @overload
    def split_with(self, fun: Callable[[Any, Any], bool]) -> Iter: ...

    def split_with(self, fun: Callable[[Any], bool] | Callable[[Any, Any], bool]) -> Iter:
        if isinstance(self.image, Dict):
            f1 = ChainMap(*[{k: v} for k, v in self.image.items() if fun(k, v)])
            f2 = ChainMap(*[{k: v} for k, v in self.image.items() if not fun(k, v)])
            self.image = [dict(f1), dict(f2)]
        else:
            t1, t2 = itertools.tee(self.image)
            self.image = [list(filter(fun, t1)), list(itertools.filterfalse(fun, t2))]
        return self

    def sum(self) -> Union[int, float, complex, str]:
        """
        Return the sum of all elements.

        ```python
        >>> Iter([1, 100]).sum()
        5050
        ```
        """
        return sum(self.image)

    def take(self, amount: int) -> Iter:
        """
        Takes an `amount` of elements from the beginning or the end of `self.image`.
        If a positive `amount` is given, it takes the amount elements from the
        beginning of `self.image`. If a negative `amount` is given, the amount of
        elements will be taken from the end. `self.image` will be enumerated once
        to retrieve the proper index and the remaining calculation is performed from
        the end. If `amount` is `0`, it returns `[]`.

        ```python
        >>> Iter([1, 3]).take(2)
        [1, 2]
        >>> Iter([1, 3]).take(10)
        [1, 2, 3]
        >>> Iter([1, 2, 3]).take(0)
        []
        >>> Iter([1, 2, 3]).take(-1)
        [3]
        ```
        """
        self.image = list(itertools.islice(self.image, amount) if amount > 0 else itertools.islice(reversed(self.image), abs(amount)))
        return self

    def take_every(self, nth: int) -> Iter:
        """
        Return a list of every `nth` element in `self.image`, starting with the
        first element. The first element is always included, unless `nth` is `0`.
        The second argument specifying every `nth` element must be a non-negative
        integer.

        ```python
        >>> Iter([1, 10]).take_every(2)
        [1, 3, 5, 7, 9]
        >>> Iter([1, 10]).take_every(0)
        []
        >>> Iter([1, 3]).take_every(1)
        [1, 2, 3]
        ```
        """
        self.image = list(itertools.islice(self.image, 0, len(self.image), nth)) if nth != 0 else []
        return self

    def take_random(self, count: int) -> Iter:
        """
        Take `count` random elements from `self.image`.

        ```python
        >>> Iter([1, 10]).take_random(2)
        [3, 1]
        >>> Iter([1, 10]).take_random(2)
        [6, 9]
        ```
        """
        self.image = random.choices(self.image, k=count)
        return self

    def take_while(self, fun: Callable[[Any], bool]) -> Iter:
        """
        Take the elements from the beginning of `self.image` while `fun` returns
        a truthy value.

        ```python
        >>> Iter([1, 3]).take_while(lambda x: x < 3)
        [1, 2]
        ```
        """
        self.image = list(itertools.takewhile(fun, self.image))
        return self

    def uniq(self) -> Iter:
        """
        Enumerates `self.image`, removing all duplicated elements.

        ```python
        >>> Iter([1, 2, 3, 3, 2, 1]).uniq()
        [1, 2, 3]
        ```
        """
        self.image = list(Counter(self.image).keys())
        return self

    def unzip(self) -> Iter:
        """
        Opposite of `self.zip`. Extracts two-element tuples from `self.image` and
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
    def with_index(self, fun_or_offset: Optional[int]=None) -> Iter:
        """
        Return `self.image` with each element wrapped in a tuple alongside its index.
        May receive a function or an integer offset. If an offset is given, it will
        index from the given offset instead of from zero. If a function is given,
        it will index by invoking the function for each element and index (zero-based)
        of the `self.image`.

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
    def with_index(self, fun_or_offset: Callable[[Any, Any], Any]) -> Iter: ...

    def with_index(self, fun_or_offset: Optional[int] | Callable[[Any, Any], Any]=None) -> Iter:
        if isinstance(fun_or_offset, int) or fun_or_offset is None:
            offset = 0 if fun_or_offset is None else fun_or_offset
            self.image = list(zip(self.image, range(offset, len(self.image)+offset)))
        else:
            self.image = list(itertools.starmap(fun_or_offset, zip(self.image, range(len(self.image)))))
        return self

    def zip(self, *iterables: Iterable) -> Iter:
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
        self.image = list(zip(self.image, *iterables))
        return self

    @overload
    def zip_reduce(self, acc: List, reducer: Callable[[Any, Any], Any]) -> Iter:
        """
        Reduce over all of `self.image`, halting as soon as any iterable is empty.
        The reducer will receive 2 args: a list of elements (one from each enum) and
        the accumulator.

        ```python
        >>> Iter([[1, 1], [2, 2], [3, 3]]).zip_reduce([], lambda x, acc: tuple(x) + (acc,))
        [(1, 2, 3), (1, 2, 3)]
        ```

        Reduce over two iterables halting as soon as either iterable is empty.

        ```python
        >>> Iter([]).zip_reduce([5, 6], lambda x, acc: tuple(x) + (acc,), [1, 2], {'a': 3, 'b': 4})
        [(1, {'a': 3}, 5), (2, {'b': 4}, 6)]
        ```
        """
        ...

    @overload
    def zip_reduce(self, acc: List, reducer: Callable[[Any, Any], Any], left: Iterable=None, right: Iterable=None) -> Iter: ...

    def zip_reduce(self, acc: List, reducer: Callable[[Any, Any], Any], left: Iterable=None, right: Iterable=None) -> Iter:
        if left is not None and right is not None:
            raise NotImplementedError()
        else:
            self.image = list(functools.reduce(reducer, zip(*self.image), acc))
        return self

    def zip_with(self, fun: Callable[..., Any], *iterable: Iterable) -> Iter:
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

    def __str__(self) -> str:
        return Iter.shorten(self.image, width=50)

    def __repr__(self) -> str:
        return f"Iter(domain={Iter.shorten(self.domain)},image={Iter.shorten(self.image)})"
