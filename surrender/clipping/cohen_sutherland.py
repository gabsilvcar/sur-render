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
