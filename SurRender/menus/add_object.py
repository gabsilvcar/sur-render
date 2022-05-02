import sys
import re
from random import randint

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsView
import random
from SurRender.shapes import *
from PyQt5.QtWidgets import * 

from SurRender.primitives import Vector, Segment
  

class AddObject(QWidget):
    def __init__(self, viewport, objectview):
        super(AddObject, self).__init__()
        self.viewport = viewport
        self.objectview = objectview

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 300, 400)

        self.nameLineEdit = QLineEdit()
        self.createForm()
        self.button_ok = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_ok.accepted.connect(self.button_ok_callback)
        
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.formGroupBox)
        self.layout().addWidget(self.button_ok)

    def button_ok_callback(self):
        name = self.nameLineEdit.text()
        widget = self.tabs.currentWidget()
        color = tuple(randint(0, 255) for i in range(3))
        shape = None

        if isinstance(widget, PointWidget):
            pos = Vector(widget.x(), widget.y())
            shape = Point(name, pos, color)

        if isinstance(widget, LineWidget):
            s = Vector(widget.x0(), widget.y0())
            e = Vector(widget.x1(), widget.y1())
            shape = Line(name, s, e, color)

        if isinstance(widget, PolygonWidget):
            vectors = [Vector(p[0], p[1]) for p in widget.data()]
            shape = Polygon(name, vectors, color)

        if isinstance(widget, RectangleWidget):
            vectors = [
                Vector(widget.x0(), widget.y0()),
                Vector(widget.x1(), widget.y0()),
                Vector(widget.x1(), widget.y1()),
                Vector(widget.x0(), widget.y1()),
            ]
            shape = Polygon(name, vectors, color)

        if shape is not None:
            self.viewport.scene.add_shape(shape)
            self.objectview.update()
            self.viewport.repaint()
        
    # creat form method
    def createForm(self):
        self.formGroupBox = QGroupBox("Add Object")
  
        # creating a form layout
        layout = QFormLayout()
  
        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Name"), self.nameLineEdit)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(PointWidget(self), "Point")
        self.tabs.addTab(LineWidget(self), "Line")
        self.tabs.addTab(PolygonWidget(self), "Polygon")
        self.tabs.addTab(RectangleWidget(self),"Rectangle")
        # self.tabs.addTab(CircleWidget(self),"Circle")
        
        layout.addWidget(self.tabs)
        self.formGroupBox.setLayout(layout)
  
class PointWidget(QWidget):
    def __init__(self, parent): 
        super().__init__()
        self.x_line = QLineEdit()
        self.y_line = QLineEdit()

        self.random_button = QPushButton('Generate Random')
        self.random_button.pressed.connect(self.random_button_callback)

        self.setLayout(QFormLayout())
        self.layout().addRow('X', self.x_line)
        self.layout().addRow('Y', self.y_line)
        self.layout().addRow(self.random_button)
    
    def random_button_callback(self):
        lines = [
            self.x_line,
            self.y_line,
        ]

        for line in lines:
            n = randint(0, 400)
            line.setText(str(n))
    
    def x(self):
        txt = self.x_line.text()
        return int(txt) if txt else None
    
    def y(self):
        txt = self.y_line.text()
        return int(txt) if txt else None


class LineWidget(QWidget):
    def __init__(self, parent): 
        super().__init__()
        self.x0_line = QLineEdit()
        self.y0_line = QLineEdit()
        self.x1_line = QLineEdit()
        self.y1_line = QLineEdit()
        
        self.random_button = QPushButton('Generate Random')
        self.random_button.pressed.connect(self.random_button_callback)

        self.setLayout(QFormLayout())
        self.layout().addRow('X0', self.x0_line)
        self.layout().addRow('Y0', self.y0_line)
        self.layout().addRow('X1', self.x1_line)
        self.layout().addRow('Y1', self.y1_line)
        self.layout().addRow(self.random_button)
    
    def random_button_callback(self):
        lines = [
            self.x0_line,
            self.y0_line,
            self.x1_line,
            self.y1_line,
        ]

        for line in lines:
            n = randint(0, 400)
            line.setText(str(n))

    def x0(self):
        txt = self.x0_line.text()
        return int(txt) if txt else None

    def y0(self):
        txt = self.y0_line.text()
        return int(txt) if txt else None

    def x1(self):
        txt = self.x1_line.text()
        return int(txt) if txt else None

    def y1(self):
        txt = self.y1_line.text()
        return int(txt) if txt else None


class PolygonWidget(QWidget):
    def __init__(self, parent): 
        super().__init__()
        self.line = QLineEdit()

        self.random_button = QPushButton('Generate Random')
        self.random_button.pressed.connect(self.random_button_callback)

        self.setLayout(QFormLayout())
        self.layout().addRow('YourPoints', self.line)
        self.layout().addRow(self.random_button)

    def random_button_callback(self):
        n_points = randint(3, 10)
        points = [(randint(0,400), randint(0,400)) for i in range(n_points)]
        text =  ''.join(f'{i}, ' for i in points)
        self.line.setText(text)
        
    def data(self):
        get_digits = lambda x: tuple(int(i) for i in re.findall(r'\d+', x))
        between_brackets = re.findall(r'\((.*?)\)', self.line.text())
        return [get_digits(i) for i in between_brackets]


class RectangleWidget(QWidget):
    def __init__(self, parent): 
        super().__init__()
        self.x0_line = QLineEdit()
        self.y0_line = QLineEdit()
        self.x1_line = QLineEdit()
        self.y1_line = QLineEdit()

        self.random_button = QPushButton('Generate Random')
        self.random_button.pressed.connect(self.random_button_callback)

        self.setLayout(QFormLayout())
        self.layout().addRow('X0', self.x0_line)
        self.layout().addRow('Y0', self.y0_line)
        self.layout().addRow('X1', self.x1_line)
        self.layout().addRow('Y1', self.y1_line)
        self.layout().addRow(self.random_button)

    def random_button_callback(self):
        lines = [
            self.x0_line,
            self.y0_line,
            self.x1_line,
            self.y1_line,
        ]

        for line in lines:
            n = randint(0, 400)
            line.setText(str(n))

    def x0(self):
        txt = self.x0_line.text()
        return int(txt) if txt else None

    def y0(self):
        txt = self.y0_line.text()
        return int(txt) if txt else None

    def x1(self):
        txt = self.x1_line.text()
        return int(txt) if txt else None

    def y1(self):
        txt = self.y1_line.text()
        return int(txt) if txt else None

# class CircleWidget(QWidget):
#     def __init__(self, parent): 
#         super().__init__()
#         layout = QFormLayout()
#         layout.addRow(QLabel("X1"), parent.Cx1LineEdit)
#         layout.addRow(QLabel("Y1"), parent.Cy1LineEdit)
#         layout.addRow(QLabel("R"), parent.CRLineEdit)
#         self.setLayout(layout)

  
# main method
if __name__ == '__main__':
  
    # create pyqt5 app
    app = QApplication(sys.argv)
  
    # create the instance of our Window
    window = AddObject()
  
    # showing the window
    window.show()
  
    # start the app
    sys.exit(app.exec())