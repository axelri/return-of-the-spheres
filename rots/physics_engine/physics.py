import numbers
#import time

import broadphase
import narrowphase
import collisions
import shapes
import games
import players
from math_classes import vectors, quaternions, matrices


GRAVITY = vectors.Vector([0.0, -10.0, 0.0])
#dt = 0.005

def collision_response(shape1, shape2, collisionInfo):
    '''
    Takes two Shape objects that have collided, calculates
    the impulse that should be applied to them and applies it,
    both to the linear and the angular velocity.

    Input:
        * shape1 and shape2 are Shape objects
        
        * collisionInfo is a tuple containing collision information:
        The point of collision, the contact normal and the
        penetration depth

        * collisionPoint is a vector describing the point of collision

        * normal is a vector describing the contact normal

        * depth is a number describing the penetration depth
    '''
    
    #print 'Entered collision response'
    assert isinstance(shape1, shapes.Shape), \
           'Input must be a Shape object'
    assert isinstance(shape2, shapes.Shape), \
           'Input must be a Shape object'
    assert isinstance(collisionInfo, tuple), \
           'Input must be a tuple'
    assert len(collisionInfo) == 3, \
           'CollisionInfo must be of length 3'

    collisionPoint, normal, depth = collisionInfo

    assert isinstance(collisionPoint, vectors.Vector), \
           'Input must be a vector'
    assert isinstance(normal, vectors.Vector), \
           'Input must be a vector'
    assert isinstance(depth, numbers.Number), \
           'Input must be a number'

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
    relMov = - relVel.dot(normal)

    if relMov < -0.01:
        return

    # NORMAL Impulse

    e = 0.5 # Coefficient of restitution

    normalInert1 = r1.triple_product_2(normal, r1).left_matrix_mult(invInertia1)
    normalInert2 = r2.triple_product_2(normal, r2).left_matrix_mult(invInertia2)

    normalImpulse = -(1+e)*relVel.dot(normal)/ \
              (invMass1 + invMass2 + (normalInert1 + normalInert2).dot(normal))
    

    # Hack fix to stop sinking
    normalImpulse += depth*1.0

    shape1.add_velocity(normal * normalImpulse * invMass1)
    shape2.add_velocity(normal * normalImpulse * invMass2 * -1.0)


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



