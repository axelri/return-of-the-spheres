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
        self._ratio

    def add_textbox(self, font, size, x_pos, y_pos, color):
        ''' Add a textbox '''
        
        text_box = TextBox(font, size, x_pos, y_pos, color)
        self._textboxes.append(text_box)

    def add_progress_bar(self, heigth, width, x_pos, y_pos, color):
        ''' Add a progress bar 
            heigth: heigth of the progress bar in fractions of window heigth
            width: width of the progress bar in fractions of window width
            x_pos, y_pos: position of the center of the progress bar in
                    screen coordinates: 0,0 = lower left, 1,1 = upper rigth
            color: color of the progress bar as RGBA'''

        progress_bar = Progress_bar(heigth, width, x_pos, y_pos, color, 
                                    self._ratio, self._distance)
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

        for progress_bar in self._progress_bars:
            progress_bar.draw()

        for text_box in self._textboxes:
            text_box.draw()

        glPopMatrix()
        pygame.display.flip()
        glEnable(GL_LIGHTING)

class Progress_bar:

    def __init__(self, heigth, width, x_pos, y_pos, color,
                window_ratio, window_distance):

        self._heigth = heigth * 2
        self._width = width * 2 * window_ratio
        self._x_pos = (x_pos - 0.5) * 2 * window_ratio
        self._y_pos = (y_pos - 0.5) * 2
        self._color = color
        self._fraction = 0
        self._distance = window_distance - 0.001

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
        glLoadIdentity()

        glTranslate(self._x_pos - self._width * 0.5 * (1 - self._fraction), 
                    self._y_pos, - self._distance)

        glScale(self._width * self._fraction, self._heigth, 1)
        glCallList(self._display_list_index)

        glPopMatrix()

    def set_fraction(self, fraction):
        self._fraction = fraction
