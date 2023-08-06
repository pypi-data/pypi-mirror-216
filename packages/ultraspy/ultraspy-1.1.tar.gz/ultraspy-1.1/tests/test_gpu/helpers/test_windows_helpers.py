"""Unit test file for all the helpers used in windows functions.
"""
import pytest
import numpy as np

from ultraspy.helpers.windows_helpers import get_hamming_squared_kernel


def test_get_hamming_squared_kernel():
    # We test a few basic examples
    assert np.allclose(get_hamming_squared_kernel(3),
                       np.array([[0.0064, 0.08, 0.0064],
                                 [0.08,   1,    0.08],
                                 [0.0064, 0.08, 0.0064]]))
    assert pytest.approx(get_hamming_squared_kernel(9)[5, 1]) == 0.1858
    assert pytest.approx(get_hamming_squared_kernel(99)[52, 63]) == 0.8197917
