from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numbers

from math_classes import vectors, quaternions, matrices
from physics_engine import supports
from graphics import draw


# TODO: Right now there is some redundance in the code since the
# create_displaylist_index() functions are almost identical in all
# shapes. However, I find it somewhat ugly to solve this like in
# fluffy, are there any better ways?

class Shape(object):

    def __init__(self):

        # Linear motion
        self._pos = vectors.Vector()
        self._velocity = vectors.Vector()
        self._mass = float('inf')               # Makes it immobile
        self._force = vectors.Vector()          # Not used right now

        # Angular motion
        #self._orientation = quaternions.Quaternion()
        self._orientation = matrices.identity()
        #print 'Made an orientation:', self._orientation
        self._angularVelocity = vectors.Vector()
        self._invInertia = [[0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0]]    # Makes it unable to rotate
        self._torque = vectors.Vector()         # Not used right now

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

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, velocity):
        assert isinstance(velocity, vectors.Vector), 'Velocity must be a vector'
        self._velocity = velocity

    def add_velocity(self, velocity):
        assert isinstance(velocity, vectors.Vector), 'Velocity must be a vector'
        self._velocity += velocity
    
    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        self._pos = pos

    def add_pos(self, pos):
        assert isinstance(pos, vectors.Vector), 'Pos must be a vector'
        self._pos += pos

    def get_angular_velocity(self):
        return self._angularVelocity

    def set_angular_velocity(self, velocity):
        assert isinstance(velocity, vectors.Vector), 'Velocity must be a vector'
        self._angularVelocity = velocity

    def add_angular_velocity(self, velocity):
        assert isinstance(velocity, vectors.Vector), 'Velocity must be a vector'
        self._angularVelocity += velocity

    def get_orientation(self):
        #print 'get_orientation', self._orientation
        return self._orientation

    def set_orientation(self, orientation):
        #assert isinstance(orientation, quaternions.Quaternion), \
        #       'Input must be a quaternion'
        #assert orientation.is_unit(), \
        #       'Input must be a quaternion of unit length'
        assert isinstance(orientation, list), 'Input must be a matrix'
        assert len(orientation) == 16, 'Input must be a 4x4 matrix'
        if __debug__:
            for item in orientation:
                assert isinstance(item, numbers.Number),\
                       'All elements in the matrix must be numbers'
        #print 'set_orientation before', self._orientation
        self._orientation = orientation
        #print 'set_orientation after', self._orientation
        

    def add_orientation(self, orientation):
        #assert isinstance(orientation, quaternions.Quaternion), \
        #       'Input must be a quaternion'
        #assert orientation.is_unit(), \
        #       'Input must be a quaternion of unit length'
        assert isinstance(orientation, list), 'Input must be a matrix'
        assert len(orientation) == 16, 'Input must be a 4x4 matrix'
        if __debug__:
            for item in orientation:
                assert isinstance(item, numbers.Number),\
                       'All elements in the matrix must be numbers'
        self._orientation = matrices.matrix_mult(orientation, self._orientation)

        #print 'add_orientation before', self._orientation
        #self._orientation = orientation * self._orientation
        #print 'add_orientation middle', self._orientation
        #self._orientation = self._orientation.check_normalize()
        #print 'add_orientation after', self._orientation

    def get_mass(self):
        return self._mass

    def set_mass(self, mass):
        assert isinstance(mass, numbers.Number), 'Mass must be a number'
        assert mass >= 0, 'Mass must be at least 0'
        self._mass = mass

    def get_invInertia(self):
        return self._invInertia

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

    def __init__(self, pos = vectors.Vector(), radius = 0.5,
                 mass = 1.0, color = [1.0, 0.5, 0.3]):
        super(Sphere, self).__init__()
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
                
        self._pos = pos
        self._mass = mass
        self._radius = radius
        self._color = color
        I = 5/(2*self._mass*self._radius*self._radius)
        self._invInertia = [[I, 0.0, 0.0],
                            [0.0, I, 0.0],
                            [0.0, 0.0, I]]

        # Material properties
        self._ambient = [1.0, 0.5, 0.3, 1.0]
        self._diffuse = [1.0, 0.5, 0.3, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 64
        #self._emissive = [0.0, 0.0, 0.0, 1.0]
        
        self._displayListIndex = self.create_displaylist_index()
        #self._orientation = quaternions.axis_angle_to_quat(Vector([1.0, 0.0, 0.0]), 0.0)
        #self._orientation = quaternions.Quaternion([1.0, 0.0, 0.0, 0.0]) #This is equivalent, maybe better?

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

    def __init__(self, pos = vectors.Vector(), side = 1,
                 mass = 1, color = [0.8, 0.8, 0.8]):
        super(Cube, self).__init__()
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

        self._pos = pos
        self._side = side
        self._mass = mass
        self._color = color
        
        # Material properties
        self._ambient = [0.8, 0.8, 0.8, 1.0]
        self._diffuse = [0.8, 0.8, 0.8, 1.0]
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

    def support_func(self, direction):
        #return supports.cube(self, direction)
        return supports.polyhedron(self, direction)

    def get_side(self):
        return self._side

    def get_bounding_radius(self):
        ''' Returns a radius that encapsules the cube, slightly
            bigger than the distance from the center to a corner.'''
        return self._side

    def get_points(self):
        h = self._side/2.0
        return [vectors.Vector([h, -h, -h]),  vectors.Vector([h, h, -h]),
                vectors.Vector([-h, h, -h]),  vectors.Vector([-h, -h, -h]),
                vectors.Vector([h, -h, h]),   vectors.Vector([h, h, h]),
                vectors.Vector([-h, -h, h]),  vectors.Vector([-h, h, h])]

    def get_normal(self, point):
        ''' Returns the normal of the cube in th given point. Assumes the point
            lies inside of the cube. '''
        assert isinstance(point, vectors.Vector), 'Input must be a vector'

        dist = point - self._pos
        halfside = self._side/2.0

        xdot = dist.dot(vectors.Vector([1.0, 0.0, 0.0]))
        ydot = dist.dot(vectors.Vector([0.0, 1.0, 0.0]))
        zdot = dist.dot(vectors.Vector([0.0, 0.0, 1.0]))

        xdist = halfside - abs(xdot)
        ydist = halfside - abs(ydot)
        zdist = halfside - abs(zdot)

        distlist = [xdist, ydist, zdist]

        # Calculates which pair of faces is closest to the point
        index = distlist.index(min(distlist))

        if index == 0:
            if xdot > 0:
                return vectors.Vector([1.0, 0.0, 0.0])
            else:
                return vectors.Vector([-1.0, 0.0, 0.0])
        elif index == 1:
            if ydot > 0:
                return vectors.Vector([0.0, 1.0, 0.0])
            else:
                return vectors.Vector([0.0, -1.0, 0.0])
        else:
            if zdot > 0:
                return vectors.Vector([0.0, 0.0, 1.0])
            else:
                return vectors.Vector([0.0, 0.0, -1.0])

    def draw(self):
        glCallList(self._displayListIndex)


class Surface(Shape):

    def __init__(self, pos = vectors.Vector(),
                 points = [vectors.Vector([-5.0, 0.0, -5.0]), vectors.Vector([5.0, 0.0, -5.0]),
                           vectors.Vector([5.0, 0.0, 5.0]), vectors.Vector([-5.0, 0.0, 5.0])],
                 color = [1.0, 0.0, 1.0]):
        super(Surface, self).__init__()
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

        self._pos = pos
        self._points = points
        self._color = color
                
        # Material properties
        self._ambient = [1.0, 0.0, 1.0, 1.0]
        self._diffuse = [1.0, 0.0, 1.0, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 80
        #self._emissive = [0.0, 0.0, 0.0, 1.0]
        
        self._normal = (points[0] - points[1]).cross(points[3] - points[1]).normalize()
        self._displayListIndex = self.create_displaylist_index()

    def create_displaylist_index(self):
        displayListIndex = glGenLists(1)
        glNewList(displayListIndex, GL_COMPILE)
        draw.surface(self)
        glEndList()
        return displayListIndex

    def support_func(self, direction):
        return supports.polyhedron(self, direction)

    def get_points(self):
        return self._points

    def get_normal(self, point = vectors.Vector()):
        return self._normal

    def draw(self):
        glCallList(self._displayListIndex)
