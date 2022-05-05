from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import Qt, QSize

from SurRender.viewport import Viewport


class ObjectList(QWidget):
    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport
        self.scene = viewport.scene
        
        self.tree = QTreeView()
        self.model = QStandardItemModel(0, 3)
        self.model.setHorizontalHeaderLabels(['NAME', 'SHAPE', 'COLOR'])
        self.tree.setModel(self.model)

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.clicked.connect(self.delete_callback)
        self.delete_button.setShortcut(Qt.Key_Delete)

        # self.move = MoveWidget(viewport)
        # self.scale = ScaleWidget(viewport)
        # self.rotate = RotateWidget(viewport)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)
    
    def selected_index(self):
        return self.tree.currentIndex().row()

    def delete_callback(self):
        try:
            i = self.tree.currentIndex().row()
            self.scene.shapes.pop(i)
            self.update()
            self.viewport.update()
        except IndexError:
            pass
    
    def populate_tree(self):
        self.model.removeRows(0, self.model.rowCount())

        for i, shape in enumerate(self.scene.shapes):
            name = QStandardItem(str(shape.name))
            types = QStandardItem(str(shape.__class__.__name__))
            color = QStandardItem()
            color.setBackground(QBrush(QColor(*shape.color)))
            self.model.appendRow([name, types, color])

    def update(self):
        super().update()
        self.populate_tree()

