from copy import deepcopy

from surrender.shapes.generic_shape import GenericShape
from surrender.shapes import Line
from surrender.clipping import sutherland_hodgeman
from surrender.utils import adjacents


class Polygon(GenericShape):
    DO_NOT_CLIP = 0
    SUTHERLAND_HODGEMAN = 1

    OPEN = 0
    CLOSED = 1
    FILLED = 2 | CLOSED  # if it is filled must be closed as well

    CLIPPING_ALGORITHM = SUTHERLAND_HODGEMAN

    def __init__(self, name, points, color=(0, 0, 0), style=CLOSED):
        super().__init__(name, "Polygon", color)
        self.pts = points
        self.style = style

    def points(self):
        return self.pts

    def lines(self):
        circular = self.style != self.OPEN
        for start, end in adjacents(self.points(), circular=circular):
            yield Line("", start, end)

    def clipped(self, window):
        clipped_points = []

        if self.CLIPPING_ALGORITHM == self.DO_NOT_CLIP:
            return self
        elif self.CLIPPING_ALGORITHM == self.SUTHERLAND_HODGEMAN:
            closed = self.style & self.CLOSED
            clipped_points = sutherland_hodgeman(self.points(), window, closed)

        c = deepcopy(self)
        c.pts = clipped_points
        return c
