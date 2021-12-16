import unittest

from src.iterfun import Iter

class TestIterator(unittest.TestCase):

    def test_hello(self):
        self.assertEqual("Hello, World!", Iter.hello())

