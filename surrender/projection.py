import numpy as np
from copy import deepcopy
from numbers import Number
from surrender.vector import *
from surrender.math_transforms import *


def _alignment_matrix(uv, nv):
    rx = vector_x_angle(nv)
    nv.rotate_x(rx)
    uv.rotate_x(rx)

    ry = vector_y_angle(nv) - np.pi / 2
    nv.rotate_y(ry)
    uv.rotate_y(ry)

    rz = vector_z_angle(uv)

    mx = rotation_matrix_x(rx)
    my = rotation_matrix_y(ry)
    mz = rotation_matrix_z(rz)

    return mx @ my @ mz

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

def align_shapes_to_window(shapes, window):
    wc = window.center()
    alignment_matrix = _alignment_matrix(window.up_vector(), window.normal_vector())

    for shape in shapes:
        shape = deepcopy(shape)
        shape.move(-wc)
        shape.apply_transform(alignment_matrix)
        yield shape
