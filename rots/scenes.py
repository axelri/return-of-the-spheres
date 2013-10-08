import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import games
import players
from objects import shapes, power_ups, interactive_objects, moving_scene
from graphics import init_graphics, lights, cameras, textures, loading_screen
from math_classes.vectors import Vector

def init_scene(loading_screen_data):
    ''' Initializes the scene (creates all objects etc)
        and returns the game object. '''

    # TODO: Make this function read info from another file and create
    # a the scene as described in that file, in order to make it easier
    # to create different scenes.

    # TODO: Move things to better order, update start screen messages.

    # Create a loading screen
    # NOTE: It can be hard to remember which textbox/progress bar 
    # corresponds to which index, is there any better solution?
    width, heigth, aspect_angle, loading_image = loading_screen_data
    start_screen = loading_screen.Loading_screen(loading_image, width, heigth, aspect_angle)
    start_screen.add_textbox('test.ttf', 40, width/2.0 - 200, heigth/2.0 - 20, [1,0,0])
    start_screen.add_textbox('test.ttf', 40, width/2.0 - 200, heigth/2.0 - 150, [0,1,0])
    start_screen.add_progress_bar(0.02, 0.2, 0.5, 0.45, [1.0, 0.0, 0.0, 1.0])
    start_screen.add_progress_bar(0.02, 0.2, 0.5, 0.35, [0.0, 1.0, 0.0, 1.0])

    start_screen.update(textbox_indices = [0],
                        messages = ['Creating world'])
    

    # Create a world object

    world = ode.World()
    world.setGravity( (0,-9.81,0) )
    world.setERP(0.8)
    world.setCFM(1E-5)
    world.setAutoDisableFlag(True)

    # Create space objects, one for spheres, one for other
    # moving objects and one for the static environment
    sphere_space = ode.Space(1)
    object_space = ode.Space(1)
    static_space = ode.Space(1)
    power_up_space = ode.Space(1)
    interactive_object_space = ode.Space(1)
    moving_scene_space = ode.Space(1)

    total_no = 53

    # Load textures
    tex_no = 6 # The number of textures (used to show progress in loading)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Loading textures: {perc:.0f}%'.format(perc = 0.0/tex_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 0.0/total_no*100)],
                        fractions = [0.0/tex_no, 0.0/total_no])

    earth_tex = textures.load_texture('celestial_bodies/earth_big.jpg')
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Loading textures: {perc:.0f}%'.format(perc = 1.0/tex_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 1.0/total_no*100)],
                        fractions = [1.0/tex_no, 1.0/total_no])

    moon_tex = textures.load_texture('celestial_bodies/moon-4k.png')
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Loading textures: {perc:.0f}%'.format(perc = 2.0/tex_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 2.0/total_no*100)],
                        fractions = [2.0/tex_no, 2.0/total_no])

    stars_tex = textures.load_texture('stars_big.jpg')
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Loading textures: {perc:.0f}%'.format(perc = 3.0/tex_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 3.0/total_no*100)],
                        fractions = [3.0/tex_no, 3.0/total_no])

    sun_tex = textures.load_texture('celestial_bodies/th_sun.png')
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Loading textures: {perc:.0f}%'.format(perc = 4.0/tex_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 4.0/total_no*100)],
                        fractions = [4.0/tex_no, 4.0/total_no])

    mars_tex = textures.load_texture('celestial_bodies/Mars_2k-050104.png')
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Loading textures: {perc:.0f}%'.format(perc = 5.0/tex_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 5.0/total_no*100)],
                        fractions = [5.0/tex_no, 5.0/total_no])

    puppy_tex = textures.load_texture('puppy.jpeg')
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Loading textures: {perc:.0f}%'.format(perc = 6.0/tex_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 6.0/total_no*100)],
                        fractions = [6.0/tex_no, 6.0/total_no])

    # Create shapes
    obj_no = 6
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating objects: {perc:.0f}%'.format(perc = 0.0/obj_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 6.0/total_no*100)],
                        fractions = [0.0/obj_no, 6.0/total_no])

    earth = shapes.Sphere(world, sphere_space, pos = Vector([0.0, 5.0, 0.0]), 
                            radius = 1.0, texture = earth_tex)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating objects: {perc:.0f}%'.format(perc = 1.0/obj_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 7.0/total_no*100)],
                        fractions = [1.0/obj_no, 7.0/total_no])

    moon = shapes.Sphere(world, sphere_space, pos = Vector([-3.0, 5.0, -3.0]),
                            radius = 0.27, mass = 0.5, texture = moon_tex)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating objects: {perc:.0f}%'.format(perc = 2.0/obj_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 8.0/total_no*100)],
                        fractions = [2.0/obj_no, 8.0/total_no])

    sun = shapes.Sphere(world, sphere_space, pos = Vector([5.0, 5.0, 5.0]), 
                            radius = 1.5, texture = sun_tex, mass = 5)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating objects: {perc:.0f}%'.format(perc = 3.0/obj_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 9.0/total_no*100)],
                        fractions = [3.0/obj_no, 9.0/total_no])

    mars = shapes.Sphere(world, sphere_space, pos = Vector([-3.0, 5.0, 3.0]),
                            radius = 0.53, mass = 1, texture = mars_tex)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating objects: {perc:.0f}%'.format(perc = 4.0/obj_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 10.0/total_no*100)],
                        fractions = [4.0/obj_no, 10.0/total_no])

    sun.set_emissive([1.0, 1.0, 1.0, 1.0])

    box = shapes.Box(world, object_space, pos = Vector([3.0, 5.0, 0.0]), x_size = 2,
                        y_size = 3, z_size = 1.5, texture = puppy_tex)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating objects: {perc:.0f}%'.format(perc = 5.0/obj_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 11.0/total_no*100)],
                        fractions = [5.0/obj_no, 11.0/total_no])

    # Create power ups
    world_flipper = power_ups.World_flipper(power_up_space, 
                                                Vector([10.0, 2.0, 10.0]))
    gravity_flipper = power_ups.Gravity_flipper(power_up_space, 
                                                Vector([10.0, 2.0, -10.0]))

    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating objects: {perc:.0f}%'.format(perc = 6.0/obj_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 12.0/total_no*100)],
                        fractions = [6.0/obj_no, 12.0/total_no])

    # Create surfaces
    scene_no = 15
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 0.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 12.0/total_no*100)],
                        fractions = [0.0/scene_no, 12.0/total_no])

    sticky_floor = shapes.Surface(world, static_space, pos = Vector((0.0, 0.0, 7.5)), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0,
                            texture = stars_tex)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 1.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 13.0/total_no*100)],
                        fractions = [1.0/scene_no, 13.0/total_no])

    slippy_floor = shapes.Surface(world, static_space, pos = Vector((0.0, 0.0, -7.5)), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 2.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 14.0/total_no*100)],
                        fractions = [2.0/scene_no, 14.0/total_no])

    wall1 = shapes.Surface(world, static_space, pos = Vector([-15.0, 8.0, 0.0]), 
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            length = 30.0, width = 16.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 3.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 15.0/total_no*100)],
                        fractions = [3.0/scene_no, 15.0/total_no])

    wall2 = shapes.Surface(world, static_space, pos = Vector([10.0, 8.0, 15.0]), 
                            normal = Vector([0.0, 0.0, -1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 50.0, width = 16.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 4.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 16.0/total_no*100)],
                        fractions = [4.0/scene_no, 16.0/total_no])

    door_wall_1 = shapes.Surface(world, static_space, pos = Vector([-9.0, 8.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 12.0, width = 16.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 5.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 17.0/total_no*100)],
                        fractions = [5.0/scene_no, 17.0/total_no])

    door_wall_2 = shapes.Surface(world, static_space, pos = Vector([0.0, 11.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 6.0, width = 14.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 6.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 18.0/total_no*100)],
                        fractions = [6.0/scene_no, 18.0/total_no])

    door_wall_3 = shapes.Surface(world, static_space, pos = Vector([19.0, 8.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 32.0, width = 16.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 7.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 19.0/total_no*100)],
                        fractions = [7.0/scene_no, 19.0/total_no])

    floor_slope = shapes.Surface(world, static_space, pos = Vector([25.0, 4.0, 0.0]), 
                            normal = Vector([-8.0, 20.0, 0.0]).normalize(),
                            forward = Vector([20.0, 8.0, 0.0]).normalize(),
                            length = Vector([20.0, 8.0, 0.0]).norm(), width = 30.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 8.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 20.0/total_no*100)],
                        fractions = [8.0/scene_no, 20.0/total_no])

    roof_slope = shapes.Surface(world, static_space, pos = Vector([25.0, 12.0, 0.0]),
                            normal = Vector([-8.0, -20.0, 0.0]).normalize(),
                            forward = Vector([20.0, -8.0, 0.0]).normalize(),
                            length = Vector([20.0, -8.0, 0.0]).norm(), width = 30.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 9.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 21.0/total_no*100)],
                        fractions = [9.0/scene_no, 21.0/total_no])

    sticky_roof = shapes.Surface(world, static_space, pos = Vector((0.0, 16.0, 7.5)), 
                            normal = Vector([0.0, -1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0,
                            texture = stars_tex)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 10.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 22.0/total_no*100)],
                        fractions = [10.0/scene_no, 22.0/total_no])

    slippy_roof = shapes.Surface(world, static_space, pos = Vector((0.0, 16.0, -7.5)), 
                            normal = Vector([0.0, -1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 11.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 23.0/total_no*100)],
                        fractions = [11.0/scene_no, 23.0/total_no])

    balcony = shapes.Surface(world, static_space, pos = Vector((0.0, 0.0, -20.0)), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 12.0, width = 10.0)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 12.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 24.0/total_no*100)],
                        fractions = [12.0/scene_no, 24.0/total_no])

    fence_1 = shapes.Surface(world, static_space, pos = Vector((-6.0, 0.75, -20.0)), 
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            length = 10.0, width = 1.5)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 13.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 25.0/total_no*100)],
                        fractions = [13.0/scene_no, 25.0/total_no])

    fence_2 = shapes.Surface(world, static_space, pos = Vector((6.0, 0.75, -20.0)), 
                            normal = Vector([-1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, -1.0]),
                            length = 10.0, width = 1.5)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 14.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 26.0/total_no*100)],
                        fractions = [14.0/scene_no, 26.0/total_no])

    fence_3 = shapes.Surface(world, static_space, pos = Vector((0.0, 0.75, -25.0)), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 12.0, width = 1.5)
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Creating scene: {perc:.0f}%'.format(perc = 15.0/scene_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 27.0/total_no*100)],
                        fractions = [15.0/scene_no, 27.0/total_no])

    # Set the color of the surfaces

    # NOTE: It takes A LOT of time to set the colors,
    # since we generate a new display list each time we
    # change color. Better/faster solution?
    col_no = 26

    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 0.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 27.0/total_no*100)],
                        fractions = [0.0/col_no, 27.0/total_no])

    slippy_floor.set_ambient([0.5, 0.5, 0.8, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 1.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 28.0/total_no*100)],
                        fractions = [1.0/col_no, 28.0/total_no])
    slippy_floor.set_diffuse([0.5, 0.5, 0.8, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 2.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 29.0/total_no*100)],
                        fractions = [2.0/col_no, 29.0/total_no])
    

    slippy_roof.set_ambient([0.8, 0.5, 0.5, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 3.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 30.0/total_no*100)],
                        fractions = [3.0/col_no, 30.0/total_no])
    slippy_roof.set_diffuse([0.8, 0.5, 0.5, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 4.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 31.0/total_no*100)],
                        fractions = [4.0/col_no, 31.0/total_no])

    wall1.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 5.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 32.0/total_no*100)],
                        fractions = [5.0/col_no, 32.0/total_no])
    wall1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 6.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 33.0/total_no*100)],
                        fractions = [6.0/col_no, 33.0/total_no])

    wall2.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 7.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 34.0/total_no*100)],
                        fractions = [7.0/col_no, 34.0/total_no])
    wall2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 8.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 35.0/total_no*100)],
                        fractions = [8.0/col_no, 35.0/total_no])

    door_wall_1.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 9.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 36.0/total_no*100)],
                        fractions = [9.0/col_no, 36.0/total_no])
    door_wall_1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 10.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 37.0/total_no*100)],
                        fractions = [10.0/col_no, 37.0/total_no])

    door_wall_2.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 11.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 38.0/total_no*100)],
                        fractions = [11.0/col_no, 38.0/total_no])
    door_wall_2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 12.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 39.0/total_no*100)],
                        fractions = [12.0/col_no, 39.0/total_no])

    door_wall_3.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 13.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 40.0/total_no*100)],
                        fractions = [13.0/col_no, 40.0/total_no])
    door_wall_3.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 14.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 41.0/total_no*100)],
                        fractions = [14.0/col_no, 41.0/total_no])

    floor_slope.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 15.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 42.0/total_no*100)],
                        fractions = [15.0/col_no, 42.0/total_no])
    floor_slope.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 16.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 43.0/total_no*100)],
                        fractions = [16.0/col_no, 43.0/total_no])

    roof_slope.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 17.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 44.0/total_no*100)],
                        fractions = [17.0/col_no, 44.0/total_no])
    roof_slope.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 18.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 45.0/total_no*100)],
                        fractions = [18.0/col_no, 45.0/total_no])

    fence_1.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 19.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 46.0/total_no*100)],
                        fractions = [19.0/col_no, 46.0/total_no])
    fence_1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 20.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 47.0/total_no*100)],
                        fractions = [20.0/col_no, 47.0/total_no])

    fence_2.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 21.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 48.0/total_no*100)],
                        fractions = [21.0/col_no, 48.0/total_no])
    fence_2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 22.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 49.0/total_no*100)],
                        fractions = [22.0/col_no, 49.0/total_no])

    fence_3.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 23.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 50.0/total_no*100)],
                        fractions = [23.0/col_no, 50.0/total_no])
    fence_3.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 24.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 51.0/total_no*100)],
                        fractions = [24.0/col_no, 51.0/total_no])

    balcony.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 25.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 52.0/total_no*100)],
                        fractions = [25.0/col_no, 52.0/total_no])
    balcony.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(textbox_indices = [0, 1], progress_bar_indices = [0, 1],
                        messages = ['Setting colours: {perc:.0f}%'.format(perc = 26.0/col_no*100),
                                    'Total: {perc:.0f}%'.format(perc = 53.0/total_no*100)],
                        fractions = [26.0/col_no, 53.0/total_no])

    # Set friction and bounce
    slippy_floor.set_friction(0.1)
    slippy_floor.set_bounce(0.5)
    sticky_floor.set_friction(10)
    sticky_floor.set_bounce(0.1)
    slippy_roof.set_friction(0.1)
    slippy_roof.set_bounce(0.5)
    sticky_roof.set_friction(10)
    sticky_roof.set_bounce(0.1)

    door = moving_scene.Sliding_door(moving_scene_space, pos = Vector((0.0, 2.0, -15.0)), 
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

    moving_platform = moving_scene.Moving_platform(moving_scene_space, normal = Vector((0.0, 1.0, 0.0)),
                            forward = Vector((0.0, 0.0, 1.0)), width = 5, length = 5,
                            turning_points = (Vector((-12.5, 1.0, 12.5)), Vector((0.0, 10.0, 12.5))))

    # Create lights
    light1 = lights.Light(GL_LIGHT0, Vector((0.0, 5.0, 0.0)),
                        ambient = [0.1, 0.1, 0.1, 1.0],
                        diffuse = [1.0, 1.0, 1.0, 1.0],
                        specular = [1.0, 1.0, 1.0, 1.0])
    light2 = lights.Light(GL_LIGHT2, Vector((8.0, 5.0, 3.0)),
                        ambient = [0.0, 0.0, 0.0, 1.0],
                        diffuse = [0.3, 0.0, 0.0, 1.0],
                        specular = [0.3, 0.0, 0.0, 1.0])
    camera = cameras.Camera()

    start_screen.update(textbox_indices = [0], progress_bar_indices = [0],
                        messages = ['Organizing'], fractions = [0.0])

    # Create player
    player = players.Player(earth)

    # Add all objects that should be drawn to a list
    object_list = [player.get_shape(), sun, moon, mars, box, 
                    sticky_floor, slippy_floor, wall1, wall2, 
                    door_wall_1, door_wall_2, door_wall_3, 
                    floor_slope, roof_slope, slippy_roof,
                    sticky_roof, balcony, fence_1, fence_2, fence_3,
                    world_flipper, gravity_flipper,
                    door, door_button_1, door_button_2,
                    moving_platform]

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
    spaces = (sphere_space, object_space, static_space, power_up_space, interactive_object_space,
            moving_scene_space)

    game = games.Game(world, spaces, player, object_list, 
                    light_list, camera, clock, contact_group, fps)

    # Initialize some constants for the shadow calculations
    #init_graphics.init_shadows(game)

    return game
