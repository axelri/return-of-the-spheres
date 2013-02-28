import unittest
from vector import *

class TestVector(unittest.TestCase):

    def setUp(self):
        self.v1 = Vector([2, 0, 3])
        self.v2 = Vector([0, 2, 3])
        self.v3 = Vector([1, 3, 0])

    def test_proj(self):
        pr = [0, 18.0/13.0, 27.0/13.0]
        proj = self.v1.projection(self.v2).get_value()
        for i in range(len(pr)):
            self.assertAlmostEqual(pr[i], proj[i])

    def check_equal(self, v1, v2):
        a = v1.get_value();
        b = v2.get_value();

if __name__ == '__main__':
    unittest.main()
