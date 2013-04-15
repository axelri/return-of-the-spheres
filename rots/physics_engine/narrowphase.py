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
##            print 'Collision with face'
            collided = True

            if distance < 0:
                normal *= -1.0

            point = projDist + surface.get_pos()
            depth = sphere.get_radius() - abs(distance)
##            print 'Point:', point
##            print 'Pos:', sphere.get_pos()
            assert isinstance(collided, bool), 'Collided must be a boolean'
            assert isinstance(point, vectors.Vector), 'Point must be a vector'
            assert isinstance(normal, vectors.Vector), 'Normal must be a vector'
            assert isinstance(depth, numbers.Number), 'Depth must be a number'
            assert depth >= 0.0, 'Depth must be positive'
    
            return collided, (point, normal, depth)
        else:
            # No collision
##            print 'No collision'
            collided = False
            normal = None
            point = None
            depth = None
    
            return collided, (point, normal, depth)
    else:
##        print 'Might have hit an edge or corner'
        # Might have hit an edge or corner
        # TODO: A lot of redundance, handle this?
        if abs(projDist.dot(normVec1)) < surfVec1.norm()*0.5:
            # Might have hit an edge parallel to surfVec1
            if distVec.dot(normVec2) < 0:
                # Might have hit edge 1
                dist = sphere.get_pos() - points[0]
                # The vector from edge 1 to the sphere, othogonal to edge 1
                distEdge = dist - dist.projected(normVec1)
                if distEdge.norm() < sphere.get_radius():
                    # Collision with edge 1
##                    print 'Hit edge 1'
                    collided = True
                    normal = distEdge.normalize()
                    if normal == None:
                        # The center of the sphere hit the edge, pick a normal
                        normal = surface.get_normal()

                    point = dist.projected(normVec1) + surface.get_pos() + points[0]
                    depth = sphere.get_radius() - distEdge.norm()

##                    print 'Collision info:'
##                    print '\tCollided:', collided
##                    print '\tPoint:', point
##                    print '\tPos:', sphere.get_pos()
##                    print '\tNormal:', normal
##                    print '\tDepth:', depth
##                    print ''

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
##                    print 'No collision'
                    collided = False
                    normal = None
                    point = None
                    depth = None
    
                    return collided, (point, normal, depth)
            else:
                # Might have hit edge 3
                dist = sphere.get_pos() - points[3]
                # The vector from edge 3 to the sphere, othogonal to edge 3
                distEdge = dist - dist.projected(normVec1)
                if distEdge.norm() < sphere.get_radius():
                    # Collision with edge 3
##                    print 'Hit edge 3'
                    collided = True
                    normal = distEdge.normalize()
                    if normal == None:
                        # The center of the sphere hit the edge, pick a normal
                        normal = surface.get_normal()

                    point = dist.projected(normVec1) + surface.get_pos() + points[3]
                    depth = sphere.get_radius() - distEdge.norm()
##                    print 'Collision info:'
##                    print '\tCollided:', collided
##                    print '\tPoint:', point
##                    print '\tPos:', sphere.get_pos()
##                    print '\tNormal:', normal
##                    print '\tDepth:', depth
##                    print ''

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
##                    print 'No collision'
                    collided = False
                    normal = None
                    point = None
                    depth = None
    
                    return collided, (point, normal, depth)
                
        elif abs(projDist.dot(normVec2)) < surfVec2.norm()*0.5:
            # Might have hit an edge parallel to surfVec2
            if distVec.dot(normVec1) < 0:
                # Might have hit edge 4
                dist = sphere.get_pos() - points[0]
                # The vector from edge 4 to the sphere, othogonal to edge 4
                distEdge = dist - dist.projected(normVec2)
                if distEdge.norm() < sphere.get_radius():
                    # Collision with edge 4
##                    print 'Hit edge 4'
                    collided = True
                    normal = distEdge.normalize()
                    if normal == None:
                        # The center of the sphere hit the edge, pick a normal
                        normal = surface.get_normal()

                    point = dist.projected(normVec2) + surface.get_pos() + points[0]
                    depth = sphere.get_radius() - distEdge.norm()
##                    print 'Collision info:'
##                    print '\tCollided:', collided
##                    print '\tPoint:', point
##                    print '\tPos:', sphere.get_pos()
##                    print '\tNormal:', normal
##                    print '\tDepth:', depth
##                    print ''

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
##                    print 'No collision'
                    collided = False
                    normal = None
                    point = None
                    depth = None
    
                    return collided, (point, normal, depth)
                    
            else:
                # Might have hit edge 2
                dist = sphere.get_pos() - points[1]
                # The vector from edge 2 to the sphere, othogonal to edge 2
                distEdge = dist - dist.projected(normVec2)
                if distEdge.norm() < sphere.get_radius():
                    # Collision with edge 2
