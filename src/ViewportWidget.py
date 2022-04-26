from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from src.Constants import Constants
from src.Scene import Scene
from src.Viewport import Viewport

class ViewportWidget(QGroupBox):

    def __init__(self):
        super().__init__()
        self.scene = Scene()
        self.viewport = Viewport(self.scene)
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

