import unittest

from src.iterfun import Functions as fun


class TestFunctions(unittest.TestCase):
    def test_is_prime(self):
        self.assertFalse(fun.is_prime(0))
        self.assertFalse(fun.is_prime(1))
        self.assertFalse(fun.is_prime(4))
        self.assertFalse(fun.is_prime(100))
        self.assertFalse(fun.is_prime(32472874282))
        self.assertFalse(fun.is_prime(2032320))
        self.assertFalse(fun.is_prime(9000600))
        self.assertTrue(fun.is_prime(2))
        self.assertTrue(fun.is_prime(3))
        self.assertTrue(fun.is_prime(5))
        self.assertTrue(fun.is_prime(7))
        self.assertTrue(fun.is_prime(43))
        self.assertTrue(fun.is_prime(59))
        self.assertTrue(fun.is_prime(83))
        self.assertTrue(fun.is_prime(97))
        self.assertTrue(fun.is_prime(2237))
        self.assertTrue(fun.is_prime(69899))
        self.assertTrue(fun.is_prime(363047))
        self.assertTrue(fun.is_prime(659713))
        self.assertTrue(fun.is_prime(2427281))
        self.assertTrue(fun.is_prime(81239489))
        self.assertTrue(fun.is_prime(81247169))
        self.assertTrue(fun.is_prime(24244807))
        self.assertTrue(fun.is_prime(3846589051))
        self.assertTrue(fun.is_prime(5224245449))
        self.assertTrue(fun.is_prime(798723477701))
        self.assertTrue(fun.is_prime(100005743))

