import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *



class Shape():
    def __init__(self, name, length, position, color, parent=None):
        self.color = color
        self.position = position
        self.length = length
        self.name = name

    def paint(self, painter):
        pass
    
class Circle(Shape):
    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
        x, y = self.position.x(), self.position.y()
        painter.drawEllipse(x, y, self.length, self.length)
        painter.restore()

