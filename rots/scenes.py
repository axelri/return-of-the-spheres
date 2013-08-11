import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import shapes
import games
import players
from graphics import init_graphics, lights, cameras, textures
from math_classes.vectors import Vector

def init_scene():
    ''' Initializes the scene (creates all objects etc)
        and returns the game object. '''

     # Create a world object
    world = ode.World()
    world.setGravity( (0,-9.81,0) )
    world.setERP(0.8)
    world.setCFM(1E-5)

    # Create a space object
    space = ode.Space()

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
    sun_light = lights.Light(GL_LIGHT1, sun.get_pos(), ambient = [0.2, 0.2, 0.0, 1.0],
                            diffuse = [1.0, 1.0, 1.0, 1.0], specular = [1.0, 1.0, 1.0, 1.0])

    cube = shapes.Cube(world, space, pos = Vector([3.0, 5.0, 0.0]), side = 1)

    floor = shapes.Surface(world, space, pos = Vector(), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([0.0, -1.0, 0.0]),
                            length = 30.0, width = 30.0)#,
                            #texture = stars_tex)
    wall1 = shapes.Surface(world, space, pos = Vector([15.0, 4.0, 0.0]), 
                            normal = Vector([-1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            length = 30.0, width = 8.0)
    wall2 = shapes.Surface(world, space, pos = Vector([-15.0, 1.0, 0.0]), 
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, -1.0]),
                            length = 30.0, width = 2.0)
    wall3 = shapes.Surface(world, space, pos = Vector([-5.0, 4.0, 15.0]), 
                            normal = Vector([0.0, 0.0, -1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 40.0, width = 8.0)
    wall4 = shapes.Surface(world, space, pos = Vector([-5.0, 4.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([-1.0, 0.0, 0.0]),
                            length = 40.0, width = 8.0)
    slope = shapes.Surface(world, space, pos = Vector([-19.0, 5.0, 0.0]),
                            normal = Vector([0.6, 0.8, 0.0]),
                            forward = Vector([0.8, -0.6, 0.0]),
                            length = 10.0, width = 30.0)

    wall1.set_ambient([0.0, 0.0, 0.2, 1.0])
    wall1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    wall2.set_ambient([0.0, 0.0, 0.2, 1.0])
    wall2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    wall3.set_ambient([0.0, 0.0, 0.2, 1.0])
    wall3.set_diffuse([0.0, 0.0, 0.2, 1.0])
    wall4.set_ambient([0.0, 0.0, 0.2, 1.0])
    wall4.set_diffuse([0.0, 0.0, 0.2, 1.0])
    slope.set_ambient([0.0, 0.0, 0.2, 1.0])
    slope.set_diffuse([0.0, 0.0, 0.2, 1.0])

    light1 = lights.Light(GL_LIGHT0, Vector([0.0, 5.0, 4.0]))
    light2 = lights.Light(GL_LIGHT2, Vector([3.0, 2.0, 3.0]))
    camera = cameras.Camera()

    player = players.Player(earth)

    objectList = [player.get_shape(), sun, moon, mars, cube, floor, wall1, wall2, wall3, wall4, slope]

    #lightList = [sun_light, light1] 
    lightList = [light1, light2]
    #lightList = []

    clock = pygame.time.Clock()

    # Create group for contact joints
    contactgroup = ode.JointGroup()

    game = games.Game(world, space, player, objectList, lightList, camera, clock, contactgroup)

    # Initialize some constants for the shadow calculations
    init_graphics.init_shadows(game)

    return game  