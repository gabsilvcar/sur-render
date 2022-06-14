from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import Qt, QSize

import numpy as np

from surrender.vector import Vector
from surrender.viewport import Viewport


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
        try:
            x = self.x_line.text()
            y = self.y_line.text()

            x = float(x) if x else 0
            y = float(y) if y else 0

            i = self.object_list.selected_index()
            shape = self.viewport.scene.shapes[i]

            shape.move(Vector(x,y))
            self.viewport.update()

        except IndexError:
            pass 

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
        try:
            x = self.x_line.text()
            y = self.y_line.text()

            x = float(x) if x else 1
            y = float(y) if y else 1

            i = self.object_list.selected_index()
            shape = self.viewport.scene.shapes[i]

            shape.scale(Vector(x,y), shape.center())
            self.viewport.update()
        except IndexError:
            pass 


class RotateWidget(QWidget):
    def __init__(self, viewport, object_list): 
        super().__init__()

        self.viewport = viewport
        self.object_list = object_list

        self.combobox = QComboBox()

        self.x_angle_line = QLineEdit()
        self.y_angle_line = QLineEdit()
        self.z_angle_line = QLineEdit()

        self.around_x_line = QLineEdit()
        self.around_y_line = QLineEdit()
        self.apply_button = QPushButton('Apply')
        self.apply_button.pressed.connect(self.apply_callback)

        self.combobox.addItem('Rotate Around Origin')
        self.combobox.addItem('Rotate Around Center')
        self.combobox.addItem('Rotate Around Vector')
        self.combobox.activated.connect(self.box_callback)
        
        self.around_x_line.setReadOnly(True)
        self.around_y_line.setReadOnly(True)
        self.around_x_line.setPlaceholderText('Not avaliable')
        self.around_y_line.setPlaceholderText('Not avaliable')

        layout = QFormLayout()
        layout.addRow('', self.combobox)
        layout.addRow('Angle x', self.x_angle_line)
        layout.addRow('Angle y', self.y_angle_line)
        layout.addRow('Angle z', self.z_angle_line)
        layout.addRow('Around X', self.around_x_line)
        layout.addRow('Around Y', self.around_y_line)
        layout.addRow('', self.apply_button)
        self.setLayout(layout)

    def apply_callback(self):
        try:
            around_x = self.around_x_line.text()
            around_y = self.around_y_line.text()
            angle_x = self.x_angle_line.text()
            angle_y = self.y_angle_line.text()
            angle_z = self.z_angle_line.text()

            around_x = float(around_x) if around_x else 1
            around_y = float(around_y) if around_y else 1
            angle_x = np.radians(float(angle_x) if angle_x else 0)
            angle_y = np.radians(float(angle_y) if angle_y else 0)
            angle_z = np.radians(float(angle_z) if angle_z else 0)

            i = self.object_list.selected_index()
            shape = self.viewport.scene.shapes[i]
            txt = self.combobox.currentText()

            if txt == 'Rotate Around Origin':
                around = Vector(0,0)
            elif txt == 'Rotate Around Center':
                around = shape.center()
            elif txt == 'Rotate Around Vector':
                around = Vector(around_x, around_y)

            shape.rotate_x(angle_x, around)
            shape.rotate_y(angle_y, around)
            shape.rotate_z(angle_z, around)

            self.viewport.update()

        except IndexError:
            pass 

    
    def box_callback(self):
        ro = self.combobox.currentText() != 'Rotate Around Vector'

        self.around_x_line.setReadOnly(ro)
        self.around_y_line.setReadOnly(ro)

        if ro:
            self.around_x_line.setPlaceholderText('Not avaliable')
            self.around_y_line.setPlaceholderText('Not avaliable')
        else:
            self.around_x_line.setPlaceholderText('')
            self.around_y_line.setPlaceholderText('')