import unittest

from sor294_recovery import twice


class TwiceTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(twice(0), 0)

    def test_three(self):
        self.assertEqual(twice(3), 6)


if __name__ == "__main__":
    unittest.main()
