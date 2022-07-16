from surrender.shapes import Point


class PointDescriptor:
    @classmethod
    def encode_shape(cls, shape, index=1):
        string = f"v {shape.pos.x} {shape.pos.y} {shape.pos.z} \n"
        string += f"o {shape.name} \n"
        string += f"p {index} \n"
        return string

    @classmethod
    def parse_string(cls, name, string, vertices):
        pos = vertices[int(string) - 1]
        return Point(name, pos)
