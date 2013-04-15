import shapes
from math_classes import vectors
import numbers

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
    surfVecs = [surfVec1, surfVec2]
    normVecs =[normVec1, normVec2]
    if normVec1 == None or normVec2 == None:
        raise Exception('The plane has width or height 0')

    distVec = sphere.get_pos() - surface.get_pos()

    projDist = distVec.projected(normVec1, normVec2)

    if abs(projDist.dot(normVec1)) < surfVec1.norm()*0.5 and\
       abs(projDist.dot(normVec2)) < surfVec2.norm()*0.5:
        # The sphere is directly above/below the face of the surface
        distance = distVec.dot(normal)
        if abs(distance) <= sphere.get_radius():
            # Collision with face
            collided = True

            if distance < 0:
                normal *= -1.0

            point = projDist + surface.get_pos()
            depth = sphere.get_radius() - abs(distance)
            assert isinstance(collided, bool), 'Collided must be a boolean'
            assert isinstance(point, vectors.Vector), 'Point must be a vector'
            assert isinstance(normal, vectors.Vector), 'Normal must be a vector'
            assert isinstance(depth, numbers.Number), 'Depth must be a number'
            assert depth >= 0.0, 'Depth must be positive'
    
            return collided, (point, normal, depth)
        else:
            # No collision
            collided = False
            normal = None
            point = None
            depth = None
    
            return collided, (point, normal, depth)
    else:
        # Might have hit an edge or corner

        for i in range(len(surfVecs)):
            if abs(projDist.dot(normVecs[i])) < surfVecs[i].norm()*0.5:
                # Might have hit an edge parallel to surfVecs[i]
                # A little ugly, but it was the best solution I found to remove redundancy
                if distVec.dot(normVecs[(i+1)%len(normVecs)]) < 0:
                    index = 0
                else:
                    index = 3 - 2*i
                    
                dist = sphere.get_pos() - points[index]
                # The vector from the edge to the sphere,
                # othogonal to the edge
                distEdge = dist - dist.projected(normVecs[i])
                if distEdge.norm() < sphere.get_radius():
                    # Collision with the edge
                    collided = True
                    normal = distEdge.normalize()
                    if normal == None:
                        # The center of the sphere hit the edge, pick a normal
                        normal = surface.get_normal()
                    point = dist.projected(normVecs[i]) + \
                            surface.get_pos() + points[index]
                    depth = sphere.get_radius() - distEdge.norm()

                    assert isinstance(collided, bool), \
                       'Collided must be a boolean'
                    assert isinstance(point, vectors.Vector), \
                           'Point must be a vector'
                    assert isinstance(normal, vectors.Vector), \
                           'Normal must be a vector'
                    assert isinstance(depth, numbers.Number), \
                           'Depth must be a number'
                    assert depth >= 0.0, \
                           'Depth must be positive'
    
                    return collided, (point, normal, depth)

                else:
                    # No collision
                    collided = False
                    normal = None
                    point = None
                    depth = None
    
                    return collided, (point, normal, depth)

        # A little ugly, but it was the best solution I found to remove redundancy
        # Might have hit a corner
        if distVec.dot(normVec1) <0:
            # Might have hit corner 0 or 3
            if distVec.dot(normVec2) < 0:
                # Might have hit corner 0
                index = 0
            else:
                # Might have hit corner 3
                index = 3
        else:
            # Might have hit corner 1 or 2
            if distVec.dot(normVec2) < 0:
                # Might have hit corner 1
                index = 1
            else:
                # Might have hit corner 2
                index = 2

        distCorn = sphere.get_pos() - points[index]
        if distCorn.norm() < sphere.get_radius():
            # Collision with corner 0
            collided = True
            normal = distCorn.normalize()
            if normal == None:
                # The center of the sphere hit the edge, pick a normal
                normal = surface.get_normal()
            point = points[index] + surface.get_pos()
            depth = sphere.get_radius() - distCorn.norm()

            assert isinstance(collided, bool), \
               'Collided must be a boolean'
            assert isinstance(point, vectors.Vector), \
                   'Point must be a vector'
            assert isinstance(normal, vectors.Vector), \
                   'Normal must be a vector'
            assert isinstance(depth, numbers.Number), \
                   'Depth must be a number'
            assert depth >= 0.0, \
                   'Depth must be positive'

            return collided, (point, normal, depth)
    
        else:
            # No collision
            collided = False
            normal = None
            point = None
            depth = None

            return collided, (point, normal, depth)
