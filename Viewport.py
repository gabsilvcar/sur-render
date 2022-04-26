import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class Viewport(QWidget):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for shape in self.scene.shapes:
            shape.paint(painter)
            