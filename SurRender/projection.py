import numpy as np
from copy import deepcopy

from SurRender.vector import Vector, vector_y_angle


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
    angle  = vector_y_angle(uv)

    for shape in shapes:
        shape = deepcopy(shape)
        shape.move(-wc)
        shape.rotate(angle)
        transformed.append(shape)

    return transformed
