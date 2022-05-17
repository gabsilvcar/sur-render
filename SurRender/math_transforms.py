import numpy as np
from SurRender.vector import Vector

def viewport_transform(vector, source, target):
    x = vector.x - source.min().x
    x /= source.max().x - source.min().x
    x *= target.max().x - target.min().x

    y = vector.y - source.min().y
    y /= source.max().y - source.min().y
    y = 1 - y
    y *= target.max().y - target.min().y

    return Vector(x, y)

def translation_matrix(delta):
    matrix = np.identity(3)
    matrix[2,0] = delta.x
    matrix[2,1] = delta.y
    return matrix

def scale_matrix(delta):
    matrix = np.identity(3)
    matrix[0,0] = delta.x
    matrix[1,1] = delta.y
    return matrix

def rotation_matrix(angle):
    matrix = np.identity(3)
    matrix[0,0] = np.cos(angle)
    matrix[0,1] = -np.sin(angle)
    matrix[1,0] = np.sin(angle)
    matrix[1,1] = np.cos(angle)
    return matrix