import pygame
from pygame.locals import *

import shapes
import players
from graphics import lights
from math_classes.vectors import Vector
from text import TextBox

# TODO: Change the surface class so that we can make objectlist and scenelist to one list
# TODO: Add a variable to the Shape class "self.moveable"; if true it sets self.geom.setBody(None)

class Game():
    ''' A class containing all the objects in the game '''
    def __init__(self, world, space, player, objectList, lightList, camera, clock, debug = False):
        # TODO: Use the Player object from fluffy instead?

        self._world = world
        self._space = space
        self._player = player
        self._objectList = objectList
        self._lightList = lightList
        self._camera = camera
        self._clock = clock
        self._debug = debug

        self._jumped_last_frame = False
        self._toggle_debug_last_frame = False
        # TODO: This should describe the game object in
        # the saved state files (levels):
        # Player = Profile + associated shape
        # objectList, sceneList
        # lighting objects
        # level constants (gravity etc), hashmap

        # TODO: Add more things to the debug screen, move textboxes to better positions
        # (perhaps use pygame.display.Info().current_w /-h to put the text relative
        # the screen's border?)
        
        # Performance
        self._debug_fps = TextBox('test.ttf', 14, 100, 150, [1,0,0], enabled = False)
        self._debug_time_used = TextBox('test.ttf', 14, 100, 100, [1,0,0], enabled = False)
        
        # Player properties
        self._debug_player_pos = TextBox('test.ttf', 14, 100, 350, [1,0,0], enabled = False)
        self._debug_player_vel = TextBox('test.ttf', 14, 100, 300, [1,0,0], enabled = False)
        self._debug_player_colliding = TextBox('test.ttf', 14, 100, 250, [1,0,0], enabled = False)

        self._debugList = [self._debug_fps, self._debug_time_used, self._debug_player_pos, self._debug_player_vel,
                            self._debug_player_colliding]

        self._objectList += self._debugList

    def get_debug(self):
        return self._debug

    def toggle_debug(self):
        self._debug = not self._debug
        for item in self._debugList:
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
        return self._world, self._space, self._player, self._objectList, \
               self._lightList, self._camera


    def take_input(self):
        current_events = pygame.event.get() # cache current events
        run = True
        for event in current_events:
            if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False
        key_state = pygame.key.get_pressed()

        xDir = key_state[K_d] - key_state[K_a]
        zDir = key_state[K_s] - key_state[K_w]

        if key_state[K_SPACE] and self._player.colliding and not self._jumped_last_frame:
            jump = True
            self._jumped_last_frame = True
        elif not key_state[K_SPACE]:
            self._jumped_last_frame = False
            jump = False
        else:
            jump = False

        if key_state[K_q] and not self._toggle_debug_last_frame:
            toggle_debug = True
            self._toggle_debug_last_frame = True
        elif not key_state[K_q]:
            toggle_debug = False
            self._toggle_debug_last_frame = False
        else:
            toggle_debug = False

        direction = Vector([xDir, 0.0, zDir]).normalize()
        if not direction:
            direction = Vector()

        return run, direction, jump, toggle_debug
