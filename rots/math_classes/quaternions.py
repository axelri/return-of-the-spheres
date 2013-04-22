# TODO: Check these functions, there is something wrong in here
# that I can't find...

import vectors
import numbers
from math import cos, sin, sqrt

class Quaternion:
    ''' A quaternion class for rotation handling.
        The values are named [w, x, y, z] or [w, v], where v is [x, y, z]. '''
    
    def __init__(self, value = [1.0, 0.0, 0.0, 0.0]):
        ''' Initializes the quaternion, sets its value. '''
        
        assert isinstance(value, list), 'Input must be a list'
        assert len(value) == 4, 'The quaternion must be of length 4'
        if __debug__:
            for number in value:
                assert isinstance(number, numbers.Number), \
                    'Every component must be a number.'
        
        self.value = value

    def norm(self):
        ''' Returns the norm (lenght) of the quaternion. '''
        v = self.value
        return sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2] + v[3]*v[3])

    def square_norm(self):
        ''' Returns the squared norm of the quaternion,
        cheaper than calling self.norm() since we can skip
        the square root. '''
        v = self.value
        return v[0]*v[0] + v[1]*v[1] + v[2]*v[2] + v[3]*v[3]

    def normalize(self):
        ''' Returns a normalized version of the quaternion
        (a quaternion with the same direction but with lenght 1).'''
        
        out = [0]*4
        n = self.norm()
        for i in range(len(self.value)):
            out[i] = self.value[i]/n

        return Quaternion(out)

    def is_unit(self):
        ''' Checks if the quaternion is of unit length, returns True
        if it is close enough, False otherwise. '''
        v = self.value
        sqNorm = self.square_norm()
        return abs(sqNorm - 1.0) < 0.00001

    def check_normalize(self):
        ''' Checks if the quaternion is of unit length, if not
        it normalizes the quaternion. '''
        
        if not self.is_unit():
            return self.normalize()
        else:
            return self

    def convert_to_matrix(self):
        ''' Converts the quaternion to a rotation matrix of OpenGL standard. '''

        xx = self.value[1]*self.value[1]
        xy = self.value[1]*self.value[2]
        xz = self.value[1]*self.value[3]
        xw = self.value[1]*self.value[0]

        yy = self.value[2]*self.value[2]
        yz = self.value[2]*self.value[3]
        yw = self.value[2]*self.value[0]

        zz = self.value[3]*self.value[3]
        zw = self.value[3]*self.value[0]

        matrix = [1 - 2*yy - 2*zz, 2*xy + 2*zw, 2*xz - 2*yw, 0,
                  2*xy - 2*zw, 1 - 2*xx - 2*zz, 2*yz - 2*xw, 0,
                  2*xz + 2*yw, 2*yz - 2*xw, 1 - 2*xx - 2*yy, 0,
                  0, 0, 0, 1]

        return matrix

    def __mul__(self, quaternion):
        ''' Multiplies self with the given quaternion, overloads * '''
        assert isinstance(quaternion, Quaternion)
        q1 = self.value
        q2 = quaternion.value

        out = [0,0,0,0]
        out[0] = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3]
        out[1] = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2]
        out[2] = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] + q1[3]*q2[1]
        out[3] = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] + q1[3]*q2[0]
        
        return Quaternion(out)

    def conjugate(self):
        ''' Returns the complex conjugate of the quaternion. '''
        value = self.value
        w = value[0]
        x = value[1]
        y = value[2]
        z = value[3]
        return Quaternion([w, -x, -y, -z])

    def __str__(self):
        ''' Returns the string representation of the quaternion.'''
        return self.value.__str__()


def matrix_to_quat(m):
    ''' Converts a rotational matrix to a quaternion. Assumes the
        matrix describes a rotation only, and therefore
        is special orthogonal.

        Input:  m: A matrix represented as a list of lists

        Output: A quaternion describing the same rotation.'''

    assert isinstance(m, list), \
           'Input must be a matrix represented as a list of lists'
    if __debug__:
        for row in m:
            assert isinstance(row, list), \
                   'Input must be a matrix represented as a list of lists'
            for item in row:
                assert isinstance(item, numbers.Number), \
                       'All elements in the matrix must be numbers'
    
    tr = m[0][0] + m[1][1] + m[2][2]

    if tr > 0:
        S = sqrt(tr + 1.0) * 2
        qw = 0.25 * S
        qx = (m[2][1] - m[1][2]) / S
        qy = (m[0][2] - m[2][0]) / S
        qz = (m[1][0] - m[0][1]) / S
    elif m[0][0] > m[1][1] and m[0][0] > m[2][2]:
        S = sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]) * 2
        qw = (m[2][1] - m[1][2]) / S
        qx = 0.25 * S
        qy = (m[0][1] + m[1][0]) / S
        qz = (m[0][2] + m[2][0]) / S
    elif m[1][1] > m[2][2]:
        S = sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2
        qw = (m[0][2] - m[2][0]) / S
        qx = (m[0][1] + m[1][0]) / S
        qy = 0.25 * S
        qz = (m[1][2] + m[2][1]) / S
    else:
        S = sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2
        qw = (m[1][0] - m[0][1]) / S
        qx = (m[0][2] + m[2][0]) / S
        qy = (m[1][2] + m[2][1]) / S
        qz = 0.25 * S

    return Quaternion([qw, qx, qy, qz])

def axis_angle_to_quat(axis, angle):
    ''' Converts a rotation axis and an angle to a quaternion.

    Input:  axis: A rotation axis represented as a vector.
            angle: A number describing the angle of rotation
                in radians.
    Output: A quaternion describing the rotation. '''
    
    assert isinstance(axis, vectors.Vector), \
           'The rotation axis must be a vector'
    assert axis.is_zero() == False, \
           "The rotation axis can't be the zero vector"
    assert axis.dim() == 3, \
           'The rotation axis must be a vector of length 3'
    assert isinstance(angle, numbers.Number), \
           'Angle must be a number'
    
    axis = axis.normalize().value
    w = cos(angle/2.0)
    x = axis[0]*sin(angle/2.0)
    y = axis[1]*sin(angle/2.0)
    z = axis[2]*sin(angle/2.0)

    return Quaternion([w, x, y, z])
