from copy import deepcopy
from surrender.shapes import Polygon
from surrender.vector import Vector


class PolygonDescriptor:
    @classmethod
    def encode_shape(cls, shape, index=1):
        string = ''
        for p in shape.points():
            string += f'v {p.x} {p.y} {p.z} \n'
        
        string += f'o {shape.name} \n'

        n = len(shape.points())
        indexes = ' '.join(str(i + index) for i in range(n))
        string += f'f {indexes} \n'
        return string

    @classmethod
    def parse_string(cls, name, string, vertices):
        params = string.split()
        indexes = []
        for p in params:
            splitted = [s.strip() for s in p.split('/')]
            indexes.append(int(splitted[0]))
        factor = 100
        vertices_used = [vertices[i-1] * factor for i in indexes]
        return Polygon(name, vertices_used)