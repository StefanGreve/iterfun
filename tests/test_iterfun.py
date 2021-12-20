import unittest
import pytest

from src.iterfun import Iter

class TestIter(unittest.TestCase):
    #region unit tests

    def test_iter(self):
        self.assertEqual([1, 2, 3], Iter([1, 2, 3]).image)
        self.assertEqual([1, 2, 3, 4, 5], Iter(1, 5).image)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], Iter(1, 10).image)

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
        self.assertEqual(5, Iter(0, 10).avg())

    def test_chunk_by(self):
        expected = [[1], [2, 2], [3], [4, 4, 6], [7, 7]]
        actual = Iter([1, 2, 2, 3, 4, 4, 6, 7, 7]).chunk_by(lambda x: x % 2 == 1).image
        self.assertEqual(expected, actual)

    def test_chunk_every(self):
        self.assertEqual([[1, 2], [3, 4], [5, 6]], Iter(range(1, 7)).chunk_every(2).image)
        self.assertEqual([[1, 2, 3], [3, 4, 5], [5, 6]], Iter(range(1,7)).chunk_every(3, 2).image)
        self.assertEqual([[1, 2, 3], [3, 4, 5], [5, 6, 7]], Iter(range(1, 7)).chunk_every(3, 2, [7]).image)
        self.assertEqual([[1, 2, 3], [4]], Iter(range(1, 5)).chunk_every(3, 3, []).image)
        self.assertEqual([[1, 2, 3, 4]], Iter(range(1,5)).chunk_every(10).image)
        self.assertEqual([[1, 2], [4, 5]], Iter(range(1, 6)).chunk_every(2, 3, []).image)

    @pytest.mark.xfail(raises=NotImplementedError, reason="TODO")
    def test_chunk_while(self):
        self.assertEqual([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]], Iter(range(1, 11)).chunk_while([], None, None))

    def test_concant(self):
        self.assertEqual([1, [2], 3, 4, 5, 6],  Iter.concat([[1, [2], 3], [4], [5, 6]]).image)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], Iter.concat((1, 3), (4, 6), (7, 9)).image)
        self.assertEqual([1, 2, 3, 4, 5, 6],  Iter.concat([[1, 2, 3], [4, 5, 6]]).image)
        self.assertEqual([1, 2, 3, 4, 5, 6], Iter.concat((1, 3), (4, 6)).image)

    def test_count(self):
        self.assertEqual(3, Iter(1, 3).count())
        self.assertEqual(2, Iter(1, 5).count(lambda x: x % 2 == 0))

    def test_count_until(self):
        self.assertEqual(5, Iter(1, 20).count_until(5))
        self.assertEqual(20, Iter(1, 20).count_until(50))
        self.assertTrue(Iter(1, 10).count_until(10) == 10)
        self.assertTrue(Iter(1, 12).count_until(10 + 1) > 10)
        self.assertTrue(Iter(1, 5).count_until(10) < 10)
        self.assertTrue(Iter(1, 10).count_until(10 + 1) == 10)
        self.assertEqual(7, Iter(1, 20).count_until(7, lambda x: x % 2 == 0))
        self.assertTrue(10, Iter(1, 20).count_until(11, lambda x: x % 2 == 0))

    def test_dedup(self):
        self.assertEqual([1, 2, 3, 2, 1], Iter([1, 2, 3, 3, 2, 1]).dedup().image)

    @pytest.mark.xfail(raises=NotImplementedError, reason="TODO")
    def test_dedup_by(self):
        self.assertEqual([5, 1, 3, 2], Iter([5, 1, 2, 3, 2, 1]).dedup_by(lambda x: x > 2).image)

    def test_drop(self):
        self.assertEqual([3], Iter(1, 3).drop(2).image)
        self.assertEqual([], Iter(1, 3).drop(10).image)
        self.assertEqual([1, 2, 3], Iter(1, 3).drop(0).image)
        self.assertEqual([1, 2], Iter(1, 3).drop(-1).image)

    def test_drop_every(self):
        self.assertEqual([2, 4, 6, 8, 10], Iter(1, 10).drop_every(2).image)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], Iter(1, 10).drop_every(0).image)
        self.assertEqual([], Iter(1, 3).drop_every(1).image)

    def test_drop_while(self):
        self.assertEqual([3, 2, 1], Iter([1, 2, 3, 2, 1]).drop_while(lambda x: x < 3).image)

    def test_each(self):
        self.assertTrue(Iter(["some", "example"]).each(print))

    def test_empty(self):
        self.assertTrue(Iter([]).empty())
        self.assertTrue(Iter(0, 0).empty())
        self.assertFalse(Iter(1, 10).empty())

    @pytest.mark.xfail(raises=NotImplementedError, reason="TODO")
    def test_fetch(self):
        self.assertTrue(Iter([2, 4, 6]).fetch(0).image)
        self.assertTrue(Iter([2, 4, 6]).fetch(-3).image)
        self.assertTrue(Iter([2, 4, 6]).fetch(2).image)
        self.assertFalse(Iter([2, 4, 6]).fetch(4).image)

    def test_filter(self):
        self.assertEqual([2], Iter(1, 3).filter(lambda x: x % 2 == 0).image)

    def test_find(self):
        self.assertEqual(3, Iter(2, 4).find(lambda x: x % 2 == 1))
        self.assertEqual(None, Iter([2, 4, 6]).find(lambda x: x % 2 == 1))
        self.assertEqual(0, Iter([2, 4, 6]).find(lambda x: x % 2 == 1, default=0))

    def test_find_index(self):
        self.assertEqual(None, Iter([2, 4, 6]).find_index(lambda x: x % 2 == 1))
        self.assertEqual(1, Iter([2, 3, 4]).find_index(lambda x: x % 2 == 1))

    def test_find_value(self):
        self.assertEqual(None, Iter([2, 4, 6]).find_value(lambda x: x % 2 == 1))
        self.assertTrue(Iter([2, 3, 4]).find_value(lambda x: x % 2 == 1))
        self.assertEqual(9, Iter([2, 3, 4]).filter(lambda x: x > 2).find_value(lambda x: x * x))
        self.assertEqual("no bools!", Iter(1, 3).find_value(lambda x: isinstance(x, bool), default="no bools!"))

    def test_flat_map(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], Iter([(1, 3), (4, 6)]).flat_map(lambda x: list(range(x[0], x[1]+1))).image)
        self.assertEqual([[1], [2], [3]], Iter([1, 2, 3]).flat_map(lambda x: [[x]]).image)

    @pytest.mark.xfail(raises=NotImplementedError, reason="TODO")
    def test_flat_map_reduce(self):
        n = 3
        fun = lambda x, acc: [[x], acc+1] if acc < n else acc
        self.assertEqual([[1, 2, 3], 3], Iter(1, 100).flat_map_reduce(fun, acc=0).image)

    #endregion

    #region leet code tests

    #endregion
