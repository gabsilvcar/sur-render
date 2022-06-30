from surrender.shapes import Object3D, Polygon
from surrender.shapes.generic_curve import GenericCurve
from surrender.parametric_curves import bicubic_bezier
from surrender.vector import Vector


class BicubicBezier(Object3D):
    def __init__(self, name, control_points, color=(0,0,0)):
        self.control_points = control_points
        segments = self.generate_segments(control_points, 20)
        
        super().__init__(name, segments, color)
        self.type = 'Bezier'

    def copy(self):
        new_control_points = []

        for line in self.control_points:
            new_line = []
            for p in line:
                new_line.append(p.copy())
            new_control_points.append(new_line)
        
        new_segments = [(a.copy(), b.copy()) for a,b in self.segments]
        c = self.__class__(self.name, new_control_points, self.color)
        # c.control_points = new_control_points
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
                    xyz_a = bicubic_bezier(i/resolution, j/resolution, points)
                    xyz_b = bicubic_bezier(i/resolution, (j+1)/resolution, points)
                    xyz_c = bicubic_bezier((i+1)/resolution, j/resolution, points)

                    a = Vector(*xyz_a)
                    b = Vector(*xyz_b)
                    c = Vector(*xyz_c)

                    segments.append((a,b))
                    segments.append((a,c))

        return segments

    def packs_of_points(self, points):
        last_point = None
        
        height = len(points) - 1
        width = len(points[0]) - 1

        for h in range(0, height, 3):
            for w in range(0, width, 3):
                yield [
                    points[h+0][w:(w+4)],
                    points[h+1][w:(w+4)],
                    points[h+2][w:(w+4)],
                    points[h+3][w:(w+4)],
                ]
