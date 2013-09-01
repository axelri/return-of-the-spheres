from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import numbers #Needed?
import math

from math_classes import matrices
from math_classes.vectors import Vector
from graphics import draw


# TODO: Right now there is some redundance in the code since the
# create_displaylist_index() functions are almost identical in all
# shapes. However, I find it somewhat ugly to solve this like in
# fluffy, are there any better ways?

class Shape(object):

    def __init__(self, world):

        # Set ODE properties
        self._body = ode.Body(world)
        self._mass = ode.Mass()
        self._geom = None

        self._friction = 1
        self._bounce = 0.2

        self.colliding = False

        # Material properties
        self._ambient = None
        self._diffuse = None
        self._specular = None
        self._shininess = None
        self._emissive = None

        self._display_list_index = None
        self._texture = None

        # Explanations of the material properties:
        #   * Ambient and diffuse "define the color" of the material,
        #     the ambient part is spread over the entire shape
        #     whereas the diffuse is the part that causes shadows
        #     on the material. They should be set to the same value
        #     in case we don't want some fancy special effect.
        #     They are defined the same way as colors, as lists
        #     of 3 or 4 elements, all between 0.0 and 1.0.
        #   * Specular and shininess define the bright spot on the
        #     material, e.g. making it look like shiny plastic
        #     (i.e. the shininess). Specular is the color of the spot
        #     and shininess defines the size of it. Specular is
        #     defined like colors (se above) and shininess is an
        #     integer between 0 (no spot) and 128 (big spot)
        #   * Emissive defines the glow of the material,
        #     e.g. glow in the dark plastic could have a greenish
        #     emissive light. Emissive is defined like colors (se above)

    def get_body(self):
        return self._body

    def get_geom(self):
        return self._geom

    def get_vel(self):
        return Vector(self._body.getLinearVel())

    def get_pos(self):
        return Vector(self._body.getPosition())

    def get_orientation(self):
        orientation = matrices.ODE_to_OpenGL(self._body.getRotation())
        return orientation

    def get_material_properties(self):
        return self._ambient, self._diffuse, self._specular,\
               self._shininess, self._emissive

    def get_texture(self):
        return self._texture

    def get_friction(self):
        return self._friction

    def get_bounce(self):
        return self._bounce

    def set_friction(self, friction):
        self._friction = friction

    def set_bounce(self, bounce):
        self._bounce = bounce

    def set_ambient(self, ambient):
        self._ambient = ambient
        self._display_list_index = self.create_displaylist_index()

    def set_diffuse(self, diffuse):
        self._diffuse = diffuse
        self._display_list_index = self.create_displaylist_index()

    def set_specular(self, specular):
        self._specular = specular
        self._display_list_index = self.create_displaylist_index()

    def set_emissive(self, emissive):
        self._emissive = emissive
        self._display_list_index = self.create_displaylist_index()

    def set_orientation(self, orientation):
        self._body.setRotation(orientation)

    def set_data(self, name, value):
        ''' Sets an attribute of the shape's geom,
            keyword 'name', value 'value' '''
        self._geom.__setattr__(name, value)

    def get_data(self, name):
        return self._geom.__getattribute__(name)

    def create_displaylist_index(self):
        return None

    def draw(self):
        pos = self.get_pos().value
        glTranslatef(pos[0], pos[1], pos[2])
        rotMatrix = self.get_orientation()
        glMultMatrixf(rotMatrix)
        glCallList(self._display_list_index)

    def draw_AABB(self):
        # aabb = self._geom.getAABB()
        # x_size = (aabb[1] - aabb[0])/2.0
        # y_size = (aabb[3] - aabb[2])/2.0
        # z_size = (aabb[5] - aabb[4])/2.0
        # pos = self.get_pos().value
        # glTranslatef(pos[0], pos[1], pos[2])
        # draw.AABB(x_size, y_size, z_size)

        aabb = self._geom.getAABB()
        draw.AABB(aabb)

