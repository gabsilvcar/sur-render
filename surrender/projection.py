import numpy as np
from copy import deepcopy
from numbers import Number

from surrender.vector import *
from surrender.math_transforms import *


def align_to_x(vector):
    vector = vector.normalized()
    mz = rotation_matrix_z(-np.arctan(vector.y / vector.x))
    vector.apply_transform(mz)
    my = rotation_matrix_y(np.arctan(vector.z / vector.x))
    return mz @ my

def align_to_y(vector):
    vector = vector.normalized()
    mx = rotation_matrix_x(-np.arctan(vector.z / vector.y))
    vector.apply_transform(mx)
    mz = rotation_matrix_z(np.arctan(vector.x / vector.y))
    return mx @ mz

def align_to_z(vector):
    vector = vector.normalized()
    my = rotation_matrix_y(-np.arctan(vector.x / vector.z))
    vector.apply_transform(my)
    mx = rotation_matrix_x(np.arctan(vector.y / vector.z))
    return my @ mx

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
    nv = window.normal_vector()
    uv = window.up_vector()

    align_normal = align_to_z(nv)
    z_angle = vector_z_angle(uv)

    for shape in shapes:
        shape = deepcopy(shape)
        shape.move(-wc)
        shape.apply_transform(align_normal)
        shape.rotate_z(z_angle)
        yield shape
