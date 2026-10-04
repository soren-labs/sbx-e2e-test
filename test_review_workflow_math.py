import unittest

from review_workflow_math import add


class ReviewWorkflowMathTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(3, 2), 5)


if __name__ == "__main__":
    unittest.main()
