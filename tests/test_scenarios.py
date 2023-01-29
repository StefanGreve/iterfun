import unittest

from src.iterfun import Iter
from src.iterfun import Functions as fun

class TestScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data2022d1 = [[1000, 2000, 3000], [4000], [5000, 6000], [7000, 8000, 9000], [10000]]

    #region custom scenarios

    def test_scenario1(self):
        actual = Iter.range(1, 10).filter(fun.is_even).map(fun.invert).sum()
        self.assertEqual(-30, actual)

    #endregion

    #region advent of code

    def test_year2022_day1_task1(self):
        actual = Iter(self.data2022d1).map(sum).max()
        self.assertEqual(24_000, actual)

    def test_year2022_day1_task2(self):
        actual = Iter(self.data2022d1).map(sum).sort(descending=True).take(3).sum()
        self.assertEqual(45_000, actual)

    #endregion
