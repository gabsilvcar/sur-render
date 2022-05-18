import sys

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.vector import Vector
from SurRender.math_transforms import (viewport_transform,
                                       translation_matrix,
                                       scale_matrix,
                                       rotation_matrix,)


class Shape:
    def __init__(self, name, objtype, color=(0,0,0)):
        self.name = name
        self.type = objtype
        self.color = color

    def points(self):
        return []
    
    def apply_transform(self, matrix):
        for p in self.points():
            p.apply_transform(matrix)

    def center(self):
        pts = self.points()
        s = Vector(0,0,0)

        for p in pts:
            s += p
        
        if pts:
            s /= len(pts)
        return s 
    
    def move(self, vector):
        matrix = translation_matrix(vector)
        self.apply_transform(matrix)

    def scale(self, vector, around=Vector(0,0)):    
        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        s = scale_matrix(vector)

        matrix = t0 @ s @ t1
        self.apply_transform(matrix)

    def rotate(self, angle, around=Vector(0,0)):
        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)

        
class Point(Shape):
    def __init__(self, name, pos, color=(0,0,0)):
        super().__init__(name, type(self), color)
        self.pos = pos
    
    def points(self):
        return [self.pos]
        
    def change_viewport(self, source, target):
        pos = viewport_transform(self.pos, source, target)
        return Point(self.name, pos, self.color)

class Line(Shape):
    def __init__(self, name, start, end, color=(0,0,0)):
        super().__init__(name, type(self), color)

        self.start = start
        self.end = end
    
    def points(self):
        return [self.start, self.end]

    def change_viewport(self, source, target):
        start = viewport_transform(self.start, source, target)
        end = viewport_transform(self.end, source, target)
        return Line(self.name, start, end, self.color)

class Polygon(Shape):
    def __init__(self, name, points, color=(0,0,0)):
        super().__init__(name, type(self), color)
        self.pts = points
    
    def points(self):
        return self.pts

    def change_viewport(self, source, target):
        points = [viewport_transform(i, source, target) for i in self.pts]
        return Polygon(self.name, points, self.color)
    

class Rectangle(Polygon):
    def __init__(self, name, start, end, color=(0,0,0)):
        '''
        p0 ------ p1 
        |          |
        |          |
        |          |
        p2 ------ p3 
        '''

        self.p0 = start
        self.p1 = Vector(start.x, end.y)
        self.p2 = end
        self.p3 = Vector(end.x, start.y)

        points = [self.p0, self.p1, self.p2, self.p3]
        super().__init__(name, points, color)
