from surrender.shapes import Polygon
from surrender.vector import Vector


class Rectangle(Polygon):
    def __init__(self, name, start, end, color=(0, 0, 0), style=1):
        """
        p0 ------ p1
        |          |
        |          |
        |          |
        p2 ------ p3
        """
        self.p0 = start
        self.p1 = Vector(start.x, end.y)
        self.p2 = end
        self.p3 = Vector(end.x, start.y)

        points = [self.p0, self.p1, self.p2, self.p3]
        super().__init__(name, points, color, style)
        self.type = "Rectangle"
