import numpy as np
from copy import deepcopy

from SurRender.vector import *
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
        return (self.p0 - self.p3).normalized()

    def right_vector(self):
        return (self.p1 - self.p0).normalized()
    
    def normal_vector(self):
        uv = self.up_vector()
        rv = self.right_vector()
        return -cross_product(uv, rv).normalized()

    def width(self):
        return (self.p1 - self.p0).length()

    def height(self):
        return (self.p0 - self.p3).length()
    
    def move(self, vector):
        uv = self.up_vector()
        nv = self.normal_vector()

        x = vector_x_angle(nv)
        y = vector_y_angle(nv) - np.pi / 2
        z = -vector_z_angle(uv)

        vector.rotate(x,y,z)
        super().move(vector)

    def zoom(self, amount, around=None):
        v = Vector(amount, amount)
        around = self.center()
        super().scale(v, around)
        
    def __str__(self):
        return f"View({self.min()} {self.max()})"
