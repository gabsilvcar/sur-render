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

def cohen_sutherland(segment, window):
    rc_start = point_code(segment.start, window)
    rc_end   = point_code(segment.end, window)

    inside_window = (rc_start == rc_end == 0)
    outside_window = (rc_start & rc_end != 0)

    if inside_window:
        return segment

    if outside_window:
        return None

    # else if crossing window:

    m = (segment.end.y - segment.start.y) / (segment.end.x - segment.start.x)

    left  = Vector(0,0)
    right = Vector(0,0)
    up    = Vector(0,0)
    down  = Vector(0,0)

    x = window.min().x
    y = m * (x - segment.start.x) + segment.start.y 
    left = Vector(x, y)

    x = window.max().x
    y = m * (x - segment.start.x) + segment.start.y 
    right = Vector(x, y)

    y = window.max().y
    x = segment.start.x + (y - segment.start.y) / m
    up = Vector(x, y)

    y = window.min().y
    x = segment.start.x + (y - segment.start.y) / m
    down = Vector(x, y)

    return (left, right, up, down)


def clip(shapes, window):
    clipped = []
    for line in shapes:
        s = cohen_sutherland(line, window)
        if s is not None:
            clipped.append(s)
        print()
        # print(point_code(line.start, window))
        # print(point_code(line.end, window))
    print('lines inside window:', len(clipped))
    return shapes