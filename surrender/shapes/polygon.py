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
        self._points = points
        self._projected_points = [p.copy() for p in self._points]
        self._clipped_points = self._projected_points
        self.style = style

    def structural_points(self):
        return self._points
    
    def projection_points(self):
        return self._projected_points
    
    def clipped_points(self):
        return self._clipped_points
    
    def projection_segments(self):
        yield from adjacents(self.projection_points(), circular=True)
    
    def clipped_segments(self):
        yield from adjacents(self.clipped_points(), circular=True)

    def clip(self, window_min, window_max):
        self._clipped_points = sutherland_hodgeman(self.projection_points(), window_min, window_max, True)
        need_plot = len(self._clipped_points) != 0
        return True

    def revert_projection(self):
        structural = self.structural_points()
        projection = self.projection_points()
        for s, p in zip(structural, projection):
            x, y, z = s.get_pos()
            p.set_pos(x, y, z)
        self._clipped_points = projection
