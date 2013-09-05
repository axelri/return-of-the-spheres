import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import games
import players
from objects import shapes, power_ups, interactive_objects, moving_scene
from graphics import init_graphics, lights, cameras, textures
from math_classes.vectors import Vector

def init_scene(start_screen):
    ''' Initializes the scene (creates all objects etc)
        and returns the game object. '''

    # TODO: Make this function read info from another file and create
    # a the scene as described in that file, in order to make it easier
    # to create different scenes.

    # TODO: Move things to better order, update start screen messages.

    # Create a world object

    world = ode.World()
    world.setGravity( (0,-9.81,0) )
    world.setERP(0.8)
    world.setCFM(1E-5)

    # Create space objects, one for spheres, one for other
    # moving objects and one for the static environment
    sphere_space = ode.Space(1)
    object_space = ode.Space(1)
    static_space = ode.Space(1)
    power_up_space = ode.Space(1)
    interactive_object_space = ode.Space(1)

    # Load textures
    tex_no = 6 # The number of textures (used to show progress in loading)
    start_screen.update('Loading textures: {perc:.0f}%'.format(perc = 0.0/tex_no*100))

    earth_tex = textures.load_texture('celestial_bodies/earth_big.jpg')
    start_screen.update('Loading textures: {perc:.0f}%'.format(perc = 1.0/tex_no*100))

    moon_tex = textures.load_texture('celestial_bodies/moon-4k.png')
    start_screen.update('Loading textures: {perc:.0f}%'.format(perc = 2.0/tex_no*100))

    stars_tex = textures.load_texture('stars_big.jpg')
    start_screen.update('Loading textures: {perc:.0f}%'.format(perc = 3.0/tex_no*100))

    sun_tex = textures.load_texture('celestial_bodies/th_sun.png')
    start_screen.update('Loading textures: {perc:.0f}%'.format(perc = 4.0/tex_no*100))

    mars_tex = textures.load_texture('celestial_bodies/Mars_2k-050104.png')
    start_screen.update('Loading textures: {perc:.0f}%'.format(perc = 5.0/tex_no*100))

    puppy_tex = textures.load_texture('puppy.jpeg')
    start_screen.update('Loading textures: {perc:.0f}%'.format(perc = 6.0/tex_no*100))

    # Create shapes
    obj_no = 6
    start_screen.update('Creating objects: {perc:.0f}%'.format(perc = 0.0/obj_no*100))

    earth = shapes.Sphere(world, sphere_space, pos = Vector([0.0, 5.0, 0.0]), 
                            radius = 1.0, texture = earth_tex)
    start_screen.update('Creating objects: {perc:.0f}%'.format(perc = 1.0/obj_no*100))

    moon = shapes.Sphere(world, sphere_space, pos = Vector([-3.0, 5.0, -3.0]),
                            radius = 0.27, mass = 0.5, texture = moon_tex)
    start_screen.update('Creating objects: {perc:.0f}%'.format(perc = 2.0/obj_no*100))

    sun = shapes.Sphere(world, sphere_space, pos = Vector([5.0, 5.0, 5.0]), 
                            radius = 1.5, texture = sun_tex, mass = 5)
    start_screen.update('Creating objects: {perc:.0f}%'.format(perc = 3.0/obj_no*100))

    mars = shapes.Sphere(world, sphere_space, pos = Vector([-3.0, 5.0, 3.0]),
                            radius = 0.53, mass = 1, texture = mars_tex)
    start_screen.update('Creating objects: {perc:.0f}%'.format(perc = 4.0/obj_no*100))

    sun.set_emissive([1.0, 1.0, 1.0, 1.0])
    #sun_light = lights.Light(GL_LIGHT1, sun.get_pos(), ambient = [0.2, 0.2, 0.0, 1.0],
    #                        diffuse = [1.0, 1.0, 1.0, 1.0], specular = [1.0, 1.0, 1.0, 1.0])

    cube = shapes.Cube(world, object_space, pos = Vector([3.0, 5.0, 0.0]), side = 2,
                        texture = puppy_tex)
    start_screen.update('Creating objects: {perc:.0f}%'.format(perc = 5.0/obj_no*100))

    # Create power ups
    world_flipper = power_ups.World_flipper(power_up_space, 
                                                Vector([10.0, 2.0, 10.0]))
    gravity_flipper = power_ups.Gravity_flipper(power_up_space, 
                                                Vector([10.0, 2.0, -10.0]))

    start_screen.update('Creating objects: {perc:.0f}%'.format(perc = 6.0/obj_no*100))

    # Create surfaces
    scene_no = 15
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 0.0/scene_no*100))

    sticky_floor = shapes.Surface(world, static_space, pos = Vector((0.0, 0.0, 7.5)), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0,
                            texture = stars_tex)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 1.0/scene_no*100))

    slippy_floor = shapes.Surface(world, static_space, pos = Vector((0.0, 0.0, -7.5)), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 2.0/scene_no*100))

    wall1 = shapes.Surface(world, static_space, pos = Vector([-15.0, 8.0, 0.0]), 
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            length = 30.0, width = 16.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 3.0/scene_no*100))

    wall2 = shapes.Surface(world, static_space, pos = Vector([10.0, 8.0, 15.0]), 
                            normal = Vector([0.0, 0.0, -1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 50.0, width = 16.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 4.0/scene_no*100))

    door_wall_1 = shapes.Surface(world, static_space, pos = Vector([-9.0, 8.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 12.0, width = 16.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 5.0/scene_no*100))

    door_wall_2 = shapes.Surface(world, static_space, pos = Vector([0.0, 11.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 6.0, width = 14.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 6.0/scene_no*100))

    door_wall_3 = shapes.Surface(world, static_space, pos = Vector([19.0, 8.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 32.0, width = 16.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 7.0/scene_no*100))

    floor_slope = shapes.Surface(world, static_space, pos = Vector([25.0, 4.0, 0.0]), 
                            normal = Vector([-8.0, 20.0, 0.0]).normalize(),
                            forward = Vector([20.0, 8.0, 0.0]).normalize(),
                            length = Vector([20.0, 8.0, 0.0]).norm(), width = 30.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 8.0/scene_no*100))

    roof_slope = shapes.Surface(world, static_space, pos = Vector([25.0, 12.0, 0.0]),
                            normal = Vector([-8.0, -20.0, 0.0]).normalize(),
                            forward = Vector([20.0, -8.0, 0.0]).normalize(),
                            length = Vector([20.0, -8.0, 0.0]).norm(), width = 30.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 9.0/scene_no*100))

    sticky_roof = shapes.Surface(world, static_space, pos = Vector((0.0, 16.0, 7.5)), 
                            normal = Vector([0.0, -1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0,
                            texture = stars_tex)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 10.0/scene_no*100))

    slippy_roof = shapes.Surface(world, static_space, pos = Vector((0.0, 16.0, -7.5)), 
                            normal = Vector([0.0, -1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 11.0/scene_no*100))

    balcony = shapes.Surface(world, static_space, pos = Vector((0.0, 0.0, -20.0)), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 12.0, width = 10.0)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 12.0/scene_no*100))

    fence_1 = shapes.Surface(world, static_space, pos = Vector((-6.0, 0.75, -20.0)), 
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            length = 10.0, width = 1.5)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 13.0/scene_no*100))

    fence_2 = shapes.Surface(world, static_space, pos = Vector((6.0, 0.75, -20.0)), 
                            normal = Vector([-1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, -1.0]),
                            length = 10.0, width = 1.5)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 14.0/scene_no*100))

    fence_3 = shapes.Surface(world, static_space, pos = Vector((0.0, 0.75, -25.0)), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 12.0, width = 1.5)
    start_screen.update('Creating scene: {perc:.0f}%'.format(perc = 15.0/scene_no*100))

    # Set the color of the surfaces

    # NOTE: It takes A LOT of time to set the colors,
    # since we generate a new display list each time we
    # change color. Better/faster solution?
    col_no = 24

    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 0.0/col_no*100))

    slippy_floor.set_ambient([0.5, 0.5, 0.8, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 1.0/col_no*100))
    slippy_floor.set_diffuse([0.5, 0.5, 0.8, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 2.0/col_no*100))

    slippy_roof.set_ambient([0.8, 0.5, 0.5, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 3.0/col_no*100))
    slippy_roof.set_diffuse([0.8, 0.5, 0.5, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 4.0/col_no*100))

    wall1.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 5.0/col_no*100))
    wall1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 6.0/col_no*100))

    wall2.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 7.0/col_no*100))
    wall2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 8.0/col_no*100))

    door_wall_1.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 9.0/col_no*100))
    door_wall_1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 10.0/col_no*100))

    door_wall_2.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 11.0/col_no*100))
    door_wall_2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 12.0/col_no*100))

    door_wall_3.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 13.0/col_no*100))
    door_wall_3.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 14.0/col_no*100))

    floor_slope.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 15.0/col_no*100))
    floor_slope.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 16.0/col_no*100))

    roof_slope.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 17.0/col_no*100))
    roof_slope.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 18.0/col_no*100))

    fence_1.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 19.0/col_no*100))
    fence_1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 20.0/col_no*100))

    fence_2.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 21.0/col_no*100))
    fence_2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 22.0/col_no*100))

    fence_3.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 23.0/col_no*100))
    fence_3.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update('Setting colours: {perc:.0f}%'.format(perc = 24.0/col_no*100))

    # Set friction and bounce
    slippy_floor.set_friction(0.1)
    slippy_floor.set_bounce(0.5)
    sticky_floor.set_friction(10)
    sticky_floor.set_bounce(0.1)
    slippy_roof.set_friction(0.1)
    slippy_roof.set_bounce(0.5)
    sticky_roof.set_friction(10)
    sticky_roof.set_bounce(0.1)

    door = moving_scene.Sliding_door(static_space, pos = Vector((0.0, 2.0, -15.0)), 
                            normal = Vector((0.0, 0.0, 1.0)),
                            slide_dir = Vector((1.0, 0.0, 0.0)), slide_size = 6,
                            ort_size = 4)

    door_button_1 = interactive_objects.Button(interactive_object_space, 
                            pos = Vector([-8.0, 1.2, -15.0]),
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            side = 1,
                            action = door.toggle)

    door_button_2 = interactive_objects.Button(interactive_object_space, 
                            pos = Vector([-6.0, 0.75, -18.0]),
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            side = 1,
                            action = door.toggle)

    # Create lights
    light1 = lights.Light(GL_LIGHT0, Vector([0.0, 5.0, 4.0]))
    light2 = lights.Light(GL_LIGHT2, Vector([3.0, 2.0, 3.0]))
    camera = cameras.Camera()

    start_screen.update('Organizing')

    # Create player
    player = players.Player(earth)

    # Add all objects that should be drawn to a list
    object_list = [player.get_shape(), sun, moon, mars, cube, 
                    sticky_floor, slippy_floor, wall1, wall2, 
                    door_wall_1, door_wall_2, door_wall_3, 
                    floor_slope, roof_slope, slippy_roof,
                    sticky_roof, balcony, fence_1, fence_2, fence_3,
                    world_flipper, gravity_flipper,
                    door, door_button_1, door_button_2]

    def add_sphere(args):
        object_list, space, world, pos = args
        sphere = shapes.Sphere(world, space, pos = pos)
        object_list.append(sphere)

    button_1 = interactive_objects.Button(interactive_object_space, 
                            pos = Vector([-15.0, 1.1, 0.0]),
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            action = add_sphere,
                            args = (object_list, sphere_space, world, Vector([0.0, 5.0, 0.0])))

    object_list.append(button_1)

    # Add all lights to a list
    light_list = [light1, light2]

    # Create a clock object for timing
    clock = pygame.time.Clock()

    # Create group for contact joints
    contact_group = ode.JointGroup()

    fps = 60

    # Create a game object
    spaces = (sphere_space, object_space, static_space, power_up_space, interactive_object_space)

    game = games.Game(world, spaces, player, object_list, 
                    light_list, camera, clock, contact_group, fps)

    # Initialize some constants for the shadow calculations
    init_graphics.init_shadows(game)

    return game  