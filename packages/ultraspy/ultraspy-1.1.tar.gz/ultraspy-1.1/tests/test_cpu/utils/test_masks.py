"""Unit test file for testing the way we build masks.
"""
import numpy as np

from ultraspy.utils import masks as masks_utils


def test_rectangular_mask():
    # Test a few masks with different locations
    x = np.arange(100)
    z = np.arange(100)

    # One within the area
    top_left = (25, 25)
    dims = (50, 50)
    m = masks_utils.create_rectangular_mask(top_left, dims, x, z)
    assert np.sum(~m) == np.prod(dims)

    # One outside
    top_left = (-20, -20)
    dims = (5, 5)
    m = masks_utils.create_rectangular_mask(top_left, dims, x, z)
    assert np.all(m)

    # In between
    top_left = (-10, -10)
    dims = (20, 20)
    m = masks_utils.create_rectangular_mask(top_left, dims, x, z)
    assert np.sum(~m) == np.prod([top_left[0] + dims[0], top_left[1] + dims[1]])


def test_circular_mask():
    # Test a few masks with different locations
    x = np.arange(100)
    z = np.arange(100)

    # One within the area
    center = (50, 50)
    radius = 10
    m = masks_utils.create_circular_mask(center, radius, x, z)
    assert np.abs(np.sum(~m) - np.pi * radius ** 2) < 5

    # One outside
    center = (-20, -20)
    radius = 10
    m = masks_utils.create_circular_mask(center, radius, x, z)
    assert np.all(m)

    # In between
    center = (50, 0)
    radius = 10
    m = masks_utils.create_circular_mask(center, radius, x, z)
    assert np.abs(np.sum(~m) - np.pi * radius ** 2 // 2 - radius) < 5
