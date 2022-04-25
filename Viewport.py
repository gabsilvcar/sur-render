from PyQt5.QtWidgets import QGraphicsView
from PyQt5 import QtGui, QtCore
import random
class Viewport(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        # pixmap = QtGui.QPixmap(100, 100)
        # pixmap.fill(QtCore.Qt.red)

        # self.pixmap_item = self.scene().addPixmap(pixmap)
        # # random position
        # self.pixmap_item.setPos(*random.sample(range(-100, 100), 2))
        # self.show()


    def mousePressEvent(self, event):
        # print(self.mapToScene(event.pos()))
        super(Viewport, self).mousePressEvent(event)