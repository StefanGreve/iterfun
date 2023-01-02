# Changelog

## Version 0.0.5 (31 Jan 2023)

> Note that this update introduces breaking changes.

Implement a `Functions` helper class for common procedures such as

- `invert`
- `is_even`
- `is_odd`
- `sign`

The overload in the `Iter` constructor was removed in favor of a static `Iter.range`
method to enforce separation of concerns more strictly. Additional minor changes
were made to pretty much all doc strings to reflect the recent changes that are
to be consolidated for more information. In brief,

- the `chunk_by` method now also provides `eject` as an optional argument
- the `concat` method was renamed to `union`
- `iterable` and `iter` keyword arguments were renamed to `iter_`
- the method signature of the `range` method has changed and added support for
  decrements

The following methods are new:

- `duplicates`
- `flatten`
- `linspace`
- `transpose`

## Version 0.0.4 (17 May 2022)

Refactors code and improves the doc strings here and there. The `Iter.__ctor` method
was removed in favor of `Iter.range` for implementing the `Iter.__init__` overload.

Additionally, the following methods have been removed as well:

-   `self.each`
-   `self.fetch`

Turns out they are not that useful in Python after all.

## Version 0.0.3 (25 Dec 2021)

See below for a break down of the development status of all methods provided by
the `Iter` class. Some methods also provide overloads via `typing`. Support for
working with dictionaries is rather scarce. Like `Enum` in Elixir, this is an eager
implementation meaning that generators are always converted into lists, thus consumed
all at once. Perhaps there will be a `Stream`-like structure in the future that's
compatible with `Iter`, though it remains to be seen whether such a thing will be
implemented in the future.

-   [x] `self.__init__`
-   [x] `self.all`
-   [x] `self.any`
-   [x] `self.at`
-   [x] `self.avg`
-   [x] `self.chunk_by`
-   [x] `self.chunk_every`
-   [ ] `self.chunk_while`
-   [x] `self.concat`
-   [x] `self.count`
-   [x] `self.count_until`
-   [x] `self.dedup`
-   [x] `self.dedup_by`
-   [x] `self.drop`
-   [x] `self.drop_every`
-   [x] `self.drop_while`
-   [x] `self.each`
-   [x] `self.empty`
-   [x] `self.fetch`
-   [x] `self.filter`
-   [x] `self.find`
-   [x] `self.find_index`
-   [x] `self.find_value`
-   [x] `self.flat_map`
-   [ ] `self.flat_map_reduce`
-   [x] `self.frequencies`
-   [x] `self.frequencies_by`
-   [x] `self.group_by`
-   [x] `self.intersperse`
-   [x] `self.into`
-   [x] `self.join`
-   [x] `self.map`
-   [x] `self.map_every`
-   [x] `self.map_intersperse`
-   [x] `self.map_join`
-   [x] `self.map_reduce`
-   [x] `self.max`
-   [x] `self.member`
-   [x] `self.min`
-   [x] `self.min_max`
-   [x] `self.product`
-   [x] `self.random`
-   [x] `Iter.range`
-   [x] `self.reduce`
-   [x] `self.reduce_while`
-   [x] `self.reject`
-   [x] `self.reverse`
-   [x] `self.reverse_slice`
-   [x] `self.scan`
-   [x] `Iter.shorten`
-   [x] `self.shuffle`
-   [x] `self.slice`
-   [x] `self.slide`
-   [x] `self.sort`
-   [x] `self.split`
-   [x] `self.split_while`
-   [x] `self.split_with`
-   [x] `self.sum`
-   [x] `self.take`
-   [x] `self.take_every`
-   [x] `self.take_random`
-   [x] `self.take_while`
-   [x] `self.uniq`
-   [x] `self.unzip`
-   [x] `self.with_index`
-   [x] `self.zip`
-   [ ] `self.zip_reduce`
-   [ ] `self.zip_with`
-   [x] `self.__repr__`
-   [x] `self.__str__`

The static non-standard functions `Iter.range` and `Iter.shorten` have been added
for convenience purposes only. The method signature `uniq_by` does not appear in
this list yet; it may be added in future versions of this library.

## Version 0.0.2 (16 Dec 2021)

Finalize package structure for development and setup release pipeline.

## Version 0.0.1 (16 Dec 2021)

Register package name of PyPI.
