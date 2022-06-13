import sys, random
import numpy as np
from copy import deepcopy

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.projection import *
from SurRender.vector import Vector
from SurRender.io.obj_writer import OBJWriter
from SurRender.shapes import Object3D


class Scene:
    def __init__(self):
        v0 = Vector(0,0,0) * 100
        v1 = Vector(0,0,1) * 100
        v2 = Vector(0,1,0) * 100
        v3 = Vector(0,1,1) * 100
        v4 = Vector(1,0,0) * 100
        v5 = Vector(1,0,1) * 100
        v6 = Vector(1,1,0) * 100
        v7 = Vector(1,1,1) * 100

        pairs = [
            (v0, v1),
            (v0, v2),
            (v0, v4),
            (v1, v3),
            (v1, v5),
            (v2, v3),
            (v2, v6),
            (v3, v7),
            (v4, v5),
            (v4, v6),
            (v5, v7),
            (v6, v7),
        ]

        
        self.shapes = [Object3D('aa', pairs, (255,0,0))]
        self.gliphs = []
        self.window = None

    def save(self, path):
        ow = OBJWriter(self.shapes)
        ow.write(path)

    def projected_shapes(self, origin, target):
        # shapes = self.shapes
        shapes = world_to_ppc(self.shapes, origin)
        # shapes = align_shapes_to_window(shapes, origin)
        shapes = [shape.change_viewport(origin.ppc(), target) for shape in shapes]
        shapes = [shape.clipped(target) for shape in shapes if shape.clipped(target) is not None]
        return shapes

    def get_gliphs(self, target):
        return self.gliphs

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)