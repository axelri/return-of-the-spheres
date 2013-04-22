# TODO: Make a Matrix class? We have two different types of matrices
# (OpenGL and list of lists), which makes it a little harder to have
# one single matrix class...

import numbers
from math import cos, sin, pi

from math_classes import vectors

def gauss_jordan(m, eps = 1.0/(10**10)):
    """ Puts given matrix (2D array) into the Reduced Row Echelon Form.
        Returns True if successful, False if 'm' is singular.
        NOTE: make sure all the matrix items support fractions!
        Int matrix will NOT work!
        Written by Jarno Elonen in April 2005, released into Public Domain"""

    assert isinstance(m, list), \
           'Input must be a matrix represented as a list of lists'
    assert isinstance(eps, numbers.Number), 'Input must be a number'
    if __debug__:
        for row in m:
            assert isinstance(row, list), \
                   'Input must be a matrix represented as a list of lists'
            for item in row:
                assert isinstance(item, numbers.Number), \
                       'All elements in the matrix must be numbers'
    
    (h, w) = (len(m), len(m[0]))
    for y in range(0,h):
        maxrow = y
        for y2 in range(y+1, h):    # Find max pivot
            if abs(m[y2][y]) > abs(m[maxrow][y]):
                maxrow = y2
        (m[y], m[maxrow]) = (m[maxrow], m[y])
        if abs(m[y][y]) <= eps:     # Singular?
            return False
        for y2 in range(y+1, h):    # Eliminate column y
            c = m[y2][y] / m[y][y]
            for x in range(y, w):
                m[y2][x] -= m[y][x] * c
    for y in range(h-1, 0-1, -1): # Backsubstitute
        c  = m[y][y]
        for y2 in range(0,y):
            for x in range(w-1, y-1, -1):
                m[y2][x] -=  m[y][x] * m[y2][y] / c
        m[y][y] /= c
        for x in range(h, w):       # Normalize row y
            m[y][x] /= c
    return True

def solve(M, b):
    """
    solves M*x = b
    return vector x so that M*x = b
    :param M: a matrix in the form of a list of list
    :param b: a vector in the form of a simple list of scalars
    """
    assert isinstance(b, list), \
           'Input must be a vector repressented as a list'
    assert isinstance(M, list), \
           'Input must be a matrix represented as a list of lists'
    if __debug__:
        for row in M:
            assert isinstance(row, list), \
                   'Input must be a matrix represented as a list of lists'
            for item in row:
                assert isinstance(item, numbers.Number), \
                       'All elements in the matrix must be numbers'
    
    m2 = [row[:]+[right] for row,right in zip(M,b) ]
    return [row[-1] for row in m2] if gauss_jordan(m2) else None

def inv(M):
    """
    return the inv of the matrix M
    """

    assert isinstance(M, list), \
           'Input must be a matrix represented as a list of lists'
    if __debug__:
        for row in M:
            assert isinstance(row, list), \
                   'Input must be a matrix represented as a list of lists'
            for item in row:
                assert isinstance(item, numbers.Number), \
                       'All elements in the matrix must be numbers'
    
    #clone the matrix and append the identity matrix
    # [int(i==j) for j in range_M] is nothing but the i:th row of the identity matrix
    m2 = [row[:]+[int(i==j) for j in range(len(M) )] for i,row in enumerate(M) ]
    # extract the appended matrix (kind of m2[m:,...]
    return [row[len(M[0]):] for row in m2] if gauss_jordan(m2) else None

def zeros( s , zero=0):
    """
    return a matrix of size `size`
    :param size: a tuple containing dimensions of the matrix
    :param zero: the value to use to fill the matrix (by default it's zero )
    """
    return [zeros(s[1:] ) for i in range(s[0] ) ] if not len(s) else zero

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

    assert isinstance(axis, vectors.Vector), \
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

