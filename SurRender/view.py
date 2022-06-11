import numpy as np
from copy import deepcopy

from SurRender.vector import Vector, vector_y_angle
from SurRender.shapes import Polygon

class View(Polygon):
    def __init__(self, p0, p1, p2, p3, border=0):
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
        super().__init__('', points, style=Polygon.CLOSED)

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
        return (self.p1 - self.p0).length()

    def height(self):
        return (self.p0 - self.p3).length()
    
    def move(self, vector):
        angle = vector_y_angle(self.up_vector())
        vector.rotate(-angle)
        super().move(vector)

    def zoom(self, amount, around=None):
        v = Vector(amount, amount)
        around = self.center()
        super().scale(v, around)
        
    def __str__(self):
        return f"View({self.min()} {self.max()})"
