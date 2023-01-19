<h1 align="center">IterFun</h1>

<p align="center">
    <a href="https://github.com/StefanGreve/iterfun/actions?query=workflow%3ACI" title="Continuous Integration" target="_blank">
        <img src="https://github.com/StefanGreve/iterfun/actions/workflows/python-app.yml/badge.svg">
    </a>
    <a href="https://github.com/StefanGreve/iterfun" title="Release Version">
        <img src="https://img.shields.io/pypi/v/iterfun?color=blue&label=Release">
    </a>
    <a title="Supported Python Versions">
        <img src="https://img.shields.io/pypi/pyversions/iterfun">
    </a>
    <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" title="License Information" target="_blank" rel="noopener noreferrer">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg">
    </a>
    <a title="Downloads per Month">
        <img src="https://img.shields.io/pypi/dm/iterfun">
    </a>
</p>

Implements an eager iterator class reminiscent of Elixir's `Enum` structure that
features a series of handy methods for performing common data transformations.

---

## Examples

See also `tests/test_scenarios.py` for more elaborate code snippets.

```python
from iterfun import Iter
from iterfun import Functions as fun

primes = Iter.range(1, 10_000).filter(fun.is_prime)

# 1229
print(primes.count())

primes.save("primes.dat")
```

---

## Method Reference

This method reference serves as a first point of contact to help you discover
what this library is capable of. Documentation and small, self-contained examples
are provided in the doc strings of each method that you can read in the privacy of
your code editor of choice.

## Functions

- `invert`
- `is_even`
- `is_odd`
- `is_prime`
- `sign`

## Iter

- `all`
- `any`
- `at`
- `avg`
- `cartesian`
- `chunk_by`
- `chunk_every`
- `chunk_while`
- `combinations`
- `combinations_with_replacement`
- `count`
- `count_until`
- `dedup`
- `dedup_by`
- `difference`
- `drop`
- `drop_every`
- `drop_while`
- `duplicates`
- `filter`
- `find`
- `find_index`
- `find_value`
- `flat_map`
- `flat_map`
- `flat_map_reduce`
- `flatten`
- `frequencies`
- `group_by`
- `intersects`
- `intersperse`
- `into`
- `is_disjoint`
- `is_empty`
- `is_member`
- `is_subset`
- `is_superset`
- `join`
- `linspace`
- `map`
- `map_every`
- `map_intersperse`
- `map_join`
- `map_reduce`
- `max`
- `min`
- `min_max`
- `open`
- `permutations`
- `product`
- `randint`
- `random`
- `range`
- `reduce`
- `reduce_while`
- `reject`
- `reverse`
- `reverse_slice`
- `save`
- `scan`
- `shorten`
- `shuffle`
- `slice`
- `slide`
- `sort`
- `split`
- `split_while`
- `split_with`
- `sum`
- `symmetric_difference`
- `take`
- `take_every`
- `take_random`
- `take_while`
- `to_dict`
- `to_list`
- `transpose`
- `union`
- `unique`
- `unzip`
- `with_index`
- `zip_reduce`
- `zip_with`
