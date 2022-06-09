from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from SurRender.tools.tool import Tool
from SurRender import constants


class HandTool(Tool):    
    cursor = Qt.OpenHandCursor

    def mousePressEvent(self, event):
        self.start_pos = event.pos()
        self.viewport.setCursor(Qt.ClosedHandCursor)
    
    def mouseReleaseEvent(self, event):
        QApplication.restoreOverrideCursor()
        self.viewport.setCursor(Qt.OpenHandCursor)
        
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