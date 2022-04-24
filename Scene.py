from PyQt5.QtWidgets import QGraphicsScene

class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.addText("Hello, world!")
        