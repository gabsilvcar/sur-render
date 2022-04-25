from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from Constants import Constants
from Scene import Scene
from Viewport import Viewport

class Zoom(QWidget):
    def __init__(self, parent): 
        super().__init__()
        self.zoomIn = QPushButton("+")
        self.zoomOut = QPushButton("-")

        layout = QGridLayout()
        layout.addWidget(self.zoomOut, 0, 1)
        layout.addWidget(QLabel('<center><h6>Zoom</h6><\center>', parent), 0, 2)
        layout.addWidget(self.zoomIn, 0, 3)

        self.setLayout(layout)
        

        
        """Create the buttons."""
        # self.buttons = {}
        # buttonsLayout = QGridLayout()
        # # Button text | position on the QGridLayout
        # buttons = {'7': (0, 0),
        #            '8': (0, 1),
        #            '9': (0, 2),
        #            '/': (0, 3),
        #            'C': (0, 4),
        #            '4': (1, 0),
        #            '5': (1, 1),
        #            '6': (1, 2),
        #            '*': (1, 3),
        #            '(': (1, 4),
        #            '1': (2, 0),
        #            '2': (2, 1),
        #            '3': (2, 2),
        #            '-': (2, 3),
        #            ')': (2, 4),
        #            '0': (3, 0),
        #            '00': (3, 1),
        #            '.': (3, 2),
        #            '+': (3, 3),
        #            '=': (3, 4),
        #           }
        # # Create the buttons and add them to the grid layout
        # for btnText, pos in buttons.items():
        #     self.buttons[btnText] = QPushButton(btnText)
        #     self.buttons[btnText].setFixedSize(40, 40)
        #     buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # # Add buttonsLayout to the general layout
        # self.setLayout(buttonsLayout)
    