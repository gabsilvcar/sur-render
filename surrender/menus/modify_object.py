import numpy as np
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from surrender.vector import Vector


class ModifyObject(QWidget):
    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport
        self.create_tabs()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(MoveWidget(self.viewport), "Move")
        self.tabs.addTab(ScaleWidget(self.viewport), "Scale")
        self.tabs.addTab(RotateWidget(self.viewport), "Rotate")


class MoveWidget(QWidget):
    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport
        self.x_line = QLineEdit()
        self.y_line = QLineEdit()
        self.z_line = QLineEdit()
        self.apply_button = QPushButton("Apply")
        self.apply_button.pressed.connect(self.apply_callback)

        layout = QFormLayout()
        layout.addRow("X", self.x_line)
        layout.addRow("Y", self.y_line)
        layout.addRow("Z", self.z_line)
        layout.addRow("", self.apply_button)
        self.setLayout(layout)

    def apply_callback(self):
        x = self.x_line.text()
        y = self.y_line.text()
        z = self.z_line.text()
        x = float(x) if x else 0
        y = float(y) if y else 0
        z = float(z) if z else 0
        v = Vector(x, y, z)

        if self.viewport.selected_shape is None:
            return

        self.viewport.selected_shape.move(v)
        self.viewport.shapeModified.emit()
        self.viewport.update()


class ScaleWidget(QWidget):
    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport
        self.x_line = QLineEdit()
        self.y_line = QLineEdit()
        self.z_line = QLineEdit()
        self.apply_button = QPushButton("Apply")
        self.apply_button.pressed.connect(self.apply_callback)

        layout = QFormLayout()
        layout.addRow("X", self.x_line)
        layout.addRow("Y", self.y_line)
        layout.addRow("Z", self.z_line)
        layout.addRow("", self.apply_button)
        self.setLayout(layout)

    def apply_callback(self):
        x = self.x_line.text()
        y = self.y_line.text()
        z = self.z_line.text()
        x = float(x) if x else 1
        y = float(y) if y else 1
        z = float(z) if z else 1
        v = Vector(x, y, z)

        if self.viewport.selected_shape is None:
            return

        center = self.viewport.selected_shape.center()
        self.viewport.selected_shape.scale(v, center)
        self.viewport.shapeModified.emit()
        self.viewport.update()


class RotateWidget(QWidget):
    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport
        self.combobox = QComboBox()

        self.x_angle_line = QLineEdit()
        self.y_angle_line = QLineEdit()
        self.z_angle_line = QLineEdit()

        self.around_x_line = QLineEdit()
        self.around_y_line = QLineEdit()
        self.apply_button = QPushButton("Apply")
        self.apply_button.pressed.connect(self.apply_callback)

        self.combobox.addItem("Rotate Around Origin")
        self.combobox.addItem("Rotate Around Center")
        self.combobox.addItem("Rotate Around Vector")
        self.combobox.activated.connect(self.box_callback)

        self.around_x_line.setReadOnly(True)
        self.around_y_line.setReadOnly(True)
        self.around_x_line.setPlaceholderText("Not avaliable")
        self.around_y_line.setPlaceholderText("Not avaliable")

        layout = QFormLayout()
        layout.addRow("", self.combobox)
        layout.addRow("Angle x", self.x_angle_line)
        layout.addRow("Angle y", self.y_angle_line)
        layout.addRow("Angle z", self.z_angle_line)
        layout.addRow("Around X", self.around_x_line)
        layout.addRow("Around Y", self.around_y_line)
        layout.addRow("", self.apply_button)
        self.setLayout(layout)

    def apply_callback(self):
        around_x = self.around_x_line.text()
        around_y = self.around_y_line.text()
        angle_x = self.x_angle_line.text()
        angle_y = self.y_angle_line.text()
        angle_z = self.z_angle_line.text()

        around_x = float(around_x) if around_x else 1
        around_y = float(around_y) if around_y else 1
        angle_x = np.radians(float(angle_x) if angle_x else 0)
        angle_y = np.radians(float(angle_y) if angle_y else 0)
        angle_z = np.radians(float(angle_z) if angle_z else 0)

        if self.viewport.selected_shape is None:
            return

        txt = self.combobox.currentText()
        if txt == "Rotate Around Origin":
            around = Vector(0, 0)
        elif txt == "Rotate Around Center":
            around = self.viewport.selected_shape.center()
        elif txt == "Rotate Around Vector":
            around = Vector(around_x, around_y)

        self.viewport.selected_shape.rotate_x(angle_x, around)
        self.viewport.selected_shape.rotate_y(angle_y, around)
        self.viewport.selected_shape.rotate_z(angle_z, around)
        self.viewport.shapeModified.emit()
        self.viewport.update()

    def box_callback(self):
        ro = self.combobox.currentText() != "Rotate Around Vector"

        self.around_x_line.setReadOnly(ro)
        self.around_y_line.setReadOnly(ro)

        if ro:
            self.around_x_line.setPlaceholderText("Not avaliable")
            self.around_y_line.setPlaceholderText("Not avaliable")
        else:
            self.around_x_line.setPlaceholderText("")
            self.around_y_line.setPlaceholderText("")
