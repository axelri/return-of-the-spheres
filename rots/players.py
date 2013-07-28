import numbers

import pygame
from pygame.locals import *

import shapes
from math_classes.vectors import Vector

# TODO: Make prettier, add more stuff

class Player:
    def __init__(self, shape):
        assert isinstance(shape, shapes.Shape), 'Input must be a shape object'
        self._shape = shape
        self._inputVelocity = Vector()
        #self._physicsVelocity = shape.get_velocity()
        self._speed = 5
        self.colliding = False
        self.jumping = False

        self.lastDir = Vector()

    def get_shape(self):
        return self._shape

    def get_speed(self):
        return self._speed

    def set_speed(self):
        assert isinstance(speed, numbers.Number), 'Input must be a number'
        assert speed > 0.0, 'Speed must be greater than 0'
        self._speed = speed

    def jump(self):

    #    if self.colliding and not self.jumping:
    #        self._shape.add_velocity(Vector([0.0, 0.4, 0.0]))
    #        self.jumping = True
        #if not self.jumping:
        self._shape.body.addForce((0.0, 20.0, 0.0))
        #    self.jumping = True


    def reset_jump(self):
        self.jumping = False


    def move(self, direction, forwardVector, jump):

        #TODO: Tweak with self._speed and the coef in addForce (currrently 10)
        # to get good movement
        
        leftVector = Vector([0.0, 1.0, 0.0]).cross(forwardVector)

        xMovement = leftVector * -direction.value[0]
        zMovement = forwardVector * -direction.value[2]
        direction = xMovement + zMovement

        current_vel = Vector(list(self._shape.body.getLinearVel()))
        projVel = current_vel.dot(direction)

        if projVel < self._speed:
            diff = self._speed - projVel
            if diff < self._speed:
                diff = self._speed

            self._shape.body.addForce((direction * diff * 10).value)

        if jump:
            #self._shape.body.addForce((0.0, 500.0, 0.0))
            current_vel = Vector(list(self._shape.body.getLinearVel()))
            jump_vel = Vector([0.0, 7.0, 0.0])
            new_vel = current_vel + jump_vel
            self._shape.body.setLinearVel(new_vel.value)

    def take_input(self):
        currentEvents = pygame.event.get() # cache current events
        run = True
        for event in currentEvents:
            if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False
        keyState = pygame.key.get_pressed()

        xDir = keyState[K_d] - keyState[K_a]
        zDir = keyState[K_s] - keyState[K_w]

        if keyState[K_SPACE] and not self.jumping:
            jump = True
            self.jumping = True
        elif not keyState[K_SPACE]:
            self.jumping = False
            jump = False
        else:
            jump = False

        direction = Vector([xDir, 0.0, zDir]).normalize()
        if not direction:
            direction = Vector()

        return run, direction, jump