class Sphere(Shape):

    def __init__(self, world, space, pos = Vector(), radius = 0.5,
                 mass = 1.0, texture = None):
        super(Sphere, self).__init__(world)

        # Set ODE properties
        self._mass.setSphere(1, radius)
        self._mass.adjust(mass)
        self._body.setPosition(pos.value)
        self._body.setMass(self._mass)
        self._geom = ode.GeomSphere(space, radius)
        self._geom.setBody(self._body)

        self._rolling_friction = 0.5

        self.set_data('shape', self)

        self._radius = radius

        self._texture = texture
        self._quadric = gluNewQuadric()

        # Set 'right' side up (to compensate for textures being drawn 'sideways')
        rotation = matrices.OpenGL_to_ODE(matrices.\
                        generate_rotation_matrix(Vector([-1.0, 0.0, 0.0]), math.pi/2.0))

        self.set_orientation(rotation)

        # Material properties
        self._ambient = [1.0, 1.0, 1.0, 1.0]
        self._diffuse = [1.0, 1.0, 1.0, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 64
        self._emissive = [0.0, 0.0, 0.0, 1.0]
        
        self._display_list_index = self.create_displaylist_index()

    def create_displaylist_index(self):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.sphere(self)
        glEndList()
        return display_list_index

    def get_radius(self):
        return self._radius

    def get_quadric(self):
        return self._quadric

    def get_rolling_friction(self):
        return self._rolling_friction

    def set_rolling_friction(self, rolling_friction):
        self._rolling_friction = rolling_friction

class Box(Shape):

    def __init__(self, world, space, pos = Vector(), x_size = 1,
                y_size = 1, z_size = 1, mass = 1, texture = None):
        super(Box, self).__init__(world)

        # Set ODE properties
        self._mass.setBox(1, x_size, y_size, z_size)
        self._mass.adjust(mass)
        self._body.setPosition(pos.value)
        self._body.setMass(self._mass)
        self._geom = ode.GeomBox(space, (x_size, y_size, z_size))
        self._geom.setBody(self._body)

        self._x_size = x_size
        self._y_size = y_size
        self._z_size = z_size

        self.set_data('shape', self)

        self._texture = texture
        
        # Material properties
        self._ambient = [1.0, 1.0, 1.0, 1.0]
        self._diffuse = [1.0, 1.0, 1.0, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 42
        self._emissive = [0.0, 0.0, 0.0, 1.0]
        
        self._display_list_index = self.create_displaylist_index()

    def get_sides(self):
        return self._x_size, self._y_size, self._z_size

    def create_displaylist_index(self):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.box(self)
        glEndList()
        return display_list_index

# NOTE: Necessary? We can delete this class and just use Box instead.
class Cube(Box):

    def __init__(self, world, space, pos = Vector(), side = 1,
                 mass = 1, texture = None):
        super(Cube, self).__init__(world, space, pos = pos, x_size = side,
                y_size = side, z_size = side, mass = mass, texture = texture)

        self._side = side

    def get_side(self):
        return self._side


class Surface(Shape):
    # TODO: Better way of defining the surface. The points at 
    # the corners is not a very good solution. Used as they are
    # right now, it's hard to decide which side is up.

    def __init__(self, world, space, pos = Vector(),
                normal = Vector([0.0, 1.0, 0.0]), 
                forward = Vector([0.0, 0.0, -1.0]),
                length = 1, width = 1, texture = None,
                subdivision_size = 1): #Bigger subdivisions for faster startup when debugging

        # normal: The normal direction
        # forward: The direction in which the surface is 'length' long.
        # length: Size in 'forward' direction.
        # width: Size orthogonal to 'forward' direction
        # subdivision_size: The target for the size of the elements of the tesselated surface.

        super(Surface, self).__init__(world)

        self._normal = normal
        self._forward = forward
        self._length = length
        self._width = width
        self._thickness = 0.1
        self._texture = texture
        self._subdivision_size = subdivision_size

        # Set ODE properties
        self._geom = ode.GeomBox(space, (self._width, self._thickness, self._length))
        self._body = None
        self._geom.setBody(self._body)

        self.set_data('shape', self)

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

        pos = pos - self._normal * self._thickness * 0.5

        self._geom.setPosition(pos.value)
        self._geom.setRotation(rotation)
                
        # Material properties
        self._ambient = [1.0, 1.0, 1.0, 1.0]
        self._diffuse = [1.0, 1.0, 1.0, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 20
        self._emissive = [0.0, 0.0, 0.0, 1.0]

        self._display_list_index = self.create_displaylist_index()

    def create_displaylist_index(self):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.surface(self)
        glEndList()
        return display_list_index

    def get_points(self):
        return self._points

    def get_normal(self, point = Vector()):
        return self._normal

    def get_pos(self):
        return Vector(list(self._geom.getPosition())) + self._normal * self._thickness * 0.5

    def get_orientation(self):
        orientation = matrices.ODE_to_OpenGL(self._geom.getRotation())
        return orientation

    def get_length(self):
        return self._length

    def get_width(self):
        return self._width

    def get_subdivision_size(self):
        return self._subdivision_size

    # def draw_bounding_box(self):

    #     x = self._x/2.0
    #     y = self._y/2.0
    #     z = self._z/2.0

    #     box_points = [[x, -y, -z],  [x, y, -z],
    #                 [-x, y, z],  [-x, -y, -z],
    #                 [x, -y, z],   [x, y, z],
    #                 [-x, -y, z],  [-x, y, z]]

    #     CUBE_EDGES = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    #                 (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))
    #     glPushMatrix()
    #     glMultMatrixf(matrices.ODE_to_OpenGL(self.rotation))

    #     glColor3f(1.0, 1.0, 1.0)    
    #     glBegin(GL_LINES)
    #     for line in CUBE_EDGES:
    #         for vert in line:
    #             glVertex3fv(box_points[vert])
    #     glEnd()
    #     glPopMatrix()
