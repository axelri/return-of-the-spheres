import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import shapes
import lights
# TODO: Add smart culling to fasten up the drawing process.
#def render(game, collisionInfo):
def render(game):
    ''' Draws the player and all other entities at their current position '''

    player, objectList, sceneList, lightList = game.get_objects()

    #collisionPoint, penetrationNormal, penetrationDepth = collisionInfo

    assert isinstance(player, shapes.Shape), \
           'Player must be a Shape object'
    assert isinstance(objectList, list), \
           'objectList must be a list of Shape objects'
    assert isinstance(sceneList, list), \
           'sceneList must be a list of Shape objects'
    assert isinstance(lightList, list), \
           'lightList must be a list of Light objects'
    if __debug__:
        for item in objectList:
            assert isinstance(item, shapes.Shape), \
                   'objectList must be a list of Shape objects'
        for item in sceneList:
            assert isinstance(item, shapes.Shape), \
                   'sceneList must be a list of Shape objects'
        for item in lightList:
            assert isinstance(item, lights.Light), \
                   'lightList must be a list of Light objects'

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    pos = player.get_pos().value

    glLoadIdentity()
    gluLookAt(pos[0], pos[1] + 4, pos[2] + 10,     # A point of reference is
              pos[0], pos[1], pos[2],              # needed, otherwise this 
              0, 1, 0)                             # is pointless.

    for light in lightList:
        glLightfv(light.get_light(), GL_POSITION, light.get_pos().value)

    #gluLookAt(0, 10, 20,
    #          0, 0, 0,
    #          0, 1, 0)

    #gluLookAt(0, 2, 4,
    #          0, 0, 0,
    #          0, 1, 0)

    
    
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    #print 'Orientation:', player.get_orientation()
    rotMatrix = player.get_orientation().convert_to_matrix()
    glMultMatrixf(rotMatrix)
    player.draw()
    glPopMatrix()

    for item in objectList:
        pos = item.get_pos().value
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        rotMatrix = item.get_orientation().convert_to_matrix()
        glMultMatrixf(rotMatrix)
        item.draw()
        glPopMatrix()

    
    for item in sceneList:
        pos = item.get_pos().value
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        rotMatrix = item.get_orientation().convert_to_matrix()
        glMultMatrixf(rotMatrix)
        item.draw()
        glPopMatrix()

##    if collisionPoint:
##        colPos = collisionPoint.value
##        glPushMatrix()
##        glTranslatef(colPos[0], colPos[1], colPos[2])
##        drawCross([1.0, 1.0, 1.0])
##        glPopMatrix()
##        drawVector(penetrationNormal.value)
    
    pygame.display.flip()
    pygame.time.wait(10)
