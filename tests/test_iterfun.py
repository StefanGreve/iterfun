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

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_chunk_by(self):
        expected = [[1], [2, 2], [3], [4, 4, 6], [7, 7]]
        actual = Iter([1, 2, 2, 3, 4, 4, 6, 7, 7]).chunk_by(lambda x: x % 2 == 1)
        self.assertEqual(expected, actual)
        print(f"{actual=}")

    #endregion

    #region integration tests

    #endregion
