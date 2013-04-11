from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numbers

import shapes
from tensors import vectors

CUBE_QUAD_VERTS = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
                   (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

CUBE_EDGES = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
              (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))

CUBE_NORMALS = ([0.0, 0.0, -1.0], [-1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0], [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0], [0.0, -1.0, 0.0])

def cube_points(size):
    assert isinstance(size, numbers.Number), 'Input must be a number'
    assert size > 0, 'Input must be a positive number'
    h = size/2.0
    return [[h, -h, -h],  [h, h, -h],
            [-h, h, -h],  [-h, -h, -h],
            [h, -h, h],   [h, h, h],
            [-h, -h, h],  [-h, h, h]]


def cube(cube):
    assert isinstance(cube, shapes.Cube), 'Input must be a cube object'
    points = cube_points(cube.get_side())


    glColor3fv(cube.get_color())
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

def plane(plane):
    assert isinstance(plane, shapes.Surface), 'Input must be a Surface object'
    points = plane.get_points()
    glColor3fv(plane.get_color())
    glBegin(GL_QUADS)
    glNormal3fv(plane.get_normal().value)
    for point in points:
        glVertex3fv(point.value)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    for i in range(len(points)):
        glVertex3fv(points[i].value)
        glVertex3fv(points[(i+1)%len(points)].value)
    glEnd()

def sphere(sphere):
    assert isinstance(sphere, shapes.Sphere), 'Input must be a sphere object'
    glColor3fv(sphere.get_color())
    glutSolidSphere(sphere.get_radius(), 10, 10)
