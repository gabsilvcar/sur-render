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

    def ppc_shapes(self, view):
        wc = view.center()
        shapes = []

        for shape in self.shapes:
            uv = view.up_vector()
            y  = Vector(0,1,0)
            a  = angle(uv, y) 

            shape = deepcopy(shape)
            shape.move(-wc)
            shape.rotate(a)
            shapes.append(shape)

        return shapes

    def projected_shapes(self, origin, target):
        shapes = world_to_ppc(self.shapes, origin)
        shapes = [shape.change_viewport(origin.ppc(), target) for shape in shapes]
        return shapes

    def get_gliphs(self, target):
        # return self.gliphs

        start = Vector(50,50)
        end   = Vector(target.width(), target.height()) - start

        rect = Rectangle(
            "Limits",
            start, 
            end,
            (255,0,0)
        )

        return [rect]

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)