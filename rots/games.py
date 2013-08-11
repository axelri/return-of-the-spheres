import pygame
from pygame.locals import *

import shapes
import players
from graphics import lights
from math_classes.vectors import Vector
from text import TextBox

# TODO: Add a variable to the Shape class "self.moveable"; if true it sets self.geom.setBody(None)

class Game():
    ''' A class containing all the objects in the game '''
    def __init__(self, world, space, player, object_list, light_list, camera, clock, contactgroup, debug = False):
        # TODO: Use the Player object from fluffy instead?

        self._world = world
        self._space = space
        self._player = player
        self._object_list = object_list
        self._light_list = light_list
        self._camera = camera
        self._clock = clock
        self._contactgroup = contactgroup
        self._debug = debug

        self._keys_pressed = None
        self._keys_pressed_last_frame = None

        self._constants = {}

        # TODO: This should describe the game object in
        # the saved state files (levels):
        # Player = Profile + associated shape
        # object_list, sceneList
        # lighting objects
        # level constants (gravity etc), hashmap

        # TODO: Add more things to the debug screen, move textboxes to better positions
        # (perhaps use pygame.display.Info().current_w /-h to put the text relative
        # the screen's border?)

        # Debug screen textboxes
        
        # Performance
        self._debug_fps = TextBox('test.ttf', 14, 100, 150, [1,0,0], enabled = False)
        self._debug_time_used = TextBox('test.ttf', 14, 100, 100, [1,0,0], enabled = False)
        
        # Player properties
        self._debug_player_pos = TextBox('test.ttf', 14, 100, 350, [1,0,0], enabled = False)
        self._debug_player_vel = TextBox('test.ttf', 14, 100, 300, [1,0,0], enabled = False)
        self._debug_player_colliding = TextBox('test.ttf', 14, 100, 250, [1,0,0], enabled = False)


        self._debug_list = [self._debug_fps, self._debug_time_used, self._debug_player_pos, self._debug_player_vel,
                            self._debug_player_colliding]

        self._object_list += self._debug_list

    def toggle_debug(self):
        self._debug = not self._debug
        for item in self._debug_list:
            item.toggle()

    def update_debug_screen(self):
        # Performance

        self._debug_fps.set_string("FPS: %0.2f" % self._clock.get_fps())
        self._debug_time_used.set_string("Time used last frame [ms]: %d" % self._clock.get_rawtime())
        
        # Player properties
        self._debug_player_pos.set_string("Player pos: [%0.2f, %0.2f, %0.2f]" % self._player.get_pos().value)
        self._debug_player_vel.set_string("Player vel: [%0.2f, %0.2f, %0.2f]" % self._player.get_vel().value)
        self._debug_player_colliding.set_string("Player colliding: %s" % self._player.colliding)

    def get_objects(self):
        return self._world, self._space, self._player, self._object_list, \
               self._light_list, self._camera

    def get_world(self):
        return self._world

    def get_space(self):
        return self._space

    def get_player(self):
        return self._player

    def get_object_list(self):
        return self._object_list

    def get_light_list(self):
        return self._light_list

    def get_camera(self):
        return self._camera

    def get_clock(self):
        return self._clock

    def get_contactgroup(self):
        return self._contactgroup

    def get_constants(self):
        return self._constants

    def get_debug(self):
        return self._debug

    def add_constant(self, key, value):
        self._constants[key] = value


    def take_input(self):
        current_events = pygame.event.get() # cache current events
        run = True
        for event in current_events:
            if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False
        self._keys_pressed = pygame.key.get_pressed()

        # The direction

        xDir = self._keys_pressed[K_d] - self._keys_pressed[K_a]
        zDir = self._keys_pressed[K_s] - self._keys_pressed[K_w]

        direction = Vector([xDir, 0.0, zDir]).normalize()
        if not direction:
            direction = Vector()

        # Jumping

        if self._keys_pressed[K_SPACE] and self._player.colliding and not self._keys_pressed_last_frame[K_SPACE]:
            jump = True
        else:
            jump = False

        # Toggle debug

        if self._keys_pressed[K_q] and not self._keys_pressed_last_frame[K_q]:
            toggle_debug = True
        else:
            toggle_debug = False

        # Toggle pause

        if self._keys_pressed[K_p] and not self._keys_pressed_last_frame[K_p]:
            toggle_pause = True
        else:
            toggle_pause = False


        self._keys_pressed_last_frame = self._keys_pressed

        return run, direction, jump, toggle_debug, toggle_pause