##                    print 'Hit edge 2'
                    collided = True
                    normal = distEdge.normalize()
                    if normal == None:
                        # The center of the sphere hit the edge, pick a normal
                        normal = surface.get_normal()

                    point = dist.projected(normVec2) + surface.get_pos() + points[1]
                    depth = sphere.get_radius() - distEdge.norm()
##                    print 'Collision info:'
##                    print '\tCollided:', collided
##                    print '\tPoint:', point
##                    print '\tPos:', sphere.get_pos()
##                    print '\tNormal:', normal
##                    print '\tDepth:', depth
##                    print ''

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
##                    print 'No collision'
                    collided = False
                    normal = None
                    point = None
                    depth = None
    
                    return collided, (point, normal, depth)
                
        else:
            # Might have hit a corner
            if distVec.dot(normVec1) < 0:
                # Might have hit corner 0 or 3
                if distVec.dot(normVec2) < 0:
                    # Might have hit corner 0
                    distCorn = sphere.get_pos() - points[0]
                    if distCorn.norm() < sphere.get_radius():
                        # Collision with corner 0
##                        print 'Hit corner 0'
                        collision = True
                        normal = distCorn.normalize()
                        if normal == None:
                            # The center of the sphere hit the edge, pick a normal
                            normal = surface.get_normal()
                        point = points[0] + surface.get_pos()
                        depth = sphere.get_radius() - distCorn.norm()
##                        print 'Collision info:'
##                        print '\tCollided:', collided
##                        print '\tPoint:', point
##                        print '\tPos:', sphere.get_pos()
##                        print '\tNormal:', normal
##                        print '\tDepth:', depth
##                        print ''

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
##                        print 'No collision'
                        collided = False
                        normal = None
                        point = None
                        depth = None
    
                        return collided, (point, normal, depth)
                    
                else:
                    # Might have hit corner 3
                    distCorn = sphere.get_pos() - points[3]
                    if distCorn.norm() < sphere.get_radius():
                        # Collision with corner 3
##                        print 'Hit corner 3'
                        collision = True
                        normal = distCorn.normalize()
                        if normal == None:
                            # The center of the sphere hit the edge, pick a normal
                            normal = surface.get_normal()
                        point = points[3] + surface.get_pos()
                        depth = sphere.get_radius() - distCorn.norm()
##                        print 'Collision info:'
##                        print '\tCollided:', collided
##                        print '\tPoint:', point
##                        print '\tPos:', sphere.get_pos()
##                        print '\tNormal:', normal
##                        print '\tDepth:', depth
##                        print ''

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
##                        print 'No collision'
                        collided = False
                        normal = None
                        point = None
                        depth = None
    
                        return collided, (point, normal, depth)
                        
            else:
                # Might have hit corner 1 or 2
                if distVec.dot(normVec2) < 0:
                    # Might have hit corner 1
                    distCorn = sphere.get_pos() - points[1]
                    if distCorn.norm() < sphere.get_radius():
                        # Collision with corner 1
##                        print 'Hit corner 1'
                        collision = True
                        normal = distCorn.normalize()
                        if normal == None:
                            # The center of the sphere hit the edge, pick a normal
                            normal = surface.get_normal()
                        point = points[1] + surface.get_pos()
                        depth = sphere.get_radius() - distCorn.norm()
##                        print 'Collision info:'
##                        print '\tCollided:', collided
##                        print '\tPoint:', point
##                        print '\tPos:', sphere.get_pos()
##                        print '\tNormal:', normal
##                        print '\tDepth:', depth
##                        print ''

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
##                        print 'No collision'
                        collided = False
                        normal = None
                        point = None
                        depth = None
    
                        return collided, (point, normal, depth)
                    
                else:
                    # Might have hit corner 2
                    distCorn = sphere.get_pos() - points[2]
                    if distCorn.norm() < sphere.get_radius():
                        # Collision with corner 2
##                        print 'Hit corner 2'
                        collision = True
                        normal = distCorn.normalize()
                        if normal == None:
                            # The center of the sphere hit the edge, pick a normal
                            normal = surface.get_normal()
                        point = points[2] + surface.get_pos()
                        depth = sphere.get_radius() - distCorn.norm()
##                        print 'Collision info:'
##                        print '\tCollided:', collided
##                        print '\tPoint:', point
##                        print '\tPos:', sphere.get_pos()
##                        print '\tNormal:', normal
##                        print '\tDepth:', depth
##                        print ''

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
##                        print 'No collision'
                        collided = False
                        normal = None
                        point = None
                        depth = None
    
                        return collided, (point, normal, depth)
