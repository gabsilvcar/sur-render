import numpy as np
from copy import deepcopy
from surrender.math_transforms import (
    rotation_matrix_x,
    rotation_matrix_y,
    rotation_matrix_z,
    translation_matrix,
)


def _alignment_matrix(uv, nv):
    rx = nv.x_angle()
    nv.rotate_x(rx)
    uv.rotate_x(rx)

    ry = nv.y_angle() - np.pi / 2
    nv.rotate_y(ry)
    uv.rotate_y(ry)

    rz = uv.z_angle()

    mx = rotation_matrix_x(rx)
    my = rotation_matrix_y(ry)
    mz = rotation_matrix_z(rz)

    return mx @ my @ mz


def perspective_projection(vectors, window):
    if len(vectors) == 0:
        return

    cop = window.center_of_projection()
    uv = window.up_vector()
    nv = window.normal_vector()
    d = window.projection_distance

    translation = translation_matrix(-cop)
    rotation = _alignment_matrix(uv, nv)

    shape = (len(vectors), 4)
    positions = np.zeros(shape)

    for pos, vec in zip(positions, vectors):
        pos[:] = vec.x, vec.y, vec.z, 1

    result = positions @ translation @ rotation
    zd = result[:, 2] / d
    xs = result[:, 0] / zd
    ys = result[:, 1] / zd

    for i in range(len(vectors)):
        vectors[i].set_pos(xs[i], ys[i], 0)


def viewport_transform(vectors, source, target):
    source_delta = source.max() - source.min()
    target_delta = target.max() - target.min()

    x_factor = target_delta.x / source_delta.x
    y_factor = target_delta.y / source_delta.y

    source_min_x = source.min().x
    source_max_y = source.max().y

    for vector in vectors:
        vector.x = (vector.x - source_min_x) * x_factor
        vector.y = (source_max_y - vector.y) * y_factor
