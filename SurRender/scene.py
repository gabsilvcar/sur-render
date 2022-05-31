import sys, random
import numpy as np
from copy import deepcopy

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.shapes import *
from SurRender.projection import world_to_ppc, clip
from SurRender.vector import Vector, angle
from SurRender.io.obj_writer import OBJWriter


class Scene:
    def __init__(self):
        self.shapes = []
        self.gliphs = []
        self.window = None

    def save(self, path):
        ow = OBJWriter(self.shapes)
        ow.write(path)

    def projected_shapes(self, origin, target):
        shapes = world_to_ppc(self.shapes, origin)
        shapes = [shape.change_viewport(origin.ppc(), target) for shape in shapes]
        shapes = [shape.clipped(target) for shape in shapes if shape.clipped(target) is not None]
        return shapes

    def get_gliphs(self, target):
        return self.gliphs

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)