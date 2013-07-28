import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import traceback
import sys
import time

import shapes
import games
import players
from graphics import render, init_graphics, lights, cameras, textures
from math_classes import vectors
from physics_engine import physics_support
from text import TextBox

def main():
    init_graphics.init_window('testODE 2')

    # Create a world object
    world = ode.World()
    world.setGravity( (0,-9.81,0) )
    world.setERP(0.8)
    world.setCFM(1E-5)

    # Create a space object
    space = ode.Space()



    PLANE_POINTS1 = [vectors.Vector([-10.0, 0.0, -10.0]),
                    vectors.Vector([10.0, 0.0, -10.0]),
                    vectors.Vector([10.0, 0.0, 10.0]),
                    vectors.Vector([-10.0, 0.0, 10.0])]

    PLANE_POINTS2 = [vectors.Vector([-10.0, 1.0, 0.0]),
                     vectors.Vector([10.0, 1.0, 0.0]),
                     vectors.Vector([10.0, -1.0, 0.0]),
                     vectors.Vector([-10.0, -1.0, 0.0])]

    PLANE_POINTS3 = [vectors.Vector([0.0, 1.0, 10.0]),
                     vectors.Vector([0.0, 1.0, -10.0]),
                     vectors.Vector([0.0, -1.0, -10.0]),
                     vectors.Vector([0.0, -1.0, 10.0])]

    earth_big_str = textures.loadImage('graphics/texture_data/celestial_bodies/earth_big.jpg')
    earth_big_tex = textures.loadTexture(earth_big_str, 1024, 1024)
    stars_big_str = textures.loadImage('graphics/texture_data/stars_big.jpg')
    stars_big_tex = textures.loadTexture(stars_big_str, 2048, 2048)
    sunset_str = textures.loadImage('graphics/texture_data/sunset.png')
    sunset_tex = textures.loadTexture(sunset_str, 256, 256)

    speed = 1

    sphere = shapes.Sphere(world, space, pos = vectors.Vector([0.0, 5.0, 0.0]), 
                            radius = 0.5, texture = earth_big_tex, 
                            color = [1.0, 1.0, 1.0])

    #cube = shapes.Cube(world, space, pos = otherPos)

    plane1 = shapes.Surface(world, space, 
                            points = PLANE_POINTS1, texture = stars_big_tex,
                            color = [1.0, 1.0, 1.0])
    plane2 = shapes.Surface(world, space, points = PLANE_POINTS2,
                            pos = vectors.Vector([0.0, 1.0, -10.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2])
    plane3 = shapes.Surface(world, space, points = PLANE_POINTS2,
                            pos = vectors.Vector([0.0, 1.0, 10.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2])
    plane4 = shapes.Surface(world, space, points = PLANE_POINTS3,
                            pos = vectors.Vector([10.0, 1.0, 0.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2])
    plane5 = shapes.Surface(world, space, points = PLANE_POINTS3,
                            pos = vectors.Vector([-10.0, 1.0, 0.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2])

    light1 = lights.Light(GL_LIGHT0, vectors.Vector([0.0, 5.0, 4.0]))
    camera = cameras.Camera()

    player = players.Player(sphere)

    text1 = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 200, [1,0,0])
    text2 = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 150, [1,0,0])
    text3 = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 100, [1,0,0])
    textList = [text1, text2, text3]

    objectList = []
    sceneList = [plane1, plane2, plane3, plane4, plane5]

    lightList = [light1] 

    game = games.Game(player, objectList, sceneList, lightList, textList, camera)

    run = True

    # Create group for contact joints
    contactgroup = ode.JointGroup()

    fps = 30
    dt = 1.0/fps
    run = True
    clock = pygame.time.Clock()
    speed = 2

    lastDir = [0.0, 0.0, 0.0]

    while run:

        # Take input
        run, direction, jump = player.take_input()

        # Move
        forwardVector = camera.update(player)
        player.move(direction, forwardVector, jump)

        # Simulate
        n = 2
        #Run multiple times for smoother simulation
        for i in range(n):
            # Detect collisions and create contact joints
            space.collide((world,contactgroup), physics_support.near_callback)

            # Simulation step
            world.step(dt/n)

            # Remove all contact joints
            contactgroup.empty()

        current_fps = clock.get_fps()

        # Render
        text1.set_string("Player position: {pos}".format(pos = player.get_shape().get_pos()))
        text2.set_string("Player velocity: {vel}".format(vel = player.get_shape().body.getLinearVel()))
        text3.set_string("FPS: {FPS}".format(FPS = current_fps))

        render.render(game)
        clock.tick(fps)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
