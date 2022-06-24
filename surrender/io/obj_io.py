from surrender.io.obj.obj_parser import OBJParser


class OBJIO:
    @classmethod
    def read(cls, path):
        with open(path, 'r') as file:
            data = file.read()
        return cls.load(data)
        
    @classmethod
    def write(cls, shapes, path):
        data = cls.dump(shapes)
        with open(path, 'w') as file:
            file.write(data)
    
    @classmethod
    def load(cls, string):
        return OBJParser.parse_string(string)
    
    @classmethod
    def dump(cls, shapes):
        return OBJParser.encode_shapes(shapes)
