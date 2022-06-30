import numpy as np 

def delta_matrix(d):
    d2 = d*d
    d3 = d*d*d
    matrix = np.array([
        [   0,    0, 0, 1],
        [  d3,   d2, d, 0],
        [6*d3, 2*d2, 0, 0],
        [6*d3,    0, 0, 0]])
    return matrix

def bezier_matrix():
    matrix = np.array([
        [-1,  3, -3, 1],
        [ 3, -6,  3, 0],
        [-3,  3,  0, 0],
        [ 1,  0,  0, 0]])
    return matrix

def bspline_matrix():
    matrix = np.array([
        [-1,  3, -3, 1],
        [ 3, -6,  3, 0],
        [-3,  0,  3, 0],
        [ 1,  4,  1, 0]]) / 6
    return matrix

def bicubic_bezier(t, s, control_points):
    t = np.array([t*t*t, t*t, t, 1])
    s = np.array([s*s*s, s*s, s, 1])
    matrix = bezier_matrix()
    matrix_t = np.transpose(matrix)

    gx = []
    gy = []
    gz = []

    for line in control_points:
        px = [p.x for p in line]
        py = [p.y for p in line]
        pz = [p.z for p in line]
        gx.append(px)
        gy.append(py)
        gz.append(pz)

    x = s @ matrix @ gx @ matrix_t @ t
    y = s @ matrix @ gy @ matrix_t @ t
    z = s @ matrix @ gz @ matrix_t @ t

    return x, y, z

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

def bspline(control_points):
    t = np.array([t*t*t, t*t, t, 1])
    matrix = bspline_matrix()

    px = [p.x for p in control_points]
    py = [p.y for p in control_points]
    pz = [p.z for p in control_points]

    x = t @ matrix @ px
    y = t @ matrix @ py
    z = t @ matrix @ pz

    return x, y, z

def fd_bspline(control_points, n):
    E = delta_matrix(1/n)
    matrix = bspline_matrix()

    px = np.array([p.x for p in control_points])
    py = np.array([p.y for p in control_points])
    pz = np.array([p.z for p in control_points])

    cx = matrix @ px
    cy = matrix @ py
    cz = matrix @ pz

    x, dx, dx2, dx3 = E @ cx
    y, dy, dy2, dy3 = E @ cy
    z, dz, dz2, dz3 = E @ cz
    
    for x,y,z in foward_diff(n, x, y, z, dx, dy, dz, dx2, dy2, dz2, dx3, dy3, dz3):
        yield x, y, z

def foward_diff(n, x, y, z, dx, dy, dz, dx2, dy2, dz2, dx3, dy3, dz3):
    yield (x,y,z)

    for i in range(n):
        x = x + dx
        y = y + dy 
        z = z + dz

        dx = dx + dx2 
        dy = dy + dy2 
        dz = dz + dz2 

        dx2 = dx2 + dx3
        dy2 = dy2 + dy3
        dz2 = dz2 + dz3

        yield (x,y,z)