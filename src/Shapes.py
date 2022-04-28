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
            self.segments.append(QtCore.QLine(a, b))

        self.segments.append(QtCore.QLine(points[0], points[-1]))

# class Shape():
#     def __init__(self, name, position1, position2, color, parent=None):
#         self.color = color
#         self.position1 = position1
#         self.position2 = position2
#         self.name = name

#     def paint(self, painter):
#         pass
    
# class Circle(Shape):
#     def __init__(self, name, length, position, color, parent=None):
#         self.color = color
#         self.position = position
#         self.length = length
#         self.name = name
        
#     def paint(self, painter):
#         if not painter.isActive():
#             return
#         painter.save()
#         painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
#         x, y = self.position.x(), self.position.y()
#         painter.drawEllipse(x, y, self.length, self.length)
#         painter.restore()

# class Line(Shape):
#     def paint(self, painter):
#         if not painter.isActive():
#             return
#         painter.save()
#         painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
#         x1, y1 = self.position1.x(), self.position1.y()
#         x2, y2 = self.position2.x(), self.position2.y()
#         painter.drawLine(x1, y1, x2, y2)
#         painter.restore()

# class Rectangle(Shape):
#     def paint(self, painter):
#         if not painter.isActive():
#             return
#         painter.save()
#         painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
#         x1, y1 = self.position1.x(), self.position1.y()
#         x2, y2 = self.position2.x(), self.position2.y()
#         painter.drawRect(x1, y1, x2, y2)
#         painter.restore()
