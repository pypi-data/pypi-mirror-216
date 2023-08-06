"""Unit test file for the post-processing.
"""
import numpy as np

from ultraspy.cpu.post_processing import distort_dynamic


def test_distort_dynamic(big_array_2d_float):
    # Builds some b-mode image
    data = np.abs(big_array_2d_float)
    data = 20 * np.log10(data / np.max(data))
    dyn = -60

    # Basic curve
    distorted = distort_dynamic(data, 'curved', {'curve': 0.2}, dyn)
    assert np.all((dyn <= distorted) & (distorted <= 0))
    assert np.mean(data) > np.mean(distorted)
    distorted = distort_dynamic(data, 'curved', {'curve': 0.8}, dyn)
    assert np.mean(data) < np.mean(distorted)

    # Sigmoid
    distorted = distort_dynamic(
        data, 'sigmoid', {'steep': 1.5, 'offset': 0}, dyn)
    assert np.all((dyn < distorted) & (distorted < 0))
    distorted = distort_dynamic(
        data, 'sigmoid', {'steep': 1.5, 'offset': 4}, dyn)
    assert np.max(distorted) < 0
    distorted = distort_dynamic(
        data, 'sigmoid', {'steep': 1.5, 'offset': 4}, dyn, True)
    assert np.min(distorted) == dyn
    assert np.max(distorted) == 0
