import unittest
from benchmark_gpt_cf291eca import answer


class TestBenchmarkGPT(unittest.TestCase):
    def test_answer(self):
        self.assertEqual(answer(), 42)


if __name__ == "__main__":
    unittest.main()
