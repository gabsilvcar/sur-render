def liang_barsky(a, b, window_min, window_max):
    dx = b.x - a.x
    dy = b.y - a.y

    p = (-dx, dx, -dy, dy)

    q = (
        a.x - window_min.x,
        window_max.x - a.x,
        a.y - window_min.y,
        window_max.y - a.y,
    )

    u0 = 0
    u1 = 1

    for k in range(4):
        pk = p[k]

        if pk < 0:
            r = q[k] / pk

            if r > u0:
                u0 = r

        elif pk > 0:
            r = q[k] / pk

            if r < u1:
                u1 = r

        elif pk == 0 and q[k] < 0:
            return False

    if u0 > u1:
        return False

    if u1 != 1:
        b.x = a.x + dx * u1
        b.y = a.y + dy * u1

    if u0 != 0:
        a.x += dx * u0
        a.y += dy * u0

    return True
