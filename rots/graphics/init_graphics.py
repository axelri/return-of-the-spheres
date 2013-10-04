import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import itertools
from math import tan, pi, radians

from graphics import textures, draw
from objects.text import TextBox

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

    # Hide cursor, move to center of screen
    pygame.mouse.set_visible(0)
    pygame.mouse.set_pos(width/ 2.0,
                         height / 2.0)

    ### Initialize OpenGL

    # Set up the projection and modelview matrices
    glMatrixMode(GL_PROJECTION)
    aspect_angle = 45.0
    gluPerspective(aspect_angle, float(width)/float(height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

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

    return width, height, aspect_angle

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

    # Save the matrices as game constants
    game.add_constant('shadow_map_size', shadow_map_size)
    game.add_constant('window_width', window_width)
    game.add_constant('window_height', window_height)
    game.add_constant('shadow_map_texture', shadow_map_texture)
    game.add_constant('camera_projection_matrix', camera_projection_matrix)
    game.add_constant('camera_view_matrix', camera_view_matrix)
    game.add_constant('light_projection_matrix', light_projection_matrix)
    game.add_constant('light_view_matrix_list', light_view_matrix_list)
    game.add_constant('bias_matrix', bias_matrix)


# TODO: Make this a 'Loading-screen' class instead

class Start_screen:
    ''' A class for the start screen. Is used to show
        an image and messages during the loading of the game. '''

    def __init__(self, start_image, width, height, aspect_angle):
        ''' Initializes the start screen. Creates a quad
            to show the background image on and a textbox
            to show messages on. '''

        # Set up the perspective
        self._ratio = float(width)/float(height)
        self._distance = tan(radians(90 - aspect_angle/2.0 ))

        # Create a display list for the start screen image
        start_texture = textures.load_texture(start_image)

        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.start_screen(start_texture, self._ratio)
        glEndList()

        self._display_list_index = display_list_index

        # Create a text box
        self._text_box = TextBox('test.ttf', 40, width/2 - 200, 
                                        height/2, [1,0,0])

    def update(self, message):
        ''' Updates and draws the start screen '''

        glDisable(GL_LIGHTING)

        self._text_box.set_string(message)

        glPushMatrix()
        glLoadIdentity()
        gluLookAt(0.0, 0.0, self._distance,
                    0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glCallList(self._display_list_index)

        self._text_box.draw()

        glPopMatrix()
        pygame.display.flip()
        glEnable(GL_LIGHTING)
