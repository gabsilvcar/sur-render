import sys

from PyQt5.QtWidgets import QApplication

from SurRender.main_window  import MainWindow

app = QApplication(sys.argv)

frame = MainWindow()

sys.exit(app.exec_())
