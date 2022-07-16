from surrender.shapes.generic_shape import GenericShape


class GenericCurve(GenericShape):
    DO_NOT_CLIP = 0
    SUTHERLAND_HODGEMAN = 1

    OPEN = 0
    CLOSED = 1
    FILLED = 2 | CLOSED  # if it is filled must be closed as well

    CLIPPING_ALGORITHM = SUTHERLAND_HODGEMAN

    def __init__(self, name, color=(0, 0, 0), style=CLOSED):
        super().__init__(name, "Curve", color)
        self.style = style
