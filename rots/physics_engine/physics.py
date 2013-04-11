import numbers
#import time

import broadphase
import narrowphase
import collisions
import shapes
import games
from tensors import vectors, quaternions


GRAVITY = vectors.Vector([0.0, -10.0, 0.0])
dt = 0.005

#                                (1+e)(relv.norm)
#j =------------------------------------------------------------------------------
#    norm.norm(1/Mass0 + 1/Mass1) + (sqr(r0 x norm) / Inertia0) + (sqr(r1 x norm) / Inertia1)

def collision_response(shape1, shape2, collisionInfo):
    #print 'Entered collision response'
    assert isinstance(shape1, shapes.Shape), 'Input must be a Shape object'
    assert isinstance(shape2, shapes.Shape), 'Input must be a Shape object'
    assert isinstance(collisionInfo, tuple), 'Input must be a tuple'
    assert len(collisionInfo) == 3, 'CollisionInfo must be of length 3'

    collisionPoint, normal, depth = collisionInfo

    assert isinstance(collisionPoint, vectors.Vector), \
           'Input must be a vector'
    assert isinstance(normal, vectors.Vector), \
           'Input must be a vector'
    assert isinstance(depth, numbers.Number), \
           'Input must be a number'

    # TODO: There is a bug causing the shapes to be considered as moving apart
    # even though they are not, thus returning without applying any impulse.
    # This causes the shapes to fall through eachother.

    #print 'Normal before:', normal
    if normal.dot(shape1.get_pos() - shape2.get_pos()) < 0:
        # It's pointing the wrong way
        normal *= -1.0
    #print 'Normal after:', normal

    # The inverted inertia matrices of the two shapes
    invInertia1 = shape1.get_invInertia()
    invInertia2 = shape2.get_invInertia()

    # The inverted masses of the two objects
    invMass1 = 1.0 / shape1.get_mass()
    invMass2 = 1.0 / shape2.get_mass()

    if invMass1 + invMass2 == 0.0:
        # Both objects are immobile
        #print 'Immobile'
        return

    # The vectors from the collision point to the respective centra of the shapes
    r1 = collisionPoint - shape1.get_pos()
    r2 = collisionPoint - shape2.get_pos()

    # The velocities of the collision point on the two shapes    
    v1 = shape1.get_velocity() + shape1.get_angular_velocity().cross(r1)
    v2 = shape2.get_velocity() + shape2.get_angular_velocity().cross(r2)

    # The relative velocity
    relVel = v1 - v2

    # If the shapes are moving away from eachother we don't need to apply an impulse
    # TODO: There is a bug when rolling over edges that causes the shapes
    # to be considered as moving apart, even though they are not. This is
    # probably because the sphere is rolling and falling at the same time, and
    # therefore the point of collision is moving upwards, despite the
    # fact that the sphere is moving downwards. Fix.
    relMov = - relVel.dot(normal)
    #print 'relVel:', relVel
    #print 'relMov:', relMov 
    if relMov < -0.01:
        #print 'Moving apart'
        #print 'Normal:', normal
        #print 'relVel:', relVel
        #print 'relMov:', relMov
        #print 'v1:', v1
        #print 'r1:', r1
        #print 'angVel:', shape1.get_angular_velocity()
        #print 'colPoint:', collisionPoint
        #print 'pos:', shape1.get_pos()
        #print ''
        return

    # NORMAL Impulse

    e = 0.5 # Coefficient of restitution

    normalInert1 = r1.triple_product_2(normal, r1).left_matrix_mult(invInertia1)
    normalInert2 = r2.triple_product_2(normal, r2).left_matrix_mult(invInertia2)

    normalImpulse = -(1+e)*relVel.dot(normal)/ \
              (invMass1 + invMass2 + (normalInert1 + normalInert2).dot(normal))
    

    # Hack fix to stop sinking
    #print 'Normal impulse before', normalImpulse
    normalImpulse += depth*1.0
    #print 'Normal impulse after', normalImpulse

    #print 'Velocity before for {shape} : {value}'\
    #      .format(shape = shape1.__class__.__name__,
    #              value = shape1.get_velocity())
    #print 'Velocity before for {shape} : {value}'\
    #      .format(shape = shape2.__class__.__name__,
    #              value = shape2.get_velocity())

    shape1.add_velocity(normal * normalImpulse * invMass1)
    shape2.add_velocity(normal * normalImpulse * invMass2 * -1.0)

    #print 'Velocity after for {shape} : {value}'\
    #      .format(shape = shape1.__class__.__name__,
    #              value = shape1.get_velocity())
    #print 'Velocity after for {shape} : {value}'\
    #      .format(shape = shape2.__class__.__name__,
    #              value = shape2.get_velocity())

    #print ''

    shape1.add_angular_velocity(r1.cross(normal*normalImpulse).\
                                left_matrix_mult(invInertia1))
    shape2.add_angular_velocity(r2.cross(normal*normalImpulse).\
                                left_matrix_mult(invInertia2))

    # TANGENT Impulse Code

    # Work out our tangent vector, with is perpendicular
    # to our collision normal

    tangent = (relVel - normal * relVel.dot(normal))
    if tangent.is_not_zero():
        tangent = tangent.normalize()
        if tangent == None:
            tangent = vectors.Vector()
    tangDiv = invMass1 + invMass2 + tangent.dot(r1.cross(tangent).left_matrix_mult(invInertia1).cross(r1) + \
                                                r2.cross(tangent).left_matrix_mult(invInertia2).cross(r2))

    tangentImpulse = -(relVel.dot(tangent))/tangDiv

    shape1.add_velocity(normal * tangentImpulse * invMass1)
    shape2.add_velocity(normal * tangentImpulse * invMass2 * -1.0)

    shape1.add_angular_velocity(r1.cross(tangent*tangentImpulse).\
                                left_matrix_mult(invInertia1))
    shape2.add_angular_velocity(r2.cross(tangent*tangentImpulse).\
                                left_matrix_mult(invInertia2))




