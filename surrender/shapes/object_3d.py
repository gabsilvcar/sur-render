from surrender.shapes.generic_shape import GenericShape
from surrender.shapes import Line
from surrender.clipping import cohen_sutherland


class Object3D(GenericShape):
    def __init__(self, name, segments, color=(0, 0, 0)):
        super().__init__(name, "Object3D", color)
        self._structural_segments = list()
        self._projection_segments = list()

        self._clipped_segments = list()
        self._structural_points = list()
        self._projection_points = list()

        self.set_segments(segments)

    def structural_points(self):
        return self._structural_points
    
    def projection_points(self):
        return self._projection_points
    
    def clipped_points(self):
        return []
    
    def structural_segments(self):
        return self._structural_segments
    
    def projection_segments(self):
        return self._projection_segments
    
    def clipped_segments(self):
        return self._clipped_segments

    def copy(self):
        new_segments = [(a.copy(), b.copy()) for a, b in self._segments]
        return self.__class__(self.name, new_segments, self.color)

    def set_segments(self, segments):
        self._structural_points.clear()
        self._projection_points.clear()

        self._structural_segments = segments
        self._projection_segments.clear()

        for a, b in segments:
            self._structural_points.append(a)
            self._structural_points.append(b)

            ac = a.copy()
            bc = b.copy()
            self._projection_points.append(ac)
            self._projection_points.append(bc)
            self._projection_segments.append((ac, bc))

        self._clipped_segments = self._projection_segments

    def clip(self, window_min, window_max):
        new_segments = []
        for a, b in self.projection_segments():
            if cohen_sutherland(a, b, window_min, window_max):
                new_segments.append((a, b))
        self._clipped_segments = new_segments
        need_plot = len(new_segments) != 0
        return need_plot

    def revert_projection(self):
        structural = self.structural_points()
        projection = self.projection_points()
        self.__clipped_segments = self._projection_segments
        for s, p in zip(structural, projection):
            x, y, z = s.get_pos()
            p.set_pos(x, y, z)
