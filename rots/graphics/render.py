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
    ''' Draws the player and all other entities at their current position '''

    assert isinstance(game, games.Game), 'Input must be a Game object'
    
    player, objectList, sceneList, lightList = game.get_objects()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    pos = player.get_shape().get_pos().value

    glLoadIdentity()
    gluLookAt(pos[0], pos[1] + 4, pos[2] + 10,
              pos[0], pos[1], pos[2],
              0, 1, 0)

    for light in lightList:
        glLightfv(light.get_light(), GL_POSITION, light.get_pos().value)
    
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    #print 'Orientation:', player.get_orientation()
    #rotMatrix = player.get_orientation().convert_to_matrix()
    rotMatrix = player.get_shape().get_orientation()
    glMultMatrixf(rotMatrix)
    player.get_shape().draw()
    glPopMatrix()

    for item in objectList:
        pos = item.get_pos().value
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        #rotMatrix = item.get_orientation().convert_to_matrix()
        rotMatrix = item.get_orientation()
        glMultMatrixf(rotMatrix)
        item.draw()
        glPopMatrix()

    
    for item in sceneList:
        pos = item.get_pos().value
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        #rotMatrix = item.get_orientation().convert_to_matrix()
        rotMatrix = item.get_orientation()
        glMultMatrixf(rotMatrix)
        item.draw()
        glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)
