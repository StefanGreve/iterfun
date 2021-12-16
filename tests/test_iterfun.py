import unittest

from src.iterfun import Iterator

class TestIterator(unittest.TestCase):

    def test_hello(self):
        self.assertEqual("Hello, World!", Iterator.hello())

