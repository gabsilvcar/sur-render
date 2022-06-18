from PyQt5.QtCore import Qt
from surrender.tools.tool import Tool


class ZoomTool(Tool):
    cursor = Qt.CrossCursor

    def mousePressEvent(self, event):
        self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.start_pos
        factor = 1 + delta.x() / 100
        self.viewport.zoom_in(factor)
        self.start_pos = event.pos()    
    