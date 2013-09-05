from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

from math import sin, cos, pi, asin, acos

from math_classes import matrices
from math_classes.vectors import Vector
from graphics import draw, textures
from sound import sound_effects

class Moving_scene(object):
    ''' Base class for all objects in the 
        'static' scene that are supposed
        to be able to move, such as doors,
        moving platforms, elevators etc. '''

    def __init__(self):
        # TODO: Put more things here, all the things that
        # are common for all moving scene objects.

        self._geom = None

        self._ambient = None
        self._diffuse = None
        self._specular = None
        self._shininess = None
        self._emissive = None

        self._texture = None

        self._display_list_index = None

        self._friction = 1
        self._bounce = 0.2

    def get_texture(self):
        return self._texture

    def get_pos(self):
        return Vector(self._geom.getPosition())

    def get_orientation(self):
        orientation = matrices.ODE_to_OpenGL(self._geom.getRotation())
        return orientation

    def get_material_properties(self):
        return self._ambient, self._diffuse, self._specular,\
               self._shininess, self._emissive

    def get_friction(self):
        return self._friction

    def get_bounce(self):
        return self._bounce

    def set_friction(self, friction):
        self._friction = friction

    def set_bounce(self, bounce):
        self._bounce = bounce

    def draw(self):
        self.update()
        pos = self.get_pos().value
        glTranslatef(pos[0], pos[1], pos[2])
        rotMatrix = self.get_orientation()
        glMultMatrixf(rotMatrix)
        glCallList(self._display_list_index)

    def set_data(self, name, value):
        ''' Sets an attribute of the object's geom,
            keyword 'name', value 'value' '''
        self._geom.__setattr__(name, value)

    def draw_AABB(self):
        aabb = self._geom.getAABB()
        draw.AABB(aabb)

    def update(self):
        pass

class Sliding_door(Moving_scene):
    ''' A class for sliding doors. '''

    def __init__(self, space, pos = Vector(), normal = Vector((0.0, 1.0, 0.0)), 
                slide_dir = Vector((1.0, 0.0, 0.0)), slide_size = 5,
                ort_size = 5, thickness = 0.5, texture = None,
                opening_time = 30):

        super(Sliding_door, self).__init__()
        
        self._slide_size = slide_size   # Size in the slide direction
        self._thickness = thickness
        self._ort_size = ort_size       # Size orthogonal to the slide direction
        self._normal = normal
        self._slide_dir = slide_dir
        self._texture = texture
        self._pos = pos

        self._open = False
        self._toggling = False  # Opening or closing

        self._opening_time = opening_time   # Time, in frames, to open/close the door
        self._opening_counter = 0

        # Set ODE properties
        self._space = space
        self._geom = ode.GeomBox(self._space, (self._ort_size, 
                                self._thickness, self._slide_size))
        self._body = None
        self._geom.setBody(self._body)

        self.set_data('object', self)
        self._slide_sound = sound_effects.load_sound('slide_2.wav')

        # Calculate the rotation matrix in the first direction needed to align the 
        # bounding box with the object
        axis = Vector([0.0, 1.0, 0.0]).cross(self._normal)
        if axis.norm() < 0.1:
            #Parallel
            axis = Vector([0.0, 0.0, 1.0])
        angle1 = acos(Vector([0.0, 1.0, 0.0]).dot(self._normal))
        rotation1 = matrices.generate_rotation_matrix(axis, angle1)

        # Calculate the second rotation matrix
        angle2 = asin(Vector([0.0, 0.0, 1.0]).cross(self._slide_dir).norm())
        rotation2 = matrices.generate_rotation_matrix(self._normal, angle2)

        # Combine the two rotations
        rotation = matrices.OpenGL_to_ODE(matrices.matrix_mult(rotation2, rotation1))

        self._pos = self._pos + self._normal * self._thickness * 0.5 # To prevent it from being inside the wall
        self._closed_pos = self._pos

        self._geom.setPosition(self._pos.value)
        self._geom.setRotation(rotation)

        self._ambient = [1.0, 0.5, 0.5, 1.0]
        self._diffuse = [1.0, 0.5, 0.5, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 10
        self._emissive = [0.0, 0.0, 0.0, 1.0]

        self._display_list_index = self.create_displaylist_index()

    def update(self):
        ''' Checks if the door should be opening or closing,
            if so do that, otherwise pass. '''

        # TODO: Change the arguments of the cos and sin calls to create smoother movement
        # (slow start, slow stop)

        # Check if it should be toggling
        if self._toggling:
            # Check in which state it is
            if self._open:
                # It is open, close it
                self._opening_counter += 1
                self._pos = self._closed_pos + self._slide_dir * \
                            (1 + cos(pi * (float(self._opening_counter)/self._opening_time))) \
                            * self._slide_size * 0.5

                # Check if it is closed
                if self._opening_counter == self._opening_time:
                    self._opening_counter = 0
                    self._toggling = False
                    self._open = False

            else:
                # It is closed, open it
                self._opening_counter += 1
                self._pos = self._closed_pos + self._slide_dir * \
                            (1 + sin(pi * (((float(self._opening_counter)/self._opening_time)) - 0.5))) \
                            * self._slide_size * 0.5

                # Check if it is open
                if self._opening_counter == self._opening_time:
                    self._opening_counter = 0
                    self._toggling = False
                    self._open = True

        self._geom.setPosition(self._pos.value)

    def toggle(self):
        ''' Toggles the door: Opens it if it is closed and vice versa.
            If the door is currently closing/opening, it does nothing. '''

        if not self._toggling:
            self._toggling = True
            self._slide_sound.play()

    def open(self):
        ''' Opens the door. If it is already open the call is ignored. '''

        if not self._open:
            self._toggling = True

    def close(self):
        ''' Closes the door. If it is already closed the call is ignored. '''

        if self._open:
            self._toggling = True

    def get_sides(self):
        return self._ort_size, self._thickness, self._slide_size

    def create_displaylist_index(self):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.box(self)
        glEndList()
        return display_list_index
