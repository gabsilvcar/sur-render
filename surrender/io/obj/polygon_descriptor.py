from copy import deepcopy
from surrender.shapes import Polygon
from surrender.vector import Vector


class PolygonDescriptor:
    @classmethod
    def encode_shape(cls, shape, index=1):
        string = ''
        # string  = f'v {shape.end.x} {shape.end.y} {shape.end.z} \n'
        # string += f'v {shape.start.x} {shape.start.y} {shape.start.z} \n'
        # string += f'o {shape.name} \n'
        # string += f'l {index} {index+1} \n'
        return string

    @classmethod
    def parse_string(cls, name, string, vertices):
        params = string.split()
        indexes = []
        for p in params:
            splitted = [s.strip() for s in p.split('/')]
            indexes.append(int(splitted[0]))

        # indexes = [int(i) for i in string.split()]
        factor = 100
        vertices_used = [vertices[i-1] * factor for i in indexes]
        return Polygon(name, vertices_used, (0,100,255))