import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.primitives import Segment


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g 
        self.b = b
    
    def name(self):
        return "name"

class Shape:
    def __init__(self, name, objtype, color=(0,0,0)):
        self.name = name
        self.type = objtype
        self.color = color

        self.coordinates = []
        self.segments = []

class Point(Shape):
    def __init__(self, name, pos, color=(0,0,0)):
        super().__init__(name, type(self), color)
        self.pos = pos
        self.coordinates.append(pos)

class Line(Shape):
    def __init__(self, name, start, end, color=(0,0,0)):
        super().__init__(name, type(self), color)

        self.start = start
        self.end = end

        self.coordinates.append(start)
        self.coordinates.append(end)
        self.segments.append(Segment(start, end))

class Polygon(Shape):
    def __init__(self, name, points, color=(0,0,0)):
        super().__init__(name, type(self), color)

        self.coordinates = points

        for a, b in zip(points, points[1:]):
            self.segments.append(Segment(a, b))

        self.segments.append(Segment(points[0], points[-1]))
