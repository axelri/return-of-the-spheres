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
        
        # The wanted distance from the camera to the player
        self._y_dist = 4.0
        self._z_dist = 8.0

        # The actual distance from the camera to the player (TODO: rename...)
        self._real_z_dist = 8.0

        # The limits of the above distance
        self._y_dist_limits = (1.0, 8.0)
        self._z_dist_limits = (2.0, 16.0)

        # The position of the camera
        self._xPos = 0.0
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
        self._zoom_sensitivity = 0.05

    def view(self, player):
        ''' Calculates a translation/rotation matrix
        to move the camera to the right position and
        multiplies it with the current matrix used by
        OpenGL. Sets the position of the camera to
        self._pos, directs it towards the player and
        sets the "up-direction" to self._up.

        Input:  
            * player: 
                A Player object

        Calls gluLookAt() with the right input to
        achieve the aforementioned result. '''
        
        pos = player.get_pos().value
        up = self._up.value
        
        gluLookAt(self._xPos, self._yPos, self._zPos,
                  pos[0], pos[1], pos[2],
                  up[0], up[1], up[2])

    def _move(self, player, mouse_movement):
        ''' Sets the position and orientation of
        the camera according to the position of
        the player and the movement of the mouse.

        Input:  
            * player: 
                A Player object
            * mouse_movement: 
                A tuple with the relative motion 
                of the mouse since the last frame,
                in pixels (?), as (x, y) '''
        
        pos = player.get_pos().value
        mouseX, mouseY = mouse_movement

        self._xAngle -= mouseX * pi / 180.0 * self._mouse_sensitivity

        y_dist = self._yPos - pos[1]
        y_diff = self._y_dist - y_dist

        direction = Vector((pos[0] - self._xPos,
                            pos[1] - self._yPos,
                            pos[2] - self._zPos))
        direction = direction.projected(Vector((1.0, 0.0, 0.0)),
                                        Vector((0.0, 0.0, 1.0)))
        z_dist = direction.norm()
        z_diff = self._z_dist - z_dist

        if abs(y_diff) > 0.01 and not player.is_jumping():
            self._yPos += y_diff * 0.1

        if abs(z_diff) > 0.01:
            self._real_z_dist += z_diff * 0.1

        self._xPos = pos[0] + sin(self._xAngle) * self._real_z_dist
        self._zPos = pos[2] + cos(self._xAngle) * self._real_z_dist

    def update(self, player, mouse_movement, scroll_direction):
        ''' Updates the camera object: Calls self._move()
        to set the position and orientation of the camera,
        and then calculates a vector pointing from the
        camera to the player.

        Input: 
            * player: 
                A Player object
            * mouse_movement: 
                A tuple with the relative motion of the 
                mouse since the last frame, in pixels (?),
                as (x, y)
            * scroll_direction: 
                An integer describing the direction the 
                scrolling wheel is moving in.
                    -1 = scrolling up
                    0 = not scrolling
                    1 = scrolling down

        Output: 
            * direction: 
                A vector pointing from the
                camera to the player, projected
                on the xz-plane and normalized.'''
        
        pos = player.get_pos().value

        # Zoom
        self._y_dist += self._y_dist * scroll_direction * self._zoom_sensitivity
        self._z_dist += self._z_dist * scroll_direction * self._zoom_sensitivity

        # Make sure we don't zoom too far
        if abs(self._y_dist) <= self._y_dist_limits[0]:
            self._y_dist = self._y_dist_limits[0]
        elif abs(self._y_dist) >= self._y_dist_limits[1]:
            self._y_dist = self._y_dist_limits[1]

        if abs(self._z_dist) <= self._z_dist_limits[0]:
            self._z_dist = self._z_dist_limits[0]
        elif abs(self._z_dist) >= self._z_dist_limits[1]:
            self._z_dist = self._z_dist_limits[1]
        
        self._move(player, mouse_movement)

        self._direction = Vector([pos[0] - self._xPos,
                                    pos[1] - self._yPos,
                                    pos[2] - self._zPos])
        self._direction = self._direction.projected(Vector([1.0, 0.0, 0.0]),
                                        Vector([0.0, 0.0, 1.0]))
        self._direction = self._direction.normalize()

        if self._flipping:

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
