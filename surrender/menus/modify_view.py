import numpy as np 

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from surrender.constants import PIX_PER_MOVEMENT, ZOOM_FACTOR
from surrender.scene import Scene
from surrender.viewport import Viewport
from surrender.shapes import *
from surrender.vector import Vector
from surrender.shapes.generic_curve import GenericCurve


class ModifyView(QWidget):
    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport
        self.create_tabs()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(MovementWidget(self, self.viewport), 'Move')
        self.tabs.addTab(ZoomWidget(self, self.viewport), 'Scale')
        self.tabs.addTab(RotationWidget(self, self.viewport), 'Rotate')
        self.tabs.addTab(ClippingWidget(self, self.viewport), 'Clipping')


class ZoomWidget(QWidget):
    def __init__(self, parent, viewport): 
        super().__init__()
        self.viewport = viewport
        self.zoom_in = QPushButton("+")
        self.zoom_out = QPushButton("-")
        self.zoom_in.clicked.connect(self.zoom_in_callback)
        self.zoom_out.clicked.connect(self.zoom_out_callback)
        
        layout = QGridLayout()
        layout.addWidget(self.zoom_out, 0, 1)
        layout.addWidget(QLabel('<center><h6>Zoom</h6><\center>'), 0, 2)
        layout.addWidget(self.zoom_in, 0, 3)

        self.setLayout(layout)
        self.add_actions()

    def add_actions(self):
        self.zoom_in_action = QAction('zoom in')
        self.zoom_out_action = QAction('zoom out')

        self.zoom_in_action.setShortcut('+')
        self.zoom_out_action.setShortcut('-')

        self.zoom_in_action.triggered.connect(self.zoom_in_callback)
        self.zoom_out_action.triggered.connect(self.zoom_out_callback)

        self.addAction(self.zoom_in_action)
        self.addAction(self.zoom_out_action)
        
    def zoom_in_callback(self):
        self.viewport.zoom(ZOOM_FACTOR)

    def zoom_out_callback(self):
        self.viewport.zoom(1/ZOOM_FACTOR)


class MovementWidget(QWidget):
    def __init__(self, parent, viewport): 
        super().__init__()
        self.viewport = viewport
        
        self.up = QPushButton("Up")
        self.down = QPushButton("Down")
        self.left = QPushButton("Left")
        self.right = QPushButton("Right")
        
        self.up.clicked.connect(self.move_up_callback)
        self.down.clicked.connect(self.move_down_callback)
        self.left.clicked.connect(self.move_left_callback)
        self.right.clicked.connect(self.move_right_callback) 
        
        layout = QGridLayout()
        
        layout.addWidget(self.up, 0, 2)
        layout.addWidget(self.left, 1, 1)
        layout.addWidget(QLabel('<center><h6>Move</h6><\center>'), 1, 2)
        layout.addWidget(self.right, 1, 3)
        layout.addWidget(self.down, 2, 2)

        self.setLayout(layout)
        self.add_actions()

    def add_actions(self):
        self.move_up_action = QAction('Up')
        self.move_down_action = QAction('Down')
        self.move_left_action = QAction('Left')
        self.move_right_action = QAction('Right')
        self.move_front_action = QAction('Front')
        self.move_back_action = QAction('Back')

        self.move_front_action.setShortcuts([Qt.Key_Up, 'W'])
        self.move_back_action.setShortcuts([Qt.Key_Down, 'S'])
        self.move_left_action.setShortcuts([Qt.Key_Left, 'A'])
        self.move_right_action.setShortcuts([Qt.Key_Right, 'D'])

        self.move_up_action.triggered.connect(self.move_up_callback)
        self.move_down_action.triggered.connect(self.move_down_callback)
        self.move_left_action.triggered.connect(self.move_left_callback)
        self.move_right_action.triggered.connect(self.move_right_callback)
        self.move_front_action.triggered.connect(self.move_front_callback)
        self.move_back_action.triggered.connect(self.move_back_callback)

        self.addAction(self.move_up_action)
        self.addAction(self.move_down_action)
        self.addAction(self.move_left_action)
        self.addAction(self.move_right_action)
        self.addAction(self.move_front_action)
        self.addAction(self.move_back_action)

    def move_up_callback(self):
        v = Vector(0, 1, 0) * PIX_PER_MOVEMENT
        self.viewport.move(v)

    def move_down_callback(self):
        v = Vector(0, -1, 0) * PIX_PER_MOVEMENT
        self.viewport.move(v)

    def move_left_callback(self):
        v = Vector(-1, 0, 0) * PIX_PER_MOVEMENT
        self.viewport.move(v)

    def move_right_callback(self):
        v = Vector(1, 0, 0) * PIX_PER_MOVEMENT
        self.viewport.move(v)
    
    def move_front_callback(self):
        v = Vector(0, 0, 1) * PIX_PER_MOVEMENT
        self.viewport.move(v)

    def move_back_callback(self):
        v = Vector(0, 0, -1) * PIX_PER_MOVEMENT
        self.viewport.move(v)

