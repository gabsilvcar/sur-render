from src.primitives import Vector

def viewport_transform(vector, source, destiny):
    x = (destiny.xmax - destiny.xmin)
    x *= (vector.x - source.xmin)
    x /= (source.xmax - source.xmin)

    y = (vector.y - source.ymin) / (source.ymax - source.ymin)
    y *= (destiny.ymax - destiny.ymin)
    
    return Vector(x, y)