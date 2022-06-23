vertex_encoding = 'v {} {} {} \n'
name_encoding = 'o {} \n'
point_encoding = 'p {} \n'

class PointDescriptor:
    def encode_shape(shape, index=1):
        string  = vertex_encoding.format(shape.pos.x, shape.pos.y, shape.pos.z)
        string += name_encoding.format(shape.name)
        string += point_encoding.format(index)
        return string

    def parse_string(name, string, vertexes):
        return Point()