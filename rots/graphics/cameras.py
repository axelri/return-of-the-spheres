import pygame
from pygame.locals import *

from OpenGL.GLU import *

from math_classes.vectors import Vector
from math import cos, sin, pi
import players

class Camera:
    ''' A class to hold the camera object, defining
    the matrix to view the scene from the desired direction. '''
    
    def __init__(self):
        ''' Initializes and creates the camera object,
        sets the default distance to the player,
        the starting position and orientation of
        the camera. '''
        
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
        OpenGL. Sets the position of the camera to
        self._pos, directs it towards the player and
        sets the "up-direction" to self._up.

        Input:  player: A Player object

        Calls gluLookAt() with the right input to
        achieve the aforementioned result. '''
        
        pos = player.get_pos().value
        
        gluLookAt(self._xPos, self._yPos, self._zPos,
                  pos[0], pos[1], pos[2],
                  self._up[0], self._up[1], self._up[2])

    def _move(self, player):
        ''' Sets the position and orientation of
        the camera according to the position of
        the player and the movement of the mouse.

        Input:  player: A Player object '''
        
        pos = player.get_pos().value
        mouseX, mouseY = pygame.mouse.get_rel()

        self._xAngle -= mouseX * pi / 180.0 * 0.3

        player_y_pos = pos[1]
        y_dist = self._yPos - player_y_pos
        y_diff = self._yDist - y_dist

        if abs(y_diff) > 0.01 and not player.is_jumping():
            self._yPos += y_diff * 0.1


        self._xPos = pos[0] + sin(self._xAngle) * self._zDist
        self._zPos = pos[2] + cos(self._xAngle) * self._zDist

    def update(self, player):
        ''' Updates the camera object: Calls self.move()
        to set the position and orientation of the camera,
        and then calculates a vector pointing from the
        camera to the player.

        Input: player: A Player object

        Output: direction: A vector pointing from the
                    camera to the player, projected
                    on the xz-plane and normalized.'''
        
        pos = player.get_pos().value
        
        self._move(player)

        direction = Vector([pos[0] - self._xPos,
                                    pos[1] - self._yPos,
                                    pos[2] - self._zPos])
        direction = direction.projected(Vector([1.0, 0.0, 0.0]),
                                        Vector([0.0, 0.0, 1.0]))
        direction = direction.normalize()
        
        return direction
