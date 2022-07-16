from surrender.shapes import Object3D
from surrender.parametric_curves import fd_bicubic_bspline
from surrender.vector import Vector


class BicubicBspline(Object3D):
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
        last_vectors = []
        first_vectors = []

        for points in self.packs_of_points(control_points):
            last_line = None
            for current_line in fd_bicubic_bspline(points, 10):
                # connects points between cols
                xyz_a = current_line[0]
                for xyz_b in current_line[1:]:
                    a = Vector(*xyz_a)
                    b = Vector(*xyz_b)
                    segments.append((a, b))
                    xyz_a = xyz_b

                xyz_a = current_line[0]
                xyz_b = current_line[-1]
                first_vectors.append(Vector(*xyz_a))
                last_vectors.append(Vector(*xyz_b))

                # connects point between lines
                if last_line is not None:
                    for xyz_a, xyz_b in zip(last_line, current_line):
                        a = Vector(*xyz_a)
                        b = Vector(*xyz_b)
                        segments.append((a, b))

                last_line = current_line

        return segments

    def packs_of_points(self, points):
        if not points:
            return

        height = len(points)
        width = len(points[0])

        for h in range(height - 3):
            for w in range(width - 3):
                yield [
                    points[h + 0][w : (w + 4)],
                    points[h + 1][w : (w + 4)],
                    points[h + 2][w : (w + 4)],
                    points[h + 3][w : (w + 4)],
                ]
