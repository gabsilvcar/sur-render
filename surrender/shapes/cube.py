from surrender.vector import Vector
from surrender.shapes.object_3d import Object3D


class Cube(Object3D):
    def __init__(self, name, pos, size, color=(0,0,0)):
        self.pos = pos
        self.size = size

        v0 = Vector(0,0,0) * size + pos
        v1 = Vector(0,0,1) * size + pos
        v2 = Vector(0,1,0) * size + pos
        v3 = Vector(0,1,1) * size + pos
        v4 = Vector(1,0,0) * size + pos
        v5 = Vector(1,0,1) * size + pos
        v6 = Vector(1,1,0) * size + pos
        v7 = Vector(1,1,1) * size + pos

        segments = [
            (v0, v1),
            (v0, v2),
            (v0, v4),
            (v1, v3),
            (v1, v5),
            (v2, v3),
            (v2, v6),
            (v3, v7),
            (v4, v5),
            (v4, v6),
            (v5, v7),
            (v6, v7),
        ]

        super().__init__(name, segments, color)
        self.type = 'Cube'
