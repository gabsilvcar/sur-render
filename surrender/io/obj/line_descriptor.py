from surrender.shapes import Line 


class LineDescriptor:
    @classmethod
    def encode_shape(cls, shape, index=1):
        string  = f'v {shape.end.x} {shape.end.y} {shape.end.z} \n'
        string += f'v {shape.start.x} {shape.start.y} {shape.start.z} \n'
        string += f'o {shape.name} \n'
        string += f'l {index} {index+1} \n'
        return string

    @classmethod
    def parse_string(cls, name, string, vertices):
        pos = vertices[int(string) + 1]
        return Point(name, pos)