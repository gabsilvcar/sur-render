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
        self._projected_points = [start.copy(), end.copy()]

    def structural_points(self):
        return [self.start, self.end]
    
    def projection_points(self):
        return self._projected_points
    
    def clipped_points(self):
        return self.projection_points()
    
    def clip(self, window_min, window_max):
        start, end = self.projection_points()
        need_plot = cohen_sutherland(start, end, window_min, window_max)
        return need_plot

    def revert_projection(self):
        structural = self.structural_points()
        projection = self.projection_points()
        for s, p in zip(structural, projection):
            x, y, z = s.get_pos()
            p.set_pos(x, y, z)


    # def structural_points(self):
    #     return [self.start, self.end]

    # def points(self):
    #     return [self.start, self.end]

    # def clip(self, window_min, window_max):
    #     if self.CLIPPING_ALGORITHM != self.COHEN_SUTHERLAND:
    #         return True        
    #     need_plot = cohen_sutherland(self.start, self.end, window_min, window_max)
    #     return need_plot

    # def clipped(self, window):
    #     line = deepcopy(self)

    #     if self.CLIPPING_ALGORITHM == self.COHEN_SUTHERLAND:
    #         p = cohen_sutherland(line.start, line.end, window.min(), window.max())
    #         if not p:
    #             return None
    #     elif self.CLIPPING_ALGORITHM == self.LIANG_BARSKY:
    #         p = liang_barsky(line.start, line.end, window)
    #     else:
    #         return self

    #     if p is None:
    #         return None

    #     return line
