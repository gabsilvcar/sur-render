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
from SurRender.clipping import cohen_sutherland, liang_barsky, sutherland_hodgeman
from SurRender.parametric_curves import bezier
from SurRender.utils import group_by

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
    DO_NOT_CLIP = 0
    TRIVIAL = 1

    CLIPPING_ALGORITHM = TRIVIAL


    def __init__(self, name, pos, color=(0,0,0)):
        super().__init__(name, 'Point', color)
        self.pos = pos
    
    def points(self):
        return [self.pos]
        
    def clipped(self, window):
        if self.CLIPPING_ALGORITHM == self.DO_NOT_CLIP:
            return self
            
        inx = window.min().x <= self.pos.x <= window.max().x
        iny = window.min().y <= self.pos.y <= window.max().y   

        if inx and iny:
            return deepcopy(self)
        else:
            return None


class Line(Shape):
    DO_NOT_CLIP = 0
    COHEN_SUTHERLAND = 1
    LIANG_BARSKY = 2

    CLIPPING_ALGORITHM = COHEN_SUTHERLAND

    def __init__(self, name, start, end, color=(0,0,0)):
        super().__init__(name, 'Line', color)
        self.start = start
        self.end = end

    def points(self):
        return [self.start, self.end]

    def clipped(self, window):
        if self.CLIPPING_ALGORITHM == self.COHEN_SUTHERLAND:
            p = cohen_sutherland(self.start, self.end, window)
        elif self.CLIPPING_ALGORITHM == self.LIANG_BARSKY:
            p = liang_barsky(self.start, self.end, window)
        else:
            return self
            
        if p is None:
            return None

        l = deepcopy(self)
        l.start = p[0]
        l.end = p[1]

        return l


class Polygon(Shape):
    DO_NOT_CLIP = 0
    SUTHERLAND_HODGEMAN = 1

    OPEN = 0
    CLOSED = 1
    FILLED = 2 | CLOSED # if it is filled must be closed as well

    CLIPPING_ALGORITHM = SUTHERLAND_HODGEMAN

    def __init__(self, name, points, color=(0,0,0), style=CLOSED):
        super().__init__(name, 'Polygon', color)
        self.pts = points
        self.style = style

    def points(self):
        return self.pts
    
    def lines(self):
        circular = self.style != self.OPEN
        for start, end in adjacents(self.points(), circular=circular):
            yield Line('', start, end)

    def clipped(self, window):
        clipped_points = []

        if self.CLIPPING_ALGORITHM == self.DO_NOT_CLIP:
            return self
        elif self.CLIPPING_ALGORITHM == self.SUTHERLAND_HODGEMAN:
            closed = self.style & self.CLOSED
            clipped_points = sutherland_hodgeman(self.points(), window, closed)

        c = deepcopy(self)
        c.pts = clipped_points
        return c 


class GenericCurve(Shape):
    DO_NOT_CLIP = 0
    SUTHERLAND_HODGEMAN = 1

    OPEN = 0
    CLOSED = 1
    FILLED = 2 | CLOSED # if it is filled must be closed as well

    CLIPPING_ALGORITHM = SUTHERLAND_HODGEMAN

    def __init__(self, name, color=(0,0,0), style=CLOSED):
        super().__init__(name, 'Curve', color)
        self.style = style


class Bezier(GenericCurve):
    def __init__(self, name, control_points, color=(0,0,0)):
        super().__init__(name, color, False)
        self.type = 'Bezier'
        self.resolution = 5
        self._control_points = control_points
        self._blended_points = self.set_resolution(self.resolution)

    def set_resolution(self, resolution):
        self.resolution = resolution
        self._blended_points = self.blended_points()

    def as_polygon(self):
        p = Polygon(self.name, self._blended_points, self.color, Polygon.OPEN)
        p.CLIPPING_ALGORITHM = self.CLIPPING_ALGORITHM
        return p

    def points(self):
        return self._control_points
    
    def lines(self):
        circular = self.style != self.OPEN
        for start, end in adjacents(self.blended_points(), circular=False):
            yield Line('', start, end)

    def packs_of_points(self, points):
        last_point = None
        for i in range(0, len(points)-1, 3):
            yield points[i:(i+4)]

    def blended_points(self):
        points = []

        for p in self.packs_of_points(self.points()):
            for i in range(self.resolution+1):
                x, y, z = bezier(i/self.resolution, p)
                points.append(Vector(x,y,z))
        return points
    
    def clipped(self, window):
        clipped_points = []

        size = 1
        for start, end in adjacents(self.points(), circular=False):
            delta = end - start
            size = max(size, delta.x, delta.y, delta.z)
        self.set_resolution(int(size) // 15 + 1)

        if self.CLIPPING_ALGORITHM == self.DO_NOT_CLIP:
            return self

        closed = self.style & self.CLOSED
        clipped_points = sutherland_hodgeman(self.blended_points(), window, closed)

        c = deepcopy(self)
        c._blended_points = clipped_points
        return c 


class Rectangle(Polygon):
    def __init__(self, name, start, end, color=(0,0,0), style=1):
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
        super().__init__(name, points, color, style)
        self.type = 'Rectangle'
