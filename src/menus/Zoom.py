from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from src.Constants import Constants
from src.Scene import Scene
from src.Viewport import Viewport

class Zoom(QWidget):

    def __init__(self, parent, viewportwidget): 
        super().__init__()
        self.viewportwidget = viewportwidget
        self.zoomIn = QPushButton("+")
        self.zoomOut = QPushButton("-")
        self.zoomIn.clicked.connect(self.zoomMore)
        self.zoomOut.clicked.connect(self.zoomLess)
        
        layout = QGridLayout()
        layout.addWidget(self.zoomOut, 0, 1)
        layout.addWidget(QLabel('<center><h6>Zoom</h6><\center>', parent), 0, 2)
        layout.addWidget(self.zoomIn, 0, 3)

        self.setLayout(layout)
        
    def zoomMore(self):
        self.viewportwidget.viewport.zoom_in(Constants.ZOOM_IN_FACTOR)

        # self.viewportwidget.viewport.resize(Constants.ZOOM_IN_FACTOR * self.viewportwidget.viewport.size())

    def zoomLess(self):
        self.viewportwidget.viewport.zoom_out(Constants.ZOOM_IN_FACTOR)
        # self.viewportwidget.viewport.resize(Constants.ZOOM_OUT_FACTOR * self.viewportwidget.viewport.size())
