import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QToolBar,
    QApplication,
    QMenu,
    QMainWindow,
    QFileDialog,
)
from surrender.menus.add_object import AddObject
from surrender.menus.object_list import ObjectList
from surrender.menus.modify_object import ModifyObject
from surrender.menus.modify_view import ModifyView
from surrender.menus.tools_menu import ToolsMenu
from surrender.constants import WINDOW_HEIGHT, WINDOW_WIDTH, APPLICATION_NAME
from surrender.viewport import Viewport
from surrender.tools import HandTool


class MainWindow(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.viewport = Viewport()
        self.current_tool = HandTool(self)
        self.init_ui()
        self.__createActions()
        self.__createMenuBar()
        self.__createToolBars()
        self.show()

    def init_ui(self):
        self.resize(WINDOW_HEIGHT, WINDOW_WIDTH)
        self.setWindowTitle(APPLICATION_NAME)
        self.setWindowIcon(QtGui.QIcon("resources/logo.jpg"))
        self.setCentralWidget(self.viewport)

    def open_callback(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Wavefront *.obj")
        if path:
            self.viewport.open(path)

    def save_callback(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Wavefront *.obj")
        if path:
            self.viewport.save(path)

    def __createActions(self):
        self.newAction = QAction(QtGui.QIcon(":logo"), "&New", self)
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

        self.openAction.triggered.connect(self.open_callback)
        self.saveAction.triggered.connect(self.save_callback)

        self.openAction.setShortcut("ctrl+o")
        self.saveAction.setShortcut("ctrl+s")

    def __createMenuBar(self):
        menuBar = self.menuBar()

        # File menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        # Edit menu
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

    def __createToolBars(self):
        # Object List
        objectListToolBar = QToolBar("Object List", self)
        objectListToolBar.addWidget(ObjectList(self.viewport))
        self.addToolBar(Qt.LeftToolBarArea, objectListToolBar)

        # ModifyView
        modifyViewToolBar = QToolBar("Mod View", self)
        modifyViewToolBar.addWidget(ModifyView(self.viewport))
        self.addToolBar(Qt.LeftToolBarArea, modifyViewToolBar)

        toolsToolBar = QToolBar("Tools", self)
        toolsToolBar.addWidget(ToolsMenu(self))
        toolsToolBar.hide()
        self.addToolBar(Qt.LeftToolBarArea, toolsToolBar)

        # AddObject
        addObjToolBar = QToolBar("Add Object", self)
        addObjToolBar.addWidget(AddObject(self.viewport))
        self.addToolBar(Qt.RightToolBarArea, addObjToolBar)

        # ModifyObject
        modifyObjToolBar = QToolBar("Mod Object", self)
        modifyObjToolBar.addWidget(ModifyObject(self.viewport))
        self.addToolBar(Qt.RightToolBarArea, modifyObjToolBar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
