from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import Qt, QSize

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
        self.tabs.addTab(MoveWidget(self.viewport), 'Move')
        self.tabs.addTab(ScaleWidget(self.viewport), 'Scale')
        self.tabs.addTab(RotateWidget(self.viewport), 'Rotate')


class MoveWidget(QWidget):
    def __init__(self, viewport): 
        super().__init__()

        self.x_line = QLineEdit()
        self.y_line = QLineEdit()
        self.apply_button = QPushButton('Apply')

        layout = QFormLayout()
        layout.addRow('X', self.x_line)
        layout.addRow('Y', self.y_line)
        layout.addRow('', self.apply_button)
        self.setLayout(layout)

    def apply_callback(self):
        pass

    def x(self):
        txt = self.x_line.text()
        return float(txt) if txt else None
    
    def y(self):
        txt = self.y_line.text()
        return float(txt) if txt else None

class ScaleWidget(QWidget):
    def __init__(self, viewport): 
        super().__init__()

        self.x_line = QLineEdit()
        self.y_line = QLineEdit()
        self.apply_button = QPushButton('Apply')

        layout = QFormLayout()
        layout.addRow('X', self.x_line)
        layout.addRow('Y', self.y_line)
        layout.addRow('', self.apply_button)
        self.setLayout(layout)

    def x(self):
        txt = self.x_line.text()
        return float(txt) if txt else None
    
    def y(self):
        txt = self.y_line.text()
        return float(txt) if txt else None

class RotateWidget(QWidget):
    def __init__(self, viewport): 
        super().__init__()

        self.combobox = QComboBox()
        self.angle_line = QLineEdit()
        self.x_line = QLineEdit()
        self.y_line = QLineEdit()
        self.apply_button = QPushButton('Apply')

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

    def angle(self):
        txt = self.angle_line.text()
        return float(txt) if txt else None
    
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