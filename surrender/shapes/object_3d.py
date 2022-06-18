from surrender.shapes.generic_shape import GenericShape
from surrender.shapes import Line


class Object3D(GenericShape):
    def __init__(self, name, segments, color=(0,0,0)):
        super().__init__(name, 'Object3D', color)
        self.segments = segments
        self.pts = set()

        for a,b in segments:
            self.pts.add(a)
            self.pts.add(b)

    def points(self):
        return list(self.pts)

    def as_lines(self):
        for a, b in self.segments:
            yield Line('', a, b, self.color)
