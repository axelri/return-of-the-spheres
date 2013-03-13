import unittest
import yaml
from pygame.locals import *
from ..profile import Profile

class TestVector(unittest.TestCase):

    def setUp(self):
        with open('test_profile.yml', 'r') as f:
            config = yaml.safe_load(f)

        self.p = Profile(config)

    def test_get_keys(self):
        expected = [K_w, K_UP]
        actual = self.p.get_keys('forward')
        self.assertEqual(expected, actual)

        expected = [K_s, K_DOWN]
        actual = self.p.get_keys('backward')
        self.assertEqual(expected, actual)

        expected = [K_a, K_LEFT]
        actual = self.p.get_keys('left')
        self.assertEqual(expected, actual)

        expected = [K_d, K_RIGHT]
        actual = self.p.get_keys('right')
        self.assertEqual(expected, actual)

        expected = [K_SPACE, None]
        actual = self.p.get_keys('jump')
        self.assertEqual(expected, actual)

        expected = [K_ESCAPE, None]
        actual = self.p.get_keys('menu')
        self.assertEqual(expected, actual)

    def test_set_keys(self):
        self.p.set_keys('forward', ['G', 'space'])
        expected = [K_g, K_SPACE]
        actual = self.p.get_keys('forward')
        self.assertEqual(expected, actual)

    def test_get_mouse_sensitivity(self):
        self.assertEqual(0.3, self.p.get_mouse_sensitivity())

    def test_set_mouse_sensitivty(self):
        self.p.set_mouse_sensitivity(0.5)
        self.assertEqual(0.5, self.p.get_mouse_sensitivity())

if __name__ == '__main__':
    unittest.main()
