import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QTransform        
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from src.Shapes import *
from src.Scene import Scene
from src.math_transforms import viewport_transform

class View:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def width(self):
        return self.xmax - self.xmin 

    def height(self):
        return self.ymax - self.ymin
    
    def __str__(self):
        return f"View({self.xmin} {self.ymin}  {self.xmax} {self.ymax})"


class Viewport(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = Scene()
    
    def zoom_in(self, factor):
        w = self.win.width() * factor / 2
        h = self.win.height() * factor / 2
        self.win.xmin += w
        self.win.xmax -= w
        self.win.ymin += h
        self.win.ymax -= h
        self.repaint()

    def zoom_out(self, factor):
        w = self.win.width() * factor / 2
        h = self.win.height() * factor / 2
        self.win.xmin -= w
        self.win.xmax += w
        self.win.ymin -= h
        self.win.ymax += h
        self.repaint()
    
    def move_up(self, amount):
        self.win.ymin += amount
        self.win.ymax += amount
        self.repaint()
    
    def move_down(self, amount):
        self.win.ymin -= amount
        self.win.ymax -= amount
        self.repaint()

    def move_left(self, amount):
        self.win.xmin += amount
        self.win.xmax += amount
        self.repaint()

    def move_right(self, amount):
        self.win.xmin -= amount
        self.win.xmax -= amount
        self.repaint()

    def draw_point(self, point, painter=None):
        if painter is None:
            painter = QPainter(self)
        point = viewport_transform(point, self.win, self.vp)
        painter.drawPoint(point.x, point.y)
    
    def draw_segment(self, segment, painter=None):
        if painter is None:
            painter = QPainter(self)
        p0 = viewport_transform(segment.p0, self.win, self.vp)
        p1 = viewport_transform(segment.p1, self.win, self.vp)
        painter.drawLine(p0.x, p0.y, p1.x, p1.y)

    def resizeEvent(self, event):
        self.vp = View(0, 0, self.width(), self.height())
        self.win = View(0, 0, self.width(), self.height())
    
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