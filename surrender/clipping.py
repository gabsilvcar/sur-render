from surrender.vector import Vector
from surrender.utils import adjacents

LEFT = int("0001", 2)
RIGHT = int("0010", 2)
BOTTOM = int("0100", 2)
UP = int("1000", 2)


def point_code(point, window_min, window_max):
    code = 0

    if point.y > window_max.y:
        code |= UP
    elif point.y < window_min.y:
        code |= BOTTOM

    if point.x > window_max.x:
        code |= RIGHT
    elif point.x < window_min.x:
        code |= LEFT

    return code


def cohen_sutherland(a, b, window_min, window_max):
    while True:
        code_a = point_code(a, window_min, window_max)
        code_b = point_code(b, window_min, window_max)

        inside_window = code_a == code_b == 0
        outside_window = code_a & code_b != 0

        if inside_window:
            return True

        if outside_window:
            return False

        if code_a == 0:
            a, b = b, a
            code_a, code_b = code_b, code_a

        dx = b.x - a.x
        dy = b.y - a.y

        if dx != 0:
            m = dy / dx

        if code_a & LEFT:
            a.y += m * (window_min.x - a.x)
            a.x = window_min.x

        elif code_a & RIGHT:
            a.y += m * (window_max.x - a.x)
            a.x = window_max.x

        elif code_a & BOTTOM:
            if b.x != a.x:
                a.x += (window_min.y - a.y) / m
            a.y = window_min.y

        elif code_a & UP:
            if b.x != a.x:
                a.x += (window_max.y - a.y) / m
            a.y = window_max.y


def liang_barsky(p0, p1, window):
    delta = p1 - p0

    p = [
        -delta.x,
        delta.x,
        -delta.y,
        delta.y,
    ]

    q = [
        p0.x - window.min().x,
        window.max().x - p0.x,
        p0.y - window.min().y,
        window.max().y - p0.y,
    ]

    for i in range(4):
        if p[i] == 0 and q[i] < 0:
            return None

    r = [(qk / pk if pk != 0 else 0) for qk, pk in zip(q, p)]

    u = [
        max(0, *[r[k] for k in range(4) if p[k] < 0]),
        min(1, *[r[k] for k in range(4) if p[k] > 0]),
    ]

    if u[0] > u[1]:
        return None

    points = []

    if u[0] == 0:
        points.append(p0)
    else:
        x = p0.x + delta.x * u[0]
        y = p0.y + delta.y * u[0]
        points.append(Vector(x, y))

    if u[1] == 1:
        points.append(p1)
    else:
        x = p0.x + delta.x * u[1]
        y = p0.y + delta.y * u[1]
        points.append(Vector(x, y))

    return points


def cut_min_x(points, minx, closed):
    points_with_intersection = []

    for p0, p1 in adjacents(points, closed):
        points_with_intersection.append(p0)
        if p0.x < minx < p1.x:
            delta = p1 - p0
            if delta.x != 0:
                m = delta.y / delta.x
                x = minx
                y = m * (x - p0.x) + p0.y
                points_with_intersection.append(Vector(x, y))

        elif p1.x < minx < p0.x:
            delta = p0 - p1
            if delta.x != 0:
                m = delta.y / delta.x
                x = minx
                y = m * (x - p1.x) + p1.y
                points_with_intersection.append(Vector(x, y))

    if not closed and points:
        points_with_intersection.append(points[-1])

    clipped = []

    for point in points_with_intersection:
        if point.x >= minx:
            clipped.append(point)

    return clipped


def cut_max_x(points, maxx, closed):
    points_with_intersection = []

    for p0, p1 in adjacents(points, closed):
        points_with_intersection.append(p0)

        if p0.x > maxx > p1.x:
            delta = p1 - p0
            if delta.x != 0:
                m = delta.y / delta.x
                x = maxx
                y = m * (x - p0.x) + p0.y
                points_with_intersection.append(Vector(x, y))

        elif p1.x > maxx > p0.x:
            delta = p0 - p1
            if delta.x != 0:
                m = delta.y / delta.x
                x = maxx
                y = m * (x - p1.x) + p1.y
            points_with_intersection.append(Vector(x, y))

    if not closed and points:
        points_with_intersection.append(points[-1])

    clipped = []

    for point in points_with_intersection:
        if point.x <= maxx:
            clipped.append(point)

    return clipped


def cut_min_y(points, miny, closed):
    points_with_intersection = []

    for p0, p1 in adjacents(points, closed):
        points_with_intersection.append(p0)

        if p0.y < miny < p1.y:
            delta = p1 - p0
            if delta.x == 0:
                y = miny
                x = p0.x
            else:
                m = delta.y / delta.x
                y = miny
                x = p0.x + (y - p0.y) / m
            points_with_intersection.append(Vector(x, y))

        elif p1.y < miny < p0.y:
            delta = p0 - p1
            if delta.x == 0:
                y = miny
                x = p1.x
            else:
                m = delta.y / delta.x
                y = miny
                x = p1.x + (y - p1.y) / m
            points_with_intersection.append(Vector(x, y))

    if not closed and points:
        points_with_intersection.append(points[-1])

    clipped = []

    for point in points_with_intersection:
        if point.y >= miny:
            clipped.append(point)

    return clipped


def cut_max_y(points, maxy, closed):
    points_with_intersection = []

    for p0, p1 in adjacents(points, closed):
        points_with_intersection.append(p0)

        if p0.y > maxy > p1.y:
            delta = p1 - p0
            if delta.x == 0:
                y = maxy
                x = p0.x
            else:
                m = delta.y / delta.x
                y = maxy
                x = p0.x + (y - p0.y) / m
            points_with_intersection.append(Vector(x, y))

        elif p1.y > maxy > p0.y:
            delta = p0 - p1
            if delta.x == 0:
                y = maxy
                x = p1.x
            else:
                m = delta.y / delta.x
                y = maxy
                x = p1.x + (y - p1.y) / m
            points_with_intersection.append(Vector(x, y))

    if not closed and points:
        points_with_intersection.append(points[-1])

    clipped = []

    for point in points_with_intersection:
        if point.y <= maxy:
            clipped.append(point)

    return clipped


# POLYGON ALGORITHMS
def sutherland_hodgeman(points, window, closed=True):
    clipped = points
    clipped = cut_min_x(clipped, window.min().x, closed)
    clipped = cut_max_x(clipped, window.max().x, closed)
    clipped = cut_min_y(clipped, window.min().y, closed)
    clipped = cut_max_y(clipped, window.max().y, closed)
    return clipped
