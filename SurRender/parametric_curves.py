import numpy as np 


def bezier_matrix():
    matrix = np.array([
        [-1,  3, -3, 1],
        [ 3, -6,  3, 0],
        [-3,  3,  0, 0],
        [ 1,  0,  0, 0]])
    return matrix

def bezier(t, control_points):
    t = np.array([t*t*t, t*t, t, 1])
    matrix = bezier_matrix()

    px = [p.x for p in control_points]
    py = [p.y for p in control_points]
    pz = [p.z for p in control_points]

    x = t @ matrix @ px
    y = t @ matrix @ py
    z = t @ matrix @ pz

    return x, y, z