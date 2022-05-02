from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from src.Constants import PIX_PER_MOVEMENT
from src.Scene import Scene
from src.Viewport import Viewport

class Movement(QWidget):
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
        layout.addWidget(QLabel('<center><h6>Move</h6><\center>', parent), 1, 2)
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
        