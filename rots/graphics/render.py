import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.depth_texture import *
from OpenGL.GL.ARB.shadow import *

import lights
import games

from shadows import *
from math import degrees, asin

from objects import shapes
from math_classes import matrices
from math_classes.vectors import Vector

shadow_color = [0.1, 0.1, 0.1]
light_color = [1.0, 1.0, 1.0]
GLLIB_SHADOW_MAP1 = 5

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

    camera.view()

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

def draw_objects(object_list):

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

def render_with_shadows(game):
    global light_focus

    camera = game.get_camera()
    player = game.get_player()
    object_list = game.get_object_list()
    light_list = game.get_light_list()
    light = light_list[0]
    view = game.get_view()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    light_pos = light.get_pos()

    light_focus = player.get_pos()
    #light_focus = Vector((0.0, 0.0, 0.0))

    dist = (light_pos - light_focus).norm()
    #light_angle = degrees(2 * asin(2.9 / dist))
    light_angle = 50
    near = dist - 2.9
    far = dist + 2.9
    glLibCreateShadowBefore(GLLIB_SHADOW_MAP1, light_pos.value,
                            light_focus.value, lightviewangle = light_angle,
                            near = near, far = far)

    #draw_objects(object_list)
    glPushMatrix()
    player.get_shape().draw()
    glPopMatrix()

    glLibCreateShadowAfter(GLLIB_SHADOW_MAP1)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    view.setup()
    camera.view(player)

    light.change_color(shadow_color)
    light.change_diffuse_color(light_color)
    pos = light.get_pos()
    light.set_pos(pos)

    draw_objects(object_list)

    glLibRenderShadowCompareBefore(GLLIB_SHADOW_MAP1)

    light.change_diffuse_color(shadow_color)

    draw_objects(object_list)

    glLibRenderShadowCompareAfter()

    if game.get_debug_state():
        game.update_debug_screen()

    if game.get_debug_state() == 2:
        draw_debug_objects(object_list, light_list)

    pygame.display.flip()