import numpy as np
from copy import deepcopy

from SurRender.vector import *


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
        yield shape
        transformed.append(shape)

    return transformed

def align_shapes_to_window(shapes, window):
    wc = window.center()
    uv = window.up_vector()
    nv = window.normal_vector()

    x_angle = vector_x_angle(uv)
    y_angle = vector_y_angle(uv)
    z_angle = vector_z_angle(uv)

    print(x_angle)
    print(y_angle)
    print(z_angle)

    for shape in shapes:
        shape = deepcopy(shape)
        shape.move(-wc)
        # shape.rotate_x(x_angle)
        # shape.rotate_y(y_angle)
        shape.rotate_z(-z_angle)
        yield shape
    # print(uv)
    # print(nv)
    # print()
    # return shapes