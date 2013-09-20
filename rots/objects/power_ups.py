from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

from math import sin, pi
from random import randrange

from math_classes import matrices
from math_classes.vectors import Vector
from graphics import draw, textures
from sound import sound_effects
import shapes

class Power_up(object):
    ''' Base class for all power ups '''

    def __init__(self):
        # TODO: Put more things here, all the things that
        # are common for all power ups.

        self._geom = None

        self._ambient = None
        self._diffuse = None
        self._specular = None
        self._shininess = None
        self._emissive = None

        self._texture = None

        self._display_list_index = None

        self._collided = False
        self._activation_sound = None

        self._AABB_color = (0.0, 1.0, 0.0, 1.0)

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

    def get_collided(self):
        return self._collided

    def get_AABB_color(self):
        return self._AABB_color

    def set_AABB_color(self, color):
        self._AABB_color = color

    def set_collided(self, collided):
        self._collided = collided

    def draw(self):
        pos = self.get_pos().value
        glTranslatef(pos[0], pos[1], pos[2])
        rotMatrix = self.get_orientation()
        glMultMatrixf(rotMatrix)
        glCallList(self._display_list_index)

    def collide_func(self, game):
        ''' The function that is called whe the player
            collides with the power up '''
        pass

    def kill(self, game):
        object_list = game.get_object_list()
        object_list.remove(self)
        self._space.remove(self._geom)
        del self

    def set_data(self, name, value):
        ''' Sets an attribute of the power up's geom,
            keyword 'name', value 'value' '''
        self._geom.__setattr__(name, value)

    def draw_AABB(self):
        aabb = self._geom.getAABB()
        color = self._AABB_color
        draw.AABB(aabb, color)

class Gravity_flipper(Power_up):
    ''' A class of power ups that flip the world's
        gravity upside down '''

    def __init__(self, space, pos):

        super(Gravity_flipper, self).__init__()
        self._radius = 0.5
        self._space = space
        self._geom = ode.GeomBox(self._space, (self._radius * 2, self._radius * 4, 
                                            self._radius * 2))
        self._geom.setBody(None)
        self._geom.setPosition(pos.value)

        self._texture = textures.load_texture('arrows_3.png')
        self._quadric = gluNewQuadric()

        self._draw_pos = self.get_pos()
        # To compensate for the texture being drawn 'sideways'
        self._draw_orientation = matrices.\
                generate_rotation_matrix(Vector([-1.0, 0.0, 0.0]),
                                                pi/2.0)
        self._oscillation_angle = 0
        self._oscillation_amplitude = self._radius

        self._ambient = [1.0, 1.0, 1.0, 1.0]
        self._diffuse = [1.0, 1.0, 1.0, 1.0]
        self._specular = [1.0, 1.0, 1.0, 1.0]
        self._shininess = 0
        self._emissive = [1.0, 1.0, 1.0, 1.0]

        self._activation_sound = sound_effects.load_sound('fall_2.wav')

        self._display_list_index = self.create_displaylist_index()

        self.set_data('object', self)

    def get_radius(self):
        return self._radius

    def get_quadric(self):
        return self._quadric

    def create_displaylist_index(self):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.sphere(self)
        glEndList()
        return display_list_index

    def draw(self):
        pos = (self.get_pos() + Vector([0.0, 1.0, 0.0]) * \
                    sin(self._oscillation_angle) * self._oscillation_amplitude).value
        glTranslatef(pos[0], pos[1], pos[2])
        rotMatrix = self.get_orientation()
        glMultMatrixf(self._draw_orientation)
        glMultMatrixf(rotMatrix)
        glCallList(self._display_list_index)

        self._oscillation_angle += pi * 0.02
        if self._oscillation_angle <= 2 * pi:
            self._oscillation_angle -= 2 * pi

    def collide_func(self, game):
        ''' The function that is called whe the player
            collides with the power up '''

        # TODO: There is a bug when using the power up 
        # causing all AABBs to become white. It is resolved
        # by pressing the button that creates a new sphere.
        # What is causing this bug? Fix it.

        self._activation_sound.play()
        world = game.get_world()
        camera = game.get_camera()
        object_list = game.get_object_list()
        player = game.get_player()

        up = camera.get_up()

        new_grav = Vector(world.getGravity()) * -1.0

        world.setGravity(new_grav.value)

        camera.flip_y_dist()

        player.set_jump_constant(player.get_jump_constant() * -1.0)
        
        new_power_pos = Vector((randrange(-14, 14), 8.0, randrange(-14, 14))) \
                                    + new_grav.normalize() * 6.0
        new_power_up = Gravity_flipper(self._space, new_power_pos)
        object_list.append(new_power_up)

        # Make sure all objects are enabled
        for item in object_list:
            if isinstance(item, shapes.Shape) and item.get_body():
                # It is a Shape object with a body
                item.get_body().enable()

        self.kill(game)


class World_flipper(Gravity_flipper):
    ''' A class of power ups that flip the entire world
        upside down '''

        # TODO: There is a bug when using the power up 
        # causing all AABBs to become white. It is resolved
        # by pressing the button that creates a new sphere.
        # What is causing this bug? Fix it.

    def __init__(self, space, pos):

        super(World_flipper, self).__init__(space, pos)

        self._texture = textures.load_texture('arrows_1.png')
        self._activation_sound = sound_effects.load_sound('brown_2.wav')
        self._display_list_index = self.create_displaylist_index()

    def collide_func(self, game):
        ''' The function that is called whe the player
            collides with the power up '''

        self._activation_sound.play()
        world = game.get_world()
        camera = game.get_camera()
        object_list = game.get_object_list()
        player = game.get_player()

        up = camera.get_up()

        new_grav = Vector(world.getGravity()) * -1.0

        world.setGravity(new_grav.value)

        camera.flip_up_vector()

        player.set_up_dir(up * -1.0)
        
        new_power_pos = Vector((randrange(-14, 14), 8.0, randrange(-14, 14))) + up * 6.0
        new_power_up = World_flipper(self._space, new_power_pos)
        object_list.append(new_power_up)

        # Make sure all objects are enabled
        for item in object_list:
            if isinstance(item, shapes.Shape) and item.get_body():
                # It is a Shape object with a body
                item.get_body().enable()

        self.kill(game)
