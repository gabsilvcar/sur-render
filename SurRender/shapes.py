import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.math_transforms import viewport_transform


class Shape:
    def __init__(self, name, objtype, color=(0,0,0)):
        self.name = name
        self.type = objtype
        self.color = color

class Point(Shape):
    def __init__(self, name, pos, color=(0,0,0)):
        super().__init__(name, type(self), color)
        self.pos = pos

    def change_viewport(self, source, target):
        pos = viewport_transform(self.pos, source, target)
        return Point(self.name, pos, self.color)

class Line(Shape):
    def __init__(self, name, start, end, color=(0,0,0)):
        super().__init__(name, type(self), color)

        self.start = start
        self.end = end

    def change_viewport(self, source, target):
        start = viewport_transform(self.start, source, target)
        end = viewport_transform(self.end, source, target)
        return Line(self.name, start, end, self.color)

class Polygon(Shape):
    def __init__(self, name, points, color=(0,0,0)):
        super().__init__(name, type(self), color)
        self.points = points

    def change_viewport(self, source, target):
        points = [viewport_transform(i, source, target) for i in self.points]
        return Polygon(self.name, points, self.color)