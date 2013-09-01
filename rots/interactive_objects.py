from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

from math_classes import matrices
from math_classes.vectors import Vector
from graphics import draw, textures

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
        ''' Sets an attribute of the power up's geom,
            keyword 'name', value 'value' '''
        self._geom.__setattr__(name, value)

    def draw_AABB(self):
        aabb = self._geom.getAABB()
        draw.AABB(aabb)

class Button(Interactive_object):
    ''' A class for buttons that the player can
        press in-game, that causes something to happen
        when pressed (e.g. open a door) '''

def __init__(self, space, pos, normal, forward, side = 2, thickness = 0.1,
                texture = None):

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

        #pos = pos - self._normal * self._thickness * 0.5

        self._geom.setPosition(pos.value)
        self._geom.setRotation(rotation)

        self._ambient = [1.0, 1.0, 1.0, 1.0]
        self._diffuse = [1.0, 1.0, 1.0, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 0
        self._emissive = [1.0, 1.0, 1.0, 1.0]

        self._display_list_index = self.create_displaylist_index()

    def create_displaylist_index(self):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.box(self)
        glEndList()
        return display_list_index

    def get_sides(self):
        return self._x_size, self._y_size, self._z_size