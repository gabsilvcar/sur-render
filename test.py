import sys, random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class Shape():
    def __init__(self, length, position, color, parent=None):
        self.color = color
        self.position = position
        self.length = length

    def paint(self, painter):
        pass

class Circle(Shape):
    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
        x, y = self.position.x(), self.position.y()
        painter.drawEllipse(x, y, self.length, self.length)
        painter.restore()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for shape in self.shapes:
            shape.paint(painter)
            
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    for _ in range(20):
        pos = QtCore.QPoint(*random.choices(range(500), k=2))
        length = random.randrange(100)
        color = QtGui.QColor(*random.choices(range(256), k=3))
        window.shapes.append(Circle(length, pos, color))
    window.show()
    sys.exit(App.exec())