from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from surrender.viewport import Viewport


class CustomTable(QTreeView):
    itemSelected = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = QStandardItemModel(0, 3)
        self.setModel(self.model)
    
    def setHorizontalHeaderLabels(self, *args, **kwargs):
        self.model.setHorizontalHeaderLabels(*args, **kwargs)
    
    def appendRow(self, *args, **kwargs):
        self.model.appendRow(*args, **kwargs)

    def clearRows(self):
        self.model.removeRows(0, self.model.rowCount())

    def selectionChanged(self, selected, deselected):
        super().selectionChanged(selected, deselected)
        self.itemSelected.emit()


class ObjectList(QWidget):
    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport
        self.viewport.shapeModified.connect(self.update)
        
        self.table = CustomTable()
        self.table.setHorizontalHeaderLabels(['NAME', 'SHAPE', 'COLOR'])
        self.table.itemSelected.connect(self.selection_callback)

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.clicked.connect(self.delete_callback)
        self.delete_button.setShortcut(Qt.Key_Delete)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.delete_button)
        
        self.setLayout(layout)
        self.update()
    
    def selected_index(self):
        return self.table.currentIndex().row()

    def selection_callback(self):
        i = self.table.currentIndex().row()
        self.viewport.selected_shape = self.viewport.get_shape_by_index(i)

    def delete_callback(self):
        selected = self.viewport.selected_shape
        self.viewport.remove_shape(selected)
    
    def populate_tree(self):
        self.table.clearRows()

        for shape in self.viewport.scene.shapes:
            name = QStandardItem(str(shape.name))
            types = QStandardItem(str(shape.type))
            color = QStandardItem()
            color.setBackground(QBrush(QColor(*shape.color)))
            self.table.appendRow([name, types, color])

    def update(self):
        self.populate_tree()
        super().update()

