import sys, random
import numpy as np 
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QTransform        
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.utils import adjacents
from SurRender.view import View
from SurRender.shapes import *
from SurRender.scene import Scene
from SurRender.vector import Vector, angle
from SurRender.math_transforms import (viewport_transform, 
                                       translation_matrix, 
                                       scale_matrix, 
                                       rotation_matrix)

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
    
    def rotate(self, angle):
        self.win.rotate(angle)
        self.repaint()
        
    def move_xy(self, x, y):
        v = Vector(x, y)
        self.win.move(v)
        self.repaint()

    def draw_shape(self, shape, painter=None):
        if painter is None:
            painter = QPainter(self)

        if isinstance(shape, Point):
            painter.drawPoint(int(shape.pos.x), int(shape.pos.y)) 

        elif isinstance(shape, Line):
            painter.drawLine(int(shape.start.x), 
                             int(shape.start.y), 
                             int(shape.end.x), 
                             int(shape.end.y))
        
        elif isinstance(shape, Polygon):
            for start, end in adjacents(shape.points(), circular=True):
                painter.drawLine(int(start.x), 
                                 int(start.y), 
                                 int(end.x), 
                                 int(end.y))

    def resizeEvent(self, event):
        super().resizeEvent(event)

        w = self.width()
        h = self.height()

        self.vp = View(
            Vector(0, h),
            Vector(w, h),
            Vector(0,0), 
            Vector(w, 0),
        )

        self.win = View(
            Vector(0, h),
            Vector(w, h),
            Vector(0,0), 
            Vector(w, 0),
        )

    def paintEvent(self, event):
        super().paintEvent(event)
 
        pen = QPen()
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)

        painter = QPainter(self)

        for shape in self.scene.projected_shapes(self.win, self.vp):
            pen.setColor(QColor(*shape.color))
            painter.setPen(pen)
            self.draw_shape(shape, painter)
