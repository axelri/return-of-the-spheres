from OpenGL.GL import *
from math_classes import vectors

# TODO: Add other attributes to the light, such as color, direction,
# angle of the spreading light etc.

class Light:
    def __init__(self, light, pos):
        assert isinstance(light, OpenGL.constant.IntConstant), \
               'Input must be an OpenGL constant'
        assert isinstance(pos, vectors.Vector), 'Input must be a vector'
        self._light = light
        self._pos = pos

    def get_light(self):
        return self._light

    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        assert isinstance(pos, vectors.Vector), 'Input must be a vector'
        self._pos = pos

    def add_pos(self, pos):
        assert isinstance(pos, vectors.Vector), 'Input must be a vector'
        self._pos += pos
