import shapes

def shape_surface(shape, surface):
    '''
    A broadphase collision detection algorithm for collisions between
    shapes and surfaces. Uses the shapes' bounding spheres and checks
    whether this sphere is close to the infinite plane coinciding with
    the surface.

    Input: A shape object and a surface object
    Output: A boolean; True if they are so close that the pair should
            move on to narrowphase, False otherwise.
    '''
    
    # NOTE: Surfaces are currently not accepted input as the shape
    # since they do not have a bounding_radius() function, but this
    # shouldn't be a problem since we don't check for collisions between
    # surfaces anyway.

    # NOTE: The bounding_radius() function returns a radius that is
    # slightly bigger than the actual bounding radius of the shape,
    # this is in order to make sure that all pairs that are supposed
    # to go to narrowphase are sent there: it is better to send to
    # many than to few.
    
    assert isinstance(shape, shapes.Shape), 'Input must be a shape object'
    assert not isinstance(shape, shapes.Surface), \
           'Input must not be a surface object'
    assert isinstance(surface, shapes.Surface), 'Input must be a surface object'

    distance = (shape.get_pos() - surface.get_pos()).dot(surface.get_normal())
    if abs(distance) < shape.get_bounding_radius():
        # The sphere is close to the surface, send to narrowphase
        return True
    else:
        # The sphere can't possibly touch the plane, don't send to narrowphase
        return False

def shape_shape(shape1, shape2):
    '''
    A broadphase collision detection algorithm for collisions between
    two shapes. Checks whether the two shapes' bounding spheres intersect.
    
    Input: Two shape objects (not surfaces)
    Output: A boolean; True if they are so close that the pair should
            move on to narrowphase, False otherwise.  
    '''
    # NOTE: Surfaces are not accepted as input, partly because thay have no
    # bounding_radius() function, but mainly because this is quite inefficient
    # for surfaces; they are much bigger in two directions than in the third,
    # and therefore the bounding sphere is almost completely empty.

    assert isinstance(shape1, shapes.Shape), 'Input must be a shape object'
    assert isinstance(shape2, shapes.Shape), 'Input must be a shape object'
    assert not isinstance(shape1, shapes.Surface), \
           'Input must not be a surface object'
    assert not isinstance(shape2, shapes.Surface), \
           'Input must not be a surface object'

    distance = shape.get_pos() - plane.get_pos()
    boundingDistance = shape1.get_bounding_radius() +\
                       shape2.get_bounding_radius()
    if distance.norm() < boundingDistance:
        # The shapes' bounding spheres intersect, send to narrowphase
        return True
    else:
        # The shapes' bounding spheres don't intersect, don't send to narrowphase
        return False
