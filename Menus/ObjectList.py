from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from Constants import Constants
from Scene import Scene
from Viewport import Viewport
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtCore import Qt

class ObjectList(QTreeView):
    def __init__(self):
        super().__init__()
        features = {('POLYGON', 'SLPR'): [('ONE WAY', ['NO', 'YES'], 'List', 3), ('CLASS', ['INTERSTATE', 'PRIMARY', 'RESIDENTIAL', 'SECONDARY', 'SERVICE', 'STATE HWY', 'TERTIARY', 'TRACK', 'US HWY'], 'List', 11)], ('POINT', 'CALC FLD'): [('NAME', [], 'TEXT', '50'), ('SURFACE', ['BLACK TOP', 'BRICK', 'CALICHE', 'CALICHE AND GRAVEL', 'CINDER', 'CONCRETE', 'DIRT', 'GRASS', 'GRAVEL', 'LIMESTONE', 'OILED', 'PAVED ASPHALT', 'ROCK', 'SAND', 'SAND AND GRAVEL', 'SCORIA', 'SHELL', 'SHELL & OIL', 'SLAG'], 'List', 18)], ('POINT', 'RKDH'): [('TYPE', ['COUNTY', 'DO NOT USE', 'ENGINEERED', 'IMPROVED', 'PRIMITIVE', 'TEMPLATE', 'TEMPORARY ACCESS'], 'List', 16)]}
        
        model = QStandardItemModel(0,3,self)
        model.setHeaderData(0,Qt.Horizontal,"CODE")
        model.setHeaderData(1,Qt.Horizontal,"DATA TYPE")
        model.setHeaderData(2,Qt.Horizontal,"LENGTH")
        self.setModel(model)
        i = 0
        for k,featuretype in features.items():
                    parent1 = QStandardItem('{}'.format(k[1]))
                    for item in featuretype:
                        child = QStandardItem(item[0])
                        if len(item[1])>0:
                            for listitem in item[1]:
                                gchild=QStandardItem(listitem)
                                child.appendRow(gchild)
                        parent1.appendRow(child)
                    model.setItem(i,0,parent1)
                    self.setFirstColumnSpanned(i,self.rootIndex(),True)
                    i+=1