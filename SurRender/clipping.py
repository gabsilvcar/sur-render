from SurRender.vector import Vector
from SurRender.utils import adjacents

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

def cohen_sutherland(p0, p1, window):
    rc_start = point_code(p0, window)
    rc_end   = point_code(p1, window)

    inside_window = (rc_start == rc_end == 0)
    outside_window = (rc_start & rc_end != 0)

    if inside_window:
        return (p0, p1)

    if outside_window:
        return None     

    dx = p1.x - p0.x
    dy = p1.y - p0.y

    if dx:
        m = dy / dx
    else:
        m = 0
        
    x = window.min().x
    y = m * (x - p0.x) + p0.y 
    left = Vector(x, y)

    x = window.max().x
    y = m * (x - p0.x) + p0.y 
    right = Vector(x, y)

    if m == 0:
        y = window.max().y
        x = p1.x
        up = Vector(x, y)

        y = window.min().y
        x = p0.x
        down = Vector(x, y)
    else:
        y = window.max().y
        x = p0.x + (y - p0.y) / m
        up = Vector(x, y)

        y = window.min().y
        x = p0.x + (y - p0.y) / m
        down = Vector(x, y)

    if rc_start == 0:
        other = point_code(p1, window)

        if (other & LEFT) and point_code(left, window) == 0:
             return [p0, left]

        if (other & RIGHT) and point_code(right, window) == 0:
             return [p0, right]

        if (other & UP) and point_code(up, window) == 0:
             return [p0, up]

        if (other & BOTTOM) and point_code(down, window) == 0:
            return [p0, down]
    elif rc_end == 0:
        other = point_code(p0, window)

        if (other & LEFT) and point_code(left, window) == 0:
             return [p1, left]

        if (other & RIGHT) and point_code(right, window) == 0:
             return [p1, right]

        if (other & UP) and point_code(up, window) == 0:
             return [p1, up]

        if (other & BOTTOM) and point_code(down, window) == 0:
            return [p1, down]

    to_test = [left, right, up, down]
    avaliable = []

    for p in to_test:
        if point_code(p, window) == 0:
            avaliable.append(p)
        if len(avaliable) == 2:
            return tuple(avaliable)
    else:
        return None

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
        points.append(Vector(x,y))

    if u[1] == 1:
        points.append(p1)
    else:
        x = p0.x + delta.x * u[1]
        y = p0.y + delta.y * u[1]
        points.append(Vector(x,y))
    
    return points

def cut_min_x(points, minx):
    points_with_intersection = []

    for p0, p1 in adjacents(points, True):
        if p0.x < minx < p1.x:
            delta = p1 - p0
            if delta.x == 0:
                continue
            m = delta.y / delta.x
            x = minx 
            y = m * (x - p0.x) + p0.y
            points_with_intersection.append(Vector(x,y))

        elif p1.x < minx < p0.x:
            delta = p0 - p1
            if delta.x == 0:
                continue
            m = delta.y / delta.x
            x = minx 
            y = m * (x - p1.x) + p1.y
            points_with_intersection.append(Vector(x,y))
        
        points_with_intersection.append(p1)

    clipped = []

    for point in points_with_intersection:
        if point.x >= minx:
            clipped.append(point)

    return clipped

def cut_max_x(points, maxx):
    points_with_intersection = []

    for p0, p1 in adjacents(points, True):
        if p0.x > maxx > p1.x:
            delta = p1 - p0
            if delta.x == 0:
                continue
            m = delta.y / delta.x
            x = maxx 
            y = m * (x - p0.x) + p0.y
            points_with_intersection.append(Vector(x,y))

        elif p1.x > maxx > p0.x:
            delta = p0 - p1
            if delta.x == 0:
                continue
            m = delta.y / delta.x
            x = maxx 
            y = m * (x - p1.x) + p1.y
            points_with_intersection.append(Vector(x,y))
        
        points_with_intersection.append(p1)
        
    clipped = []

    for point in points_with_intersection:
        if point.x <= maxx:
            clipped.append(point)

    return clipped

def cut_min_y(points, miny):
    points_with_intersection = []

    for p0, p1 in adjacents(points, True):
        if p0.y < miny < p1.y:
            delta = p1 - p0
            if delta.x == 0:
                y = miny
                x = p0.x 
            else:
                m = delta.y / delta.x
                y = miny
                x = p0.x + (y - p0.y) / m
            points_with_intersection.append(Vector(x,y))

        elif p1.y < miny < p0.y:
            delta = p0 - p1
            if delta.x == 0:
                y = miny
                x = p1.x
            else: 
                m = delta.y / delta.x
                y = miny
                x = p1.x + (y - p1.y) / m
            points_with_intersection.append(Vector(x,y))
        
        points_with_intersection.append(p1)

    clipped = []

    for point in points_with_intersection:
        if point.y >= miny:
            clipped.append(point)

    return clipped

def cut_max_y(points, maxy):
    points_with_intersection = []

    for p0, p1 in adjacents(points, True):
        if p0.y > maxy > p1.y:
            delta = p1 - p0
            if delta.x == 0:
                y = maxy
                x = p0.x 
            else:
                m = delta.y / delta.x
                y = maxy
                x = p0.x + (y - p0.y) / m
            points_with_intersection.append(Vector(x,y))

        elif p1.y > maxy > p0.y:
            delta = p0 - p1
            if delta.x == 0:
                y = maxy
                x = p1.x
            else: 
                m = delta.y / delta.x
                y = maxy
                x = p1.x + (y - p1.y) / m
            points_with_intersection.append(Vector(x,y))
        
        points_with_intersection.append(p1)

    clipped = []

    for point in points_with_intersection:
        if point.y <= maxy:
            clipped.append(point)

    return clipped

# POLYGON ALGORITHMS 
def sutherland_hodgeman(points, window):
    clipped = points
    clipped = cut_min_x(clipped, window.min().x)
    clipped = cut_max_x(clipped, window.max().x)
    clipped = cut_min_y(clipped, window.min().y)
    clipped = cut_max_y(clipped, window.max().y)
    return clipped
