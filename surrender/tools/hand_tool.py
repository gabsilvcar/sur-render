from PyQt5.QtCore import Qt
from surrender.tools.tool import Tool
from surrender.vector import Vector
from surrender import constants


class HandTool(Tool):
    cursor = Qt.OpenHandCursor

    def mousePressEvent(self, event):
        self.start_pos = event.pos()
        self.viewport.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.viewport.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        delta = self.start_pos - event.pos()
        self.start_pos = event.pos()
        v = Vector(delta.x(), -delta.y())
        self.viewport.move(v)

    def wheelEvent(self, event):
        x = event.angleDelta().y() / 120
        if x > 0:
            self.viewport.zoom(constants.ZOOM_FACTOR)
        elif x < 0:
            self.viewport.zoom(1 / constants.ZOOM_FACTOR)
