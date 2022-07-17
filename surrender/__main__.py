import sys
import surrender.breeze_resources  # noqa: F401
from surrender.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream


def main():
    app = QApplication(sys.argv)

    file = QFile(":/dark/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    MainWindow()
    sys.exit(app.exec_())


main()
