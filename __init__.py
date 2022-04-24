import sys

from PyQt5.QtWidgets import QApplication


from GUIPanel import GUIFrame

app = QApplication(sys.argv)

# 3. Create an instance of your application's GUI
frame = GUIFrame()

# 4. Show your application's GUI
frame.show()

# 5. Run your application's event loop (or main loop)
sys.exit(app.exec_())
