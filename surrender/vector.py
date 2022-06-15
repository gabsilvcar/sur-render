import numpy as np
from numbers import Number

from surrender.math_transforms import *
                                       

def vector_angle(v0, v1):
    if v0.length() == 0 or v1.length() == 0:
        print('iih deu merda')
        return 0

    cos = v0.normalized() @ v1.normalized()
    angle = np.arccos(cos)
    return angle

def vector_x_angle(v):
    z = Vector(0,0,1)
    v_yz = Vector(0, v.y, v.z)
    angle = vector_angle(z, v_yz)
    return (angle if v.y >= 0 else -angle)

def vector_y_angle(v):
    x = Vector(1,0,0)
    v_zx = Vector(v.x, 0, v.z)
    angle = vector_angle(x, v_zx)
    return (angle if v.z >= 0 else -angle)

def vector_z_angle(v):
    y = Vector(0,1,0)
    v_xy = Vector(v.x, v.y, 0)
    angle = vector_angle(y, v_xy)
    return (angle if v.x >= 0 else -angle)

def cross_product(v0, v1):
    a = [v0.x, v0.y, v0.z]
    b = [v1.x, v1.y, v1.z]
    c = np.cross(a, b)
    return Vector(*c)

def dot_product(v0, v1):
    a = [v0.x, v0.y, v0.z]
    b = [v1.x, v1.y, v1.z]
    return np.dot(a, b)


class Vector:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    @property
    def data(self):
        return np.array([self.x, self.y, self.z, 1], dtype=float)

    @data.setter
    def data(self, sequence):
        self.x = sequence[0]
        self.y = sequence[1]
        self.z = sequence[2]

    def length(self):
        return np.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def normalized(self):
        return self / self.length()

    def apply_transform(self, matrix):
        self @= matrix
        return self

    def move(self, vector):
        matrix = translation_matrix(vector)
        self.apply_transform(matrix)
        return self

    def scale(self, vector, around=None):
        if around is None:
            around = Vector(0,0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        s = scale_matrix(vector)

        matrix = t0 @ s @ t1
        self.apply_transform(matrix)
        return self
    
    def rotate_x(self, angle, around=None):
        if around is None:
            around = Vector(0,0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix_x(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)
        return self
    
    def rotate_y(self, angle, around=None):
        if around is None:
            around = Vector(0,0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix_y(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)
        return self
    
    def rotate_z(self, angle, around=None):
        if around is None:
            around = Vector(0,0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix_z(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)
        return self

    def rotate(self, x, y, z, around=None):
        self.rotate_x(x, around)
        self.rotate_y(y, around)
        self.rotate_z(z, around)
        return self

    def __add__(self, other):
        if isinstance(other, Vector):
            x = self.x + other.x
            y = self.y + other.y 
            z = self.z + other.z
            return Vector(x,y,z)
        
        if isinstance(other, Number):
            x = self.x + other
            y = self.y + other 
            z = self.z + other
            return Vector(x,y,z)
        
        raise ValueError('Vector only supports additions with other Vectors or Scalars')

    def __sub__(self, other):
        if isinstance(other, Vector):
            x = self.x - other.x
            y = self.y - other.y 
            z = self.z - other.z
            return Vector(x,y,z)
        
        if isinstance(other, Number):
            x = self.x - other
            y = self.y - other 
            z = self.z - other
            return Vector(x,y,z)
        
        raise ValueError('Vector only supports subtraction with other Vectors or Scalars')

    def __mul__(self, other):
        if isinstance(other, Number):
            x = self.x * other
            y = self.y * other 
            z = self.z * other
            return Vector(x,y,z)
        
        message = 'Vector only supports multiplications against scalars.' \
                  'Try using the operator @ for dot product'

        raise ValueError(message)

    def __truediv__(self, other):
        if isinstance(other, Number):
            x = self.x / other
            y = self.y / other 
            z = self.z / other
            return Vector(x,y,z)
        
        message = 'Vector only supports division against scalars.' \
                  'Try using the operator @ for dot product'

        raise ValueError(message)

    def __matmul__(self, other):
        if isinstance(other, Vector):
            return dot_product(self, other)

        if isinstance(other, np.ndarray):
            v = (self.data @ other)[:3]
            return Vector(*v)

        raise ValueError('Vector only supports dot product between instances of Vector and numpy.ndarray')


    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __iadd__(self, other):
        self.data = (self + other).data
        return self

    def __isub__(self, other):
        self.data = (self - other).data
        return self
    
    def __imul__(self, other):
        self.data = (self * other).data
        return self

    def __itruediv__(self, other):
        self.data = (self / other).data
        return self
    
    def __imatmul__(self, other):
        self.data = (self @ other).data
        return self

    def __str__(self):
        return f'Vector({self.x :.2f}, {self.y :.2f}, {self.z :.2f})'
    
    def __repr__(self):
        return str(self)

