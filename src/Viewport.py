import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen, QTransform        
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from src.Shapes import *


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
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.win = None
    
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

    def transform(self, point):
        if self.win is None:
            self.win = View(0, 0, self.width(), self.height())

        w = self.win
        vp = View(0, 0, self.width(), self.height())
        out = Coord(0,0)

        out.x = (vp.xmax - vp.xmin)
        out.x *= (point.x() - w.xmin)
        out.x /= (w.xmax - w.xmin)

        out.y = (point.y() - w.ymin) / (w.ymax - w.ymin)
        out.y *= (vp.ymax - vp.ymin)
        
        return out

    def resizeEvent(self, event):
        self.win = View(0, 0, self.width(), self.height())
    
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)

        for shape in self.scene.shapes:
            for coord in shape.coordinates:
                c = self.transform(coord)
                painter.drawPoint(c.x, c.y)

            for segment in shape.segments:
                s = self.transform(segment.p1())
                e = self.transform(segment.p2())
                painter.drawLine(s.x, s.y, e.x, e.y)