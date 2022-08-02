import numpy as np
from surrender.vector import Vector
from surrender.clipping import liang_barsky


class TestLiangBarsky:
    window_min = Vector(0, 0)
    window_max = Vector(400, 300)

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
            if liang_barsky(a, b, self.window_min, self.window_max):
                assert np.allclose(a, c, 0.001)
                assert np.allclose(b, d, 0.001)
            else:
                assert False

        a = Vector(-10, -10)
        b = Vector(-20, -20)
        assert not liang_barsky(a, b, self.window_min, self.window_max)
