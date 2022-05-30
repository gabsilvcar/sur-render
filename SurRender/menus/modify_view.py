import numpy as np 

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from SurRender.constants import PIX_PER_MOVEMENT, ZOOM_FACTOR
from SurRender.scene import Scene
from SurRender.viewport import Viewport
from SurRender.shapes import Line

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
        self.viewport.zoom_in(ZOOM_FACTOR)

    def zoom_out_callback(self):
        self.viewport.zoom_out(ZOOM_FACTOR)


class MovementWidget(QWidget):
    def __init__(self, parent, viewport): 
        super().__init__()
        self.viewport = viewport
        
        self.up = QPushButton("Up")
        self.down = QPushButton("Down")
        self.left = QPushButton("Left")
        self.right = QPushButton("Right")
        
        self.up.clicked.connect(self.moveUp)
        self.down.clicked.connect(self.moveDown)
        self.left.clicked.connect(self.moveLeft)
        self.right.clicked.connect(self.moveRight) 
        
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

        self.move_up_action.setShortcuts([Qt.Key_Up, 'W'])
        self.move_down_action.setShortcuts([Qt.Key_Down, 'S'])
        self.move_left_action.setShortcuts([Qt.Key_Left, 'A'])
        self.move_right_action.setShortcuts([Qt.Key_Right, 'D'])

        self.move_up_action.triggered.connect(self.moveUp)
        self.move_down_action.triggered.connect(self.moveDown)
        self.move_left_action.triggered.connect(self.moveLeft)
        self.move_right_action.triggered.connect(self.moveRight)

        self.addAction(self.move_up_action)
        self.addAction(self.move_down_action)
        self.addAction(self.move_left_action)
        self.addAction(self.move_right_action)

    def moveUp(self):
        self.viewport.move_up(PIX_PER_MOVEMENT)

    def moveLeft(self):
        self.viewport.move_left(PIX_PER_MOVEMENT)

    def moveRight(self):
        self.viewport.move_right(PIX_PER_MOVEMENT)

    def moveDown(self):
        self.viewport.move_down(PIX_PER_MOVEMENT)
    

class RotationWidget(QWidget):
    def __init__(self, parent, viewport):
        super().__init__()
        self.viewport = viewport

        self.angle_box = QSpinBox()
        self.apply_button = QPushButton("Apply")

        self.angle_box.setRange(-360, 360)
        self.angle_box.setSingleStep(10)
        self.apply_button.clicked.connect(self.apply_callback)

        layout = QFormLayout()
        layout.addRow('Angle', self.angle_box)
        layout.addRow('', self.apply_button)
        self.setLayout(layout)
    
    def apply_callback(self):
        angle = self.angle_box.value()
        angle = np.radians(angle)
        self.viewport.rotate(angle)


class ClippingWidget(QWidget):
    def __init__(self, parent, viewport):
        super().__init__()
        self.viewport = viewport

        self.line_algorithm_buttons = [
            QRadioButton('Nothing'),
            QRadioButton('Cohen Sutherland'),
            QRadioButton('Liang Barsky'),
        ]
        self.line_algorithm_buttons[1].setChecked(True)

        self.line_group = QButtonGroup()
        self.line_group.addButton(self.line_algorithm_buttons[0], 0)
        self.line_group.addButton(self.line_algorithm_buttons[1], 1)
        self.line_group.addButton(self.line_algorithm_buttons[2], 2)
        self.line_group.buttonClicked.connect(self.line_algorithm_callback)

        layout = QVBoxLayout()

        for button in self.line_algorithm_buttons:
            layout.addWidget(button)

        self.setLayout(layout)

    def line_algorithm_callback(self):
        i = self.line_group.checkedId()
        Line.CLIPPING_ALGORITHM = i
        self.viewport.repaint()