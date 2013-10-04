import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import tan, pi, radians

from graphics import textures, draw
from objects.text import TextBox

class Loading_screen:
    ''' A class for the loading screen. Is used to show
        an image and messages during the loading of the game. '''

    def __init__(self, image, width, heigth, aspect_angle):
        ''' Initializes the loading screen. Creates a quad
            to show the background image on. '''

        # Set up the perspective
        self._ratio = float(width)/float(heigth)
        self._distance = tan(radians(90 - aspect_angle/2.0 ))

        # Create a display list for the start screen image
        texture = textures.load_texture(image)

        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.loading_screen(texture, self._ratio)
        glEndList()

        self._display_list_index = display_list_index

        self._textboxes = []
        self._progress_bars = []

    def add_textbox(self, font, size, x_pos, y_pos, color):
        ''' Add a textbox '''
        
        text_box = TextBox(font, size, x_pos, y_pos, color)
        self._textboxes.append(text_box)

    def add_progress_bar(self, heigth, width, x_pos, y_pos, color):
        ''' Add a progress bar '''

        progress_bar = Progress_bar(heigth, width, x_pos, y_pos, color)
        self._progress_bars.append(progress_bar)

    def get_textboxes(self):
        return self._textboxes

    def update(self, textbox_indices = [], messages = [],
                    progress_bar_indices = [], fractions = []):
        ''' Draws the loading screen '''
        # TODO: Better API for this function?

        for i in textbox_indices:
            self._textboxes[i].set_string(messages[i])

        for i in progress_bar_indices:
            self._progress_bars[i].set_fraction(fractions[i])

        glDisable(GL_LIGHTING)

        glPushMatrix()
        glLoadIdentity()
        gluLookAt(0.0, 0.0, self._distance,
                    0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glCallList(self._display_list_index)

        for text_box in self._textboxes:
            text_box.draw()

        for progress_bar in self._progress_bars:
            progress_bar.draw()

        glPopMatrix()
        pygame.display.flip()
        glEnable(GL_LIGHTING)

class Progress_bar:

    def __init__(self, heigth, width, x_pos, y_pos, color):

        self._heigth = heigth/100.0
        self._width = width/100.0
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._color = color
        self._fraction = 0

        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)

        glColor4fv(color)
        glBegin(GL_QUADS)

        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
        glVertex3f(0.5, 0.5, 0.0)
        glVertex3f(-0.5, 0.5, 0.0)

        glEnd()

        glEndList()

        self._display_list_index = display_list_index

    def draw(self):

        glPushMatrix()
        #glLoadIdentity()
        #pushScreenCoordinateMatrix()

        #glTranslatef(self._x_pos - self._width * (1 - self._fraction) * 0.5,
        #            self._y_pos, 1)
        glTranslate(0.0, 0.0, 0.1)
        glScale(self._width * self._fraction, self._heigth, 1)

        #print 'scale factor: ', (self._width * self._fraction, self._heigth, 1)

        #pop_projection_matrix()
        glPopMatrix()

    def set_fraction(self, fraction):
        self._fraction = fraction

# A fairly straight forward function that pushes
# a projection matrix that will make object world 
# coordinates identical to window coordinates.
def pushScreenCoordinateMatrix():
    glPushAttrib(GL_TRANSFORM_BIT)
    viewport = glGetIntegerv(GL_VIEWPORT)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(viewport[0],viewport[2],viewport[1],viewport[3])
    glPopAttrib()
    return

# Pops the projection matrix without changing the current
# MatrixMode.
def pop_projection_matrix():
    glPushAttrib(GL_TRANSFORM_BIT)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glPopAttrib()
    return