import unittest

from benchmark_gpt_22cfe49d import answer


class TestAnswer(unittest.TestCase):
    def test_answer_equals_42(self):
        self.assertEqual(answer(), 42)


if __name__ == "__main__":
    unittest.main()
