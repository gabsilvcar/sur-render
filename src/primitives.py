import numpy as np


class Vector:
    def __init__(self, x, y, z=0):
        self.data = np.array([x,y,z])
    
    @property
    def x(self):
        return self.data[0]
    
    @property
    def y(self):
        return self.data[1]
    
    @property
    def z(self):
        return self.data[2]

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