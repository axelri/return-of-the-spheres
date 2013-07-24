# Test of the physics engine

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import traceback
import sys
import time

import shapes
import games
import players
from graphics import render, init_graphics, lights, cameras, textures, glFreeType
from physics_engine import physics
from math_classes import vectors

def main():
    init_graphics.init_window('testPhysics')
    our_font = glFreeType.font_data('graphics/texture_data/fonts/test.ttf', 20)


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

    #puppy_str = textures.loadImage('graphics/texture_data/puppy.jpeg')
    #puppy_tex = textures.loadTexture(puppy_str, 256, 256)
    #sunset_str = textures.loadImage('graphics/texture_data/sunset.png')
    #sunset_tex = textures.loadTexture(sunset_str, 256, 256)
    #earth_str = textures.loadImage('graphics/texture_data/earth.jpg')
    #earth_tex = textures.loadTexture(earth_str, 256, 256)
    earth_big_str = textures.loadImage('graphics/texture_data/celestial_bodies/earth_big.jpg')
    earth_big_tex = textures.loadTexture(earth_big_str, 1024, 1024)
    # moon_str = textures.loadImage('graphics/texture_data/celestial_bodies/moon-4k.png')
    # moon_tex = textures.loadTexture(moon_str, 4096, 2048)
    #stars_str = textures.loadImage('graphics/texture_data/stars.jpg')
    #stars_tex = textures.loadTexture(stars_str, 512, 512)
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

    sphere = shapes.Sphere(pos = pos, radius = 2, texture = earth_big_tex, 
                            color = [1.0, 1.0, 1.0])

    cube = shapes.Cube(pos = otherPos)

    

    plane1 = shapes.Surface(points = PLANE_POINTS1, texture = stars_big_tex,
                            color = [1.0, 1.0, 1.0])
    plane2 = shapes.Surface(points = PLANE_POINTS2,
                            pos = vectors.Vector([0.0, 1.0, -10.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2])
    plane3 = shapes.Surface(points = PLANE_POINTS2,
                            pos = vectors.Vector([0.0, 1.0, 10.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2])
    plane4 = shapes.Surface(points = PLANE_POINTS3,
                            pos = vectors.Vector([10.0, 1.0, 0.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2])
    plane5 = shapes.Surface(points = PLANE_POINTS3,
                            pos = vectors.Vector([-10.0, 1.0, 0.0]),
                            #texture = sunset_tex, color = [1.0, 1.0, 1.0])
                            color = [0.0, 0.0, 0.2])

    #glEnable(GL_LIGHT0)

    light1 = lights.Light(GL_LIGHT0, vectors.Vector([0.0, 5.0, 4.0]))
    camera = cameras.Camera()

    player = players.Player(sphere)
    #player = players.Player(cube)
    #player = cube

    #objectList = [cube]
    #sceneList = []

    objectList = []
    sceneList = [plane1, plane2, plane3, plane4, plane5]
    #sceneList = [plane1]

    lightList = [light1]

    game = games.Game(player, objectList, sceneList, lightList, camera)

    run = True

    dt = 0.005
    # Start timing
    currentTime = time.clock()
    accumulator = 0.0
    counter = 0

    while run:

        newTime = time.clock()
        #print 'NewTime:', newTime
        frameTime = newTime - currentTime
        #print 'FrameTime:', frameTime
        if frameTime > 0.02:
            frameTime = 0.02    # To avoid to large timesteps
        currentTime = newTime
        
        accumulator += frameTime
        #print 'Accumulator:', accumulator
        while accumulator >= dt:
            

            # TODO: Make an input function instead?
            currentEvents = pygame.event.get() # cache current events
            for event in currentEvents:
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                    run = False
            keyState = pygame.key.get_pressed()

            xDir = keyState[K_d] - keyState[K_a]
            zDir = keyState[K_s] - keyState[K_w]

            if keyState[K_SPACE]:
                player.jump()

            direction = vectors.Vector([xDir, 0.0, zDir]).normalize()
            if direction == None:
                direction = vectors.Vector()
            
            forwardVector = camera.update(player)
            
            player.update_velocity(direction, forwardVector)
            
            physics.update_physics(game, dt)
            accumulator -= dt
            counter += 1

        #print 'Number of iterations before rendering:', counter
        #print ''
        counter = 0

        # TODO: Add linear interpolation and SLERP for
        # smoother animation

        render.render(game)
        pos = str(player.get_shape().get_pos().value)
        # TODO: Make text an object instead to be renderable
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()              
        glPushMatrix()
        glColor3f (1, 0, 0)
        our_font.glPrint(200,200,pos)
        glPopMatrix()
        pygame.display.flip()

        #print 'Pos:', player.get_pos().value

if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        pygame.quit()
