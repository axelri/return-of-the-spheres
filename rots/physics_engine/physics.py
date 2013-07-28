import ode
from math_classes import vectors

def update_physics(world, space, contactgroup, player, dt):
    n = 2
    #Run multiple times for smoother simulation
    for i in range(n):
        # Detect collisions and create contact joints
        space.collide((world,contactgroup), near_callback)

        # Simulation step
        world.step(dt/n)

        player.colliding = bool(player.get_shape().body.getNumJoints())

        # Remove all contact joints
        contactgroup.empty()


def near_callback(args, geom1, geom2):
    """Callback function for the collide() method.

    This function checks if the given geoms do collide and
    creates contact joints if they do.

    There is also a homemaid version of rolling rolling_friction. """
    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)

    # Create contact joints
    world,contactgroup = args
    for c in contacts:
        # TODO: Make the friction and bounce coefficients object properties.
        # NOTE: High friction between the cube and the sphere, that's why
        # the sphere 'climbs' the cube when pushing it.
        c.setBounce(0.2)

        if "Sphere" in str(geom1) or "Sphere" in str(geom2):
            # Higher friction for spheres
            c.setMu(5000)
        else:
            c.setMu(2)

        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

    # Homemaid rolling friction

    # NOTE: This part makes the cube behave strangely, would be better to apply
    # only to spheres.
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
                ang_vel = vectors.Vector(list(bodies[i].getAngularVel()))
                rolling_friction = 0.5
                bodies[i].addTorque((-ang_vel*rolling_friction).value)