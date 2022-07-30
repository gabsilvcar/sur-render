from surrender.shapes.generic_shape import GenericShape
from surrender.shapes import Line
from surrender.clipping import cohen_sutherland


class Object3D(GenericShape):
    def __init__(self, name, segments, color=(0, 0, 0)):
        super().__init__(name, "Object3D", color)
        self.segments = list()
        self.visual_points = list()
        self.set_segments(segments)

    def copy(self):
        new_segments = [(a.copy(), b.copy()) for a, b in self.segments]
        return self.__class__(self.name, new_segments, self.color)

    def set_segments(self, segments):
        self.visual_points.clear()
        self.segments = list(segments)

        for a, b in segments:
            self.visual_points.append(a)
            self.visual_points.append(b)

    def clipped(self, window):
        new_segments = []
        wmin = window.min()
        wmax = window.max()
        for a, b in self.segments:
            if cohen_sutherland(a, b, wmin, wmax):
                new_segments.append((a, b))
        c = self.copy()
        c.set_segments(new_segments)
        return c

    def points(self):
        return self.visual_points

    def as_lines(self):
        for a, b in self.segments:
            yield Line("", a, b, self.color)
