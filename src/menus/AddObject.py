import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsView
import random
from src.Shapes import *
from PyQt5.QtWidgets import * 

from src.primitives import Vector, Segment
  

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
  
        # printing the form information
        # print("Current : {0}".format(self.tabs.tabText(self.tabs.currentIndex())))
        # print("Person Name : {0}".format(self.nameLineEdit.text()))
        # print("Age : {0}".format(self.ageSpinBar.text()))
        # print("X1L : {0}".format(self.Lx1LineEdit.text()))
        # print("Y1L : {0}".format(self.Ly1LineEdit.text()))
        # print("X2L : {0}".format(self.Lx2LineEdit.text()))
        # print("Y2L : {0}".format(self.Ly2LineEdit.text()))
        # print("X1R : {0}".format(self.Rx1LineEdit.text()))
        # print("Y1R : {0}".format(self.Ry1LineEdit.text()))
        # print("X2R : {0}".format(self.Rx2LineEdit.text()))
        # print("Y2R : {0}".format(self.Ry2LineEdit.text()))
        # print("X1C : {0}".format(self.Cx1LineEdit.text()))
        # print("Y1C : {0}".format(self.Cy1LineEdit.text()))
        # print("R : {0}".format(self.CRLineEdit.text()))

        widget = self.tabs.currentWidget()

        if (self.tabs.tabText(self.tabs.currentIndex()) == "Point"):
            name = self.nameLineEdit.text()
            pos = Vector(widget.x(), widget.y())
            shape = Point(name, pos)
            self.viewport.scene.add_shape(shape)

        if (self.tabs.tabText(self.tabs.currentIndex()) == "Line"):
            name = self.nameLineEdit.text()
            s = Vector(widget.x0(), widget.y0())
            e = Vector(widget.x1(), widget.y1())
            shape = Line(name, s, e)
            self.viewport.scene.add_shape(shape)


            # pos1 = QtCore.QPoint(widget.x0(), widget.y0())
            # pos2 = QtCore.QPoint(widget.x1(), widget.y1())
            # length = random.randrange(100)
            # color = QtGui.QColor(*random.choices(range(256), k=3))
            # shape = Line(self.nameLineEdit.text(), pos1, pos2, color)
            # self.viewport.scene.shapes.append(shape)

        # s = Polygon("Polinho", 
        #     [
        #         QtCore.QPoint(0, 0),
        #         QtCore.QPoint(100, 100),
        #         QtCore.QPoint(50, 20),
        #         QtCore.QPoint(10, 40),
        #     ]
        # )

        # self.viewport.scene.shapes.append(s)
            
        # if (self.tabs.tabText(self.tabs.currentIndex()) == "Rectangle"):
        #     pos1 = QtCore.QPoint(int(self.Lx1LineEdit.text()), int(self.Ly1LineEdit.text()))
        #     pos2 = QtCore.QPoint(int(self.Lx2LineEdit.text()), int(self.Ly2LineEdit.text()))
        #     length = random.randrange(100)
        #     color = QtGui.QColor(*random.choices(range(256), k=3))
        #     shape = Rectangle(self.nameLineEdit.text(), pos1, pos2, color)
        #     self.viewport.scene.shapes.append(shape)
    
        # if (self.tabs.tabText(self.tabs.currentIndex()) == "Circle"):
        #     pos = QtCore.QPoint(int(self.Cx1LineEdit.text()), int(self.Cy1LineEdit.text()))
        #     length = int(self.CRLineEdit.text())
        #     color = QtGui.QColor(*random.choices(range(256), k=3))  
        #     print(length, pos, color)          
        #     shape = Circle(self.nameLineEdit.text(), length, pos, color)
        #     self.viewport.scene.shapes.append(shape)

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
        self.tabs.addTab(PointWidget(self),"Point")
        self.tabs.addTab(LineWidget(self),"Line")
        # self.tabs.addTab(RectangleWidget(self),"Rectangle")
        # self.tabs.addTab(CircleWidget(self),"Circle")

        
        layout.addWidget(self.tabs)

        # for age and adding spin box
        # layout.addRow(QLabel("Age"), self.ageSpinBar)
  
        # setting layout
        self.formGroupBox.setLayout(layout)
  
class PointWidget(QWidget):
    def __init__(self, parent): 
        super().__init__()
        self.x_line = QLineEdit()
        self.y_line = QLineEdit()

        self.setLayout(QFormLayout())
        self.layout().addRow('X', self.x_line)
        self.layout().addRow('Y', self.y_line)
    
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

        self.setLayout(QFormLayout())
        self.layout().addRow('X0', self.x0_line)
        self.layout().addRow('Y0', self.y0_line)
        self.layout().addRow('X1', self.x1_line)
        self.layout().addRow('Y1', self.y1_line)

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

# class RectangleWidget(QWidget):
#     def __init__(self, parent): 
#         super().__init__()
#         layout = QFormLayout()
#         layout.addRow(QLabel("X1"), parent.Rx1LineEdit)
#         layout.addRow(QLabel("Y1"), parent.Ry1LineEdit)
#         layout.addRow(QLabel("X2"), parent.Rx2LineEdit)
#         layout.addRow(QLabel("Y2"), parent.Ry2LineEdit)
#         self.setLayout(layout)

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