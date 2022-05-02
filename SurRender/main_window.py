import sys
from SurRender.menus.add_object import AddObject
from SurRender.menus.movement import Movement
from SurRender.menus.object_list import ObjectList
from SurRender.menus.zoom import Zoom
import SurRender.qrc_resources

from SurRender.constants import WINDOW_HEIGHT, WINDOW_WIDTH, APPLICATION_NAME
from SurRender.viewport_widget import ViewportWidget
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.init_ui()
        self.__createActions()
        self.__createMenuBar()
        self.__createToolBars()
        self.show()
        
    def init_ui(self):
        self.resize(WINDOW_HEIGHT, WINDOW_WIDTH)
        self.setWindowTitle(APPLICATION_NAME)
        self.setWindowIcon(QtGui.QIcon(":logo"))
        self.centralWidget = ViewportWidget()
        self.setCentralWidget(self.centralWidget)

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
        self.objectview = ObjectList(self.centralWidget.viewport.scene)
        objectListToolBar = QToolBar("Object List", self)
        objectListToolBar.addWidget(self.objectview)
        self.addToolBar(Qt.LeftToolBarArea, objectListToolBar)

        # Zoom
        zoomToolBar = QToolBar("Zoom", self)
        zoomToolBar.addWidget(Zoom(self, self.centralWidget.viewport))
        self.addToolBar(Qt.LeftToolBarArea, zoomToolBar)

        # Movement
        movementToolBar = QToolBar("Movement", self)
        movementToolBar.addWidget(Movement(self, self.centralWidget.viewport))
        self.addToolBar(Qt.LeftToolBarArea, movementToolBar)

        # AddObject
        addObjToolBar = QToolBar("Add Object", self)
        addObjToolBar.addWidget(AddObject(self.centralWidget.viewport, self.objectview))
        self.addToolBar(Qt.LeftToolBarArea, addObjToolBar)


        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())