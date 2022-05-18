import numpy as np

def angle(v0, v1):
    uv0 = v0.data / np.linalg.norm(v0.data)
    uv1 = v1.data / np.linalg.norm(v1.data)
    cos = np.dot(uv0, uv1)
    return np.arccos(cos)


class Vector:
    def __init__(self, x, y, z=1):
        self.data = np.array([x,y,z], dtype=float)
    
    @property
    def x(self):
        return self.data[0]
    
    @property
    def y(self):
        return self.data[1]
    
    @property
    def z(self):
        return self.data[2]

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