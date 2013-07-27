from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import numbers
import math

from math_classes import vectors, quaternions, matrices
from graphics import draw


# TODO: Right now there is some redundance in the code since the
# create_displaylist_index() functions are almost identical in all
# shapes. However, I find it somewhat ugly to solve this like in
# fluffy, are there any better ways?

class Shape(object):

    def __init__(self, world):

        # Set ODE properties
        self.body = ode.Body(world)
        self.mass = ode.Mass()
        # Moved to subclasses
        #self.body.setMass(self.mass)

        self._color = None      # Should be removed when material properties
                                # work properly

        # Material properties
        self._ambient = None
        self._diffuse = None
        self._specular = None
        self._shininess = None
        #self._emissive = None

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

    # NOTE: Function names kept in case we want to build a better API

    # def get_velocity(self):

    # def set_velocity(self, velocity):

    # def add_velocity(self, velocity):

    def get_pos(self):
        return vectors.Vector(list(self.body.getPosition()))

    # def set_pos(self, pos):

    # def add_pos(self, pos):

    # def get_angular_velocity(self):

    # def set_angular_velocity(self, velocity):

    # def add_angular_velocity(self, velocity):

    def get_orientation(self):
        orientation = matrices.ODE_to_OpenGL(self.body.getRotation())
        return orientation

    # def set_orientation(self, orientation):

    # def add_orientation(self, orientation):

    # def get_mass(self):

    # def set_mass(self, mass):

    # def get_invInertia(self):

    def get_color(self):
        return self._color

    def set_color(self, color):
        assert isinstance(color, list), 'Color must be a list'
        # NOTE: If we use alpha values this should be 4
        assert len(color) == 3, 'Color must be of length 3' 
        if __debug__:
            for item in color:
                assert isinstance(item, numbers.Number), \
                       'Every component of color must be a number'
                assert 0 <= item <= 1, \
                       'Every component of color must be a number between 0 and 1'
        self._color = color

    def get_material_properties(self):
        return self._ambient, self._diffuse, self._specular,\
               self._shininess#, self._emissive

class Sphere(Shape):

    def __init__(self, world, space, pos = vectors.Vector(), radius = 0.5,
                 mass = 1.0, color = [1.0, 0.5, 0.3], texture = None):
        super(Sphere, self).__init__(world)
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        assert isinstance(mass, numbers.Number), 'Mass must be a number'
        assert mass >= 0, 'Mass must be at least 0'
        assert isinstance(radius, numbers.Number), 'Radius must be a number'
        assert radius >= 0, 'Radius must be at least 0'
        assert isinstance(color, list), 'Color must be a list'
        # NOTE: If we use alpha values this should be 4
        assert len(color) == 3, 'Color must be of length 3'
        if __debug__:
            for item in color:
                assert isinstance(item, numbers.Number), \
                       'Every component of color must be a number'
                assert 0 <= item <= 1, \
                       'Every component of color must be a number between 0 and 1'
        # Set ODE properties

        self.mass.setSphere(1, radius)
        self.mass.adjust(mass)
        self.body.setPosition(pos.value)
        self.body.setMass(self.mass)
        self.geom = ode.GeomSphere(space, radius)
        self.geom.setBody(self.body)

#        self._pos = pos
#        self._mass = mass
        self._radius = radius

        self._color = color
        self._texture = texture
        self._quadric = gluNewQuadric()

        # Material properties
        self._ambient = self._color + [1.0] #[1.0, 0.5, 0.3, 1.0]
        #self._ambient = [0.0, 1.0, 0.0, 1.0]
        self._diffuse = self._color + [1.0] #[1.0, 0.5, 0.3, 1.0]
        #self._diffuse = [1.0, 0.0, 0.0, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 64
        #self._emissive = [0.0, 0.0, 0.0, 1.0]
        
        self._displayListIndex = self.create_displaylist_index()

    def create_displaylist_index(self):
        displayListIndex = glGenLists(1)
        glNewList(displayListIndex, GL_COMPILE)
        draw.sphere(self)
        glEndList()
        return displayListIndex

    def support_func(self, direction):
        return supports.sphere(self, direction)

    def get_normal(self, point):
        ''' Returns the normal of the sphere in the given point '''
        assert isinstance(point, vectors.Vector), 'Input must be a vector'
        return (point - self._pos).normalize()

    def get_radius(self):
        return self._radius

    def get_bounding_radius(self):
        ''' Returns a radius that encapsules the sphere, slightly
            bigger than the sphere's radius.'''
        return self._radius*1.1

    def draw(self):
        glCallList(self._displayListIndex)

        
