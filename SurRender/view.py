from SurRender.math_transforms import translation_matrix, scale_matrix, rotation_matrix
from SurRender.vector import Vector, angle
from SurRender.shapes import Polygon


class View(Polygon):
    def __init__(self, p0, p1, p2, p3):
        '''
        p0 ------ p1 
        |          |
        |          |
        |          |
        p3 ------ p2 
        '''

        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        points = [self.p0, self.p1, self.p2, self.p3]
        super().__init__('', points)

    def ppc(self):
        w = self.width()
        h = self.height()
        v = Vector(-w/2, -h/2)

        ppc = View(
            Vector(0, h),
            Vector(w, h),
            Vector(w, 0),
            Vector(0,0), 
        )

        ppc.move(v)
        return ppc

    def min(self):
        return self.p3
    
    def max(self):
        return self.p1

    def up_vector(self):
        return self.p0 - self.p3

    def width(self):
        return (self.p1 - self.p0).size()

    def height(self):
        return (self.p0 - self.p3).size()
        
    def zoom(self, amount, around=None):
        v = Vector(amount, amount)
        around = self.center()
        super().scale(v, around)

    def rotate(self, angle):
        around = self.center()
        super().rotate(angle, around)
        
    def __str__(self):
        return f"View({self.min()} {self.max()})"
