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
from math_classes.vectors import Vector
from physics_engine import physics
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



    PLANE_POINTS1 = [Vector([-10.0, 0.0, -10.0]),
                    Vector([10.0, 0.0, -10.0]),
                    Vector([10.0, 0.0, 10.0]),
                    Vector([-10.0, 0.0, 10.0])]

    PLANE_POINTS2 = [Vector([-10.0, 1.0, 0.0]),
                     Vector([10.0, 1.0, 0.0]),
                     Vector([10.0, -1.0, 0.0]),
                     Vector([-10.0, -1.0, 0.0])]

    PLANE_POINTS3 = [Vector([0.0, 1.0, 10.0]),
                     Vector([0.0, 1.0, -10.0]),
                     Vector([0.0, -1.0, -10.0]),
                     Vector([0.0, -1.0, 10.0])]

    earth_big_tex = textures.loadTexture('graphics/texture_data/celestial_bodies/earth_big.jpg', 1024, 1024)
    moon_tex = textures.loadTexture('graphics/texture_data/celestial_bodies/moon-4k.png', 4096, 2048)
    stars_big_tex = textures.loadTexture('graphics/texture_data/stars_big.jpg', 2048, 2048)
    sun_tex = textures.loadTexture('graphics/texture_data/celestial_bodies/th_sun.png', 1024, 512)

    speed = 1

    earth = shapes.Sphere(world, space, pos = Vector([0.0, 5.0, 0.0]), 
                            radius = 0.5, texture = earth_big_tex, 
                            color = [1.0, 1.0, 1.0])

    moon = shapes.Sphere(world, space, pos = Vector([-3.0, 5.0, -3.0]),
                            radius = 0.27, color = [1.0, 1.0, 1.0], 
                            mass = 1, texture = moon_tex)

    sun = shapes.Sphere(world, space, pos = Vector([5.0, 5.0, 5.0]), 
                            radius = 1.5, texture = sun_tex, 
                            color = [1.0, 1.0, 1.0], emissive = [1.0, 1.0, 1.0, 1.0])

    cube = shapes.Cube(world, space, pos = Vector([3.0, 5.0, 0.0]),
                        side = 1)

    plane1 = shapes.Surface(world, space, 
                            points = PLANE_POINTS1, texture = stars_big_tex,
                            color = [1.0, 1.0, 1.0])
    plane2 = shapes.Surface(world, space, points = PLANE_POINTS2,
                            pos = Vector([0.0, 1.0, -10.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2], normal = Vector([0.0, 0.0, 1.0]))
    plane3 = shapes.Surface(world, space, points = PLANE_POINTS2,
                            pos = Vector([0.0, 1.0, 10.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2], normal = Vector([0.0, 0.0, -1.0]))
    plane4 = shapes.Surface(world, space, points = PLANE_POINTS3,
                            pos = Vector([10.0, 1.0, 0.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2], normal = Vector([-1.0, 0.0, 0.0]))
    plane5 = shapes.Surface(world, space, points = PLANE_POINTS3,
                            pos = Vector([-10.0, 1.0, 0.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2], normal = Vector([1.0, 0.0, 0.0]))

    light1 = lights.Light(GL_LIGHT0, Vector([0.0, 5.0, 4.0]))
    camera = cameras.Camera()

    player = players.Player(moon)

    text1 = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 200, [1,0,0])
    text2 = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 150, [1,0,0])
    text3 = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 100, [1,0,0])
    text4 = TextBox('graphics/texture_data/fonts/test.ttf', 14, 100, 50, [1,0,0])
    #textList = [text1, text2, text3, text4]
    textList = []

    objectList = [sun, earth]
    sceneList = [plane1, plane2, plane3, plane4, plane5]

    lightList = [light1] 

    clock = pygame.time.Clock()

    game = games.Game(player, objectList, sceneList, lightList, textList, camera, clock)

    run = True

    # Create group for contact joints
    contactgroup = ode.JointGroup()

    fps = 30
    dt = 1.0/fps
    run = True

    while run:

        # Take input
        run, direction, jump, toggle_debug = player.take_input()

        if toggle_debug:
            game.debug = not game.debug

        # Simulate
        physics.update_physics(world, space, contactgroup, player, dt)

        # Move
        forwardVector = camera.update(player)
        player.move(direction, forwardVector, jump)

        current_fps = clock.get_fps()

        # Render
        #text1.set_string("Player position: {pos}".format(pos = player.get_shape().get_pos()))
        #text2.set_string("Player velocity: {vel}".format(vel = player.get_shape().body.getLinearVel()))
        #text3.set_string("FPS: {FPS}".format(FPS = current_fps))
        #text4.set_string("Player colliding: {colliding}".format(colliding = player.colliding))

        render.render(game)
        clock.tick(fps)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
