from PyQt5.QtWidgets import QGraphicsView

class Viewport(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.show()