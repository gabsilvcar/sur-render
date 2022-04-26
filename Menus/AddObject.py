import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsView
import random
from Shapes import *
from PyQt5.QtWidgets import * 
  
# creating a class
# that inherits the QDialog class
class AddObject(QWidget):
  
    # constructor
    def __init__(self, viewport_widget):
        super(AddObject, self).__init__()
        self.viewportWidget = viewport_widget
        # setting window title
        self.setWindowTitle("Python")
  
        # setting geometry to the window
        self.setGeometry(100, 100, 300, 400)
  
        # creating a group box
        self.formGroupBox = QGroupBox("Add Object")
  
        # creating spin box to select age
        self.ageSpinBar = QSpinBox()
  
        # creating a line edit
        self.nameLineEdit = QLineEdit()
  
  
        self.Lx1LineEdit = QLineEdit();
        self.Rx1LineEdit = QLineEdit();
        self.Lx2LineEdit = QLineEdit();
        self.Rx2LineEdit = QLineEdit();
        self.Ly1LineEdit = QLineEdit();
        self.Ry1LineEdit = QLineEdit();
        self.Ly2LineEdit = QLineEdit();
        self.Ry2LineEdit = QLineEdit();
        self.Cx1LineEdit = QLineEdit();
        self.Cy1LineEdit = QLineEdit();
        self.CRLineEdit = QLineEdit();

        # calling the method that create the form
        self.createForm()
  
        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
  
        # adding action when form is accepted
        self.buttonBox.accepted.connect(self.getInfo)
  
        # adding action when form is rejected
        # self.buttonBox.rejected.connect(self.reject)
  
        # creating a vertical layout
        mainLayout = QVBoxLayout()
  
        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
  
        # adding button box to the layout
        mainLayout.addWidget(self.buttonBox)
  
        # setting lay out
        self.setLayout(mainLayout)
  
    # get info method called when form is accepted
    def getInfo(self):
  
        # printing the form information
        print("Current : {0}".format(self.tabs.tabText(self.tabs.currentIndex())))
        print("Person Name : {0}".format(self.nameLineEdit.text()))
        print("Age : {0}".format(self.ageSpinBar.text()))
        print("X1L : {0}".format(self.Lx1LineEdit.text()))
        print("Y1L : {0}".format(self.Ly1LineEdit.text()))
        print("X2L : {0}".format(self.Lx2LineEdit.text()))
        print("Y2L : {0}".format(self.Ly2LineEdit.text()))
        print("X1R : {0}".format(self.Rx1LineEdit.text()))
        print("Y1R : {0}".format(self.Ry1LineEdit.text()))
        print("X2R : {0}".format(self.Rx2LineEdit.text()))
        print("Y2R : {0}".format(self.Ry2LineEdit.text()))
        print("X1C : {0}".format(self.Cx1LineEdit.text()))
        print("Y1C : {0}".format(self.Cy1LineEdit.text()))
        print("R : {0}".format(self.CRLineEdit.text()))

            
        if (self.tabs.tabText(self.tabs.currentIndex()) == "Circle"):
            pos = QtCore.QPoint(int(self.Cx1LineEdit.text()), int(self.Cy1LineEdit.text()))
            length = int(self.CRLineEdit.text())
            color = QtGui.QColor(*random.choices(range(256), k=3))  
            print(length, pos, color)          
            shape = Circle(self.nameLineEdit.text(), length, pos, color)
            self.viewportWidget.scene.shapes.append(shape)
    
        
  
    # creat form method
    def createForm(self):
  
        # creating a form layout
        layout = QFormLayout()
  
        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Name"), self.nameLineEdit)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(Line(self),"Line")
        self.tabs.addTab(Rectangle(self),"Rectangle")
        self.tabs.addTab(Circle(self),"Circle")

        
        layout.addWidget(self.tabs)

        # for age and adding spin box
        # layout.addRow(QLabel("Age"), self.ageSpinBar)
  
        # setting layout
        self.formGroupBox.setLayout(layout)
  
class Line(QWidget):
    def __init__(self, parent): 
        super().__init__()
        layout = QFormLayout()
        layout.addRow(QLabel("X1"), parent.Lx1LineEdit)
        layout.addRow(QLabel("Y1"), parent.Ly1LineEdit)
        layout.addRow(QLabel("X2"), parent.Lx2LineEdit)
        layout.addRow(QLabel("Y2"), parent.Ly2LineEdit)
        self.setLayout(layout)

class Rectangle(QWidget):
    def __init__(self, parent): 
        super().__init__()
        layout = QFormLayout()
        layout.addRow(QLabel("X1"), parent.Rx1LineEdit)
        layout.addRow(QLabel("Y1"), parent.Ry1LineEdit)
        layout.addRow(QLabel("X2"), parent.Rx2LineEdit)
        layout.addRow(QLabel("Y2"), parent.Ry2LineEdit)
        self.setLayout(layout)

class Circle(QWidget):
    def __init__(self, parent): 
        super().__init__()
        layout = QFormLayout()
        layout.addRow(QLabel("X1"), parent.Cx1LineEdit)
        layout.addRow(QLabel("Y1"), parent.Cy1LineEdit)
        layout.addRow(QLabel("R"), parent.CRLineEdit)
        self.setLayout(layout)

  
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