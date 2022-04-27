import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from src.Shapes import *


class Scene:
    def __init__(self):
        # s = Shape('forma', 0)
        # s.segments.append(Segment(Coord(0,0), Coord(100,100)))

        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)