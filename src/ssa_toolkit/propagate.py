import resource
import time

import numpy as np


def chunk_bounds(total, chunk):
    out = []
    for i in range(0, total, chunk):
        out.append((i, min(chunk, total - i)))
    return out


def chunk_grid(jd0, fr0, start, size, step_s):
    jds = np.full(size, jd0)
    steps = np.arange(start, start + size)
    frs = fr0 + (steps * step_s) / 86400
    return (jds, frs)


def propagate_chunked(arr, jd0, fr0, n_steps, step_s, chunk_steps):
    count = 0
    t0 = time.perf_counter()
    for start, size in chunk_bounds(n_steps, chunk_steps):
        jds, frs = chunk_grid(jd0, fr0, start, size, step_s)
        e, _r, _v = arr.sgp4(jds, frs)
        count += int(np.count_nonzero(e))

    elapsed = time.perf_counter() - t0
    peak_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024

    return (count, elapsed, peak_mb)
