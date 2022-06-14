from copy import deepcopy

from surrender.shapes.generic_shape import GenericShape


class Point(GenericShape):
    DO_NOT_CLIP = 0
    TRIVIAL = 1

    CLIPPING_ALGORITHM = TRIVIAL


    def __init__(self, name, pos, color=(0,0,0)):
        super().__init__(name, 'Point', color)
        self.pos = pos
    
    def points(self):
        return [self.pos]
        
    def clipped(self, window):
        if self.CLIPPING_ALGORITHM == self.DO_NOT_CLIP:
            return self
            
        inx = window.min().x <= self.pos.x <= window.max().x
        iny = window.min().y <= self.pos.y <= window.max().y   

        if inx and iny:
            return deepcopy(self)
        else:
            return None
