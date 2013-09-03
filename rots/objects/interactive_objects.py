from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import math

from math_classes import matrices
from math_classes.vectors import Vector
from graphics import draw, textures

def do_nothing():
    pass

class Interactive_object(object):
    ''' A base class for all interactive objects in the game,
        such as buttons, levers etc. '''

    def __init__(self):
        # TODO: Put more things here, all the things that
        # are common for all interactive objects.

        self._geom = None

        self._ambient = None
        self._diffuse = None
        self._specular = None
        self._shininess = None
        self._emissive = None

        self._texture = None

        self._display_list_index = None

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

    def draw(self):
        pos = self.get_pos().value
        glTranslatef(pos[0], pos[1], pos[2])
        rotMatrix = self.get_orientation()
        glMultMatrixf(rotMatrix)
        glCallList(self._display_list_index)

    def set_data(self, name, value):
        ''' Sets an attribute of the interactive object's geom,
            keyword 'name', value 'value' '''
        self._geom.__setattr__(name, value)

    def draw_AABB(self):
        aabb = self._geom.getAABB()
        draw.AABB(aabb)

    def collide_func(self):
        ''' The function that is called when the interactive 
            object is activated '''
        pass

class Button(Interactive_object):
    ''' A class for buttons that the player can
        press in-game, that causes something to happen
        when pressed (e.g. open a door) '''

    def __init__(self, space, pos, normal, forward, side = 2, thickness = 0.1,
                texture = None, action = do_nothing, args = None):

        super(Button, self).__init__()
        self._x_size = side
        self._y_size = thickness
        self._z_size = side
        self._normal = normal
        self._forward = forward
        self._texture = texture
        self._pos = pos

        # Set ODE properties
        self._space = space
        self._geom = ode.GeomBox(self._space, (self._x_size, 
                                self._y_size, self._z_size))
        self._body = None
        self._geom.setBody(self._body)

        self.set_data('object', self)

        self._pressed = False
        self._pressed_last_frame = False

        self._action = action
        self._args = args

        # Calculate the rotation matrix in the first direction needed to align the 
        # bounding box with the surface
        axis = Vector([0.0, 1.0, 0.0]).cross(self._normal)
        if axis.norm() < 0.1:
            #Parallel
            axis = Vector([0.0, 0.0, 1.0])
        angle1 = math.acos(Vector([0.0, 1.0, 0.0]).dot(self._normal))
        rotation1 = matrices.generate_rotation_matrix(axis, angle1)

        # Calculate the second rotation matrix
        angle2 = math.asin(Vector([0.0, 0.0, 1.0]).cross(self._forward).norm())
        rotation2 = matrices.generate_rotation_matrix(self._normal, angle2)

        # Combine the two rotations
        rotation = matrices.OpenGL_to_ODE(matrices.matrix_mult(rotation2, rotation1))

        self._pos = self._pos + self._normal * self._y_size * 0.5

        self._geom.setPosition(self._pos.value)
        self._geom.setRotation(rotation)

        self._ambient = [1.0, 1.0, 1.0, 1.0]
        self._diffuse = [1.0, 1.0, 1.0, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 0
        self._emissive = [0.0, 0.0, 0.0, 1.0]

        self._display_list_index = self.create_displaylist_index()

    def create_displaylist_index(self):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.box(self)
        glEndList()
        return display_list_index

    def get_sides(self):
        return self._x_size, self._y_size, self._z_size

    def set_pressed(self, pressed):
        self._pressed = pressed

    def set_pressed_last_frame(self, pressed):
        self._pressed_last_frame = pressed

    def get_pressed(self):
        return self._pressed

    def get_pressed_last_frame(self):
        return self._pressed_last_frame

    def collide_func(self):
        ''' The function that is called when the button is pressed '''

        # TODO: Make it get pressed and unpressed slowly with an animation.
        # TODO: Add click sound

        if self._args != None:
            self._action(self._args)
        else:
            self._action()

    def draw(self):
        pos = self.get_pos()
        if self._pressed:
            pos -= self._normal * self._y_size * 0.9

        pos = pos.value

        glTranslatef(pos[0], pos[1], pos[2])
        rotMatrix = self.get_orientation()
        glMultMatrixf(rotMatrix)
        glCallList(self._display_list_index)
