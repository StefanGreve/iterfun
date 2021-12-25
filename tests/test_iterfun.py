import operator
import unittest

import pytest

from src.iterfun import Iter


class TestIter(unittest.TestCase):
    def test_iter_domain(self):
        iter = Iter([1, 4])
        self.assertEqual(iter.domain, iter.image)
        self.assertNotEqual(iter.domain, iter.filter(lambda x: x % 2 == 0).image)

    def test_iter_image(self):
        self.assertEqual([1, 2, 3], Iter([1, 2, 3]).image)
        self.assertEqual([1, 2, 3, 4, 5], Iter([1, 5]).image)
        self.assertEqual([1, 5], Iter([1, 5], interval=False).image)
        self.assertEqual([2, 3, 4, 5, 6, 7, 8, 9], Iter((1, 10)).domain)

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
        expected = [[1], [2, 2], [3], [4, 4, 6], [7, 7]]
        actual = Iter([1, 2, 2, 3, 4, 4, 6, 7, 7]).chunk_by(lambda x: x % 2 == 1).image
        self.assertEqual(expected, actual)

    def test_chunk_every(self):
        self.assertEqual([[1, 2], [3, 4], [5, 6]], Iter([1, 6]).chunk_every(2).image)
        self.assertEqual([[1, 2, 3], [3, 4, 5], [5, 6]], Iter([1, 6]).chunk_every(3, 2).image)
        self.assertEqual([[1, 2, 3], [3, 4, 5], [5, 6, 7]], Iter([1, 6]).chunk_every(3, 2, [7]).image)
        self.assertEqual([[1, 2, 3], [4]], Iter([1, 4]).chunk_every(3, 3, []).image)
        self.assertEqual([[1, 2, 3, 4]], Iter([1, 4]).chunk_every(10).image)
        self.assertEqual([[1, 2], [4, 5]], Iter([1, 5]).chunk_every(2, 3, []).image)

    @pytest.mark.xfail(raises=NotImplementedError, reason="TODO")
    def test_chunk_while(self):
        self.assertEqual([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]], Iter([1, 10]).chunk_while([], None, None))

    def test_concat(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], Iter([[1, 2, 3], [4, 5, 6]]).concat().image)
        self.assertEqual([1, [2], 3, 4, 5, 6], Iter([[1, [2], 3], [4], [5, 6]]).concat().image)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], Iter([[1, 4], [5, 6], [7, 9]]).concat().image)
        self.assertEqual([1, 2, 3, 8], Iter([(0, 4), (5, 6), (7, 9)]).concat().image)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], Iter([(0, 4), (3, 7), (6, 10)]).concat().image)

    def test_count(self):
        self.assertEqual(3, Iter([1, 3]).count())
        self.assertEqual(2, Iter([1, 5]).count(lambda x: x % 2 == 0))

    def test_count_until(self):
        self.assertEqual(5, Iter([1, 20]).count_until(5))
        self.assertEqual(20, Iter([1, 20]).count_until(50))
        self.assertTrue(Iter([1, 10]).count_until(10) == 10)
        self.assertTrue(Iter([1, 12]).count_until(10 + 1) > 10)
        self.assertTrue(Iter([1, 5]).count_until(10) < 10)
        self.assertTrue(Iter([1, 10]).count_until(10 + 1) == 10)
        self.assertEqual(7, Iter([1, 20]).count_until(7, lambda x: x % 2 == 0))
        self.assertTrue(10, Iter([1, 20]).count_until(11, lambda x: x % 2 == 0))

    def test_dedup(self):
        self.assertEqual([1, 2, 3, 2, 1], Iter([1, 2, 3, 3, 2, 1]).dedup().image)

    def test_dedup_by(self):
        self.assertEqual([5, 1, 3, 2], Iter([5, 1, 2, 3, 2, 1]).dedup_by(lambda x: x > 2).image)
        self.assertEqual([0, 3, 2], Iter([0, 1, 2, 3, 2, 1]).dedup_by(lambda x: x > 2).image)
        self.assertEqual([0, 4, 1, 2, 0, 3], Iter([0, 4, 9, 1, 2, 0, 3, 4, 9]).dedup_by(lambda x: x < 2).image)
        self.assertEqual([3, 2, 4, 1], Iter([3, 6, 7, 7, 2, 0, 1, 4, 1]).dedup_by(lambda x: x > 2).image)
        self.assertEqual([3, 2, 0], Iter([3, 6, 7, 7, 2, 0, 1, 4, 1]).dedup_by(lambda x: x == 2).image)

    def test_drop(self):
        self.assertEqual([3], Iter([1, 3]).drop(2).image)
        self.assertEqual([], Iter([1, 3]).drop(10).image)
        self.assertEqual([1, 2, 3], Iter([1, 3]).drop(0).image)
        self.assertEqual([1, 2], Iter([1, 3]).drop(-1).image)

    def test_drop_every(self):
        self.assertEqual([2, 4, 6, 8, 10], Iter([1, 10]).drop_every(2).image)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], Iter([1, 10]).drop_every(0).image)
        self.assertEqual([], Iter([1, 3]).drop_every(1).image)

    def test_drop_while(self):
        self.assertEqual([3, 2, 1], Iter([1, 2, 3, 2, 1]).drop_while(lambda x: x < 3).image)

    def test_each(self):
        self.assertTrue(Iter(["some", "example"], interval=False).each(print))

    def test_empty(self):
        self.assertTrue(Iter([]).empty())
        self.assertTrue(Iter([0, 0]).empty())
        self.assertFalse(Iter([1, 10]).empty())

    @pytest.mark.xfail(raises=NotImplementedError, reason="TODO")
    def test_fetch(self):
        self.assertTrue(Iter([2, 4, 6]).fetch(0).image)
        self.assertTrue(Iter([2, 4, 6]).fetch(-3).image)
        self.assertTrue(Iter([2, 4, 6]).fetch(2).image)
        self.assertFalse(Iter([2, 4, 6]).fetch(4).image)

    def test_filter(self):
        self.assertEqual([2], Iter([1, 3]).filter(lambda x: x % 2 == 0).image)

    def test_find(self):
        self.assertEqual(3, Iter([2, 4]).find(lambda x: x % 2 == 1))
        self.assertEqual(None, Iter([2, 4, 6]).find(lambda x: x % 2 == 1))
        self.assertEqual(0, Iter([2, 4, 6]).find(lambda x: x % 2 == 1, default=0))

    def test_find_index(self):
        self.assertEqual(None, Iter([2, 4, 6]).find_index(lambda x: x % 2 == 1))
        self.assertEqual(1, Iter([2, 3, 4]).find_index(lambda x: x % 2 == 1))

    def test_find_value(self):
        self.assertEqual(None, Iter([2, 4, 6]).find_value(lambda x: x % 2 == 1))
        self.assertTrue(Iter([2, 3, 4]).find_value(lambda x: x % 2 == 1))
        self.assertTrue(Iter([2, 3, 4]).find_value(lambda x: x % 2 == 1))
        self.assertEqual("no bools!", Iter([1, 3]).find_value(lambda x: isinstance(x, bool), default="no bools!"))

    def test_flat_map(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], Iter([(1, 3), (4, 6)], interval=False).flat_map(lambda x: Iter.range(list(x))).image)
        self.assertEqual([[1], [2], [3]], Iter([1, 2, 3]).flat_map(lambda x: [[x]]).image)

    @pytest.mark.xfail(raises=NotImplementedError, reason="TODO")
    def test_flat_map_reduce(self):
        n = 3
        fun = lambda x, acc: [[x], acc+1] if acc < n else acc
        self.assertEqual([[1, 2, 3], 3], Iter([1, 100]).flat_map_reduce(fun, acc=0).image)

    def test_frequencies(self):
        self.assertEqual({1: 1, 2: 2, 3: 1, 4: 1, 5: 2, 6: 1}, Iter([1, 2, 2, 3, 4, 5, 5, 6]).frequencies().image)

    def test_frequencies_by(self):
        self.assertEqual({"aa": 2, "bb": 1, "cc": 1}, Iter(["aa", "aA", "bb", "cc"]).frequencies_by(str.lower).image)
        self.assertEqual({3: 2, 2: 2, 1: 1}, Iter(["aaa", "aA", "bbb", "cc", "c"]).frequencies_by(len).image)

    def test_group_by(self):
        self.assertEqual({3: ["ant", "cat"], 5: ["dingo"], 7: ["buffalo"]},  Iter(["ant", "buffalo", "cat", "dingo"]).group_by(len).image)
        self.assertEqual({3: ["a", "c"], 5: ["d"], 7: ["b"]},  Iter(["ant", "buffalo", "cat", "dingo"]).group_by(len, operator.itemgetter(0)).image)

    def test_intersperse(self):
        self.assertEqual([1, 0, 2, 0, 3], Iter([1, 3]).intersperse(0).image)
        self.assertEqual([1], Iter([1]).intersperse(0).image)
        self.assertEqual([], Iter([]).intersperse(0).image)

    def test_into(self):
        self.assertEqual([1, 2], Iter([1, 2]).into([]).image)
        self.assertEqual({'a': 1, 'b': 2}, Iter({'a': 1, 'b': 2}).into({}).image)
        self.assertEqual({'a': 1, 'b': 2}, Iter({'a': 1}).into({'b': 2}).image)

    def test_join(self):
        self.assertEqual('12345', Iter([1, 5]).join())
        self.assertEqual('1,2,3,4,5', Iter([1, 5]).join(','))

    def test_map(self):
        self.assertEqual([2, 4, 6], Iter([1, 3]).map(lambda x: 2 * x).image)
        self.assertEqual({'a': -1, 'b': -2}, Iter({'a': 1, 'b': 2}).map(lambda k, v: {k: -v}).image)
        self.assertEqual({'a': 2, 'b': 4}, Iter({'a': 1, 'b': 2}).map(lambda k, v: {k: 2 * v}).image)

    def test_map_every(self):
        self.assertEqual([1001, 2, 1003, 4, 1005, 6, 1007, 8, 1009, 10], Iter([1, 10]).map_every(2, lambda x: x+1000).image)
        self.assertEqual([1001, 2, 3, 1004, 5, 6, 1007, 8, 9, 1010], Iter([1, 10]).map_every(3, lambda x: x + 1000).image)
        self.assertEqual([1, 2, 3, 4, 5], Iter([1, 5]).map_every(0, lambda x: x + 1000).image)
        self.assertEqual([1001, 1002, 1003], Iter([1, 3]).map_every(1, lambda x: x + 1000).image)

    def test_map_intersperse(self):
        self.assertEqual([2, None, 4, None, 6], Iter([1, 3]).map_intersperse(None, lambda x: 2 * x).image)

    def test_map_join(self):
        self.assertEqual('246', Iter([1, 3]).map_join(lambda x: 2 * x))
        self.assertEqual('2 = 4 = 6', Iter([1, 3]).map_join(lambda x: 2 * x, " = "))

    def test_map_reduce(self):
        self.assertEqual(([2, 4, 6], 6), Iter([1, 3]).map_reduce(0, lambda x: 2 * x, operator.add).image)
        self.assertEqual(([1, 4, 9], 0), Iter([1, 3]).map_reduce(6, lambda x: x * x, operator.sub).image)

    def test_max(self):
        self.assertEqual(3, Iter([1, 3]).max())
        self.assertEqual('you', Iter("you shall not pass".split()).max())
        self.assertEqual('shall', Iter("you shall not pass".split()).max(len))
        self.assertEqual('n/a', Iter([]).max(empty_fallback='n/a'))

    def test_member(self):
        self.assertTrue(Iter([1, 10]).member(5))
        self.assertTrue(Iter([1, 10]).member(5.0))
        self.assertTrue(Iter([1.0, 2.0, 3.0]).member(2))
        self.assertTrue(Iter([1.0, 2.0, 3.0]).member(2.000))
        self.assertFalse(Iter(['a', 'b', 'c']).member('d'))

    def test_max(self):
        self.assertEqual(1, Iter([1, 3]).min())
        self.assertEqual('not', Iter("you shall not pass".split()).min())
        self.assertEqual('you', Iter("you shall not pass".split()).min(len))
        self.assertEqual('n/a', Iter([]).min(empty_fallback='n/a'))

    def test_min_max(self):
        self.assertEqual((1, 3), Iter([1, 3]).min_max())
        self.assertEqual((None, None), Iter([]).min_max(empty_fallback=None))
        self.assertEqual(('a', 'aaa'), Iter(["aaa", "a", "bb", "c", "ccc"]).min_max(len))

    def test_product(self):
        self.assertEqual(24, Iter([2, 3, 4]).product())
        self.assertEqual(24.0, Iter([2.0, 3.0, 4.0]).product())

    def test_random(self):
        numbers = Iter.range([1, 100])
        self.assertIn(Iter(numbers).random(), numbers)

    def test_range(self):
        self.assertEqual([1, 2, 3, 4, 5], Iter.range([1, 5]))
        self.assertEqual([2, 3, 4], Iter.range((1, 5)))

    def test_reduce(self):
        self.assertEqual(10,  Iter([1, 4]).reduce(operator.add))
        self.assertEqual(24,  Iter([1, 4]).reduce(lambda x, acc: x * acc, acc=1))

    def test_reduce_while(self):
        self.assertEqual(10, Iter([1, 100]).reduce_while(lambda x, acc: (True, x + acc) if x < 5 else (False, acc)))
        self.assertEqual(5050, Iter([1, 100]).reduce_while(lambda x, acc: (True, acc + x) if x > 0 else (False, acc)))
        self.assertEqual(0, Iter([1, 100]).reduce_while(lambda x, acc: (True, acc - x) if x % 2 == 0 else (False, acc), acc=2550))

    def test_reject(self):
        self.assertEqual([1, 3], Iter([1, 3]).reject(lambda x: x % 2 == 0).image)

    def test_reverse(self):
        self.assertEqual([5, 4, 3, 2, 1], Iter([1, 5]).reverse().image)
        self.assertEqual([3, 2, 1, 4, 5, 6], Iter([1, 3]).reverse([4, 5, 6]).image)

    def test_reverse_slice(self):
        self.assertEqual([1, 2, 6, 5, 4, 3], Iter([1, 6]).reverse_slice(2, 4).image)
        self.assertEqual([1, 2, 6, 5, 4, 3, 7, 8, 9, 10], Iter([1, 10]).reverse_slice(2, 4).image)
        self.assertEqual([1, 2, 10, 9, 8, 7, 6, 5, 4, 3], Iter([1, 10]).reverse_slice(2, 30).image)

    def test_scan(self):
        self.assertEqual([1, 3, 6, 10, 15], Iter([1, 5]).scan(operator.add).image)
        self.assertEqual([1, 3, 6, 10, 15], Iter([1, 5]).scan(lambda x, y: x + y, acc=0).image)
        self.assertEqual([2, 4, 7, 11, 16], Iter([1, 5]).scan(operator.add, acc=1).image)

    def test_shorten(self):
        self.assertEqual("[1, 2, 3, 4, 5]", Iter.shorten(range(1, 6)))
        self.assertEqual("[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, ...]", Iter.shorten(range(1, 101), width=50))

    def test_shuffle(self):
        iter = Iter([1, 10]).shuffle()
        self.assertTrue(iter.all(lambda x: x in Iter.range([1, 10])))

    def test_slice(self):
        self.assertEqual([6, 7, 8, 9, 10, 11], Iter([1, 100]).slice([5, 10]).image)
        self.assertEqual([6, 7, 8, 9, 10], Iter([1, 10]).slice([5, 20]).image)
        self.assertEqual([26, 27, 28, 29, 30], Iter([1, 30]).slice([-5, -1]).image)
        self.assertEqual([7, 8, 9], Iter([1, 10]).slice([-4, -2]).image)
        self.assertEqual([7, 8, 9, 10], Iter([1, 10]).slice([-4, 100]).image)
        self.assertEqual([6, 7, 8, 9, 10], Iter([1, 10]).slice(5, 100).image)
        self.assertEqual([], Iter([1, 10]).slice(10, 5).image)
        self.assertEqual([], Iter([1, 10]).slice(-11, 5).image)

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
        self.assertEqual([[1, 2], [3]], Iter([1, 3]).split(2).image)
        self.assertEqual([[1, 2, 3], []], Iter([1, 3]).split(10).image)
        self.assertEqual([[], [1, 2, 3]], Iter([1, 3]).split(0).image)
        self.assertEqual([[1, 2], [3]], Iter([1, 3]).split(-1).image)
        self.assertEqual([[1], [2, 3]], Iter([1, 3]).split(-2).image)
        self.assertEqual([[], [1, 2, 3]], Iter([1, 3]).split(-5).image)

    def test_split_while(self):
        self.assertEqual([[1, 2], [3, 4]], Iter([1, 4]).split_while(lambda x: x < 3).image)
        self.assertEqual([[], [1, 2, 3, 4]], Iter([1, 4]).split_while(lambda x: x < 0).image)
        self.assertEqual([[1, 2, 3, 4], []], Iter([1, 4]).split_while(lambda x: x > 0).image)

    def test_split_with(self):
        self.assertEqual([[4, 2, 0], [5, 3, 1]], Iter([0, 5]).reverse().split_with(lambda x: x % 2 == 0).image)
        self.assertEqual([{'b': -2, 'd': -3}, {'a': 1, 'c':1}], Iter({'a': 1, 'b': -2, 'c': 1, 'd': -3}).split_with(lambda k, v: v < 0).image)
        self.assertEqual([{}, {'a': 1, 'b': -2, 'c': 1, 'd': -3}], Iter({'a': 1, 'b': -2, 'c': 1, 'd': -3}).split_with(lambda k, v: v > 50).image)
        self.assertEqual([{}, {}], Iter({}).split_with(lambda k, v: v > 50).image)

    def test_sum(self):
        self.assertEqual(5050, Iter([1, 100]).sum())

    def test_take(self):
        self.assertEqual([1, 2], Iter([1, 3]).take(2).image)
        self.assertEqual([1, 2, 3], Iter([1, 3]).take(10).image)
        self.assertEqual([], Iter([1, 3]).take(0).image)
        self.assertEqual([3], Iter([1, 3]).take(-1).image)

    def test_take_every(self):
        self.assertEqual([1, 3, 5, 7, 9], Iter([1, 10]).take_every(2).image)
        self.assertEqual([], Iter([1, 10]).take_every(0).image)
        self.assertEqual([1, 2, 3], Iter([1, 3]).take_every(1).image)

    def test_take_random(self):
        numbers = set(Iter.range([1, 100]))
        self.assertTrue(set(Iter([1, 100]).take_random(2).image).issubset(numbers))

    def test_take_while(self):
        self.assertEqual([1, 2], Iter([1, 3]).take_while(lambda x: x < 3).image)

    def test_uniq(self):
        self.assertEqual([1, 2, 3], Iter([1, 2, 3, 3, 2, 1]).uniq().image)

    def test_unzip(self):
        self.assertEqual([['a', 'b', 'c'], [1, 2, 3]], Iter({'a': 1, 'b': 2, 'c': 3}).unzip().image)
        self.assertEqual([['a', 'b', 'c'], [1, 2, 3]], Iter([('a', 1), ('b', 2), ('c', 3)]).unzip().image)
        self.assertEqual([['a', 'b', 'c'], [1, 2, 3]], Iter([['a', 1], ['b', 2], ['c', 3]]).unzip().image)

    def test_with_index(self):
        self.assertEqual([('a', 0), ('b', 1), ('c', 2)], Iter(list("abc")).with_index().image)
        self.assertEqual([('a', 2), ('b', 3), ('c', 4)], Iter(list("abc")).with_index(2).image)
        self.assertEqual([(0, 'a'), (1, 'b'), (2, 'c')], Iter(list("abc")).with_index(lambda k, v: (v, k)).image)

    def test_zip(self):
        self.assertEqual([(1, 'a', "foo"), (2, 'b', "bar"), (3, 'c', "baz")], Iter([1, 3]).zip(list("abc"), ["foo", "bar", "baz"]).image)
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

    def test_str(self):
        self.assertEqual("[1, 2, 3, 4, 5]", str(Iter([1, 5])))
        self.assertEqual("[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, ...]", str(Iter([1, 100])))

    def test_repr(self):
        self.assertEqual("Iter(domain=[1, 2, 3, 4, 5],image=[1, 2, 3, 4, 5])", repr(Iter([1, 5])))
        self.assertEqual("Iter(domain=[1, 2, 3, 4, 5, ...],image=[1, 2, 3, 4, 5, ...])", repr(Iter([1, 50])))
