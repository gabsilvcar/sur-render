import sys
from src.menus.AddObject import AddObject
from src.menus.AddObject import AddObject
from src.menus.Movement import Movement
from src.menus.ObjectList import ObjectList
from src.menus.Zoom import Zoom
import src.qrc_resources

from src.Constants import Constants
from src.ViewportWidget import ViewportWidget
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
        self.resize(Constants.WINDOW_HEIGHT, Constants.WINDOW_WIDTH)
        self.setWindowTitle(Constants.APPLICATION_NAME)
        self.setWindowIcon(QtGui.QIcon(":logo"))
        self.centralWidget = ViewportWidget()
        self.setCentralWidget(self.centralWidget)

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
        # Help menu
        # helpMenu = menuBar.addMenu(QIcon(":help-content.svg"), "&Help")
        # helpMenu.addAction(self.helpContentAction)
        # helpMenu.addAction(self.aboutAction)

        
    def __createToolBars(self):
        # Object List
        self.objectview = ObjectList(self.centralWidget.viewport.scene)
        objectListToolBar = QToolBar("Object List", self)
        objectListToolBar.addWidget(self.objectview)
        self.addToolBar(Qt.LeftToolBarArea, objectListToolBar)

        # Zoom
        zoomToolBar = QToolBar("Zoom", self)
        zoomToolBar.addWidget(Zoom(self, self.centralWidget))
        self.addToolBar(Qt.LeftToolBarArea, zoomToolBar)
        # Movement
        movementToolBar = QToolBar("Movement", self)
        movementToolBar.addWidget(Movement(self, self.centralWidget))
        self.addToolBar(Qt.LeftToolBarArea, movementToolBar)
        # AddObject
        addObjToolBar = QToolBar("Add Object", self)
        addObjToolBar.addWidget(AddObject(self.centralWidget, self.objectview))
        self.addToolBar(Qt.LeftToolBarArea, addObjToolBar)

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
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
