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

def take_input():
    currentEvents = pygame.event.get() # cache current events
    run = True
    for event in currentEvents:
        if event.type == QUIT or \
        (event.type == KEYDOWN and event.key == K_ESCAPE):
            run = False
    keyState = pygame.key.get_pressed()

    xDir = keyState[K_d] - keyState[K_a]
    zDir = keyState[K_s] - keyState[K_w]

    direction = vectors.Vector([xDir, 0.0, zDir]).normalize()
    if not direction:
        direction = [0,0,0]
    else:
        direction = direction.value

    return run, direction

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

    speed = 0.1
    xPos = 0.0
    yPos = 5.0
    zPos = 0.0
    pos = [xPos, yPos, zPos]

    otherPos = [-2.0, 5.0, 0.0]

    pos = vectors.Vector(pos)
    otherPos = vectors.Vector(otherPos)

    sphere = shapes.Sphere(world, space, pos = pos, radius = 2, texture = earth_big_tex, 
                            color = [1.0, 1.0, 1.0])

    cube = shapes.Cube(world, space, pos = otherPos)

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

    text = TextBox('graphics/texture_data/fonts/test.ttf', 14, 200, 200, [1,0,0])
    textList = [text]

    objectList = []
    sceneList = [plane1, plane2, plane3, plane4, plane5]

    lightList = [light1] 

    game = games.Game(player, objectList, sceneList, lightList, textList, camera)

    run = True

    # Create group for contact joints
    contactgroup = ode.JointGroup()

    fps = 50
    dt = 1.0/fps
    run = True
    clock = pygame.time.Clock()
    speed = 2

    lastDir = [0.0, 0.0, 0.0]

    while run:

        run, direction = take_input()

        # Move

        if direction == lastDir:
            current_vel = vectors.Vector(list(player.get_shape().body.getLinearVel()))
            if current_vel.norm() < speed:
                corr_vel = vectors.Vector(direction)*(speed - current_vel.norm())
                new_vel = current_vel + corr_vel
                player.get_shape().body.setLinearVel(new_vel.value)
        else:
            current_vel = vectors.Vector(list(player.get_shape().body.getLinearVel()))
            corr_vel = vectors.Vector(direction)*speed
            new_vel = current_vel + corr_vel
            player.get_shape().body.setLinearVel(new_vel.value)
            lastDir = direction

        forwardVector = camera.update(player)

        # Simulate
        n = 2

        for i in range(n):
            # Detect collisions and create contact joints
            space.collide((world,contactgroup), physics_support.near_callback)

            # Simulation step
            world.step(dt/n)

            # Remove all contact joints
            contactgroup.empty()

        # Render
        text.set_string("Position: {pos}".format(pos = player.get_shape().get_pos()))
        render.render(game)
        pygame.display.flip()



if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
