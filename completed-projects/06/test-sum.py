import unittest
import sum

class TestSum(unittest.TestCase):

    def test_should_add_correctly(self):
        self.assertEqual(sum.sum(1,2), 3)

if __name__ == '__main__':
    unittest.main()
