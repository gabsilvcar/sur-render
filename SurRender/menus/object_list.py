from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from SurRender.viewport import Viewport
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import Qt, QSize

class ObjectList(QTreeView):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.model = QStandardItemModel(0, 3, self)
        self.model.setHeaderData(0, Qt.Horizontal, 'NAME')
        self.model.setHeaderData(1, Qt.Horizontal, 'SHAPE')
        self.model.setHeaderData(2, Qt.Horizontal, 'COLOR')

        self.setModel(self.model)
        self.update()
            
    def update(self):
        for i, shape in enumerate(self.scene.shapes):
            name = QStandardItem(str(shape.name))
            types = QStandardItem(str(shape.__class__.__name__))
            color = QStandardItem()
            color.setBackground(QBrush(QColor(*shape.color)))

            self.model.setItem(i, 0, name)
            self.model.setItem(i, 1, types)
            self.model.setItem(i, 2, color)
