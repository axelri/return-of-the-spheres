import numbers

import pygame
from pygame.locals import *

import shapes
from math_classes import vectors

# TODO: Make prettier, add more stuff

class Player:
    def __init__(self, shape):
        assert isinstance(shape, shapes.Shape), 'Input must be a shape object'
        self._shape = shape
        self._inputVelocity = vectors.Vector()
        #self._physicsVelocity = shape.get_velocity()
        self._speed = 0.1
        self.colliding = False

    def get_shape(self):
        return self._shape

    def get_speed(self):
        return self._speed

    def set_speed(self):
        assert isinstance(speed, numbers.Number), 'Input must be a number'
        assert speed > 0.0, 'Speed must be greater than 0'
        self._speed = speed


    def update_velocity(self, direction):
        # TODO: You get a small boost when changing direction, fix
        # set the velocity we want according to the input
        self._inputVelocity = direction * self._speed


        shapeVel = self._shape.get_velocity()
        projVel = shapeVel.dot(direction)
        perpVel = shapeVel - direction * projVel

        if shapeVel != self._inputVelocity:
            #print 'Not the same velocity'
            #print 'shapeVel:', shapeVel
            #print 'inputVel:', self._inputVelocity
            # we haven't reached the velocity we want yet
            speedDiff = abs(projVel - self._speed)
            if speedDiff != 0.0 and speedDiff < 0.0001 :
                #print 'Close enough!'
                # we're close enough, set the velocity to what we want
                self._shape.add_velocity(direction*projVel*-1.0)
                self._shape.add_velocity(self._inputVelocity)
                #print 'After:', self._shape.get_velocity()
            elif projVel < self._speed:
                #print 'Too slow!'
                # we're slower than we want, accelerate
                if projVel > 0:
                    #print 'Right direction'
                    # we're mowing in the right direction
                    self._shape.add_velocity(direction * \
                                      (self._speed - projVel)*0.5)
                    #print 'After:', self._inputVelocity
                else:
                    #print 'Wrong direction'
                    # we're moving in the wrong direction
                    # (this is added to avoid extreme acceleration
                    # when moving in the wrong direction)
                    self._shape.add_velocity(direction * self._speed*0.5)
                    #print 'After:', self._inputVelocity
