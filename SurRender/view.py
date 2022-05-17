from SurRender.math_transforms import translation_matrix, scale_matrix, rotation_matrix
from SurRender.vector import Vector


class View:
    def __init__(self, p0, p1, p2, p3):
        '''
        p0 ------ p1 
        |          |
        |          |
        |          |
        p2 ------ p3 
        '''

        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def min(self):
        return self.p2
    
    def max(self):
        return self.p1

    def up_vector(self):
        return self.p0 - self.p2

    def width(self):
        return (self.max() - self.min()).x.size()

    def height(self):
        return (self.max() - self.min()).y.size()

    def move(self, delta):
        matrix = translation_matrix(delta)

        self.p0 @= matrix
        self.p1 @= matrix
        self.p2 @= matrix
        self.p3 @= matrix
    
    def middle(self):
        return (self.p0 + self.p1 + self.p2 + self.p3) / 4
    
    def zoom(self, amount, around=None):
        if around is None:
            around = Vector(100, 100)

        matrix = scale_matrix(Vector(amount, amount))

        self.p0 @= matrix
        self.p1 @= matrix
        self.p2 @= matrix
        self.p3 @= matrix

    def rotate(self, angle):
        around = self.middle()

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix(angle)
        matrix = t0 @ r @ t1

        points = [self.p0, self.p1, self.p2, self.p3]
        for p in points:
            p @= matrix

        
    def __str__(self):
        return f"View({self.min} {self.max})"
