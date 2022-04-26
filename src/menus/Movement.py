from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from src.Constants import Constants
from src.Scene import Scene
from src.Viewport import Viewport

class Movement(QWidget):
    def __init__(self, parent, viewportwidget): 
        super().__init__()
        self.viewportwidget = viewportwidget
        
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
        
    def moveUp(self):
        self.viewportwidget.viewport.translationY += Constants.PIX_PER_MOVEMENT
        self.viewportwidget.viewport.repaint()
    def moveLeft(self):
        self.viewportwidget.viewport.translationX += Constants.PIX_PER_MOVEMENT
        self.viewportwidget.viewport.repaint()
    def moveRight(self):
        self.viewportwidget.viewport.translationX -= Constants.PIX_PER_MOVEMENT
        self.viewportwidget.viewport.repaint()
    def moveDown(self):
        self.viewportwidget.viewport.translationY -= Constants.PIX_PER_MOVEMENT
        self.viewportwidget.viewport.repaint()
