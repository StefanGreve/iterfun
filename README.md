<p align="center">
  <a title="Project Logo">
    <img height="150" style="margin-top:15px" src="https://github.com/StefanGreve/iterfun/blob/master/iterfun.svg">
  </a>
</p>

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

### Two Sum Problem

Given an array of integers `domain` and an integer `target`, return indices of the
two numbers such that they add up to target. You may assume that each input would
have exactly one solution, and you may not use the same element twice. You can
return the answer in any order.

```python
from iterfun import Iter

target = 12
domain = [45, 26, 5, 41, 58, 97, 82, 9, 79, 22, 3, 74, 70, 84, 17, 79, 41, 96, 13, 89]

pair = Iter(domain) \
    .filter(lambda x: x < target) \
    .combinations(2) \
    .filter(lambda x: sum(x) == target) \
    .flatten() \
    .to_list()

# [7, 10]
print(Iter(domain).find_index(lambda x: x in pair).image)
```

---

## Technical Limitations

For reasons of simplicity, the mutable state in `image` is exposed as a list or
dictionary and not as a generator which is capable of dealing with very large
sequences. It's an implementation detail that is necessary for some index-based methods,
though this behavior might change in future versions of this library where applicable.

There is probably room to improve the overall performance and accuracy of this library.
To this end, future updates will also increase the test coverage in order to consider
more edge cases and method interoperability. Notice that the terms and conditions
of the MIT License will always apply.

## Method Reference

This method reference serves as a first point of contact to help you discover
what this library is capable of. Documentation and small, self-contained examples
are provided in the doc strings of each method that you can read in the privacy of
your code editor of choice.

### Functions

- `invert`
- `is_even`
- `is_odd`
- `is_prime`
- `miller_rabin`
- `sign`

### Iter

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

---

## Authors

| Name             | Mail Address            | GitHub Profile                                |
|------------------|-------------------------|-----------------------------------------------|
| Stefan Greve     | greve.stefan@outlook.jp | [StefanGreve](https://github.com/StefanGreve) |

See also the list of [contributors](https://github.com/stefangreve/iterfun/contributors)
who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for more details.
