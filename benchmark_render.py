from surrender.scene import Scene
from surrender.io.obj_io import OBJIO
from surrender.view import View
from surrender.vector import Vector
import numpy as np
from numba import njit
import timeit

from cProfile import Profile
from pstats import Stats


def create_scene():
    scene = Scene()
    for shape in OBJIO.read('resources/bowler.obj'):
        scene.add_shape(shape)
    return scene

def create_views():
    w = 400
    h = 300
    b = 10

    origin = View(
        Vector(0, h),
        Vector(w, h),
        Vector(w, 0),
        Vector(0, 0),
    )

    target = View(
        Vector(0 + b, h - b),
        Vector(w - b, h - b),
        Vector(w - b, 0 + b),
        Vector(0 + b, 0 + b),
    )

    return origin, target

def profile():
    scene = create_scene()
    origin, target = create_views()
    # scene.projected_shapes(origin, target)

    test = lambda: scene.projected_shapes(origin, target)

    profiler = Profile()
    profiler.runcall(test)

    stats = Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats()
    # stats.print_callers()

def tests():
    n = 100_000

    def helper(a, b, c):
        return a * a + b * b + c * c

    def indirect():
        s = 0
        for i in range(n):
            a = i
            b = 2 * i
            c = 3 * i
            s += helper(a, b, c)

    def direct():
        s = 0
        for i in range(n):
            a = i
            b = 2 * i
            c = 3 * i
            s += a * a + b * b + c * c

    t1 = timeit.Timer(direct).timeit(10)
    print('direct', t1)
    
    t0 = timeit.Timer(indirect).timeit(10)
    print('indirect', t0)


tests()