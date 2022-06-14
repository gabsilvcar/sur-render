from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import * 

from surrender.tools import *


class ToolsMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.selection_button = QPushButton('Selection')
        self.hand_button = QPushButton('Hand')
        self.zoom_button = QPushButton('Zoom')
        self.camera_pan_button = QPushButton('Pan')

        self.selection_button.pressed.connect(self.selection_callback)
        self.hand_button.pressed.connect(self.hand_callback)
        self.zoom_button.pressed.connect(self.zoom_callback)
        self.camera_pan_button.pressed.connect(self.camera_pan_callback)
                
        layout = QVBoxLayout()
        layout.addWidget(self.selection_button)
        layout.addWidget(self.hand_button)
        layout.addWidget(self.zoom_button)
        layout.addWidget(self.camera_pan_button)
        self.setLayout(layout)

    def hand_callback(self):
        self.parent.current_tool = HandTool(self.parent)
    
    def selection_callback(self):
        self.parent.current_tool = SelectionTool(self.parent)

    def zoom_callback(self):
        self.parent.current_tool = ZoomTool(self.parent)

    def camera_pan_callback(self):
        self.parent.current_tool = CameraPanTool(self.parent)

