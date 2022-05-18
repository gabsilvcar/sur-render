from SurRender.math_transforms import translation_matrix, scale_matrix, rotation_matrix
from SurRender.vector import Vector, angle


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
    
    def ppc(self):
        w = self.width()
        h = self.height()
        v = Vector(-w/2, -h/2)

        ppc = View(
            Vector(0, h),
            Vector(w, h),
            Vector(0,0), 
            Vector(w, 0)
        )

        ppc.move(v)
        return ppc

    def min(self):
        return self.p2
    
    def max(self):
        return self.p1

    def up_vector(self):
        return self.p0 - self.p2

    def width(self):
        return (self.p1 - self.p0).size()

    def height(self):
        return (self.p0 - self.p2).size()
    
    def center(self):
        return (self.p0 + self.p1 + self.p2 + self.p3) / 4

    def move(self, delta):
        around = self.center()
        a = angle(self.up_vector(), Vector(0,1,0))
        delta.rotate(-a)
        
        matrix = translation_matrix(delta)

        self.p0 @= matrix
        self.p1 @= matrix
        self.p2 @= matrix
        self.p3 @= matrix
        
    def zoom(self, amount, around=None):
        around = self.center()
        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        s = scale_matrix(Vector(amount, amount))
        matrix = t0 @ s @ t1

        self.p0 @= matrix
        self.p1 @= matrix
        self.p2 @= matrix
        self.p3 @= matrix

    def rotate(self, angle):
        around = self.center()
        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix(angle)
        matrix = t0 @ r @ t1

        self.p0 @= matrix
        self.p1 @= matrix
        self.p2 @= matrix
        self.p3 @= matrix
        
    def __str__(self):
        return f"View({self.min} {self.max})"
