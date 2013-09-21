from math import sqrt

import ode

from math_classes.vectors import Vector

# NOTE: Replaced all the calls to geom.__getattribute__('object')
# with geom.object. Is it readable?

def update_physics(game, iterations = 2):

    sphere_space = game.get_sphere_space()
    object_space = game.get_object_space()
    static_space = game.get_static_space()
    power_up_space = game.get_power_up_space()
    interactive_object_space = game.get_interactive_object_space()
    moving_scene_space = game.get_moving_scene_space()

    world = game.get_world()
    contact_group = game.get_contact_group()
    dt = game.get_dt()
    player = game.get_player()

    #Run multiple times for smoother simulation
    for i in range(iterations):

        # Detect collisions and create contact joints
        # sphere-static collisions
        ode.collide2(sphere_space, static_space, game, sphere_static_callback)
        # object-static collisions
        ode.collide2(object_space, static_space, game, object_static_callback)
        # sphere-moving scene collisions
        ode.collide2(sphere_space, moving_scene_space, game, sphere_moving_scene_callback)
        # object-moving scene collisions
        ode.collide2(object_space, moving_scene_space, game, object_moving_scene_callback)
        # sphere-object collisions
        ode.collide2(sphere_space, object_space, game, sphere_object_callback)
        # sphere-sphere collisions
        sphere_space.collide(game, sphere_sphere_callback)
        # object-object collisions
        object_space.collide(game, object_object_callback)
        # player-power up collisions
        ode.collide2(player.get_shape().get_geom(), power_up_space, 
                        game, player_power_up_callback)

        # Manual collision detection for interactive objects
        # (Couldn't make them "unpressed" properly any other way)
        # TODO: Fix that
        for i in range(interactive_object_space.getNumGeoms()):
            obj_geom = interactive_object_space.getGeom(i)
            obj = obj_geom.object

            contacts = ode.collide(player.get_shape().get_geom(), obj_geom)

            if contacts:
                obj.set_pressed(True)
            else:
                obj.set_pressed(False)

            pressed = obj.get_pressed()
            pressed_last_frame = obj.get_pressed_last_frame()

            if pressed and not pressed_last_frame:
                obj.collide_func()

            obj.set_pressed_last_frame(obj.get_pressed())


        # Simulation step
        world.step(dt/iterations)

        # Check if the player is colliding
        # TODO: Move? Is there a prettier way to check this?
        player.colliding = bool(player.get_shape().get_body().getNumJoints())

        # Remove all contact joints
        contact_group.empty()

        # Call power up functions
        # NOTE: Couldn't find a better place to put this, is there any?
        for i in range(power_up_space.getNumGeoms()):
            power_up_geom = power_up_space.getGeom(i)
            power_up = power_up_geom.object
            if power_up.get_collided():
                power_up.collide_func(game)


def sphere_static_callback(game, sphere, static):
    ''' Callback function for collisions between spheres
        and the static environment. This function checks
        if the given geoms do collide and creates contact
        joints if they do. '''

    contact_group = game.get_contact_group()
    world = game.get_world()
    sphere_shape = sphere.object
    static_shape = static.object
    sphere_body = sphere.getBody()
    static_body = static.getBody()

    # Check if the objects do collide
    contacts = ode.collide(sphere, static)

    # Create contact joints
    for c in contacts:
        bounce = sqrt(sphere_shape.get_bounce() * static_shape.get_bounce())
        friction = sqrt(sphere_shape.get_friction() * static_shape.get_friction()) * 1000
        c.setBounce(bounce)
        c.setMu(friction)

        j = ode.ContactJoint(world, contact_group, c)
        j.attach(sphere_body, static_body)

    # Rolling friction
    if contacts:
        ang_vel = Vector(sphere_body.getAngularVel())
        rolling_friction = sqrt(sphere_shape.get_rolling_friction() * static_shape.get_friction())
        sphere_body.addTorque((-ang_vel * rolling_friction).value)

