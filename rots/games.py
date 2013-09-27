import pygame
from pygame.locals import *

import players
from graphics import lights
from math_classes.vectors import Vector
from objects import shapes
from objects.text import TextBox

# TODO: Add a variable to the Shape class "self.moveable"; 
# if true it sets self.geom.setBody(None)

class Game():
    ''' A class containing all the objects in the game '''
    def __init__(self, world, spaces, player, 
                object_list, light_list, camera, clock, 
                contact_group, fps, debug_state = 0):
        
        sphere_space, object_space, static_space, power_up_space, \
                interactive_object_space, moving_scene_space = spaces

        self._world = world
        self._sphere_space = sphere_space
        self._object_space = object_space
        self._static_space = static_space
        self._power_up_space = power_up_space
        self._interactive_object_space = interactive_object_space
        self._moving_scene_space = moving_scene_space
        self._player = player
        self._object_list = object_list
        self._light_list = light_list
        self._camera = camera
        self._clock = clock
        self._contact_group = contact_group
        self._fps = fps
        self._dt = 1/float(fps)
        self._debug_state = debug_state

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
        ''' Toggle the debug state. There are three debug states:
            0, 1 and 2. This function toggles from the current
            state to the next (0 -> 1, 1 -> 2, 2 -> 0).
            0 means 'no debug', 1 means 'only debug screen'
            and 2 means 'both debug screen and drawn AABBs' '''

        self._debug_state = (self._debug_state + 1) % 3
        if self._debug_state == 0 or self._debug_state == 1:
            for item in self._debug_list:
                item.toggle()

    def update_debug_screen(self):
        ''' Updates the debug screen. Gets the data to be 
            displayed on the debug screen and adds that data 
            to the textboxes in the debug screen. '''

        # Performance

        self._debug_fps.set_string("FPS: %0.2f" % self._clock.get_fps())
        self._debug_time_used.set_string("Time used last frame [ms]: %d" % self._clock.get_rawtime())
        
        # Player properties
        self._debug_player_pos.set_string("Player pos: [%0.2f, %0.2f, %0.2f]" % self._player.get_pos().value)
        self._debug_player_vel.set_string("Player vel: [%0.2f, %0.2f, %0.2f]" % self._player.get_vel().value)
        self._debug_player_colliding.set_string("Player colliding: %s" % self._player.colliding)



    def take_input(self):
        ''' Take input from the keyboard and translates
            that to "game commands".

            Output:
                * run:  
                    A boolean telling whether the game should
                    keep running or be shut down. 
                    - True = keep running, False = shut down
                * direction: 
                    A unit Vector describing the direction that 
                    the player should move in, given in 
                    coordinates relative the player.
                * jump:
                    A boolean telling whether or not the player
                    should jump.
                    - True = jump, False = don't jump
                * toggle_debug:
                    A boolean telling whether or not to toggle
                    the debug state.
                    - True = toggle, False = don't toggle
                * toggle_pause:
                    A boolean telling whether or not to toggle
                    the pause state.
                    - True = toggle, False = don't toggle '''

        # Take input from the keyboard
        self._keys_pressed = pygame.key.get_pressed()

        # Cache current events, empty event queue
        current_events = pygame.event.get()

        # To run, or not to run...
        run = True

        for event in current_events:
            if event.type == QUIT:
                run = False

        if self._keys_pressed[K_ESCAPE]:
            run = False

        # The direction

        xDir = self._keys_pressed[K_d] - self._keys_pressed[K_a]
        zDir = self._keys_pressed[K_w] - self._keys_pressed[K_s]

        direction = Vector([xDir, 0.0, zDir]).normalize()
        if not direction:
            direction = Vector()

        # Mouse movement
        mouse_movement = pygame.mouse.get_rel()

        # Jumping

        if self._keys_pressed[K_SPACE] and self._player.colliding and not self._keys_pressed_last_frame[K_SPACE]:
            jump = True
        else:
            jump = False

        # Toggle debug state

        if self._keys_pressed[K_q] and not self._keys_pressed_last_frame[K_q]:
            self.toggle_debug()

        # Toggle pause

        if self._keys_pressed[K_p] and not self._keys_pressed_last_frame[K_p]:
            toggle_pause = True
        else:
            toggle_pause = False


        self._keys_pressed_last_frame = self._keys_pressed

        return run, direction, jump, toggle_pause, mouse_movement

    ### Getters

    def get_world(self):
        return self._world

    def get_sphere_space(self):
        return self._sphere_space

    def get_object_space(self):
        return self._object_space

    def get_static_space(self):
        return self._static_space

    def get_power_up_space(self):
        return self._power_up_space

    def get_interactive_object_space(self):
        return self._interactive_object_space

    def get_moving_scene_space(self):
        return self._moving_scene_space

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

    def get_contact_group(self):
        return self._contact_group

    def get_constants(self):
        return self._constants

    def get_fps(self):
        return self._fps

    def get_dt(self):
        return self._dt

    def get_debug_state(self):
        return self._debug_state

    ### Setters

    def add_constant(self, key, value):
        self._constants[key] = value

    def set_fps(self, fps):
        self._fps = fps
        self._dt = 1/float(fps)
