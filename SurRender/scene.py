import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from SurRender.shapes import *


class Scene:
    def __init__(self):
        self.shapes = []
        self.window = None
    
    def projected_shapes(self, origin, target):
        shapes = [shape.change_viewport(origin, target) for shape in self.shapes]
        return shapes

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)