import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *



class Shape():
    def __init__(self, name, position1, position2, color, parent=None):
        self.color = color
        self.position1 = position1
        self.position2 = position2
        self.name = name

    def paint(self, painter):
        pass
    
class Circle(Shape):
    def __init__(self, name, length, position, color, parent=None):
        self.color = color
        self.position = position
        self.length = length
        self.name = name
        
    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
        x, y = self.position.x(), self.position.y()
        painter.drawEllipse(x, y, self.length, self.length)
        painter.restore()

class Line(Shape):
    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
        x1, y1 = self.position1.x(), self.position1.y()
        x2, y2 = self.position2.x(), self.position2.y()
        painter.drawLine(x1, y1, x2, y2)
        painter.restore()

class Rectangle(Shape):
    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
        x1, y1 = self.position1.x(), self.position1.y()
        x2, y2 = self.position2.x(), self.position2.y()
        painter.drawRect(x1, y1, x2, y2)
        painter.restore()
