import numpy as np

def translation_matrix(delta):
    matrix = np.identity(4)
    matrix[3, 0] = delta.x
    matrix[3, 1] = delta.y
    matrix[3, 2] = delta.z
    return matrix 

def scale_matrix(delta):
    matrix = np.identity(4)
    matrix[0,0] = delta.x
    matrix[1,1] = delta.y
    matrix[2,2] = delta.z
    return matrix

def rotation_matrix_x(angle):
    matrix = np.identity(4)
    matrix[1,1] = np.cos(angle)
    matrix[1,2] = np.sin(angle)
    matrix[2,1] = -np.sin(angle)
    matrix[2,2] = np.cos(angle)
    return matrix

def rotation_matrix_y(angle):
    matrix = np.identity(4)
    matrix[0,0] = np.cos(angle)
    matrix[0,2] = -np.sin(angle)
    matrix[2,0] = np.sin(angle)
    matrix[2,2] = np.cos(angle)
    return matrix

def rotation_matrix_z(angle):
    matrix = np.identity(4)
    matrix[0,0] = np.cos(angle)
    matrix[0,1] = np.sin(angle)
    matrix[1,0] = -np.sin(angle)
    matrix[1,1] = np.cos(angle)
    return matrix

def rotation_matrix(delta):
    rx = rotation_matrix_x(delta.x)
    ry = rotation_matrix_y(delta.y)
    rz = rotation_matrix_z(delta.z)
    matrix = rx @ ry @ rz
    return matrix
