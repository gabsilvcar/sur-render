from SurRender.vector import Vector

LEFT   = int('0001', 2)
RIGHT  = int('0010', 2)
BOTTOM = int('0100', 2)
UP     = int('1000', 2)


def point_code(point, window):
    code = 0

    if point.y > window.max().y:
        code |= UP
    elif point.y < window.min().y:
        code |= BOTTOM

    if point.x > window.max().x:
        code |= RIGHT
    elif point.x < window.min().x:
        code |= LEFT

    return code

def cohen_sutherland(points, window):
    rc_start = point_code(points[0], window)
    rc_end   = point_code(points[1], window)

    inside_window = (rc_start == rc_end == 0)
    outside_window = (rc_start & rc_end != 0)

    if inside_window:
        return points

    if outside_window:
        return None     

    m = (points[1].y - points[0].y) / (points[1].x - points[0].x)

    x = window.min().x
    y = m * (x - points[0].x) + points[0].y 
    left = Vector(x, y)

    x = window.max().x
    y = m * (x - points[0].x) + points[0].y 
    right = Vector(x, y)

    y = window.max().y
    x = points[0].x + (y - points[0].y) / m
    up = Vector(x, y)

    y = window.min().y
    x = points[0].x + (y - points[0].y) / m
    down = Vector(x, y)

    if rc_start == 0:
        other = point_code(points[1], window)

        if (other & LEFT) and point_code(left, window) == 0:
             return [points[0], left]

        if (other & RIGHT) and point_code(right, window) == 0:
             return [points[0], right]

        if (other & UP) and point_code(up, window) == 0:
             return [points[0], up]

        if (other & BOTTOM) and point_code(down, window) == 0:
            return [points[0], down]
    elif rc_end == 0:
        other = point_code(points[0], window)

        if (other & LEFT) and point_code(left, window) == 0:
             return [points[1], left]

        if (other & RIGHT) and point_code(right, window) == 0:
             return [points[1], right]

        if (other & UP) and point_code(up, window) == 0:
             return [points[1], up]

        if (other & BOTTOM) and point_code(down, window) == 0:
            return [points[1], down]


    to_test = [left, right, up, down]
    avaliable = []

    for p in to_test:
        if point_code(p, window) == 0:
            avaliable.append(p)
        if len(avaliable) == 2:
            return avaliable
    else:
        return None
