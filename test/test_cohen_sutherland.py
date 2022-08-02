import numpy as np
from surrender.vector import Vector
from surrender.clipping.cohen_sutherland import (
    LEFT,
    RIGHT,
    BOTTOM,
    UP,
    point_code,
    cohen_sutherland,
)


class TestCohenSutherland:
    window_min = Vector(0, 0)
    window_max = Vector(400, 300)

    def test_new_point_code(self):
        # fmt: off
        # These lines are a bit long, but it is more readable to not break apart
        assert point_code(Vector(100, 100), self.window_min, self.window_max) == 0
        assert point_code(Vector(-10, 100), self.window_min, self.window_max) == LEFT
        assert point_code(Vector(500, 100), self.window_min, self.window_max) == RIGHT
        assert point_code(Vector(100, -10), self.window_min, self.window_max) == BOTTOM
        assert point_code(Vector(100, 500), self.window_min, self.window_max) == UP
        assert point_code(Vector(-10, -10), self.window_min, self.window_max) == LEFT | BOTTOM
        assert point_code(Vector(500, 500), self.window_min, self.window_max) == RIGHT | UP
        # fmt: on

    def test_new_cohen_sutherland(self):
        inputs = [
            (Vector(20, 30), Vector(40, 50)),
            (Vector(-10, 30), Vector(500, 30)),
            (Vector(30, -10), Vector(30, 500)),
            (Vector(-10, 100), Vector(100, 500)),
            (Vector(100, -10), Vector(500, 100)),
        ]

        expected = [
            (Vector(20, 30), Vector(40, 50)),
            (Vector(0, 30), Vector(400, 30)),
            (Vector(30, 0), Vector(30, 300)),
            (Vector(0, 136.36), Vector(45, 300)),
            (Vector(136.36, 0), Vector(400, 72.50)),
        ]

        for (a, b), (c, d) in zip(inputs, expected):
            if cohen_sutherland(a, b, self.window_min, self.window_max):
                assert np.allclose(a, c, 0.001)
                assert np.allclose(b, d, 0.001)
            else:
                assert False

        a = Vector(-10, -10)
        b = Vector(-20, -20)
        assert not cohen_sutherland(a, b, self.window_min, self.window_max)
