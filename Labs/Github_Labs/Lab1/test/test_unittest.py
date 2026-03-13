import sys
import os
import unittest

# Get the path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src.calculator import fun1, fun2, fun3, fun4, fun5

class TestCalculator(unittest.TestCase):

    def test_fun1(self):
        self.assertEqual(fun1(2, 3), 5)
        self.assertEqual(fun1(5, 0), 5)
        self.assertEqual(fun1(-1, 1), 0)
        self.assertEqual(fun1(-1, -1), -2)

    def test_fun2(self):
        self.assertEqual(fun2(2, 3), -1)
        self.assertEqual(fun2(5, 0), 5)
        self.assertEqual(fun2(-1, 1), -2)
        self.assertEqual(fun2(-1, -1), 0)

    def test_fun3(self):
        self.assertEqual(fun3(2, 3), 6)
        self.assertEqual(fun3(5, 0), 0)
        self.assertEqual(fun3(-1, 1), -1)
        self.assertEqual(fun3(-1, -1), 1)

    def test_fun4(self):
        self.assertEqual(fun4(2, 3, 5), 10)
        self.assertEqual(fun4(5, 0, -1), 4)
        self.assertEqual(fun4(-1, -1, -1), -3)
        self.assertEqual(fun4(-1, -1, 100), 98)

    def test_fun5(self):
        self.assertEqual(fun5(10, 2), 5)
        self.assertEqual(fun5(15, 3), 5)
        self.assertEqual(fun5(10, 0), "Error: Division by zero")

if __name__ == '__main__':
    unittest.main()