class Cube(Shape):

    def __init__(self, world, space, pos = vectors.Vector(), side = 1,
                 mass = 1, color = [0.8, 0.8, 0.8]):
        super(Cube, self).__init__(world)
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        assert isinstance(mass, numbers.Number), 'Mass must be a number'
        assert mass >= 0, 'Mass must be at least 0'
        assert isinstance(side, numbers.Number), 'Side must be a number'
        assert side > 0, 'Side must be greater than 0'
        assert isinstance(color, list), 'Color must be a list'
        # NOTE: If we use alpha values this should be 4
        assert len(color) == 3, 'Color must be of length 3'
        if __debug__:
            for item in color:
                assert isinstance(item, numbers.Number), \
                       'Every component of color must be a number'
                assert 0 <= item <= 1, \
                       'Every component of color must be a number between 0 and 1'

        # Set ODE properties
        self.mass.setBox(1, side, side, side)
        self.mass.adjust(mass)
        self.body.setPosition(pos.value)
        self.body.setMass(self.mass)
        self.geom = ode.GeomBox(space, (side, side, side))
        self.geom.setBody(self.body)

#        self._pos = pos
        self._side = side
#        self._mass = mass
        self._color = color
        
        # Material properties
        self._ambient = self._color + [1.0] #[0.8, 0.8, 0.8, 1.0]
        self._diffuse = self._color + [1.0] #[0.8, 0.8, 0.8, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 42
        #self._emissive = [0.0, 0.0, 0.0, 1.0]
        
        self._displayListIndex = self.create_displaylist_index()

    def create_displaylist_index(self):
        displayListIndex = glGenLists(1)
        glNewList(displayListIndex, GL_COMPILE)
        draw.cube(self)
        glEndList()
        return displayListIndex

    def get_side(self):
        return self._side

    def draw(self):
        glCallList(self._displayListIndex)


class Surface(Shape):

    def __init__(self, world, space, pos = vectors.Vector(),
                 points = [vectors.Vector([-5.0, 0.0, -5.0]), vectors.Vector([5.0, 0.0, -5.0]),
                           vectors.Vector([5.0, 0.0, 5.0]), vectors.Vector([-5.0, 0.0, 5.0])],
                 color = [1.0, 0.0, 1.0], texture = None):
        super(Surface, self).__init__(world)
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        assert isinstance(color, list), 'Color must be a list'
        # NOTE: If we use alpha values this should be 4
        assert len(color) == 3, 'Color must be of length 3'
        if __debug__:
            for item in color:
                assert isinstance(item, numbers.Number), \
                       'Every component of color must be a number'
                assert 0 <= item <= 1, \
                       'Every component of color must be a number between 0 and 1'
        assert isinstance(points, list), 'Points must be a list'
        assert len(points) == 4, 'Points must be of length 4'
        if __debug__:
            for point in points:
                assert isinstance(point, vectors.Vector), \
                       'Every component of points must be a vector'

        # Set ODE properties
        x_side = (points[1] - points[0]).norm()
        y_side = 0.1
        z_side = (points[3] - points[0]).norm()
        self.geom = ode.GeomBox(space, (x_side, y_side, z_side))
        self.body = None
        self.geom.setBody(self.body)
        print "New surface"
        print "\tpoints:"
        for point in points:
            print "\t\t", point
        normal = (points[0] - points[1]).cross(points[3] - points[1]).normalize()
        axis = vectors.Vector([0.0, 1.0, 0.0]).cross(normal)
        print "\taxis: ", axis
        if axis.norm() < 0.1:
            #Parallel
            axis = vectors.Vector([0.0, 0.0, 1.0])
            print "\taxis changed; new value: ", axis
        angle = math.acos(vectors.Vector([0.0, 1.0, 0.0]).dot(normal))
        print "\tangle: ", angle
        rotation = matrices.OpenGL_to_ODE(
                    matrices.generate_rotation_matrix(axis, angle))
        print "\trotation: ", rotation

        print ""

        self.geom.setPosition(pos.value)
        self.geom.setRotation(rotation)

        #self._pos = pos
        self._points = points
        self._color = color
        self._texture = texture
        # ugly, any solution?
        self._texCoords = ((0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0))
                
        # Material properties
        self._ambient = self._color + [1.0] #[1.0, 0.0, 1.0, 1.0]
        self._diffuse = self._color + [1.0] #[1.0, 0.0, 1.0, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 80
        #self._emissive = [0.0, 0.0, 0.0, 1.0]
        
        self._normal = normal
        self._displayListIndex = self.create_displaylist_index()

    def create_displaylist_index(self):
        displayListIndex = glGenLists(1)
        glNewList(displayListIndex, GL_COMPILE)
        draw.surface(self)
        glEndList()
        return displayListIndex

    def get_points(self):
        return self._points

    def get_normal(self, point = vectors.Vector()):
        return self._normal

    def get_pos(self):
        return vectors.Vector(list(self.geom.getPosition()))

    def get_orientation(self):
        orientation = matrices.ODE_to_OpenGL(self.geom.getRotation())
        return orientation

    def draw(self):
        glCallList(self._displayListIndex)
