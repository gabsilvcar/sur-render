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
def sutherland_hodgeman(points, window_min, window_max, closed=True):
    clipped = points
    clipped = cut_min_x(clipped, window_min.x, closed)
    clipped = cut_max_x(clipped, window_max.x, closed)
    clipped = cut_min_y(clipped, window_min.y, closed)
    clipped = cut_max_y(clipped, window_max.y, closed)
    return clipped
