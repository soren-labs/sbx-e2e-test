import unittest

from sbx_production_greeting import greet


class GreetingTest(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet(), "hello")


if __name__ == "__main__":
    unittest.main()
