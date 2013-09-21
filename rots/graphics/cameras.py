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
        self._x_dist = 0.0
        self._y_dist = 4.0
        self._z_dist = 10.0

        # The position of the camera
        self._xPos = self._x_dist
        self._yPos = self._y_dist
        self._zPos = self._z_dist

        self._xAngle = 0.0

        # The up vector for the camera
        self._up = Vector([0.0, 1.0, 0.0])
        self._new_up = None
        self._direction = None

        self._flipping = False
        self._flip_axis = None
        self._mouse_sensitivity = 0.3

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
        up = self._up.value
        
        gluLookAt(self._xPos, self._yPos, self._zPos,
                  pos[0], pos[1], pos[2],
                  up[0], up[1], up[2])

    def _move(self, player):
        ''' Sets the position and orientation of
        the camera according to the position of
        the player and the movement of the mouse.

        Input:  player: A Player object '''
        
        pos = player.get_pos().value
        mouseX, mouseY = pygame.mouse.get_rel()

        self._xAngle -= mouseX * pi / 180.0 * self._mouse_sensitivity

        player_y_pos = pos[1]
        y_dist = self._yPos - player_y_pos
        y_diff = self._y_dist - y_dist

        if abs(y_diff) > 0.01 and not player.is_jumping():
            self._yPos += y_diff * 0.1


        self._xPos = pos[0] + sin(self._xAngle) * self._z_dist
        self._zPos = pos[2] + cos(self._xAngle) * self._z_dist

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

        self._direction = Vector([pos[0] - self._xPos,
                                    pos[1] - self._yPos,
                                    pos[2] - self._zPos])
        self._direction = self._direction.projected(Vector([1.0, 0.0, 0.0]),
                                        Vector([0.0, 0.0, 1.0]))
        self._direction = self._direction.normalize()

        if self._flipping:
            # TODO: Remove the bug that causes strange
            # rotation if moving the mouse while flipping

            rot_vec = self._up.cross(self._flip_axis) * 0.1
            self._up += rot_vec
            self._up = self._up.normalize()

            if (self._up - self._new_up).norm() < 0.1:
                self._up = self._new_up
                self._flipping = False

        return self._direction, self._up

    def flip_up_vector(self):
        ''' Flip the camera upside down '''

        self._flipping = True
        self._new_up = self._up * -1.0
        self._y_dist *= -1.0
        self._mouse_sensitivity *= -1.0
        self._flip_axis = self._direction

    def flip_y_dist(self):
        ''' Flip the distance from the player 
            in the y-direction (if the player
            is viewed from above, view it 
            from below instead, and vice versa) '''

        self._y_dist *= -1.0

    ### Getters

    def get_up(self):
        return self._up
