import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen, QTransform        
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class Viewport(QWidget):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.translationX = 0
        self.translationY = 0

    def paintEvent(self, event):
        super().paintEvent(event)
        trans = QTransform()
        painter = QPainter(self)
        trans.translate(self.translationX, self.translationY);
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setTransform(trans);

        for shape in self.scene.shapes:
            shape.paint(painter)
            