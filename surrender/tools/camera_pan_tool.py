import numpy as np
from PyQt5.QtCore import Qt

from surrender.tools.tool import Tool


class CameraPanTool(Tool):
    cursor = Qt.SizeAllCursor

    def mousePressEvent(self, event):
        self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.start_pos
        x = delta.x() / 100 * np.pi
        y = delta.y() / 100 * np.pi

        print(x, y)
        self.viewport.rotate(y, x, 0)

        # self.viewport.zoom_in(factor)
        self.start_pos = event.pos()    

    