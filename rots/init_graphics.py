import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def init_window():
    ''' Initiate pygame, initiate OpenGL, create a window, setup OpenGL'''

    # Initialize a pygame window
    pygame.init()
    pygame.display.set_mode((640, 480), OPENGL|DOUBLEBUF)
    pygame.display.set_caption("testPhysics")
    pygame.mouse.set_visible(0)


    # Initialize OpenGL
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)
    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glShadeModel(GL_SMOOTH)
    glDisable(GL_CULL_FACE)
    glColorMaterial(GL_FRONT, GL_DIFFUSE) 

    glClearColor(0.0, 0.0, 0.0, 0.0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, 640.0/480.0, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
