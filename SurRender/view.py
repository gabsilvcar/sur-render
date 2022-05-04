from SurRender.math_transforms import translation_matrix, scale_matrix, rotation_matrix
from SurRender.vector import Vector


class View:
    def __init__(self, start, end):
        self.min = start
        self.max = end

    def width(self):
        return (end - start).x

    def height(self):
        return (end - start).y

    def move(self, delta):
        matrix = translation_matrix(delta)
        self.min @= matrix
        self.max @= matrix
    
    def middle(self):
        return (self.min + self.max) / 2
    
    def zoom(self, amount, around=None):
        if around is None:
            around = Vector(100, 100)

        matrix = scale_matrix(Vector(amount, amount))

        self.min @= matrix
        self.max @= matrix
        
    def __str__(self):
        return f"View({self.min} {self.max})"
