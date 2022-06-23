from dataclasses import dataclass
import re
from surrender.vector import Vector


# line_regex = re.compile(r'([fplov][\s|\d|\w|.]*)\n')
line_regex = re.compile(r'[fplov]((\s*)|(\s[\d|\s|\w|.]*))')


@dataclass 
class Token:
    type : str
    args : str


class OBJParser:
    def encode_shapes(shapes):
        pass 

    def create_tokens(self, string):
        tokens = []
        for line in string.splitlines():
            if not line_regex.match(line):
                continue
            splitter = line.find(' ')
            if splitter == -1:
                token = Token(type = line.strip(),
                              args = '')
            else:
                token = Token(type = line[:splitter].strip(),
                              args = line[splitter:].strip())
            yield token
    
    def read_vertices(self, tokens):
        for token in tokens:
            if token.type == 'v':
                x, y, z = (float(i) for i in token.args.split())
                yield Vector(x,y,z)
    
    def parse_string(self, string):
        tokens = self.create_tokens(string)
        vertices = self.read_vertices(tokens)

        name = ''
        is_grouping = False
        current_group = []
        objects = []

        for token in tokens:
            if token.type == 'v':
                continue

            elif token.type == 'o':
                name = token.args
            
            elif token.type == 'g':
                name = token.args
                is_grouping = True
            
            elif token.type == 'end':
                name = ''
                is_grouping = False
                current_group = []
                return Object3DDescriptor(name, current_group, vertices)
            
            elif token.type == 'p':
                name = ''
                return PointDescriptor.parse_string(name, token.args, vertices)
            
            elif token.type == 'l':
                name = ''
                if len(token.args.split()) == 2:
                    return LineDescriptor.parse_string(name, token.args, vertices)
                else:
                    return PolygonDescriptor.parse_string(name, token.args, vertices)
            
            elif token.type == 'f':
                pass

            else:
                print(f'deu problema no {token}')
