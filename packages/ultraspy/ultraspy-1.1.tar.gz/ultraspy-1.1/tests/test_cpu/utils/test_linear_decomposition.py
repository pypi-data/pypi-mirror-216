"""Unit test file for testing the linear decomposition utilities methods.
TODO: Understand and test inverse of a
TODO: Understand and test b[0] = 0 constraint
"""
import numpy as np

from ultraspy.utils import linear_decomposition as linear_utils


def test_lu_decomposition_routines_basic():
    # Arguments, sparse simple matrix
    a = np.array([
        [9,  0,    0,    0,  0,    0],
        [0,  8.8,  0,    0,  0,   -0.4],
        [0,  0,    8.8,  0,  0.4,  0],
        [0,  0,    0,    1,  0,    0],
        [0,  0,    0.4,  0,  1.2,  0],
        [0, -0.4,  0,    0,  0,    1.2]])
    n = 6
    b = np.random.randn(n)
    b[0] = 0
    pivot_indexes = np.zeros(n)

    # LU Routine
    inv_a, pivot_indexes = linear_utils.ludcmp(a.flatten().copy(), n,
                                               pivot_indexes)
    x = linear_utils.lubksb(inv_a, n, pivot_indexes, b.copy())

    # We should have a . x = b
    assert np.allclose((a @ x)[1:], b[1:])


def test_lu_decomposition_routines_singular():
    # Arguments, the matrix is singular, this shouldn't work
    n = 5
    a = np.arange(n * n).reshape(n, n)
    b = np.random.randn(n)
    b[0] = 0
    pivot_indexes = np.zeros(n)

    # LU Routine
    inv_a, pivot_indexes = linear_utils.ludcmp(a.flatten().copy(), n,
                                               pivot_indexes)
    x = linear_utils.lubksb(inv_a, n, pivot_indexes, b.copy())

    # We should have a . x != b
    assert np.any((a @ x)[1:] != b[1:])


def test_lu_decomposition_routines_random_non_singular():
    # Arguments, the matrix is not singular, but is randomly generated
    n = np.random.randint(1, 100)
    a = np.arange(n * n).reshape(n, n) + np.identity(n)
    b = np.random.randn(n)
    b[0] = 0
    pivot_indexes = np.zeros(n)

    # LU Routine
    inv_a, pivot_indexes = linear_utils.ludcmp(a.flatten().copy(), n,
                                               pivot_indexes)
    x = linear_utils.lubksb(inv_a, n, pivot_indexes, b.copy())

    # We should have a . x = b
    assert np.allclose((a @ x)[1:], b[1:])
