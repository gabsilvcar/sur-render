from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from src.Constants import ZOOM_IN_FACTOR
from src.Scene import Scene
from src.Viewport import Viewport

class Zoom(QWidget):
    def __init__(self, parent, viewport): 
        super().__init__()
        self.viewport = viewport
        self.zoom_in = QPushButton("+")
        self.zoom_out = QPushButton("-")
        self.zoom_in.clicked.connect(self.zoom_in_callback)
        self.zoom_out.clicked.connect(self.zoom_out_callback)
        
        layout = QGridLayout()
        layout.addWidget(self.zoom_out, 0, 1)
        layout.addWidget(QLabel('<center><h6>Zoom</h6><\center>', parent), 0, 2)
        layout.addWidget(self.zoom_in, 0, 3)

        self.setLayout(layout)
        
    def zoom_in_callback(self):
        self.viewport.zoom_in(ZOOM_IN_FACTOR)

    def zoom_out_callback(self):
        self.viewport.zoom_out(ZOOM_IN_FACTOR)