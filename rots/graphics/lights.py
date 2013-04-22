from OpenGL.GL import *
from math_classes import vectors

# TODO: Add other attributes to the light, such as color, direction,
# angle of the spreading light etc.

class Light:
    ''' A class to hold Light objects, contains the OpenGL-index
    for the light and the properties of the light. '''
    
    def __init__(self, lightIndex, pos):
        ''' Initializes the Light object, sets the OpenGL-index
        of the light and its starting position.

        Input:  lightIndex: An OpenGL constant referencing the
                    light in OpenGL.
                pos: A vector describing the position of the light. '''
        
        assert isinstance(lightIndex, OpenGL.constant.IntConstant), \
               'Input must be an OpenGL constant'
        assert isinstance(pos, vectors.Vector), \
               'Input must be a vector'
        
        self._lightIndex = lightIndex
        self._pos = pos

    def get_lightIndex(self):
        return self._lightIndex

    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        assert isinstance(pos, vectors.Vector), \
               'Input must be a vector'
        self._pos = pos

    def add_pos(self, pos):
        assert isinstance(pos, vectors.Vector), \
               'Input must be a vector'
        self._pos += pos