class RotationWidget(QWidget):
    def __init__(self, parent, viewport):
        super().__init__()
        self.viewport = viewport

        self.x_angle_box = QSpinBox()
        self.y_angle_box = QSpinBox()
        self.z_angle_box = QSpinBox()
        self.apply_button = QPushButton("Apply")

        self.x_angle_box.setRange(-360, 360)
        self.y_angle_box.setRange(-360, 360)
        self.z_angle_box.setRange(-360, 360)

        self.x_angle_box.setSingleStep(10)
        self.y_angle_box.setSingleStep(10)
        self.z_angle_box.setSingleStep(10)

        self.apply_button.clicked.connect(self.apply_callback)

        layout = QFormLayout()
        layout.addRow('Angle X', self.x_angle_box)
        layout.addRow('Angle Y', self.y_angle_box)
        layout.addRow('Angle Z', self.z_angle_box)
        layout.addRow('', self.apply_button)
        self.setLayout(layout)
    
    def apply_callback(self):
        x = np.radians(self.x_angle_box.value())
        y = np.radians(self.y_angle_box.value())
        z = np.radians(self.z_angle_box.value())
        delta = Vector(x, y, z)
        self.viewport.rotate(delta)


class ClippingWidget(QWidget):
    def __init__(self, parent, viewport):
        super().__init__()
        self.viewport = viewport

        self.point_algorithm_buttons = [
            QRadioButton('Nothing'),
            QRadioButton('Trivial'),
        ]

        self.line_algorithm_buttons = [
            QRadioButton('Nothing'),
            QRadioButton('Cohen Sutherland'),
            QRadioButton('Liang Barsky'),
        ]

        self.polygon_algorithm_buttons = [
            QRadioButton('Nothing'),
            QRadioButton('Sutherland Hodgeman'),
        ]

        self.curve_algorithm_buttons = [
            QRadioButton('Nothing'),
            QRadioButton('Sutherland Hodgeman'),
        ]

        self.point_algorithm_buttons[1].setChecked(True)
        self.line_algorithm_buttons[1].setChecked(True)
        self.polygon_algorithm_buttons[1].setChecked(True)
        self.curve_algorithm_buttons[1].setChecked(True)

        self.point_group = QButtonGroup()
        self.line_group = QButtonGroup()
        self.polygon_group = QButtonGroup()
        self.curve_group = QButtonGroup()

        for i, b in enumerate(self.point_algorithm_buttons):
            self.point_group.addButton(b, i)

        for i, b in enumerate(self.line_algorithm_buttons):
            self.line_group.addButton(b, i)

        for i, b in enumerate(self.polygon_algorithm_buttons):
            self.polygon_group.addButton(b, i)

        for i, b in enumerate(self.curve_algorithm_buttons):
            self.curve_group.addButton(b, i)

        self.point_group.buttonClicked.connect(self.point_algorithm_callback)
        self.line_group.buttonClicked.connect(self.line_algorithm_callback)
        self.polygon_group.buttonClicked.connect(self.polygon_algorithm_callback)
        self.curve_group.buttonClicked.connect(self.curve_algorithm_callback)

        layout = QVBoxLayout()

        layout.addWidget(QLabel('Point clipping algorithm'))
        for button in self.point_algorithm_buttons:
            layout.addWidget(button)

        layout.addWidget(QLabel('Line clipping algorithm'))
        for button in self.line_algorithm_buttons:
            layout.addWidget(button)

        layout.addWidget(QLabel('Polygon clipping algorithm'))
        for button in self.polygon_algorithm_buttons:
            layout.addWidget(button)

        layout.addWidget(QLabel('Curve clipping algorithm'))
        for button in self.curve_algorithm_buttons:
            layout.addWidget(button)

        self.setLayout(layout)

    def point_algorithm_callback(self):
        i = self.point_group.checkedId()
        Point.CLIPPING_ALGORITHM = i
        self.viewport.repaint()

    def line_algorithm_callback(self):
        i = self.line_group.checkedId()
        Line.CLIPPING_ALGORITHM = i
        self.viewport.repaint()
    
    def polygon_algorithm_callback(self):
        i = self.polygon_group.checkedId()
        Polygon.CLIPPING_ALGORITHM = i
        self.viewport.repaint()

    def curve_algorithm_callback(self):
        i = self.curve_group.checkedId()
        GenericCurve.CLIPPING_ALGORITHM = i
        self.viewport.repaint()