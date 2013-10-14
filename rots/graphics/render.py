import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.depth_texture import *
from OpenGL.GL.ARB.shadow import *

import lights
import games
from objects import shapes
from math_classes import matrices
from math_classes.vectors import Vector

shadow_color = [0.1, 0.1, 0.1]
light_color = [1.0, 1.0, 1.0]

def render(game):
    ''' Renders the scene: Clears the screen, sets up the camera
    and lights, draws the player and all other entities at their
    current position and flips the buffers.

    Input:  game: A Game object '''
    
    camera = game.get_camera()
    player = game.get_player()
    object_list = game.get_object_list()
    light_list = game.get_light_list()

    glLoadIdentity()

    camera.view(player)

    if game.get_debug_state():
        game.update_debug_screen()

    # Update the light positions

    for light in light_list:
        pos = light.get_pos()
        light.set_pos(pos)

    draw_scene(object_list, game)

    if game.get_debug_state() == 2:
        draw_debug_objects(object_list, light_list)

    pygame.display.flip()


def draw_scene(object_list, game):
    ''' Draws the scene. '''

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    for item in object_list:
        glPushMatrix()
        item.draw()
        glPopMatrix()

def draw_debug_objects(object_list, light_list):
    ''' Draw AABBs and the position of the lights '''

    for item in object_list:
        glPushMatrix()
        item.draw_AABB()
        glPopMatrix()

    for light in light_list:
        glPushMatrix()
        light.draw_pos()
        glPopMatrix()
