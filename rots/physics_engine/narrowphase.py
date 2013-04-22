# Narrowphase collision detection algoritmhs

import shapes
from math_classes import vectors
import numbers

def sphere_surface(sphere, surface):
    '''
    A narrowphase collision detection algorithm for collisions between
    spheres and surfaces.

    Input: A Sphere object and a Surface object.
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

    # Check for collision with the face

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
        # Check for collisions with edges and corners

        # Check for collisions with edges
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
        # Check for collisions with corners
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
            # Collision with corner index
            collided = True
            normal = distCorn.normalize()
            if normal == None:
                # The center of the sphere hit the corner, pick a normal
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

def sphere_cube(sphere, cube):
    '''
    A narrowphase collision detection algorithm for collisions between
    spheres and axis-aligned cubes.

    Input: A Sphere object and a Cube object.
    Output:
            collided: A boolean, True if there is a collision, False otherwise
            point:  A vector describing the best collision point
                    if there is a collision, None otherwise.
            normal: A vector describing the collision normal if there
                    is a collision, None otherwise.
            depth:  A float describing the penetration depth if there is a
                    collision, None otherwise.
    '''
    distance = sphere.get_pos() - cube.get_pos()

    normals = [vectors.Vector([1.0, 0.0, 0.0]),
               vectors.Vector([-1.0, 0.0, 0.0]),
               vectors.Vector([0.0, 1.0, 0.0]),
               vectors.Vector([0.0, -1.0, 0.0]),
               vectors.Vector([0.0, 0.0, 1.0]),
               vectors.Vector([0.0, 0.0, -1.0])]
               
    side = cube.get_side()

    # Check collision with faces
    for i in range(3):
        if abs(distance.dot(normals[2*i])) <= side * 0.5 \
           and abs(distance.dot(normals[2*(i+1)%len(normals)])) <= side * 0.5 \
           and abs(distance.dot(normals[2*(i+2)%len(normals)])) \
           <= side * 0.5 + sphere._radius:
            # Collision with face 2*(i+2)%len(normals) or (2*(i+2)+1)%len(normals)
            if distance.dot(normals[2*(i+2)%len(normals)]) < 0:
                # Collision with face 2*(i+2)%len(normals)
                normal = normals[2*(i+2)%len(normals)]
            else:
                # Collision with face (2*(i+2)+1)%len(normals)
                normal = normals[(2*(i+2)+1)%len(normals)]
                
            collided = True
            # The midpoint of the face
            faceMidpoint = cube.get_pos() + normal * side * 0.5
            # The distance from the sphere to the midpoint
            dist = sphere.get_pos() - faceMidpoint
            # That distance projected on the face
            projDist = dist.projected(normals[2*i], normals[2*(i+1)%len(normals)])
            point = projDist + cube.get_pos()
            depth = sphere.get_radius() + side * 0.5 - abs(distance.dot(normal))

##            print 'Collided; collisioninfo:'
##            print '\tNormal:', normal
##            print '\tPoint:', point
##            print '\tDepth:', depth
##            print '\tCubePos:', cube.get_pos()
##            print '\tSpherePos:', sphere.get_pos()
##            print ''

            assert isinstance(collided, bool), 'Collided must be a boolean'
            assert isinstance(point, vectors.Vector), 'Point must be a vector'
            assert isinstance(normal, vectors.Vector), 'Normal must be a vector'
            assert isinstance(depth, numbers.Number), 'Depth must be a number'
            assert depth >= 0.0, 'Depth must be positive'

            return collided, (point, normal, depth)

    # Check collisions with edges

    # Check collisions with corners


    # No collision
    collided = False
    normal = None
    point = None
    depth = None
    
    return collided, (point, normal, depth)


def cube_surface(cube, surface):
    '''
    A narrowphase collision detection algorithm for collisions between
    axis-aligned cubes and axis-aligned surfaces.

    Input: A Cube object and a Surface object.
    Output:
            collided: A boolean, True if there is a collision, False otherwise
            point:  A vector describing the best collision point
                    if there is a collision, None otherwise.
            normal: A vector describing the collision normal if there
                    is a collision, None otherwise.
            depth:  A float describing the penetration depth if there is a
                    collision, None otherwise.
    '''

    assert isinstance(cube, shapes.Cube), 'Input must be a Cube object'
    assert isinstance(surface, shapes.Surface), 'Input must be a Surface object'

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

    distVec = cube.get_pos() - surface.get_pos()

    projDist = distVec.projected(normVec1, normVec2)
    distance = distVec.dot(normal)
    
    if abs(projDist.dot(normVec1)) < surfVec1.norm()*0.5 and\
       abs(projDist.dot(normVec2)) < surfVec2.norm()*0.5:
        # The cube is directly above/below the face of the surface
        if abs(distance) <= cube.get_side()*0.5:
            # Collision with face
            collided = True

            if distance < 0:
                normal *= -1.0

            point = projDist + surface.get_pos()
            depth = cube.get_side()*0.5 - abs(distance)

            print 'Depth:', depth
            
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

    # Check for collision with edges
    for i in range(len(normVecs)):
        if abs(projDist.dot(normVecs[i])) < (surfVecs[i].norm() + cube.get_side())*0.5 \
           and abs(projDist.dot(normVecs[(i+1)%2])) < surfVecs[(i+1)%2].norm()*0.5:

            if abs(distance) <= cube.get_side()*0.5:
                # Collision with face
                collided = True

                if distance < 0:
                    normal *= -1.0

                point = surface.get_pos() + projDist.projected(normVecs[(i+1)%2]) + \
                        (surfVecs[i]*0.5 + projDist.projected(normVecs[i]) \
                         - normVecs[i]*cube.get_side()*0.5)*0.5
                depth = cube.get_side()*0.5 - abs(distance)
                
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

    # Check for collisions with corners
    
    # TODO: There is a bug when colliding with corners that causes a crash:
    
    # Traceback (most recent call last):
    # File "C:\Documents and Settings\Martin2\Mina dokument\GitHub\return-of-the-sph
    # eres\rots\testPhysics.py", line 108, in <module>
    # main()
    # File "C:\Documents and Settings\Martin2\Mina dokument\GitHub\return-of-the-sph
    # eres\rots\testPhysics.py", line 102, in main
    #   physics.update_physics(game)
    # File "C:\Documents and Settings\Martin2\Mina dokument\GitHub\return-of-the-sph
    # eres\rots\physics_engine\physics.py", line 236, in update_physics
    #   cube_surface(player.get_shape(), item)
    # TypeError: 'NoneType' object is not iterable

    # What is wrong and how do we fix it?
    
    if abs(projDist.dot(normVec1)) < (surfVec1.norm() + cube.get_side())*0.5 \
           and abs(projDist.dot(normVec2)) < (surfVec2.norm()*0.5 + cube.get_side())*0.5:

        if abs(distance) <= cube.get_side()*0.5:
            # Collision with a corner
            collided = True

            if distance < 0:
                normal *= -1.0

            point = surface.get_pos() + \
                    (surfVec1*0.5 + projDist.projected(normVec1) - \
                     normVec1*cube.get_side()*0.5)*0.5 + \
                    (surfVec2*0.5 + projDist.projected(normVec2) - \
                     normVec2*cube.get_side()*0.5)*0.5

            depth = cube.get_side()*0.5 - abs(distance)
                
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
