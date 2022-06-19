import numpy as np
from PyQt5.QtCore import Qt
from surrender.tools.tool import Tool
from surrender.vector import Vector


class CameraPanTool(Tool):
    cursor = Qt.SizeAllCursor

    def mousePressEvent(self, event):
        self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.start_pos
        x = delta.x() / 100 * np.pi
        y = delta.y() / 100 * np.pi
        delta = Vector(x, y, 0)
        self.viewport.rotate(delta)
        self.start_pos = event.pos()    
