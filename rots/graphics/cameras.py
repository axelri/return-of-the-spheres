import pygame
from pygame.locals import *

from OpenGL.GLU import *

from math_classes import vectors
from math import cos, sin, pi

class Camera:
    def __init__(self):
        # The distance from the camera to the player
        self._xDist = 0.0
        self._yDist = 4.0
        self._zDist = 10.0

        # The position of the camera
        self._xPos = self._xDist
        self._yPos = self._yDist
        self._zPos = self._zDist

        self._xAngle = 0.0

        # The up vector for the camera
        self._up = [0.0, 1.0, 0.0]        

    def view(self, player):
        ''' Calculates a translation/rotation matrix
        to move the camera to the right position and
        multiplies it with the current matrix used by
        OpenGL '''
        pos = player.get_shape().get_pos().value
        gluLookAt(self._xPos, self._yPos, self._zPos,
                  pos[0], pos[1], pos[2],
                  self._up[0], self._up[1], self._up[2])

    def move(self, player):
        ''' Moves the camera to the right position based
        on the movement of the player and the mouse '''
        pos = player.get_shape().get_pos().value
        mouseX, mouseY = pygame.mouse.get_rel()

        self._xAngle -= mouseX * pi / 180.0 * 0.3

        self._xPos = pos[0] + sin(self._xAngle) * self._zDist
        self._zPos = pos[2] + cos(self._xAngle) * self._zDist

    def update(self, player):
        ''' Updates the camera '''
        pos = player.get_shape().get_pos().value
        self.move(player)
        #self.view(player)
        return vectors.Vector([pos[0] - self._xPos, pos[1] - self._yPos,
                pos[2] - self._zPos]).projected(vectors.Vector([1.0, 0.0, 0.0]),
                        vectors.Vector([0.0, 0.0, 1.0])).normalize()