def object_static_callback(game, obj, static):
    ''' Callback function for collisions between objects
        and the static environment. This function checks
        if the given geoms do collide and creates contact
        joints if they do. '''

    contact_group = game.get_contact_group()
    world = game.get_world()
    obj_shape = obj.object
    static_shape = static.object

    # Check if the objects do collide
    contacts = ode.collide(obj, static)

    # Create contact joints
    for c in contacts:
        bounce = sqrt(obj_shape.get_bounce() * static_shape.get_bounce())
        friction = sqrt(obj_shape.get_friction() * static_shape.get_friction())
        c.setBounce(bounce)
        c.setMu(friction)
        j = ode.ContactJoint(world, contact_group, c)
        j.attach(obj.getBody(), static.getBody())

def sphere_object_callback(game, sphere, obj):
    ''' Callback function for collisions between spheres
        and objects. This function checks if the given geoms
        do collide and creates contact joints if they do. '''

    # TODO: Add rolling friction

    contact_group = game.get_contact_group()
    world = game.get_world()
    sphere_shape = sphere.object
    obj_shape = obj.object

    # Check if the objects do collide
    contacts = ode.collide(sphere, obj)

    # Create contact joints
    for c in contacts:
        bounce = sqrt(sphere_shape.get_bounce() * obj_shape.get_bounce())
        friction = sqrt(sphere_shape.get_friction() * obj_shape.get_friction()) * 0.1
        c.setBounce(bounce)
        c.setMu(friction)
        j = ode.ContactJoint(world, contact_group, c)
        j.attach(sphere.getBody(), obj.getBody())

def sphere_sphere_callback(game, sphere1, sphere2):
    ''' Callback function for collisions between spheres. 
        This function checks if the given geoms do collide
        and creates contact joints if they do. '''

    contact_group = game.get_contact_group()
    world = game.get_world()
    sphere1_shape = sphere1.object
    sphere2_shape = sphere2.object

    # Check if the objects do collide
    contacts = ode.collide(sphere1, sphere2)

    # Create contact joints
    for c in contacts:
        bounce = sqrt(sphere1_shape.get_bounce() * sphere2_shape.get_bounce())
        friction = sqrt(sphere1_shape.get_friction() * sphere2_shape.get_friction()) * 0.1
        c.setBounce(bounce)
        c.setMu(friction)
        j = ode.ContactJoint(world, contact_group, c)
        j.attach(sphere1.getBody(), sphere2.getBody())

def object_object_callback(game, obj1, obj2):
    ''' Callback function for collisions between objects. 
        This function checks if the given geoms do collide
        and creates contact joints if they do. '''

    contact_group = game.get_contact_group()
    world = game.get_world()
    obj1_shape = obj1.object
    obj2_shape = obj2.object

    # Check if the objects do collide
    contacts = ode.collide(obj1, obj2)

    # Create contact joints
    for c in contacts:
        bounce = sqrt(obj1_shape.get_bounce() * obj2_shape.get_bounce())
        friction = sqrt(obj1_shape.get_friction() * obj2_shape.get_friction())
        c.setBounce(bounce)
        c.setMu(friction)

        j = ode.ContactJoint(world, contact_group, c)
        j.attach(obj1.getBody(), obj2.getBody())

def player_power_up_callback(game, player_geom, power_up_geom):
    ''' Callback function for collisions between the
        player and power ups. If they have collided,
        the power up's collide_func is called. '''

    power_up = power_up_geom.object

    contacts = ode.collide(player_geom, power_up_geom)

    if contacts:
        #power_up.collide_func(game)
        # NOTE: Calling the function from here makes the 
        # game crash since we are not allowed to remove 
        # any geom from a space that is currently checked
        # for collisions. Set a collision flag instead 
        # and call the function later.
        power_up.set_collided(True)

def player_interactive_object_callback(game, player_geom, obj_geom):

    obj = obj_geom.object

    contacts = ode.collide(player_geom, obj_geom)

    obj.set_pressed(False)

    if contacts:
        obj.set_pressed(True)

# TODO: Make this work |
#                      V

