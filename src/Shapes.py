import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from src.primitives import Segment


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g 
        self.b = b
    
    def name(self):
        return "name"

class Shape:
    def __init__(self, name, objtype):
        self.name = name
        self.type = objtype
        self.color = Color(0,0,0)

        self.coordinates = []
        self.segments = []


class Point(Shape):
    def __init__(self, name, pos):
        super().__init__(name, type(self))
        self.pos = pos
        self.coordinates.append(pos)


class Line(Shape):
    def __init__(self, name, start, end):
        super().__init__(name, type(self))

        self.start = start
        self.end = end

        self.coordinates.append(start)
        self.coordinates.append(end)
        self.segments.append(Segment(start, end))

class Polygon(Shape):
    def __init__(self, name, points):
        super().__init__(name, type(self))

        self.coordinates = points

        for a, b in zip(points, points[1:]):
            self.segments.append(Segment(a, b))

        self.segments.append(Segment(points[0], points[-1]))
