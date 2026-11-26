import numpy as np

from ssa_toolkit.propagate import chunk_bounds, chunk_grid


def test_chunk_bounds():
    a = chunk_bounds(23, 5)
    b = chunk_bounds(12, 4)
    a_sum = 0
    for start, size in a:
        assert size >= 1
        a_sum += size
    for start, size in b:
        assert size >= 1
        b_sum += size
    assert a_sum == 23
    assert b_sum == 12
    assert a == [(0, 5), (5, 5), (10, 5), (15, 5), (20, 3)]
    assert b == [(0, 4), (4, 4), (8, 4)]


def test_chunk_grid():
    a = chunk_bounds(23, 5)
    pieces = []
    for start, size in a:
        _jd, frs = chunk_grid(2459731.5, 0.25, start, size, 60)
        pieces.append(frs)
    joined_pieces = np.concatenate(pieces)
    _jd, whole_frs = chunk_grid(2459731.5, 0.25, 0, 23, 60)
    assert np.array_equal(whole_frs, joined_pieces)
