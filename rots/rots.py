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
    ''' Main routine of the game.'''

    init_graphics.init_window('testODE 2')

    # Create a world object
    world = ode.World()
    world.setGravity( (0,-9.81,0) )
    world.setERP(0.8)
    world.setCFM(1E-5)

    # Create a space object
    space = ode.Space()

    # PLANE_POINTS1 = [Vector([-10.0, 0.0, -10.0]),
    #                 Vector([10.0, 0.0, -10.0]),
    #                 Vector([10.0, 0.0, 10.0]),
    #                 Vector([-10.0, 0.0, 10.0])]

    # PLANE_POINTS2 = [Vector([-10.0, 1.0, 0.0]),
    #                  Vector([10.0, 1.0, 0.0]),
    #                  Vector([10.0, -1.0, 0.0]),
    #                  Vector([-10.0, -1.0, 0.0])]

    # PLANE_POINTS3 = [Vector([0.0, 1.0, 10.0]),
    #                  Vector([0.0, 1.0, -10.0]),
    #                  Vector([0.0, -1.0, -10.0]),
    #                  Vector([0.0, -1.0, 10.0])]

    earth_tex = textures.load_texture('celestial_bodies/earth_big.jpg')
    moon_tex = textures.load_texture('celestial_bodies/moon-4k.png')
    stars_tex = textures.load_texture('stars_big.jpg')
    sun_tex = textures.load_texture('celestial_bodies/th_sun.png')
    mars_tex = textures.load_texture('celestial_bodies/Mars_2k-050104.png')

    speed = 1

    earth = shapes.Sphere(world, space, pos = Vector([0.0, 5.0, 0.0]), 
                            radius = 1.0, texture = earth_tex)

    moon = shapes.Sphere(world, space, pos = Vector([-3.0, 5.0, -3.0]),
                            radius = 0.27, mass = 0.5, texture = moon_tex)

    sun = shapes.Sphere(world, space, pos = Vector([5.0, 15.0, 5.0]), 
                            radius = 1.5, texture = sun_tex, mass = 5)

    mars = shapes.Sphere(world, space, pos = Vector([-3.0, 5.0, 3.0]),
                            radius = 0.53, mass = 1, texture = mars_tex)

    sun.set_emissive([1.0, 1.0, 1.0, 1.0])
    #sun_light = lights.Light(GL_LIGHT1, sun.get_pos(), ambient = [0.2, 0.2, 0.0, 1.0],
    #                        diffuse = [1.0, 1.0, 0.0, 1.0], specular = [1.0, 1.0, 1.0, 1.0])

    cube = shapes.Cube(world, space, pos = Vector([3.0, 5.0, 0.0]), side = 1)

    plane1 = shapes.Surface(world, space, pos = Vector(), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([0.0, -1.0, 0.0]),
                            length = 20.0, width = 20.0,
                            texture = stars_tex)
    plane2 = shapes.Surface(world, space, pos = Vector([10.0, 1.0, 0.0]), 
                            normal = Vector([-1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            length = 20.0, width = 2.0)
    plane3 = shapes.Surface(world, space, pos = Vector([-10.0, 1.0, 0.0]), 
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, -1.0]),
                            length = 20.0, width = 2.0)
    plane4 = shapes.Surface(world, space, pos = Vector([0.0, 1.0, 10.0]), 
                            normal = Vector([0.0, 0.0, -1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 20.0, width = 2.0)
    plane5 = shapes.Surface(world, space, pos = Vector([0.0, 1.0, -10.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([-1.0, 0.0, 0.0]),
                            length = 20.0, width = 2.0)

    plane2.set_ambient([0.0, 0.0, 0.2, 1.0])
    plane2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    plane3.set_ambient([0.0, 0.0, 0.2, 1.0])
    plane3.set_diffuse([0.0, 0.0, 0.2, 1.0])
    plane4.set_ambient([0.0, 0.0, 0.2, 1.0])
    plane4.set_diffuse([0.0, 0.0, 0.2, 1.0])
    plane5.set_ambient([0.0, 0.0, 0.2, 1.0])
    plane5.set_diffuse([0.0, 0.0, 0.2, 1.0])

    light1 = lights.Light(GL_LIGHT0, Vector([0.0, 5.0, 4.0]))
    light2 = lights.Light(GL_LIGHT2, Vector([3.0, 2.0, 3.0]))
    camera = cameras.Camera()

    player = players.Player(earth)

    objectList = [player.get_shape(), sun, moon, mars, cube, plane1, plane2, plane3, plane4, plane5]

    #lightList = [sun_light] 
    lightList = [light1, light2]

    clock = pygame.time.Clock()

    game = games.Game(world, space, player, objectList, lightList, camera, clock)

    run = True

    # Create group for contact joints
    contactgroup = ode.JointGroup()

    fps = 30
    dt = 1.0/fps
    run = True

    # Background music
    pygame.mixer.music.load('sound/sound_data/02. II. Molto vivace.ogg')
    pygame.mixer.music.play(-1)

    while run:

        #sun_light.set_pos(sun.get_pos())

        # Take input
        run, direction, jump, toggle_debug = game.take_input()

        if toggle_debug:
            game.toggle_debug()

        # Simulate
        physics.update_physics(world, space, contactgroup, game, dt)

        # Move
        forwardVector = camera.update(player)
        player.move(direction, forwardVector, jump)

        # Render

        render.render(game)
        clock.tick(fps)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
