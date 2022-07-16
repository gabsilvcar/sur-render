from surrender.shapes import Object3D
from surrender.utils import adjacents


class OBJ3DDescriptor:
    @classmethod
    def encode_shape(cls, shape, index=1):
        vertices = ""
        lines = ""

        i = index
        for a, b in shape.segments:
            vertices += f"v {a.x} {a.y} {a.z} \n"
            vertices += f"v {b.x} {b.y} {b.z} \n"
            lines += f"l {i} {i+1}"
            i += 2

        string = vertices
        string += f"o {shape.name} \n"
        string += lines
        return string

    @classmethod
    def parse_string(cls, name, tokens, vertices):
        segments = []
        factor = 100
        for token in tokens:
            if token.type == "l":
                points = [int(i) for i in token.args.split()]
                for a, b in adjacents(points):
                    segment = (vertices[a - 1] * factor, vertices[b - 1] * factor)
                    segments.append(segment)

            if token.type == "f":
                points = []
                for vargs in token.args.split():
                    splited = vargs.split("/")
                    points.append(int(splited[0]))

                for a, b in adjacents(points, circular=True):
                    segment = (vertices[a - 1] * factor, vertices[b - 1] * factor)
                    segments.append(segment)

        return Object3D(name, segments, color=(0, 100, 200))
