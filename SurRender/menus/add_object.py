import sys
import re
from random import randint

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import * 

from SurRender.shapes import *
from SurRender.vector import Vector
  

class AddObject(QWidget):
    def __init__(self, viewport, objectview):
        super(AddObject, self).__init__()

        self.viewport = viewport
        self.objectview = objectview
        self.create_tabs()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(PointWidget(self.viewport, self.objectview), "Point")
        self.tabs.addTab(LineWidget(self.viewport, self.objectview), "Line")
        self.tabs.addTab(PolygonWidget(self.viewport, self.objectview), "Polygon")
        self.tabs.addTab(BezierWidget(self.viewport, self.objectview), "Bezier")
        self.tabs.addTab(RectangleWidget(self.viewport, self.objectview), "Rectangle")

  
class GenericShapeWidget(QWidget):
    def __init__(self, viewport, object_list):
        super().__init__()

        self.viewport = viewport
        self.object_list = object_list

        self.name_line = QLineEdit()
        self.random_button = QPushButton('Generate Random')
        self.apply_button = QPushButton('Apply')
        self.color_button = QPushButton('')
        self.color = (255,0,0)

        self.paint_button(self.color_button, self.color)
        self.color_button.pressed.connect(self.color_callback)
        self.random_button.pressed.connect(self.random_callback)
        self.apply_button.pressed.connect(self.apply_callback)

    def add_shape(self, shape):
        self.viewport.scene.add_shape(shape)
        self.object_list.update()
        self.viewport.repaint()

    def color_callback(self):
        c = QColorDialog.getColor()
        self.color = (c.red(), c.green(), c.blue())
        self.paint_button(self.color_button, self.color)

    def paint_button(self, button, color):
        button.setStyleSheet(f'background-color: rgb({color[0]},{color[1]},{color[2]})')

    def random_callback(self):
        pass 
    
    def apply_callback(self):
        pass 


class PointWidget(GenericShapeWidget):
    def __init__(self, viewport, object_list): 
        super().__init__(viewport, object_list)

        self.x_line = QLineEdit()
        self.y_line = QLineEdit()

        layout = QFormLayout()
        layout.addRow('Name', self.name_line)
        layout.addRow('X', self.x_line)
        layout.addRow('Y', self.y_line)
        layout.addRow('Color', self.color_button)
        layout.addRow(self.random_button)
        layout.addRow(self.apply_button)
        self.setLayout(layout)
    
    def random_callback(self):
        self.color = [randint(0,255) for _ in range(3)]
        self.paint_button(self.color_button, self.color)

        lines = [self.x_line, self.y_line]
        for line in lines:
            n = randint(0, 400)
            line.setText(str(n))

    def apply_callback(self):
        try:
            name = self.name_line.text()
            x = int(self.x_line.text())
            y = int(self.y_line.text())

            pos = Vector(x, y)
            shape = Point(name, pos, self.color)
            self.add_shape(shape)
        except ValueError:
            pass

class LineWidget(GenericShapeWidget):
    def __init__(self, viewport, object_list): 
        super().__init__(viewport, object_list)

        self.x0_line = QLineEdit()
        self.y0_line = QLineEdit()
        self.x1_line = QLineEdit()
        self.y1_line = QLineEdit()

        layout = QFormLayout()
        layout.addRow('Name', self.name_line)
        layout.addRow('X0', self.x0_line)
        layout.addRow('Y0', self.y0_line)
        layout.addRow('X1', self.x1_line)
        layout.addRow('Y1', self.y1_line)
        layout.addRow('Color', self.color_button)
        layout.addRow(self.random_button)
        layout.addRow(self.apply_button)
        self.setLayout(layout)
    
    def random_callback(self):
        self.color = [randint(0,255) for _ in range(3)]
        self.paint_button(self.color_button, self.color)

        lines = [
            self.x0_line,
            self.y0_line,
            self.x1_line,
            self.y1_line,
        ]

        for line in lines:
            n = randint(0, 400)
            line.setText(str(n))

    def apply_callback(self):
        try:
            name = self.name_line.text()
            x0 = int(self.x0_line.text())
            y0 = int(self.y0_line.text())
            x1 = int(self.x1_line.text())
            y1 = int(self.y1_line.text())

            s = Vector(x0, y0)
            e = Vector(x1, y1)
            shape = Line(name, s, e, self.color)
            self.add_shape(shape)
        except ValueError:
            pass


