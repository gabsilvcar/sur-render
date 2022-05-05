from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import Qt, QSize

import numpy as np

from SurRender.vector import Vector
from SurRender.viewport import Viewport


class ModifyObject(QWidget):
    def __init__(self, viewport, object_list):
        super().__init__()

        self.viewport = viewport
        self.object_list = object_list

        self.create_tabs()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(MoveWidget(self.viewport, self.object_list), 'Move')
        self.tabs.addTab(ScaleWidget(self.viewport, self.object_list), 'Scale')
        self.tabs.addTab(RotateWidget(self.viewport, self.object_list), 'Rotate')


class MoveWidget(QWidget):
    def __init__(self, viewport, object_list): 
        super().__init__()

        self.viewport = viewport
        self.object_list = object_list

        self.x_line = QLineEdit()
        self.y_line = QLineEdit()
        self.apply_button = QPushButton('Apply')
        self.apply_button.pressed.connect(self.apply_callback)


        layout = QFormLayout()
        layout.addRow('X', self.x_line)
        layout.addRow('Y', self.y_line)
        layout.addRow('', self.apply_button)
        self.setLayout(layout)

    def apply_callback(self):
        x = self.x_line.text()
        y = self.y_line.text()

        x = float(x) if x else 0
        y = float(y) if y else 0

        i = self.object_list.selected_index()
        shape = self.viewport.scene.shapes[i]

        shape.move(Vector(x,y))
        self.viewport.update()


class ScaleWidget(QWidget):
    def __init__(self, viewport, object_list): 
        super().__init__()

        self.viewport = viewport
        self.object_list = object_list

        self.x_line = QLineEdit()
        self.y_line = QLineEdit()
        self.apply_button = QPushButton('Apply')
        self.apply_button.pressed.connect(self.apply_callback)

        layout = QFormLayout()
        layout.addRow('X', self.x_line)
        layout.addRow('Y', self.y_line)
        layout.addRow('', self.apply_button)
        self.setLayout(layout)
    
    def apply_callback(self):
        x = self.x_line.text()
        y = self.y_line.text()

        x = float(x) if x else 1
        y = float(y) if y else 1

        i = self.object_list.selected_index()
        shape = self.viewport.scene.shapes[i]

        shape.scale(Vector(x,y), shape.center())
        self.viewport.update()


class RotateWidget(QWidget):
    def __init__(self, viewport, object_list): 
        super().__init__()

        self.viewport = viewport
        self.object_list = object_list

        self.combobox = QComboBox()
        self.angle_line = QLineEdit()
        self.x_line = QLineEdit()
        self.y_line = QLineEdit()
        self.apply_button = QPushButton('Apply')
        self.apply_button.pressed.connect(self.apply_callback)

        self.combobox.addItem('Rotate Around Origin')
        self.combobox.addItem('Rotate Around Center')
        self.combobox.addItem('Rotate Around Vector')
        self.combobox.activated.connect(self.box_callback)
        
        self.x_line.setReadOnly(True)
        self.y_line.setReadOnly(True)
        self.x_line.setPlaceholderText('Not avaliable')
        self.y_line.setPlaceholderText('Not avaliable')

        layout = QFormLayout()
        layout.addRow('', self.combobox)
        layout.addRow('Angle', self.angle_line)
        layout.addRow('X', self.x_line)
        layout.addRow('Y', self.y_line)
        layout.addRow('', self.apply_button)
        self.setLayout(layout)

    def apply_callback(self):
        x = self.x_line.text()
        y = self.y_line.text()
        a = self.angle_line.text()
        x = float(x) if x else 1
        y = float(y) if y else 1
        a = float(a) if a else 0
        a = np.radians(a)

        i = self.object_list.selected_index()
        shape = self.viewport.scene.shapes[i]
        txt = self.combobox.currentText()

        if txt == 'Rotate Around Origin':
            around = Vector(0,0)
        elif txt == 'Rotate Around Center':
            around = shape.center()
        elif txt == 'Rotate Around Vector':
            around = Vector(x,y)

        shape.rotate(a, around)
        self.viewport.update()

    
    def box_callback(self):
        ro = self.combobox.currentText() != 'Rotate Around Vector'
        self.x_line.setReadOnly(ro)
        self.y_line.setReadOnly(ro)

        if ro:
            self.x_line.setPlaceholderText('Not avaliable')
            self.y_line.setPlaceholderText('Not avaliable')
        else:
            self.x_line.setPlaceholderText('')
            self.y_line.setPlaceholderText('')