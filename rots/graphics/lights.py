from OpenGL.GL import *
from math_classes.vectors import Vector

# TODO: Add other attributes to the light, such as color, direction,
# angle of the spreading light etc.

class Light:
    ''' A class to hold Light objects, contains the OpenGL-index
    for the light and the properties of the light. '''
    
    def __init__(self, light_index, pos, is_spotlight = False,
                 ambient = [0.2, 0.2, 0.2, 1.0],
                 diffuse = [0.8, 0.8, 0.8, 1.0],
                 specular = [0.5, 0.5, 0.5, 1.0]):
        ''' Initializes the Light object, sets the OpenGL-index
        of the light and its starting position.

        Input:  light_index: An OpenGL constant referencing the
                    light in OpenGL.
                pos: A vector describing the position of the light. '''
        
        assert isinstance(light_index, OpenGL.constant.IntConstant), \
               'Input must be an OpenGL constant'
        assert isinstance(pos, Vector), \
               'Input must be a vector'
        
        self._light_index = light_index
        self._pos = pos
        self._is_spotlight = False
        self._ambient = ambient
        self._diffuse = diffuse
        self._specular = specular

        glEnable(self._light_index)

        self._setup()

        # TODO: Add spotlight properties like cutoff etc.

    # Getters

    def get_light_index(self):
        return self._light_index

    def get_pos(self):
        return self._pos

    def get_ambient(self):
        return self._ambient

    def get_diffuse(self):
        return self._diffuse
    
    def get_specular(self):
        return self._specular

    #Setters

    def set_pos(self, pos):
        self._pos = pos
        self.move()

    def add_pos(self, pos):
        self._pos += pos
        self.move()

    def set_ambient(self, ambient):
        self._ambient = ambient
        self._setup()

    def set_diffuse(self, diffuse):
        self._diffuse = diffuse
        self._setup()

    def set_specular(self, specular):
        self._specular = specular
        self._setup()



    def move(self):
        ''' Moves the light to its current position '''
        # The last part (+[float(not self._is_spotlight)])
        # is there because the fourth element in the position
        # is used by OpenGL to define if it is a spotlight
        # or not: 1.0 means no spotlight, 0.0 means spotlight.
        glLightfv(self._light_index, GL_POSITION,
                  self._pos.value+tuple([float(not self._is_spotlight)]))

    def _setup(self):
        ''' Sets the wanted properties of the light in OpenGL '''
        glLightfv(self._light_index, GL_AMBIENT, self._ambient)
        glLightfv(self._light_index, GL_DIFFUSE, self._diffuse)
        glLightfv(self._light_index, GL_SPECULAR, self._specular)
        self.move()

    def disable(self):
        ''' Disables the light '''
        glDisable(self._light_index)
