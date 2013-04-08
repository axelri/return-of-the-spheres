# Test of the physics engine

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import shapes
import render
import physics
import games
import vectors


pygame.init()
pygame.display.set_mode((640, 480), OPENGL|DOUBLEBUF)

glEnable(GL_DEPTH_TEST)
#glEnable(GL_LIGHTING)
#glEnable(GL_LIGHT0)

glClearColor(0.0, 0.0, 0.0, 0.0)

glMatrixMode(GL_PROJECTION)

gluPerspective(45.0, 640.0/480.0, 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

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

speed = 0.1
xPos = 0.0
yPos = 5.0
zPos = 0.0
pos = [xPos, yPos, zPos]

otherPos = [-2.0, 5.0, 0.0]

pos = vectors.Vector(pos)
otherPos = vectors.Vector(otherPos)

sphere = shapes.Sphere(pos = pos, radius = 0.5)

cube = shapes.Cube(pos = otherPos)

plane1 = shapes.Surface(points = PLANE_POINTS1)
plane2 = shapes.Surface(points = PLANE_POINTS2,
                        pos = vectors.Vector([0.0, 1.0, -10.0]))
plane3 = shapes.Surface(points = PLANE_POINTS2,
                        pos = vectors.Vector([0.0, 1.0, 10.0]))
plane4 = shapes.Surface(points = PLANE_POINTS3,
                        pos = vectors.Vector([10.0, 1.0, 0.0]))
plane5 = shapes.Surface(points = PLANE_POINTS3,
                        pos = vectors.Vector([-10.0, 1.0, 0.0]))

player = sphere
#player = cube

#objectList = [cube]
#sceneList = []

objectList = []
sceneList = [plane1, plane2, plane3, plane4, plane5]


game = games.Game(player, objectList, sceneList)

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
    zDir = keyState[K_s] - keyState[K_w]

    direction = vectors.Vector([xDir, yDir, zDir])

    if not direction.is_zero():
        direction = direction.normalize()

    # NOTE: A primitive version of friction

    projVel = player.get_velocity().dot(direction)
    if projVel < speed:
        if projVel > 0:
            player.add_velocity(direction * (speed - projVel)*0.3)
        else:
            player.add_velocity(direction * speed*0.3)
    if direction.is_zero():
        player.set_velocity(player.get_velocity()*0.9)
    perpVel = player.get_velocity() - direction * projVel
    if not perpVel.is_zero():
        player.add_velocity(perpVel*-0.3)
        

    physics.update_physics(game)
    render.render(game)
    #print 'Pos:', player.get_pos().value

pygame.quit()
