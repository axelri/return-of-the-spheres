from math import sqrt

import ode

from math_classes.vectors import Vector

# NOTE: A bit ugly with __getattribute__() (we shouldn't call 
# internal methods). Solution?

def update_physics(game, iterations = 2):

    sphere_space = game.get_sphere_space()
    object_space = game.get_object_space()
    static_space = game.get_static_space()
    world = game.get_world()
    contact_group = game.get_contact_group()
    dt = game.get_dt()

    #Run multiple times for smoother simulation
    for i in range(iterations):

        # Detect collisions and create contact joints
        # sphere-static collisions
        ode.collide2(sphere_space, static_space, game, sphere_static_callback)
        # object-static collisions
        ode.collide2(object_space, static_space, game, object_static_callback)
        # sphere-object collisions
        ode.collide2(sphere_space, object_space, game, sphere_object_callback)
        # sphere-sphere collisions
        sphere_space.collide(game, sphere_sphere_callback)
        # object-object collisions
        object_space.collide(game, object_object_callback)

        # Simulation step
        world.step(dt/iterations)

        # Check if the player is colliding
        # TODO: Move? Is there a prettier way to check this?
        game._player.colliding = bool(game._player.get_shape().get_body().getNumJoints())

        # Remove all contact joints
        contact_group.empty()

def sphere_static_callback(game, sphere, static):
    ''' Callback function for collisions between spheres
        and the static environment. This function checks
        if the given geoms do collide and creates contact
        joints if they do. '''

    contact_group = game.get_contact_group()
    world = game.get_world()
    sphere_shape = sphere.__getattribute__('shape')
    static_shape = static.__getattribute__('shape')
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
    obj_shape = obj.__getattribute__('shape')
    static_shape = static.__getattribute__('shape')

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
    sphere_shape = sphere.__getattribute__('shape')
    obj_shape = obj.__getattribute__('shape')

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
    sphere1_shape = sphere1.__getattribute__('shape')
    sphere2_shape = sphere2.__getattribute__('shape')

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
    obj1_shape = obj1.__getattribute__('shape')
    obj2_shape = obj2.__getattribute__('shape')

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
