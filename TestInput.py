import unittest
from Calculator import *
class TestCar(unittest.TestCase):
    def test(self):
        self.assertEqual(is_prime(5), False)

