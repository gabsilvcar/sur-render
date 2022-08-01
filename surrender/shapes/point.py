from copy import deepcopy

from surrender.shapes.generic_shape import GenericShape


class Point(GenericShape):
    DO_NOT_CLIP = 0
    TRIVIAL = 1
    CLIPPING_ALGORITHM = TRIVIAL

    def __init__(self, name, pos, color=(0, 0, 0)):
        super().__init__(name, "Point", color)
        self._pos = pos
        self._projected = pos.copy()

    def structural_points(self):
        return [self._pos]
    
    def projection_points(self):
        return [self._projected]

    def clipped_points(self):
        return self.projection_points()

    def clip(self, window_min, window_max):
        inx = window_min.x <= self._projected.x <= window_max.x
        iny = window_min.y <= self._projected.y <= window_max.y

        if inx and iny:
            return True
        else:
            return False

    def revert_projection(self):
        x, y, z = self._pos.get_pos()
        self._projected.set_pos(x, y, z)
