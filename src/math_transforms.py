from src.primitives import Vector

def viewport_transform(vector, win, vp):
    x = (vp.xmax - vp.xmin)
    x *= (vector.x - win.xmin)
    x /= (win.xmax - win.xmin)

    y = (vector.y - win.ymin) / (win.ymax - win.ymin)
    y *= (vp.ymax - vp.ymin)
    
    return Vector(x, y)