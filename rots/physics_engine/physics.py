import ode
from math_classes.vectors import Vector

# TODO: Test if we can solve the problem with different contact
# coefficients for different object by using several spaces, one
# for each type of object.

# NOTE:
# geom.setData() and geom.getData() could enable us to tell which
# geom belongs to which shape (e.g. shape._geom.setData(shape)?)
# geom.getClass() can be used instead of the ugly solution below.
# use hashspace instead of simplespace

def update_physics(game, iterations = 2):

    object_space = game.get_object_space()
    scene_space = game.get_scene_space()
    world = game.get_world()
    object_contactgroup = game.get_object_contactgroup()
    scene_contactgroup = game.get_scene_contactgroup()
    dt = game.get_dt()

    #Run multiple times for smoother simulation
    for i in range(iterations):
        # Detect collisions and create contact joints
        # object-object collisions
        object_space.collide(game, object_near_callback)
        # object-scene collisions
        ode.collide2(object_space, scene_space, game, object_scene_near_callback)

        # Simulation step
        world.step(dt/iterations)

        game._player.colliding = bool(game._player.get_shape().get_body().getNumJoints())

        # Remove all contact joints
        object_contactgroup.empty()
        scene_contactgroup.empty()

# TODO: Different callback functions for objects and scene
# (Right now they are copies of each other, just wanted to test if this worked)

def object_near_callback(game, geom1, geom2):
    """Callback function for the collide() method.

    This function checks if the given geoms do collide and
    creates contact joints if they do.

    There is also a homemaid version of rolling rolling_friction. """

    object_contactgroup = game.get_object_contactgroup()
    world = game.get_world()

    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)

    # Create contact joints
    for c in contacts:
        # TODO: Make the friction and bounce coefficients object properties.
        # NOTE: High friction between the cube and the sphere, that's why
        # the sphere 'climbs' the cube when pushing it.
        c.setBounce(0.2)

        if "Sphere" in str(geom1) and "Sphere" in str(geom2):
            # Low friction for two spheres
            c.setMu(0.1)
        elif "Sphere" in str(geom1) or "Sphere" in str(geom2):
            # Higher friction for spheres
            c.setMu(5000)
        else:
            # Lower friction for other things
            c.setMu(2)

        j = ode.ContactJoint(world, object_contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

    # Homemaid rolling friction

    # TODO: Add spinning friction
    # TODO: Make this part prettier

    if contacts != []:
        geoms = [geom1, geom2]
        bodies = [geom1.getBody(), geom2.getBody()]
        
        if bodies[0]:
            num_joints1 = bodies[0].getNumJoints()
        else:
            num_joints1 = 0
        if bodies[1]:
            num_joints2 = bodies[1].getNumJoints()
        else:
            num_joints2 = 0

        num_joints = [num_joints1, num_joints2]

        for i in range(len(num_joints)):
        #for num_joint in num_joints, body in bodies:
        # The last 'and' is a bit ugly, better solution?
            if num_joints[i] != 0 and bodies[i] and "Sphere" in str(geoms[i]):
                ang_vel = Vector(list(bodies[i].getAngularVel()))
                rolling_friction = 0.5
                bodies[i].addTorque((-ang_vel*rolling_friction).value)

def object_scene_near_callback(game, geom1, geom2):
    """Callback function for the collide() method.

    This function checks if the given geoms do collide and
    creates contact joints if they do.

    There is also a homemaid version of rolling rolling_friction. """

    scene_contactgroup = game.get_scene_contactgroup()
    world = game.get_world()

    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)

    # Create contact joints
    for c in contacts:
        # TODO: Make the friction and bounce coefficients object properties.
        # NOTE: High friction between the cube and the sphere, that's why
        # the sphere 'climbs' the cube when pushing it.
        c.setBounce(0.2)

        if "Sphere" in str(geom1) and "Sphere" in str(geom2):
            # Low friction for two spheres
            c.setMu(0.1)
        elif "Sphere" in str(geom1) or "Sphere" in str(geom2):
            # Higher friction for spheres
            c.setMu(5000)
        else:
            # Lower friction for other things
            c.setMu(2)

        j = ode.ContactJoint(world, scene_contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

    # Homemaid rolling friction

    # TODO: Add spinning friction
    # TODO: Make this part prettier

    if contacts != []:
        geoms = [geom1, geom2]
        bodies = [geom1.getBody(), geom2.getBody()]
        
        if bodies[0]:
            num_joints1 = bodies[0].getNumJoints()
        else:
            num_joints1 = 0
        if bodies[1]:
            num_joints2 = bodies[1].getNumJoints()
        else:
            num_joints2 = 0

        num_joints = [num_joints1, num_joints2]

        for i in range(len(num_joints)):
        #for num_joint in num_joints, body in bodies:
        # The last 'and' is a bit ugly, better solution?
            if num_joints[i] != 0 and bodies[i] and "Sphere" in str(geoms[i]):
                ang_vel = Vector(list(bodies[i].getAngularVel()))
                rolling_friction = 0.5
                bodies[i].addTorque((-ang_vel*rolling_friction).value)
