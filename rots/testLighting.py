import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import traceback
import sys

import shapes
import games
import players
from graphics import render, init_graphics, lights, cameras
from physics_engine import physics
from math_classes import vectors

def init():
    init_graphics.init_window('testLighting')

    pos = vectors.Vector([0.0, 2.0, 0.0])

    PLANE_POINTS1 = [vectors.Vector([-10.0, 0.0, -10.0]),
                    vectors.Vector([10.0, 0.0, -10.0]),
                    vectors.Vector([10.0, 0.0, 10.0]),
                    vectors.Vector([-10.0, 0.0, 10.0])]

    sphere = shapes.Sphere(pos = pos, radius = 0.5)

    plane1 = shapes.Surface(points = PLANE_POINTS1)

    light1 = lights.Light(GL_LIGHT0, vectors.Vector([0.0, 5.0, 4.0]))

    camera = cameras.Camera()

    player = players.Player(sphere)

    sceneList = [plane1]
    objectList = []
    lightList = [light1]

    game = games.Game(player, objectList, sceneList, lightList, camera)

    return game

def main():

    game = init()

    player, objectList, sceneList, lightList, camera = game.get_objects()

    run = True

    while run:

        currentEvents = pygame.event.get() # cache current events
        for event in currentEvents:
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False
        keyState = pygame.key.get_pressed()

        xDir = keyState[K_d] - keyState[K_a]
        yDir = keyState[K_SPACE] - keyState[K_LSHIFT]
        zDir = keyState[K_w] - keyState[K_s]

        direction = vectors.Vector([xDir, yDir, zDir]).normalize()
        if direction == None:
            direction = vectors.Vector()

        forwardVector = camera.update(player)

        speed = 0.1
        upVector = vectors.Vector([0.0, 1.0, 0.0])
        rightVector = forwardVector.cross(upVector)

        Dir = direction.value

        moveDir = (rightVector*Dir[0] + upVector*Dir[1] + forwardVector*Dir[2])*speed

        player.get_shape().add_pos(moveDir)

        render.render(game)

if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
        

        
