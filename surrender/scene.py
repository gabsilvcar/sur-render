from surrender.projection import (
    perspective_projection,
    viewport_transform,
)


class Scene:
    def __init__(self):
        self.shapes = []
        self.gliphs = []
        self._shape_vectors_cache = []

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)
        self._shape_vectors_cache = self._get_shapes_vectors(self.shapes)

    def remove_shape(self, shape):
        try:
            i = self.shapes.index(shape)
        finally:
            self.shapes.pop(i)
            self._shape_vectors_cache = self._get_shapes_vectors(self.shapes)

    def projected_shapes(self, origin, target):    
        shapes = self.shapes

        for shape in shapes:
            shape.revert_projection()

        vectors = self._shape_vectors_cache
        perspective_projection(vectors, origin)
        viewport_transform(vectors, origin.ppc(), target)
        return self._clip_shapes(shapes, target)

    def _clip_shapes(self, shapes, window):
        window_min = window.min()
        window_max = window.max()

        clipped_shapes = []
        for shape in shapes:
            if shape.clip(window_min, window_max):
                clipped_shapes.append(shape)
        return clipped_shapes

    def _get_shapes_vectors(self, shapes):
        vectors = []
        for shape in shapes:
            for point in shape.projection_points():
                vectors.append(point)
        print('Num vertices: ', len(vectors))
        return vectors

    def get_gliphs(self, target):
        return self.gliphs
