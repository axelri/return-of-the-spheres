import unittest
import math
from ..vector import Vector # relative import - good thingie!

class TestVector(unittest.TestCase):

    def setUp(self):
        self.v1 = Vector([2, 0, 3])
        self.v2 = Vector([0, 2, 3])
        self.v3 = Vector([1, 3, -2])

    def test_dim(self):
        self.assertEqual(3, self.v1.dim())
        self.assertEqual(4, Vector([1, 2, 3, 4]).dim())

    def test_is_zero(self):
        self.assertFalse(self.v1.is_zero())
        self.assertTrue(Vector([0, 0, 0]).is_zero())

    def test_is_not_zero(self):
        self.assertTrue(self.v1.is_not_zero())
        self.assertFalse(Vector([0, 0, 0]).is_not_zero())

    def test_dot(self):
        self.assertEqual(9, self.v1.dot(self.v2))

    def test_cross(self):
        self.assertEqual([-6, -6, 4], self.v1.cross(self.v2).value)

    def test_project(self):
        expected = [0, 18.0/13.0, 27.0/13.0]
        actual = self.v1.projected(self.v2).value

        for a, b in zip(expected, actual):
            self.assertAlmostEqual(a, b)

        expected = [-2.0/7.0, 18.0/13.0 - 6.0/7.0, 27.0/13.0 + 4.0/7.0]
        actual = self.v1.projected(self.v2, self.v3).value

        for a, b in zip(expected, actual):
            self.assertAlmostEqual(a, b)

    def test_norm(self):
        self.assertAlmostEqual(math.sqrt(13), self.v1.norm())

    def test_normalized(self):
        v = Vector(self.v1.value)
        self.assertAlmostEqual(1, self.v1.normalized().norm())
        self.assertEqual(v, self.v1) # should not mutate

    def test_equal(self):
        self.assertEqual(self.v1, Vector([2, 0, 3]))

    def test_not_equal(self):
        self.assertNotEqual(self.v1, self.v2)
    
    def test_mult_scalar(self):
        self.assertEqual([4, 0 , 6], (self.v1 * 2).value)

    def test_unary_neg(self):
        self.assertEqual([-2, 0, -3], (-self.v1).value)

    def test_vector_addition(self):
        self.assertEqual([2, 2, 6], (self.v1 + self.v2).value)

    def test_vector_subtraction(self):
        self.assertEqual([2, -2, 0], (self.v1 - self.v2).value)

if __name__ == '__main__':
    unittest.main()
