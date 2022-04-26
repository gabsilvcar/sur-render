from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from Constants import Constants
from Viewport import Viewport
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtCore import Qt

class ObjectList(QTreeView):
    def __init__(self, scene):
        super().__init__()
                
        model = QStandardItemModel(0,3,self)
        model.setHeaderData(0,Qt.Horizontal,"NAME")
        model.setHeaderData(1,Qt.Horizontal,"SHAPE")
        model.setHeaderData(2,Qt.Horizontal,"COLOR")

        self.setModel(model)
        i = 0
        
        for shape in scene.shapes:
            parent1 = QStandardItem('{}'.format(shape.name))
            model.setItem(i,0,parent1)
            parent1 = QStandardItem('{}'.format(shape.__class__.__name__))
            model.setItem(i,1,parent1)
            parent1 = QStandardItem('{}'.format(shape.color.name()))
            model.setItem(i,2,parent1)
            i+= 1