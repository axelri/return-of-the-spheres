import numbers

import shapes
from math_classes.vectors import Vector
from sound import sound_effects

# TODO: Make prettier, add more stuff

class Player:
    def __init__(self, shape):

        self._shape = shape
        self._speed = 5
        self.colliding = False
        self._collided_last_frame = False
        self._jump_sound = sound_effects.load_sound('boing.wav')
        self._bounce_sound = sound_effects.load_sound('bounce.wav')

        self.lastDir = Vector()

    def get_shape(self):
        return self._shape

    def get_speed(self):
        return self._speed

    def get_pos(self):
        return self._shape.get_pos()

    def get_vel(self):
        return self._shape.get_vel()

    def set_speed(self):
        self._speed = speed

    def jump(self):
        self._jump_sound.play()
        self._shape.get_body().addForce((0.0, 300.0, 0.0))

    def move(self, direction, forward_vector, jump):

        # TODO: Tweak with self._speed and the coefficient in addForce 
        # (currrently 10) to get good movement
        # TODO: Fix so you can't move faster than intended just by moving the mouse
        # back and forth.
        
        left_vector = Vector((0.0, 1.0, 0.0)).cross(forward_vector)

        x_movement = left_vector * -direction.value[0]
        z_movement = forward_vector * -direction.value[2]
        direction = x_movement + z_movement

        current_vel = Vector(list(self._shape.get_body().getLinearVel()))
        proj_vel = current_vel.dot(direction)

        if proj_vel < self._speed:
            diff = self._speed - proj_vel
            if diff < self._speed:
                diff = self._speed

            self._shape.get_body().addForce((direction * diff * 10).value)

        if jump:
            self.jump()

        if self.colliding and not self._collided_last_frame:
            self._bounce_sound.play()

        self._collided_last_frame = self.colliding
