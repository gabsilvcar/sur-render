from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import * 

from SurRender.tools.hand_tool import HandTool
from SurRender.tools.selection_tool import SelectionTool
from SurRender.tools.zoom_tool import ZoomTool

class ToolsMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.selection_button = QPushButton('Selection')
        self.hand_button = QPushButton('Hand')
        self.zoom_button = QPushButton('Zoom')

        self.selection_button.pressed.connect(self.selection_callback)
        self.hand_button.pressed.connect(self.hand_callback)
        self.zoom_button.pressed.connect(self.zoom_callback)
                
        layout = QVBoxLayout()
        layout.addWidget(self.selection_button)
        layout.addWidget(self.hand_button)
        layout.addWidget(self.zoom_button)
        self.setLayout(layout)

    def hand_callback(self):
        self.parent.current_tool = HandTool(self.parent)
    
    def selection_callback(self):
        self.parent.current_tool = SelectionTool(self.parent)

    def zoom_callback(self):
        self.parent.current_tool = ZoomTool(self.parent)
