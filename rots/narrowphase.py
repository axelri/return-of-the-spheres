import shapes

# TODO: More functions: cube-plane, sphere-cube

def sphere_surface(sphere, surface):
    '''
    A narrowphase collision detection algorithm for collisions between
    spheres and surfaces.

    Input: A sphere object and a surface object.
    Output:
            collided: A boolean, True if there is a collision, False otherwise
            point:  A vector describing the best collision point
                    if there is a collision, None otherwise.
            normal: A vector describing the collision normal if there
                    is a collision, None otherwise.
            depth:  A float describing the penetration depth if there is a
                    collision, None otherwise.
    '''

    assert isinstance(sphere, shapes.Sphere), 'Input must be a sphere object'
    assert isinstance(surface, shapes.Surface), 'Input must be a surface object'

    points = surface.get_points()
    normal = surface.get_normal()
    surfVec1 = points[1] - points[0]
    surfVec2 = points[3] - points[0]
    normVec1 = surfVec1.normalize()
    normVec2 = surfVec2.normalize()
    if normVec1 == None or normVec2 == None:
        raise Exception('The plane has width or height 0')

    distVec = sphere.get_pos() - surface.get_pos()

    projDist = distVec.projected(normVec1, normVec2)

    if abs(projDist.dot(normVec1)) < surfVec1.norm()*0.5 and\
       abs(projDist.dot(normVec2)) < surfVec2.norm()*0.5:
        # The sphere is directly above/below the face of the surface
        distance = distVec.dot(normal)
        if abs(distance) <= sphere.get_radius():
            # Collision
            collided = True

            if distance < 0:
                normal *= -1.0

            point = projDist + surface.get_pos()

            depth = sphere.get_radius() - abs(distance)
        else:
            # No collision
            collided = False
            normal = None
            point = None
            depth = None
    else:
        # Might have hit an edge
        # TODO: Handle this
        print 'Might have hit and edge, to be completed'
        collided = False
        normal = None
        point = None
        depth = None

    return collided, (point, normal, depth)

