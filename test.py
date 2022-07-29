from cProfile import Profile
from pstats import Stats
from numba import njit, prange

@njit
def collatz(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n /= 2
        else:
            n = 3*n + 1
        steps += 1
    return steps

@njit(parallel=True)
def sum_collatz(n):
    s = 0
    for i in prange(1, n):
        s += collatz(i)
    return s

test = lambda: sum_collatz(837799)

profiler = Profile()
profiler.runcall(test)

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()