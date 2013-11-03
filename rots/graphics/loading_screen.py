import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

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

    def add_progress_bar(self, height, width, x_pos, y_pos, color, layer):
        ''' Add a progress bar 
            height: height of the progress bar in fractions of window height
            width: width of the progress bar in fractions of window width
            x_pos, y_pos: position of the center of the progress bar in
                    screen coordinates: 0,0 = lower left, 1,1 = upper rigth
            color: color of the progress bar as RGBA'''

        progress_bar = Progress_bar(height, width, x_pos, y_pos, color, 
                                    self._ratio, self._distance)
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

class Menu(object):
    
    def __init__(self, window_width, window_height, aspect_angle):
        ''' Window width and height in pixels'''
        self._width = window_width
        self._height = window_height
        self._ratio = float(window_width)/float(window_height)
        self._distance = tan(radians(90 - aspect_angle/2.0 ))

        self._space = ode.Space(1)
        self._objects = []

    def add_button(self, height, width, x_pos, y_pos, color, layer):

        b = Button(height, width, x_pos, y_pos, color, self._ratio, self._distance, 1, self._space)
        self._objects.append(b)

    def update(self, counter_increase = 0):
        ''' Draws the loading screen, updates all textboxes and progress bars '''

        ligthing_enabled = glGetBooleanv(GL_LIGHTING)
        glDisable(GL_LIGHTING)

        # Draw the background image
        glPushMatrix()
        glLoadIdentity()
        gluLookAt(0.0, 0.0, self._distance,
                    0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        for obj in self._objects:
            obj.draw()

        glPopMatrix()
        pygame.display.flip()

        if ligthing_enabled:
            glEnable(GL_LIGHTING)

class MenuObj(object):

    def __init__(self, height, width, x_pos, y_pos, color,
                 window_ratio, window_distance, layer, active):

        self._height = height * 2
        self._width = width * 2 * window_ratio
        self._x_pos = (x_pos - 0.5) * 2 * window_ratio
        self._y_pos = (y_pos - 0.5) * 2
        self._color = color
        self._distance = window_distance - layer * 0.001
        self._active = active

        r,g,b,a = color
        dark_f = 0.5
        r = r * dark_f
        g = g * dark_f
        b = b * dark_f
        self._hovercolor = (r,g,b,a)

        r,g,b,a = color
        light_f = 2
        r = r * light_f
        g = g * light_f
        b = b * light_f
        self._inactive_color = (r,g,b,a)
 

    def create_display_list_index(self,color):
        display_list_index = glGenLists(1)
        glNewList(display_list_index, GL_COMPILE)
        draw.draw2D_box(color, self._width, self._height)
        glEndList()
        return display_list_index


class Surface(MenuObj):
    def __init__(self, height, width, x_pos, y_pos, color,
                 window_ratio, window_distance, layer, active, texture=None):
        super(Surface, self).__init__(height, width, x_pos, y_pos, color,
                    window_ratio, window_distance, layer, active)
        
        self._display_list_index = self.create_display_list_index(self._color)

    def draw(self):
        glLoadIdentity()
        glTranslate(self._x_pos, self._y_pos, - self.distance)

        # compile a specific color based on the context
        if self._active and not self._prev_active:
            self._display_list_index = self.create_display_list_index(self._color)
        elif not self._active and self._prev_active:
            self._display_list_index = self.create_display_list_index(self._inactive_color)

        glCallList(self._display_list_index)

class Clickable(MenuObj):

    def __init__(self, height, width, x_pos, y_pos, color,
                window_ratio, window_distance, layer, space, active):
        super(Clickable, self).__init__(height, width, x_pos, y_pos, color,
                window_ratio, window_distance, layer, active)

        # create a surface-like ODE geometry
        self._geom = ode.GeomBox(space, (self._width, self._height, 0.1))
        self._geom.setBody(None)
        self._is_colliding = False

    def get_geom(self):
        return self._geom

class Button(Clickable):

    def __init__(self, height, width, x_pos, y_pos, color,
                window_ratio, window_distance, layer, space, active=True):
        super(Button, self).__init__(height, width, x_pos, y_pos, color,
                    window_ratio, window_distance, layer, space, active)
        self._geom.__setattr__('object', self)

        self._display_list_index = self.create_display_list_index(self._color)

        # to avoid unnessecary compiling later on
        self._prev_active = self._active
        self._prev_colliding = self._is_colliding

    def draw(self):
        glLoadIdentity()
        glTranslate(self._x_pos, self._y_pos, - self._distance)

        # compile a specific color based on the context
        if self._is_colliding and not self._prev_colliding:
            self._display_list_index = self.create_display_list_index(self._hovercolor)
        elif self._active and not self._prev_active:
            self._display_list_index = self.create_display_list_index(self._color)
        elif not self._active and self._prev_active:
            self._display_list_index = self.create_display_list_index(self._inactive_color)

        glCallList(self._display_list_index)

class Progress_bar:

    def __init__(self, height, width, x_pos, y_pos, color,
                window_ratio, window_distance):

        # The factor 2 is there since the coordinates
        # and sizes are given in window-relative coordinates
        # (x and y is in the range [0, 1]), whereas in the loading
        # screen we have OpenGLs coordinates (y is in the range [-1, 1]
        # and x is in the range [-window_ratio, window_ratio])
        self._height = height * 2
        self._width = width * 2 * window_ratio
        self._x_pos = (x_pos - 0.5) * 2 * window_ratio
        self._y_pos = (y_pos - 0.5) * 2
        self._color = color
        self._counter = 0
        self._denominator = 1
        self._distance = window_distance - 0.001
        self._active = True

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

        if self._active:

            glPushMatrix()
            glLoadIdentity()

            fraction = self._counter / float(self._denominator)

            glTranslate(self._x_pos - self._width * 0.5 * (1 - fraction), 
                        self._y_pos, - self._distance)

            glScale(self._width * fraction, self._height, 1)
            glCallList(self._display_list_index)

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
