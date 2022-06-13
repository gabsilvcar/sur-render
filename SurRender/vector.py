import numpy as np
from numbers import Number

from SurRender.math_transforms import *
                                       

def vector_angle(v0, v1):
    cos = v0.normalized() @ v1.normalized()
    angle = np.arccos(cos)
    return angle

def vector_x_angle(v):
    x = Vector(1,0,0)
    return vector_angle(x, v)

def vector_y_angle(v):
    y = Vector(0,1,0)
    return vector_angle(y, v)

def vector_z_angle(v):
    z = Vector(0,0,1)
    return vector_angle(z, v)

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
    def __init__(self, x, y, z=5):
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

    def move(self, vector):
        matrix = translation_matrix(vector)
        self.apply_transform(matrix)

    def scale(self, vector, around=None):
        if around is None:
            around = Vector(0,0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        s = scale_matrix(vector)

        matrix = t0 @ s @ t1
        self.apply_transform(matrix)
    
    def rotate_x(self, angle, around=None):
        if around is None:
            around = Vector(0,0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix_x(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)
    
    def rotate_y(self, angle, around=None):
        if around is None:
            around = Vector(0,0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix_y(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)
    
    def rotate_z(self, angle, around=None):
        if around is None:
            around = Vector(0,0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix_z(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)

    def rotate(self, angle, around=None):
        self.rotate_z(-angle, around)

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
        return f'Vector({self.x}, {self.y}, {self.z})'
    
    def __repr__(self):
        return str(self)

