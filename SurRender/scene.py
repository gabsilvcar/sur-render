import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from SurRender.shapes import *


class Scene:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)