class PolygonWidget(GenericShapeWidget):
    def __init__(self, viewport, object_list): 
        super().__init__(viewport, object_list)

        self.points_line = QLineEdit()
        self.fill_box = QCheckBox()

        self.type_buttons = [
            QRadioButton('Open'),
            QRadioButton('Closed'),
            QRadioButton('Filled'),
        ]
        self.type_buttons[0].setChecked(True)
        self.type_group = QButtonGroup()

        for i, b in enumerate(self.type_buttons):
            self.type_group.addButton(b, i)

        layout = QFormLayout()
        layout.addRow('Name', self.name_line)
        layout.addRow('Your Points', self.points_line)
        layout.addRow('Color', self.color_button)
        layout.addRow('', self.type_buttons[0])
        layout.addRow('', self.type_buttons[1])
        layout.addRow('', self.type_buttons[2])
        layout.addRow(self.random_button)
        layout.addRow(self.apply_button)
        self.setLayout(layout)

    def random_callback(self):
        self.color = [randint(0,255) for _ in range(3)]
        self.paint_button(self.color_button, self.color)

        n_points = randint(3, 8)
        points = [(randint(0,400), randint(0,400)) for i in range(n_points)]
        text =  ''.join(f'{i}, ' for i in points)
        self.points_line.setText(text)
    
    def apply_callback(self):
        try:
            get_digits = lambda x: tuple(int(i) for i in re.findall(r'-?\d+', x))
            between_brackets = re.findall(r'\((.*?)\)', self.points_line.text())
            
            name = self.name_line.text()
            digits = [get_digits(i) for i in between_brackets]

            types = [
                Polygon.OPEN,
                Polygon.CLOSED,
                Polygon.FILLED
            ]
            style = types[self.type_group.checkedId()]

            vectors = [Vector(p[0], p[1]) for p in digits]
            shape = Polygon(name, vectors, self.color, style)

            if vectors:
               self.add_shape(shape)
               
        except ValueError:
            pass


class RectangleWidget(GenericShapeWidget):
    def __init__(self, viewport, object_list): 
        super().__init__(viewport, object_list)

        self.x0_line = QLineEdit()
        self.y0_line = QLineEdit()
        self.x1_line = QLineEdit()
        self.y1_line = QLineEdit()
        self.fill_box = QCheckBox()

        layout = QFormLayout()
        layout.addRow('Name', self.name_line)
        layout.addRow('X0', self.x0_line)
        layout.addRow('Y0', self.y0_line)
        layout.addRow('X1', self.x1_line)
        layout.addRow('Y1', self.y1_line)
        layout.addRow('Color', self.color_button)
        layout.addRow('Fill color', self.fill_box)
        layout.addRow(self.random_button)
        layout.addRow(self.apply_button)
        self.setLayout(layout)

    def random_callback(self):
        self.color = [randint(0,255) for _ in range(3)]
        self.paint_button(self.color_button, self.color)

        lines = [
            self.x0_line,
            self.y0_line,
            self.x1_line,
            self.y1_line,
        ]

        for line in lines:
            n = randint(0, 400)
            line.setText(str(n))

    def apply_callback(self):
        try:
            name = self.name_line.text()
            x0 = int(self.x0_line.text())
            y0 = int(self.y0_line.text())
            x1 = int(self.x1_line.text())
            y1 = int(self.y1_line.text())
            fill = bool(self.fill_box.checkState())
            style = Polygon.FILLED if fill else Polygon.CLOSED

            s = Vector(x0, y0)
            e = Vector(x1, y1)
            shape = Rectangle(name, s, e, self.color, style)
            self.add_shape(shape)
        except ValueError:
            pass


class BezierWidget(GenericShapeWidget):
    def __init__(self, viewport, object_list): 
        super().__init__(viewport, object_list)

        self.points_line = QLineEdit()

        layout = QFormLayout()
        layout.addRow('Name', self.name_line)
        layout.addRow('Your Points', self.points_line)
        layout.addRow('Color', self.color_button)
        layout.addRow(self.random_button)
        layout.addRow(self.apply_button)
        self.setLayout(layout)

    def random_callback(self):
        self.color = [randint(0,255) for _ in range(3)]
        self.paint_button(self.color_button, self.color)

        n_points = randint(1, 5) * 3 + 1
        points = [(randint(0,400), randint(0,400)) for i in range(n_points)]
        text =  ''.join(f'{i}, ' for i in points)
        self.points_line.setText(text)
    
    def apply_callback(self):
        try:
            get_digits = lambda x: tuple(int(i) for i in re.findall(r'-?\d+', x))
            between_brackets = re.findall(r'\((.*?)\)', self.points_line.text())
            
            name = self.name_line.text()
            digits = [get_digits(i) for i in between_brackets]

            vectors = [Vector(p[0], p[1]) for p in digits]
            shape = Bezier(name, vectors, self.color)

            if vectors:
               self.add_shape(shape)
               
        except ValueError:
            pass