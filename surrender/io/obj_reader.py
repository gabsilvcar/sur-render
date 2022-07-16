# copia o arquivo ignorando comentários
# cria todos os vértices necessários
# agrupa os 


class OBJReader:
    def __init__(self):
        self.shapes = []

    def read(self, path):
        is_empty = lambda line: line.strip() == ''
        is_comment = lambda line: line.strip()[0] == '#'

        usefull_lines = []
        with open(path, 'r') as file:
            for line in file.readlines():
                if is_empty(line) or is_comment(line):
                    continue
                usefull_lines.append(line)
        
        name = ''
        groups = []
        for line in usefull_lines:
            token, *args = (L.strip() for L in line.split())
            print(f'[{token.capitalize()}]({args})')


    # def read(self):
    #     vertices = []
    #     strings = []
    #     shapes = []
        
    #     with open(path, 'w') as file:
    #         for line in file.readlines():

    #             if token == 'v':
    #                 xyz = (int(i) for i in args)
    #                 v = Vector(*xyz)
    #                 vertices.append(v)

    #             elif token == '#':
    #                 pass

    #             elif line.strip() != '':
    #                 strings.append(line)

    #     name = ''
    #     for line in strings:
    #         token, *args = line.split()

    #         if token == 'o':
    #             name = ' '.join(args)
    #             continue
    #         else:
    #             name = ''

    #         if token == 'p':
    #             index = int(args[0])
    #             v = vertices[index]
    #             s = Point(name=name, pos=v)

    #         elif token == 'l' and len(args) == 2:
    #             pts = [int(i) for i in args]
    #             s = Line(name=name, start=pts[0], end=pts[1])
            
    #         elif token == 'l' and len(args) > 2:
    #             pts = [int(i) for i in args]
    #             s = Polygon(name=name, points=pts)
            
    #         else:
    #             continue
            
    #         shapes.append(s)

    #     return shapes