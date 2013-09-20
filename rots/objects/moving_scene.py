from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

from math import sin, cos, pi, asin, acos

from math_classes import matrices
from math_classes.vectors import Vector
from graphics import draw, textures
from sound import sound_effects

# TODO: Make the 'moving time' be a number in seconds
# instead of frames, for example by using the current fps.

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

        self._AABB_color = (0.0, 0.0, 1.0, 1.0)

        self._friction = 1
        self._bounce = 0.2

        self._velocity = Vector()

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

    def get_velocity(self):
        return self._velocity

    def get_AABB_color(self):
        return self._AABB_color

    def set_AABB_color(self, color):
        self._AABB_color = color

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
        color = self._AABB_color
        draw.AABB(aabb, color)

    def update(self):
        pass

class Sliding_door(Moving_scene):
    ''' A class for sliding doors. '''

    def __init__(self, space, pos = Vector(), normal = Vector((0.0, 1.0, 0.0)), 
                slide_dir = Vector((1.0, 0.0, 0.0)), slide_size = 5,
                ort_size = 5, thickness = 0.5, texture = None,
                opening_time = 30, subdivision_size = 1):

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
        self._subdivision_size = subdivision_size

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

        # Check if it should be toggling
        if self._toggling:
            # Check in which state it is
            if self._open:
                # It is open, close it
                self._opening_counter += 1
                self._pos = self._closed_pos + self._slide_dir * \
                            (1 + cos(pi * (float(self._opening_counter)/self._opening_time))) \
                            * self._slide_size * 0.5

                self._velocity = self._slide_dir * \
                        -sin(pi * (float(self._opening_counter)/self._opening_time)) * \
                                self._slide_size * 0.5

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

                self._velocity = self._slide_dir * \
                    cos(pi * (((float(self._opening_counter)/self._opening_time)) - 0.5)) * \
                        self._slide_size * 0.5

                # Check if it is open
                if self._opening_counter == self._opening_time:
                    self._opening_counter = 0
                    self._toggling = False
                    self._open = True
        else:
            # Isn't toggling, therefore not moving
            self._velocity = Vector()

        self._geom.setPosition(self._pos.value)

    def toggle(self):
        ''' Toggles the door: Opens it if it is closed and vice versa.
            If the door is currently closing/opening, it does nothing. '''

        if not self._toggling:
            self._toggling = True
            self._slide_sound.play()

    def open(self):
        ''' Opens the door. If it is already open the call is ignored. '''

        if not self._open and not self._toggling:
            self._toggling = True

    def close(self):
        ''' Closes the door. If it is already closed the call is ignored. '''

        if self._open and not self._toggling:
            self._toggling = True

    def get_sides(self):
        return self._ort_size, self._thickness, self._slide_size

    def get_subdivision_size(self):
        return self._subdivision_size

    def create_displaylist_index(self):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.box(self)
        glEndList()
        return display_list_index

class Moving_platform(Moving_scene):

    # TODO: There are some odd effects when using the platform:
    # the player starts bouncing and sliding. Fix this.

    def __init__(self, space, normal = Vector((0.0, 1.0, 0.0)), 
                forward = Vector((1.0, 0.0, 0.0)),
                width = 5, length = 5, thickness = 0.5, texture = None,
                move_time = 480, turning_points = (Vector((0.0, 2.0, 0.0)), Vector((0.0, 10.0, 0.0))),
                subdivision_size = 1):

        super(Moving_platform, self).__init__()

        # Set ODE properties
        self._space = space
        self._geom = ode.GeomBox(self._space, (width, thickness, length))
        self._body = None
        self._geom.setBody(self._body)

        self._normal = normal
        self._forward = forward
        self._width = width
        self._thickness = thickness
        self._length = length
        self._texture = texture
        self._move_time = move_time
        self._counter = 0
        self._turning_points = turning_points
        self._move_dist = (turning_points[1] - turning_points[0]).norm() / 2.0
        self._move_dir = (turning_points[1] - turning_points[0]).normalize()
        self._middle_point = (turning_points[1] + turning_points[0]) * 0.5
        self._pos = self._middle_point
        self._subdivision_size = subdivision_size

        self._bounce = 0.0

        # Calculate the rotation matrix in the first direction needed to align the 
        # bounding box with the object
        axis = Vector([0.0, 1.0, 0.0]).cross(self._normal)
        if axis.norm() < 0.1:
            #Parallel
            axis = Vector([0.0, 0.0, 1.0])
        angle1 = acos(Vector([0.0, 1.0, 0.0]).dot(self._normal))
        rotation1 = matrices.generate_rotation_matrix(axis, angle1)

        # Calculate the second rotation matrix
        angle2 = asin(Vector([0.0, 0.0, 1.0]).cross(self._forward).norm())
        rotation2 = matrices.generate_rotation_matrix(self._normal, angle2)

        # Combine the two rotations
        rotation = matrices.OpenGL_to_ODE(matrices.matrix_mult(rotation2, rotation1))

        self._geom.setPosition(self._middle_point.value)
        self._geom.setRotation(rotation)

        self._ambient = [0.0, 1.0, 0.2, 1.0]
        self._diffuse = [0.0, 1.0, 0.2, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 10
        self._emissive = [0.0, 0.0, 0.0, 1.0]

        self._display_list_index = self.create_displaylist_index()

        self.set_data('object', self)

    def get_sides(self):
        return self._width, self._thickness, self._length

    def get_subdivision_size(self):
        return self._subdivision_size

    def create_displaylist_index(self):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.box(self)
        glEndList()
        return display_list_index

    def update(self):

        old_pos = self._pos

        self._pos = self._middle_point + self._move_dir * \
                    sin(pi * self._counter / self._move_time) * \
                    self._move_dist * -1.0

        # NOTE: Something wrong here...
        #self._velocity =  self._move_dir * \
        #        cos(pi * self._counter / self._move_time) * \
        #                    self._move_dist * -1.0

        #curr_vel = (self._pos - old_pos) * 60

        self._velocity = (self._pos - old_pos) * 60

        # try:
        #     error_factor = self._velocity.norm()/curr_vel.norm()
        # except ZeroDivisionError:
        #     print 'Division by zero'
        #     error_factor = None

        # print 'Pos: ', self._pos
        # print 'Vel: ', self._velocity
        # print 'Vel (should be): ', curr_vel
        # print 'Error factor: ', error_factor
        # print

        self._geom.setPosition(self._pos.value)

        self._counter += 1

        if self._counter >= self._move_time * 2:
            self._counter = 0
