from copy import deepcopy

from surrender.vector import Vector, angle
from surrender.projection import viewport_transform


class GenericShape:
    def __init__(self, name, objtype, color=(0,0,0)):
        self.name = name
        self.type = objtype
        self.color = color

    def clipped(self, window):
        return self

    def points(self):
        return []
    
    def clip(self, view):
        return None

    def apply_transform(self, matrix):
        for p in self.points():
            p.apply_transform(matrix)

    def change_viewport(self, source, target):
        v = deepcopy(self)
        for p in self.points():
            viewport_transform(p, source, target)
        return self

    def center(self):
        pts = self.points()
        s = Vector(0,0,0)

        for p in pts:
            s += p
        
        if pts:
            s /= len(pts)
        return s 

    def move(self, vector):
        for p in self.points():
            p.move(vector)

    def scale(self, vector, around=None):
        for p in self.points():
            p.scale(vector, around)
    
    def rotate(self, angle, around=None):
        for p in self.points():
            p.rotate(angle, around)
