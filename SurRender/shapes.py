import sys
import numpy as np

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.vector import Vector, angle
from SurRender.utils import adjacents
from SurRender.projection import viewport_transform
from SurRender.math_transforms import (translation_matrix,
                                       scale_matrix,
                                       rotation_matrix,)


class Shape:
    def __init__(self, name, objtype, color=(0,0,0)):
        self.name = name
        self.type = objtype
        self.color = color

    def points(self):
        return []
    
    def clip(self, view):
        return None

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
    def __init__(self, name, points, color=(0,0,0), fill=False):
        super().__init__(name, type(self), color)
        self.pts = points
        self.fill = fill

    def points(self):
        return self.pts
    
    def lines(self):
        for start, end in adjacents(self.points(), circular=True):
            yield Line('', start, end)

    def surrounds(self, point):
        last = self.points()[-1] - point
        a = 0

        for p in self.points():
            delta = p - point
            a += angle(last, delta)
            last = delta
            
        return int(np.degrees(a)) % 360 == 0

    def change_viewport(self, source, target):
        points = [viewport_transform(i, source, target) for i in self.pts]
        return Polygon(self.name, points, self.color, self.fill)
    

class Rectangle(Polygon):
    def __init__(self, name, start, end, color=(0,0,0), fill=False):
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
        super().__init__(name, points, color, fill)
