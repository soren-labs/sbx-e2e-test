import unittest

from benchmark_gpt_cb4cc647 import answer


class BenchmarkAnswerTest(unittest.TestCase):
    def test_answer_returns_42(self):
        self.assertEqual(answer(), 42)


if __name__ == "__main__":
    unittest.main()