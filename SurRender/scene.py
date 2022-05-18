import sys, random
import numpy as np
from copy import deepcopy

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from SurRender.shapes import *
from SurRender.vector import Vector, angle

class Scene:
    def __init__(self):
        self.shapes = []
        self.window = None

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
        a = self.ppc_shapes(origin)
        shapes = [shape.change_viewport(origin.ppc(), target) for shape in a]
        return shapes

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)