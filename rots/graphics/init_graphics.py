import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import itertools

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
    pygame.mixer.pre_init(44100, -16, 2, 1024) # setup mixer to avoid sound lag
    pygame.init()

    FULLSCREEN_WIDTH = pygame.display.Info().current_w
    FULLSCREEN_HEIGHT = pygame.display.Info().current_h

    if HAVE_FULLSCREEN:
        pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), 
                OPENGL|DOUBLEBUF|FULLSCREEN|HWSURFACE)
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
    # TODO: Change the order of these calls to be more logical,
    # maybe add comments.
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1.0))

    glClearColor(0.0, 0.0, 0.0, 0.0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    return width, height

def init_shadows(game):
    ''' Sets the necessary constants for shadow mapping. '''

    shadow_map_size = 512
    window_width = pygame.display.Info().current_w
    window_height = pygame.display.Info().current_h

    # Create the shadow map texture
    shadow_map_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, shadow_map_texture)
    glTexImage2D( GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, shadow_map_size, shadow_map_size, 0,
        GL_DEPTH_COMPONENT, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    # Calculate and save matrices
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    glLoadIdentity()
    gluPerspective(45.0, float(window_width) / float(window_height), 1.0, 100.0)
    camera_projection_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    glLoadIdentity()
    game._camera.view(game._player)
    camera_view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    glLoadIdentity()
    gluPerspective(45.0, 1.0, 2.0, 8.0)
    light_projection_matrix_c = glGetFloatv(GL_MODELVIEW_MATRIX)
    light_proj_list = [list(value) for value in list(light_projection_matrix_c)]
    merged = list(itertools.chain.from_iterable(light_proj_list))
    light_projection_matrix = merged



    light_view_matrix_list = []
    for light in game.get_light_list():
        light_pos = light.get_pos().value
        glLoadIdentity()
        gluLookAt( light_pos[0], light_pos[1], light_pos[2],
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0)
        light_view_matrix_c = glGetFloatv(GL_MODELVIEW_MATRIX)
        
        light_view_list = [list(value) for value in list(light_view_matrix_c)]
        merged = list(itertools.chain.from_iterable(light_view_list))
        light_view_matrix = merged
        light_view_matrix_list.append(light_view_matrix)

    glPopMatrix()

    bias_matrix = (0.5, 0.0, 0.0, 0.0,
                    0.0, 0.5, 0.0, 0.0,
                    0.0, 0.0, 0.5, 0.0,
                    0.5, 0.5, 0.5, 1.0)

    game.add_constant('shadow_map_size', shadow_map_size)
    game.add_constant('window_width', window_width)
    game.add_constant('window_height', window_height)
    game.add_constant('shadow_map_texture', shadow_map_texture)
    game.add_constant('camera_projection_matrix', camera_projection_matrix)
    game.add_constant('camera_view_matrix', camera_view_matrix)
    game.add_constant('light_projection_matrix', light_projection_matrix)
    game.add_constant('light_view_matrix_list', light_view_matrix_list)
    game.add_constant('bias_matrix', bias_matrix)
