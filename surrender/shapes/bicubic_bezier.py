from surrender.parametric_curves import bicubic_bezier
from surrender.shapes import Object3D
from surrender.vector import Vector


class BicubicBezier(Object3D):
    def __init__(self, name, control_points, color=(0, 0, 0)):
        super().__init__(name, [], color)
        self.type = "Bezier"

        self.control_points = control_points
        segments = self.generate_segments(control_points, 20)
        self.set_segments(segments)

    def copy(self):
        new_control_points = []
        new_segments = [(a.copy(), b.copy()) for a, b in self.segments]

        for line in self.control_points:
            new_line = []
            for p in line:
                new_line.append(p.copy())
            new_control_points.append(new_line)

        c = self.__class__(self.name, [], self.color)
        c.control_points = new_control_points
        c.set_segments(new_segments)
        return c

    def points(self):
        points = self.visual_points
        for line in self.control_points:
            for p in line:
                points.append(p)
        return points

    def generate_segments(self, control_points, resolution=1):
        segments = []

        for points in self.packs_of_points(control_points):
            for i in range(resolution):
                for j in range(resolution):
                    xyz_a = bicubic_bezier(i / resolution, j / resolution, points)
                    xyz_b = bicubic_bezier(i / resolution, (j + 1) / resolution, points)
                    xyz_c = bicubic_bezier((i + 1) / resolution, j / resolution, points)

                    a = Vector(*xyz_a)
                    b = Vector(*xyz_b)
                    c = Vector(*xyz_c)

                    segments.append((a, b))
                    segments.append((a, c))

        return segments

    def packs_of_points(self, points):
        if not points:
            return

        height = len(points)
        width = len(points[0])

        for h in range(0, height - 3, 3):
            for w in range(0, width - 3, 3):
                yield [
                    points[h + 0][w : (w + 4)],
                    points[h + 1][w : (w + 4)],
                    points[h + 2][w : (w + 4)],
                    points[h + 3][w : (w + 4)],
                ]
