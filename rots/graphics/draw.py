# Drawing routines for the objects

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numbers

import shapes

CUBE_QUAD_VERTS = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
                   (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

CUBE_EDGES = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
              (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))

CUBE_NORMALS = ([0.0, 0.0, -1.0], [-1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0], [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0], [0.0, -1.0, 0.0])

def cube_points(size):
    ''' Calculates the vertices of a cube of size size.

    Input:  size: The length of the side of the cube,
                must be a positive number.

    Output: A list containing the vertices of the cube,
            represented as lists. '''
    
    assert isinstance(size, numbers.Number), 'Input must be a number'
    assert size > 0, 'Input must be a positive number'
    
    h = size/2.0
    return [[h, -h, -h],  [h, h, -h],
            [-h, h, -h],  [-h, -h, -h],
            [h, -h, h],   [h, h, h],
            [-h, -h, h],  [-h, h, h]]


def cube(cube):
    ''' The drawing routine for a Cube object.

    Input:  cube: A Cube object

    Calls OpenGL to draw the cube. '''
    
    assert isinstance(cube, shapes.Cube), \
           'Input must be a Cube object'

    points = cube_points(cube.get_side())

    ambient, diffuse, specular, shininess, emissive = cube.get_material_properties()

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, emissive)
    #glColor3fv(cube.get_color())
    glBegin(GL_QUADS)
    for face in CUBE_QUAD_VERTS:
        glNormal3fv(CUBE_NORMALS[CUBE_QUAD_VERTS.index(face)])
        for vert in face:     
            glVertex3fv(points[vert])
    glEnd()

    # TODO: Use something like "cube.get_line_color()" instead?
    glColor3f(0.0, 0.0, 0.0)    
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            glVertex3fv(points[vert])
    glEnd()

def surface(surface):
    ''' The drawing routine for a Surface object.

    Input:  surface: A Surface object

    Calls OpenGL to draw the surface. '''

    # TODO: Tesselate the surface for better lighting effects

    ambient, diffuse, specular, \
             shininess , emissive = surface.get_material_properties()

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, emissive)

    #points = surface.get_points()
    #glColor3fv(surface.get_color())

    if surface._texture:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, surface._texture)

    # The dimensions of the surface
    length = surface._length
    width = surface._width
    half_length = length / 2.0
    half_width = width / 2.0
    
    # The wanted subdivision size
    goal_sub_size = surface._subdivision_size

    # Number of subdivisions
    length_subs = int(surface._length // goal_sub_size)
    width_subs = int(surface._width // goal_sub_size)

    # Actual size of the subdivisions
    length_sub_size = surface._length / float(length_subs)
    width_sub_size = surface._width / float(width_subs)

    # Size as fractions of the whole surface
    length_sub_frac = 1.0 / length_subs
    width_sub_frac = 1.0 / width_subs
    
    glBegin(GL_QUADS)
    

    for l in range(length_subs):
        for w in range(width_subs):
            glNormal3fv(surface.get_normal().value)
            glTexCoord2f(w * width_sub_frac, 1 - l * length_sub_frac)
            glVertex3f(-half_width + w * width_sub_size, 
                        0.0,
                        -half_length + l * length_sub_size)
            glTexCoord2f(w * width_sub_frac, 1 - (l + 1) *length_sub_frac)
            glVertex3f(-half_width + w * width_sub_size, 
                        0.0,
                        -half_length + (l + 1) * length_sub_size)
            glTexCoord2f((w + 1) * width_sub_frac, 1 - (l + 1) * length_sub_frac)
            glVertex3f(-half_width + (w + 1) * width_sub_size, 
                        0.0,
                        -half_length + (l + 1) * length_sub_size)
            glTexCoord2f((w + 1) * width_sub_frac, 1 - l * length_sub_frac)
            glVertex3f(-half_width + (w + 1) * width_sub_size, 
                        0.0,
                        -half_length + l * length_sub_size)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def sphere(sphere):
    ''' The drawing routine for a Sphere object.

    Input:  surface: A Sphere object

    Calls OpenGL to draw the sphere. '''
    
    assert isinstance(sphere, shapes.Sphere), \
           'Input must be a Sphere object'
    
    ambient, diffuse, specular, \
             shininess, emissive = sphere.get_material_properties()

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, emissive)

    if sphere._texture:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, sphere._texture)

    #glColor3fv(sphere.get_color())
    #glutSolidSphere(sphere.get_radius(), 10, 10)
    #glutSolidSphere(sphere.get_radius(), 40, 40)
    #glutSolidTeapot(sphere.get_radius())

    #gluQuadricDrawStyle(sphere._quadric, GLU_FILL)
    if sphere._texture:
        gluQuadricTexture(sphere._quadric, True)
    #gluQuadricNormals(sphere._quadric, GLU_SMOOTH)
    gluSphere(sphere._quadric,sphere.get_radius(), 60, 60)

    glDisable(GL_TEXTURE_2D)
