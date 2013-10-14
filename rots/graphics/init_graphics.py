import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import itertools
from math import tan, pi, radians

from graphics import textures, draw, views
from objects.text import TextBox

from shadows import glLibShadowInit

def init_window(window_name, HAVE_FULLSCREEN = True):
    ''' Initiates pygame, creates and sets up the window,
    sets up OpenGL.

    Input:  
        * window_name: 
            The desired name of the window;
            what the caption of the window will be
            set to, a string.
        * HAVE_FULLSCREEN:
            Whether or not the window
            should be fullscreen, a boolean. '''

    # Initialize a pygame window
    pygame.mixer.pre_init(44100, -16, 2, 1024) # setup mixer to avoid sound lag
    pygame.init()

    FULLSCREEN_WIDTH = pygame.display.Info().current_w
    FULLSCREEN_HEIGHT = pygame.display.Info().current_h

    if HAVE_FULLSCREEN:
        pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), 
                OPENGL|DOUBLEBUF|FULLSCREEN|HWSURFACE)
    else:
        pygame.display.set_mode((640, 480), OPENGL|DOUBLEBUF)
    
    pygame.display.set_caption(window_name)
    # NOTE: Locks all input events to the pygame window, maybe DANGEROUS
    pygame.event.set_grab(True)

    width = pygame.display.Info().current_w
    height = pygame.display.Info().current_h
    aspect_angle = 45.0

    # Hide cursor, move to center of screen
    pygame.mouse.set_visible(0)
    pygame.mouse.set_pos(width/ 2.0,
                         height / 2.0)

    ### Initialize OpenGL

    # Set up the projection and modelview matrices
    view = views.View(width, height, aspect_angle)
    view.setup()

    # Set clearing color
    glClearColor(0.0, 0.0, 0.0, 0.0)

    # Enable depth testing and textures
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    # Enable and set up alpha blending
    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Enable and set up lighting
    glEnable(GL_LIGHTING)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glShadeModel(GL_SMOOTH)

    # Enable back-face culling
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    # Make OpenGL choose some parameters for best result
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

    # Initialize shadows
    shadowmap_size = 512
    glLibShadowInit([[shadowmap_size, 5]])

    return view
