from surrender.io.obj_descriptors.obj_descriptor import OBJParser

data = '''
# OBJ file created by ply_to_obj.c
#
g Object001

v  0  0  0
v  1  0  0
v  1  1  0
v  0  1  0
v  0.5  0.5  1.6

f  5  2  3
f  4  5  3
f  6  3  2
f  5  6  2
f  4  6  5
f  6  4  3

'''
parser = OBJParser()
shape = parser.parse_string(data)
print(shape)
# tokens = parser.create_tokens(data)
# vertices = parser.read_vertices(tokens)