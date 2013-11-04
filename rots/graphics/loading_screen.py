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

    def __init__(self, image, width, height, aspect_angle):
        ''' Initializes the loading screen. Creates a quad
            to show the background image on. '''

        # Set up the perspective
        self._width = width
        self._height = height
        self._ratio = float(width)/float(height)
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
        
        textbox = _Loading_screen_textbox(font, size, x_pos, y_pos, color,
                                            self._width, self._height)
        self._textboxes.append(textbox)
        return textbox

    def add_progress_bar(self, height, width, x_pos, y_pos, color, texture = None):
        ''' Add a progress bar 
            height: height of the progress bar in fractions of window height
            width: width of the progress bar in fractions of window width
            x_pos, y_pos: position of the center of the progress bar in
                    screen coordinates: 0,0 = lower left, 1,1 = upper right
            color: color of the progress bar as RGBA'''

        progress_bar = Progress_bar(height, width, x_pos, y_pos, color, 
                                    self._ratio, self._distance, texture)
        self._progress_bars.append(progress_bar)

        return progress_bar

    def get_textboxes(self):
        return self._textboxes

    def get_progress_bars(self):
        return self._progress_bars

    def update(self, counter_increase = 0):
        ''' Draws the loading screen, updates all textboxes and progress bars '''

        ligthing_enabled = glGetBooleanv(GL_LIGHTING)
        glDisable(GL_LIGHTING)

        # Update counters
        if counter_increase != 0:
            for textbox in self._textboxes:
                textbox.increase_counter(counter_increase)
            for progress_bar in self._progress_bars:
                progress_bar.increase_counter(counter_increase)  

        # Update textboxes
        for textbox in self._textboxes:
            textbox.update()

        # Draw the background image
        glPushMatrix()
        glLoadIdentity()
        gluLookAt(0.0, 0.0, self._distance,
                    0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glCallList(self._display_list_index)

        # Draw textboxes and progress bars
        for progress_bar in self._progress_bars:
            progress_bar.draw()

        for textbox in self._textboxes:
            textbox.draw()

        glPopMatrix()
        pygame.display.flip()

        if ligthing_enabled:
            glEnable(GL_LIGHTING)

class Progress_bar:

    def __init__(self, height, width, x_pos, y_pos, color,
                window_ratio, window_distance, texture = None):

        # The factor 2 is there since the coordinates
        # and sizes are given in window-relative coordinates
        # (x and y is in the range [0, 1]), whereas in the loading
        # screen we have OpenGLs coordinates (y is in the range [-1, 1]
        # and x is in the range [-window_ratio, window_ratio])
        self._height = height * 2
        self._width = width * 2 * window_ratio
        self._x_pos = (x_pos - 0.5) * 2 * window_ratio
        self._y_pos = (y_pos - 0.5) * 2
        self._z_pos = 0.001
        self._texture = texture
        if texture == None:
            self._color = color
        else:
            self._color = (1.0, 1.0, 1.0, 1.0)
        self._counter = 0
        self._denominator = 1

        self._active = True

    def draw(self):

        if self._active:

            glPushMatrix()

            fraction = self._counter / float(self._denominator)

            glTranslate(self._x_pos - self._width * 0.5 * (1 - fraction), 
                        self._y_pos, self._z_pos)
            
            draw.progress_bar(self)

            glPopMatrix()

        else:
            pass

    def set_denominator(self, denominator):
        if denominator != 0:
            self._denominator = denominator
        else:
            print 'Dividing by zero is a bad thing to do! Choose a non-zero denominator'

    def increase_counter(self, i):
        self._counter += i

    def reset_counter(self):
        self._counter = 0

    def enable(self):
        self._active = True

    def disable(self):
        self._active = False

    def get_counter(self):
        return self._counter

    def get_denominator(self):
        return self._denominator

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_texture(self):
        return self._texture

    def get_color(self):
        return self._color

class _Loading_screen_textbox:

    def __init__(self, font, size, x_pos, y_pos, color,
                window_width, window_height):

        size = int(window_height * size)
        x_pos = int(window_width * x_pos)
        y_pos = int(window_height * y_pos)

        self._textbox = TextBox(font, size, x_pos, y_pos, color)

        self._counter = 0
        self._message = ''
        self._denominator = 1
        self._mode = 'percentage'
        self._active = True


    def set_message(self, message, mode, denominator = 1):

        if denominator != 0:
            self._denominator = denominator
        else:
            print 'Dividing by zero is a bad thing to do! Choose a non-zero denominator'

        if mode == 'percentage' or mode == 'plain text':
            self._mode = mode
        else:
            print "The mode isn't recognised, please use either 'plain text' or 'percentage'"

        self._message = message

    def update(self):

        if self._mode == 'percentage':
            message = self._message + ': {percentage:.0f}%'.format(percentage = \
                                                self._counter/float(self._denominator) * 100)
            self._textbox.set_string(message)
        else:
            self._textbox.set_string(self._message)

    def draw(self):
        if self._active:
            self._textbox.draw()

    def increase_counter(self, i):
        self._counter += i

    def reset_counter(self):
        self._counter = 0

    def enable(self):
        self._active = True

    def disable(self):
        self._active = False
