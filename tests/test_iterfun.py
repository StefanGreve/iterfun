import operator
import unittest

import pytest

from src.iterfun import Iter


class TestIter(unittest.TestCase):
    def test_all(self):
        self.assertTrue(Iter([1, 2, 3]).all())
        self.assertFalse(Iter([1, None, 3]).all())
        self.assertTrue(Iter([]).all())
        self.assertTrue(Iter([2, 4, 6]).all(lambda x: x % 2 == 0))
        self.assertFalse(Iter([1, 2, 3]).all(lambda x: x % 2 == 0))
        self.assertTrue(Iter([]).all(lambda: None))

    def test_any(self):
        self.assertFalse(Iter([False, False, False]).any())
        self.assertTrue(Iter([False, True, False]).any())
        self.assertFalse(Iter([]).any())
        self.assertFalse(Iter([2, 4, 6]).any(lambda x: x % 2 == 1))
        self.assertTrue(Iter([1, 2, 3]).any(lambda x: x % 2 == 1))
        self.assertFalse(Iter([]).any(lambda: None))

    def test_at(self):
        self.assertEqual(2, Iter([2, 4, 6]).at(0))
        self.assertEqual(6, Iter([2, 4, 6]).at(2))
        self.assertEqual(6, Iter([2, 4, 6]).at(-1))

    def test_at_throws(self):
        with pytest.raises(IndexError):
            self.assertEqual(None, Iter([2, 4, 6]).at(4))

    def test_avg(self):
        self.assertEqual(5, Iter([0, 10]).avg())

    def test_chunk_by(self):
        self.assertEqual([[1], [2, 2], [3], [4, 4, 6], [7, 7]], Iter([1, 2, 2, 3, 4, 4, 6, 7, 7]).chunk_by(lambda x: x % 2 == 1).image)
        self.assertEqual([['a', 'b'], ['c', 'd'], ['e', 'f']], Iter(['a', 'b', '1', 'c', 'd', '2', 'e', 'f']).chunk_by(lambda x: x.isdigit(), eject=True).image)

    def test_chunk_every(self):
        self.assertEqual([[1, 2], [3, 4], [5, 6]], Iter.range(1, 6).chunk_every(2).image)
        self.assertEqual([[1, 2, 3], [3, 4, 5], [5, 6]], Iter.range(1, 6).chunk_every(3, 2).image)
        self.assertEqual([[1, 2, 3], [3, 4, 5], [5, 6, 7]], Iter.range(1, 6).chunk_every(3, 2, [7]).image)
        self.assertEqual([[1, 2, 3], [4]], Iter.range(1, 4).chunk_every(3, 3, []).image)
        self.assertEqual([[1, 2, 3, 4]], Iter.range(1, 4).chunk_every(10).image)
        self.assertEqual([[1, 2], [4, 5]], Iter.range(1, 5).chunk_every(2, 3, []).image)

    @pytest.mark.xfail(raises=NotImplementedError, reason="TODO")
    def test_chunk_while(self):
        self.assertEqual([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]], Iter([1, 10]).chunk_while([], None, None))

    def test_count(self):
        self.assertEqual(3, Iter([1, 2, 3]).count())
        self.assertEqual(2, Iter.range(1, 5).count(lambda x: x % 2 == 0))

    def test_count_until(self):
        self.assertEqual(5, Iter.range(1, 20).count_until(5))
        self.assertEqual(20, Iter.range(1, 20).count_until(50))
        self.assertTrue(Iter.range(1, 10).count_until(10) == 10)
        self.assertTrue(Iter.range(1, 12).count_until(10 + 1) > 10)
        self.assertTrue(Iter.range(1, 5).count_until(10) < 10)
        self.assertTrue(Iter.range(1, 10).count_until(10 + 1) == 10)
        self.assertEqual(7, Iter.range(1, 20).count_until(7, lambda x: x % 2 == 0))
        self.assertTrue(10, Iter.range(1, 20).count_until(11, lambda x: x % 2 == 0))

    def test_dedup(self):
        self.assertEqual([1, 2, 3, 2, 1], Iter([1, 2, 3, 3, 2, 1]).dedup().image)

    def test_dedup_by(self):
        self.assertEqual([5, 1, 3, 2], Iter([5, 1, 2, 3, 2, 1]).dedup_by(lambda x: x > 2).image)
        self.assertEqual([0, 3, 2], Iter([0, 1, 2, 3, 2, 1]).dedup_by(lambda x: x > 2).image)
        self.assertEqual([0, 4, 1, 2, 0, 3], Iter([0, 4, 9, 1, 2, 0, 3, 4, 9]).dedup_by(lambda x: x < 2).image)
        self.assertEqual([3, 2, 4, 1], Iter([3, 6, 7, 7, 2, 0, 1, 4, 1]).dedup_by(lambda x: x > 2).image)
        self.assertEqual([3, 2, 0], Iter([3, 6, 7, 7, 2, 0, 1, 4, 1]).dedup_by(lambda x: x == 2).image)

    def test_difference(self):
        self.assertEqual([1, 5, 6, 7, 8, 9], Iter.range(1, 10).difference([4, 3, 2, 10]).image)
        self.assertEqual(['a', 'b', 'c'], Iter(list("abc")).difference(range(1, 11)).image)

    def test_drop(self):
        self.assertEqual([3], Iter.range(1, 3).drop(2).image)
        self.assertEqual([], Iter.range(1, 3).drop(10).image)
        self.assertEqual([1, 2, 3], Iter.range(1, 3).drop(0).image)
        self.assertEqual([1, 2], Iter.range(1, 3).drop(-1).image)

    def test_drop_every(self):
        self.assertEqual([2, 4, 6, 8, 10], Iter.range(1, 10).drop_every(2).image)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], Iter.range(1, 10).drop_every(0).image)
        self.assertEqual([], Iter.range(1, 3).drop_every(1).image)

    def test_drop_while(self):
        self.assertEqual([3, 2, 1], Iter([1, 2, 3, 2, 1]).drop_while(lambda x: x < 3).image)

    def test_duplicates(self):
        self.assertEqual([1, 2, 4], Iter([1, 1, 1, 2, 2, 3, 4, 4]).duplicates().image)

    def test_empty(self):
        self.assertTrue(Iter([]).empty())
        self.assertFalse(Iter([0]).empty())
        self.assertFalse(Iter.range(1, 10).empty())

    def test_filter(self):
        self.assertEqual([2], Iter.range(1, 3).filter(lambda x: x % 2 == 0).image)

    def test_find(self):
        self.assertEqual(3, Iter.range(2, 4).find(lambda x: x % 2 == 1))
        self.assertEqual(None, Iter([2, 4, 6]).find(lambda x: x % 2 == 1))
        self.assertEqual(0, Iter([2, 4, 6]).find(lambda x: x % 2 == 1, default=0))

    def test_find_index(self):
        self.assertEqual(None, Iter([2, 4, 6]).find_index(lambda x: x % 2 == 1))
        self.assertEqual(1, Iter([2, 3, 4]).find_index(lambda x: x % 2 == 1))

    def test_find_value(self):
        self.assertEqual(None, Iter([2, 4, 6]).find_value(lambda x: x % 2 == 1))
        self.assertTrue(Iter([2, 3, 4]).find_value(lambda x: x % 2 == 1))
        self.assertTrue(Iter([2, 3, 4]).find_value(lambda x: x % 2 == 1))
        self.assertEqual("no bools!", Iter.range(1, 3).find_value(lambda x: isinstance(x, bool), default="no bools!"))

    def test_flat_map(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], Iter([(1, 3), (4, 6)]).flat_map(lambda x: list(range(x[0], x[1]+1))).image)
        self.assertEqual([[1], [2], [3]], Iter([1, 2, 3]).flat_map(lambda x: [[x]]).image)

    @pytest.mark.xfail(raises=NotImplementedError, reason="TODO")
    def test_flat_map_reduce(self):
        pass

    def test_flatten(self):
        self.assertEqual([1, 2, 3, 4, 5, 6, None], Iter([[1, 2], [3, 4], [5], [6, None]]).flatten().image)

    def test_frequencies(self):
        self.assertEqual({1: 1, 2: 2, 3: 1, 4: 1, 5: 2, 6: 1}, Iter([1, 2, 2, 3, 4, 5, 5, 6]).frequencies().image)

    def test_frequencies_by(self):
        self.assertEqual({"aa": 2, "bb": 1, "cc": 1}, Iter(["aa", "aA", "bb", "cc"]).frequencies_by(str.lower).image)
        self.assertEqual({3: 2, 2: 2, 1: 1}, Iter(["aaa", "aA", "bbb", "cc", "c"]).frequencies_by(len).image)

    def test_group_by(self):
        self.assertEqual({3: ["ant", "cat"], 5: ["dingo"], 7: ["buffalo"]},  Iter(["ant", "buffalo", "cat", "dingo"]).group_by(len).image)
        self.assertEqual({3: ["a", "c"], 5: ["d"], 7: ["b"]},  Iter(["ant", "buffalo", "cat", "dingo"]).group_by(len, operator.itemgetter(0)).image)

    def test_intersects(self):
        self.assertEqual([1, 2], Iter([1, 2, 3, 4]).intersects([5, 6, 1, 2]).image)
        self.assertEqual([1, 2], Iter([1, 2, 3, 4]).intersects([5, 6, 2, 1]).image)
        self.assertTrue(Iter.range(1, 10).intersects(range(1, 11)).count() > 0)
        self.assertFalse(Iter.range(1, 10).intersects(list("abc")).count() > 0)

    def test_intersperse(self):
        self.assertEqual([1, 0, 2, 0, 3], Iter.range(1,3).intersperse(0).image)
        self.assertEqual([1], Iter([1]).intersperse(0).image)
        self.assertEqual([], Iter([]).intersperse(0).image)

    def test_into(self):
        self.assertEqual([1, 2], Iter([1, 2]).into([]).image)
        self.assertEqual({'a': 1, 'b': 2}, Iter({'a': 1, 'b': 2}).into({}).image)
        self.assertEqual({'a': 1, 'b': 2}, Iter({'a': 1}).into({'b': 2}).image)

    def test_is_disjoint(self):
        self.assertTrue(Iter.range(1, 10).is_disjoint([11, 12, 13]))
        self.assertFalse(Iter([1, 2, 3]).is_disjoint([1, 2, 3]))

    def test_is_subset(self):
        self.assertTrue(Iter.range(1, 10).is_subset([1, 2]))
        self.assertTrue(Iter([1, 2, 3]).is_subset([1, 2, 3]))
        self.assertFalse(Iter([1, 2, 3]).is_subset([1, 2, 3], proper=True))

    def test_is_superset(self):
        self.assertTrue(Iter([1, 2]).is_superset(range(1, 11)))
        self.assertTrue(Iter([1, 2, 3]).is_superset([1, 2, 3]))
        self.assertFalse(Iter([1, 2, 3]).is_superset([1, 2, 3], proper=True))

    def test_join(self):
        self.assertEqual('12345', Iter.range(1, 5).join())
        self.assertEqual('1,2,3,4,5', Iter.range(1, 5).join(','))

    def test_linspace(self):
        self.assertEqual([1.1, 1.32, 1.54, 1.76, 1.98, 2.2, 2.42, 2.64, 2.86, 3.08, 3.3], Iter.linspace(1.1, 3.3, step=10, prec=2).image)

    def test_map(self):
        self.assertEqual([2, 4, 6], Iter.range(1, 3).map(lambda x: 2 * x).image)
        self.assertEqual({'a': -1, 'b': -2}, Iter({'a': 1, 'b': 2}).map(lambda k, v: {k: -v}).image)
        self.assertEqual({'a': 2, 'b': 4}, Iter({'a': 1, 'b': 2}).map(lambda k, v: {k: 2 * v}).image)

    def test_map_every(self):
        self.assertEqual([1001, 2, 1003, 4, 1005, 6, 1007, 8, 1009, 10], Iter.range(1, 10).map_every(2, lambda x: x+1000).image)
        self.assertEqual([1001, 2, 3, 1004, 5, 6, 1007, 8, 9, 1010], Iter.range(1, 10).map_every(3, lambda x: x + 1000).image)
        self.assertEqual([1, 2, 3, 4, 5], Iter.range(1, 5).map_every(0, lambda x: x + 1000).image)
        self.assertEqual([1001, 1002, 1003], Iter.range(1, 3).map_every(1, lambda x: x + 1000).image)

    def test_map_intersperse(self):
        self.assertEqual([2, None, 4, None, 6], Iter.range(1, 3).map_intersperse(None, lambda x: 2 * x).image)

    def test_map_join(self):
        self.assertEqual('246', Iter.range(1, 3).map_join(lambda x: 2 * x))
        self.assertEqual('2 = 4 = 6', Iter.range(1, 3).map_join(lambda x: 2 * x, " = "))

    def test_map_reduce(self):
        self.assertEqual(([2, 4, 6], 6), Iter.range(1, 3).map_reduce(0, lambda x: 2 * x, operator.add).image)
        self.assertEqual(([1, 4, 9], 0), Iter.range(1, 3).map_reduce(6, lambda x: x * x, operator.sub).image)

    def test_max(self):
        self.assertEqual(3, Iter.range(1, 3).max())
        self.assertEqual('you', Iter("you shall not pass".split()).max())
        self.assertEqual('shall', Iter("you shall not pass".split()).max(len))
        self.assertEqual('n/a', Iter([]).max(empty_fallback='n/a'))

    def test_member(self):
        self.assertTrue(Iter.range(1, 10).is_member(5))
        self.assertTrue(Iter.range(1, 10).is_member(5.0))
        self.assertTrue(Iter([1.0, 2.0, 3.0]).is_member(2))
        self.assertTrue(Iter([1.0, 2.0, 3.0]).is_member(2.000))
        self.assertFalse(Iter(['a', 'b', 'c']).is_member('d'))

    def test_min(self):
        self.assertEqual(1, Iter([1, 3]).min())
        self.assertEqual('not', Iter("you shall not pass".split()).min())
        self.assertEqual('you', Iter("you shall not pass".split()).min(len))
        self.assertEqual('n/a', Iter([]).min(empty_fallback='n/a'))

    def test_min_max(self):
        self.assertEqual((1, 3), Iter.range(1, 3).min_max())
        self.assertEqual((None, None), Iter([]).min_max(empty_fallback=None))
        self.assertEqual(('a', 'aaa'), Iter(["aaa", "a", "bb", "c", "ccc"]).min_max(len))

    def test_product(self):
        self.assertEqual(24, Iter([2, 3, 4]).product())
        self.assertEqual(24.0, Iter([2.0, 3.0, 4.0]).product())

    def test_randint(self):
        a, b, size = 1, 100, 1000
        random_numbers = Iter.randint(a, b, size).to_list()
        self.assertEqual(size, len(random_numbers))
        self.assertTrue(min(random_numbers) >= a)
        self.assertTrue(max(random_numbers) <= b)

    def test_randint_secure(self):
        a, b, size = 1, 100, 1000
        random_numbers = Iter.randint(a, b, size, secure=True).to_list()
        self.assertEqual(size, len(random_numbers))
        self.assertTrue(min(random_numbers) >= a)
        self.assertTrue(max(random_numbers) <= b)

    def test_random(self):
        numbers = Iter.range(1, 100).image
        self.assertIn(Iter(numbers).random(), numbers)

    def test_range_increments(self):
        self.assertEqual([1, 2, 3, 4, 5], Iter.range(1, 5).image)
        self.assertEqual([1, 3, 5, 7, 9], Iter.range(1, 10, 2).image)
        self.assertEqual([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], Iter.range(0.1, 1.0).image)
        self.assertEqual([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0], Iter.range(0.2, 2.0, 0.1).image)
        self.assertEqual([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0], Iter.range(0.5, 5.0, step=0.5).image)

    def test_range_decrements(self):
        self.assertEqual([5, 4, 3, 2, 1, 0], Iter.range(5, 0, -1).image)
        self.assertEqual([0.2, 0.4, 0.6, 0.8, 1.0], Iter.range(0.2, 1.0, 0.2).image)
        self.assertEqual([5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5], Iter.range(5.0, 0.5, -0.5).image)
        self.assertEqual([], Iter.range(0.5, 5.0, -0.5).image)
        self.assertEqual([], Iter.range(0, 5, -1).image)
        with pytest.raises(ValueError):
            self.assertEqual([], Iter.range(5, 0, 0).image)

    def test_reduce(self):
        self.assertEqual(10,  Iter.range(1, 4).reduce(operator.add))
        self.assertEqual(24,  Iter.range(1, 4).reduce(lambda x, acc: x * acc, acc=1))

    def test_reduce_while(self):
        self.assertEqual(10, Iter.range(1, 100).reduce_while(lambda x, acc: (True, x + acc) if x < 5 else (False, acc)))
        self.assertEqual(5050, Iter.range(1, 100).reduce_while(lambda x, acc: (True, acc + x) if x > 0 else (False, acc)))
        self.assertEqual(0, Iter.range(1, 100).reduce_while(lambda x, acc: (True, acc - x) if x % 2 == 0 else (False, acc), acc=2550))

    def test_reject(self):
        self.assertEqual([1, 3], Iter.range(1, 3).reject(lambda x: x % 2 == 0).image)

    def test_reverse(self):
        self.assertEqual([5, 4, 3, 2, 1], Iter.range(1, 5).reverse().image)
        self.assertEqual([3, 2, 1, 4, 5, 6], Iter.range(1, 3).reverse([4, 5, 6]).image)

    def test_reverse_slice(self):
        self.assertEqual([1, 2, 6, 5, 4, 3], Iter.range(1, 6).reverse_slice(2, 4).image)
        self.assertEqual([1, 2, 6, 5, 4, 3, 7, 8, 9, 10], Iter.range(1, 10).reverse_slice(2, 4).image)
        self.assertEqual([1, 2, 10, 9, 8, 7, 6, 5, 4, 3], Iter.range(1, 10).reverse_slice(2, 30).image)

    def test_scan(self):
        self.assertEqual([1, 3, 6, 10, 15], Iter.range(1, 5).scan(operator.add).image)
        self.assertEqual([1, 3, 6, 10, 15], Iter.range(1, 5).scan(lambda x, y: x + y, acc=0).image)
        self.assertEqual([2, 4, 7, 11, 16], Iter.range(1, 5).scan(operator.add, acc=1).image)

    def test_shorten(self):
        self.assertEqual("[1, 2, 3, 4, 5]", Iter.range(1, 5).shorten())
        self.assertEqual("[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, ...]", Iter.range(1, 100).shorten(width=50))

    def test_shuffle(self):
        iter = Iter.range(1, 10).shuffle()
        self.assertTrue(iter.all(lambda x: x in Iter.range(1, 10).image))

    def test_slice(self):
        self.assertEqual([6, 7, 8, 9, 10, 11], Iter.range(1, 100).slice([5, 10]).image)
        self.assertEqual([6, 7, 8, 9, 10], Iter.range(1, 10).slice([5, 20]).image)
        self.assertEqual([26, 27, 28, 29, 30], Iter.range(1, 30).slice([-5, -1]).image)
        self.assertEqual([7, 8, 9], Iter.range(1, 10).slice([-4, -2]).image)
        self.assertEqual([7, 8, 9, 10], Iter.range(1, 10).slice([-4, 100]).image)
        self.assertEqual([6, 7, 8, 9, 10], Iter.range(1, 10).slice(5, 100).image)
        self.assertEqual([], Iter.range(1, 10).slice(10, 5).image)
        self.assertEqual([], Iter.range(1, 10).slice(-11, 5).image)

    def test_slide(self):
        self.assertEqual(['a', 'f', 'b', 'c', 'd', 'e', 'g'], Iter(list("abcdefg")).slide(5, 1).image, msg="Sliding a single element")
        self.assertEqual(['a', 'd', 'e', 'f', 'b', 'c', 'g'], Iter(list("abcdefg")).slide([3, 5], 1).image, msg="Slide a range of elements backward")
        self.assertEqual(['a', 'e', 'f', 'b', 'c', 'd', 'g'], Iter(list("abcdefg")).slide([1, 3], 5).image, msg="Slide a range of elements forward")
        self.assertEqual(['a', 'd', 'e', 'f', 'b', 'c', 'g'], Iter(list("abcdefg")).slide([-4, -2], 1).image, msg="Slide with negative indices (counting from the end)")
        self.assertEqual(['a', 'b', 'c', 'e', 'f', 'g', 'd'], Iter(list("abcdefg")).slide(3, -1).image, msg="Slide with negative indices (counting from the end)")
        self.assertEqual(['a', 'b', 'c', 'e', 'f', 'd', 'g'], Iter(list("abcdefg")).slide(3, -2).image, msg="Slide with negative indices (counting from the end)")

    def test_sorted(self):
        self.assertEqual([1, 2, 3], Iter([3, 1, 2]).sort().image)
        self.assertEqual([3, 2, 1], Iter([3, 1, 2]).sort(descending=True).image)

    def test_split(self):
        self.assertEqual([[1, 2], [3]], Iter.range(1, 3).split(2).image)
        self.assertEqual([[1, 2, 3], []], Iter.range(1, 3).split(10).image)
        self.assertEqual([[], [1, 2, 3]], Iter.range(1, 3).split(0).image)
        self.assertEqual([[1, 2], [3]], Iter.range(1, 3).split(-1).image)
        self.assertEqual([[1], [2, 3]], Iter.range(1, 3).split(-2).image)
        self.assertEqual([[], [1, 2, 3]], Iter.range(1, 3).split(-5).image)

    def test_split_while(self):
        self.assertEqual([[1, 2], [3, 4]], Iter.range(1, 4).split_while(lambda x: x < 3).image)
        self.assertEqual([[], [1, 2, 3, 4]], Iter.range(1, 4).split_while(lambda x: x < 0).image)
        self.assertEqual([[1, 2, 3, 4], []], Iter.range(1, 4).split_while(lambda x: x > 0).image)

    def test_split_with(self):
        self.assertEqual([[4, 2, 0], [5, 3, 1]], Iter.range(0, 5).reverse().split_with(lambda x: x % 2 == 0).image)
        self.assertEqual([{'b': -2, 'd': -3}, {'a': 1, 'c':1}], Iter({'a': 1, 'b': -2, 'c': 1, 'd': -3}).split_with(lambda k, v: v < 0).image)
        self.assertEqual([{}, {'a': 1, 'b': -2, 'c': 1, 'd': -3}], Iter({'a': 1, 'b': -2, 'c': 1, 'd': -3}).split_with(lambda k, v: v > 50).image)
        self.assertEqual([{}, {}], Iter({}).split_with(lambda k, v: v > 50).image)

    def test_sum(self):
        self.assertEqual(5050, Iter.range(1, 100).sum())

    def test_symmetric_difference(self):
        self.assertEqual([1, 2, 3, 4, 11, 12, 13, 14, 15], Iter.range(1, 10).symmetric_difference(range(5, 16)).image)

    def test_take(self):
        self.assertEqual([1, 2], Iter.range(1, 3).take(2).image)
        self.assertEqual([1, 2, 3], Iter.range(1, 3).take(10).image)
        self.assertEqual([], Iter.range(1, 3).take(0).image)
        self.assertEqual([3], Iter.range(1, 3).take(-1).image)

    def test_take_every(self):
        self.assertEqual([1, 3, 5, 7, 9], Iter.range(1, 10).take_every(2).image)
        self.assertEqual([], Iter.range(1, 10).take_every(0).image)
        self.assertEqual([1, 2, 3], Iter.range(1, 3).take_every(1).image)

    def test_take_random(self):
        numbers = Iter.range(1, 100)
        self.assertTrue(set(numbers.take_random(2).image).issubset(set(numbers.image)))

    def test_take_while(self):
        self.assertEqual([1, 2], Iter.range(1, 3).take_while(lambda x: x < 3).image)

    def test_transpose(self):
        self.assertEqual([('a', 'd', 'g'), ('b', 'e', 'h'), ('c', 'f', 'i')], Iter([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]).transpose().image)
        self.assertEqual([('a', 'd', 'g'), ('b', 'e', 'h'), ('c', False, False)], Iter([['a', 'b', 'c'], ['d', 'e'], ['g', 'h']]).transpose(fillvalue=False).image)

    def test_union(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], Iter([1, 2, 3, 4]).union([5, 6]).image)
        self.assertEqual([1, 2, 3, 4, 5, 6], Iter([[1, 2], [3]]).flatten().union([4, 5, 6]).image)

    def test_uniq(self):
        self.assertEqual([1, 2, 3], Iter([1, 2, 3, 3, 2, 1]).unique().image)

    def test_unzip(self):
        self.assertEqual([['a', 'b', 'c'], [1, 2, 3]], Iter({'a': 1, 'b': 2, 'c': 3}).unzip().image)
        self.assertEqual([['a', 'b', 'c'], [1, 2, 3]], Iter([('a', 1), ('b', 2), ('c', 3)]).unzip().image)
        self.assertEqual([['a', 'b', 'c'], [1, 2, 3]], Iter([['a', 1], ['b', 2], ['c', 3]]).unzip().image)

    def test_with_index(self):
        self.assertEqual([('a', 0), ('b', 1), ('c', 2)], Iter(list("abc")).with_index().image)
        self.assertEqual([('a', 2), ('b', 3), ('c', 4)], Iter(list("abc")).with_index(2).image)
        self.assertEqual([(0, 'a'), (1, 'b'), (2, 'c')], Iter(list("abc")).with_index(lambda k, v: (v, k)).image)

    def test_zip(self):
        self.assertEqual([(1, 'a', "foo"), (2, 'b', "bar"), (3, 'c', "baz")], Iter.range(1, 3).zip(list("abc"), ["foo", "bar", "baz"]).image)
        self.assertEqual([('a', 0), ('b', 1), ('c', 2)], Iter(list("abc")).zip(range(3)).image)
        self.assertEqual([('a', 0, 'd'), ('b', 1, 'e'), ('c', 2, 'f')], Iter(list("abc")).zip(range(3), list("def")).image)

    @pytest.mark.xfail(raises=NotImplementedError,reason='TODO')
    def test_zip_reduce(self):
        self.assertEqual([(1, 2, 3), (1, 2, 3)], Iter([[1, 1], [2, 2], [3, 3]]).zip_reduce([], lambda x, acc: tuple(x) + (acc,)).image)
        self.assertEqual([(1, {'a': 3}, 5), (2, {'b': 4}, 6)],  Iter([]).zip_reduce([5, 6], lambda x, acc: tuple(x) + (acc,), [1, 2], {'a': 3, 'b': 4}).image)

    def test_zip_with(self):
        self.assertEqual([5, 7, 9], Iter([]).zip_with(operator.add, [1, 2, 3], [4, 5, 6]).image)
        self.assertEqual([5, 11], Iter([]).zip_with(lambda x, y, z: x + y + z, [1, 3], [3, 5], [1, 3]).image)
        self.assertEqual([5, 7], Iter([]).zip_with(operator.add, [1, 2], [4, 5, 6, 7]).image)

    def test_eq(self):
        a = Iter.range(a, b)
        b = Iter.range(a, b)
        self.assertEqual(a, b)

    def test_ne(self):
        a = Iter.range(1, 10)
        b = Iter.range(5, 12)
        self.assertNotEqual(a, b)

    def test_iter(self):
        a, b = 1, 10
        for i in Iter.range(a, b):
            self.assertTrue(a <= i and i <= b)

    def test_next(self):
        a, b = 3, 6
        sequence = Iter.range(a, b)
        self.assertEqual(3, next(sequence))
        self.assertEqual(4, next(sequence))
        self.assertEqual(5, next(sequence))
        self.assertEqual(6, next(sequence))

    def test_str(self):
        self.assertEqual("1,2,3,4,5", str(Iter.range(1, 5)))
        self.assertEqual("1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20", str(Iter.range(1, 20)))

    def test_repr(self):
        self.assertEqual("Iter(domain=[1, 2, 3, 4, 5],image=[1, 2, 3, 4, 5])", repr(Iter.range(1, 5)))
        self.assertEqual("Iter(domain=[1, 2, 3, 4, 5, ...],image=[1, 2, 3, 4, 5, ...])", repr(Iter.range(1, 50)))
