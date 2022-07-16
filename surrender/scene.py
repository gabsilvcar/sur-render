from surrender.projection import (
    faster_perspective_projection,
    faster_transform_viewport,
)


class Scene:
    def __init__(self):
        self.shapes = []
        self.gliphs = []
        self.window = None

    def projected_shapes(self, origin, target):
        shapes = [shape.copy() for shape in self.shapes]

        faster_perspective_projection(shapes, origin)
        faster_transform_viewport(shapes, origin.ppc(), target)

        clipped_shapes = []
        for shape in shapes:
            clipped = shape.clipped(target)
            if clipped is not None:
                clipped_shapes.append(clipped)
        shapes = clipped_shapes

        return shapes

    def get_gliphs(self, target):
        return self.gliphs

    def add_shape(self, shape):
        if shape is None:
            return
        self.shapes.append(shape)
