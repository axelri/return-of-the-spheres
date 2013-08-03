import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import shapes
import lights
import games

# TODO: Add smart culling to fasten up the drawing process.

def render(game):
    ''' Renders the scene: Clears the screen, sets up the camera
    and lights, draws the player and all other entities at their
    current position and flips the buffers.

    Input:  game: A Game object '''

    assert isinstance(game, games.Game), 'Input must be a Game object'
    
    world, space, player, objectList, lightList, camera = game.get_objects()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    camera.view(player)

    draw_scene(game, objectList)

    pygame.display.flip()


def draw_scene(game, objectList):# , lightList):

    if game.get_debug():
        game.update_debug_screen()

    #for light in lightList:
    #    light.move()    # NOTE: Is this needed every frame?

    for item in objectList:
        glPushMatrix()
        item.draw()
        glPopMatrix()
