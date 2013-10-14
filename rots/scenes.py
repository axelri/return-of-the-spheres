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
    view, loading_image = loading_screen_data
    width = view.get_width()
    heigth = view.get_heigth()
    aspect_angle = view.get_aspect_angle()
    start_screen = loading_screen.Loading_screen(loading_image, width, heigth, aspect_angle)

    # TODO: Place them better
    module_textbox = start_screen.add_textbox('test.ttf', 0.035, 0.35, 0.5, [1,0,0])
    total_textbox = start_screen.add_textbox('test.ttf', 0.035, 0.35, 0.38, [0,1,0])
    module_progress_bar = start_screen.add_progress_bar(0.02, 0.2, 0.5, 0.45, [1,0,0,1])
    total_progress_bar = start_screen.add_progress_bar(0.02, 0.2, 0.5, 0.35, [0,1,0,1])

    module_textbox.set_message('Creating world', 'plain text')
    module_progress_bar.disable()
    total_textbox.set_message('Total', 'percentage', denominator = 53)
    total_progress_bar.set_denominator(53)
    start_screen.update()

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

    # Load textures
    module_textbox.set_message('Loading textures', 'percentage', denominator = 6)
    module_progress_bar.enable()
    module_progress_bar.set_denominator(6)
    start_screen.update()

    earth_tex = textures.load_texture('celestial_bodies/earth_big.jpg')
    start_screen.update(counter_increase = 1)

    moon_tex = textures.load_texture('celestial_bodies/moon-4k.png')
    start_screen.update(counter_increase = 1)

    stars_tex = textures.load_texture('stars_big.jpg')
    start_screen.update(counter_increase = 1)

    sun_tex = textures.load_texture('celestial_bodies/th_sun.png')
    start_screen.update(counter_increase = 1)

    mars_tex = textures.load_texture('celestial_bodies/Mars_2k-050104.png')
    start_screen.update(counter_increase = 1)

    puppy_tex = textures.load_texture('puppy.jpeg')
    start_screen.update(counter_increase = 1)

    # Create shapes
    module_textbox.set_message('Creating objects', 'percentage', denominator = 6)
    module_textbox.reset_counter()
    module_progress_bar.reset_counter()
    module_progress_bar.set_denominator(6)
    start_screen.update()

    earth = shapes.Sphere(world, sphere_space, pos = Vector([0.0, 5.0, 0.0]), 
                            radius = 1.0, texture = earth_tex)
    start_screen.update(counter_increase = 1)

    moon = shapes.Sphere(world, sphere_space, pos = Vector([-3.0, 5.0, -3.0]),
                            radius = 0.27, mass = 0.5, texture = moon_tex)
    start_screen.update(counter_increase = 1)

    sun = shapes.Sphere(world, sphere_space, pos = Vector([5.0, 5.0, 5.0]), 
                            radius = 1.5, texture = sun_tex, mass = 5)
    start_screen.update(counter_increase = 1)

    mars = shapes.Sphere(world, sphere_space, pos = Vector([-3.0, 5.0, 3.0]),
                            radius = 0.53, mass = 1, texture = mars_tex)
    start_screen.update(counter_increase = 1)

    sun.set_emissive([1.0, 1.0, 1.0, 1.0])

    box = shapes.Box(world, object_space, pos = Vector([3.0, 5.0, 0.0]), x_size = 2,
                        y_size = 3, z_size = 1.5, texture = puppy_tex, mass = 2)
    start_screen.update(counter_increase = 1)

    # Create power ups
    world_flipper = power_ups.World_flipper(power_up_space, 
                                                Vector([10.0, 2.0, 10.0]))
    gravity_flipper = power_ups.Gravity_flipper(power_up_space, 
                                                Vector([10.0, 2.0, -10.0]))

    start_screen.update(counter_increase = 1)

    # Create surfaces
    module_textbox.set_message('Creating scene', 'percentage', denominator = 15)
    module_textbox.reset_counter()
    module_progress_bar.reset_counter()
    module_progress_bar.set_denominator(15)
    start_screen.update()

    sticky_floor = shapes.Surface(world, static_space, pos = Vector((0.0, 0.0, 7.5)), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0,
                            texture = stars_tex)
    start_screen.update(counter_increase = 1)

    slippy_floor = shapes.Surface(world, static_space, pos = Vector((0.0, 0.0, -7.5)), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0)
    start_screen.update(counter_increase = 1)

    wall1 = shapes.Surface(world, static_space, pos = Vector([-15.0, 8.0, 0.0]), 
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            length = 30.0, width = 16.0)
    start_screen.update(counter_increase = 1)

    wall2 = shapes.Surface(world, static_space, pos = Vector([10.0, 8.0, 15.0]), 
                            normal = Vector([0.0, 0.0, -1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 50.0, width = 16.0)
    start_screen.update(counter_increase = 1)

    door_wall_1 = shapes.Surface(world, static_space, pos = Vector([-9.0, 8.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 12.0, width = 16.0)
    start_screen.update(counter_increase = 1)

    door_wall_2 = shapes.Surface(world, static_space, pos = Vector([0.0, 11.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 6.0, width = 14.0)
    start_screen.update(counter_increase = 1)

    door_wall_3 = shapes.Surface(world, static_space, pos = Vector([19.0, 8.0, -15.0]), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 32.0, width = 16.0)
    start_screen.update(counter_increase = 1)

    floor_slope = shapes.Surface(world, static_space, pos = Vector([25.0, 4.0, 0.0]), 
                            normal = Vector([-8.0, 20.0, 0.0]).normalize(),
                            forward = Vector([20.0, 8.0, 0.0]).normalize(),
                            length = Vector([20.0, 8.0, 0.0]).norm(), width = 30.0)
    start_screen.update(counter_increase = 1)

    roof_slope = shapes.Surface(world, static_space, pos = Vector([25.0, 12.0, 0.0]),
                            normal = Vector([-8.0, -20.0, 0.0]).normalize(),
                            forward = Vector([20.0, -8.0, 0.0]).normalize(),
                            length = Vector([20.0, -8.0, 0.0]).norm(), width = 30.0)
    start_screen.update(counter_increase = 1)

    sticky_roof = shapes.Surface(world, static_space, pos = Vector((0.0, 16.0, 7.5)), 
                            normal = Vector([0.0, -1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0,
                            texture = stars_tex)
    start_screen.update(counter_increase = 1)

    slippy_roof = shapes.Surface(world, static_space, pos = Vector((0.0, 16.0, -7.5)), 
                            normal = Vector([0.0, -1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 30.0, width = 15.0)
    start_screen.update(counter_increase = 1)

    balcony = shapes.Surface(world, static_space, pos = Vector((0.0, 0.0, -20.0)), 
                            normal = Vector([0.0, 1.0, 0.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 12.0, width = 10.0)
    start_screen.update(counter_increase = 1)

    fence_1 = shapes.Surface(world, static_space, pos = Vector((-6.0, 0.75, -20.0)), 
                            normal = Vector([1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, 1.0]),
                            length = 10.0, width = 1.5)
    start_screen.update(counter_increase = 1)

    fence_2 = shapes.Surface(world, static_space, pos = Vector((6.0, 0.75, -20.0)), 
                            normal = Vector([-1.0, 0.0, 0.0]),
                            forward = Vector([0.0, 0.0, -1.0]),
                            length = 10.0, width = 1.5)
    start_screen.update(counter_increase = 1)

    fence_3 = shapes.Surface(world, static_space, pos = Vector((0.0, 0.75, -25.0)), 
                            normal = Vector([0.0, 0.0, 1.0]),
                            forward = Vector([1.0, 0.0, 0.0]),
                            length = 12.0, width = 1.5)
    start_screen.update(counter_increase = 1)

    # Set the color of the surfaces

    # NOTE: It takes A LOT of time to set the colors,
    # since we generate a new display list each time we
    # change color. Better/faster solution?

    module_textbox.set_message('Setting colours', 'percentage', denominator = 26)
    module_textbox.reset_counter()
    module_progress_bar.reset_counter()
    module_progress_bar.set_denominator(26)
    start_screen.update()

    slippy_floor.set_ambient([0.5, 0.5, 0.8, 1.0])
    start_screen.update(counter_increase = 1)
    slippy_floor.set_diffuse([0.5, 0.5, 0.8, 1.0])
    start_screen.update(counter_increase = 1)
    

    slippy_roof.set_ambient([0.8, 0.5, 0.5, 1.0])
    start_screen.update(counter_increase = 1)
    slippy_roof.set_diffuse([0.8, 0.5, 0.5, 1.0])
    start_screen.update(counter_increase = 1)

    wall1.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    wall1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    wall2.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    wall2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    door_wall_1.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    door_wall_1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    door_wall_2.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    door_wall_2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    door_wall_3.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    door_wall_3.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    floor_slope.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    floor_slope.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    roof_slope.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    roof_slope.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    fence_1.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    fence_1.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    fence_2.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    fence_2.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    fence_3.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    fence_3.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

    balcony.set_ambient([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)
    balcony.set_diffuse([0.0, 0.0, 0.2, 1.0])
    start_screen.update(counter_increase = 1)

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

    module_textbox.set_message('Organizing', 'plain text')
    module_progress_bar.disable()
    start_screen.update()

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
                    light_list, camera, clock, contact_group, fps, view)

    # Initialize some constants for the shadow calculations
    #init_graphics.init_shadows(game)

    return game
