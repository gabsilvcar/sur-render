import numpy as np
from copy import deepcopy

from SurRender.vector import Vector, angle


def viewport_transform(vector, source, target):
    x = vector.x - source.min().x
    x /= source.max().x - source.min().x
    x *= target.max().x - target.min().x

    y = vector.y - source.min().y
    y /= source.max().y - source.min().y
    y = 1 - y
    y *= target.max().y - target.min().y

    vector.x = x
    vector.y = y
    return vector

def world_to_ppc(shapes, window):
    wc = window.center()
    uv = window.up_vector()

    transformed = []

    for shape in shapes:
        y  = Vector(0,1,0)
        a  = angle(uv, y) 

        shape = deepcopy(shape)
        shape.move(-wc)
        shape.rotate(a)
        transformed.append(shape)

    return transformed

def clip(shapes, window):
    clipped = []

    for shape in shapes:
        if window.surrounds(shape.center()):
            clipped.append(shape)

    return clipped