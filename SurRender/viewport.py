import sys, random
import numpy as np 
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QTransform        
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.shapes import *
from SurRender.scene import Scene
from SurRender.primitives import Vector
from SurRender.math_transforms import (viewport_transform, 
                                 translation_matrix, 
                                 scale_matrix, 
                                 rotation_matrix)

class View:
    def __init__(self, start, end):
        self.min = start
        self.max = end

    def width(self):
        return (end - start).x

    def height(self):
        return (end - start).y

    def move(self, delta):
        matrix = translation_matrix(delta)
        self.min @= matrix
        self.max @= matrix
    
    def middle(self):
        return (self.min + self.max) / 2
    
    def zoom(self, amount, around=None):
        if around is None:
            around = Vector(100, 100)

        matrix = scale_matrix(Vector(amount, amount))

        self.min @= matrix
        self.max @= matrix
        
    def __str__(self):
        return f"View({self.xmin} {self.ymin}  {self.xmax} {self.ymax})"


class Viewport(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = Scene()
    
    def zoom_in(self, factor):
        self.win.zoom(1/factor)
        self.repaint()

    def zoom_out(self, factor):
        self.win.zoom(factor)
        self.repaint()
    
    def move_up(self, amount):
        v = Vector(0, -amount)
        self.win.move(v)
        self.repaint()
    
    def move_down(self, amount):
        v = Vector(0, amount)
        self.win.move(v)
        self.repaint()

    def move_left(self, amount):
        v = Vector(amount, 0)
        self.win.move(v)
        self.repaint()

    def move_right(self, amount):
        v = Vector(-amount, 0)
        self.win.move(v)
        self.repaint()
        
    def move_xy(self, x, y):
        v = Vector(x, y)
        self.win.move(v)
        self.repaint()

    def draw_point(self, point, painter=None):
        if painter is None:
            painter = QPainter(self)
        point = viewport_transform(point, self.win, self.vp)
        painter.drawPoint(int(point.x), int(point.y))
    
    def draw_segment(self, segment, painter=None):
        if painter is None:
            painter = QPainter(self)
        p0 = viewport_transform(segment.p0, self.win, self.vp)
        p1 = viewport_transform(segment.p1, self.win, self.vp)
        painter.drawLine(int(p0.x), int(p0.y), int(p1.x), int(p1.y))

    def resizeEvent(self, event):
        self.vp = View(Vector(0,0), 
                       Vector(self.width(), self.width()))

        self.win = View(Vector(0,0), 
                        Vector(self.width(), self.width()))
    
    def paintEvent(self, event):
        super().paintEvent(event)

        if self.win is None:
            self.win = View(0, 0, self.width(), self.height())
            self.vp = View(0, 0, self.width(), self.height())
        
        pen = QPen()
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)

        painter = QPainter(self)

        for shape in self.scene.shapes:
            pen.setColor(QColor(*shape.color))
            painter.setPen(pen)

            for point in shape.coordinates:
                self.draw_point(point, painter)

            for segment in shape.segments:
                self.draw_segment(segment, painter)