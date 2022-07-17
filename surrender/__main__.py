import sys
from PyQt5.QtWidgets import QApplication
from surrender.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    # app.setStyleSheet(dark_stylesheet)
    MainWindow()
    sys.exit(app.exec_())


main()
