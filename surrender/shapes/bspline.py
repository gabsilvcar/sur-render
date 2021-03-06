from copy import deepcopy

from surrender.shapes import Polygon, Line
from surrender.shapes.generic_curve import GenericCurve
from surrender.parametric_curves import fd_bspline
from surrender.vector import Vector
from surrender.utils import adjacents
from surrender.clipping import sutherland_hodgeman


class BSpline(GenericCurve):
    def __init__(self, name, control_points, color=(0, 0, 0)):
        super().__init__(name, color, False)
        self.type = "B-Spline"
        self.resolution = 5
        self._control_points = control_points
        self._blended_points = control_points
        self.set_resolution(self.resolution)

    def set_resolution(self, resolution):
        self.resolution = resolution
        self._blended_points = self.blended_points()

    def as_polygon(self):
        p = Polygon(self.name, self._blended_points, self.color, Polygon.OPEN)
        p.CLIPPING_ALGORITHM = self.CLIPPING_ALGORITHM
        return p

    def points(self):
        return self._control_points

    def lines(self):
        for start, end in adjacents(self.blended_points(), circular=False):
            yield Line("", start, end)

    def packs_of_points(self, points):
        for i in range(len(points) - 3):
            yield points[i : (i + 4)]

    def blended_points(self):
        points = []
        for p in self.packs_of_points(self.points()):
            for x, y, z in fd_bspline(p, self.resolution):
                points.append(Vector(x, y, z))
        return points

    def clipped(self, window):
        clipped_points = []

        size = 1
        for start, end in adjacents(self.points(), circular=False):
            delta = end - start
            size = max(size, delta.x, delta.y, delta.z)
        self.set_resolution(int(size) // 20 + 1)

        if self.CLIPPING_ALGORITHM == self.DO_NOT_CLIP:
            return self

        closed = self.style & self.CLOSED
        clipped_points = sutherland_hodgeman(self.blended_points(), window, closed)

        c = deepcopy(self)
        c._blended_points = clipped_points
        return c