def update_physics(game, dt):
    ''' Updates all physics in the game; takes all the objects in
    the game, calculates collisions etc and moves them to their
    new locations.'''

    # TODO: Needs A LOT of cleaning, this code is a mess...
    
    assert isinstance(game, games.Game), 'Input must be a game object'
    
    # TODO: Add broadphase collision detection, for example
    # check_collision = collisions.broadphase(shape1, shape2)
    # if check_collision:
    #     collided, collisionInfo = collisions.GJK(shape1, shape2)
    # broadphase should return a boolean; True if the shapes should be
    # passed on to narrowphase, False otherwise.
    # NOTE: Some broadphase added
    # TODO: Add octrees/something like that? This broadphase algorithm
    # works, but I think we can enhance it.
    
    #print 'Entered loop at', time.clock()
    player, objectList, sceneList, lightList, textList, camera = game.get_objects()

    player.collided = False
    
    for item in objectList:
        #print 'Checking collision with item:', item

        check_collision = broadphase.shape_shape(player.get_shape(), item)
        if check_collision:
            # NOTE: Only works with Cubes
            # TODO: Add this?
            # if item.__class__.__name__ == 'Cube':
            #     do sphere_cube-algorithm
            # elif item.__class__.__name__ == 'blah blah':
            #     do other algorithms
            collided, collisionInfo = narrowphase.sphere_cube(player.get_shape(), item)
            #collided, collisionInfo = collisions.GJK(player.get_shape(), item)
        else:
            collided, collisionInfo = False, None

        if collided:
            #print 'Player collided with item'
            collision_response(player.get_shape(), item, collisionInfo)
            player.colliding = True
            # Resets player.jumping to False so it can jump again
            if collisionInfo[1].dot(vectors.Vector([0.0, 1.0, 0.0])) < 0.0:
                player.reset_jump()

        for elem in sceneList:
            check_collision = broadphase.shape_surface(item, elem)
            if check_collision:
                # NOTE: Only works with cubes, see the proposed solutions above
                collided, collisionInfo = narrowphase.cube_surface(item, elem)
                #collided, collisionInfo = collisions.GJK(item, elem)
            else:
                collided, collisionInfo = False, None

            if collided:
                #print 'Item collided with scene'
                collision_response(item, elem, collisionInfo)

    for item in sceneList:
        #print 'Checking collision with scene:', item
        check_collision = broadphase.shape_surface(player.get_shape(), item)
        if check_collision:
            #collided, collisionInfo = collisions.GJK(player, item)
            if player.get_shape().__class__.__name__ == 'Sphere':
                collided, collisionInfo = narrowphase.\
                                          sphere_surface(player.get_shape(), item)
            elif player.get_shape().__class__.__name__ == 'Cube':
                collided, collisionInfo = narrowphase.\
                                          cube_surface(player.get_shape(), item)
        else:
            collided, collisionInfo = False, None

        if collided:
            #print 'Player collided with scene'
            collision_response(player.get_shape(), item, collisionInfo)
            #print 'Collided before:', player.collided
            player.colliding = True
            #print 'Collided after:', player.collided
            # Resets player.jumping to False so it can jump again
            if collisionInfo[1].dot(vectors.Vector([0.0, 1.0, 0.0])) > 0.0:
                #print 'Normal correct; jumping:', player.jumping
                player.reset_jump()
                #print 'Jumping after:', player.jumping
    
    # TODO: switch to semi-implicit Euler integration

    # Friction
    if player.colliding:
        player.get_shape().add_velocity(player.get_shape()\
                                        .get_velocity()*-0.05)
        if player.get_shape().get_velocity().norm() < 0.001:
            player.get_shape().set_velocity(vectors.Vector())
        player.get_shape().add_angular_velocity(player.get_shape()\
                                        .get_angular_velocity()*-0.05)
        if player.get_shape().get_angular_velocity().norm() < 0.001:
            player.get_shape().set_angular_velocity(vectors.Vector())

    #print 'Velocity before gravity:', player.get_shape().get_velocity()        
    player.get_shape().add_velocity(GRAVITY*dt)
    #print 'Velocity after gravity:', player.get_shape().get_velocity()
    #print ''
    player.get_shape().add_pos(player.get_shape().get_velocity())
    
    angVel = player.get_shape().get_angular_velocity()
    angle = angVel.norm()
    axis = angVel.normalize()
    #print 'Angle: {angle}, Axis: {axis}'.format(angle = angle, axis = axis)
    if axis == None:
        axis = vectors.Vector([1.0, 0.0, 0.0])  #Dummy variable
    #rotQuat = quaternions.axis_angle_to_quat(axis, angle)
    rotQuat = matrices.generate_rotation_matrix(axis, angle)
    player.get_shape().add_orientation(rotQuat)
    #print 'rotQuat: {rotQuat}, Orientation: {orientation}'\
    #      .format(rotQuat = rotQuat, orientation = player.get_orientation())
    #print ''

    for item in objectList:
        # Friction
        item.add_velocity(item.get_velocity() *-0.05)
        if item.get_velocity().norm() < 0.001:
            item.set_velocity(vectors.Vector())
        item.add_angular_velocity(item.get_angular_velocity() *-0.05)
        if item.get_angular_velocity().norm() < 0.001:
            item.set_angular_velocity(vectors.Vector())

        item.add_velocity(GRAVITY*dt)
        item.add_pos(item.get_velocity())
        
        angVel = item.get_angular_velocity()
        angle = angVel.norm()
        axis = angVel.normalize()
        if axis == None:
            axis = vectors.Vector([1.0, 0.0, 0.0])  #Dummy variable
        #rotQuat = quaternions.axis_angle_to_quat(axis, angle)
        rotQuat = matrices.generate_rotation_matrix(axis, angle)
        item.add_orientation(rotQuat)
    #print ''
