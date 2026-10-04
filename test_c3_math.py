import unittest

from c3_math import add


class TestAdd(unittest.TestCase):
    def test_positive_arguments(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative_arguments(self):
        self.assertEqual(add(-2, -3), -5)

    def test_zero_arguments(self):
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(0, 3), 3)
        self.assertEqual(add(3, 0), 3)


if __name__ == "__main__":
    unittest.main()
