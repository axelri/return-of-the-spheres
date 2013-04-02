import unittest
from pygame.locals import *
from ..profile import Profile

class TestVector(unittest.TestCase):

    def setUp(self):
        self.config = {'control': {'jump': ['SPACE', None],
            'right': ['d', 'RIGHT'], 'mouse_sensitivity': 0.3,
            'forward': ['w', 'UP'], 'menu': ['ESCAPE', None],
            'backward': ['s', 'DOWN'], 'left': ['a', 'LEFT']},
            'debug': {'debug_mode': True},
            'visual': {'fullscreen': False,
            'fullscreen_width': None,
            'window_width': 640,
            'fullscreen_height': None, 'window_height': 480}}
        self.p1 = Profile(self.config)

        self.config2 = {'control': {'jump': ['LSHIFT', 'b'],
            'right': ['d', 'RIGHT'], 'mouse_sensitivity': 0.3,
            'forward': ['w', 'UP'], 'menu': ['ESCAPE', None],
            'backward': ['s', 'DOWN'], 'left': ['a', 'LEFT']},
            'debug': {'debug_mode': True},
            'visual': {'fullscreen': False,
            'fullscreen_width': None,
            'window_width': 640,
            'fullscreen_height': None, 'window_height': 480}}
        self.p2 = Profile(self.config2)

    def test_eq(self):
        self.assertTrue(self.p1 == Profile(self.config))
        self.assertFalse(self.p1 == self.p2)

    def test_neq(self):
        self.assertFalse(self.p1 != Profile(self.config))
        self.assertTrue(self.p1 != self.p2)

    def test_get_pygame_keys(self):
        expected = [K_w, K_UP]
        actual = self.p1.get_pygame_keys('forward')
        self.assertEqual(expected, actual)

        expected = [K_s, K_DOWN]
        actual = self.p1.get_pygame_keys('backward')
        self.assertEqual(expected, actual)

        expected = [K_a, K_LEFT]
        actual = self.p1.get_pygame_keys('left')
        self.assertEqual(expected, actual)

        expected = [K_d, K_RIGHT]
        actual = self.p1.get_pygame_keys('right')
        self.assertEqual(expected, actual)

        expected = [K_SPACE, None]
        actual = self.p1.get_pygame_keys('jump')
        self.assertEqual(expected, actual)

        expected = [K_ESCAPE, None]
        actual = self.p1.get_pygame_keys('menu')
        self.assertEqual(expected, actual)

        self.assertEqual(self.p1, Profile(self.config))

    def test_get_keys(self):
        expected = ['w', 'UP']
        actual = self.p1.get_keys('forward')
        self.assertEqual(expected, actual)

        self.assertEqual(self.p1, Profile(self.config))

    def test_set_keys(self):
        self.p1.set_keys('forward', ['G', 'space'])
        expected = [K_g, K_SPACE]
        actual = self.p1.get_pygame_keys('forward')
        self.assertEqual(expected, actual)

        expected = ['G', 'space']
        actual = self.p1.get_keys('forward')
        self.assertEqual(expected, actual)

    def test_get_mouse_sensitivity(self):
        self.assertEqual(0.3, self.p1.get_mouse_sensitivity())

    def test_set_mouse_sensitivty(self):
        self.p1.set_mouse_sensitivity(0.5)
        self.assertEqual(0.5, self.p1.get_mouse_sensitivity())

    def test_repr(self):
        config1_s = self.config.__repr__()
        config2_s = self.config2.__repr__()

        self.assertEqual(config1_s, self.p1.__repr__())
        self.assertEqual(config2_s, self.p2.__repr__())

if __name__ == '__main__':
    unittest.main()
