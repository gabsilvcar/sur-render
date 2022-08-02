from surrender.shapes.generic_shape import GenericShape
from surrender.shapes import Line
from surrender.clipping import cohen_sutherland, liang_barsky
from surrender.vector import Vector


class Object3D(GenericShape):
    def __init__(self, name, segments, color=(0, 0, 0)):
        super().__init__(name, "Object3D", color)
        self._structural_segments = list()
        self._projection_segments = list()

        self._clipped_segments = list()
        self._structural_points = list()
        self._projection_points = list()

        self.set_segments(segments)

    def structural_points(self):
        return self._structural_points

    def projection_points(self):
        return self._projection_points

    def clipped_points(self):
        return []

    def structural_segments(self):
        return self._structural_segments

    def projection_segments(self):
        return self._projection_segments

    def clipped_segments(self):
        return self._clipped_segments

    def copy(self):
        new_segments = [(a.copy(), b.copy()) for a, b in self._segments]
        return self.__class__(self.name, new_segments, self.color)

    def set_segments(self, segments):
        # If the vector position is the same as another previously created
        # you can use just the first object instead of having multiple ones.

        cache_structural = dict()
        cache_projection = dict()

        def cache_it(vector):
            h = hash(vector)
            if h not in cache_structural:
                cache_structural[h] = vector
                cache_projection[h] = vector.copy()
            return h

        self._structural_points.clear()
        self._projection_points.clear()
        self._structural_segments.clear()
        self._projection_segments.clear()

        for a, b in segments:
            ha = cache_it(a)
            hb = cache_it(b)

            cached_a = cache_structural.get(ha)
            cached_b = cache_structural.get(hb)
            copied_a = cache_projection.get(ha)
            copied_b = cache_projection.get(hb)

            self._structural_segments.append((cached_a, cached_b))
            self._projection_segments.append((copied_a, copied_b))

        self._clipped_segments = self._projection_segments
        self._structural_points = list(cache_structural.values())
        self._projection_points = list(cache_projection.values())

    def clip(self, window_min, window_max):
        tmp_a = Vector(0)
        tmp_b = Vector(0)

        new_segments = []
        for a, b in self.projection_segments():
            tmp_a.x = a.x
            tmp_a.y = a.y
            tmp_a.z = a.z
            tmp_b.x = b.x
            tmp_b.y = b.y
            tmp_b.z = b.z

            should_plot = cohen_sutherland(tmp_a, tmp_b, window_min, window_max)
            # should_plot = liang_barsky(tmp_a, tmp_b, window_min, window_max)

            if should_plot:
                same_a = a == tmp_a
                same_b = b == tmp_b

                if same_a and same_b:
                    new_segments.append((a, b))
                elif same_a:
                    new_segments.append((a, tmp_b.copy()))
                elif same_b:
                    new_segments.append((tmp_a.copy(), b))

        self._clipped_segments = new_segments
        need_plot = len(new_segments) != 0
        return need_plot

    def revert_projection(self):
        structural = self.structural_points()
        projection = self.projection_points()
        self._clipped_segments = self._projection_segments
        for s, p in zip(structural, projection):
            x, y, z = s.get_pos()
            p.set_pos(x, y, z)
