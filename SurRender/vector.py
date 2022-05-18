import numpy as np

from SurRender.math_transforms import (translation_matrix, 
                                       scale_matrix,
                                       rotation_matrix,)

def angle(v0, v1):
    uv0 = v0.data / np.linalg.norm(v0.data)
    uv1 = v1.data / np.linalg.norm(v1.data)
    cos = np.dot(uv0, uv1)
    return np.arccos(cos)


class Vector:
    def __init__(self, x, y, z=1):
        self.x = x
        self.y = y
        self.z = z
    
    @property
    def data(self):
        return np.array([self.x, self.y, self.z], dtype=float)

    @data.setter
    def data(self, sequence):
        self.x = sequence[0]
        self.y = sequence[1]
        self.z = sequence[2]

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

    def rotate(self, angle, around=None):
        if around is None:
            around = Vector(0,0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)


    def angle_between(self):
        return 

    def size(self):
        return np.sqrt(self.x*self.x + self.y*self.y)
    
    def __add__(self, other):
        if isinstance(other, Vector):
            other = other.data  
        v = self.data + other
        return Vector(*v)

    def __iadd__(self, other):
        self.data = (self + other).data
        return self
    
    def __sub__(self, other):
        if isinstance(other, Vector):
            other = other.data  
        v = self.data - other
        return Vector(*v)

    def __isub__(self, other):
        self.data = (self - other).data
        return self

    def __mul__(self, other):
        v = self.data * other
        return Vector(*v)
    
    def __imul__(self, other):
        self.data = (self * other).data
        return self
    
    def __truediv__(self, other):
        v = self.data / other
        return Vector(*v)

    def __itruediv__(self, other):
        self.data = (self / other).data
        return self

    def __matmul__(self, other):
        v = self.data @ other
        return Vector(*v)
    
    def __imatmul__(self, other):
        self.data = (self @ other).data
        return self

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __str__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'
    
    def __repr__(self):
        return str(self)

class Segment:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

    def __str__(self):
        return f"Segment({self.p0.data}, {self.p1.data})"