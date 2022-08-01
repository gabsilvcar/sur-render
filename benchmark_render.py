from surrender.scene import Scene
from surrender.io.obj_io import OBJIO
from surrender.view import View
from surrender.vector import Vector
import numpy as np
from numba import njit

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


# arrays = [np.random.randint(-300, 300, (3,)) for _ in range(70_000)]
# vectors = [Vector(*i) for i in arrays]

# win, _ = create_views()
# win_min = np.asarray(win.min())
# win_max = np.asarray(win.max())

# def old_cs():
#     for a, b in zip(vectors, reversed(vectors)):
#         cohen_sutherland(a, b, win)

# def new_cs():
#     for a, b in zip(vectors, reversed(vectors)):
#         cohen_sutherland_(a, b, win.min(), win.max())

# import timeit

# t0 = timeit.Timer(old_cs).timeit(5)
# print('old', t0)

# t1 = timeit.Timer(new_cs).timeit(5)
# print('new', t1)


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