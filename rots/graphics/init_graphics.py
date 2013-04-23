import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def init_window(windowName, HAVE_FULLSCREEN = True):
    ''' Initiates pygame, creates and sets up the window,
    sets up OpenGL.

    Input:  windowName: The desired name of the window;
                what the caption of the window will be
                set to, a string.
            HAVE_FULLSCREEN: Whether or not the window
                should be fullscreen, a boolean. '''

    assert isinstance(windowName, str), \
           'The name must be a string'
    assert isinstance(HAVE_FULLSCREEN, bool), \
           'HAVE_FULLSCREEN must be a boolean'

    # Initialize a pygame window
    pygame.init()

    FULLSCREEN_WIDTH = pygame.display.Info().current_w
    FULLSCREEN_HEIGHT = pygame.display.Info().current_h

    if HAVE_FULLSCREEN:
        pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), 
                OPENGL|DOUBLEBUF|FULLSCREEN)
    else:
        pygame.display.set_mode((640, 480), OPENGL|DOUBLEBUF)
    
    pygame.display.set_caption(windowName)
    # NOTE: Locks all input events to the pygame window, maybe DANGEROUS
    pygame.event.set_grab(True)
    width = pygame.display.Info().current_w
    height = pygame.display.Info().current_h

    pygame.mouse.set_visible(0)
    pygame.mouse.set_pos(width/ 2.0,
                         height / 2.0)


    # Initialize OpenGL
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
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
