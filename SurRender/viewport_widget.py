from ast import Constant
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from SurRender import constants
from SurRender.scene import Scene
from SurRender.viewport import Viewport

class ViewportWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        self.viewport = Viewport()
        self.viewport.show()
        self.setTitle("Viewport")
        self.setFlat(True)
        self.init_ui()

    def init_ui(self):
        self.__center()
        self.__createWidgets()
        # self.__createMenuBars()
        self.show()

    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __createWidgets(self):
        layout = QGridLayout()

        # layout.addWidget(QLabel('<h3>Viewport</h3>', parent=self), 0, 0)

        layout.addWidget(self.viewport, 1, 0)
  
        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.start_pos = event.pos()
        
    def mouseMoveEvent(self, event):
        delta = self.start_pos - event.pos() 
        self.start_pos = event.pos()
        self.viewport.move_xy(delta.x(), -delta.y())
        
    def wheelEvent(self,event):
        x = event.angleDelta().y() / 120
        if x > 0:
            self.viewport.zoom_in(constants.ZOOM_FACTOR)
        elif x < 0:
            self.viewport.zoom_out(constants.ZOOM_FACTOR)