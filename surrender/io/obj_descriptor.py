from surrender.shapes import Line, Point, Polygon


class OBJDescriptor:
    def __init__(self, shape):
        self.obj_type = self.figure_out_type(shape)

    def shape(self):
        return self.obj_type.shape

    def figure_out_type(self, shape):
        if isinstance(shape, Point):
            return PointDescriptor(shape)
        elif isinstance(shape, Line):
            return LineDescriptor(shape)
        elif isinstance(shape, Polygon):
            return PolygonDescriptor(shape)
        else:
            return None

    def generate(self, index=0):
        if self.obj_type is None:
            return ""
        return self.obj_type.generate(index)


class PointDescriptor:
    def __init__(self, shape):
        self.shape = shape

    def generate(self, index=1):
        p = self.shape.pos
        string = f"v {p.x} {p.y} {p.z} \n"
        string += f"o {self.shape.name} \n"
        string += f"p {index} \n"
        return string


class LineDescriptor:
    def __init__(self, shape):
        self.shape = shape

    def generate(self, index=1):
        s = self.shape.start
        e = self.shape.end
        string = f"v {e.x} {e.y} {e.z} \n"
        string += f"v {s.x} {s.y} {s.z} \n"
        string += f"o {self.shape.name} \n"
        string += f"l {index} {index+1} \n"
        return string


class PolygonDescriptor:
    def __init__(self, shape):
        self.shape = shape

    def generate(self, index=1):
        points = self.shape.points()
        string = ""

        for p in points:
            string += f"v {p.x} {p.y} {p.z} \n"

        string += f"o {self.shape.name} \n"
        string += "l "
        string += "".join(f"{p + index} " for p in range(len(points)))
        string += f"{index} \n"

        return string
