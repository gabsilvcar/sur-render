import sys
import numpy as np
from copy import deepcopy

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.vector import Vector, angle
from SurRender.utils import adjacents
from SurRender.projection import viewport_transform
from SurRender.clipping import cohen_sutherland


class Shape:
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
    
        
class Point(Shape):
    def __init__(self, name, pos, color=(0,0,0)):
        super().__init__(name, type(self), color)
        self.pos = pos
    
    def points(self):
        return [self.pos]
        
    def clipped(self, window):
        inx = window.min().x <= self.pos.x <= window.max().x
        iny = window.min().y <= self.pos.y <= window.max().y   

        if inx and iny:
            return deepcopy(self)
        else:
            return None


class Line(Shape):
    COHEN_SUTHERLAND = 0

    def __init__(self, name, start, end, color=(0,0,0), clipping_algorithm=0):
        super().__init__(name, type(self), color)

        self.start = start
        self.end = end
        self.clipping_algorithm = clipping_algorithm

    def points(self):
        return [self.start, self.end]

    def clipped(self, window):
        p = None
        if self.clipping_algorithm == self.COHEN_SUTHERLAND:
            p = cohen_sutherland([self.start, self.end], window)

        if p is None:
            return None

        l = deepcopy(self)
        l.start = p[0]
        l.end = p[1]

        return l


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