def linear_collision_response(shape1, shape2, collisionInfo):
    assert isinstance(shape1, shapes.Shape), 'Input must be a Shape object'
    assert isinstance(shape2, shapes.Shape), 'Input must be a Shape object'
    assert isinstance(collisionInfo, tuple), 'Input must be a tuple'
    assert len(collisionInfo) == 3, 'CollisionInfo must be of length 3'

    collisionPoint, penetrationNormal, penetrationDepth = collisionInfo

    assert isinstance(collisionPoint, vectors.Vector), \
           'Input must be a vector'
    assert isinstance(penetrationNormal, vectors.Vector), \
           'Input must be a vector'
    assert isinstance(penetrationDepth, numbers.Number), \
           'Input must be a number'

    if penetrationNormal.dot(shape2.get_pos() - shape1.get_pos()) < 0:
        # It's pointing the wrong way
        penetrationNormal *= -1.0

    mass1 = shape1.get_mass()
    mass2 = shape2.get_mass()

    invMass1 = 1.0/shape1.get_mass()
    invMass2 = 1.0/shape2.get_mass()

    relativeVel = shape1.get_velocity() - shape2.get_velocity()

    if relativeVel.dot(penetrationNormal) < 0:
        # They are moving apart, no need to apply an impulse
        return
    
    e = 0.0     # coefficient of elasticity

    v_ab = relativeVel
    n = penetrationNormal   

    impulse = -(1+e)*v_ab.dot(n)/((invMass1+invMass2)*n.dot(n))

    #print 'impulse before:', impulse
    # Hack to prevent sinking
    impulse -= penetrationDepth*1.0
    #print 'depth:', penetrationDepth
    #print 'impulse after:', impulse
    shape1.add_velocity(n*impulse*invMass1)
    shape2.add_velocity(n*impulse*invMass2*(-1.0))


def update_physics(game):
    ''' Updates all physics in the game; takes all the objects in
        the game, calculates collisions etc and moves them to their
        new locations.'''
    assert isinstance(game, games.Game), 'Input must be a game object'
    # TODO: Make it have an input called dt, which gives it the
    # timestep it should simulate
    # TODO: Add broadphase collision detection, for example
    # check_collision = collisions.broadphase(shape1, shape2)
    # if check_collision:
    #     collided, collisionInfo = collisions.GJK(shape1, shape2)
    # broadphase should return a boolean; True if the shapes should be
    # passed on to narrowphase, False otherwise.
    # TODO: Add octrees/something like that? This broadphase algorithm
    # works, but I think we can enhance it.
    # NOTE: Broadphase added
    #print 'Entered loop at', time.clock()
    player, objectList, sceneList, lightList = game.get_objects()
    #print ''
    for item in objectList:
        #print 'Checking collision with item:', item

        check_collision = broadphase.shape_shape(player, item)
        if check_collision:
            collided, collisionInfo = collisions.GJK(player, item)
        else:
            collided, collisionInfo = False, None

        if collided:
            #print 'Player collided with item'
            collision_response(player, item, collisionInfo)

        for elem in sceneList:
            check_collision = broadphase.shape_surface(item, elem)
            if check_collision:
                collided, collisionInfo = collisions.GJK(item, elem)
            else:
                collided, collisionInfo = False, None

            if collided:
                #print 'Item collided with scene'
                collision_response(item, elem, collisionInfo)

    for item in sceneList:
        #print 'Checking collision with scene:', item
        check_collision = broadphase.shape_surface(player, item)
        if check_collision:
            #collided, collisionInfo = collisions.GJK(player, item)
            collided, collisionInfo = narrowphase.sphere_surface(player, item)
        else:
            collided, collisionInfo = False, None

        if collided:
            #print 'Player collided with scene'
            collision_response(player, item, collisionInfo)
    
    # TODO: switch to semi-implicit Euler integration
    
    player.add_velocity(GRAVITY*dt)
    player.add_pos(player.get_velocity())
    
    angVel = player.get_angular_velocity()
    angle = angVel.norm()
    axis = angVel.normalize()
    if axis == None:
        axis = vectors.Vector([1.0, 0.0, 0.0])  #Dummy variable
    rotQuat = quaternions.axis_angle_to_quat(axis, angle)
    player.add_orientation(rotQuat)

    for item in objectList:
        item.add_velocity(GRAVITY*dt)
        item.add_pos(item.get_velocity())
        
        angVel = item.get_angular_velocity()
        angle = angVel.norm()
        axis = angVel.normalize()
        if axis == None:
            axis = vectors.Vector([1.0, 0.0, 0.0])  #Dummy variable
        rotQuat = quaternions.axis_angle_to_quat(axis, angle)
        item.add_orientation(rotQuat)
    #print ''
