import unittest
from src.calculator import sum, substract, multiply, divide

class CalculatorTests(unittest.TestCase):
    def test_sum(self):
        assert sum(2, 3) == 5

    def test_substract(self):
        assert substract(10, 5) == 5

    def test_multiply(self):
        assert multiply(4, 5) == 20

    def test_divide_cero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)
    
    def test_divide(self):
        assert divide(10,5) == 2
