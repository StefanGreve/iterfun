from itertools import accumulate
import unittest
import pytest

from src.iterfun import Iter

class TestIter(unittest.TestCase):
    #region unit tests

    def test_all(self):
        self.assertTrue(Iter([1, 2, 3]).all())
        self.assertFalse(Iter([1, None, 3]).all())
        self.assertTrue(Iter([]).all())
        self.assertTrue(Iter([2,4,6]).all(lambda x: x % 2 == 0))
        self.assertFalse(Iter([1,2,3]).all(lambda x: x % 2 == 0))
        self.assertTrue(Iter([]).all(lambda: None))

    def test_any(self):
        self.assertFalse(Iter([False, False, False]).any())
        self.assertTrue(Iter([False, True, False]).any())
        self.assertFalse(Iter([]).any())
        self.assertFalse(Iter([2,4,6]).any(lambda x: x % 2 == 1))
        self.assertTrue(Iter([1,2,3]).any(lambda x: x % 2 == 1))
        self.assertFalse(Iter([]).any(lambda: None))

    def test_at(self):
        self.assertEqual(2, Iter([2,4,6]).at(0))
        self.assertEqual(6, Iter([2,4,6]).at(2))
        self.assertEqual(6, Iter([2,4,6]).at(-1))

    def test_at_throws(self):
        with pytest.raises(IndexError):
            self.assertEqual(None, Iter([2,4,6]).at(4))

    def test_avg(self):
        self.assertEqual(5, Iter(range(11)).avg())

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
        self.assertEqual(3, Iter(range(1, 4)).count())
        self.assertEqual(2, Iter(range(1, 6)).count(lambda x: x % 2 == 0))

    #endregion

    #region integration tests

    #endregion
