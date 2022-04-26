import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from src.Shapes import *
class Scene():
    def __init__(self):
        self.shapes = []
        # for _ in range(20):
        #     pos1 = QtCore.QPoint(*random.choices(range(500), k=2))
        #     pos2 = QtCore.QPoint(*random.choices(range(500), k=2))
        #     length = random.randrange(100)
        #     color = QtGui.QColor(*random.choices(range(256), k=3))
        #     self.shapes.append(Rectangle("teste", pos1, pos2, color))