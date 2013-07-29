# TODO: Make a Matrix class? We have two different types of matrices
# (OpenGL and list of lists), which makes it a little harder to have
# one single matrix class...

import numbers
from math import cos, sin, pi

from math_classes.vectors import Vector

def OpenGL_to_matrix(matrix):
    ''' Takes a matrix in OpenGL standard (a single list of all elements
    in column major order, 4x4) and turns it into a matrix represented as
    a list of lists in row major order. The matrices must be 4x4.

    Input:  matrix: A 4x4 matrix in OpenGL standard (a list with
                all 16 elements in column major order).

    Output: out: A 4x4 matrix represented as a list of lists in
                row major order. '''
    
    assert isinstance(matrix, list), \
           'Input must be a matrix in OpenGl standard'
    assert len(matrix) == 16, 'Input must be a matrix in OpenGl standard'
    if __debug__:
        for item in matrix:
            assert isinstance(item, numbers.Number), \
                   'Input must be a matrix in OpenGl standard'

    copy = matrix[:]
    out  = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for i in range(len(copy)):
        out[i%4][i//4] = copy[i]
    return out

def matrix_to_OpenGL(matrix):
    ''' Takes a matrix represented as a list of lists and turns it
    into a matrix in OpenGL standard. The matrices must be 4x4.

    Input:  matrix: A 4x4 matrix represented as a list of lists in
                row major order.

    Output: out: A 4x4 matrix in OpenGL standard (a list with
                all 16 elements in column major order). '''
    
    assert isinstance(matrix, list), \
           'Input must be a matrix represented as a list of lists'
    assert len(matrix) == 4, 'The matrix must be 4x4'
    if __debug__:
        for row in matrix:
            assert isinstance(row, list), \
                   'Input must be a matrix represented as a list of lists'
            assert len(row) == 4, 'The matrix must be 4x4'
            for elem in row:
                assert isinstance(elem, numbers.Number), \
                       'All elements must be numbers'

    copy = matrix[:][:]
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for i in range(4):
        for j in range(4):
            out[4*j + i] = copy[i][j]

    return out

def generate_rotation_matrix(axis, angle):
    ''' Generates a rotation matrix according to OpenGL standards
    with a rotation of angle (in radians) and axis as rotation axis.

    Input:  axis: A vector describing the rotation axis.
            angle: A number describing the angle of rotation
                in radians.

    Output: rotation_matrix: A 4x4 matrix in OpenGL standard
                (a list with all 16 elements in column major
                order) describing the rotation. '''

    assert isinstance(axis, Vector), \
           'The axis must be a vector'
    assert isinstance(angle, numbers.Number), \
           'The angle must be a number'

    v = axis.normalize()

    if v == None:
        v = [0, 0, 0]   #Dummy variable, will return identity matrix
                        #whatever we put here
    else:
        v = v.value
    
    rotation_matrix = [v[0] * v[0] * (1.0 - cos(angle)) + cos(angle),
                       v[1] * v[0] * (1.0 - cos(angle)) + v[2] * sin(angle),
                       v[0] * v[2] * (1.0 - cos(angle)) - v[1] * sin(angle),
                       0.0,
                       v[0] * v[1] * (1.0 - cos(angle)) - v[2] * sin(angle),
                       v[1] * v[1] * (1.0 - cos(angle)) + cos(angle),
                       v[1] * v[2] * (1.0 - cos(angle)) + v[0] * sin(angle),
                       0.0,
                       v[0] * v[2] * (1.0 - cos(angle)) + v[1] * sin(angle),
                       v[1] * v[2] * (1.0 - cos(angle)) - v[0] * sin(angle),
                       v[2] * v[2] * (1.0 - cos(angle)) + cos(angle),
                       0.0,
                       0.0,
                       0.0,
                       0.0,
                       1.0]
    return rotation_matrix

def matrix_mult(a, b):
    ''' Multiplies the matrices a and b as (a * b).
        The matrices are given in OpenGL standard, that is,
        a 4x4 matrix written in column-major order, represented
        as a list.

        Input:  a,b: Matrices in OpenGL standard (a list with
                    all 16 elements in column major order).

        Output: out: The matrix product of a and b, a matrix
                    in OpenGL standard (a list with all 16
                    elements in column major order). '''
    
    out = [0]*16
    for i in range(4):
        for k in range(4):
            out[4*i + k] = a[k]*b[4*i] + a[k+4]*b[4*i+1] + a[k+8]*b[4*i+2] + a[k+12]*b[4*i+3]
    return out
            
def identity():
    ''' Returns an identity matrix in OpenGL standard
    (a list with all 16 elements in column major order). '''
    
    return [1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0]

def OpenGL_to_ODE(matrix):
    ''' Takes a matrix on OpenGL form (16-list, column major)
        and converts it to ODE form (9-list, row major) '''

    #TODO: Make prettier?

    c = matrix[:]
    out = [c[0], c[4], c[8],
            c[1], c[5], c[9],
            c[2], c[6], c[10]]
    return out

def ODE_to_OpenGL(matrix):
    ''' Takes a matrix on ODE form (9-list, row major)
        and converts it to OpenGL form (16-list, column major) '''

    #TODO: Make prettier?

    c = matrix[:]
    out = [c[0], c[3], c[6], 0,
            c[1], c[4], c[7], 0,
            c[2], c[5], c[8], 0,
            0, 0, 0, 1]
    return out