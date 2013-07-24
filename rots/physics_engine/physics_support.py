import ode
from math_classes import vectors

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
        c.setBounce(0.2)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

    #Homemaid rolling friction

    #TODO: Add spinning friction
    #TODO: Make this part prettier

    if contacts != []:
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
            if num_joints[i] != 0 and bodies[i]:
                ang_vel = vectors.Vector(list(bodies[i].getAngularVel()))
                rolling_friction = 0.5
                bodies[i].addTorque((-ang_vel*rolling_friction).value)