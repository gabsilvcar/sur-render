import sys, random
import numpy as np 
from copy import deepcopy

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QTransform        
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.shapes import *
from SurRender.view import View
from SurRender.scene import Scene
from SurRender.vector import Vector, angle


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
        self.win.rotate(angle, self.win.center())
        self.repaint()
        
    def move_xy(self, x, y):
        v = Vector(x, y)
        self.win.move(v)
        self.repaint()

    def draw_point(self, point, painter=None):
        if painter is None:
            painter = QPainter(self)

        painter.drawPoint(int(point.pos.x), int(point.pos.y)) 
    
    def draw_line(self, line, painter=None):
        if painter is None:
            painter = QPainter(self)

        painter.drawLine(int(line.start.x), 
                         int(line.start.y), 
                         int(line.end.x), 
                         int(line.end.y))
    
    def draw_polygon(self, polygon, painter=None):
        if painter is None:
            painter = QPainter(self)

        if polygon.style == Polygon.FILLED:
            poly = QtGui.QPolygonF() 
            for p in polygon.points():
                poly.append(QtCore.QPointF(p.x, p.y))
            painter.drawPolygon(poly)
        else:
            for line in polygon.lines():
                self.draw_line(line, painter)

    def draw_curve(self, curve, painter=None):
        if painter is None:
            painter = QPainter(self)

        p = curve.as_polygon()
        self.draw_polygon(p, painter)

    def draw_shape(self, shape, painter=None):
        if painter is None:
            painter = QPainter(self)

        if isinstance(shape, Point):
            self.draw_point(shape, painter)

        elif isinstance(shape, Line):
            self.draw_line(shape, painter)

        elif isinstance(shape, Polygon):
            self.draw_polygon(shape, painter)

        elif isinstance(shape, GenericCurve):
            self.draw_curve(shape, painter)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        w = self.width()
        h = self.height()
        b = 50

        self.vp = View(
            Vector(0+b, h-b),
            Vector(w-b, h-b),
            Vector(w-b, 0+b),
            Vector(0+b, 0+b),
        )

        self.win = View(
            Vector(0, h),
            Vector(w, h),
            Vector(w, 0),
            Vector(0,0), 
        )

        self.scene.gliphs = [self.vp]

    def paintEvent(self, event):
        super().paintEvent(event)
 
        pen = QPen()
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)

        brush = QBrush()
        brush.setStyle(1)

        painter = QPainter(self)

        for shape in self.scene.projected_shapes(self.win, self.vp):
            pen.setColor(QColor(*shape.color))
            brush.setColor(QColor(*shape.color))
            painter.setPen(pen)
            painter.setBrush(brush)
            self.draw_shape(shape, painter)

        for shape in self.scene.get_gliphs(self.vp):
            pen.setColor(QColor(*shape.color))
            brush.setColor(QColor(*shape.color))
            painter.setPen(pen)
            painter.setBrush(brush)
            self.draw_shape(shape, painter)
