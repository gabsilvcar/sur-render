import sys, random
import numpy as np
from copy import deepcopy
from surrender.projection import *
from surrender.shapes import *
from surrender.vector import Vector


class Scene:
    def __init__(self):
        self.shapes = []
        self.gliphs = []
        self.window = None

    def projected_shapes(self, origin, target):
        shapes = self.shapes
        shapes = perspective_projection(shapes, origin)
        shapes = [shape.change_viewport(origin.ppc(), target) for shape in shapes]
        shapes = [shape.clipped(target) for shape in shapes if shape.clipped(target) is not None]
        return shapes

    def get_gliphs(self, target):
        return self.gliphs

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)