def sphere_moving_scene_callback(game, sphere, scene):
    ''' Callback function for collisions between spheres
        and moving scene objects. This function checks
        if the given geoms do collide and creates contact
        joints if they do. '''

    contact_group = game.get_contact_group()
    world = game.get_world()
    sphere_shape = sphere.object
    scene_shape = scene.object
    sphere_body = sphere.getBody()
    scene_body = scene.getBody()

    #scene_vel = scene_shape.get_velocity()
    vel = scene_shape.get_velocity()

    # Check if the objects do collide
    contacts = ode.collide(sphere, scene)

    # Create contact joints
    for c in contacts:
        # Set friction and bounce
        bounce = sqrt(sphere_shape.get_bounce() * scene_shape.get_bounce())
        friction = sqrt(sphere_shape.get_friction() * scene_shape.get_friction()) * 1000
        c.setBounce(bounce)
        c.setMu(friction)

        ### Hack to add friction (kind of...)
        # Doesn't work as it should at all yet, very buggy...
        #pos, normal, depth, geom1, geom2 = c.getContactGeomParams()

        #sphere_vel = sphere_shape.get_vel()
        #rel_vel = scene_vel - sphere_vel

        #pos = sphere_shape.get_pos() - Vector(normal) * sphere_shape.get_radius()

        #print 'pos: ', pos
        #print 'normal: ', normal
        #print 'rel_vel: ', rel_vel
        #print

        #sphere_body.addForceAtRelPos((rel_vel * 5).value, pos.value)
        


        ### Adjust the velocity of the contact
        pos, normal, depth, geom1, geom2 = c.getContactGeomParams()
        normal = Vector(normal)
        dir_1 = Vector((1.0, 0.0, 0.0)).cross(normal)
        if dir_1.norm() < 0.1:
            dir_1 = Vector((0.0, 0.0, 1.0)).cross(normal)
        dir_1 = dir_1.normalize()
        dir_2 = normal.cross(dir_1)

        c.setFDir1(dir_1.value)

        # #print 'Number of contacts: ', len(contacts)

        # print 'Normal: ', normal
        # print 'dir_1: ', dir_1
        # print 'dir_2: ', dir_2

        vel_1 = vel.dot(dir_1)
        vel_2 = vel.dot(dir_2)

        # print 'vel: ', vel

        # print 'vel_1 before: ', c.getMotion1()
        # print 'vel_2 before: ', c.getMotion2()

        # # Don't seem to do anything... What's wrong?
        c.setMotion1(vel_1)
        c.setMotion2(vel_2)

        # print 'vel_1 after: ', c.getMotion1()
        # print 'vel_2 after: ', c.getMotion2()
        # print

        j = ode.ContactJoint(world, contact_group, c)
        j.attach(sphere_body, scene_body)

    # Rolling friction
    if contacts:
        ang_vel = Vector(sphere_body.getAngularVel())
        rolling_friction = sqrt(sphere_shape.get_rolling_friction() * scene_shape.get_friction())
        sphere_body.addTorque((-ang_vel * rolling_friction).value)

def object_moving_scene_callback(game, obj, scene):
    ''' Callback function for collisions between objects
        and moving scene objects. This function checks
        if the given geoms do collide and creates contact
        joints if they do. '''

    contact_group = game.get_contact_group()
    world = game.get_world()
    obj_shape = obj.object
    scene_shape = scene.object

    vel = scene_shape.get_velocity()

    # Check if the objects do collide
    contacts = ode.collide(obj, scene)

    # Create contact joints
    for c in contacts:
        bounce = sqrt(obj_shape.get_bounce() * scene_shape.get_bounce())
        friction = sqrt(obj_shape.get_friction() * scene_shape.get_friction())
        c.setBounce(bounce)
        c.setMu(friction)

        # Adjust the velocity of the contact
        pos, normal, depth, geom1, geom2 = c.getContactGeomParams()
        normal = Vector(normal)
        dir_1 = Vector(c.getFDir1())
        dir_2 = normal.cross(dir_1)

        vel_1 = vel.dot(dir_1)
        vel_2 = vel.dot(dir_2)

        c.setMotion1(vel_1)
        c.setMotion2(vel_2)
        
        j = ode.ContactJoint(world, contact_group, c)
        j.attach(obj.getBody(), scene.getBody())
