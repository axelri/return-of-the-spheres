from math import *
import numbers
class Vector:
    ''' A vector class to simplify calculations on vectors '''
    
    def __init__(self, value = [0.0, 0.0, 0.0]):
        # Shorter calls for vectors we use a lot
        assert isinstance(value, str) or isinstance(value, list), \
                'Input must be either a string or a list'

        if __debug__:
            if isinstance(value, str):
                assert value == 'e_x' or value == 'e_y' or value == 'e_z', \
                        'Input string must be a unit vector.'
            if isinstance(value, list):
                for number in value:
                    assert isinstance(number, numbers.Number), \
                    'Every component must be a number.'

        if value == 'e_x':
            self._value = [1.0, 0.0, 0.0]
        elif value == 'e_y':
            self._value = [0.0, 1.0, 0.0]
        elif value == 'e_z':
            self._value = [0.0, 0.0, 1.0]
        else:
            self._value = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
    
    def dot(self, v2):
        ''' Calculates the dot product of the vector and v2 '''
        assert isinstance(v2, Vector), 'Input must be a vector'
        assert len(self.get_value() == v2.get_value()), \
                'Vectors must be of the same length'

        tot = 0
        for i in range(len(self._value)):
            tot += self._value[i] * v2._value[i]
        return tot

    def cross(self, V2):
        ''' Calculates the cross product of the vector and another vector V2.
            Note that it is calculated as (self x V2), since the cross product
            isn't commutative '''
        assert isinstance(V2, Vector), 'Input must be a vector'
        assert len(self.get_value()) == 3 and  len(v2.get_value()) == 3, \
                'Cross product is only defined in 3 dimensions.'

        v1 = self._value
        v2 = V2._value
        out = [v1[1] * v2[2] - v1[2] * v2[1],
               v1[2] * v2[0] - v1[0] * v2[2],
               v1[0] * v2[1] - v1[1] * v2[0]]
        return Vector(out)

    def norm(self):
        ''' Calculates the norm of the vector '''
        return (self.dot(self))**0.5

    def normalize(self):
        ''' Normalizes the vector. Returns None if the vector
        is the zero vector.'''
        n = self.norm()
        v = self._value
        if n != 0:
            for i in range(len(v)):
                v[i] /= n
        else:
            return None
        return Vector(v)

    def __mul__(self, scalar):
        ''' Multiplies the vector with the scalar '''
        assert isinstance(scalar, numbers.Number), \
            'Input must be a real number.' 
        out = [0]*len(self._value)
        for i in range(len(self._value)):
            out[i] = self._value[i] * scalar
        return Vector(out)

    def __add__(self, v2):
        ''' Adds the vector to v2 '''
        assert isinstance(v2, Vector), 'Input must be a vector.'
        assert len(self.get_value() == v2.get_value()), \
                'Vectors must be of the same length'

        out = [0]*len(self._value)
        for i in range(len(self._value)):
            out[i] = self._value[i] + v2._value[i]
        return Vector(out)

    def __sub__(self, v2):
        assert isinstance(v2, Vector), 'Input must be a vector.'
        assert len(self.get_value() == v2.get_value()), \
                'Vectors must be of the same length'

        return self.__add__(v2.__mul__(-1.0))

    # TODO: Make projection a single function with varargs
    # TODO: Write more assertions
    def proj_norm(self, v2):
        ''' Returns the norm of the projection of the vector 
            on the vector v2 '''
        assert isinstance(v2, Vector), 'Input must be a vector.'
        assert len(self.get_value() == v2.get_value()), \
                'Vectors must be of the same length'

        if v2.norm() != 0:
            e2 = v2.normalize()
            return self.dot(e2)
        else:
            return 0

    def projection(self, v2):
        ''' Returns the projection of the vector on the vector v2 '''
        assert isinstance(v2, Vector), 'Input must be a vector.'
        n = self.proj_norm(v2)
        e2 = v2.normalize()
        if e2 != None:
            out = e2.__mul__(n)
            return out
        else:
            return Vector([0]*len(self._value)) # A zero vector

    def proj_syst(self, e1, e2, e3):
        ''' Returns the projection of the vector in the coordinate system
            defined by the vectors e1, e2 and e3 (e1, e2 and e3 must be
            orthogonal'''
        proj1 = self.projection(e1)
        proj2 = self.projection(e2)
        proj3 = self.projection(e3)
        out = proj1.v_add(proj2.v_add(proj3)) # Adds all vectors
        
        return out

    def proj_plane(self, e1, e2):
        ''' Returns the projection of the vector on the plane defined
            by the vectors e1 and e2 (e1 and e2 must be orthogonal) '''
        proj1 = self.projection(e1)
        proj2 = self.projection(e2)
        out = proj1.v_add(proj2)

        return out

    def distance_vector(self, point):
        ''' Returns a vector from self to point '''
        # Rather unnessecary, why not just use point.v_add(self.v_mult(-1.0))?
        p = point.get_value()
        s = self._value
        return Vector([p[0] - s[0],
                       p[1] - s[1],
                       p[2] - s[2]])
    
    def triple_product_1(self, v2, v3):
        ''' Calculates the triple product self x (v2 x v3)
            in a faster and simpler way.'''

        term1 = v2.v_mult(self.dot(v3))
        term2 = v3.v_mult(-self.dot(v2))
        out = term1.v_add(term2)
        return out

    def triple_product_2(self, v2, v3):
        ''' Calculates the triple product (self x v2) x v3
            in a faster and simpler way.'''

        term1 = self.v_mult(-v2.dot(v3))
        term2 = v2.v_mult(self.dot(v3))
        out = term1.v_add(term2)
        return out
