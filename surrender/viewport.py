from time import time

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget

from surrender.io.obj_io import OBJIO
from surrender.scene import Scene
from surrender.shapes import (
    Bezier,
    BicubicBezier,
    BSpline,
    Line,
    Object3D,
    Point,
    Polygon,
)
from surrender.vector import Vector
from surrender.view import View


class Viewport(QWidget):
    moved = pyqtSignal()
    shapeModified = pyqtSignal()
    shapeSelected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.scene = Scene()
        self.selected_shape = None
        self.current_tool = None

    def open(self, path):
        new_shapes = OBJIO.read(path)
        for shape in new_shapes:
            self.scene.add_shape(shape)
        self.shapeModified.emit()

    def save(self, path):
        OBJIO.write(self.scene.shapes, path)

    def get_shape_by_index(self, index):
        if index not in range(len(self.scene.shapes)):
            return None
        return self.scene.shapes[index]

    def add_shape(self, shape):
        self.scene.add_shape(shape)
        self.shapeModified.emit()
        self.repaint()

    def remove_shape(self, shape):
        self.scene.remove_shape(shape)
        self.shapeModified.emit()
        self.repaint()

    def zoom(self, factor):
        self.win.zoom(factor)
        self.repaint()
        self.moved.emit()

    def rotate(self, delta):
        self.win.rotate(delta, self.win.center())
        self.repaint()
        self.moved.emit()

    def move(self, vector):
        scalar = self.win.width() / self.vp.width()
        self.win.move(vector * scalar)
        self.repaint()
        self.moved.emit()

    def draw_point(self, point, painter=None):
        if painter is None:
            painter = QPainter(self)

        (pos,) = point.projection_points()
        painter.drawPoint(int(pos.x), int(pos.y))

    def draw_line(self, line, painter=None):
        if painter is None:
            painter = QPainter(self)

        start, end = line.projection_points()

        painter.drawLine(int(start.x), int(start.y), int(end.x), int(end.y))

    def draw_polygon(self, polygon, painter=None):
        if painter is None:
            painter = QPainter(self)

        if polygon.style == Polygon.FILLED:
            poly = QtGui.QPolygonF()
            for p in polygon.visual_points():
                poly.append(QtCore.QPointF(p.x, p.y))
            painter.drawPolygon(poly)
        else:
            for start, end in polygon.clipped_segments():
                painter.drawLine(int(start.x), int(start.y), int(end.x), int(end.y))

                # self.draw_line(line, painter)

    def draw_curve(self, curve, painter=None):
        if painter is None:
            painter = QPainter(self)

        poly = curve.as_polygon()
        poly.CLIPPING_ALGORITHM = curve.CLIPPING_ALGORITHM
        self.draw_polygon(poly, painter)

    def draw_3d(self, shape, painter=None):
        if painter is None:
            painter = QPainter(self)

        for start, end in shape.clipped_segments():
            painter.drawLine(int(start.x), int(start.y), int(end.x), int(end.y))

    def draw_shape(self, shape, painter=None):
        if painter is None:
            painter = QPainter(self)

        if isinstance(shape, Point):
            self.draw_point(shape, painter)

        elif isinstance(shape, Line):
            self.draw_line(shape, painter)

        elif isinstance(shape, Polygon):
            self.draw_polygon(shape, painter)

        # elif isinstance(shape, Bezier | BSpline):
        #     self.draw_curve(shape, painter)

        elif isinstance(shape, Object3D):
            self.draw_3d(shape, painter)

        # elif isinstance(shape, BicubicBezier):
        #     self.draw_3d(shape.as_object_3d(), painter)

        else:
            raise ValueError(f"The object {shape} is not supported.")

    def resizeEvent(self, event):
        super().resizeEvent(event)

        w = self.width()
        h = self.height()
        b = 50

        self.vp = View(
            Vector(0 + b, h - b),
            Vector(w - b, h - b),
            Vector(w - b, 0 + b),
            Vector(0 + b, 0 + b),
        )

        self.win = View(
            Vector(0, h),
            Vector(w, h),
            Vector(w, 0),
            Vector(0, 0),
        )

        self.scene.gliphs = [self.vp, Point("Center", self.vp.center())]

    def paintEvent(self, event):
        super().paintEvent(event)

        pen = QPen()
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)

        brush = QBrush()
        brush.setStyle(1)

        painter = QPainter(self)

        s = time()
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
        e = time()
        print("FPS", 1 / (e - s))
