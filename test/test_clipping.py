import numpy as np
from surrender.vector import Vector, vector
from surrender.view import View
from surrender.clipping import (
    LEFT, 
    RIGHT, 
    BOTTOM, 
    UP,

    point_code,
    cohen_sutherland,

    point_code_,
    cohen_sutherland_,
)


class TestCohenSutherland:
    w = 400
    h = 300

    window = View(
        Vector(0, h),
        Vector(w, h),
        Vector(w, 0),
        Vector(0, 0),
    )

    def test_point_code(self):
        assert point_code(Vector(100, 100), self.window) == 0
        assert point_code(Vector(-10, 100), self.window) == LEFT
        assert point_code(Vector(500, 100), self.window) == RIGHT
        assert point_code(Vector(100, -10), self.window) == BOTTOM
        assert point_code(Vector(100, 500), self.window) == UP
        assert point_code(Vector(-10, -10), self.window) == LEFT | BOTTOM
        assert point_code(Vector(500, 500), self.window) == RIGHT | UP
    
    def vectors_assertion(self, a, b, a_expected, b_expected):
        opt1 = ((a.x == a_expected.x)
               and (a.y == a_expected.y)
               and (b.x == b_expected.x)
               and (b.y == b_expected.y))

        opt2 = ((a.x == b_expected.x)
               and (a.y == b_expected.y)
               and (b.x == a_expected.x)
               and (b.y == a_expected.y))

        assert opt1 or opt2

    def test_cohen_sutherland(self):
        s, e  = cohen_sutherland(Vector(20, 30), Vector(40, 50), self.window)
        assert (s.x == 20) and (s.y == 30) 
        assert (e.x == 40) and (e.y == 50)

        s, e  = cohen_sutherland(Vector(-10, 30), Vector(500, 30), self.window)
        assert (s.x == 0) and (s.y == 30) 
        assert (e.x == 400) and (e.y == 30)

        s, e  = cohen_sutherland(Vector(30, -10), Vector(30, 500), self.window)
        assert (s.x == 30) and (s.y == 300) 
        assert (e.x == 30) and (e.y == 0)

        s, e  = cohen_sutherland(Vector(-10, 100), Vector(100, 500), self.window)
        assert (s.x == 0) and (int(s.y) == 136) 
        assert (e.x == 45) and (e.y == 300)

        s, e  = cohen_sutherland(Vector(100, -10), Vector(500, 100), self.window)
        assert (s.x == 400) and (int(s.y) == 72) 
        assert (int(e.x) == 136) and (e.y == 0)

        r = cohen_sutherland(Vector(-10, -10), Vector(-20, -20), self.window)
        assert r is None

class TestNewCohenSutherland:
    window_min = vector(0, 0)
    window_max = vector(400, 300)

    def test_new_point_code(self):
        assert point_code_(vector(100, 100), self.window_min, self.window_max) == 0
        assert point_code_(vector(-10, 100), self.window_min, self.window_max) == LEFT
        assert point_code_(vector(500, 100), self.window_min, self.window_max) == RIGHT
        assert point_code_(vector(100, -10), self.window_min, self.window_max) == BOTTOM
        assert point_code_(vector(100, 500), self.window_min, self.window_max) == UP
        assert point_code_(vector(-10, -10), self.window_min, self.window_max) == LEFT | BOTTOM
        assert point_code_(vector(500, 500), self.window_min, self.window_max) == RIGHT | UP

    def test_new_cohen_sutherland(self):
        inputs = [
            (vector( 20,  30), vector( 40, 50)),
            (vector(-10,  30), vector(500, 30)),
            (vector( 30, -10), vector( 30, 500)),
            (vector(-10, 100), vector(100, 500)),
            (vector(100, -10), vector(500, 100)),
        ]

        expected = [
            (vector(20,  30), vector(40,  50)),
            (vector(0,   30), vector(400, 30)),
            (vector(30,   0), vector(30, 300)),
            (vector(0,  136), vector(45, 300)),
            (vector(136,  0), vector(400, 72)),
        ]

        for (a, b), (c, d) in zip(inputs, expected):
            if cohen_sutherland_(a, b, self.window_min, self.window_max):
                assert np.array_equal(a, c)
                assert np.array_equal(b, d)
            else:
                assert False

        a = vector(-10, -10)
        b = vector(-20, -20)
        assert not cohen_sutherland_(a, b, self.window_min, self.window_max)
