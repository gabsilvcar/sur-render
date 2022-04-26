from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from src.Constants import Constants
from src.Viewport import Viewport
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtCore import Qt

class ObjectList(QTreeView):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.model = QStandardItemModel(0,3,self)
        self.model.setHeaderData(0,Qt.Horizontal,"NAME")
        self.model.setHeaderData(1,Qt.Horizontal,"SHAPE")
        self.model.setHeaderData(2,Qt.Horizontal,"COLOR")

        self.setModel(self.model)
        self.update()
            
    def update(self):
        i = 0
        for shape in self.scene.shapes:
            parent1 = QStandardItem('{}'.format(shape.name))
            self.model.setItem(i,0,parent1)
            parent1 = QStandardItem('{}'.format(shape.__class__.__name__))
            self.model.setItem(i,1,parent1)
            parent1 = QStandardItem('{}'.format(shape.color.name()))
            self.model.setItem(i,2,parent1)
            i+= 1