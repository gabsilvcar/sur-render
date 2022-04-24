from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from Constants import Constants
from Scene import Scene
from Viewport import Viewport

class GUIPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.__center()
        self.__createWidgets()
        # self.__createMenuBars()
        self.show()

    def __center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def __createWidgets(self):
        layout = QGridLayout()

        layout.addWidget(QPushButton('Button (0, 0)'), 0, 0)
        layout.addWidget(QLabel('<h3>Viewport</h>', parent=self), 0, 1)

        layout.addWidget(Viewport(Scene()), 1, 1, 2, 2);
        # layout.addWidget(QPushButton('Button (0, 2)'), 0, 2);
        # layout.addWidget(QPushButton('Button (1, 1)'), 1, 1);
        # layout.addWidget(QPushButton('Button (1, 2)'), 1, 2);
        layout.addWidget(QPushButton('Button (1, 0)'), 1, 0)
  
        # layout.addWidget(QPushButton('Button (2, 0)'), 2, 0)
        # layout.addWidget(QPushButton('Button (2, 1) + 2 Columns Span'), 2, 1, 1, 2)

        self.setLayout(layout)

    # def __createMenuBars(self):
    #     menuBar = self.menuBar()
    #     # Creating menus using a QMenu object
    #     fileMenu = QMenu("&File", self)
    #     menuBar.addMenu(fileMenu)
    #     # Creating menus using a title
    #     editMenu = menuBar.addMenu("&Edit")
    #     helpMenu = menuBar.addMenu("&Help")
