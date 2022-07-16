import numpy as np
from surrender.vector import Vector
from surrender.shapes import Polygon


class View(Polygon):
    def __init__(self, p0, p1, p2, p3, projection_distance=1000):
        """
        p0 ------ p1
        |          |
        |          |
        |          |
        p3 ------ p2
        """

        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.projection_distance = projection_distance

        points = [self.p0, self.p1, self.p2, self.p3]
        super().__init__("", points, style=Polygon.CLOSED)

    def center_of_projection(self):
        return self.center() - self.normal_vector() * self.projection_distance

    def ppc(self):
        w = self.width()
        h = self.height()
        v = Vector(-w / 2, -h / 2)

        ppc = View(
            Vector(0, h),
            Vector(w, h),
            Vector(w, 0),
            Vector(0, 0),
        )

        ppc.move(v)
        return ppc

    def min(self):
        return self.p3

    def max(self):
        return self.p1

    def up_vector(self):
        return (self.p0 - self.p3).normalized()

    def right_vector(self):
        return (self.p1 - self.p0).normalized()

    def normal_vector(self):
        uv = self.up_vector()
        rv = self.right_vector()
        return -np.cross(uv, rv).normalized()

    def width(self):
        return (self.p1 - self.p0).length()

    def height(self):
        return (self.p0 - self.p3).length()

    def move(self, vector):
        """
        The user don't want to move the window according to
        global coordinates, but according to the window local
        coordinates.

        The equivalent to local Y is the up vector, and the equivalent
        to the local X is the right vector. As these are unit vectors,
        we can multiply each of them by the magnitude of X and Y then
        combine both in a single vector instead of calculating a matrix
        and stuff like that.
        """

        uv = self.up_vector()
        rv = self.right_vector()
        nv = self.normal_vector()
        vector = (rv * vector.x) + (uv * vector.y) + (nv * vector.z)
        super().move(vector)

    def zoom(self, amount, around=None):
        v = Vector(amount, amount, amount)
        around = self.center()
        super().scale(v, around)

    def __str__(self):
        return f"View({self.min()} {self.max()})"
