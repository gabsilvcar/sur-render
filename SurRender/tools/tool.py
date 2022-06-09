from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


class Tool:
    cursor = None

    def __init__(self, parent):
        self.parent = parent
        self.viewport = parent.centralWidget.viewport
        self.override_viewport_functions()
        
        if self.cursor is None:
            self.cursor = Qt.ArrowCursor
        self.viewport.setCursor(self.cursor)

    def override_viewport_functions(self):
        self.viewport.mousePressEvent = self.mousePressEvent
        self.viewport.mouseReleaseEvent = self.mouseReleaseEvent
        self.viewport.mouseMoveEvent = self.mouseMoveEvent
        self.viewport.wheelEvent = self.wheelEvent

    def mousePressEvent(self, event):
        pass 
    
    def mouseReleaseEvent(self, event):
        pass 
    
    def mouseMoveEvent(self, event):
        pass 
    
    def wheelEvent(self, event):
        pass 

    