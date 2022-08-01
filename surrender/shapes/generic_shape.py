from copy import deepcopy
from abc import ABC
from surrender.vector import Vector
from surrender.projection import viewport_transform


class GenericShape(ABC):
    def __init__(self, name, objtype, color=(0, 0, 0)):
        self.name = name
        self.type = objtype
        self.color = color
    
    def structural_points(self):
        return []
        
    def projection_points(self):
        return []
    
    def clipped_points(self):
        return []
    
    def clip(self, window_min, window_max):
        return True

    def revert_projection(self):
        pass

    def copy(self):
        return deepcopy(self)

    def center(self):
        pts = self.structural_points()
        s = Vector(0, 0, 0)

        for p in pts:
            s += p

        if pts:
            s /= len(pts)
        return s

    def apply_transform(self, matrix):
        for p in self.structural_points():
            p.apply_transform(matrix)

    def move(self, vector):
        for p in self.structural_points():
            p.move(vector)

    def scale(self, vector, around=None):
        for p in self.structural_points():
            p.scale(vector, around)

    def rotate_x(self, angle, around=None):
        for p in self.structural_points():
            p.rotate_x(angle, around)

    def rotate_y(self, angle, around=None):
        for p in self.structural_points():
            p.rotate_y(angle, around)

    def rotate_z(self, angle, around=None):
        for p in self.structural_points():
            p.rotate_z(angle, around)

    def rotate(self, delta, around=None):
        for p in self.structural_points():
            p.rotate(delta, around)
