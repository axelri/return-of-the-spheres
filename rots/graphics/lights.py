from OpenGL.GL import *
from math_classes import vectors

# TODO: Add other attributes to the light, such as color, direction,
# angle of the spreading light etc.

class Light:
    ''' A class to hold Light objects, contains the OpenGL-index
    for the light and the properties of the light. '''
    
    def __init__(self, lightIndex, pos, isSpotlight = False,
                 ambient = [0.2, 0.2, 0.2, 1.0],
                 diffuse = [0.8, 0.8, 0.8, 1.0],
                 specular = [0.5, 0.5, 0.5, 1.0]):
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
        self._isSpotlight = False
        self._ambient = ambient
        self._diffuse = diffuse
        self._specular = specular

        glEnable(self._lightIndex)

        self.setup()

        # TODO: Add spotlight properties like cutoff etc.

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

    def move(self):
        ''' Moves the light to its current position '''
        # The last part (+[float(not self._isSpotlight)])
        # is there because the fourth element in the position
        # is used by OpenGL to define if it is a spotlight
        # or not: 1.0 means no spotlight, 0.0 means spotlight.
        glLightfv(self._lightIndex, GL_POSITION,
                  self._pos.value+[float(not self._isSpotlight)])

    def setup(self):
        ''' Sets the wanted properties of the light in OpenGL '''
        glLightfv(self._lightIndex, GL_AMBIENT, self._ambient)
        glLightfv(self._lightIndex, GL_DIFFUSE, self._diffuse)
        glLightfv(self._lightIndex, GL_SPECULAR, self._specular)
        glLightfv(self._lightIndex, GL_POSITION,
                  self._pos.value+[float(not self._isSpotlight)])

    def disable(self):
        ''' Disables the light '''
        glDisable(self._lightIndex)
        
        
        
