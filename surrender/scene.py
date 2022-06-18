import sys, random
import numpy as np
from copy import deepcopy
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from surrender.projection import *
from surrender.vector import Vector
from surrender.io.obj_writer import OBJWriter


class Scene:
    def __init__(self):
        self.shapes = []
        self.gliphs = []
        self.window = None

    def save(self, path):
        ow = OBJWriter(self.shapes)
        ow.write(path)

    def projected_shapes(self, origin, target):
        shapes = self.shapes
        shapes = align_shapes_to_window(shapes, origin)
        shapes = [shape.change_viewport(origin.ppc(), target) for shape in shapes]
        shapes = [shape.clipped(target) for shape in shapes if shape.clipped(target) is not None]
        return shapes

    def get_gliphs(self, target):
        return self.gliphs

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)