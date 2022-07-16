from copy import deepcopy

from surrender.shapes.generic_shape import GenericShape
from surrender.clipping import cohen_sutherland, liang_barsky


class Line(GenericShape):
    DO_NOT_CLIP = 0
    COHEN_SUTHERLAND = 1
    LIANG_BARSKY = 2

    CLIPPING_ALGORITHM = COHEN_SUTHERLAND

    def __init__(self, name, start, end, color=(0, 0, 0)):
        super().__init__(name, "Line", color)
        self.start = start
        self.end = end

    def points(self):
        return [self.start, self.end]

    def clipped(self, window):
        if self.CLIPPING_ALGORITHM == self.COHEN_SUTHERLAND:
            p = cohen_sutherland(self.start, self.end, window)
        elif self.CLIPPING_ALGORITHM == self.LIANG_BARSKY:
            p = liang_barsky(self.start, self.end, window)
        else:
            return self

        if p is None:
            return None

        line = deepcopy(self)
        line.start = p[0]
        line.end = p[1]

        return line
